// Called by the cart page after Paymob (card, Apple Pay, Tamara) sends the
// customer back. Reports 'paid', 'failed' or 'pending' and whether the
// confirmation emails went out (if not, the page sends them as a fallback).
//
// Paymob appends its signed transaction result to that return address. If the
// webhook hasn't marked the order paid yet (or never reaches us), a valid
// signature here marks it paid and sends the emails: the same HMAC secret
// protects both, so a customer cannot fake it.
const { db } = require('../_lib/db');
const { afterPaid } = require('../_lib/order-emails');
const { markPaid, markFailed } = require('../_lib/paymob-orders');
const { redirectValid } = require('../_lib/paymob-hmac');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  res.setHeader('Cache-Control', 'no-store');
  const q = req.query || {};
  const ref = String(q.ref || '');
  if (!/^[a-f0-9]{24}$/.test(ref)) return res.status(400).json({ error: 'invalid_ref' });

  let order;
  try {
    const rows = await db('GET', 'card_orders?order_ref=eq.' + ref + '&select=status,emails_sent_at');
    order = rows[0];
    if (!order) return res.status(404).json({ error: 'order_not_found' });
  } catch (e) {
    return res.status(502).json({ error: 'order_store_unavailable' });
  }

  const secret = process.env.PAYMOB_HMAC_SECRET;
  if (order.status !== 'paid' && q.hmac && secret) {
    if (String(q.merchant_order_id || '') !== ref) {
      console.error('paymob return: merchant_order_id does not match', ref, q.merchant_order_id);
    } else if (!redirectValid(q, secret)) {
      console.error('paymob return: HMAC mismatch - check PAYMOB_HMAC_SECRET in Vercel', ref);
    } else if (q.success === 'true' && q.pending === 'false' && q.error_occured === 'false') {
      try {
        if (await markPaid(ref, q.id, Number(q.amount_cents))) {
          console.log('paymob return: marked paid', ref);
          order.status = 'paid';
        }
      } catch (e) {
        console.error('paymob return: could not mark paid', ref, e.message);
      }
    } else if (q.success === 'false' && q.pending === 'false') {
      try { await markFailed(ref); order.status = 'failed'; } catch (e) { /* the webhook can still record it */ }
    }
  }

  if (order.status === 'paid' && !order.emails_sent_at) {
    const r = await afterPaid('card_orders', ref);
    return res.status(200).json({ status: 'paid', emailsSent: !!(r && r.emailsSent) });
  }
  return res.status(200).json({ status: order.status, emailsSent: !!order.emails_sent_at });
};
