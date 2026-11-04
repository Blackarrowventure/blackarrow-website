#!/usr/bin/env python3
"""Adds every /3d/ store URL (homepage, shop, categories, products, blog,
compare — English + the new Arabic mirrors) to the site-wide sitemap.xml.
Idempotent: strips any previously-added /3d/ block (marked by the
BEGIN/END comment below) before re-adding a fresh one, so it's safe to
re-run after generate_3d_static.py whenever the catalog changes.

<lastmod> is honest (5 Nov 2026): every URL in the sitemap (store and main site) gets the date
its page content last really changed - title, description, structured data (price, stock) or
the visible text of <main> - tracked by a fingerprint in scripts/sitemap-lastmod.json. A rebuild
that changes nothing keeps the old date. Stamping every page with today's date on each build
taught Google to ignore our dates, so a real price or stock change waited for a routine crawl.
The daily /api/cron/indexnow job reports the recently changed URLs to IndexNow (Bing etc.).

Usage: python scripts/update_sitemap_3d.py
"""
import hashlib
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, 'sitemap.xml')
PRODUCTS_JSON = os.path.join(ROOT, '3d', 'assets', 'data', '3d-products.json')

SITE = 'https://www.blackarrowksa.com'
LASTMOD_STATE = os.path.join(ROOT, 'scripts', 'sitemap-lastmod.json')
TODAY = date.today().isoformat()

CATEGORY_SLUGS = {
    '3D Printers': '3d-printers',
    'Filament': 'filament',
    'Accessories': 'accessories',
    '3D Artwork': '3d-artwork',
}

# Every post folder under /3d/blog/ (so new guides are picked up automatically).
BLOG_SLUGS = sorted(d for d in os.listdir(os.path.join(ROOT, '3d', 'blog'))
                    if os.path.isfile(os.path.join(ROOT, '3d', 'blog', d, 'index.html')))
# Pick up any newer article folder too, so a new post never misses the sitemap.
BLOG_SLUGS += sorted(d for d in os.listdir(os.path.join(ROOT, '3d', 'blog'))
                     if d not in BLOG_SLUGS and os.path.isfile(os.path.join(ROOT, '3d', 'blog', d, 'index.html')))

BEGIN_MARK = '  <!-- BEGIN /3d/ store URLs (managed by scripts/update_sitemap_3d.py) -->\n'
END_MARK = '  <!-- END /3d/ store URLs -->\n'


def url_block(loc, priority, changefreq, en=None, ar=None):
    lines = ['  <url>', '    <loc>' + loc + '</loc>', '    <lastmod>' + TODAY + '</lastmod>'  # replaced by the real date in apply_lastmods(),
              '    <changefreq>' + changefreq + '</changefreq>', '    <priority>' + priority + '</priority>']
    if en and ar:
        lines.append('    <xhtml:link rel="alternate" hreflang="en" href="' + en + '"/>')
        lines.append('    <xhtml:link rel="alternate" hreflang="ar" href="' + ar + '"/>')
        lines.append('    <xhtml:link rel="alternate" hreflang="x-default" href="' + en + '"/>')
    lines.append('  </url>')
    return '\n'.join(lines) + '\n'


