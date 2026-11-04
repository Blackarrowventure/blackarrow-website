// Daily IndexNow run (Vercel Cron, vercel.json, 04:30 Saudi time - after the nightly CRM price
// sync at 03:00 has published). Reads the live sitemap and tells IndexNow (Bing, Yandex, Seznam,
// Naver; Bing also feeds ChatGPT and Copilot search) which pages changed in the last 2 days, so a
// new price or stock status is re-crawled within hours instead of at the next routine visit.
//
// The <lastmod> dates are honest: scripts/update_sitemap_3d.py only moves a page's date when its
// content really changes. Google does not take IndexNow; it reads the same sitemap dates.
//
// Needs, in Vercel: CRON_SECRET (already set for the birthday job). The IndexNow key is public by
// design: it is the file /75f0d41bdcdc770501cf2d9723a86ede.txt at the site root, which proves to
// IndexNow that the submission comes from the site owner. ?dry=1 lists the URLs without sending.
const SITE = 'https://www.blackarrowksa.com';
const HOST = 'www.blackarrowksa.com';
const KEY = '75f0d41bdcdc770501cf2d9723a86ede';
const DAYS = 2;

module.exports = async (req, res) => {
  const secret = process.env.CRON_SECRET;
  const auth = String(req.headers.authorization || '');
  if (!secret || auth !== 'Bearer ' + secret) return res.status(401).json({ error: 'unauthorized' });

  let xml;
  try {
    const r = await fetch(SITE + '/sitemap.xml', { headers: { 'Cache-Control': 'no-cache' } });
    if (!r.ok) throw new Error('sitemap HTTP ' + r.status);
    xml = await r.text();
  } catch (e) {
    console.error('indexnow: sitemap fetch failed:', e.message);
    return res.status(502).json({ error: 'sitemap_unavailable' });
  }

  const since = new Date(Date.now() - DAYS * 86400000).toISOString().slice(0, 10);
  const urls = [];
  for (const m of xml.matchAll(/<url>\s*<loc>([^<]+)<\/loc>\s*<lastmod>([^<]+)<\/lastmod>/g)) {
    if (m[2].slice(0, 10) >= since && m[1].startsWith(SITE + '/')) urls.push(m[1]);
  }
  if (!urls.length) return res.status(200).json({ ok: true, submitted: 0 });
  if (req.query && req.query.dry) return res.status(200).json({ ok: true, dry: true, urls });

  try {
    const r = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ host: HOST, key: KEY, keyLocation: SITE + '/' + KEY + '.txt', urlList: urls.slice(0, 10000) }),
    });
    // 200 = accepted, 202 = accepted (key check pending). Anything else is logged.
    if (r.status !== 200 && r.status !== 202) {
      const body = (await r.text()).slice(0, 300);
      console.error('indexnow rejected:', r.status, body);
      return res.status(502).json({ error: 'indexnow_rejected', status: r.status });
    }
    console.log('indexnow: submitted', urls.length, 'urls, status', r.status);
    return res.status(200).json({ ok: true, submitted: urls.length, status: r.status });
  } catch (e) {
    console.error('indexnow failed:', e.message);
    return res.status(502).json({ error: 'indexnow_unreachable' });
  }
};
