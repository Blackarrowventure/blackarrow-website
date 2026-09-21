# -*- coding: utf-8 -*-
"""Generate the Technical Consultancy pages (hub + 6 sector pages + policy).

Re-runnable. It (1) writes the English pages, (2) merges the new strings into
assets/translations/en.json and ar.json, (3) registers the pages in
scripts/pages.json and assets/translations/ar-pages.json. Then run:

    python scripts/build_consultancy.py
    python scripts/build_ar.py --build
    python scripts/build_sitemap.py --apply && python scripts/update_sitemap_3d.py

Header, nav and footer are copied from the HVAC service page (and the terms
page for the policy) so the new pages cannot drift from the rest of the site.
"""
import html as H
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from consultancy_content import S, SECTOR, SECTORS, POLICY, POLICY_META

ROOT = Path(__file__).parent.parent
SITE = 'https://www.blackarrowksa.com'
TPL = (ROOT / 'services/hvac-solutions/index.html').read_text('utf-8')
TERMS = (ROOT / 'terms-of-service.html').read_text('utf-8')

EN_KEYS, AR_KEYS = {}, {}


def T(key, pair=None):
    """Register a (en, ar) string and return the English text for HTML."""
    if pair is None:
        pair = S[key]
    EN_KEYS[key] = pair[0]
    AR_KEYS[key] = pair[1]
    return pair[0]


def e(text):
    return H.escape(text, quote=False)


def tx(key, pair=None, tag=None, attrs=''):
    """Element text with data-i18n."""
    return 'data-i18n="%s"' % key, e(T(key, pair))


def el(tag, key, pair=None, cls='', extra=''):
    a, t = tx(key, pair)
    return '<%s%s %s%s>%s</%s>' % (tag, (' class="%s"' % cls) if cls else '', a, (' ' + extra) if extra else '', t, tag)


# ---- shared chrome, cut from the HVAC page ----------------------------------
def chrome():
    body_start = TPL.index('<body>')
    main_start = TPL.index('<main id="main">')
    main_end = TPL.index('</main>')
    nav = TPL[body_start:main_start]
    foot = TPL[main_end + len('</main>'):]
    styles = re.findall(r'<style>.*?</style>', TPL, re.S)
    return nav, foot, styles


NAV, FOOT, STYLES = chrome()


def patch_chrome(nav, foot, url, wa_text):
    ar_url = '/ar' + url
    nav = nav.replace('href="/services/hvac-solutions/" id="lang-en"', 'href="%s" id="lang-en"' % url)
    nav = nav.replace('href="/ar/services/hvac-solutions/" id="lang-ar"', 'href="%s" id="lang-ar"' % ar_url)
    nav = nav.replace('/contact.html?service=hvac', '/contact.html?service=consultancy')
    wa = 'https://wa.me/966560224715?text=' + wa_text
    foot = re.sub(r'https://wa\.me/966560224715\?text=[^"]*', wa, foot)
    foot = foot.replace(
        '<li><a href="/services/isolated-power-panels/" data-i18n="service_ipp">',
        '<li><a href="/services/consultancy/" data-i18n="service_consultancy">' + e(T('service_consultancy')) + '</a></li>\n            <li><a href="/services/isolated-power-panels/" data-i18n="service_ipp">', 1)
    return nav, foot


def wa_msg(text):
    from urllib.parse import quote
    return quote('Hello! I would like to ask about ' + text + '.', safe='')


CSS_EXTRA = """  <style>
    .cons-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;}
    a.cons-card{display:block;text-decoration:none;background:rgba(255,255,255,.03);border:1px solid rgba(245,158,11,.2);border-radius:12px;padding:24px;transition:border-color .2s,transform .2s;}
    a.cons-card:hover,a.cons-card:focus-visible{border-color:var(--clr-accent);transform:translateY(-2px);}
    a.cons-card h3{color:var(--clr-accent);font-size:1.05rem;margin-bottom:8px;}
    a.cons-card p{color:rgba(255,255,255,.75);font-size:.9rem;line-height:1.7;margin-bottom:10px;}
    a.cons-card .more{color:#fff;font-weight:700;font-size:.85rem;}
    .cons-note{max-width:820px;margin:24px auto 0;color:rgba(255,255,255,.7);font-size:.9rem;text-align:center;}
    .cons-prose{max-width:820px;margin:0 auto;}
    .cons-prose p{color:rgba(255,255,255,.85);font-size:1rem;line-height:1.9;margin-bottom:20px;}
  </style>
"""


