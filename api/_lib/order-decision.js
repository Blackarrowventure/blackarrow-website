// POST /api/order-decision/  { order_ref }   (Authorization: Bearer <CRM user's access token>)
//
// The BAV CRM calls this right after someone presses Confirm or Reject on a website order
// (BAV 3D Accounting > Online Orders). It emails the customer the outcome:
//   confirmed -> "Your order is confirmed" with the full order details
//   rejected  -> "Your order has been cancelled" with the reason and what happens to the money
//
// Nothing in the request decides what the email says: the order, its status and the reason are
// read from the CRM's own bav3d_online_orders row. The caller must be signed in to the CRM and
// must be the person who made that decision, within the last hour.
// Served from api/checkout-health.js (the Vercel Hobby plan allows 12 functions; all are used).
const catalog = require('../../3d/assets/data/3d-products.json');
const { groupedSummary } = require('./pricing');
const { sendEmailJs, isPlaceholderEmail, emailCopy, SILENT_REASONS } = require('./order-emails');

const CRM_URL = process.env.CRM_SUPABASE_URL || 'https://iorbuqljfxifgtrdniwq.supabase.co';
const DECISION_WINDOW_MS = 60 * 60 * 1000;

async function crmUser(token) {
  const key = process.env.CRM_SUPABASE_SERVICE_ROLE_KEY;
  const r = await fetch(CRM_URL + '/auth/v1/user', { headers: { apikey: key, Authorization: 'Bearer ' + token } });
  if (!r.ok) return null;
  const u = await r.json().catch(() => null);
  return u && u.id ? u : null;
}

async function onlineOrder(ref) {
  const key = process.env.CRM_SUPABASE_SERVICE_ROLE_KEY;
  const r = await fetch(CRM_URL + '/rest/v1/bav3d_online_orders?order_ref=eq.' + encodeURIComponent(ref) + '&select=*', {
    headers: { apikey: key, Authorization: 'Bearer ' + key },
  });
  if (!r.ok) throw new Error('crm_' + r.status);
  const rows = await r.json();
  return rows && rows[0] ? rows[0] : null;
}

const sar = (n) => (Math.round(Number(n || 0) * 100) / 100).toLocaleString('en-US') + ' SAR';

// The order details block, in the same grouped layout as the checkout emails.
function summaryOf(o) {
  const byId = new Map(catalog.products.map((p) => [p.id, p]));
  const lines = (Array.isArray(o.lines) ? o.lines : []).map((l, i) => {
    const p = byId.get(l.product_slug);
    return {
      id: l.product_slug || 'line-' + i,
      productName: (p && p.name) || l.product_name || l.name || 'Item',
      brand: (p && p.brand) || '',
      category: (p && p.category) || 'Other',
      variantLabel: l.variant_label || '',
      unitCents: Math.round(Number(l.unit_price || 0) * 100),
      qty: Number(l.quantity) || 1,
    };
  });
  const out = groupedSummary(lines, (c) => sar(c / 100));
  if (Number(o.discount) > 0) out.push((o.discount_note || 'Discount') + ': -' + sar(o.discount));
  if (Number(o.pay_later_fee) > 0) out.push('Pay-later service fee: ' + sar(o.pay_later_fee));
  out.push('Shipping: ' + (o.delivery_label || '') + ' — ' + (Number(o.delivery_fee) > 0 ? sar(o.delivery_fee) : 'Free'));
  out.push('Grand Total: ' + sar(o.total));
  return out.join('\n');
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  // Bearer-token auth (no cookies), so any origin may call it: the CRM website and its Android app.
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Authorization, Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });
  if (!process.env.CRM_SUPABASE_SERVICE_ROLE_KEY || !process.env.EMAILJS_PRIVATE_KEY) return res.status(503).json({ error: 'not_configured' });

  const token = String(req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
  const ref = String(body.order_ref || '');
  if (!token) return res.status(401).json({ error: 'sign_in_required' });
  if (!/^[A-Za-z0-9_-]{4,64}$/.test(ref)) return res.status(400).json({ error: 'bad_order_ref' });

  try {
    const user = await crmUser(token);
    if (!user) return res.status(401).json({ error: 'sign_in_required' });
    const o = await onlineOrder(ref);
    if (!o) return res.status(404).json({ error: 'order_not_found' });
    if (o.status !== 'confirmed' && o.status !== 'rejected') return res.status(409).json({ error: 'not_decided' });
    if (o.decided_by !== user.id) return res.status(403).json({ error: 'not_your_decision' });
    if (!o.decided_at || Date.now() - new Date(o.decided_at).getTime() > DECISION_WINDOW_MS) return res.status(409).json({ error: 'decision_too_old' });

    if (o.status === 'rejected' && SILENT_REASONS.includes(o.reject_reason)) return res.status(200).json({ sent: false, reason: 'test_order' });
    const email = String(o.customer_email || '').trim();
    if (!email || isPlaceholderEmail(email)) return res.status(200).json({ sent: false, reason: 'no_email' });

    const cash = /cash/i.test([o.payment_method, o.method_label, o.notes].join(' '));
    const copy = emailCopy(o.status, {
      ref, name: o.customer_name || '', paid: !!o.paid, cash,
      reason: o.reject_reason || 'Order could not be accepted', delivery: o.delivery_label,
    });
    await sendEmailJs(Object.assign({
      to_email: email,
      to_name: o.customer_name || '',
      order_id: ref,
      order_summary: summaryOf(o),
      shipping_method: o.delivery_label || '',
      payment_method: (o.method_label || o.payment_method || '') + (o.paid ? ' (paid)' : ''),
      order_total: sar(o.total),
    }, copy));
    return res.status(200).json({ sent: true, to: email, status: o.status });
  } catch (e) {
    console.error('order-decision:', ref, e.message);
    return res.status(502).json({ error: 'email_failed', detail: String(e.message || '').slice(0, 200) });
  }
};
