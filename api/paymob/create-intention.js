const crypto = require('crypto');
const { buildOrder } = require('../_lib/pricing');
const { insertOrder, db } = require('../_lib/db');
const rewards = require('../_lib/rewards');
const { liveProducts } = require('../_lib/crm-catalog');

const PAYMOB_BASE = 'https://ksa.paymob.com';
const SITE = process.env.VERCEL_ENV === 'production' || !process.env.VERCEL_URL
  ? 'https://www.blackarrowksa.com'
  : 'https://' + process.env.VERCEL_URL;

function cleanBilling(b) {
  const s = (v, max) => String(v || '').trim().slice(0, max);
  const phone = s(b && b.phone, 20);
  const email = s(b && b.email, 120);
  const firstName = s(b && b.firstName, 60);
  const lastName = s(b && b.lastName, 60);
  if (!phone || !firstName || !lastName || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return null;
  const na = 'NA';
  return {
    first_name: firstName,
    last_name: lastName,
    email,
    phone_number: phone,
    city: s(b.city, 60) || na,
    country: 'SA',
    state: s(b.state, 60) || na,
    street: s(b.street, 120) || na,
    building: s(b.building, 20) || na,
    floor: na,
    apartment: s(b.apartment, 40) || na,
    postal_code: s(b.postalCode, 20) || na,
  };
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }

  const secret = process.env.PAYMOB_SECRET_KEY;
  const publicKey = process.env.PAYMOB_PUBLIC_KEY;
  const integrationId = Number(process.env.PAYMOB_INTEGRATION_ID);
  const applePayIntegrationId = Number(process.env.PAYMOB_INTEGRATION_ID_APPLEPAY) || null;
  const tamaraIntegrationId = Number(process.env.PAYMOB_INTEGRATION_ID_TAMARA) || null;
  if (!secret || !publicKey || !integrationId) {
    const missing = [
      !secret && 'PAYMOB_SECRET_KEY',
      !publicKey && 'PAYMOB_PUBLIC_KEY',
      !integrationId && 'PAYMOB_INTEGRATION_ID',
    ].filter(Boolean);
    return res.status(500).json({ error: 'payment_not_configured', missing });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};

  // 'card' (the default) is the card/mada checkout, with Apple Pay offered
  // alongside it when configured. 'tamara' is its own buy-now-pay-later checkout.
  const channel = body.channel === 'tamara' ? 'tamara' : 'card';
  let paymentMethods;
  if (channel === 'tamara') {
    if (!tamaraIntegrationId) {
      return res.status(500).json({ error: 'payment_not_configured', missing: ['PAYMOB_INTEGRATION_ID_TAMARA'] });
    }
    paymentMethods = [tamaraIntegrationId];
  } else {
    paymentMethods = [integrationId].concat(applePayIntegrationId ? [applePayIntegrationId] : []);
  }

  // Rewards need the customer's real items total first, then the final order.
  // Stock and prices as set in the CRM's Website Inventory tab.
  const products = await liveProducts();
  const draft = buildOrder(body.items, body.shipping, channel === 'tamara', null, products);
  if (draft.error) return res.status(400).json({ error: draft.error });
  const rw = await rewards.checkoutRewards(body.authToken, body.useRewards === true, draft.itemsCents);
  const order = buildOrder(body.items, body.shipping, channel === 'tamara', rw, products);

  const billing = cleanBilling(body.billing);
  if (!billing) return res.status(400).json({ error: 'invalid_billing' });

  const orderRef = crypto.randomBytes(12).toString('hex');
  const method = channel === 'tamara' ? 'Tamara (Pay Later)' : 'Card (Paymob)';

  // Paymob wants the item lines to add up to the amount. With a rewards
  // discount there is no negative line it accepts, so the order goes as one
  // line; the itemised order stays in our own records and emails.
  let paymobItems;
  if (order.discountCents) {
    paymobItems = [{ name: 'Black Arrow 3D order ' + orderRef.slice(0, 8) + ' (rewards applied)', amount: order.totalCents, quantity: 1, description: 'Black Arrow 3D order' }];
  } else {
    paymobItems = order.lines.map((l) => ({ name: l.name, amount: l.unitCents, quantity: l.qty, description: l.name }));
    paymobItems.push({ name: order.shippingLabel, amount: order.shippingCents, quantity: 1, description: order.shippingLabel });
    if (order.feeCents) paymobItems.push({ name: 'Pay-later service fee', amount: order.feeCents, quantity: 1, description: 'Pay-later service fee' });
  }

  const intentionBody = {
    amount: order.totalCents,
    currency: 'SAR',
    payment_methods: paymentMethods,
    items: paymobItems,
    billing_data: billing,
    special_reference: orderRef,
    notification_url: SITE + '/api/paymob/webhook',
    redirection_url: SITE + '/3d/cart/?paid=' + orderRef + (channel === 'tamara' ? '&pm=tamara' : ''),
  };

  try {
    await insertOrder('card_orders', {
      order_ref: orderRef,
      status: 'pending',
      amount_cents: order.totalCents,
      currency: 'SAR',
      items: order.lines.map((l) => ({ name: l.name, amount_cents: l.unitCents, quantity: l.qty })),
      billing: { first_name: billing.first_name, last_name: billing.last_name, email: billing.email, phone_number: billing.phone_number, city: billing.city, street: billing.street },
    }, {
      details: {
        method,
        lang: body.lang === 'ar' ? 'ar' : 'en',
        billing: {
          first_name: billing.first_name, last_name: billing.last_name, email: billing.email, phone: billing.phone_number,
          city: billing.city, street: billing.street, building: billing.building, apartment: billing.apartment, postal_code: billing.postal_code,
        },
        summary: order.summary,
        shipping_label: order.shippingLabel,
        rewards: order.discountCents ? { phone: rw.phone, discount_cents: order.discountCents } : null,
      },
    });
  } catch (e) {
    console.error('card_orders insert failed:', e.message, e.body || '');
    return res.status(502).json({ error: 'order_store_unavailable' });
  }

  let intention;
  try {
    const r = await fetch(PAYMOB_BASE + '/v1/intention/', {
      method: 'POST',
      headers: { Authorization: 'Token ' + secret, 'Content-Type': 'application/json' },
      body: JSON.stringify(intentionBody),
    });
    intention = await r.json();
    if (!r.ok || !intention.client_secret) {
      console.error('paymob intention rejected:', channel, r.status, JSON.stringify(intention).slice(0, 1000));
      const out = { error: 'gateway_rejected' };
      if (body.debug === true) out.detail = intention;
      return res.status(502).json(out);
    }
    await db('PATCH', 'card_orders?order_ref=eq.' + orderRef, { paymob_intention_id: String(intention.id || '') }, 'return=minimal');
  } catch (e) {
    return res.status(502).json({ error: 'gateway_unreachable' });
  }

  return res.status(200).json({
    orderRef,
    amount_sar: order.totalCents / 100,
    rewards_used_sar: order.discountCents / 100,
    checkoutUrl: PAYMOB_BASE + '/unifiedcheckout/?publicKey=' + encodeURIComponent(publicKey) + '&clientSecret=' + encodeURIComponent(intention.client_secret),
  });
};
