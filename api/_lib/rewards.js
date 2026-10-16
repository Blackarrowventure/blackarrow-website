// Black Arrow Loyalty Rewards: every loyalty call goes from here to the BAV CRM's
// Supabase with its service_role key (the CRM functions are not callable
// from browsers). A customer is identified only through their signed-in
// website account, never through a phone number typed into a form.
const { db, websiteUser } = require('./db');

const CRM_URL = process.env.CRM_SUPABASE_URL || 'https://iorbuqljfxifgtrdniwq.supabase.co';
const MIN_REDEEM = 4;

function configured() {
  return !!process.env.CRM_SUPABASE_SERVICE_ROLE_KEY;
}

async function crmRpc(fn, args) {
  const key = process.env.CRM_SUPABASE_SERVICE_ROLE_KEY;
  if (!key) throw new Error('rewards_not_configured');
  const r = await fetch(CRM_URL + '/rest/v1/rpc/' + fn, {
    method: 'POST',
    headers: { apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
    body: JSON.stringify(args),
  });
  const text = await r.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (e) { /* non-json */ }
  if (!r.ok) {
    const e = new Error('crm_' + r.status);
    e.detail = data && data.message ? data.message : text.slice(0, 200);
    throw e;
  }
  return data;
}

// The phone that identifies this account's rewards card. Fixed at the first
// enrolment (rewards_phone), so editing the profile phone later can't move
// the account onto a fresh card with a fresh welcome credit.
async function accountPhone(userId) {
  let rows;
  try {
    rows = await db('GET', 'customers?id=eq.' + encodeURIComponent(userId) + '&select=*');
  } catch (e) {
    return { name: '', phone: '', locked: false };
  }
  const c = rows && rows[0];
  if (!c) return { name: '', phone: '', locked: false };
  const locked = !!(c.rewards_phone && String(c.rewards_phone).trim());
  return { name: c.name || '', phone: String((locked ? c.rewards_phone : c.phone) || '').trim(), locked };
}

async function lockPhone(userId, phone) {
  try {
    await db('PATCH', 'customers?id=eq.' + encodeURIComponent(userId) + '&rewards_phone=is.null', { rewards_phone: phone }, 'return=minimal');
  } catch (e) {
    // Column not added yet (supabase/3d-order-details.sql): not fatal.
  }
}

function toMember(row) {
  return {
    name: row.full_name || '',
    tier: row.tier,
    balance: Number(row.reward_balance) || 0,
    lifetimeSpend: Number(row.lifetime_spend) || 0,
    memberSince: row.member_since,
  };
}

// { user, phone, member } | { user, needsPhone: true } | null (not signed in)
async function memberForToken(token, opts) {
  const user = await websiteUser(token);
  if (!user) return null;
  const acct = await accountPhone(user.id);
  if (!acct.phone) return { user, needsPhone: true };
  if (opts && opts.enroll) {
    const name = acct.name || (user.email ? user.email.split('@')[0] : 'Member');
    await crmRpc('bav3d_loyalty_signup', { p_full_name: name, p_phone: acct.phone, p_date_of_birth: null });
    if (!acct.locked) await lockPhone(user.id, acct.phone);
  }
  const rows = await crmRpc('bav3d_loyalty_get', { p_phone: acct.phone });
  const row = rows && rows[0];
  if (!row || !row.found) return { user, phone: acct.phone, member: null };
  return { user, phone: acct.phone, member: toMember(row) };
}

function freeDelivery(member) {
  return !!member && (member.tier === 'Gold' || member.tier === 'Platinum');
}

// Spends balance on an order; idempotent per ref. Returns SAR actually used.
async function redeem(phone, amountSar, ref) {
  const used = await crmRpc('bav3d_loyalty_redeem', { p_phone: phone, p_amount: amountSar, p_ref: ref });
  return Number(used) || 0;
}

// For the payment endpoints: who is paying, what they may use, free delivery.
async function checkoutRewards(token, useRewards, itemsCents) {
  if (!token || !configured()) return { member: null, phone: null, discountCents: 0, freeDelivery: false };
  let m = null;
  try { m = await memberForToken(token, { enroll: false }); } catch (e) { console.error('rewards lookup failed:', e.message); }
  if (!m || !m.member) return { member: null, phone: null, discountCents: 0, freeDelivery: false };
  let discountCents = 0;
  if (useRewards && m.member.balance >= MIN_REDEEM) {
    discountCents = Math.min(Math.floor(m.member.balance * 100), itemsCents);
  }
  return { member: m.member, phone: m.phone, discountCents, freeDelivery: freeDelivery(m.member) };
}

module.exports = { configured, crmRpc, memberForToken, freeDelivery, redeem, checkoutRewards, MIN_REDEEM };
