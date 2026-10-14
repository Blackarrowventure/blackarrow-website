// Called by the cart page after Paymob (card, Apple Pay, Tamara) sends the
// customer back. Reports what the signed webhook recorded for the order:
// 'paid', 'failed' or 'pending'. Nothing else about the order is returned.
module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  const ref = String((req.query && req.query.ref) || '');
  if (!/^[a-f0-9]{24}$/.test(ref)) return res.status(400).json({ error: 'invalid_ref' });

  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return res.status(500).json({ error: 'order_store_unavailable' });
  try {
    const r = await fetch(url + '/rest/v1/card_orders?order_ref=eq.' + ref + '&select=status', {
      headers: { apikey: key, Authorization: 'Bearer ' + key },
    });
    if (!r.ok) throw new Error('supabase_' + r.status);
    const rows = await r.json();
    if (!rows[0]) return res.status(404).json({ error: 'order_not_found' });
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ status: rows[0].status });
  } catch (e) {
    return res.status(502).json({ error: 'order_store_unavailable' });
  }
};
