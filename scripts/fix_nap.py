"""
Fix the NAP (Name / Address / Phone) and opening-hours contradiction.

Before this script the site stated three different things:

  address  footer (23 pages) : "Al Khobar, Saudi Arabia"
           contact.html      : "Ad Dammam, Ash Sharqiyah 32245, Saudi Arabia"
           JSON-LD (17 pages): addressLocality "Dammam", postalCode 32245

  hours    footer (23 pages) : "9 AM - 5 PM, Sat-Thu"      <- Saturday OPEN
           contact.html      : "Friday - Saturday: Closed"  <- Saturday CLOSED

Google cross-checks a Business Profile against the site, so contradictory NAP
actively suppresses local ranking. Confirmed with the owner: the address is
Dammam and the hours are Sunday-Thursday 08:00-18:00, Friday and Saturday
closed.

This script:
  1. rewrites the footer address + hours on every page,
  2. renames the now-misleading key location_khobar -> location_dammam,
  3. updates en.json and ar.json,
  4. injects openingHoursSpecification into every LocalBusiness JSON-LD block.

    py scripts/fix_nap.py --check
    py scripts/fix_nap.py --apply
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

ADDRESS_EN = 'Ad Dammam, Ash Sharqiyah, Saudi Arabia'
ADDRESS_AR = 'الدمام، الشرقية، المملكة العربية السعودية'
HOURS_EN = 'Sun - Thu, 8 AM - 6 PM'
HOURS_AR = 'الأحد - الخميس، 8 ص - 6 م'   # Western digits: site-wide convention

OPENING_HOURS = '''"openingHoursSpecification": [
      {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Sunday","Monday","Tuesday","Wednesday","Thursday"],
        "opens": "08:00",
        "closes": "18:00"
      },
      {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Friday","Saturday"],
        "opens": "00:00",
        "closes": "00:00"
      }
    ],
    '''


def html_files():
    skip = ('PREVIEW_', 'COLOR_', 'business-card-')
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if 'assets' in rel.parts or 'company-materials' in rel.parts or 'scripts' in rel.parts:
            continue
        if p.name.startswith(skip):
            continue
        yield p


def main():
    apply = '--apply' in sys.argv
    stats = {'address': 0, 'hours': 0, 'key': 0, 'schema': 0}
    touched = []

    for path in html_files():
        src, bom = read(path)
        original = src

        # 1. Footer address text + rename the key in the same tag.
        if 'location_khobar' in src or 'Al Khobar, Saudi Arabia' in src:
            src = src.replace(
                '<span data-i18n="location_khobar">Al Khobar, Saudi Arabia</span>',
                f'<span data-i18n="location_dammam">{ADDRESS_EN}</span>')
            # Any stragglers that use the key with different text.
            src = src.replace('data-i18n="location_khobar"', 'data-i18n="location_dammam"')
            src = src.replace('Al Khobar, Saudi Arabia', ADDRESS_EN)
            stats['address'] += 1
            stats['key'] += 1

        # 2. Footer hours.
        if '9 AM - 5 PM, Sat-Thu' in src:
            src = src.replace('9 AM - 5 PM, Sat-Thu', HOURS_EN)
            stats['hours'] += 1

        # 3. openingHoursSpecification into standalone LocalBusiness JSON-LD.
        #    Only the top-level entities (4-space indent) get it. The 14
        #    six-space-indented LocalBusiness blocks on service/solution pages
        #    are "provider" sub-objects pointing at the same company, so
        #    repeating hours there would be redundant bloat.
        if 'openingHoursSpecification' not in src:
            new_src, n = re.subn(
                r'\n    "@type": "LocalBusiness",\n',
                '\n    "@type": "LocalBusiness",\n    ' + OPENING_HOURS.rstrip() + '\n',
                src, count=1)
            if n:
                src = new_src
                stats['schema'] += 1

        if src != original:
            touched.append(str(path.relative_to(ROOT)))
            if apply:
                write(path, src, bom)

    # 4. Translation files.
    for lang, addr, hours in (('en', ADDRESS_EN, HOURS_EN), ('ar', ADDRESS_AR, HOURS_AR)):
        jp = ROOT / 'assets' / 'translations' / f'{lang}.json'
        data = json.loads(jp.read_text('utf-8'))
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if 'location_khobar' in data:
            del data['location_khobar']
        data['location_dammam'] = addr
        data['business_hours_range'] = hours
        # Two keys referenced in HTML but missing from both files.
        data.setdefault('footer_quicklinks', 'Quick Links' if lang == 'en' else 'روابط سريعة')
        if lang == 'ar':
            data.setdefault('what_we_offer', 'ما نقدمه')
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if before != after:
            if apply:
                jp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n',
                              encoding='utf-8')
            touched.append(f'assets/translations/{lang}.json')

    verb = 'Applied' if apply else 'Would apply'
    print(f'{verb}:')
    print(f"  footer address -> Dammam        : {stats['address']} pages")
    print(f"  footer hours   -> Sun-Thu 8-6   : {stats['hours']} pages")
    print(f"  key location_khobar -> _dammam  : {stats['key']} pages")
    print(f"  openingHoursSpecification added : {stats['schema']} JSON-LD blocks")
    print(f'  files touched                   : {len(touched)}')
    if not apply:
        print('\n(dry run - pass --apply to write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
