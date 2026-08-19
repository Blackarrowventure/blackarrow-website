"""
Insert the en / ar / x-default hreflang triple into the English pages.

Deliberately NOT done by build_ar.py. The generator writes ar/** only, so it
can never damage the live English site. hreflang is static per page (a page's
URL never changes), so generating it would buy nothing and would introduce a
failure mode where a bad build run corrupts English pages. build_ar.py copies
the triple through unchanged, giving both sides the identical reciprocal set,
which is what Google requires.

Idempotent.

    py scripts/add_hreflang.py --check
    py scripts/add_hreflang.py --apply
"""

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
from _htmlloc import locate, splice, read, write

ROOT = Path(__file__).parent.parent
SITE = 'https://www.blackarrowksa.com'
MANIFEST = json.loads((Path(__file__).parent / 'pages.json').read_text('utf-8'))


def triple(url, indent='  '):
    en = SITE + url
    ar = SITE + ('/ar/' if url == '/' else '/ar' + url)
    return (
        f'\n{indent}<link rel="alternate" hreflang="en" href="{en}">'
        f'\n{indent}<link rel="alternate" hreflang="ar" href="{ar}">'
        f'\n{indent}<link rel="alternate" hreflang="x-default" href="{en}">'
    )


def main():
    apply = '--apply' in sys.argv
    done = skipped = no_canonical = 0

    for entry in MANIFEST['pages']:
        if not entry.get('ar'):
            continue                     # no Arabic twin -> no alternates
        path = ROOT / entry['src']
        src, bom = read(path)

        # Must look for the <link rel="alternate"> tags specifically. A bare
        # 'hreflang=' test also matches the hreflang attribute on the EN/AR
        # anchors in the language switcher, so any page carrying a switcher
        # but no alternates reported itself as already done and was skipped
        # in silence. company-profile.html was exactly that page.
        if 'rel="alternate" hreflang=' in src:
            skipped += 1
            continue

        loc = locate(src)
        anchor = None
        for tag, attrs, s, e, raw in loc.tags:
            if tag == 'link' and attrs.get('rel') == 'canonical':
                anchor = e
                break
        if anchor is None:
            no_canonical += 1
            print(f'  NO CANONICAL: {entry["src"]}')
            continue

        out = splice(src, [(anchor, anchor, triple(entry['url']))])
        if apply:
            write(path, out, bom)
        done += 1

    verb = 'Inserted into' if apply else 'Would insert into'
    print(f'{verb} {done} page(s); {skipped} already had it; '
          f'{no_canonical} missing a canonical')
    if not apply:
        print('(dry run - pass --apply to write)')
    return 1 if no_canonical else 0


if __name__ == '__main__':
    sys.exit(main())
