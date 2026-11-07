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
    lines.push({ id: product.id, name, productName: product.name, brand: product.brand || '', category: product.category, variantLabel: variant && variant.label ? variant.label : '', unitCents, qty });
    itemsCents += unitCents * qty;
    if (product.category === '3D Artwork') artworkCents += unitCents * qty;
    categories.add(product.category);
  }
  // Free Regular delivery: any order with a 3D printer, 3D artwork from 100 SAR, anything from 3,000 SAR.
  const freeShipping = categories.has('3D Printers') || artworkCents >= FREE_SHIP_ARTWORK_MIN * 100 || itemsCents >= FREE_SHIP_ORDER_MIN * 100;
  return { lines, itemsCents, freeShipping, categories };
}

// The first cart line asking for more than is in hand (the CRM's max_qty, see crm-catalog.js),
// as { name, max }; null when everything fits. Lines for the same option are added up.
function stockProblem(items, products) {
  const byId = new Map((products || catalog.products).map((p) => [p.id, p]));
  const wanted = new Map();
  for (const item of Array.isArray(items) ? items : []) {
    const product = byId.get(item && item.productId);
    if (!product) continue;
    const vi = item.variantIndex == null ? null : Number(item.variantIndex);
    const variant = vi != null && product.variants ? product.variants[vi] : null;
    const max = variant ? variant.maxQty : product.maxQty;
    if (max == null) continue;
    const key = product.id + '|' + vi;
    const qty = (wanted.get(key) || 0) + (Number(item.qty) || 0);
    wanted.set(key, qty);
    if (qty > max) return { name: variant && variant.label ? product.name + ' - ' + variant.label : product.name, max };
  }
  return null;
}

// Pay-later (Tabby / Tamara) service fee: 100 SAR with a printer, 50 SAR for
// filament with no printed items, otherwise none.
function bnplFeeCents(cats) {
  if (cats.has('3D Printers')) return 10000;
  if (cats.has('Filament') && !cats.has('3D Artwork')) return 5000;
  return 0;
}

// Everything that decides the final amount, in one place.
//   shipping: 'regular' | 'fast' | 'pickup'; payLater: add the BNPL fee;
//   rewards: { discountCents, freeDelivery } from api/_lib/rewards.js
//   products: the catalog with the CRM's stock and prices applied
//   (crm-catalog.liveProducts); defaults to the plain catalog file.
//   city: the customer's City field (Khobar / Dammam get free Standard delivery).
// Free Standard delivery to Khobar and Dammam (owner's rule, 6 Nov 2026). Matched on the
// customer's City field, English or Arabic; same test as isFreeCity() in 3d-store.js.
// Free Standard delivery to Khobar / Dammam. Same test as the checkout (3d-store.js isFreeCity):
// the usual spellings, plus small typos ("Kobar", "Damam", "الدمامم") via edit distance.
const FREE_CITY_NAMES = ['khobar', 'khubar', 'alkhobar', 'khober', 'dammam', 'damam', 'خبر', 'دمام'];
function cityNorm(s) {
  s = String(s || '').toLowerCase().trim()
    .replace(/[\u064B-\u0652\u0640]/g, '').replace(/[أإآ]/g, 'ا').replace(/ة/g, 'ه').replace(/ى/g, 'ي')
    .replace(/^(al|el|ad|ar|as|at|an|az)[\s-]+/, '').replace(/^ال/, '');
  return s.replace(/[^a-z\u0621-\u064A]/g, '');
}
function cityDist(a, b, max) {
  if (Math.abs(a.length - b.length) > max) return max + 1;
  let prev = [];
  for (let j = 0; j <= b.length; j++) prev[j] = j;
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    for (let j = 1; j <= b.length; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    prev = cur;
  }
  return prev[b.length];
}
function freeCity(city) {
  if (/khobar|khubar|dammam|damam|الخبر|خبر|الدمام|دمام/i.test(String(city || ''))) return true;
  const q = cityNorm(city);
  if (q.length < 4) return false;
  const max = q.length >= 7 ? 2 : 1;
  return FREE_CITY_NAMES.some(n => cityDist(q, n, max) <= max);
}

