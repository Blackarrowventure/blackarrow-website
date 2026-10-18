const { afterPaid } = require('../_lib/order-emails');
const { markPaid, markFailed } = require('../_lib/paymob-orders');
const { webhookValid } = require('../_lib/paymob-hmac');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).end();
  }

  const secret = process.env.PAYMOB_HMAC_SECRET;
  if (!secret) { console.error('paymob webhook: PAYMOB_HMAC_SECRET is not set'); return res.status(500).end(); }

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  const tx = body.obj;
  const received = String((req.query && req.query.hmac) || '');
  const ref = tx && tx.order && tx.order.merchant_order_id;
  if (!tx || !received) { console.error('paymob webhook: no transaction or hmac', body.type || ''); return res.status(400).end(); }

  if (!webhookValid(tx, received, secret)) {
    console.error('paymob webhook: HMAC mismatch - check PAYMOB_HMAC_SECRET in Vercel', ref, tx.id);
    return res.status(401).end();
  }
  console.log('paymob webhook:', ref, 'tx', tx.id, 'success', tx.success, 'pending', tx.pending);

  if (tx.success === true && tx.pending === false && tx.error_occured === false) {
    if (!ref || !/^[a-f0-9]{24}$/.test(ref)) { console.error('paymob webhook: unexpected merchant_order_id', ref); return res.status(200).end(); }
    try {
      await markPaid(ref, tx.id, Number(tx.amount_cents));
    } catch (e) {
      console.error('paymob webhook: could not mark paid', ref, e.message);
      return res.status(500).end();
    }
    // Rewards spent + "Order CONFIRMED" emails, from the server, whether or not
    // the customer ever returns to the site. Safe if Paymob retries the webhook.
    const r = await afterPaid('card_orders', ref);
    console.log('paymob webhook: emails', ref, r && r.emailsSent ? 'sent' : 'NOT sent');
  } else if (tx.success === false && tx.pending === false) {
    // Declined or cancelled: lets the cart page tell the customer straight away.
    if (ref && /^[a-f0-9]{24}$/.test(ref)) {
      try { await markFailed(ref); } catch (e) { return res.status(500).end(); }
    }
  }

  return res.status(200).end();
};
