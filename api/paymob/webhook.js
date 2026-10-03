const crypto = require('crypto');

async function supabase(method, path, body, prefer) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error('supabase_not_configured');
  const headers = { apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' };
  if (prefer) headers.Prefer = prefer;
  const r = await fetch(url + '/rest/v1/' + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (!r.ok) throw new Error('supabase_' + r.status);
  return r.json();
}

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
    const orderRef = tx.order && tx.order.merchant_order_id;
    if (!orderRef || !/^[a-f0-9]{24}$/.test(orderRef)) return res.status(200).end();
    try {
      const rows = await supabase('GET', 'card_orders?order_ref=eq.' + orderRef + '&select=order_ref,status,amount_cents');
      const order = rows[0];
      if (!order) return res.status(200).end();
      if (order.status === 'pending' && Number(tx.amount_cents) === order.amount_cents) {
        await supabase('PATCH', 'card_orders?order_ref=eq.' + orderRef + '&status=eq.pending', {
          status: 'paid',
          paymob_transaction_id: tx.id,
          paid_at: new Date().toISOString(),
        }, 'return=minimal');
      }
    } catch (e) {
      return res.status(500).end();
    }
  }

  return res.status(200).end();
};
