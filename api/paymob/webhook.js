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

function computeHmac(tx, secret) {
  const concatenated = HMAC_FIELDS.map((f) => {
    const v = f === 'obj.id' ? tx.id : readPath(tx, f);
    return v == null ? '' : String(v);
  }).join('');
  return crypto.createHmac('sha512', secret).update(concatenated).digest('hex');
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).end();
  }

  const secret = process.env.PAYMOB_HMAC_SECRET;
  if (!secret) return res.status(500).end();

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  const tx = body.obj;
  const received = String((req.query && req.query.hmac) || '');
  if (!tx || !received) return res.status(400).end();

  const expected = computeHmac(tx, secret);
  const a = Buffer.from(expected, 'utf8');
  const b = Buffer.from(received, 'utf8');
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
    return res.status(401).end();
  }

  if (tx.success === true && tx.pending === false && tx.error_occured === false) {
    // Mark the order paid here once the order store is wired up (not yet built).
  }

  return res.status(200).end();
};
