"""Audit hreflang + canonical pairs across the /3d/ store.

Every page that declares hreflang alternates must:
  * self-canonicalize (canonical == its own URL),
  * point to an existing page for each language,
  * be pointed back to by that page (reciprocal), with the same en/ar pair.

Usage: py scripts/check_hreflang.py   (exit code 1 if any problem is found)
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.blackarrowksa.com'

pages = {}
for f in glob.glob(os.path.join(ROOT, '3d', '**', 'index.html'), recursive=True):
    rel = os.path.relpath(f, ROOT).replace('\\', '/')
    path = '/' + rel[:-len('index.html')]
    s = open(f, encoding='utf-8').read()
    canon = re.search(r'rel="canonical" href="([^"]*)"', s)
    alts = dict(re.findall(r'hreflang="([^"]*)" href="([^"]*)"', s))
    pages[path] = (canon.group(1) if canon else None, alts)

problems = []
for path, (canon, alts) in pages.items():
    if not alts:
        continue
    if canon != SITE + path:
        problems.append(('canonical is not the page itself', path, canon))
    for lang, url in alts.items():
        if lang == 'x-default':
            continue
        target = url.replace(SITE, '')
        if target not in pages:
            problems.append(('alternate points to a missing page', path, url))
            continue
        back = pages[target][1]
        if back.get('en') != alts.get('en') or back.get('ar') != alts.get('ar'):
            problems.append(('not reciprocal', path, url))
    if SITE + path not in (alts.get('en'), alts.get('ar')):
        problems.append(('page does not list itself', path, ''))

with_alts = sum(1 for v in pages.values() if v[1])
print('%d pages checked, %d declare hreflang, %d problem(s)' % (len(pages), with_alts, len(problems)))
for p in problems[:25]:
    print('  ', p)
sys.exit(1 if problems else 0)
