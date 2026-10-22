#!/usr/bin/env python3
"""Adds FAQPage structured data (JSON-LD) to every 3D blog article, EN and AR, that has a
"Frequently asked questions" / "الأسئلة الشائعة" section: each <h3> question and the <p>
answer under it. Helps Google and AI assistants quote the answers. Pages that already carry
their own FAQPage are left alone. Safe to re-run: the block it adds is replaced, not duplicated.

Run after the blog generators: python scripts/add_blog_faq_schema.py
"""
import glob
import html as htmllib
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MARK = 'id="b3d-faq-jsonld"'
HEADINGS = ('Frequently asked questions', 'Frequently Asked Questions', 'FAQ', 'الأسئلة الشائعة', 'أسئلة شائعة')


def text(fragment):
    return re.sub(r'\s+', ' ', htmllib.unescape(re.sub(r'<[^>]+>', '', fragment))).strip()


def faq_pairs(page):
    m = re.search(r'<h2>\s*(?:' + '|'.join(map(re.escape, HEADINGS)) + r')\s*</h2>(.*?)(?=<h2|<div class="b3d-article__cta"|</article>)', page, re.S)
    if not m:
        return []
    return [(text(q), text(a)) for q, a in re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', m.group(1), re.S) if text(q) and text(a)]


def main():
    added = skipped = 0
    for path in glob.glob(os.path.join(ROOT, '3d', 'blog', '*', 'index.html')) + glob.glob(os.path.join(ROOT, '3d', 'ar', 'blog', '*', 'index.html')):
        with open(path, encoding='utf-8') as f:
            page = f.read()
        page = re.sub(r'\n\s*<script type="application/ld\+json" ' + MARK + r'>.*?</script>', '', page, flags=re.S)
        if '"FAQPage"' in page:
            skipped += 1
            continue
        pairs = faq_pairs(page)
        if not pairs:
            continue
        data = {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in pairs],
        }
        block = '\n  <script type="application/ld+json" ' + MARK + '>' + json.dumps(data, ensure_ascii=False) + '</script>'
        page = page.replace('</head>', block + '\n</head>', 1)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(page)
        added += 1
    print('FAQPage added:', added, '| already had one:', skipped)


if __name__ == '__main__':
    main()
