"""
Resolve every same-origin href/src/srcset/action on every site page against
disk. Exits non-zero if anything fails to resolve.

This is the gate for path normalisation (Phase 3) and for the Arabic build
(Phase 6): if a link cannot be resolved locally it is either dead in
production or ambiguous to the generator.

    py scripts/check_links.py            # all pages
    py scripts/check_links.py --baseline # write the known-bad baseline
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _htmlloc import locate, read

ROOT = Path(__file__).parent.parent
MANIFEST = json.loads((Path(__file__).parent / 'pages.json').read_text('utf-8'))

# Schemes and forms we never resolve against disk.
EXTERNAL_PREFIXES = (
    'http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:', '//',
)

URL_ATTRS = {'href', 'src', 'action', 'poster'}


def candidates(value, page_rel):
    """Filesystem paths a URL value could resolve to."""
    path = value.split('#', 1)[0].split('?', 1)[0]
    if not path:
        return []
    if path.startswith('/'):
        base = ROOT / path.lstrip('/')
    else:
        base = (ROOT / page_rel).parent / path
    out = [base]
    # Directory URLs resolve to their index.html
    if path.endswith('/') or not base.suffix:
        out.append(base / 'index.html')
    return out


def check_page(page_rel):
    src, _bom = read(ROOT / page_rel)
    loc = locate(src)
    problems = []
    for tag, attrs, _s, _e, _raw in loc.tags:
        for attr in URL_ATTRS & attrs.keys():
            value = (attrs[attr] or '').strip()
            if not value or value.startswith(EXTERNAL_PREFIXES) or value.startswith('#'):
                continue
            if not any(c.exists() for c in candidates(value, page_rel)):
                problems.append((tag, attr, value))
        # srcset carries comma-separated "url descriptor" pairs
        if 'srcset' in attrs and attrs['srcset']:
            for part in attrs['srcset'].split(','):
                url = part.strip().split()[0] if part.strip() else ''
                if not url or url.startswith(EXTERNAL_PREFIXES):
                    continue
                if not any(c.exists() for c in candidates(url, page_rel)):
                    problems.append((tag, 'srcset', url))
    return problems


def main():
    total = 0
    for entry in MANIFEST['pages']:
        problems = check_page(entry['src'])
        if problems:
            print(f"\n{entry['src']}")
            for tag, attr, value in problems:
                print(f"    <{tag} {attr}=\"{value}\">")
            total += len(problems)
    print(f"\n{len(MANIFEST['pages'])} pages checked, {total} unresolved reference(s)")
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
