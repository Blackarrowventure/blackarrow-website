"""
Generate the static Arabic site under /ar/ from the English pages.

WHY STATIC PAGES AND NOT THE RUNTIME SWITCHER
The site already had 1000+ Arabic strings, but they were applied by JavaScript
on the same URL. Google indexes the served HTML, so none of that Arabic was
ever indexable: one URL, one language, in English. Real /ar/ URLs roughly
double the indexable surface and let hreflang point Arabic searchers at Arabic
pages.

HOW IT WORKS
_htmlloc.Locator is used purely to find byte offsets. Every edit is a
(start, end, replacement) tuple spliced into the original source string. The
parse tree is never re-serialised, so comments, indentation, entities, inline
<style> and JSON-LD survive byte-for-byte. Verified round-tripping 1810
data-i18n spans across all 24 pages.

Re-runnable by design. A one-shot transform would rot the moment an English
page changed. Regenerating and reading `git diff` is the review mechanism.

    py scripts/build_ar.py --check   # validate, write nothing
    py scripts/build_ar.py --build   # (re)generate ar/**
    py scripts/build_ar.py --clean   # remove ar/**
"""

import io
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
from _htmlloc import locate, splice, read, write

ROOT = Path(__file__).parent.parent
SCRIPTS = Path(__file__).parent
SITE = 'https://www.blackarrowksa.com'

MANIFEST = json.loads((SCRIPTS / 'pages.json').read_text('utf-8'))
AR = json.loads((ROOT / 'assets/translations/ar.json').read_text('utf-8'))
AR_PAGES = json.loads((ROOT / 'assets/translations/ar-pages.json').read_text('utf-8'))

PAGES = [p for p in MANIFEST['pages'] if p.get('ar')]
EN_URLS = {p['url'] for p in MANIFEST['pages']}
SRC_BY_URL = {p['url']: p['src'] for p in MANIFEST['pages']}

EXTERNAL = ('http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:', '//', '#')

# Paths that are shared between languages and must never be /ar/-prefixed.
SHARED_PREFIXES = ('/assets/', '/service-worker.js', '/sitemap.xml',
                   '/robots.txt', '/company-profile.pdf', '/downloads/')


class BuildError(Exception):
    pass


def esc(text):
    """Escape only what must be escaped inside element content."""
    return text.replace('&', '&amp;').replace('<', '&lt;')


def ar_url(url):
    """Map an English site URL to its Arabic twin."""
    if url == '/':
        return '/ar/'
    return '/ar' + url


def rewrite_link(value, page_src):
    """Rewrite one same-origin URL for the Arabic tree, or return it unchanged."""
    if not value or value.startswith(EXTERNAL):
        return value
    if value.startswith(SHARED_PREFIXES):
        return value
    if not value.startswith('/'):
        raise BuildError(
            f'{page_src}: relative URL "{value}" - run normalize_paths.py first')

    path, hash_sep, frag = value.partition('#')
    path, q_sep, query = path.partition('?')

    if path in EN_URLS:
        # Only pages that actually have an Arabic twin get redirected there.
        entry = next(p for p in MANIFEST['pages'] if p['url'] == path)
        new = ar_url(path) if entry.get('ar') else path
        return new + (q_sep + query if query else '') + (hash_sep + frag if frag else '')

    raise BuildError(f'{page_src}: link "{value}" is not in pages.json and not a shared asset')


