// Which products the CRM's Website Inventory tab has marked Not Available
// (quantity 0, or switched off). Read through the server so the CRM key never
// reaches the browser. Only "unavailable" rows are returned; anything not
// listed keeps whatever 3d-products.json says.
const rewards = require('./_lib/rewards');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  if (!rewards.configured()) {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ unavailable: [] });
  }
  try {
    const rows = await rewards.crmRpc('bav3d_website_availability', {});
    const unavailable = (Array.isArray(rows) ? rows : [])
      .filter((r) => r && r.available === false)
      .map((r) => ({ id: r.product_slug, variant: r.variant_label || '' }));
    // A CRM change shows on the site within about a minute.
    res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300');
    return res.status(200).json({ unavailable });
  } catch (e) {
    console.error('availability failed:', e.message, e.detail || '');
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ unavailable: [] });
  }
};