// Order email lines grouped by brand, then product, one line per colour/option
// (same layout as groupedSummary() in 3d/assets/js/3d-store.js):
//   KINGROON — PLA Basic Filament 1.75 mm (1 kg)
//      • Black ×1 — 65 SAR
//   (blank line)
//   Bambu Lab — A1 mini ×1 — 1,699 SAR
function groupedSummary(lines, sar) {
  const groups = [];
  const byId = new Map();
  for (const l of lines) {
    if (!byId.has(l.id)) { const g = { l, items: [] }; byId.set(l.id, g); groups.push(g); }
    byId.get(l.id).items.push(l);
  }
  const brandOrder = [];
  for (const g of groups) if (!brandOrder.includes(g.l.brand)) brandOrder.push(g.l.brand);
  groups.sort((a, b) => brandOrder.indexOf(a.l.brand) - brandOrder.indexOf(b.l.brand));
  const out = [];
  groups.forEach((g, i) => {
    if (i) out.push('');
    const brand = g.l.brand;
    let name = g.l.productName;
    if (brand && name.toLowerCase().startsWith(brand.toLowerCase() + ' ')) name = name.slice(brand.length + 1);
    const head = brand ? brand + ' — ' + name : name;
    if (g.items.length === 1 && !g.items[0].variantLabel) {
      out.push(head + ' ×' + g.items[0].qty + ' — ' + sar(g.items[0].unitCents * g.items[0].qty));
      return;
    }
    out.push(head);
    for (const l of g.items) out.push('   • ' + (l.variantLabel ? l.variantLabel + ' ' : '') + '×' + l.qty + ' — ' + sar(l.unitCents * l.qty));
  });
  out.push('');
  out.push(itemCountLine(lines));
  return out;
}

// "Items: 10 filaments · 1 printer (11 in total)" — same wording as itemCountLine() in 3d-store.js.
const COUNT_WORDS = [['3D Printers', 'printer', 'printers'], ['Filament', 'filament', 'filaments'],
  ['Accessories', 'accessory', 'accessories'], ['3D Artwork', '3D print', '3D prints'], ['Other', 'other item', 'other items']];
function itemCountLine(lines) {
  const by = {};
  let all = 0;
  for (const l of lines) { by[l.category] = (by[l.category] || 0) + l.qty; all += l.qty; }
  const parts = [];
  for (const [cat, one, many] of COUNT_WORDS) {
    const n = by[cat];
    if (n) { parts.push(n + ' ' + (n === 1 ? one : many)); delete by[cat]; }
  }
  for (const k of Object.keys(by)) parts.push(by[k] + ' ' + String(k).toLowerCase());
  return 'Items: ' + parts.join(' · ') + ' (' + all + ' in total)';
}

function buildOrder(items, shipping, payLater, rewards, products, city) {
  const priced = priceCart(items, products);
  if (!priced) return { error: 'invalid_cart' };
  if (shipping !== 'regular' && shipping !== 'fast' && shipping !== 'pickup') return { error: 'invalid_shipping' };

  // Free delivery only ever waives Regular shipping; Fast always stays paid. Self pickup is always free.
  const pickup = shipping === 'pickup';
  const free = pickup || (shipping === 'regular' && (priced.freeShipping || !!(rewards && rewards.freeDelivery) || freeCity(city)));
  const shippingCents = free ? 0 : shipping === 'fast' ? 5000 : 3000;
  const shippingLabel = pickup ? 'Self pickup (Free)'
    : (shipping === 'fast' ? 'Fast shipping' : 'Regular shipping') + (free ? ' (Free)' : '');
  const feeCents = payLater ? bnplFeeCents(priced.categories) : 0;
  const discountCents = Math.min((rewards && rewards.discountCents) || 0, priced.itemsCents);
  const totalCents = priced.itemsCents - discountCents + shippingCents + feeCents;

  const sar = (c) => (c / 100).toLocaleString('en-US') + ' SAR';
  const summary = groupedSummary(priced.lines, sar);
  if (discountCents) summary.push('Black Arrow Loyalty Rewards balance used: -' + sar(discountCents));
  if (feeCents) summary.push('Pay-later service fee: ' + sar(feeCents));
  summary.push('Shipping: ' + shippingLabel + ' — ' + (free ? 'Free' : sar(shippingCents)));
  summary.push('Grand Total: ' + sar(totalCents));

  return Object.assign({}, priced, { shippingCents, shippingLabel, feeCents, discountCents, totalCents, summary });
}

module.exports = { buildOrder, groupedSummary, stockProblem, freeCity, FREE_SHIP_ARTWORK_MIN, FREE_SHIP_ORDER_MIN };
