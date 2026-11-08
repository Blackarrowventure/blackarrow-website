const crypto = require('crypto');
const { buildOrder, stockProblem } = require('../_lib/pricing');
const { insertOrder, db, nextOrderId } = require('../_lib/db');
const rewards = require('../_lib/rewards');
const { liveProducts } = require('../_lib/crm-catalog');
const { crmDetails } = require('../_lib/crm-orders');

const TABBY_API = 'https://api.tabby.ai/api/v2';
const SITE = process.env.VERCEL_ENV === 'production' || !process.env.VERCEL_URL
  ? 'https://www.blackarrowksa.com'
  : 'https://' + process.env.VERCEL_URL;
// No order-amount limit of our own (5 Nov 2026): the 75-10,000 SAR range that used to be here was a
// placeholder never confirmed with Tabby. Tabby decides per account and per customer, and a refusal
// comes back as status "rejected", which is reported to the shopper as tabby_rejected below.

function cleanBilling(b) {
  const s = (v, max) => String(v || '').trim().slice(0, max);
  const phone = s(b && b.phone, 20);
  const email = s(b && b.email, 120);
  const firstName = s(b && b.firstName, 60);
  const lastName = s(b && b.lastName, 60);
  if (!phone || !firstName || !lastName || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return null;
  return {
    firstName,
    lastName,
    name: (firstName + ' ' + lastName).slice(0, 120),
    email,
    phone,
    city: s(b.city, 60) || 'NA',
    street: s(b.street, 120),
    building: s(b.building, 20),
    apartment: s(b.apartment, 40),
    address: [s(b.street, 120), s(b.building, 20), s(b.apartment, 40)].filter(Boolean).join(', ') || 'NA',
    zip: s(b.postalCode, 20) || '00000',
  };
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }

  const secret = process.env.TABBY_SECRET_KEY;
  const merchantCode = process.env.TABBY_MERCHANT_CODE;
  if (!secret || !merchantCode) return res.status(500).json({ error: 'payment_not_configured' });

  let body;
  try {
    body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  } catch (e) {
    return res.status(400).json({ error: 'invalid_json' });
  }
  // Stock and prices as set in the CRM's Website Inventory tab. Refuse rather than price against
  // stale/default stock if the CRM can't be reached right now.
  let products;
  try {
    products = await liveProducts();
  } catch (e) {
    return res.status(503).json({ error: 'crm_unavailable' });
  }
  const draft = buildOrder(body.items, body.shipping, true, null, products, body.billing && body.billing.city);
  if (draft.error) return res.status(400).json({ error: draft.error });
  const short = stockProblem(body.items, products);
  if (short) return res.status(409).json({ error: 'not_enough_stock', item: short.name, max: short.max });
  const rw = await rewards.checkoutRewards(body.authToken, body.useRewards === true, draft.itemsCents);
  const order = buildOrder(body.items, body.shipping, true, rw, products, body.billing && body.billing.city);

  const totalSar = order.totalCents / 100;
  if (!(totalSar > 0)) return res.status(400).json({ error: 'amount_out_of_range' });

  const buyer = cleanBilling(body.billing);
  if (!buyer) return res.status(400).json({ error: 'invalid_billing' });

  const orderRef = crypto.randomBytes(12).toString('hex');
  // A friendly number for display only (emails, thank-you page, CRM) - the random orderRef above
  // stays what Tabby, verify and the return URL use.
  const orderNumber = await nextOrderId();
  const money = (c) => (c / 100).toFixed(2);

  const tabbyItems = order.lines.map((l) => ({ title: l.name, unit_price: money(l.unitCents), quantity: l.qty, reference_id: l.id }));
  if (order.feeCents) tabbyItems.push({ title: 'Pay-later service fee', unit_price: money(order.feeCents), quantity: 1, reference_id: 'pay-later-fee' });

  const payload = {
    payment: {
      amount: totalSar.toFixed(2),
      currency: 'SAR',
      description: 'Black Arrow 3D order ' + orderNumber,
      buyer: { name: buyer.name, email: buyer.email, phone: buyer.phone },
      shipping_address: { city: buyer.city, address: buyer.address, zip: buyer.zip },
      order: {
        reference_id: orderRef,
        items: tabbyItems,
        shipping_amount: money(order.shippingCents),
        discount_amount: money(order.discountCents),
        tax_amount: '0.00',
      },
    },
    lang: body.lang === 'ar' ? 'ar' : 'en',
    merchant_code: merchantCode,
    merchant_urls: {
      success: SITE + '/3d/cart/?tabby=' + orderRef,
      cancel: SITE + '/3d/cart/?tabby_cancelled=1',
      failure: SITE + '/3d/cart/?tabby_failed=1',
    },
  };

  try {
    await insertOrder('tabby_orders', {
      order_ref: orderRef,
      status: 'pending',
      amount_cents: order.totalCents,
      currency: 'SAR',
      items: tabbyItems,
    }, {
      details: {
        method: 'Tabby (Pay in 4)',
        order_number: orderNumber,
        lang: body.lang === 'ar' ? 'ar' : 'en',
        billing: {
          first_name: buyer.firstName, last_name: buyer.lastName, email: buyer.email, phone: buyer.phone,
          city: buyer.city, street: buyer.street, building: buyer.building, apartment: buyer.apartment, postal_code: buyer.zip,
        },
        summary: order.summary,
        shipping_label: order.shippingLabel,
        rewards: order.discountCents ? { phone: rw.phone, discount_cents: order.discountCents } : null,
        crm: crmDetails(order),
      },
    });
  } catch (e) {
    console.error('tabby_orders insert failed:', e.message, e.body || '');
    return res.status(502).json({ error: 'order_store_unavailable' });
  }

  let data;
  try {
    const r = await fetch(TABBY_API + '/checkout', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + secret, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const text = await r.text();
    try {
      data = JSON.parse(text);
    } catch (e) {
      console.error('tabby non-json reply:', r.status, text.slice(0, 200));
      return res.status(502).json({ error: 'gateway_rejected' });
    }
    const webUrl = data && data.configuration && data.configuration.available_products
      && data.configuration.available_products.installments
      && data.configuration.available_products.installments[0]
      && data.configuration.available_products.installments[0].web_url;
    if (data && data.status === 'rejected') {
      // Tabby declined this order (e.g. amount above/below what it allows, or the shopper is not eligible).
      const reason = (data.configuration && data.configuration.products && data.configuration.products.installments
        && data.configuration.products.installments.rejection_reason) || 'not_available';
      console.warn('tabby rejected order', orderRef, reason);
      return res.status(422).json({ error: 'tabby_rejected', reason });
    }
    if (!r.ok || !data.payment || !data.payment.id || !webUrl) {
      console.error('tabby checkout rejected:', r.status, JSON.stringify(data).slice(0, 300));
      return res.status(502).json({ error: 'gateway_rejected' });
    }
    await db('PATCH', 'tabby_orders?order_ref=eq.' + orderRef, { tabby_payment_id: data.payment.id }, 'return=minimal');
    return res.status(200).json({ orderRef, orderNumber, amount_sar: totalSar, rewards_used_sar: order.discountCents / 100, checkoutUrl: webUrl });
  } catch (e) {
    console.error('tabby checkout failed:', e.message);
    return res.status(502).json({ error: 'gateway_unreachable' });
  }
};
