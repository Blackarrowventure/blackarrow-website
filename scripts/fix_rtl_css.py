"""
Convert unambiguous physical CSS properties to logical ones, so RTL works by
construction instead of by a growing list of [dir="rtl"] overrides.

SCOPE IS DELIBERATELY NARROW. Only properties with an exact logical
equivalent and NO positioning semantics are converted:

    padding-left/right  -> padding-inline-start/end
    border-left/right   -> border-inline-start/end
    margin-left/right   -> margin-inline-start/end
    text-align:left/right -> text-align:start/end

In an LTR context padding-inline-start behaves identically to padding-left, so
this is a no-op for the English site -- that asymmetry is exactly why this
subset is safe to sweep wholesale.

NOT converted: the ~28 `left:`/`right:` declarations on absolutely-positioned
elements. Several are genuinely physical (decorative placement that should not
flip) and getting one wrong fails silently. Those need individual review
against real /ar/ pages.

Once converted, the [dir="rtl"] rules that existed ONLY to flip these become
dead weight and are removed.

    py scripts/fix_rtl_css.py --check
    py scripts/fix_rtl_css.py --apply
"""

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
CSS = ROOT / 'assets' / 'css' / 'styles.css'

LOGICAL = [
    (r'\bpadding-left\b',  'padding-inline-start'),
    (r'\bpadding-right\b', 'padding-inline-end'),
    (r'\bborder-left\b',   'border-inline-start'),
    (r'\bborder-right\b',  'border-inline-end'),
    (r'\bmargin-left\b',   'margin-inline-start'),
    (r'\bmargin-right\b',  'margin-inline-end'),
]

# [dir="rtl"] rules that existed solely to mirror the properties above.
# With logical properties these are not merely redundant -- they would now
# DOUBLE-flip and break RTL.
DEAD_RTL_RULES = [
    '[dir="rtl"] .vm-card { border-left: none; border-right: 4px solid var(--clr-accent); }',
    '[dir="rtl"] .contact-info-card { border-left: none; border-right: 3px solid var(--clr-accent); }',
    '[dir="rtl"] .stats__item { border-right: none; border-left: 1px solid rgba(255,255,255,.1); }',
    '[dir="rtl"] .stats__item:last-child { border-left: none; }',
    '[dir="rtl"] .vm-card ul li { padding-left: 0; padding-right: 20px; }',
    '[dir="rtl"] .footer__col ul li a:hover { padding-left: 0; padding-right: 4px; }',
    '[dir="rtl"] .footer__col .cr { border-left: none; border-right: 2px solid var(--clr-accent); }',
]

# This selector matches an element that ITSELF carries dir="rtl". dir is set on
# <html>, so it has never matched anything. The correct rule already exists in
# the RTL section below it.
BROKEN_SELECTOR = '.wa-float[dir="rtl"] { right: auto; left: 28px; }'

ARABIC_FONT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Playfair+Display:wght@600;700;800;900&display=swap');"
)
ARABIC_FONT_NEW = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Playfair+Display:wght@600;700;800;900&display=swap');\n"
    "/* Noto Kufi Arabic was declared in --ff-ar but never actually loaded, so\n"
    "   every Arabic heading fell back to Playfair Display, which has no Arabic\n"
    "   glyphs at all. */\n"
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Noto+Kufi+Arabic:wght@400;500;700&display=swap');"
)

ARABIC_HEADINGS = '''
/* Playfair Display has no Arabic glyphs, so headings must switch face in RTL
   or they fall back to an arbitrary system font. */
[dir="rtl"] h1, [dir="rtl"] h2, [dir="rtl"] h3,
[dir="rtl"] h4, [dir="rtl"] h5, [dir="rtl"] h6,
[dir="rtl"] .hero__eyebrow, [dir="rtl"] .overline {
  font-family: var(--ff-ar);
}
'''


def main():
    apply = '--apply' in sys.argv
    src = CSS.read_text('utf-8')
    original = src
    counts = {}

    # 1. physical -> logical
    for pattern, replacement in LOGICAL:
        src, n = re.subn(pattern, replacement, src)
        if n:
            counts[replacement] = n

    # text-align needs value-level, not property-level, replacement
    src, n1 = re.subn(r'text-align:\s*left\b', 'text-align: start', src)
    src, n2 = re.subn(r'text-align:\s*right\b', 'text-align: end', src)
    if n1 or n2:
        counts['text-align: start/end'] = n1 + n2

    # 2. drop the now-harmful RTL mirror rules
    removed = 0
    for rule in DEAD_RTL_RULES:
        # they were rewritten in step 1 too, so match the converted form
        converted = rule
        for pattern, replacement in LOGICAL:
            converted = re.sub(pattern, replacement, converted)
        for candidate in (rule, converted):
            if candidate in src:
                src = src.replace(candidate + '\n', '').replace(candidate, '')
                removed += 1
                break

    broken = 0
    for pattern, replacement in LOGICAL:
        pass
    if BROKEN_SELECTOR in src:
        src = src.replace(BROKEN_SELECTOR + '\n', '').replace(BROKEN_SELECTOR, '')
        broken = 1

    # 3. load the Arabic font and apply it to headings
    font_added = 0
    if 'Noto+Kufi+Arabic' not in src and ARABIC_FONT in src:
        src = src.replace(ARABIC_FONT, ARABIC_FONT_NEW, 1)
        font_added = 1
    heading_added = 0
    if '[dir="rtl"] h1' not in src:
        src = src.rstrip() + '\n' + ARABIC_HEADINGS
        heading_added = 1

    print('Physical -> logical properties:')
    for k, v in sorted(counts.items()):
        print(f'  {v:3}  {k}')
    print(f'\nRemoved {removed} now-redundant [dir="rtl"] mirror rule(s)')
    print(f'Removed {broken} selector that could never match (.wa-float[dir="rtl"])')
    print(f'Arabic font @import added: {bool(font_added)}')
    print(f'Arabic heading rule added: {bool(heading_added)}')

    if apply and src != original:
        CSS.write_text(src, encoding='utf-8')
        print('\nwritten')
    elif not apply:
        print('\n(dry run - pass --apply to write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
