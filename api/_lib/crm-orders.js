// Website orders into the BAV CRM's "Online Orders" inbox (BAV 3D Accounting), where each one
// waits until it is confirmed (becomes an invoice) or rejected (dummy / refused order). The CRM
// keys every order by order_ref, so sending the same order twice is harmless.
const { crmRpc, configured } = require('./rewards');

const sar = (cents) => Math.round(cents) / 100;

// Stored with the order at checkout (details.crm): everything the CRM needs to rebuild the
// invoice exactly - product + variant per line, delivery, pay-later fee, rewards discount.
function crmDetails(order) {
  return {
    lines: order.lines.map((l) => ({
      product_slug: l.id,
      variant_label: l.variantLabel || '',
      product_name: l.productName || l.name,
      name: l.name,
      unit_price: sar(l.unitCents),
      quantity: l.qty,
    })),
    delivery_fee: sar(order.shippingCents),
    delivery_label: order.shippingLabel,
    pay_later_fee: sar(order.feeCents || 0),
    discount: sar(order.discountCents || 0),
    discount_note: order.discountCents ? 'Loyalty Rewards balance used: ' + sar(order.discountCents) + ' SAR' : null,
    total: sar(order.totalCents),
  };
}

// Orders created before details.crm existed: rebuild what we can from the stored lines.
function fromStoredItems(order) {
  const lines = (order.items || [])
    .filter((i) => i && i.reference_id !== 'pay-later-fee')
    .map((i) => ({
      product_slug: i.reference_id || '',
      variant_label: '',
      product_name: i.name || i.title || 'Item',
      name: i.name || i.title || 'Item',
      unit_price: i.amount_cents != null ? sar(i.amount_cents) : Number(i.unit_price) || 0,
      quantity: Number(i.quantity) || 1,
    }));
  const items = lines.reduce((a, l) => a + l.unit_price * l.quantity, 0);
  const total = sar(order.amount_cents || 0);
  return { lines, delivery_fee: Math.max(Math.round((total - items) * 100) / 100, 0), delivery_label: 'Delivery and fees (from the order total)', pay_later_fee: 0, discount: 0, discount_note: null, total };
}

function customerOf(b) {
  const clean = (v) => (v && v !== 'NA' ? String(v) : '');
  return {
    customer_name: [b.first_name, b.last_name].filter(Boolean).join(' '),
    customer_phone: b.phone || b.phone_number || '',
    customer_email: b.email || '',
    customer_city: clean(b.city),
    customer_address: [b.street, b.building, b.apartment, b.postal_code].map(clean).filter(Boolean).join(', '),
  };
}

// A paid card_orders / tabby_orders row -> the CRM inbox.
async function sendPaidOrder(table, order) {
  if (!configured()) return false;
  const d = order.details || {};
  const payload = Object.assign(
    {
      order_ref: order.order_ref,
      source: table,
      method_label: d.method || (table === 'tabby_orders' ? 'Tabby (Pay in 4)' : 'Paymob'),
      payment_method: table === 'tabby_orders' ? 'Tabby' : 'Paymob',
      paid: true,
      paid_at: order.paid_at || null,
      ordered_at: order.created_at || null,
    },
    customerOf(d.billing || order.billing || {}),
    d.crm || fromStoredItems(order),
  );
  await crmRpc('bav3d_online_order_receive', { p_order: payload });
  return true;
}

// A bank transfer order (placed, not paid yet) -> the CRM inbox.
async function sendBankOrder(payload) {
  if (!configured()) return false;
  await crmRpc('bav3d_online_order_receive', { p_order: payload });
  return true;
}

module.exports = { crmDetails, sendPaidOrder, sendBankOrder };
