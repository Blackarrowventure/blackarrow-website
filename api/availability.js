// Stock and prices from the CRM's Website Inventory tab, for the store pages.
// Read through the server so the CRM key never reaches the browser.
const { fetchRows } = require('./_lib/crm-catalog');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  const rows = await fetchRows();
  // A CRM change shows on the site within about a minute.
  res.setHeader('Cache-Control', rows.length ? 'public, s-maxage=60, stale-while-revalidate=300' : 'no-store');
  return res.status(200).json({
    rows,
    // Kept for pages still running an older store script.
    unavailable: rows.filter((r) => !r.available).map((r) => ({ id: r.id, variant: r.variant })),
  });
};