def head(url, title, desc, extra_ld):
    canon = SITE + url
    ar = SITE + '/ar' + url
    return ('<!DOCTYPE html>\n<html lang="en" dir="ltr">\n<head>\n'
            '  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '  <meta name="description" content="%s">\n  <meta name="robots" content="index, follow">\n'
            '  <link rel="canonical" href="%s">\n'
            '  <link rel="alternate" hreflang="en" href="%s">\n  <link rel="alternate" hreflang="ar" href="%s">\n'
            '  <link rel="alternate" hreflang="x-default" href="%s">\n'
            '  <link rel="icon" type="image/png" href="/assets/images/black-arrow-logo.png">\n'
            '  <title>%s</title>\n  <link rel="apple-touch-icon" href="/assets/images/black-arrow-logo.png">\n\n'
            '  <meta property="og:title" content="%s">\n  <meta property="og:description" content="%s">\n'
            '  <meta property="og:type" content="website">\n  <meta property="og:url" content="%s">\n'
            '  <meta property="og:image" content="%s/assets/images/black-arrow-og.png">\n'
            '  <meta name="twitter:card" content="summary_large_image">\n\n%s\n\n  %s\n'
            '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800;900&family=Noto+Kufi+Arabic:wght@400;500;700&display=swap">\n'
            '  <link rel="stylesheet" href="/assets/css/styles.css">\n\n  %s\n%s\n</head>\n'
            % (H.escape(desc), canon, canon, ar, canon, H.escape(title), H.escape(title), H.escape(desc), canon, SITE,
               extra_ld[0], STYLES[0], STYLES[1], CSS_EXTRA))


PROVIDER = {
    "@type": "LocalBusiness", "name": "Black Arrow Venture company", "telephone": "+966560224715",
    "email": "info@blackarrowksa.com",
    "address": {"@type": "PostalAddress", "streetAddress": "Ad Dammam", "addressLocality": "Dammam",
                "addressRegion": "Ash Sharqiyah", "addressCountry": "SA"},
    "logo": SITE + "/assets/images/black-arrow-logo-schema.png",
}


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>'


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
                                for i, (n, u) in enumerate(items)]}


def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}


def faq_html(items):
    out = []
    for qk, ak in items:
        out.append('<details class="faq-item">\n            <summary data-i18n="%s">%s</summary>\n            <p data-i18n="%s">%s</p>\n          </details>'
                   % (qk, e(EN_KEYS[qk]), ak, e(EN_KEYS[ak])))
    return '\n          '.join(out)


def section(cls, heading_id, overline_key, h2_key, inner):
    return ('    <section class="section%s" aria-labelledby="%s">\n      <div class="container">\n'
            '        <div class="section-header">\n          %s\n          <h2 id="%s" data-i18n="%s">%s</h2>\n        </div>\n'
            '        %s\n      </div>\n    </section>\n\n'
            % ((' ' + cls) if cls else '', heading_id, el('span', overline_key, cls='overline'), heading_id, h2_key, e(EN_KEYS[h2_key]), inner))


def cta_block(prefix_url_note=''):
    h = el('h2', 'cons_cta_h', extra='style="color: #F59E0B !important;"')
    p = el('p', 'cons_cta_sub')
    return ('    <section class="wa-banner" style="background:var(--clr-navy-dark);">\n      <div class="container">\n        <div class="wa-banner__inner">\n'
            '          <div class="wa-banner__text">\n            %s\n            %s\n          </div>\n'
            '          <div style="display:flex;gap:16px;flex-wrap:wrap;">\n'
            '            <a href="/contact.html?service=consultancy" class="btn btn-primary" data-i18n="cons_cta_request">%s</a>\n'
            '            <a href="tel:+966560224715" class="btn btn-outline">+966 560 224 715</a>\n'
            '          </div>\n        </div>\n      </div>\n    </section>\n\n' % (h, p, e(EN_KEYS['cons_cta_request'])))


