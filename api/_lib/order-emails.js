// "Order CONFIRMED" emails, sent by the server once a gateway has confirmed
// the payment, so they go out even if the customer never comes back to the
// site. Uses the same EmailJS template the cart page already uses; the shop
// gets its own copy (with the customer's contact and address) at
// SHOP_NOTIFY_EMAIL.
//
// Needs, in Vercel: EMAILJS_PRIVATE_KEY (EmailJS > Account > Security, with
// "Allow EmailJS API for non-browser applications" turned on) and
// SHOP_NOTIFY_EMAIL. Without them nothing is sent from here and the cart
// page falls back to sending from the customer's browser, as before.
const { db } = require('./db');
const rewards = require('./rewards');
const crmOrders = require('./crm-orders');

const EMAILJS = { serviceId: 'service_2rpw1y5', templateId: 'template_hopo6zf', publicKey: 'DN3sB2Ge_A6IXCu_f' };

function emailsConfigured() {
  return !!(process.env.EMAILJS_PRIVATE_KEY && process.env.SHOP_NOTIFY_EMAIL);
}

function isPlaceholderEmail(email) {
  const m = /^([^@]+)@([^@]+)$/.exec(String(email || '').trim().toLowerCase());
  if (!m) return true;
  const local = m[1];
  const domain = m[2];
  if (local.length <= 1 || domain.replace(/\.[a-z.]+$/, '').length <= 1) return true;
  return ['example.com', 'example.org', 'example.net', 'test.com', 'test.co', 'a.com', 'b.com', 'asdf.com', 'mailinator.com'].includes(domain);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function sendEmailJs(params, templateId) {
  const r = await fetch('https://api.emailjs.com/api/v1.0/email/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      service_id: EMAILJS.serviceId,
      template_id: templateId || EMAILJS.templateId,
      user_id: EMAILJS.publicKey,
      accessToken: process.env.EMAILJS_PRIVATE_KEY,
      template_params: params,
    }),
  });
  if (!r.ok) throw new Error('emailjs_' + r.status + ': ' + (await r.text()).slice(0, 200));
}

async function sendConfirmedEmails(order) {
  const d = order.details || {};
  const b = d.billing || {};
  const total = (order.amount_cents / 100).toLocaleString('en-US') + ' SAR';
  const summary = (d.summary || []).join('\n');
  const name = ((b.first_name || '') + ' ' + (b.last_name || '')).trim();
  const address = [b.city, b.street, b.building && 'Building ' + b.building, b.apartment && 'Apt ' + b.apartment, b.postal_code]
    .filter((v) => v && v !== 'NA').join(', ');
  const rewardsNote = d.rewards_note ? '\n\n' + d.rewards_note : '';

  await sendEmailJs({
    to_email: process.env.SHOP_NOTIFY_EMAIL,
    to_name: 'Black Arrow 3D',
    order_id: order.order_ref,
    order_summary: 'PAID - payment confirmed by ' + d.method + '. Ready to prepare and ship.\n\n' +
      'Customer: ' + name + '\nPhone: ' + (b.phone || '') + '\nEmail: ' + (b.email || '') + '\nAddress: ' + address +
      '\n\n' + summary + rewardsNote,
    shipping_method: d.shipping_label || '',
    payment_method: d.method + ' (PAID)',
    order_total: total,
  });

  if (b.email && !isPlaceholderEmail(b.email)) {
    await sleep(1100); // EmailJS allows one request per second
    try {
      await sendEmailJs({
        to_email: b.email,
        to_name: name,
        order_id: order.order_ref,
        order_summary: summary,
        shipping_method: d.shipping_label || '',
        payment_method: d.method + ' (paid)',
        order_total: total,
      });
    } catch (e) {
      console.error('customer confirmation email failed:', order.order_ref, e.message);
    }
  }
}

// Run after an order is marked paid (Paymob webhook, Tabby verify). Safe to
// call any number of times: rewards are spent once per order (the CRM keys
// it by order ref) and emails are claimed with a single conditional update.
async function afterPaid(table, ref) {
  let rows;
  try {
    rows = await db('GET', table + '?order_ref=eq.' + ref + '&select=*');
  } catch (e) {
    console.error('afterPaid: load failed', table, ref, e.message);
    return { emailsSent: false };
  }
  const order = rows && rows[0];
  if (!order || order.status !== 'paid') return { emailsSent: false };
  const d = order.details || null;

  if (d && d.rewards && d.rewards.discount_cents > 0 && !order.rewards_redeemed_at) {
    try {
      const used = await rewards.redeem(d.rewards.phone, d.rewards.discount_cents / 100, ref);
      await db('PATCH', table + '?order_ref=eq.' + ref, { rewards_redeemed_at: new Date().toISOString() }, 'return=minimal');
      if (Math.round(used * 100) < d.rewards.discount_cents) {
        d.rewards_note = 'NOTE: the customer was given ' + (d.rewards.discount_cents / 100) + ' SAR rewards discount but only ' + used + ' SAR was left on their card.';
      }
    } catch (e) {
      console.error('afterPaid: rewards redeem failed', ref, e.message, e.detail || '');
      d.rewards_note = 'NOTE: ' + (d.rewards.discount_cents / 100) + ' SAR rewards discount was given but could not be taken off the customer\'s card (' + (e.detail || e.message) + '). Check it in the CRM.';
    }
  }

  // Into the CRM's Online Orders inbox, to be confirmed or rejected there. Never blocks the emails;
  // the CRM ignores a repeat, so the webhook and the customer's return both trying is fine.
  try {
    await crmOrders.sendPaidOrder(table, order);
  } catch (e) {
    console.error('afterPaid: CRM online order failed', ref, e.message, e.detail || '');
  }

  if (order.emails_sent_at) return { emailsSent: true };
  if (!emailsConfigured() || !d) return { emailsSent: false };

  let claimed;
  try {
    claimed = await db('PATCH', table + '?order_ref=eq.' + ref + '&emails_sent_at=is.null', { emails_sent_at: new Date().toISOString() }, 'return=representation');
  } catch (e) {
    return { emailsSent: false };
  }
  if (!claimed || !claimed.length) return { emailsSent: true }; // another call already sent them

  try {
    await sendConfirmedEmails(Object.assign({}, order, { details: d }));
    return { emailsSent: true };
  } catch (e) {
    console.error('afterPaid: shop email failed', ref, e.message);
    await db('PATCH', table + '?order_ref=eq.' + ref, { emails_sent_at: null }, 'return=minimal').catch(() => {});
    return { emailsSent: false };
  }
}

module.exports = { afterPaid, emailsConfigured, sendEmailJs, isPlaceholderEmail };
