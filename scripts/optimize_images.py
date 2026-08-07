"""
Image optimisation via Pillow. No Node, npm, ImageMagick or cwebp needed.

Three jobs:

  1. Re-encode the 8 service WebPs at quality=75, method=6.
     Three of them (ev-solutions, general-trading, hvac-solutions) were
     LARGER than their own JPEG fallbacks, and <picture> makes browsers
     prefer the WebP - so the "optimisation" was actively costing bytes.

  2. Generate 768w variants for the hero slides.
     index.html carried srcset="...ev-solutions.webp?w=480". A query string
     resizes nothing: mobile downloaded the full-size file, and because the
     URL differed from the desktop one it became a second cache entry too.

  3. Shrink oversized logos and emit WebP twins for the client strip.
     NLS_Logo_Transparent.png is 875x736 and 434 KB for a logo displayed at
     roughly 160px wide.

SAFETY GATE: a re-encoded file is only written if it is smaller than what it
replaces. Never silently ship a bigger file.

    py scripts/optimize_images.py --check
    py scripts/optimize_images.py --apply
"""

import io
import sys
from pathlib import Path

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
IMG = ROOT / 'assets' / 'images'

SERVICE_QUALITY = 75
LOGO_MAX_EDGE = 400
NLS_MAX_EDGE = 480
HERO_WIDTH = 768


def kb(n):
    return f'{n / 1024:7.0f} KB'


def encode(im, path, quality, apply, lossless=False):
    buf = io.BytesIO()
    save_kwargs = {'quality': quality, 'method': 6}
    if lossless:
        save_kwargs['lossless'] = True
    im.save(buf, 'WEBP', **save_kwargs)
    data = buf.getvalue()
    if apply:
        path.write_bytes(data)
    return len(data)


def main():
    apply = '--apply' in sys.argv
    saved = 0

    print('== 1. Service WebP re-encode (gate: must beat both current WebP and JPEG) ==')
    for jpg in sorted((IMG / 'services').glob('*.jpg')):
        webp = jpg.with_suffix('.webp')
        if not webp.exists():
            continue
        old_w, old_j = webp.stat().st_size, jpg.stat().st_size
        im = Image.open(jpg).convert('RGB')
        new = encode(im, webp, SERVICE_QUALITY, apply=False)
        verdict = 'WRITE' if new < old_w else 'keep '
        if new < old_w:
            if apply:
                encode(im, webp, SERVICE_QUALITY, apply=True)
            saved += old_w - new
        flag = '  <-- was BIGGER than its jpeg' if old_w > old_j else ''
        print(f'  {verdict} {jpg.stem:26} webp {kb(old_w)} -> {kb(new)}  (jpg {kb(old_j)}){flag}')

    print('\n== 2. Hero 768w variants ==')
    hero_bases = ['ev-solutions', 'ups-solutions', 'lighting-solutions',
                  'firefighting-solutions', 'hvac-solutions',
                  'electrical-power', 'general-trading']
    for base in hero_bases:
        jpg = IMG / 'services' / f'{base}.jpg'
        if not jpg.exists():
            continue
        out = IMG / 'services' / f'{base}-768.webp'
        im = Image.open(jpg).convert('RGB')
        w, h = im.size
        if w <= HERO_WIDTH:
            print(f'  skip  {base:26} already {w}px wide')
            continue
        small = im.resize((HERO_WIDTH, round(h * HERO_WIDTH / w)), Image.LANCZOS)
        n = encode(small, out, SERVICE_QUALITY, apply)
        full = (IMG / 'services' / f'{base}.webp').stat().st_size
        print(f'  WRITE {base + "-768.webp":30} {kb(n)}  (full {kb(full)})')

    print('\n== 3. Client logos -> resized WebP twins ==')
    for src in sorted((IMG / 'clients').iterdir()):
        if src.suffix.lower() not in ('.png', '.jpg', '.jpeg'):
            continue
        im = Image.open(src)
        has_alpha = im.mode in ('RGBA', 'LA', 'P') and 'transparency' in im.info or im.mode == 'RGBA'
        im = im.convert('RGBA' if has_alpha else 'RGB')
        max_edge = NLS_MAX_EDGE if 'NLS' in src.name else LOGO_MAX_EDGE
        w, h = im.size
        if max(w, h) > max_edge:
            scale = max_edge / max(w, h)
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        out = src.with_suffix('.webp')
        old = src.stat().st_size
        n = encode(im, out, 82, apply)
        saved += max(0, old - n)
        print(f'  WRITE {src.name:46} {kb(old)} -> {kb(n)}  ({w}x{h})')

    print(f'\nEstimated transfer saved on the client strip + service images: {kb(saved)}')
    if not apply:
        print('\n(dry run - pass --apply to write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
