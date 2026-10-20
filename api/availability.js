// Stock and prices from the CRM's Website Inventory tab, for the store pages.
// Read through the server so the CRM key never reaches the browser.
//
// /api/availability/?check=1 explains what the website receives from the CRM:
// whether the CRM is connected, how many inventory rows came back, and which
// rows don't match any product or option on the website (those rows have no
// effect). Shows no keys or secrets — only product ids and option names.
const catalog = require('../3d/assets/data/3d-products.json');
const rewards = require('./_lib/rewards');
const { fetchRows } = require('./_lib/crm-catalog');

async function check() {
  const out = {
    crmConnected: rewards.configured(),
    crmProject: (process.env.CRM_SUPABASE_URL || 'https://iorbuqljfxifgtrdniwq.supabase.co').replace(/^https:\/\//, '').split('.')[0],
    catalogFunction: null,
    rows: 0,
    rowsWithNoMatchingProduct: [],
    rowsWithNoMatchingOption: [],
    productsControlledByCrm: [],
  };
  if (!out.crmConnected) {
    out.catalogFunction = 'not called: CRM_SUPABASE_SERVICE_ROLE_KEY is not set in Vercel';
    return out;
  }
  let data;
  try {
    data = await rewards.crmRpc('bav3d_website_catalog', {});
    out.catalogFunction = 'ok';
  } catch (e) {
    out.catalogFunction = 'error: ' + e.message + (e.detail ? ' (' + e.detail + ')' : '');
    return out;
  }
  const rows = Array.isArray(data) ? data : [];
  out.rows = rows.length;
  const byId = new Map(catalog.products.map((p) => [p.id, p]));
  const key = (s) => String(s || '').trim().toLowerCase();
  const seen = new Set();
  for (const r of rows) {
    const p = byId.get(r.product_slug);
    const label = r.variant_label || '';
    if (!p) { out.rowsWithNoMatchingProduct.push({ product: r.product_slug, option: label }); continue; }
    if (label && !(p.variants || []).some((v) => key(v.label) === key(label))) {
      out.rowsWithNoMatchingOption.push({ product: r.product_slug, option: label, websiteOptions: (p.variants || []).map((v) => v.label) });
    }
    if (!seen.has(p.id)) { seen.add(p.id); out.productsControlledByCrm.push(p.id); }
  }
  return out;
}

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  if (req.query && req.query.check) {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json(await check());
  }
  const rows = await fetchRows();
  // A CRM change shows on the site within about a minute (30 s cache, 30 s grace).
  res.setHeader('Cache-Control', rows.length ? 'public, s-maxage=30, stale-while-revalidate=30' : 'no-store');
  return res.status(200).json({
    rows,
    // Kept for pages still running an older store script.
    unavailable: rows.filter((r) => !r.available).map((r) => ({ id: r.id, variant: r.variant })),
  });
};
