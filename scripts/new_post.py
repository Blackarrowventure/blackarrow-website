"""
Scaffold a new blog post so writing one costs prose, not clerical work.

Why this exists
---------------
A post file is 247 lines, of which 219 - 89% - are head, nav, footer and
schema that are identical on every post. Publishing one by hand also means
touching pages.json, ar-pages.json, en.json, ar.json and the blog index, then
running three scripts. Miss any of it and build_ar.py fails, or worse, the
page ships without hreflang.

That overhead is why the blog has two posts. This script removes it.

It does NOT write the article. It takes a spec file holding the English and
Arabic prose and produces every mechanical artefact around it.

The boilerplate is not hardcoded here. An existing post is read as the
template, so nav, footer and schema changes made to the site flow into the
next post automatically instead of this file drifting out of date.

Usage
-----
    py scripts/new_post.py --init my-slug        # write a blank spec to fill in
    py scripts/new_post.py --spec drafts/my-slug.json --check
    py scripts/new_post.py --spec drafts/my-slug.json --apply

Then, as for any content change:

    py scripts/build_ar.py --build
    py scripts/build_sitemap.py --apply
    py scripts/check_links.py
"""

import argparse
import collections
import io
import json
import re
import sys
from urllib.parse import quote
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / 'resources' / 'blog'
TEMPLATE_SLUG = 'nfpa-99-compliance-saudi-hospitals'
SITE = 'https://www.blackarrowksa.com'

# Same budget the rest of the site was rewritten to. Google truncates around
# 60 characters for titles and 155-160 for descriptions; over that, the end of
# the sentence - usually the useful half - is never shown.
TITLE_MAX = 60
DESC_MAX = 155

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


class SpecError(Exception):
    pass


def read(path):
    """Read preserving the BOM and line endings the repo already uses."""
    raw = io.open(path, encoding='utf-8-sig', newline='').read()
    bom = io.open(path, 'rb').read(3) == b'\xef\xbb\xbf'
    return raw, bom


def write(path, text, bom=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='') as fh:
        fh.write(text)


def nl_of(text):
    return '\r\n' if '\r\n' in text else '\n'


BLANK_SPEC = collections.OrderedDict([
    ('slug', ''),
    ('date', ''),
    ('image', '/assets/images/services/isolated-power-panels.jpg'),
    ('wa_topic', ''),
    ('related', [collections.OrderedDict([('href', '/resources/faqs/'),
                                          ('i18n', 'faq_page_title'),
                                          ('label', 'FAQs')])]),
    ('en', collections.OrderedDict([
        ('title', ''),
        ('description', ''),
        ('og_description', ''),
        ('excerpt', ''),
        ('breadcrumb', ''),
        ('subhead', ''),
        ('lead', ''),
        ('sections', [collections.OrderedDict([('h2', ''), ('p', ['', ''])])]),
        ('cta', collections.OrderedDict([('lead', ''), ('text', ''),
                                         ('href', ''), ('label', ''),
                                         ('label_i18n', '')])),
    ])),
    ('ar', collections.OrderedDict([
        ('title', ''),
        ('description', ''),
        ('og_description', ''),
        ('excerpt', ''),
        ('breadcrumb', ''),
        ('subhead', ''),
        ('lead', ''),
        ('sections', [collections.OrderedDict([('h2', ''), ('p', ['', ''])])]),
        ('cta', collections.OrderedDict([('lead', ''), ('text', '')])),
    ])),
])