def related_block(links):
    a = ''.join('<a href="%s" class="btn btn-outline" data-i18n="%s">%s</a>\n          ' % (u, k, e(EN_KEYS[k])) for u, k in links)
    return ('    <section class="section section--gray">\n      <div class="container" style="text-align:center;">\n'
            '        <p style="color:rgba(255,255,255,.7);margin-bottom:16px;" data-i18n="cons_related">%s</p>\n'
            '        <div style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center;">\n          %s</div>\n      </div>\n    </section>\n\n'
            % (e(EN_KEYS['cons_related']), a))


def hero(h1_key, sub_key, crumb_key, crumb_link=None, ctas=True):
    bc = ('<a href="/" data-i18n="nav_home">Home</a>\n              <span>›</span>\n'
          '              <a href="/services.html" data-i18n="nav_services">Services</a>\n              <span>›</span>\n')
    if crumb_link:
        bc += '              <a href="/services/consultancy/" data-i18n="cons_bc_hub">%s</a>\n              <span>›</span>\n' % e(EN_KEYS['cons_bc_hub'])
    bc += '              <span data-i18n="%s">%s</span>' % (crumb_key, e(EN_KEYS[crumb_key]))
    btn = ''
    if ctas:
        btn = ('<div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:24px;">\n'
               '              <a href="/contact.html?service=consultancy" class="btn btn-primary" data-i18n="cons_cta_request">%s</a>\n'
               '              <a href="/consultancy-policy.html" class="btn btn-outline" data-i18n="cons_cta_policy">%s</a>\n            </div>'
               % (e(EN_KEYS['cons_cta_request']), e(EN_KEYS['cons_cta_policy'])))
    return ('    <section class="page-hero">\n      <div class="container">\n        <div class="page-hero__text" style="max-width:860px;">\n'
            '            <nav class="breadcrumb" aria-label="Breadcrumb" data-i18n-aria-label="breadcrumb_aria">\n              %s\n            </nav>\n'
            '            <h1 data-i18n="%s">%s</h1>\n            <p data-i18n="%s">%s</p>\n            %s\n          </div>\n      </div>\n    </section>\n\n'
            % (bc, h1_key, e(EN_KEYS[h1_key]), sub_key, e(EN_KEYS[sub_key]), btn))


def cards(pairs):
    return '<div class="svc-maint-grid">' + ''.join(
        '<div class="svc-maint-card"><h3 data-i18n="%s">%s</h3><p data-i18n="%s">%s</p></div>' % (tk, e(EN_KEYS[tk]), dk, e(EN_KEYS[dk]))
        for tk, dk in pairs) + '</div>'


def numbered(pairs):
    out = ['<div class="svc-breakdown">']
    for i, (tk, dk) in enumerate(pairs, 1):
        out.append('<div class="svc-breakdown__item"><span class="num">%02d</span><h3 data-i18n="%s">%s</h3><p data-i18n="%s">%s</p></div>'
                   % (i, tk, e(EN_KEYS[tk]), dk, e(EN_KEYS[dk])))
    out.append('</div>')
    return ''.join(out)


def register_shared():
    for k, v in S.items():
        T(k, v)


