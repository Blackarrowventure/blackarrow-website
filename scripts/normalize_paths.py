"""
Normalise bare-relative URLs on the 6 root-level pages to root-absolute.

Why this is needed, not cosmetic:

  Nested pages (services/*, solutions/*, resources/*) are already 100%
  root-absolute. Root pages are MIXED - index.html alone has 22 root-absolute
  and 64 relative references, and its own footer already links
  /services/ev-charging-solutions/.

  The Arabic build copies each page to /ar/<path>. A relative "assets/css/
  styles.css" on /ar/about.html resolves to /ar/assets/css/styles.css, which
  does not exist. Every relative reference would break in the Arabic tree.

  Normalising first also makes head/nav/footer text-identical across all
  pages, which collapses the generator's link-rewrite rules to a single case.

Safety rule: a value is only rewritten if the resolved target EXISTS ON DISK.
Anything unresolvable is reported and left alone.

    py scripts/normalize_paths.py --check
    py scripts/normalize_paths.py --apply
"""

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
from _htmlloc import locate, splice, read, write

ROOT = Path(__file__).parent.parent
MANIFEST = json.loads((Path(__file__).parent / 'pages.json').read_text('utf-8'))

EXTERNAL = ('http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:', '//')
URL_ATTRS = ('href', 'src', 'action', 'poster')

# Only root-level pages have the mixed-path problem.
ROOT_PAGES = [e['src'] for e in MANIFEST['pages'] if '/' not in e['src']]


def normalise(value):
    """Return the root-absolute form of a bare-relative URL, or None."""
    if not value or value.startswith(EXTERNAL) or value.startswith('#'):
        return None
    if value.startswith('/'):
        return None  # already absolute
    path, _, tail = value.partition('#')
    path, _, query = path.partition('?')
    if not path:
        return None
    target = ROOT / path
    exists = target.exists() or (target / 'index.html').exists()
    if not exists:
        return None
    out = '/' + path
    if query:
        out += '?' + query
    if tail:
        out += '#' + tail
    return out


def process(page_rel, apply):
    src, bom = read(ROOT / page_rel)
    loc = locate(src)
    edits = []
    changed = skipped = 0

    for tag, attrs, start, end, raw in loc.tags:
        new_raw = raw
        for attr in URL_ATTRS:
            if attr not in attrs:
                continue
            value = attrs[attr] or ''
            new_value = normalise(value)
            if new_value is None:
                if value and not value.startswith(EXTERNAL) and not value.startswith(('#', '/')):
                    skipped += 1
                    print(f'    SKIP (unresolved) <{tag} {attr}="{value}">')
                continue
            for quote in ('"', "'"):
                needle = f'{attr}={quote}{value}{quote}'
                if needle in new_raw:
                    new_raw = new_raw.replace(needle, f'{attr}={quote}{new_value}{quote}', 1)
                    changed += 1
                    break

        # srcset: comma-separated "url descriptor" pairs
        if 'srcset' in attrs and attrs['srcset']:
            old_set = attrs['srcset']
            parts = []
            touched = False
            for part in old_set.split(','):
                bits = part.strip().split(None, 1)
                if not bits:
                    continue
                url = bits[0]
                new_url = normalise(url)
                if new_url:
                    url = new_url
                    touched = True
                parts.append(' '.join([url] + bits[1:]))
            if touched:
                new_srcset = ', '.join(parts)
                for quote in ('"', "'"):
                    needle = f'srcset={quote}{old_set}{quote}'
                    if needle in new_raw:
                        new_raw = new_raw.replace(needle, f'srcset={quote}{new_srcset}{quote}', 1)
                        changed += 1
                        break

        if new_raw != raw:
            edits.append((start, end, new_raw))

    if edits and apply:
        write(ROOT / page_rel, splice(src, edits), bom)
    return changed, skipped


def main():
    apply = '--apply' in sys.argv
    total = total_skipped = 0
    for page in ROOT_PAGES:
        print(f'  {page}')
        changed, skipped = process(page, apply)
        print(f'    {changed} rewritten, {skipped} skipped')
        total += changed
        total_skipped += skipped
    verb = 'Rewrote' if apply else 'Would rewrite'
    print(f'\n{verb} {total} reference(s) across {len(ROOT_PAGES)} root pages'
          f' ({total_skipped} skipped)')
    if not apply:
        print('(dry run - pass --apply to write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
