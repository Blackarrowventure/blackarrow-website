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

// Wording of every order email. They all go through the one EmailJS order template, which
// shows {{heading}} and {{message}} above the order details (the free plan allows 2 templates;
// the other one is the birthday email). Bilingual, English first.
//   received  - right after checkout: we got it, the team is checking it
//   confirmed - the shop pressed Confirm in the CRM
//   rejected  - the shop pressed Reject in the CRM, with the reason and what happens to the money
//   shop      - the shop's own copy of a new order
const REASONS_AR = {
  'Out of stock': 'المنتج غير متوفر حاليًا',
  'Duplicate order': 'طلب مكرر',
  'Wrong or incomplete details': 'بيانات الطلب غير صحيحة أو غير مكتملة',
  'Cancelled at your request': 'تم الإلغاء بناءً على طلبك',
};
// Rejections that never email the customer (the CRM's internal reasons).
const SILENT_REASONS = ['Dummy / test order'];

function emailCopy(kind, o) {
  const ref = o.ref;
  const hi = o.name ? ' ' + o.name.split(' ')[0] : '';
  if (kind === 'received') {
    return {
      subject: 'Order received #' + ref + ' | Black Arrow 3D',
      heading: 'We have received your order · استلمنا طلبك',
      message: 'Thank you' + hi + '! We have received your order' + (o.paid ? ' and your payment' : '') + '. ' +
        'Our team is checking it now, and you will get a confirmation email as soon as it is approved.\n\n' +
        'شكرًا لك! استلمنا طلبك' + (o.paid ? ' ودفعتك' : '') + '، وفريقنا يراجعه الآن. ستصلك رسالة تأكيد فور اعتماد الطلب.',
    };
  }
  if (kind === 'confirmed') {
    const pickup = /pickup/i.test(o.delivery || '');
    // Paid orders get their tax invoice as a link (api/_lib/invoice-link.js).
    const invoice = o.invoiceUrl
      ? '\n\nYour invoice (view, print or save as PDF):\n' + o.invoiceUrl
      : '';
    const invoiceAr = o.invoiceUrl
      ? '\n\nفاتورتك (للعرض أو الطباعة أو الحفظ PDF):\n' + o.invoiceUrl
      : '';
    return {
      subject: 'Order confirmed #' + ref + ' | Black Arrow 3D',
      heading: 'Your order is confirmed · تم تأكيد طلبك',
      message: 'Good news' + hi + '! Your order is confirmed and we are preparing it now. ' +
        (pickup ? 'We will let you know when it is ready for pickup.' : 'We will contact you to arrange delivery.') + invoice + '\n\n' +
        'خبر رائع! تم تأكيد طلبك ونقوم بتجهيزه الآن. ' +
        (pickup ? 'سنبلغك عندما يصبح جاهزًا للاستلام.' : 'سنتواصل معك لترتيب التوصيل.') + invoiceAr,
    };
  }
  if (kind === 'rejected') {
    const reasonAr = REASONS_AR[o.reason] || o.reason;
    let refund = '';
    let refundAr = '';
    if (o.paid) {
      refund = 'Your payment will be refunded in full to your original payment method within 24 to 48 hours.';
      refundAr = 'سيتم استرداد المبلغ كاملًا إلى وسيلة الدفع الأصلية خلال 24 إلى 48 ساعة.';
    } else if (o.cash) {
      refund = 'No payment was taken.';
      refundAr = 'لم يتم تحصيل أي مبلغ.';
    } else {
      refund = 'If you have already made the bank transfer, it will be refunded in full within 24 to 48 hours.';
      refundAr = 'إذا كنت قد أجريت التحويل البنكي، فسيتم استرداد المبلغ كاملًا خلال 24 إلى 48 ساعة.';
    }
    return {
      subject: 'Order cancelled #' + ref + ' | Black Arrow 3D',
      heading: 'Your order has been cancelled · تم إلغاء طلبك',
      message: 'Sorry' + hi + ', we could not accept your order.\nReason: ' + o.reason + '\n' + refund +
        '\nIf you have any questions, just reply to this email or message us on WhatsApp.\n\n' +
        'نعتذر، لم نتمكن من قبول طلبك.\nالسبب: ' + reasonAr + '\n' + refundAr +
        '\nلأي استفسار، رد على هذه الرسالة أو تواصل معنا عبر واتساب.',
    };
  }
  return {
    subject: 'New order #' + ref + (o.paid ? ' (PAID)' : ''),
    heading: 'New order: confirm or reject it in the CRM',
    message: o.message || '',
  };
}

async function sendConfirmedEmails(order) {
  const d = order.details || {};
  const b = d.billing || {};
  // The friendly number (emails, CRM) when the order has one; the random internal ref otherwise
  // (older orders, before this shipped). order.order_ref itself stays the random payment ref.
  const ref = d.order_number || order.order_ref;
  const total = (order.amount_cents / 100).toLocaleString('en-US') + ' SAR';
  const summary = (d.summary || []).join('\n');
  const name = ((b.first_name || '') + ' ' + (b.last_name || '')).trim();
  const address = [b.city, b.street, b.building && 'Building ' + b.building, b.apartment && 'Apt ' + b.apartment, b.postal_code]
    .filter((v) => v && v !== 'NA').join(', ');
  const rewardsNote = d.rewards_note ? '\n\n' + d.rewards_note : '';

  await sendEmailJs(Object.assign({
    to_email: process.env.SHOP_NOTIFY_EMAIL,
    to_name: 'Black Arrow 3D',
    order_id: ref,
    order_summary: 'PAID - payment confirmed by ' + d.method + '. Confirm or reject it in the CRM (Online Orders); the customer is emailed when you do.\n\n' +
      'Customer: ' + name + '\nPhone: ' + (b.phone || '') + '\nEmail: ' + (b.email || '') + '\nAddress: ' + address +
      '\n\n' + summary + rewardsNote,
    shipping_method: d.shipping_label || '',
    payment_method: d.method + ' (PAID)',
    order_total: total,
  }, emailCopy('shop', { ref, paid: true })));

  if (b.email && !isPlaceholderEmail(b.email)) {
    await sleep(1100); // EmailJS allows one request per second
    try {
      await sendEmailJs(Object.assign({
        to_email: b.email,
        to_name: name,
        order_id: ref,
        order_summary: summary,
        shipping_method: d.shipping_label || '',
        payment_method: d.method + ' (paid)',
        order_total: total,
      }, emailCopy('received', { ref, name, paid: true })));
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

module.exports = { afterPaid, emailsConfigured, sendEmailJs, isPlaceholderEmail, emailCopy, SILENT_REASONS };
