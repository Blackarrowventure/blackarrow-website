// Stock and prices set in the CRM's Website Inventory tab, layered over
// 3d/assets/data/3d-products.json. Used by /api/availability (what the store
// shows) and by checkout pricing (what is charged), so the two always agree.
// The same rules run in the browser: applyCrmStock in 3d/assets/js/3d-store.js.
const catalog = require('../../3d/assets/data/3d-products.json');
const rewards = require('./rewards');

// -> [{ id, variant, available, price, oldPrice, preorder, maxQty }]; [] if the CRM can't be reached.
async function fetchRows() {
  if (!rewards.configured()) return [];
  let data;
  try {
    data = await rewards.crmRpc('bav3d_website_catalog', {});
  } catch (e) {
    // Before migration 0150 only the stock function exists.
    try { data = await rewards.crmRpc('bav3d_website_availability', {}); } catch (e2) { return []; }
  }
  return (Array.isArray(data) ? data : [])
    .filter((r) => r && r.product_slug)
    .map((r) => ({
      id: r.product_slug,
      variant: r.variant_label || '',
      available: r.available !== false,
      price: r.price_sar == null ? null : Number(r.price_sar),
      oldPrice: r.old_price_sar == null ? null : Number(r.old_price_sar),
      preorder: r.preorder === true,
      // In hand, when the item can only be sold from stock; null = no limit (supplier / pre-order).
      maxQty: r.max_qty == null ? null : Number(r.max_qty),
    }));
}

const key = (s) => String(s || '').trim().toLowerCase();

// Once a product has any CRM row, the CRM decides every option of it: an
// option with no row is out of stock. A shop product with no row at all is
// out of stock too (see the end of applyRows). A row's price replaces the catalog
// price; its old price (if any) is the crossed-out "was" price.
function applyRows(products, rows) {
  const byId = new Map(products.map((p) => [p.id, p]));
  const byProduct = new Map();
  for (const r of rows) {
    if (!byProduct.has(r.id)) byProduct.set(r.id, new Map());
    byProduct.get(r.id).set(key(r.variant), r);
  }
  for (const [id, crm] of byProduct) {
    const p = byId.get(id);
    if (!p) continue;
    const whole = crm.get('');
    if (p.variants && p.variants.length) {
      for (const v of p.variants) {
        const row = crm.get(key(v.label));
        v.available = row ? row.available : !!(whole && whole.available);
        const src = row || whole;
        if (src && src.maxQty != null) v.maxQty = src.maxQty;
        if (row && row.price != null) {
          v.price = row.price;
          if (row.oldPrice != null && row.oldPrice > row.price) v.oldPrice = row.oldPrice;
          else delete v.oldPrice;
        }
      }
      p.available = !(whole && !whole.available) && p.variants.some((v) => v.available !== false);
      for (const v of p.variants) {
        const row = crm.get(key(v.label));
        v.preorder = !!(row ? row.preorder : whole && whole.preorder);
      }
      const buyable = p.variants.filter((v) => v.available);
      if (buyable.length && buyable.every((v) => v.preorder)) p.preorder = true;
    } else {
      p.available = !!(whole && whole.available);
      if (whole && whole.preorder) p.preorder = true;
      if (whole && whole.maxQty != null) p.maxQty = whole.maxQty;
      if (whole && whole.price != null) {
        if (whole.oldPrice != null && whole.oldPrice > whole.price) {
          p.price = whole.oldPrice;
          p.onSale = true;
          p.salePrice = whole.price;
        } else {
          p.price = whole.price;
          p.onSale = false;
          delete p.salePrice;
        }
      }
    }
  }
  // The CRM's Website Inventory is the only stock list: a shop product (printer, filament,
  // accessory) that is not in it is out of stock. 3D Artwork is printed to order, and kits /
  // pick-bundles follow their parts. Only when the CRM answered (rows), never on an outage.
  if (rows.length) {
    for (const p of products) {
      if (byProduct.has(p.id) || p.category === '3D Artwork' || p.kit || p.bundlePick) continue;
      p.available = false;
      p.preorder = false;
      for (const v of p.variants || []) v.available = false;
    }
  }
  return products;
}

// A fresh copy of the catalog with the CRM's stock and prices applied.
async function liveProducts() {
  const products = JSON.parse(JSON.stringify(catalog.products));
  return applyRows(products, await fetchRows());
}

module.exports = { fetchRows, applyRows, liveProducts };
