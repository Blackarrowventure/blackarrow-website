// Daily birthday run (Vercel Cron, vercel.json, 08:00 Saudi time).
// The CRM credits every member whose birthday is today (Silver 10, Gold 20,
// Platinum 30 SAR, once a year) and says who got it; this then emails each of
// them a happy-birthday message with the reward, in English and Arabic.
//
// Needs, in Vercel: CRON_SECRET (Vercel sends it with the cron call; nobody else
// can trigger the run), EMAILJS_PRIVATE_KEY, and EMAILJS_BIRTHDAY_TEMPLATE_ID
// (the EmailJS template for this email). Without the template the reward is
// still credited, only the email is skipped.
const { db } = require('../_lib/db');
const rewards = require('../_lib/rewards');
const { sendEmailJs, isPlaceholderEmail } = require('../_lib/order-emails');

const TIER_AR = { Silver: 'الفضي', Gold: 'الذهبي', Platinum: 'البلاتيني' };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Website accounts by normalised rewards phone -> { name, email, id }.
async function accountsByPhone() {
  const rows = await db('GET', 'customers?select=id,name,email,phone,rewards_phone');
  const map = new Map();
  for (const c of rows || []) {
    const p = rewards.normalizePhone(c.rewards_phone || c.phone);
    if (p && !map.has(p)) map.set(p, c);
  }
  return map;
}

// Accounts made before customers.email was filled in: ask Supabase Auth.
async function authEmail(userId) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  const r = await fetch(url + '/auth/v1/admin/users/' + encodeURIComponent(userId), {
    headers: { apikey: key, Authorization: 'Bearer ' + key },
  });
  if (!r.ok) return '';
  const u = await r.json().catch(() => null);
  return (u && u.email) || '';
}

module.exports = async (req, res) => {
  const secret = process.env.CRON_SECRET;
  const auth = String(req.headers.authorization || '');
  if (!secret || auth !== 'Bearer ' + secret) return res.status(401).json({ error: 'unauthorized' });
  if (!rewards.configured()) return res.status(503).json({ error: 'rewards_not_configured' });

  let credited;
  try {
    credited = (await rewards.crmRpc('bav3d_loyalty_birthday_run', {})) || [];
  } catch (e) {
    console.error('birthday run failed:', e.message, e.detail || '');
    return res.status(502).json({ error: 'crm_failed' });
  }

  const templateId = process.env.EMAILJS_BIRTHDAY_TEMPLATE_ID;
  const report = [];
  let accounts = null;
  for (const m of credited) {
    const line = { tier: m.tier, amount: Number(m.amount), emailed: false };
    report.push(line);
    if (!templateId || !process.env.EMAILJS_PRIVATE_KEY) { line.skipped = 'email_not_configured'; continue; }
    try {
      if (!accounts) accounts = await accountsByPhone();
      const acct = accounts.get(rewards.normalizePhone(m.phone));
      let email = acct && acct.email;
      if (acct && (!email || isPlaceholderEmail(email))) email = await authEmail(acct.id);
      if (!email || isPlaceholderEmail(email)) { line.skipped = 'no_email'; continue; }
      const name = String(m.full_name || (acct && acct.name) || '').trim().split(/\s+/)[0] || 'there';
      const amount = Number(m.amount);
      const balance = Number(m.reward_balance);
      if (report.length > 1) await sleep(1100); // EmailJS allows one request per second
      await sendEmailJs({
        to_email: email,
        to_name: name,
        amount: amount.toFixed(0),
        balance: balance.toFixed(2),
        tier: m.tier,
        tier_ar: TIER_AR[m.tier] || m.tier,
        rewards_url: 'https://www.blackarrowksa.com/3d/rewards/',
        shop_url: 'https://www.blackarrowksa.com/3d/shop/',
      }, templateId);
      line.emailed = true;
    } catch (e) {
      line.error = e.message;
      console.error('birthday email failed:', e.message);
    }
  }
  console.log('birthday run:', JSON.stringify(report));
  return res.status(200).json({ credited: report.length, report });
};
