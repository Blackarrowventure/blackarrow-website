// GET /api/orders/   (Authorization: Bearer <website customer's access token>)
//
// The signed-in customer's own website orders for the account page (Order History + Order Tracking).
// Every website order - bank transfer, cash at pickup, card / Apple Pay, Tabby, Tamara, pre-orders -
// lands in the CRM's bav3d_online_orders inbox; once confirmed it becomes an invoice whose
// progress_status (Order received -> Packed -> Ready for delivery -> Dispatched -> Delivered ->
// Completed) is updated in the CRM. Both are read live here, so the page always matches the CRM.
//
// Whose orders: those placed with the account's email address, and only once that email has been
// confirmed. The phone number is deliberately NOT used: it is not verified, so matching on it would
// let anyone type someone else's number into their profile and see that person's orders.
//
// Returns only what the customer's own emails and invoice already show: items, prices, delivery,
// totals, status and progress. Never costs, internal notes, stock holds or who decided.
// Served from api/checkout-health.js (the Vercel Hobby plan's 12 functions are all in use).
const catalog = require('../../3d/assets/data/3d-products.json');
const { bearer, websiteUser } = require('./db');
const { tokenFor, invoiceUrl } = require('./invoice-link');
const { SILENT_REASONS } = require('./order-emails');

const CRM_URL = process.env.CRM_SUPABASE_URL || 'https://iorbuqljfxifgtrdniwq.supabase.co';
const LIMIT = 50;
const num = (v) => Math.round(Number(v || 0) * 100) / 100;

async function crmGet(path) {
  const key = process.env.CRM_SUPABASE_SERVICE_ROLE_KEY;
  const r = await fetch(CRM_URL + '/rest/v1/' + path, { headers: { apikey: key, Authorization: 'Bearer ' + key } });
  if (!r.ok) throw new Error('crm_' + r.status);
  return r.json();
}

function productInfo() {
  const byId = new Map();
  catalog.products.forEach((p) => byId.set(p.id, p));
  return byId;
}

function lineOut(l, byId) {
  const p = byId.get(l.product_slug);
  return {
    id: l.product_slug || '',
    name: (p && p.name) || l.product_name || l.name || 'Item',
    nameAr: (p && p.name_ar) || '',
    variant: l.variant_label || '',
    qty: Number(l.quantity) || 1,
    price: num(l.unit_price),
    image: (p && p.images && p.images[0]) || '',
    url: p ? '/3d/product/' + p.id + '/' : '',
  };
}

async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  if (!process.env.CRM_SUPABASE_SERVICE_ROLE_KEY) return res.status(503).json({ error: 'orders_not_configured' });

  let user;
  try { user = await websiteUser(bearer(req)); } catch (e) { user = null; }
  if (!user) return res.status(200).json({ signedIn: false });
  const email = String(user.email || '').trim().toLowerCase();
  if (!email || !user.email_confirmed_at) return res.status(200).json({ signedIn: true, needsVerify: true, orders: [] });

  try {
    // ilike for a case-insensitive match; the exact comparison below removes anything the
    // pattern characters (_ and %) could let through.
    const rows = await crmGet('bav3d_online_orders?customer_email=ilike.' + encodeURIComponent(email)
      + '&select=order_ref,customer_email,status,method_label,payment_method,paid,ordered_at,lines,items_total,discount,delivery_fee,delivery_label,pay_later_fee,total,invoice_id,reject_reason'
      + '&order=ordered_at.desc&limit=' + LIMIT);
    const mine = (rows || []).filter((o) => String(o.customer_email || '').trim().toLowerCase() === email
      && !(o.status === 'rejected' && SILENT_REASONS.includes(o.reject_reason)));

    const ids = mine.map((o) => o.invoice_id).filter(Boolean);
    const invoices = new Map();
    if (ids.length) {
      const q = 'bav3d_acc_invoices?id=in.(' + ids.map(encodeURIComponent).join(',') + ')&select=id,invoice_number,status';
      // progress_status comes from CRM migration 0192; without it the orders still show, just without progress.
      const inv = await crmGet(q + ',progress_status').catch(() => crmGet(q)).catch(() => []);
      (inv || []).forEach((i) => invoices.set(i.id, i));
    }

    const byId = productInfo();
    const orders = mine.map((o) => {
      const inv = o.invoice_id ? invoices.get(o.invoice_id) : null;
      // Confirmed, then its invoice set to Cancelled in the CRM: shown as cancelled.
      const cancelled = !!(inv && inv.status === 'Cancelled');
      const paid = !cancelled && (!!o.paid || !!(inv && inv.status === 'Paid'));
      return {
        ref: o.order_ref,
        date: o.ordered_at,
        status: cancelled ? 'rejected' : o.status,          // pending | confirmed | rejected
        progress: inv && !cancelled ? inv.progress_status || 'Order received' : null,
        method: o.method_label || o.payment_method || '',
        paid,
        lines: (Array.isArray(o.lines) ? o.lines : []).map((l) => lineOut(l, byId)),
        itemsTotal: num(o.items_total),
        discount: num(o.discount),
        delivery: num(o.delivery_fee),
        deliveryLabel: o.delivery_label || '',
        fee: num(o.pay_later_fee),
        total: num(o.total),
        reason: o.status === 'rejected' ? (o.reject_reason || '') : '',
        invoiceNumber: inv ? inv.invoice_number || '' : '',
        // The same signed invoice link the confirmation email carries, for paid invoices only.
        invoiceUrl: inv && paid && tokenFor(inv.id) ? invoiceUrl(inv.id) : '',
      };
    });
    return res.status(200).json({ signedIn: true, email, orders });
  } catch (e) {
    console.error('my-orders failed:', e.message);
    return res.status(502).json({ error: 'orders_unavailable' });
  }
}

module.exports = { handler };
