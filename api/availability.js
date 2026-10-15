// Stock rules from the CRM's Website Inventory tab. Read through the server so
// the CRM key never reaches the browser. Per product: once a product has any
// row there, the CRM decides all of its options (an option with no row is
// out of stock). Products with no rows keep what 3d-products.json says.
const rewards = require('./_lib/rewards');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  if (!rewards.configured()) {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ rows: [], unavailable: [] });
  }
  try {
    const data = await rewards.crmRpc('bav3d_website_availability', {});
    const rows = (Array.isArray(data) ? data : [])
      .filter((r) => r && r.product_slug)
      .map((r) => ({ id: r.product_slug, variant: r.variant_label || '', available: r.available !== false }));
    // A CRM change shows on the site within about a minute.
    res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300');
    return res.status(200).json({
      rows,
      // Kept for pages still running the previous store script.
      unavailable: rows.filter((r) => !r.available).map((r) => ({ id: r.id, variant: r.variant })),
    });
  } catch (e) {
    console.error('availability failed:', e.message, e.detail || '');
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ rows: [], unavailable: [] });
  }
};
