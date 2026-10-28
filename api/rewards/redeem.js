// Spends reward balance on a bank-transfer order (card, Tabby and Tamara
// orders spend it automatically once the payment is confirmed). Called just
// before the order is sent; idempotent per order id, so a retried checkout
// with the same order id never spends twice.
const { bearer } = require('../_lib/db');
const rewards = require('../_lib/rewards');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  if (!rewards.configured()) return res.status(503).json({ error: 'rewards_not_configured' });

  let body;
  try {
    body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  } catch (e) {
    return res.status(400).json({ error: 'invalid_json' });
  }
  const orderId = String(body.orderId || '');
  const amount = Number(body.amount);
  if (!/^BAV-3D-\d{1,16}$/.test(orderId)) return res.status(400).json({ error: 'invalid_order' });
  if (!(amount > 0) || amount > 100000) return res.status(400).json({ error: 'invalid_amount' });

  try {
    const m = await rewards.memberForToken(bearer(req), { enroll: false });
    if (!m || !m.member) return res.status(403).json({ error: 'not_a_member' });
    const used = await rewards.redeem(m.phone, Math.floor(amount * 100) / 100, orderId);
    return res.status(200).json({ used });
  } catch (e) {
    console.error('rewards/redeem failed:', e.message, e.detail || '');
    return res.status(502).json({ error: 'rewards_unavailable' });
  }
};
