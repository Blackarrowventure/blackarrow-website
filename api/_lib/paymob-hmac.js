// Paymob's HMAC check, shared by the webhook (JSON body) and the customer's
// return to the site (the same fields flattened into the query string).
const crypto = require('crypto');

const HMAC_FIELDS = [
  'amount_cents', 'created_at', 'currency', 'error_occured', 'has_parent_transaction',
  'obj.id', 'integration_id', 'is_3d_secure', 'is_auth', 'is_capture', 'is_refunded',
  'is_standalone_payment', 'is_voided', 'order.id', 'owner', 'pending',
  'source_data.pan', 'source_data.sub_type', 'source_data.type', 'success',
];

function readPath(obj, path) {
  return path.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj);
}

function concat(get) {
  return HMAC_FIELDS.map((f) => {
    const v = get(f);
    return v == null ? '' : String(v);
  }).join('');
}

function sameHex(expected, received) {
  const a = Buffer.from(expected, 'utf8');
  const b = Buffer.from(String(received || ''), 'utf8');
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

const sign = (s, secret) => crypto.createHmac('sha512', secret).update(s).digest('hex');

// Webhook: body.obj is the transaction.
function webhookValid(tx, received, secret) {
  return sameHex(sign(concat((f) => (f === 'obj.id' ? tx.id : readPath(tx, f))), secret), received);
}

// Return to site: flat query params; "id" is the transaction, "order" its order.
function redirectValid(q, secret) {
  return sameHex(sign(concat((f) => (f === 'obj.id' ? q.id : f === 'order.id' ? q.order : q[f])), secret), q.hmac);
}

module.exports = { webhookValid, redirectValid };
