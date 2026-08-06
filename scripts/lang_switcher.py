"""
Replace the JavaScript language switcher with plain links to the counterpart URL.

This is required, not cosmetic. With static /ar/ pages the old switcher is
actively broken: an /ar/ page loads, initLang() reads localStorage.lang ===
'en' and calls setLang('en'), which sets <html lang="en" dir="ltr"> on a page
whose text is Arabic. applyTranslations only ever APPLIES a dictionary, so it
cannot restore English -- the result is Arabic text in a left-to-right layout.

Replacing the buttons with links also:
  - drops a 126 KB ar.json fetch from every page load,
  - removes the flash where English renders then swaps to Arabic,
  - removes the inline onclick handlers, which are the main blocker to ever
    shipping a real Content-Security-Policy.

Marked with data-lang-switch so build_ar.py leaves the hrefs alone (they are
already the correct absolute URLs for both sides) and only moves the active
state.

    py scripts/lang_switcher.py --check
    py scripts/lang_switcher.py --apply
"""

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
from _htmlloc import read, write

ROOT = Path(__file__).parent.parent
MANIFEST = json.loads((Path(__file__).parent / 'pages.json').read_text('utf-8'))

SWITCHER_RE = re.compile(
    r'<div class="lang-switcher">.*?</div>', re.S)


def new_switcher(en_url, ar_url, has_ar):
    if not has_ar:
        # No Arabic twin: point AR at the Arabic homepage rather than a 404.
        ar_url = '/ar/'
    return (
        '<div class="lang-switcher" data-lang-switch>\n'
        f'            <a href="{en_url}" id="lang-en" class="lang-btn active" '
        'hreflang="en" lang="en" aria-current="true">EN</a>\n'
        f'            <a href="{ar_url}" id="lang-ar" class="lang-btn" '
        'hreflang="ar" lang="ar">AR</a>\n'
        '          </div>'
    )


def main():
    apply = '--apply' in sys.argv
    done = missing = 0

    for entry in MANIFEST['pages']:
        path = ROOT / entry['src']
        if not path.exists():
            continue
        src, bom = read(path)
        if 'data-lang-switch' in src:
            continue
        if 'lang-switcher' not in src:
            missing += 1
            continue

        en_url = entry['url']
        ar_url = '/ar/' if en_url == '/' else '/ar' + en_url
        out = SWITCHER_RE.sub(
            lambda m: new_switcher(en_url, ar_url, entry.get('ar', False)),
            src, count=1)
        if out != src:
            done += 1
            if apply:
                write(path, out, bom)

    verb = 'Rewrote' if apply else 'Would rewrite'
    print(f'{verb} the switcher on {done} page(s); {missing} page(s) have none')
    if not apply:
        print('(dry run - pass --apply to write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
