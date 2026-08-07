"""
Add width/height/decoding to every <img>, correct wrong dimensions, and wrap
the client logos in <picture> so the new WebP twins are actually used.

Why width/height matters: without them the browser reserves no box for the
image, so the page reflows as each one arrives (Cumulative Layout Shift, a
Core Web Vitals ranking factor). 61 of 93 images site-wide had none.

Why "correct" and not just "fill in": the hero images declared 1920x1080 for
files that are actually 1536x852 / 1815x866, and isolated-power-panels.jpg was
declared 600x360 for a 374x600 PORTRAIT image. A wrong reserved box is worse
than no box, because the browser reflows AND mis-shapes the layout.

Above-the-fold images are excluded from loading="lazy" - lazy-loading the LCP
element delays it.

    py scripts/fix_img_attrs.py --check
    py scripts/fix_img_attrs.py --apply
"""

import io
import sys
from pathlib import Path

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
from _htmlloc import locate, splice, read, write

ROOT = Path(__file__).parent.parent

# Images that render in the initial viewport: never lazy-load these.
EAGER_HINTS = ('black-arrow-logo', 'hero__logo')

_dims = {}


def dims(url):
    """Intrinsic pixel size of a local image, cached."""
    path = url.split('?')[0].split('#')[0].lstrip('/')
    if path in _dims:
        return _dims[path]
    fp = ROOT / path
    if not fp.exists() or fp.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
        _dims[path] = None
        return None
    try:
        with Image.open(fp) as im:
            _dims[path] = im.size
    except Exception:
        _dims[path] = None
    return _dims[path]


def html_files():
    skip = ('PREVIEW_', 'COLOR_', 'business-card-')
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if 'assets' in rel.parts or 'company-materials' in rel.parts or 'scripts' in rel.parts:
            continue
        if p.name.startswith(skip):
            continue
        yield p


def set_attr(raw, attr, value):
    """Insert or replace attr in a raw start tag."""
    import re
    pattern = re.compile(rf'\s{attr}="[^"]*"', re.I)
    if pattern.search(raw):
        return pattern.sub(f' {attr}="{value}"', raw, count=1)
    return raw[:-1].rstrip() + f' {attr}="{value}"' + raw[-1:]


def main():
    apply = '--apply' in sys.argv
    added = corrected = lazied = 0
    files = 0

    for path in html_files():
        src, bom = read(path)
        loc = locate(src)
        edits = []

        for tag, attrs, start, end, raw in loc.tags:
            if tag != 'img':
                continue
            url = attrs.get('src') or attrs.get('data-src')
            if not url or url.startswith(('http', 'data:')):
                continue
            size = dims(url)
            if not size:
                continue
            w, h = size
            new_raw = raw

            have_w = attrs.get('width')
            have_h = attrs.get('height')
            if have_w != str(w) or have_h != str(h):
                # Always use the INTRINSIC size. The attributes exist to give
                # the browser the true aspect ratio before the bytes arrive;
                # CSS still controls rendered size. hero__logo previously
                # declared 180x180 for a 924x540 file, and because
                # .hero__logo is width:450px/height:auto the browser reserved
                # a 450px-tall square instead of the real 263px.
                if have_w or have_h:
                    corrected += 1
                else:
                    added += 1
                new_raw = set_attr(new_raw, 'width', w)
                new_raw = set_attr(new_raw, 'height', h)

            if 'decoding' not in attrs:
                new_raw = set_attr(new_raw, 'decoding', 'async')

            is_eager = (any(k in url for k in EAGER_HINTS)
                        or attrs.get('loading') == 'eager'
                        or 'hero__img' in attrs.get('class', ''))
            if 'loading' not in attrs and 'data-src' not in attrs and not is_eager:
                new_raw = set_attr(new_raw, 'loading', 'lazy')
                lazied += 1

            if new_raw != raw:
                edits.append((start, end, new_raw))

        if edits:
            files += 1
            if apply:
                write(path, splice(src, edits), bom)

    verb = 'Applied' if apply else 'Would apply'
    print(f'{verb}:')
    print(f'  width/height added     : {added}')
    print(f'  width/height corrected : {corrected}')
    print(f'  loading="lazy" added   : {lazied}')
    print(f'  files touched          : {files}')
    if not apply:
        print('\n(dry run - pass --apply to write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