def build_hub():
    url = '/services/consultancy/'
    for k in S:
        T(k)
    t = 'Technical Consultancy Saudi Arabia | UPS, HVAC, Fire Safety'
    d = 'Paid technical consultancy for UPS, firefighting, HVAC, isolated power, facility management and airports in Saudi Arabia. Project plan with reference costing.'
    meta_ar = ('الاستشارات الفنية في السعودية | UPS والتكييف والحريق',
               'استشارات فنية مدفوعة لأنظمة UPS ومكافحة الحريق والتكييف والطاقة المعزولة وإدارة المرافق والمطارات في السعودية. خطة مشروع مع تكلفة مرجعية.')
    faqs = [('cons_q%d' % i, 'cons_a%d' % i) for i in range(1, 6)]
    ld_blocks = [
        ld({"@context": "https://schema.org", "@type": "Service", "serviceType": "Technical consultancy",
            "name": "Technical Consultancy", "description": d, "provider": PROVIDER,
            "areaServed": "Saudi Arabia",
            "audience": {"@type": "Audience", "audienceType": "Facility owners, operators and developers"}}),
        ld(crumbs([("Home", "/"), ("Services", "/services.html"), ("Technical Consultancy", url)])),
        ld(faq_ld([(EN_KEYS[q], EN_KEYS[a]) for q, a in faqs])),
    ]
    sector_cards = ''.join(
        '<a class="cons-card" href="%s%s/"><h3 data-i18n="cons_%s_name">%s</h3><p data-i18n="cons_%s_sub">%s</p><span class="more" data-i18n="cons_learn_more">%s</span></a>'
        % (url, s, s.replace('-', '_'), e(SECTOR[s]['name'][0]), s.replace('-', '_'), e(SECTOR[s]['sub'][0]), e(EN_KEYS['cons_learn_more']))
        for s in SECTORS)
    for s in SECTORS:
        sk = s.replace('-', '_')
        T('cons_%s_name' % sk, SECTOR[s]['name'])
        T('cons_%s_sub' % sk, SECTOR[s]['sub'])
    main = hero('cons_hub_h1', 'cons_hub_sub', 'cons_bc_hub')
    main += section('section--dark', 'cons-why-h', 'cons_overline', 'cons_why_h',
                    '<div class="cons-prose"><p data-i18n="cons_why_p1">%s</p><p data-i18n="cons_why_p2">%s</p></div>'
                    % (e(EN_KEYS['cons_why_p1']), e(EN_KEYS['cons_why_p2'])))
    main += section('', 'cons-sectors-h', 'cons_sectors_o', 'cons_sectors_h', '<div class="cons-cards">%s</div>' % sector_cards)
    main += section('section--dark', 'cons-recv-h', 'cons_recv_o', 'cons_recv_h',
                    numbered([('cons_recv_%dt' % i, 'cons_recv_%dd' % i) for i in range(1, 6)]))
    main += section('', 'cons-proc-h', 'cons_proc_o', 'cons_proc_h',
                    numbered([('cons_proc_%dt' % i, 'cons_proc_%dd' % i) for i in range(1, 5)]))
    main += section('section--dark', 'cons-price-h', 'cons_price_o', 'cons_price_h',
                    '<div class="cons-prose"><p data-i18n="cons_price_p1">%s</p><p data-i18n="cons_price_p2">%s</p></div>'
                    % (e(EN_KEYS['cons_price_p1']), e(EN_KEYS['cons_price_p2'])))
    main += section('', 'cons-indep-h', 'cons_indep_o', 'cons_indep_h',
                    '<div class="cons-prose"><p data-i18n="cons_indep_p">%s</p></div>' % e(EN_KEYS['cons_indep_p']))
    main += section('section--dark', 'cons-faq-h', 'cons_faq_o', 'cons_faq_h', '<div class="svc-faq-list">' + faq_html(faqs) + '</div>')
    main += cta_block()
    main += related_block([('/consultancy-policy.html', 'cons_cta_policy'), ('/services.html', 'view_all_services')])
    nav, foot = patch_chrome(NAV, FOOT, url, wa_msg('technical consultancy'))
    out = head(url, t, d, ld_blocks) + nav + '<main id="main">\n\n' + main + '  </main>' + foot
    (ROOT / 'services/consultancy').mkdir(parents=True, exist_ok=True)
    (ROOT / 'services/consultancy/index.html').write_text(out, 'utf-8')
    return 'services/consultancy/index.html', url, dict(title=meta_ar[0], description=meta_ar[1], og_title=meta_ar[0], og_description=meta_ar[1])


