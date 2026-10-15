// Called by the cart page after Paymob (card, Apple Pay, Tamara) sends the
// customer back. Reports what the signed webhook recorded for the order:
// 'paid', 'failed' or 'pending', and whether the server already sent the
// confirmation emails (if not, the page sends them itself as a fallback).
const { db } = require('../_lib/db');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  const ref = String((req.query && req.query.ref) || '');
  if (!/^[a-f0-9]{24}$/.test(ref)) return res.status(400).json({ error: 'invalid_ref' });

  try {
    const rows = await db('GET', 'card_orders?order_ref=eq.' + ref + '&select=*');
    if (!rows[0]) return res.status(404).json({ error: 'order_not_found' });
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ status: rows[0].status, emailsSent: !!rows[0].emails_sent_at });
  } catch (e) {
    return res.status(502).json({ error: 'order_store_unavailable' });
  }
};
