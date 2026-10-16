// The signed-in customer's Black Arrow Loyalty Rewards card. First call auto-enrols
// them (Silver, 5 SAR welcome credit) using their account's phone number.
const { bearer } = require('../_lib/db');
const rewards = require('../_lib/rewards');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  res.setHeader('Cache-Control', 'no-store');
  if (!rewards.configured()) return res.status(503).json({ error: 'rewards_not_configured' });

  try {
    const m = await rewards.memberForToken(bearer(req), { enroll: true });
    if (!m) return res.status(200).json({ signedIn: false });
    if (m.needsPhone) return res.status(200).json({ signedIn: true, needsPhone: true });
    if (!m.member) return res.status(502).json({ error: 'enrol_failed' });
    return res.status(200).json({
      signedIn: true,
      member: m.member,
      freeDelivery: rewards.freeDelivery(m.member),
      minRedeem: rewards.MIN_REDEEM,
    });
  } catch (e) {
    console.error('rewards/me failed:', e.message, e.detail || '');
    return res.status(502).json({ error: 'rewards_unavailable' });
  }
};
