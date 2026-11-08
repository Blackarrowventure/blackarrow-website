// Customer invoice links: https://www.blackarrowksa.com/3d/invoice/?t=<token>
//
// The confirmation email of a PAID website order carries this link (api/_lib/order-decision.js).
// The token is the CRM invoice id plus a signature only this server can make, so a link cannot
// be guessed or altered to open someone else's invoice. Nothing is stored for it.
//
// GET /api/invoice/?t=<token> returns ONLY what the customer's invoice shows: items, prices,
// discount, delivery, VAT and totals. Never the costs, suppliers or profit kept on the same CRM row.
// Served from api/checkout-health.js (the Vercel Hobby plan's 12 functions are all in use).
const crypto = require('crypto');

const CRM_URL = process.env.CRM_SUPABASE_URL || 'https://iorbuqljfxifgtrdniwq.supabase.co';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const PAYMENT_LABELS = {
  'Bank transfer': 'Bank transfer',
  Cash: 'Cash',
  Paymob: 'Card / mada / Apple Pay',
  Tabby: 'Tabby / Tamara (pay later)',
};

// INVOICE_LINK_SECRET if set in Vercel; otherwise derived from the CRM key (changing that key
// would make older invoice links stop working, nothing else).
function secret() {
  return process.env.INVOICE_LINK_SECRET || process.env.CRM_SUPABASE_SERVICE_ROLE_KEY || '';
}
function sign(id) {
  return crypto.createHmac('sha256', secret()).update('bav3d-invoice:' + id).digest('base64url').slice(0, 32);
}
function tokenFor(invoiceId) {
  if (!secret() || !UUID.test(String(invoiceId || ''))) return null;
  return invoiceId + '.' + sign(invoiceId);
}
function invoiceUrl(invoiceId) {
  const t = tokenFor(invoiceId);
  return t ? 'https://www.blackarrowksa.com/3d/invoice/?t=' + t : null;
}
function idFromToken(token) {
  const m = /^([0-9a-f-]{36})\.([A-Za-z0-9_-]{32})$/.exec(String(token || ''));
  if (!m || !UUID.test(m[1]) || !secret()) return null;
  const want = Buffer.from(sign(m[1]));
  const got = Buffer.from(m[2]);
  return want.length === got.length && crypto.timingSafeEqual(want, got) ? m[1] : null;
}

async function crmGet(path) {
  const key = process.env.CRM_SUPABASE_SERVICE_ROLE_KEY;
  const r = await fetch(CRM_URL + '/rest/v1/' + path, { headers: { apikey: key, Authorization: 'Bearer ' + key } });
  if (!r.ok) throw new Error('crm_' + r.status);
  return r.json();
}

const num = (v) => Math.round(Number(v || 0) * 100) / 100;

async function handler(req, res) {
  res.setHeader('Cache-Control', 'private, no-store');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');
  if (req.method !== 'GET') return res.status(405).json({ error: 'method_not_allowed' });
  if (!process.env.CRM_SUPABASE_SERVICE_ROLE_KEY) return res.status(503).json({ error: 'not_configured' });
  const id = idFromToken(req.query && req.query.t);
  if (!id) return res.status(404).json({ error: 'not_found' });
  try {
    const rows = await crmGet('bav3d_acc_invoices?id=eq.' + id +
      '&select=invoice_number,invoice_date,status,paid_date,customer_id,items,discount,delivery_fee,pay_later_fee,payment_method,subtotal,total,vat_amount,online_order_ref');
    const inv = rows && rows[0];
    if (!inv) return res.status(404).json({ error: 'not_found' });
    let customer = {};
    if (inv.customer_id && UUID.test(inv.customer_id)) {
      const c = await crmGet('bav3d_customers?id=eq.' + inv.customer_id + '&select=full_name,email');
      customer = (c && c[0]) || {};
    }
    const total = num(inv.total);
    const vat = num(inv.vat_amount);
    return res.status(200).json({
      invoiceNumber: inv.invoice_number,
      invoiceDate: inv.invoice_date,
      status: inv.status,
      paidDate: inv.paid_date,
      orderRef: inv.online_order_ref || '',
      customer: { name: customer.full_name || '', email: customer.email || '' },
      items: (Array.isArray(inv.items) ? inv.items : []).map((i) => ({
        description: i.variant_label ? (i.product_name || '') + ' — ' + i.variant_label : (i.product_name || ''),
        quantity: Number(i.quantity) || 0,
        unitPrice: num(i.unit_price),
      })),
      subtotal: num(inv.subtotal),
      discount: num(inv.discount),
      deliveryFee: num(inv.delivery_fee),
      payLaterFee: num(inv.pay_later_fee),
      taxableAmount: num(total - vat),
      vatRate: 15,
      vatAmount: vat,
      total,
      paymentMethod: PAYMENT_LABELS[inv.payment_method] || inv.payment_method || '',
    });
  } catch (e) {
    console.error('invoice:', e.message);
    return res.status(502).json({ error: 'unavailable' });
  }
}

module.exports = { handler, invoiceUrl, tokenFor, idFromToken };