def init(slug):
    spec = json.loads(json.dumps(BLANK_SPEC), object_pairs_hook=collections.OrderedDict)
    spec['slug'] = slug
    spec['date'] = date.today().isoformat()
    out = ROOT / 'drafts' / f'{slug}.json'
    if out.exists():
        raise SpecError(f'{out} already exists')
    write(out, json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
    print(f'Wrote {out.relative_to(ROOT)}')
    print('Fill it in, then run with --check.')
    print()
    print('The Arabic is not optional: build_ar.py fails the build if any')
    print('data-i18n key is missing from ar.json, which is what keeps the')
    print('Arabic site from silently shipping English.')


def validate(spec):
    problems = []
    slug = spec.get('slug', '')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug or ''):
        problems.append('slug must be lowercase words separated by single hyphens')
    if (BLOG / slug).exists():
        problems.append(f'resources/blog/{slug}/ already exists')
    try:
        y, m, d = (int(x) for x in spec.get('date', '').split('-'))
        date(y, m, d)
    except Exception:
        problems.append('date must be YYYY-MM-DD')

    for lang in ('en', 'ar'):
        block = spec.get(lang) or {}
        for field in ('title', 'description', 'excerpt', 'lead', 'subhead'):
            if not (block.get(field) or '').strip():
                problems.append(f'{lang}.{field} is empty')
        secs = block.get('sections') or []
        if not secs:
            problems.append(f'{lang}.sections is empty')
        for i, sec in enumerate(secs):
            if not (sec.get('h2') or '').strip():
                problems.append(f'{lang}.sections[{i}].h2 is empty')
            if not [p for p in (sec.get('p') or []) if p.strip()]:
                problems.append(f'{lang}.sections[{i}].p has no paragraphs')

    en, ar = spec.get('en') or {}, spec.get('ar') or {}
    # The two languages must have the same shape or the generated Arabic page
    # would carry English headings, which is exactly the failure the static
    # Arabic build exists to prevent.
    if len(en.get('sections') or []) != len(ar.get('sections') or []):
        problems.append('en and ar must have the same number of sections')
    else:
        for i, (e, a) in enumerate(zip(en.get('sections') or [], ar.get('sections') or [])):
            if len(e.get('p') or []) != len(a.get('p') or []):
                problems.append(f'en/ar sections[{i}] have different paragraph counts')

    for lang in ('en', 'ar'):
        t = ((spec.get(lang) or {}).get('title') or '').strip()
        d = ((spec.get(lang) or {}).get('description') or '').strip()
        if len(t) > TITLE_MAX:
            problems.append(f'{lang}.title is {len(t)} chars, over the {TITLE_MAX} Google will show')
        if len(d) > DESC_MAX:
            problems.append(f'{lang}.description is {len(d)} chars, over {DESC_MAX}')

    # Anything reused from the shared translation files must already exist in
    # them. build_ar.py fails the entire build on a single missing key, so
    # catching it here turns a confusing build failure into a named problem.
    ar_json = json.loads(io.open(ROOT / 'assets' / 'translations' / 'ar.json',
                                 encoding='utf-8-sig').read())
    for i, item in enumerate(spec.get('related') or []):
        for field in ('href', 'i18n', 'label'):
            if not (item.get(field) or '').strip():
                problems.append(f'related[{i}].{field} is empty')
        key = item.get('i18n') or ''
        if key and key not in ar_json:
            problems.append(f'related[{i}].i18n "{key}" is not in ar.json')

    encta, arcta = (en.get('cta') or {}), (ar.get('cta') or {})
    if encta or arcta:
        for field in ('lead', 'text', 'href', 'label', 'label_i18n'):
            if not (encta.get(field) or '').strip():
                problems.append(f'en.cta.{field} is empty')
        for field in ('lead', 'text'):
            if not (arcta.get(field) or '').strip():
                problems.append(f'ar.cta.{field} is empty')
        key = encta.get('label_i18n') or ''
        if key and key not in ar_json:
            problems.append(f'en.cta.label_i18n "{key}" is not in ar.json')
    return problems


def key_prefix(slug):
    """post_<slug with hyphens as underscores>_ - namespaced so two posts can
    never collide in the shared translation files."""
    return 'post_' + slug.replace('-', '_') + '_'