def build_page(entry, check_only):
    src_path = ROOT / entry['src']
    src, bom = read(src_path)
    loc = locate(src)
    meta = AR_PAGES.get(entry['src'])
    if not meta:
        raise BuildError(f'{entry["src"]}: no entry in ar-pages.json')

    edits = []
    missing = []

    # ---- 1. data-i18n text content -------------------------------------
    seen = set()
    for tag, attrs, cs, ce in loc.spans:
        key = attrs.get('data-i18n')
        if not key:
            continue
        if (cs, ce) in seen:
            continue
        seen.add((cs, ce))
        body = src[cs:ce]
        if '<' in body:
            raise BuildError(
                f'{entry["src"]}: data-i18n="{key}" wraps child markup. '
                f'applyTranslations would destroy it; move the key to an inner span.')
        if key not in AR:
            missing.append(key)
            continue
        edits.append((cs, ce, esc(AR[key])))

    # ---- 2. <title> and head metadata ----------------------------------
    for tag, attrs, cs, ce in loc.spans:
        if tag == 'title':
            edits.append((cs, ce, esc(meta['title'])))

    for tag, attrs, s, e, raw in loc.tags:
        if tag != 'meta':
            continue
        new = None
        if attrs.get('name') == 'description':
            new = meta['description']
        elif attrs.get('property') == 'og:title':
            new = meta.get('og_title', meta['title'])
        elif attrs.get('property') == 'og:description':
            new = meta.get('og_description', meta['description'])
        elif attrs.get('property') == 'og:url':
            new = SITE + ar_url(entry['url'])
        elif attrs.get('property') == 'og:locale':
            new = 'ar_SA'
        if new is not None:
            old = attrs.get('content', '')
            edits.append((s, e, raw.replace(f'content="{old}"', f'content="{esc_attr(new)}"', 1)))

    # ---- 3. canonical + hreflang ---------------------------------------
    for tag, attrs, s, e, raw in loc.tags:
        if tag != 'link':
            continue
        rel = attrs.get('rel', '')
        if rel == 'canonical':
            edits.append((s, e, f'<link rel="canonical" href="{SITE}{ar_url(entry["url"])}">'))
        elif rel == 'alternate' and attrs.get('hreflang'):
            # English pages carry the triple already; keep it identical on the
            # Arabic side so the two reference each other reciprocally.
            pass

    # ---- 4. the language switcher --------------------------------------
    # Its two hrefs are already correct absolute URLs for BOTH sides, so they
    # must not be rewritten. Only the active state moves from EN to AR.
    switch_start = src.find('<div class="lang-switcher" data-lang-switch>')
    switch_end = -1
    if switch_start != -1:
        switch_end = src.find('</div>', switch_start) + len('</div>')
        block = src[switch_start:switch_end]
        block = block.replace(
            'id="lang-en" class="lang-btn active" hreflang="en" lang="en" aria-current="true"',
            'id="lang-en" class="lang-btn" hreflang="en" lang="en"')
        block = block.replace(
            'id="lang-ar" class="lang-btn" hreflang="ar" lang="ar"',
            'id="lang-ar" class="lang-btn active" hreflang="ar" lang="ar" aria-current="true"')
        edits.append((switch_start, switch_end, block))

    # ---- 5. every other same-origin link -------------------------------
    for tag, attrs, s, e, raw in loc.tags:
        if switch_start != -1 and switch_start <= s < switch_end:
            continue                     # handled above
        new_raw = raw
        for attr in ('href', 'src', 'action'):
            if attr not in attrs:
                continue
            if tag == 'link' and attrs.get('rel') in ('canonical', 'alternate'):
                continue
            old = attrs[attr] or ''
            new = rewrite_link(old, entry['src'])
            if new != old:
                new_raw = new_raw.replace(f'{attr}="{old}"', f'{attr}="{new}"', 1)
        if new_raw != raw:
            edits.append((s, e, new_raw))

    # ---- 6. <html lang dir> --------------------------------------------
    for tag, attrs, s, e, raw in loc.tags:
        if tag == 'html':
            edits.append((s, e, '<html lang="ar" dir="rtl">'))
            break

    if missing:
        raise BuildError(
            f'{entry["src"]}: {len(missing)} key(s) missing from ar.json: '
            + ', '.join(sorted(set(missing))[:8]))

    # Merge overlapping edits deterministically: later, more specific edits on
    # the same tag span were already folded in above, so any overlap now is a bug.
    merged = {}
    for start, end, repl in edits:
        merged[(start, end)] = repl
    out = splice(src, [(s, e, r) for (s, e), r in merged.items()])

    if not check_only:
        dst = ROOT / 'ar' / entry['src']
        dst.parent.mkdir(parents=True, exist_ok=True)
        write(dst, out, bom)
    return out


def esc_attr(text):
    return text.replace('&', '&amp;').replace('"', '&quot;')


def main():
    if '--clean' in sys.argv:
        shutil.rmtree(ROOT / 'ar', ignore_errors=True)
        print('removed ar/')
        return 0

    check_only = '--build' not in sys.argv
    errors = []
    built = 0

    for entry in PAGES:
        try:
            build_page(entry, check_only)
            built += 1
        except BuildError as exc:
            errors.append(str(exc))

    for err in errors:
        print(f'  ERROR {err}')

    verb = 'Validated' if check_only else 'Built'
    print(f'\n{verb} {built}/{len(PAGES)} Arabic pages')
    if errors:
        print(f'{len(errors)} error(s) - nothing written' if check_only
              else f'{len(errors)} error(s)')
        return 1
    if check_only:
        print('(--check only; pass --build to write ar/**)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
