const crypto = require('crypto');
const catalog = require('../../3d/assets/data/3d-products.json');

const PAYMOB_BASE = 'https://ksa.paymob.com';
const SITE = process.env.VERCEL_ENV === 'production' || !process.env.VERCEL_URL
  ? 'https://www.blackarrowksa.com'
  : 'https://' + process.env.VERCEL_URL;
const MAX_LINES = 20;
const MAX_QTY = 10;

function unitPrice(product, variantIndex) {
  if (product.variants && product.variants.length) {
    const v = product.variants[variantIndex];
    if (!v) return null;
    if (v.available === false) return null;
    return v.price;
  }
  if (product.available === false) return null;
  return product.onSale && product.salePrice != null ? product.salePrice : product.price;
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
    lines.push({ name: product.name, amount_cents: Math.round(unit * 100), quantity: qty });
    total += Math.round(unit * 100) * qty;
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
    building: na,
    floor: na,
    apartment: na,
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
  if (!secret || !publicKey || !integrationId) {
    return res.status(500).json({ error: 'payment_not_configured' });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  const priced = priceCart(body.items);
  if (!priced) return res.status(400).json({ error: 'invalid_cart' });
  const shippingCents = body.shipping === 'fast' ? 5000 : body.shipping === 'regular' ? 3000 : null;
  if (shippingCents == null) return res.status(400).json({ error: 'invalid_shipping' });
  priced.lines.push({ name: body.shipping === 'fast' ? 'Fast shipping' : 'Regular shipping', amount_cents: shippingCents, quantity: 1 });
  priced.total_cents += shippingCents;

  const billing = cleanBilling(body.billing);
  if (!billing) return res.status(400).json({ error: 'invalid_billing' });

  const orderRef = crypto.randomBytes(12).toString('hex');

  const intentionBody = {
    amount: priced.total_cents,
    currency: 'SAR',
    payment_methods: [integrationId],
    items: priced.lines.map((l) => ({ name: l.name, amount: l.amount_cents, quantity: l.quantity, description: l.name })),
    billing_data: billing,
    special_reference: orderRef,
    notification_url: SITE + '/api/paymob/webhook',
    redirection_url: SITE + '/3d/cart/?paid=' + orderRef,
  };

  try {
    await supabase('POST', 'card_orders', {
      order_ref: orderRef,
      status: 'pending',
      amount_cents: priced.total_cents,
      currency: 'SAR',
      items: priced.lines,
      billing: { first_name: billing.first_name, last_name: billing.last_name, email: billing.email, phone_number: billing.phone_number, city: billing.city, street: billing.street },
    });
  } catch (e) {
    console.error('card_orders insert failed:', e.message);
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
      return res.status(502).json({ error: 'gateway_rejected' });
    }
    await supabase('PATCH', 'card_orders?order_ref=eq.' + orderRef, { paymob_intention_id: String(intention.id || '') });
  } catch (e) {
    return res.status(502).json({ error: 'gateway_unreachable' });
  }

  return res.status(200).json({
    orderRef,
    amount_sar: priced.total_cents / 100,
    checkoutUrl: PAYMOB_BASE + '/unifiedcheckout/?publicKey=' + encodeURIComponent(publicKey) + '&clientSecret=' + encodeURIComponent(intention.client_secret),
  });
};