def build_article(spec, indent='          '):
    """The only part of the file that is actually unique to a post."""
    pre = key_prefix(spec['slug'])
    en = spec['en']
    out = [f'<article class="blog-article">']
    out.append(f'{indent}<p data-i18n="{pre}lead">{en["lead"]}</p>')
    for i, sec in enumerate(en['sections'], 1):
        out.append('')
        out.append(f'{indent}<h2 data-i18n="{pre}h2_{i}">{sec["h2"]}</h2>')
        for j, para in enumerate([p for p in sec['p'] if p.strip()], 1):
            out.append(f'{indent}<p data-i18n="{pre}s{i}_p{j}">{para}</p>')
    cta = en.get('cta')
    if cta:
        out.append('')
        out.append(f'{indent}<div class="blog-cta-box">')
        out.append(f'{indent}  <p><strong data-i18n="{pre}cta_lead">{cta["lead"]}</strong> '
                   f'<span data-i18n="{pre}cta_text">{cta["text"]}</span></p>')
        out.append(f'{indent}  <a href="{cta["href"]}" class="btn btn-primary" '
                   f'data-i18n="{cta["label_i18n"]}">{cta["label"]}</a>')
        out.append(f'{indent}</div>')
    out.append(f'{indent[:-2]}</article>')
    return ('\n' + indent).join([out[0]]) + '\n' + '\n'.join(out[1:])


def collect_keys(spec):
    """Every data-i18n key the generated page will reference, with both
    languages' text, so en.json and ar.json can be filled in one pass."""
    pre = key_prefix(spec['slug'])
    pairs = collections.OrderedDict()
    pairs[pre + 'lead'] = (spec['en']['lead'], spec['ar']['lead'])
    for i, (e, a) in enumerate(zip(spec['en']['sections'], spec['ar']['sections']), 1):
        pairs[f'{pre}h2_{i}'] = (e['h2'], a['h2'])
        ep = [p for p in e['p'] if p.strip()]
        ap = [p for p in a['p'] if p.strip()]
        for j, (ept, apt) in enumerate(zip(ep, ap), 1):
            pairs[f'{pre}s{i}_p{j}'] = (ept, apt)
    pairs[pre + 'h1'] = (spec['en']['title'], spec['ar']['title'])
    pairs[pre + 'subhead'] = (spec['en']['subhead'], spec['ar']['subhead'])
    pairs[pre + 'crumb'] = (
        (spec['en'].get('breadcrumb') or spec['en']['title']).strip(),
        (spec['ar'].get('breadcrumb') or spec['ar']['title']).strip())
    encta, arcta = (spec['en'].get('cta') or {}), (spec['ar'].get('cta') or {})
    if encta:
        pairs[pre + 'cta_lead'] = (encta['lead'], arcta.get('lead', ''))
        pairs[pre + 'cta_text'] = (encta['text'], arcta.get('text', ''))
    pairs[pre + 'card_title'] = (spec['en']['title'], spec['ar']['title'])
    pairs[pre + 'card_excerpt'] = (spec['en']['excerpt'], spec['ar']['excerpt'])
    return pairs