def build_sector(s):
    data = SECTOR[s]
    sk = s.replace('-', '_')
    url = '/services/consultancy/%s/' % s
    pre = 'cons_%s_' % sk
    T(pre + 'name', data['name'])
    T(pre + 'h1', data['h1'])
    T(pre + 'sub', data['sub'])
    T(pre + 'intro', data['intro'])
    for i, (tt, dd) in enumerate(data['covers'], 1):
        T('%sc%dt' % (pre, i), tt)
        T('%sc%dd' % (pre, i), dd)
    T(pre + 'q1', data['q'][0])
    T(pre + 'a1', data['q'][1])
    T(pre + 'service', data['service'][1])
    for k in ('cons_bc_hub', 'cons_overline', 'cons_covers_o', 'cons_covers_note', 'cons_recv_o', 'cons_recv_h', 'cons_price_o', 'cons_price_h',
              'cons_price_p1', 'cons_price_p2', 'cons_faq_o', 'cons_faq_h', 'cons_cta_h', 'cons_cta_sub', 'cons_cta_request', 'cons_cta_policy',
              'cons_related', 'cons_all_sectors', 'cons_q1', 'cons_a1', 'cons_q3', 'cons_a3', 'cons_q4', 'cons_a4', 'cons_q5', 'cons_a5', 'cons_q2', 'cons_a2', 'cons_covers_h'):
        if k in S:
            T(k)
    T('cons_covers_h', ('What the consultancy covers', 'ما تغطيه الاستشارة'))
    for i in range(1, 6):
        T('cons_recv_%dt' % i)
        T('cons_recv_%dd' % i)
    faqs = [(pre + 'q1', pre + 'a1'), ('cons_q1', 'cons_a1'), ('cons_q4', 'cons_a4'), ('cons_q5', 'cons_a5')]
    ld_blocks = [
        ld({"@context": "https://schema.org", "@type": "Service", "serviceType": data['name'][0] + ' consultancy',
            "name": data['h1'][0], "description": data['meta_desc'][0], "provider": PROVIDER, "areaServed": "Saudi Arabia"}),
        ld(crumbs([("Home", "/"), ("Services", "/services.html"), ("Technical Consultancy", "/services/consultancy/"), (data['name'][0], url)])),
        ld(faq_ld([(EN_KEYS[q], EN_KEYS[a]) for q, a in faqs])),
    ]
    main = hero(pre + 'h1', pre + 'sub', pre + 'name', crumb_link=True)
    main += section('section--dark', pre + 'intro-h', 'cons_overline', pre + 'name',
                    '<div class="cons-prose"><p data-i18n="%sintro">%s</p></div>' % (pre, e(EN_KEYS[pre + 'intro'])))
    main += section('', pre + 'covers-h', 'cons_covers_o', 'cons_covers_h',
                    cards([('%sc%dt' % (pre, i), '%sc%dd' % (pre, i)) for i in range(1, 6)])
                    + '<p class="cons-note" data-i18n="cons_covers_note">%s</p>' % e(EN_KEYS['cons_covers_note']))
    main += section('section--dark', pre + 'recv-h', 'cons_recv_o', 'cons_recv_h',
                    numbered([('cons_recv_%dt' % i, 'cons_recv_%dd' % i) for i in range(1, 6)]))
    main += section('', pre + 'price-h', 'cons_price_o', 'cons_price_h',
                    '<div class="cons-prose"><p data-i18n="cons_price_p1">%s</p><p data-i18n="cons_price_p2">%s</p></div>'
                    % (e(EN_KEYS['cons_price_p1']), e(EN_KEYS['cons_price_p2'])))
    main += section('section--dark', pre + 'faq-h', 'cons_faq_o', 'cons_faq_h', '<div class="svc-faq-list">' + faq_html(faqs) + '</div>')
    main += cta_block()
    T(pre + 'service', data['service'][1])
    main += related_block([(data['service'][0], pre + 'service'), ('/services/consultancy/', 'cons_all_sectors'), ('/consultancy-policy.html', 'cons_cta_policy')])
    nav, foot = patch_chrome(NAV, FOOT, url, wa_msg(data['wa'][0]))
    out = head(url, data['meta_title'][0], data['meta_desc'][0], ld_blocks) + nav + '<main id="main">\n\n' + main + '  </main>' + foot
    d = ROOT / ('services/consultancy/%s' % s)
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(out, 'utf-8')
    return ('services/consultancy/%s/index.html' % s, url,
            dict(title=data['meta_title'][1], description=data['meta_desc'][1], og_title=data['meta_title'][1], og_description=data['meta_desc'][1]))