def build_3d_urls():
    with open(PRODUCTS_JSON, encoding='utf-8') as f:
        products = json.load(f)['products']

    out = [BEGIN_MARK]

    out.append(url_block(SITE + '/3d/', '0.9', 'weekly', en=SITE + '/3d/', ar=SITE + '/3d/ar/'))
    out.append(url_block(SITE + '/3d/ar/', '0.9', 'weekly', en=SITE + '/3d/', ar=SITE + '/3d/ar/'))
    out.append(url_block(SITE + '/3d/shop/', '0.9', 'weekly', en=SITE + '/3d/shop/', ar=SITE + '/3d/ar/shop/'))
    out.append(url_block(SITE + '/3d/ar/shop/', '0.9', 'weekly', en=SITE + '/3d/shop/', ar=SITE + '/3d/ar/shop/'))
    out.append(url_block(SITE + '/3d/compare/', '0.4', 'monthly'))
    out.append(url_block(SITE + '/3d/blog/', '0.6', 'weekly', en=SITE + '/3d/blog/', ar=SITE + '/3d/ar/blog/'))
    out.append(url_block(SITE + '/3d/ar/blog/', '0.6', 'weekly', en=SITE + '/3d/blog/', ar=SITE + '/3d/ar/blog/'))

    for cat, slug in CATEGORY_SLUGS.items():
        en = SITE + '/3d/shop/' + slug + '/'
        ar = SITE + '/3d/ar/shop/' + slug + '/'
        out.append(url_block(en, '0.8', 'weekly', en=en, ar=ar))
        out.append(url_block(ar, '0.8', 'weekly', en=en, ar=ar))

    # Indexable brand landing pages (see BRAND_SLUGS in generate_3d_static.py):
    # only brands with enough available stock get one.
    for brand, slug in {'Bambu Lab': 'bambu-lab'}.items():
        if sum(1 for p in products if p.get('brand') == brand and p.get('available') is not False) >= 3:
            en = SITE + '/3d/brands/' + slug + '/'
            ar = SITE + '/3d/ar/brands/' + slug + '/'
            out.append(url_block(en, '0.8', 'weekly', en=en, ar=ar))
            out.append(url_block(ar, '0.8', 'weekly', en=en, ar=ar))

    # Out-of-stock products keep their page (and their ranking) — list them too.
    for p in products:
        en = SITE + '/3d/product/' + p['id'] + '/'
        ar = SITE + '/3d/ar/product/' + p['id'] + '/'
        out.append(url_block(en, '0.85', 'weekly', en=en, ar=ar))
        out.append(url_block(ar, '0.85', 'weekly', en=en, ar=ar))

    # Gift collections (/3d/gifts/<slug>/), whatever generate_3d_static.py built.
    gifts_dir = os.path.join(ROOT, '3d', 'gifts')
    for slug in sorted(os.listdir(gifts_dir)) if os.path.isdir(gifts_dir) else []:
        if os.path.isfile(os.path.join(gifts_dir, slug, 'index.html')):
            en = SITE + '/3d/gifts/' + slug + '/'
            ar = SITE + '/3d/ar/gifts/' + slug + '/'
            out.append(url_block(en, '0.7', 'weekly', en=en, ar=ar))
            out.append(url_block(ar, '0.7', 'weekly', en=en, ar=ar))

    if os.path.isfile(os.path.join(ROOT, '3d', 'deals', 'index.html')):
        out.append(url_block(SITE + '/3d/deals/', '0.8', 'weekly', en=SITE + '/3d/deals/', ar=SITE + '/3d/ar/deals/'))
        out.append(url_block(SITE + '/3d/ar/deals/', '0.8', 'weekly', en=SITE + '/3d/deals/', ar=SITE + '/3d/ar/deals/'))

    for slug in ('3d-printing-service-saudi-arabia', 'quote', 'business', 'shipping', 'reviews'):
        en = SITE + '/3d/' + slug + '/'
        ar = SITE + '/3d/ar/' + slug + '/'
        prio = '0.8' if slug in ('3d-printing-service-saudi-arabia', 'quote', 'business') else '0.4'
        out.append(url_block(en, prio, 'monthly', en=en, ar=ar))
        out.append(url_block(ar, prio, 'monthly', en=en, ar=ar))

    # English-only policy pages
    for slug in ('returns', 'terms'):
        out.append(url_block(SITE + '/3d/' + slug + '/', '0.3', 'yearly'))

    for slug in BLOG_SLUGS:
        en = SITE + '/3d/blog/' + slug + '/'
        ar = SITE + '/3d/ar/blog/' + slug + '/'
        out.append(url_block(en, '0.6', 'monthly', en=en, ar=ar))
        out.append(url_block(ar, '0.6', 'monthly', en=en, ar=ar))

    out.append(END_MARK)
    return ''.join(out)


def page_file(loc):
    """Local HTML file behind a sitemap URL, or None."""
    path = loc[len(SITE):] if loc.startswith(SITE) else None
    if path is None:
        return None
    f = os.path.join(ROOT, *[x for x in path.split('/') if x])
    if path.endswith('/'):
        f = os.path.join(f, 'index.html')
    return f if os.path.isfile(f) else None


def fingerprint(html):
    """What a visitor or Google sees change: title, description, JSON-LD and the text of <main>.
    Asset version strings (?v=...), scripts and styles are ignored so a code-only deploy is not a change."""
    parts = re.findall(r'<title>(.*?)</title>', html, re.S)
    parts += re.findall(r'<meta name="description" content="([^"]*)"', html)
    parts += re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    m = re.search(r'<main\b.*?</main>', html, re.S)
    if m:
        body = re.sub(r'<(script|style)\b.*?</\1>', ' ', m.group(0), flags=re.S)
        body = re.sub(r'\?v=[0-9a-z]+', '', body)
        parts.append(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body)))
    return hashlib.sha1('\n'.join(parts).encode('utf-8')).hexdigest()[:16]


def apply_lastmods(content):
    """Give every sitemap URL the date its page content last changed (see the module docstring)."""
    try:
        with open(LASTMOD_STATE, encoding='utf-8') as f:
            state = json.load(f)
    except (OSError, ValueError):
        state = {}
    new_state = {}
    changed = []

    def fix(m):
        block, loc = m.group(0), m.group(1)
        f = page_file(loc)
        if not f:
            return block
        with open(f, encoding='utf-8', errors='replace') as fh:
            h = fingerprint(fh.read())
        prev = state.get(loc)
        if prev and prev.get('h') == h:
            d = prev['d']
        else:
            d = TODAY
            if prev:
                changed.append(loc)
        new_state[loc] = {'h': h, 'd': d}
        old = re.search(r'<lastmod>[^<]*</lastmod>', block)
        if old:
            return block.replace(old.group(0), '<lastmod>' + d + '</lastmod>')
        return block.replace('</loc>', '</loc>\n    <lastmod>' + d + '</lastmod>', 1)

    content = re.sub(r'<url>\s*<loc>([^<]+)</loc>.*?</url>', fix, content, flags=re.S)
    with open(LASTMOD_STATE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(new_state, f, indent=0, sort_keys=True)
        f.write('\n')
    print('sitemap lastmod: %d pages changed since the last build' % len(changed))
    return content


def main():
    with open(SITEMAP, encoding='utf-8') as f:
        content = f.read()

    if BEGIN_MARK in content:
        content = re.sub(re.escape(BEGIN_MARK) + '.*?' + re.escape(END_MARK), '', content, flags=re.DOTALL)

    new_block = build_3d_urls()
    content = content.replace('</urlset>', new_block + '</urlset>')
    content = apply_lastmods(content)

    with open(SITEMAP, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('sitemap updated')


if __name__ == '__main__':
    main()