def render_page(spec):
    src, bom = read(BLOG / TEMPLATE_SLUG / 'index.html')
    nl = nl_of(src)
    body = src.replace('\r\n', '\n')
    slug = spec['slug']
    en = spec['en']

    # The template slug appears in canonical, all three hreflang tags, og:url,
    # the JSON-LD @id, the breadcrumb item and both language-switcher hrefs.
    # One replace covers every one of them, which is why this cannot fall out
    # of sync the way a hand-maintained list of substitutions would.
    body = body.replace(TEMPLATE_SLUG, slug)

    tmpl_title = 'NFPA 99 Compliance for Saudi Hospitals: A Practical Guide'
    tmpl_desc = ('A practical guide to NFPA 99 compliance for hospitals in Saudi Arabia '
                 '— what the standard covers, why it matters for electrical systems, and '
                 'what to check before your next inspection.')
    tmpl_ogdesc = ('What NFPA 99 covers, why it matters for hospital electrical systems in '
                   'Saudi Arabia, and what to check before your next inspection.')
    tmpl_crumb = 'NFPA 99 Compliance for Saudi Hospitals'
    tmpl_img = 'https://www.blackarrowksa.com/assets/images/services/isolated-power-panels.jpg'
    tmpl_subhead = ('What the standard covers, why it matters for electrical systems, '
                    'and what to check before your next inspection')
    tmpl_meta = 'Black Arrow Venture company \u00b7 Updated July 31, 2026'
    # Prefilled WhatsApp text, in both the float and the mobile sticky bar.
    tmpl_wa = 'Hello%21%20I%27d%20like%20to%20ask%20about%20NFPA%2099%20compliance.'

    y, m, d = (int(x) for x in spec['date'].split('-'))
    wa_topic = (spec.get('wa_topic') or en.get('breadcrumb') or en['title']).strip()
    ogdesc = (en.get('og_description') or en['description']).strip()
    replacements = [
        (tmpl_title, en['title']),
        (tmpl_desc, en['description']),
        (tmpl_ogdesc, ogdesc),
        (tmpl_crumb, (en.get('breadcrumb') or en['title']).strip()),
        (tmpl_img, SITE + spec['image']),
        (tmpl_subhead, en['subhead']),
        (tmpl_meta, f'Black Arrow Venture company \u00b7 Updated {MONTHS[m-1]} {d}, {y}'),
        (tmpl_wa, quote(f"Hello! I'd like to ask about {wa_topic}.", safe='')),
        ('"datePublished": "2026-07-31"', f'"datePublished": "{spec["date"]}"'),
        ('"dateModified": "2026-07-31"', f'"dateModified": "{spec["date"]}"'),
    ]
    for old, new in replacements:
        if old not in body:
            raise SpecError(f'template no longer contains: {old[:70]!r}')
        body = body.replace(old, new)

    # The hero's data-i18n keys are named for the TEMPLATE post. Left alone,
    # they resolve through ar.json to the NFPA post's Arabic headline, so every
    # new post would look right in English and carry the wrong title in Arabic.
    pre = key_prefix(slug)
    for tmpl_key, new_key in (('nfpa_post_h1', pre + 'h1'),
                              ('nfpa_post_subhead', pre + 'subhead'),
                              ('nfpa_post_title_short', pre + 'crumb')):
        old = f'data-i18n="{tmpl_key}"'
        if old not in body:
            raise SpecError(f'template: expected {old} in the hero')
        body = body.replace(old, f'data-i18n="{new_key}"')

    # Related links are per-post, and the template's point at the IPP article.
    rel = spec.get('related') or []
    if rel:
        marker = '<div style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center;">'
        block = re.search(re.escape(marker) + r'.*?</div>', body, re.S)
        if not block:
            raise SpecError('template: related-links container not found')
        links = [f'          <a href="{r["href"]}" class="btn btn-outline" '
                 f'data-i18n="{r["i18n"]}">{r["label"]}</a>' for r in rel]
        body = (body[:block.start()] + marker + '\n' + '\n'.join(links)
                + '\n        </div>' + body[block.end():])

    art = re.search(r'<article class="blog-article">.*?</article>', body, re.S)
    if not art:
        raise SpecError('template article block not found')
    body = body[:art.start()] + build_article(spec) + body[art.end():]

    # The visible post date sits outside the article block.
    y, m, d = (int(x) for x in spec['date'].split('-'))
    body = re.sub(r'(<span class="date"[^>]*>)[^<]*(</span>)',
                  lambda mm: mm.group(1) + f'{MONTHS[m-1]} {d}, {y}' + mm.group(2),
                  body, count=1)

    return body.replace('\n', nl), bom


def card_html(spec, nl):
    pre = key_prefix(spec['slug'])
    y, m, d = (int(x) for x in spec['date'].split('-'))
    return nl.join([
        '          <div class="blog-card">',
        f'            <span class="date">{MONTHS[m-1]} {d}, {y}</span>',
        f'            <h2 data-i18n="{pre}card_title">{spec["en"]["title"]}</h2>',
        f'            <p data-i18n="{pre}card_excerpt">{spec["en"]["excerpt"]}</p>',
        f'            <a href="/resources/blog/{spec["slug"]}/" data-i18n="read_article">Read Article →</a>',
        '          </div>',
    ])


