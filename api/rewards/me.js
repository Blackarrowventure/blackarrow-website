// The signed-in customer's Black Arrow Loyalty Rewards card. First call auto-enrols
// them (Silver, 5 SAR welcome credit) using their account's phone number.
// POST { dob: "YYYY-MM-DD" } saves their date of birth (once; the CRM keeps the
// first one) for the birthday reward, and returns the card like GET does.
const { bearer } = require('../_lib/db');
const rewards = require('../_lib/rewards');

function validDob(v) {
  if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(v)) return false;
  const d = new Date(v + 'T00:00:00Z');
  if (Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== v) return false;
  const year = d.getUTCFullYear();
  return year >= 1920 && year <= new Date().getUTCFullYear() - 10;
}

module.exports = async (req, res) => {
  if (req.method !== 'GET' && req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  res.setHeader('Cache-Control', 'no-store');
  if (!rewards.configured()) return res.status(503).json({ error: 'rewards_not_configured' });

  let dob = null;
  if (req.method === 'POST') {
    const body = typeof req.body === 'string' ? (() => { try { return JSON.parse(req.body); } catch (e) { return {}; } })() : (req.body || {});
    if (!validDob(body.dob)) return res.status(400).json({ error: 'invalid_dob' });
    dob = body.dob;
  }

  try {
    let m = await rewards.memberForToken(bearer(req), { enroll: true });
    if (!m) return res.status(200).json({ signedIn: false });
    if (m.needsPhone) return res.status(200).json({ signedIn: true, needsPhone: true });
    if (!m.member) return res.status(502).json({ error: 'enrol_failed' });
    if (dob && !m.member.dateOfBirth) {
      await rewards.setBirthday(m.phone, dob);
      m = await rewards.memberForToken(bearer(req), { enroll: false });
    }
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
