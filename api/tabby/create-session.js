const crypto = require('crypto');
const catalog = require('../../3d/assets/data/3d-products.json');

const TABBY_API = 'https://api.tabby.ai/api/v2';
const SITE = process.env.VERCEL_ENV === 'production' || !process.env.VERCEL_URL
  ? 'https://www.blackarrowksa.com'
  : 'https://' + process.env.VERCEL_URL;
const MAX_LINES = 20;
const MAX_QTY = 10;
// Limits to confirm with Tabby for your account before going live.
const MIN_SAR = 75;
const MAX_SAR = 10000;

function unitPrice(product, variantIndex) {
  if (product.variants && product.variants.length) {
    const v = product.variants[variantIndex];
    if (!v || v.available === false) return null;
    return v.price;
  }
  if (product.available === false) return null;
  return product.onSale && product.salePrice != null ? product.salePrice : product.price;
}

function priceCart(items) {
  if (!Array.isArray(items) || items.length === 0 || items.length > MAX_LINES) return null;
  const byId = new Map(catalog.products.map((p) => [p.id, p]));
  const lines = [];
  let total = 0;
  for (const item of items) {
    const product = byId.get(item && item.productId);
    const qty = Number(item && item.qty);
    if (!product || !Number.isInteger(qty) || qty < 1 || qty > MAX_QTY) return null;
    const variantIndex = item.variantIndex == null ? null : Number(item.variantIndex);
    if (product.variants && product.variants.length && variantIndex == null) return null;
    const unit = unitPrice(product, variantIndex == null ? 0 : variantIndex);
    if (unit == null) return null;
    const cents = Math.round(unit * 100);
    lines.push({ title: product.name, unit_price: (cents / 100).toFixed(2), quantity: qty, reference_id: product.id });
    total += cents * qty;
  }
  return { lines, total_cents: total };
}

function cleanBilling(b) {
  const s = (v, max) => String(v || '').trim().slice(0, max);
  const phone = s(b && b.phone, 20);
  const email = s(b && b.email, 120);
  const firstName = s(b && b.firstName, 60);
  const lastName = s(b && b.lastName, 60);
  if (!phone || !firstName || !lastName || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return null;
  return {
    name: (firstName + ' ' + lastName).slice(0, 120),
    email,
    phone,
    city: s(b.city, 60) || 'NA',
    address: [s(b.street, 120), s(b.building, 20), s(b.apartment, 40)].filter(Boolean).join(', ') || 'NA',
    zip: s(b.postalCode, 20) || '00000',
  };
}

async function supabase(method, path, body, prefer) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error('supabase_not_configured');
  const headers = { apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' };
  if (prefer) headers.Prefer = prefer;
  const r = await fetch(url + '/rest/v1/' + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (!r.ok) throw new Error('supabase_' + r.status);
  return r;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }

  const secret = process.env.TABBY_SECRET_KEY;
  const merchantCode = process.env.TABBY_MERCHANT_CODE;
  if (!secret || !merchantCode) return res.status(500).json({ error: 'payment_not_configured' });

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  const priced = priceCart(body.items);
  if (!priced) return res.status(400).json({ error: 'invalid_cart' });
  const shippingCents = body.shipping === 'fast' ? 5000 : body.shipping === 'regular' ? 3000 : null;
  if (shippingCents == null) return res.status(400).json({ error: 'invalid_shipping' });
  priced.lines.push({ title: body.shipping === 'fast' ? 'Fast shipping' : 'Regular shipping', unit_price: (shippingCents / 100).toFixed(2), quantity: 1, reference_id: 'shipping-' + body.shipping });
  priced.total_cents += shippingCents;

  const totalSar = priced.total_cents / 100;
  if (totalSar < MIN_SAR || totalSar > MAX_SAR) return res.status(400).json({ error: 'amount_out_of_range' });

  const buyer = cleanBilling(body.billing);
  if (!buyer) return res.status(400).json({ error: 'invalid_billing' });

  const orderRef = crypto.randomBytes(12).toString('hex');
  const amount = totalSar.toFixed(2);

  const payload = {
    payment: {
      amount,
      currency: 'SAR',
      description: 'Black Arrow 3D order',
      buyer: { name: buyer.name, email: buyer.email, phone: buyer.phone },
      shipping_address: { city: buyer.city, address: buyer.address, zip: buyer.zip },
      order: {
        reference_id: orderRef,
        items: priced.lines,
        shipping_amount: (shippingCents / 100).toFixed(2),
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
    await supabase('POST', 'tabby_orders', {
      order_ref: orderRef,
      status: 'pending',
      amount_cents: priced.total_cents,
      currency: 'SAR',
      items: priced.lines,
    });
  } catch (e) {
    console.error('tabby_orders insert failed:', e.message);
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
    if (!r.ok || !data.payment || !data.payment.id || !webUrl) {
      console.error('tabby checkout rejected:', r.status, JSON.stringify(data).slice(0, 300));
      return res.status(502).json({ error: 'gateway_rejected' });
    }
    await supabase('PATCH', 'tabby_orders?order_ref=eq.' + orderRef, { tabby_payment_id: data.payment.id });
    return res.status(200).json({ orderRef, amount_sar: totalSar, checkoutUrl: webUrl });
  } catch (e) {
    console.error('tabby checkout failed:', e.message);
    return res.status(502).json({ error: 'gateway_unreachable' });
  }
};