def apply(spec, dry):
    slug = spec['slug']
    url = f'/resources/blog/{slug}/'
    src_rel = f'resources/blog/{slug}/index.html'
    actions = []

    page, bom = render_page(spec)
    actions.append((BLOG / slug / 'index.html', page, bom, 'create post'))

    # blog index: newest first
    idx_path = BLOG / 'index.html'
    idx, idx_bom = read(idx_path)
    nl = nl_of(idx)
    anchor = '        <div class="blog-grid">'
    a = anchor.replace('\n', nl)
    if a not in idx:
        raise SpecError('blog index: .blog-grid container not found')
    idx_new = idx.replace(a, a + nl + card_html(spec, nl), 1)
    actions.append((idx_path, idx_new, idx_bom, 'add card to blog index'))

    # pages.json - insert next to the other posts so the manifest stays readable
    pj_path = ROOT / 'scripts' / 'pages.json'
    pj_raw, pj_bom = read(pj_path)
    pj = json.loads(pj_raw, object_pairs_hook=collections.OrderedDict)
    if any(e['src'] == src_rel for e in pj['pages']):
        raise SpecError(f'pages.json already lists {src_rel}')
    entry = collections.OrderedDict([('src', src_rel), ('url', url), ('ar', True)])
    last_blog = max((i for i, e in enumerate(pj['pages']) if e['src'].startswith('resources/blog/')),
                    default=len(pj['pages']) - 1)
    pj['pages'].insert(last_blog + 1, entry)
    actions.append((pj_path, json.dumps(pj, ensure_ascii=False, indent=2).replace('\n', nl_of(pj_raw)) + nl_of(pj_raw), pj_bom, 'register in pages.json'))

    # ar-pages.json - required, build_ar.py raises without it
    ap_path = ROOT / 'assets' / 'translations' / 'ar-pages.json'
    ap_raw, ap_bom = read(ap_path)
    ap = json.loads(ap_raw, object_pairs_hook=collections.OrderedDict)
    ap[src_rel] = collections.OrderedDict([
        ('title', spec['ar']['title']),
        ('description', spec['ar']['description']),
        ('og_title', spec['ar']['title']),
        ('og_description', (spec['ar'].get('og_description') or spec['ar']['description'])),
    ])
    actions.append((ap_path, json.dumps(ap, ensure_ascii=False, indent=2).replace('\n', nl_of(ap_raw)) + nl_of(ap_raw), ap_bom, 'add Arabic head strings'))

    # en.json / ar.json
    pairs = collect_keys(spec)
    for lang, idxpos in (('en', 0), ('ar', 1)):
        tp = ROOT / 'assets' / 'translations' / f'{lang}.json'
        traw, tbom = read(tp)
        t = json.loads(traw, object_pairs_hook=collections.OrderedDict)
        clash = [k for k in pairs if k in t]
        if clash:
            raise SpecError(f'{lang}.json already has: {", ".join(clash[:4])}')
        for k, v in pairs.items():
            t[k] = v[idxpos]
        actions.append((tp, json.dumps(t, ensure_ascii=False, indent=2).replace('\n', nl_of(traw)) + nl_of(traw), tbom, f'add {len(pairs)} keys to {lang}.json'))

    for path, text, bom_flag, what in actions:
        print(f'  {"would " if dry else ""}{what:<32} {path.relative_to(ROOT)}')
        if not dry:
            write(path, text, bom_flag)
    return len(pairs)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--init', metavar='SLUG', help='write a blank spec to drafts/')
    ap.add_argument('--spec', help='path to a filled-in spec file')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--check', action='store_true', help='validate only (default)')
    g.add_argument('--apply', action='store_true', help='write the files')
    args = ap.parse_args()

    if args.init:
        init(args.init)
        return 0
    if not args.spec:
        ap.error('pass --init SLUG or --spec PATH')

    spec = json.loads(io.open(args.spec, encoding='utf-8-sig').read(),
                      object_pairs_hook=collections.OrderedDict)
    problems = validate(spec)
    if problems:
        print(f'{len(problems)} problem(s) with {args.spec}:')
        for p in problems:
            print('   -', p)
        return 1

    n = apply(spec, dry=not args.apply)
    print()
    if args.apply:
        print('Now run, in this order:')
        print('   py scripts/build_ar.py --build')
        print('   py scripts/build_sitemap.py --apply')
        print('   py scripts/check_links.py')
    else:
        print(f'Valid. {n} translation keys would be added. Pass --apply to write.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SpecError as exc:
        print('error:', exc)
        sys.exit(1)
