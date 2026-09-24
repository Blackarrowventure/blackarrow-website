#!/usr/bin/env python3
"""Adds every /3d/ store URL (homepage, shop, categories, products, blog,
compare — English + the new Arabic mirrors) to the site-wide sitemap.xml.
Idempotent: strips any previously-added /3d/ block (marked by the
BEGIN/END comment below) before re-adding a fresh one, so it's safe to
re-run after generate_3d_static.py whenever the catalog changes.

Usage: python scripts/update_sitemap_3d.py
"""
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, 'sitemap.xml')
PRODUCTS_JSON = os.path.join(ROOT, '3d', 'assets', 'data', '3d-products.json')

SITE = 'https://www.blackarrowksa.com'
TODAY = date.today().isoformat()

CATEGORY_SLUGS = {
    '3D Printers': '3d-printers',
    'Filament': 'filament',
    'Accessories': 'accessories',
    '3D Artwork': '3d-artwork',
}

BLOG_SLUGS = [
    '3d-printer-maintenance-guide',
    'bambu-lab-a1-vs-a1-mini-vs-a2l',
    'best-3d-printer-for-beginners-saudi-arabia',
    'buy-3d-printer-saudi-arabia-price-guide',
    'multi-color-3d-printing-explained',
    'pla-vs-petg-vs-abs-filament-guide',
]

BEGIN_MARK = '  <!-- BEGIN /3d/ store URLs (managed by scripts/update_sitemap_3d.py) -->\n'
END_MARK = '  <!-- END /3d/ store URLs -->\n'


def url_block(loc, priority, changefreq, en=None, ar=None):
    lines = ['  <url>', '    <loc>' + loc + '</loc>', '    <lastmod>' + TODAY + '</lastmod>',
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

    for p in products:
        if p.get('available') is False:
            continue
        en = SITE + '/3d/product/' + p['id'] + '/'
        ar = SITE + '/3d/ar/product/' + p['id'] + '/'
        out.append(url_block(en, '0.85', 'weekly', en=en, ar=ar))
        out.append(url_block(ar, '0.85', 'weekly', en=en, ar=ar))

    for slug in ('3d-printing-service-saudi-arabia', 'shipping'):
        en = SITE + '/3d/' + slug + '/'
        ar = SITE + '/3d/ar/' + slug + '/'
        prio = '0.8' if slug != 'shipping' else '0.4'
        out.append(url_block(en, prio, 'monthly', en=en, ar=ar))
        out.append(url_block(ar, prio, 'monthly', en=en, ar=ar))

    for slug in BLOG_SLUGS:
        en = SITE + '/3d/blog/' + slug + '/'
        ar = SITE + '/3d/ar/blog/' + slug + '/'
        out.append(url_block(en, '0.6', 'monthly', en=en, ar=ar))
        out.append(url_block(ar, '0.6', 'monthly', en=en, ar=ar))

    out.append(END_MARK)
    return ''.join(out)


def main():
    with open(SITEMAP, encoding='utf-8') as f:
        content = f.read()

    if BEGIN_MARK in content:
        content = re.sub(re.escape(BEGIN_MARK) + '.*?' + re.escape(END_MARK), '', content, flags=re.DOTALL)

    new_block = build_3d_urls()
    content = content.replace('</urlset>', new_block + '</urlset>')

    with open(SITEMAP, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('sitemap updated')


if __name__ == '__main__':
    main()