def build_policy():
    url = '/consultancy-policy.html'
    t, d = POLICY_META[0][0], POLICY_META[1][0]
    body = []
    for key, pair, mode in POLICY:
        if key in ('cp_h1', 'cp_sub', 'cp_updated'):
            T(key, pair)
            continue
        T(key, pair)
        if key.startswith('cp_h_'):
            body.append('<h2 data-i18n="%s">%s</h2>' % (key, e(pair[0])))
        elif mode == 'html':
            body.append('<p data-i18n-html="%s">%s</p>' % (key, pair[0]))
        else:
            body.append('<p data-i18n="%s">%s</p>' % (key, e(pair[0])))
    body.append('<h2 data-i18n="legal_language_h">Language</h2>\n        <p data-i18n="legal_language">This document is published in English and Arabic. If there is any conflict or inconsistency between the two versions, the English version shall prevail.</p>')
    body.append('<h2 data-i18n="tos_h_contact">Contact</h2>\n        <p data-i18n-html="pp_contact">Black Arrow Venture company<br>\n        Ad Dammam, Ash Sharqiyah, Saudi Arabia<br>\n        Email: <a href="mailto:info@blackarrowksa.com">info@blackarrowksa.com</a><br>\n        Phone: <a href="tel:+966560224715">+966 560 224 715</a></p>')
    main = ('<main id="main">\n    <section class="page-hero">\n      <div class="container">\n        <nav class="breadcrumb" aria-label="Breadcrumb">\n'
            '          <a href="/" data-i18n="nav_home">Home</a>\n          <span aria-hidden="true">&rsaquo;</span>\n'
            '          <a href="/services/consultancy/" data-i18n="cons_bc_hub">%s</a>\n          <span aria-hidden="true">&rsaquo;</span>\n'
            '          <span data-i18n="cp_h1">%s</span>\n        </nav>\n        <h1 data-i18n="cp_h1">%s</h1>\n        <p data-i18n="cp_sub">%s</p>\n      </div>\n    </section>\n\n'
            '    <section class="section">\n      <div class="container legal" style="max-width:820px;">\n        <p data-i18n-html="cp_updated">%s</p>\n\n        %s\n      </div>\n    </section>\n  </main>'
            % (e(EN_KEYS['cons_bc_hub']), e(EN_KEYS['cp_h1']), e(EN_KEYS['cp_h1']), e(EN_KEYS['cp_sub']), EN_KEYS['cp_updated'], '\n\n        '.join(body)))
    page = TERMS
    page = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % H.escape(t), page, 1)
    page = re.sub(r'(name="description" content=")[^"]*"', lambda m: m.group(1) + H.escape(d) + '"', page, 1)
    page = re.sub(r'(property="og:title" content=")[^"]*"', lambda m: m.group(1) + H.escape(t) + '"', page, 1)
    page = re.sub(r'(property="og:description" content=")[^"]*"', lambda m: m.group(1) + H.escape(d) + '"', page, 1)
    page = page.replace('terms-of-service.html', 'consultancy-policy.html')
    page = page.replace('href="/ar/" id="lang-ar"', 'href="/ar/consultancy-policy.html" id="lang-ar"')
    page = re.sub(r'<main id="main">.*?</main>', lambda m: main, page, 1, flags=re.S)
    (ROOT / 'consultancy-policy.html').write_text(page, 'utf-8')
    return 'consultancy-policy.html', url, dict(title=POLICY_META[0][1], description=POLICY_META[1][1],
                                               og_title=POLICY_META[0][1], og_description=POLICY_META[1][1])


def merge_json(path, new):
    p = ROOT / path
    d = json.loads(p.read_text('utf-8'))
    d.update(new)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', 'utf-8')


def main():
    en0 = json.loads((ROOT / 'assets/translations/en.json').read_text('utf-8'))
    ar0 = json.loads((ROOT / 'assets/translations/ar.json').read_text('utf-8'))
    for k in ('view_all_services',):          # reuse the site's existing strings, never overwrite them
        EN_KEYS[k], AR_KEYS[k] = en0[k], ar0[k]
    results = [build_hub()] + [build_sector(s) for s in SECTORS] + [build_policy()]
    merge_json('assets/translations/en.json', EN_KEYS)
    merge_json('assets/translations/ar.json', AR_KEYS)
    pages = json.loads((ROOT / 'scripts/pages.json').read_text('utf-8'))
    have = {p['src'] for p in pages['pages']}
    ap = json.loads((ROOT / 'assets/translations/ar-pages.json').read_text('utf-8'))
    for src, url, meta in results:
        if src not in have:
            pages['pages'].append({'src': src, 'url': url, 'ar': True})
        ap[src] = meta
    (ROOT / 'scripts/pages.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    (ROOT / 'assets/translations/ar-pages.json').write_text(json.dumps(ap, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print('built', len(results), 'pages;', len(EN_KEYS), 'strings')


if __name__ == '__main__':
    main()
