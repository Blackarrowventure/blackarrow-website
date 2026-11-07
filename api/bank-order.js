// A bank transfer order, sent by the cart once its order email has gone out, so it also lands in
// the CRM's Online Orders inbox (as not paid yet). Prices and delivery are recomputed from the
// live catalog. The coupon and the rewards balance the cart already used are checked here, not
// taken from the browser: the coupon by its redemption, the rewards by what the CRM recorded as
// spent on this order; member free delivery by the signed-in account. Anything that cannot be
// checked is flagged in the order notes. The order waits in the CRM until it is confirmed (as an
// Unpaid invoice) or rejected.
const { buildOrder, stockProblem } = require('./_lib/pricing');
const { liveProducts } = require('./_lib/crm-catalog');
const { crmDetails, sendBankOrder } = require('./_lib/crm-orders');
const rewards = require('./_lib/rewards');
const { db, rateHit, clientIp } = require('./_lib/db');

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

  // Flood guard: 5 bank-transfer orders per visitor per hour, 100 a day in total.
  if (!(await rateHit('bank-order:' + clientIp(req), 5, '1 hour')) || !(await rateHit('bank-order:all', 100, '1 day'))) {
    return res.status(429).json({ error: 'too_many_orders' });
  }

  const s = (v, max) => String(v || '').trim().slice(0, max);
  const b = body.billing || {};
  const name = (s(b.firstName, 60) + ' ' + s(b.lastName, 60)).trim();
  const phone = s(b.phone, 20);
  if (!name || !phone) return res.status(400).json({ error: 'invalid_billing' });

  const num = (v) => (Number.isFinite(Number(v)) && Number(v) > 0 ? Number(v) : 0);
  const checks = [];
  // Cash is only for self pickup (paid when the customer collects); it gets the same saving.
  const cash = body.payment === 'cash';
  if (cash && body.shipping !== 'pickup') return res.status(400).json({ error: 'cash_pickup_only' });

  // Signed-in member: Gold / Platinum free Regular delivery comes from their account.
  let member = null;
  if (body.authToken && rewards.configured()) {
    try {
      const m = await rewards.memberForToken(String(body.authToken), { enroll: false });
      if (m && m.member) member = m.member;
    } catch (e) {
      console.error('bank-order: member lookup failed', e.message);
    }
  }

  // Refuse rather than price against stale/default stock if the CRM can't be reached right now.
  let products;
  try {
    products = await liveProducts();
  } catch (e) {
    return res.status(503).json({ error: 'crm_unavailable' });
  }
  const order = buildOrder(body.items, body.shipping, false, member ? { freeDelivery: rewards.freeDelivery(member) } : null, products, b.city);
  if (order.error) return res.status(400).json({ error: order.error });
  // The order is already placed (bank transfer), so a short item is flagged for staff, not refused.
  const short = stockProblem(body.items, products);
  if (short) checks.push('More than in hand: ' + short.name + ' (only ' + short.max + ' in stock)');
  const shippingCents = order.shippingCents;
  if (Math.round(num(body.shippingPrice) * 100) < shippingCents) {
    checks.push('Customer saw delivery ' + num(body.shippingPrice) + ' SAR, charged ' + shippingCents / 100 + ' SAR (free delivery not confirmed for this account)');
  }

  // Coupon: only what its redemption (used up at checkout) says.
  let couponCents = 0;
  const couponCode = s(body.couponCode, 40);
  if (couponCode) {
    const rid = s(body.couponRedemption, 80);
    try {
      const rows = rid ? await db('GET', 'coupon_redemptions?id=eq.' + encodeURIComponent(rid) + '&select=code,amount') : [];
      const r = rows && rows[0];
      if (r && String(r.code).toUpperCase() === couponCode.toUpperCase()) couponCents = Math.round(Number(r.amount) * 100);
      else checks.push('Coupon ' + couponCode + ' NOT verified: discount left off, check with the customer');
    } catch (e) {
      couponCents = Math.round(num(body.couponDiscount) * 100);
      checks.push('Coupon ' + couponCode + ' could not be checked just now: check it');
    }
  }

  // Rewards: what the CRM recorded as spent on this order (the cart spends it just before sending).
  let rewardsCents = 0;
  const rewardsClaimed = num(body.rewardsUsed);
  if (rewardsClaimed) {
    try {
      const used = await rewards.redeemedFor(orderId);
      rewardsCents = Math.round(used * 100);
      if (Math.abs(used - rewardsClaimed) > 0.009) checks.push('Rewards: customer claimed ' + rewardsClaimed + ' SAR, CRM recorded ' + used + ' SAR used');
    } catch (e) {
      rewardsCents = Math.round(rewardsClaimed * 100);
      checks.push('Rewards ' + rewardsClaimed + ' SAR could not be checked just now: check the loyalty history');
    }
  }

  const discountCents = Math.min(couponCents + rewardsCents, order.itemsCents);
  // Bank transfer / cash-at-pickup saving: 1% off the items after coupon / rewards (the cart shows the same).
  const savingCents = Math.round((order.itemsCents - discountCents) * 0.01);
  const totalCents = order.itemsCents - discountCents - savingCents + shippingCents;

  const details = crmDetails(Object.assign({}, order, { discountCents: discountCents + savingCents, shippingCents, totalCents, feeCents: 0 }));
  const notes = [];
  if (couponCents) notes.push('Coupon ' + couponCode + ': -' + couponCents / 100 + ' SAR');
  if (rewardsCents) notes.push('Loyalty Rewards used: -' + rewardsCents / 100 + ' SAR');
  if (savingCents) notes.push((cash ? 'Cash payment saving (1%): -' : 'Bank transfer saving (1%): -') + (savingCents / 100) + ' SAR');
  checks.forEach((c) => notes.push('CHECK: ' + c));
  notes.push(cash
    ? 'CASH AT PICKUP: collect ' + totalCents / 100 + ' SAR in cash when the customer picks up, then mark the invoice Paid.'
    : 'Bank transfer: check the amount reached the bank before marking the invoice Paid.');

  const order_ = Object.assign(details, {
    order_ref: orderId,
    source: 'bank',
    method_label: cash ? 'Cash at Pickup' : 'Bank Transfer',
    payment_method: cash ? 'Cash' : 'Bank transfer',
    paid: false,
    customer_name: name,
    customer_phone: phone,
    customer_email: s(b.email, 120),
    customer_city: s(b.city, 60),
    customer_address: [s(b.street, 120), s(b.building, 20), s(b.apartment, 40), s(b.postalCode, 20)].filter(Boolean).join(', '),
    discount_note: discountCents + savingCents ? notes.slice(0, -1).join(' · ') : null,
    notes: notes.join(' · '),
  });
  try {
    try {
      await sendBankOrder(order_);
    } catch (e) {
      // Until the CRM accepts 'Cash' for website orders (bav-crm migration 0192), file it as an
      // unpaid bank-style order with the cash instruction at the front of the notes.
      if (!cash) throw e;
      console.error('bank-order: CRM refused Cash, retrying as Bank transfer', orderId, e.message);
      await sendBankOrder(Object.assign({}, order_, { payment_method: 'Bank transfer', notes: 'PAYMENT: CASH AT PICKUP · ' + order_.notes }));
    }
  } catch (e) {
    console.error('bank-order: CRM inbox failed', orderId, e.message, e.detail || '');
    return res.status(502).json({ error: 'crm_unavailable' });
  }
  return res.status(200).json({ ok: true });
};
