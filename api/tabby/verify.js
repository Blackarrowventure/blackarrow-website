const TABBY_API = 'https://api.tabby.ai/api/v2';

async function supabase(method, path, body, prefer) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error('supabase_not_configured');
  const headers = { apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' };
  if (prefer) headers.Prefer = prefer;
  const r = await fetch(url + '/rest/v1/' + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (!r.ok) throw new Error('supabase_' + r.status);
  const text = await r.text();
  return text ? JSON.parse(text) : null;
}

// Called by the cart page after Tabby sends the customer back.
// The server asks Tabby for the real payment status, captures it if it is
// authorised, and only then marks the order paid.
module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  const secret = process.env.TABBY_SECRET_KEY;
  if (!secret) return res.status(500).json({ error: 'payment_not_configured' });

  const ref = String((req.query && req.query.ref) || '');
  if (!/^[a-f0-9]{24}$/.test(ref)) return res.status(400).json({ error: 'invalid_ref' });

  let rows;
  try {
    rows = await supabase('GET', 'tabby_orders?order_ref=eq.' + ref + '&select=order_ref,status,amount_cents,tabby_payment_id');
  } catch (e) {
    return res.status(502).json({ error: 'order_store_unavailable' });
  }
  const order = rows[0];
  if (!order || !order.tabby_payment_id) return res.status(404).json({ error: 'order_not_found' });
  if (order.status === 'paid') return res.status(200).json({ status: 'paid' });

  const auth = { Authorization: 'Bearer ' + secret, 'Content-Type': 'application/json' };
  try {
    const pr = await fetch(TABBY_API + '/payments/' + order.tabby_payment_id, { headers: auth });
    const prText = await pr.text();
    let payment;
    try { payment = JSON.parse(prText); } catch (e) {
      console.error('tabby payment status non-json:', pr.status, prText.slice(0, 200));
      throw new Error('tabby_status_' + pr.status);
    }
    const amount = (order.amount_cents / 100).toFixed(2);

    if (payment.status === 'AUTHORIZED') {
      const cr = await fetch(TABBY_API + '/payments/' + order.tabby_payment_id + '/captures', {
        method: 'POST',
        headers: auth,
        body: JSON.stringify({ amount }),
      });
      if (!cr.ok) {
        console.error('tabby capture failed:', cr.status);
        return res.status(502).json({ error: 'capture_failed' });
      }
    } else if (payment.status === 'REJECTED' || payment.status === 'EXPIRED') {
      await supabase('PATCH', 'tabby_orders?order_ref=eq.' + ref, { status: 'failed' }, 'return=minimal');
      return res.status(200).json({ status: 'failed' });
    } else if (payment.status !== 'CLOSED') {
      return res.status(200).json({ status: 'pending' });
    }

    await supabase('PATCH', 'tabby_orders?order_ref=eq.' + ref + '&status=eq.pending', {
      status: 'paid',
      paid_at: new Date().toISOString(),
    }, 'return=minimal');
    return res.status(200).json({ status: 'paid' });
  } catch (e) {
    console.error('tabby verify failed:', e.message);
    return res.status(502).json({ error: 'verify_failed' });
  }
};
