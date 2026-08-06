"""
Phase 1 sitewide edits. Idempotent - safe to re-run.

  1. --nav-h:130px -> 180px in inline critical CSS
       The inline block declared 130px while styles.css:105 declares 180px.
       Because the inline block applies before styles.css parses, every page
       laid out at 130px then jumped to 180px: a ~50px CLS hit sitewide.

  2. Strip <meta name="keywords">
       Google has ignored it since 2009. index.html carried 973 chars and
       services.html 1056 - keyword stuffing with no upside.

  3. index.html only: old palette in critical CSS -> #1a1a1a
       The inline block still carried #C41E3A / #1a3d5c from the pre-rebrand
       palette while styles.css uses #1a1a1a, so the homepage flashed red
       before the stylesheet loaded.

  4. index.html only: favicon MIME (svg+xml declared for a .png) and the
       three stray blank lines before <!DOCTYPE>.

    py scripts/phase1_sitewide.py --check   # report only
    py scripts/phase1_sitewide.py --apply
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _htmlloc import locate, splice, read, write

ROOT = Path(__file__).parent.parent
MANIFEST = json.loads((Path(__file__).parent / 'pages.json').read_text('utf-8'))

# Every .html that ships, including the ones outside the manifest.
def all_html():
    skip = ('PREVIEW_', 'COLOR_', 'business-card-')
    seen = []
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if any(part in ('node_modules', 'scripts') for part in rel.parts):
            continue
        if 'assets' in rel.parts or 'company-materials' in rel.parts:
            continue
        if p.name.startswith(skip):
            continue
        seen.append(p)
    return seen


def strip_keywords(src):
    """Remove the whole <meta name="keywords" ...> line via the locator."""
    loc = locate(src)
    edits = []
    for tag, attrs, start, end, _raw in loc.tags:
        if tag == 'meta' and attrs.get('name', '').lower() == 'keywords':
            # Swallow the trailing newline and this line's leading indent.
            line_start = src.rfind('\n', 0, start) + 1
            line_end = end
            if src[line_end:line_end + 1] == '\n':
                line_end += 1
            if src[line_start:start].strip() == '':
                edits.append((line_start, line_end, ''))
            else:
                edits.append((start, end, ''))
    return splice(src, edits), len(edits)


def main():
    apply = '--apply' in sys.argv
    changes = {'nav_h': 0, 'keywords': 0, 'palette': 0, 'favicon': 0, 'doctype': 0}
    touched = []

    for path in all_html():
        src, bom = read(path)
        original = src

        # 1. nav height
        if '--nav-h:130px' in src:
            src = src.replace('--nav-h:130px', '--nav-h:180px')
            changes['nav_h'] += 1

        # 2. meta keywords
        src, n = strip_keywords(src)
        changes['keywords'] += n

        if path.name == 'index.html' and path.parent == ROOT:
            # 3. old palette inside the inline critical CSS only.
            for old, new in (('#C41E3A', '#1a1a1a'),
                             ('#1a3d5c', '#1a1a1a'),
                             ('#0f2538', '#1a1a1a')):
                if old in src:
                    src = src.replace(old, new)
                    changes['palette'] += 1
            # 4a. favicon MIME
            if 'type="image/svg+xml" href="assets/images/black-arrow-logo.png"' in src:
                src = src.replace(
                    'type="image/svg+xml" href="assets/images/black-arrow-logo.png"',
                    'type="image/png" href="assets/images/black-arrow-logo.png"')
                changes['favicon'] += 1
            # 4b. blank lines before doctype
            stripped = re.sub(r'^\s*\n(?=<!DOCTYPE)', '', src, flags=re.IGNORECASE)
            if stripped != src:
                src = stripped
                changes['doctype'] += 1

        if src != original:
            touched.append(path.relative_to(ROOT))
            if apply:
                write(path, src, bom)

    verb = 'Applied' if apply else 'Would apply'
    print(f'{verb}:')
    print(f"  --nav-h 130px -> 180px : {changes['nav_h']} pages")
    print(f"  <meta keywords> removed: {changes['keywords']} tags")
    print(f"  index.html palette     : {changes['palette']} replacements")
    print(f"  index.html favicon MIME: {changes['favicon']}")
    print(f"  index.html doctype gap : {changes['doctype']}")
    print(f'  files touched          : {len(touched)}')
    if not apply:
        print('\n(dry run - pass --apply to write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
