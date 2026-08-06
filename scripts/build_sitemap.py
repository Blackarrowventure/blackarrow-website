"""
Regenerate sitemap.xml from pages.json, with reciprocal xhtml:link hreflang
annotations for every English/Arabic pair.

Annotating alternates inside the sitemap (rather than relying on the <head>
links alone) is Google's recommended belt-and-braces approach: it tells the
crawler about the Arabic pages even before it has fetched the English one.

    py scripts/build_sitemap.py --check
    py scripts/build_sitemap.py --apply
"""

import io
import json
import sys
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
SITE = 'https://www.blackarrowksa.com'
MANIFEST = json.loads((Path(__file__).parent / 'pages.json').read_text('utf-8'))

# Confirmation pages must never be in the sitemap.
EXCLUDE = {'/thank-you.html'}

PRIORITY = {
    '/': '1.0',
    '/services.html': '0.9',
    '/contact.html': '0.8',
    '/about.html': '0.8',
}
CHANGEFREQ = {'/': 'weekly', '/services.html': 'weekly', '/resources/blog/': 'weekly'}


def priority(url):
    if url in PRIORITY:
        return PRIORITY[url]
    if url.startswith('/services/'):
        return '0.9'
    if url.startswith('/solutions/'):
        return '0.8'
    if url.startswith('/resources/'):
        return '0.7'
    return '0.6'


def ar_of(url):
    return '/ar/' if url == '/' else '/ar' + url


def entry(url, lastmod, has_ar, is_ar=False, en_url=None):
    lines = [
        '  <url>',
        f'    <loc>{SITE}{url}</loc>',
        f'    <lastmod>{lastmod}</lastmod>',
        f'    <changefreq>{CHANGEFREQ.get(en_url or url, "monthly")}</changefreq>',
        f'    <priority>{priority(en_url or url)}</priority>',
    ]
    if has_ar:
        base = en_url or url
        lines += [
            f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{base}"/>',
            f'    <xhtml:link rel="alternate" hreflang="ar" href="{SITE}{ar_of(base)}"/>',
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{base}"/>',
        ]
    lines.append('  </url>')
    return '\n'.join(lines)


def main():
    apply = '--apply' in sys.argv
    today = date.today().isoformat()

    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    en_count = ar_count = 0
    for page in MANIFEST['pages']:
        url = page.get('url')
        if not url or url in EXCLUDE:
            continue
        has_ar = bool(page.get('ar'))
        out.append(entry(url, today, has_ar))
        en_count += 1

    for page in MANIFEST['pages']:
        url = page.get('url')
        if not url or url in EXCLUDE or not page.get('ar'):
            continue
        out.append(entry(ar_of(url), today, True, is_ar=True, en_url=url))
        ar_count += 1

    out.append('</urlset>')
    xml = '\n'.join(out) + '\n'

    print(f'{en_count} English + {ar_count} Arabic = {en_count + ar_count} URLs')
    if apply:
        (ROOT / 'sitemap.xml').write_text(xml, encoding='utf-8')
        print('written to sitemap.xml')
    else:
        print('(dry run - pass --apply to write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
