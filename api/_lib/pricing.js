// Server-side order pricing shared by Paymob and Tabby, recomputed from the
// catalog so a browser can never set its own prices, shipping or discount.
// Mirrors the cart page in 3d/assets/js/3d-store.js.
const catalog = require('../../3d/assets/data/3d-products.json');

const MAX_LINES = 20;
const MAX_QTY = 10;
// Free Regular delivery: 3D Artwork worth 100+ SAR, or a whole order of 3,000+ SAR.
const FREE_SHIP_ARTWORK_MIN = 100;
const FREE_SHIP_ORDER_MIN = 3000;

function unitPrice(product, variantIndex) {
  if (product.variants && product.variants.length) {
    const v = product.variants[variantIndex];
    if (!v || v.available === false) return null;
    return v.price;
  }
  if (product.available === false) return null;
  return product.onSale && product.salePrice != null ? product.salePrice : product.price;
}

function priceCart(items, products) {
  if (!Array.isArray(items) || items.length === 0 || items.length > MAX_LINES) return null;
  const byId = new Map((products || catalog.products).map((p) => [p.id, p]));
  const lines = [];
  let itemsCents = 0;
  let artworkCents = 0;
  const categories = new Set();
  for (const item of items) {
    const product = byId.get(item && item.productId);
    const qty = Number(item && item.qty);
    if (!product || !Number.isInteger(qty) || qty < 1 || qty > MAX_QTY) return null;
    const variantIndex = item.variantIndex == null ? null : Number(item.variantIndex);
    if (product.variants && product.variants.length && variantIndex == null) return null;
    const unit = unitPrice(product, variantIndex == null ? 0 : variantIndex);
    if (unit == null) return null;
    const unitCents = Math.round(unit * 100);
    const variant = product.variants && product.variants.length ? product.variants[variantIndex] : null;
    const name = variant && variant.label ? product.name + ' - ' + variant.label : product.name;
    lines.push({ id: product.id, name, unitCents, qty });
    itemsCents += unitCents * qty;
    if (product.category === '3D Artwork') artworkCents += unitCents * qty;
    categories.add(product.category);
  }
  const freeShipping = artworkCents >= FREE_SHIP_ARTWORK_MIN * 100 || itemsCents >= FREE_SHIP_ORDER_MIN * 100;
  return { lines, itemsCents, freeShipping, categories };
}

// Pay-later (Tabby / Tamara) service fee: 100 SAR with a printer, 50 SAR for
// filament with no printed items, otherwise none.
function bnplFeeCents(cats) {
  if (cats.has('3D Printers')) return 10000;
  if (cats.has('Filament') && !cats.has('3D Artwork')) return 5000;
  return 0;
}

// Everything that decides the final amount, in one place.
//   shipping: 'regular' | 'fast'; payLater: add the BNPL fee;
//   rewards: { discountCents, freeDelivery } from api/_lib/rewards.js
//   products: the catalog with the CRM's stock and prices applied
//   (crm-catalog.liveProducts); defaults to the plain catalog file.
function buildOrder(items, shipping, payLater, rewards, products) {
  const priced = priceCart(items, products);
  if (!priced) return { error: 'invalid_cart' };
  if (shipping !== 'regular' && shipping !== 'fast') return { error: 'invalid_shipping' };

  // Free delivery only ever waives Regular shipping; Fast always stays paid.
  const free = shipping === 'regular' && (priced.freeShipping || !!(rewards && rewards.freeDelivery));
  const shippingCents = free ? 0 : shipping === 'fast' ? 5000 : 3000;
  const shippingLabel = (shipping === 'fast' ? 'Fast shipping' : 'Regular shipping') + (free ? ' (Free)' : '');
  const feeCents = payLater ? bnplFeeCents(priced.categories) : 0;
  const discountCents = Math.min((rewards && rewards.discountCents) || 0, priced.itemsCents);
  const totalCents = priced.itemsCents - discountCents + shippingCents + feeCents;

  const sar = (c) => (c / 100).toLocaleString('en-US') + ' SAR';
  const summary = priced.lines.map((l) => l.qty + ' x ' + l.name + ' — ' + sar(l.unitCents * l.qty));
  if (discountCents) summary.push('Black Arrow Loyalty Rewards balance used: -' + sar(discountCents));
  if (feeCents) summary.push('Pay-later service fee: ' + sar(feeCents));
  summary.push('Shipping: ' + shippingLabel + ' — ' + (free ? 'Free' : sar(shippingCents)));
  summary.push('Grand Total: ' + sar(totalCents));

  return Object.assign({}, priced, { shippingCents, shippingLabel, feeCents, discountCents, totalCents, summary });
}

module.exports = { buildOrder, FREE_SHIP_ARTWORK_MIN, FREE_SHIP_ORDER_MIN };
