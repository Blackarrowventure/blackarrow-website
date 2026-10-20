// A bank transfer order, sent by the cart once its order email has gone out, so it also lands in
// the CRM's Online Orders inbox (as not paid yet). Prices and delivery are recomputed from the
// live catalog; only the discount comes from the browser (coupon / rewards it already applied),
// capped at the items total. Nothing here holds stock or touches the accounts: the order just
// waits in the CRM until it is confirmed (as an Unpaid invoice) or rejected.
const { buildOrder } = require('./_lib/pricing');
const { liveProducts } = require('./_lib/crm-catalog');
const { crmDetails, sendBankOrder } = require('./_lib/crm-orders');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  let body;
  try {
    body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  } catch (e) {
    return res.status(400).json({ error: 'invalid_json' });
  }

  const orderId = String(body.orderId || '').trim();
  if (!/^[A-Za-z0-9-]{3,40}$/.test(orderId)) return res.status(400).json({ error: 'invalid_order_id' });

  const s = (v, max) => String(v || '').trim().slice(0, max);
  const b = body.billing || {};
  const name = (s(b.firstName, 60) + ' ' + s(b.lastName, 60)).trim();
  const phone = s(b.phone, 20);
  if (!name || !phone) return res.status(400).json({ error: 'invalid_billing' });

  const products = await liveProducts();
  const order = buildOrder(body.items, body.shipping, false, null, products);
  if (order.error) return res.status(400).json({ error: order.error });

  const num = (v) => (Number.isFinite(Number(v)) && Number(v) > 0 ? Number(v) : 0);
  const discountCents = Math.min(Math.round((num(body.couponDiscount) + num(body.rewardsUsed)) * 100), order.itemsCents);
  // Gold/Platinum members get free Regular delivery in the cart; accept a lower delivery than the
  // standard price, never a higher one.
  const shippingCents = Math.min(Math.round(num(body.shippingPrice) * 100), order.shippingCents);
  // Bank transfer saving: 1% off the items after coupon / rewards (the cart shows the same).
  const savingCents = Math.round((order.itemsCents - discountCents) * 0.01);
  const totalCents = order.itemsCents - discountCents - savingCents + shippingCents;

  const details = crmDetails(Object.assign({}, order, { discountCents: discountCents + savingCents, shippingCents, totalCents, feeCents: 0 }));
  const notes = [];
  if (body.couponCode) notes.push('Coupon ' + s(body.couponCode, 40) + ': -' + num(body.couponDiscount) + ' SAR');
  if (num(body.rewardsUsed)) notes.push('Loyalty Rewards used: -' + num(body.rewardsUsed) + ' SAR');
  if (savingCents) notes.push('Bank transfer saving (1%): -' + (savingCents / 100) + ' SAR');
  notes.push('Bank transfer: check the amount reached the bank before marking the invoice Paid.');

  try {
    await sendBankOrder(Object.assign(details, {
      order_ref: orderId,
      source: 'bank',
      method_label: 'Bank Transfer',
      payment_method: 'Bank transfer',
      paid: false,
      customer_name: name,
      customer_phone: phone,
      customer_email: s(b.email, 120),
      customer_city: s(b.city, 60),
      customer_address: [s(b.street, 120), s(b.building, 20), s(b.apartment, 40), s(b.postalCode, 20)].filter(Boolean).join(', '),
      discount_note: discountCents + savingCents ? notes.slice(0, -1).join(' · ') : null,
      notes: notes.join(' · '),
    }));
  } catch (e) {
    console.error('bank-order: CRM inbox failed', orderId, e.message, e.detail || '');
    return res.status(502).json({ error: 'crm_unavailable' });
  }
  return res.status(200).json({ ok: true });
};
