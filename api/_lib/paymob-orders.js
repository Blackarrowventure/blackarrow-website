// Marking a Paymob order paid or failed, shared by the webhook and by the
// signed result Paymob attaches when it sends the customer back to the site.
const { db } = require('./db');

// Only a pending/failed order whose amount matches is moved to paid.
// ('failed' too: a declined card retried successfully in the same checkout.)
async function markPaid(ref, transactionId, amountCents) {
  const rows = await db('GET', 'card_orders?order_ref=eq.' + ref + '&select=order_ref,status,amount_cents');
  const order = rows && rows[0];
  if (!order) { console.error('paymob: no order for ref', ref); return false; }
  if (order.status === 'paid') return true;
  if (amountCents !== order.amount_cents) {
    console.error('paymob: amount mismatch', ref, 'paid', amountCents, 'expected', order.amount_cents);
    return false;
  }
  await db('PATCH', 'card_orders?order_ref=eq.' + ref + '&status=in.(pending,failed)', {
    status: 'paid',
    paymob_transaction_id: transactionId,
    paid_at: new Date().toISOString(),
  }, 'return=minimal');
  return true;
}

async function markFailed(ref) {
  await db('PATCH', 'card_orders?order_ref=eq.' + ref + '&status=eq.pending', { status: 'failed' }, 'return=minimal');
}

module.exports = { markPaid, markFailed };
