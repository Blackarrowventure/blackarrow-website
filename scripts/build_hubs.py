"""
One-shot structural pass for the main site:

  * grouped navigation (Services / Industries / Projects / Resources / About
    dropdowns) applied to every English page that carries the site navbar;
  * two new hub pages: /solutions/ (Industries) and /resources/ (Resources);
  * new Arabic strings, manifest entries and dropdown CSS.

Nothing here invents company facts: every label and blurb is taken from pages
that already exist (their H1s / sub-headings and their Arabic keys).

    py scripts/build_hubs.py

Safe to re-run: the navbar block is replaced wholesale, hub pages are rewritten,
JSON entries are set (not appended).  Run scripts/build_ar.py --build afterwards.
"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.stdout.reconfigure(encoding='utf-8')

SITE = 'https://www.blackarrowksa.com'

# ---------------------------------------------------------------- strings
NEW_AR = {
    'nav_industries': 'القطاعات',
    'nav_projects': 'المشاريع',
    'nav_resources': 'المصادر',
    'nav_company_profile': 'ملف الشركة',
    'nav_certifications': 'الشهادات',
    'nav_ind_hospitals': 'المستشفيات والرعاية الصحية',
    'nav_ind_commercial': 'المولات والمكاتب والتجزئة',
    'nav_ind_government': 'المنشآت الحكومية',
    'nav_ind_hospitality': 'الفنادق والضيافة',
    'nav_ind_industrial': 'المصانع والمنشآت الصناعية',
    'nav_ind_aviation': 'الطيران',
    'nav_technical_articles': 'مقالات تقنية',
    'nav_guides': 'الأدلة',
    'nav_downloads': 'التحميلات',
    'ind_hub_h1': 'القطاعات التي نخدمها',
    'ind_hub_sub': 'حلول البنية التحتية حسب نوع المنشأة',
    'ind_hub_intro': 'تختلف متطلبات الطاقة والتكييف والسلامة من منشأة إلى أخرى. اختر قطاعك لترى الخدمات التي نقدمها له.',
    'ind_hub_more': 'عرض الحلول ←',
    'ind_hub_services_h2': 'الخدمات',
    'ind_hub_services_p': 'كل قطاع يعتمد على مجموعة من هذه الخدمات. يمكنك أيضاً تصفح جميع خدماتنا مباشرة.',
    'res_hub_h1': 'المصادر',
    'res_hub_sub': 'مقالات تقنية وأدلة وأسئلة شائعة ودراسات حالة وملف الشركة',
    'res_hub_intro': 'كل ما نشرناه في مكان واحد: مقالات تقنية عن المعايير والتصميم، وأدلة عملية، وإجابات عن الأسئلة المتكررة، وحسابات مشاريع تمثيلية.',
    'res_hub_articles_h2': 'المقالات التقنية',
    'res_hub_articles_p': 'شروحات عن المعايير والاختيار والتصميم في المنشآت السعودية.',
    'res_hub_all_articles': 'جميع المقالات ←',
    'res_hub_guides_h2': 'الأدلة',
    'res_hub_faq_h2': 'الأسئلة الشائعة',
    'res_hub_faq_p': 'إجابات عن الأسئلة التي نتلقاها بشكل متكرر عن خدماتنا وطريقة العمل.',
    'res_hub_faq_link': 'عرض الأسئلة الشائعة ←',
    'res_hub_cs_h2': 'دراسات الحالة',
    'res_hub_cs_p': 'حسابات تمثيلية لمشاريع في الرعاية الصحية والتجارة والضيافة والطيران.',
    'res_hub_cs_link': 'عرض دراسات الحالة ←',
    'res_hub_dl_h2': 'التحميلات',
    'res_hub_dl_p': 'ملف الشركة بصيغة PDF أو عبر الإنترنت.',
    'res_hub_dl_pdf': 'تحميل ملف الشركة (PDF)',
    'res_hub_dl_web': 'عرض ملف الشركة',
}

# short (dropdown) labels, English
IND = [
    ('hospitals', 'nav_ind_hospitals', 'Hospitals &amp; Healthcare', 'hosp_page_h1', 'hosp_page_subhead',
     'Infrastructure Solutions for Hospitals &amp; Healthcare Facilities',
     'Isolated power panels, UPS, HVAC &amp; fire safety systems built for compliance and zero-downtime operation'),
    ('commercial', 'nav_ind_commercial', 'Malls, Offices &amp; Retail', 'comm_page_h1', 'comm_page_subhead',
     'Infrastructure Solutions for Malls, Offices &amp; Retail',
     'EV charging, HVAC, lighting &amp; electrical distribution built for commercial facility operators'),
    ('government', 'nav_ind_government', 'Government Facilities', 'gov_page_h1', 'gov_page_subhead',
     'Infrastructure Solutions for Government Facilities',
     'Electrical distribution, lighting &amp; fire safety systems built for public-sector compliance and reliability'),
    ('hospitality', 'nav_ind_hospitality', 'Hotels &amp; Hospitality', 'hosp2_page_h1', 'hosp2_page_subhead',
     'Infrastructure Solutions for Hotels &amp; Hospitality',
     'EV charging, lighting &amp; HVAC systems built for guest experience and reliable operations'),
    ('industrial', 'nav_ind_industrial', 'Industrial Plants &amp; Factories', 'ind_page_h1', 'ind_page_subhead',
     'Infrastructure Solutions for Industrial Plants &amp; Factories',
     'Electrical distribution, firefighting &amp; HVAC systems built for continuous industrial operation'),
    ('aviation', 'nav_ind_aviation', 'Aviation', 'avi_page_h1', 'avi_page_subhead',
     'Aviation Infrastructure Solutions &mdash; Helipad &amp; Obstruction Lighting',
     'ICAO-compliant obstruction lighting, electrical systems &amp; aviation equipment supply'),
]

SERVICES = [
    ('/services/ups-power-backup/', 'service_ups', 'UPS Solutions'),
    ('/services/isolated-power-panels/', 'service_ipp', 'Isolated Power Panels'),
    ('/services/ev-charging-solutions/', 'service_ev', 'EV Solutions'),
    ('/services/hvac-solutions/', 'service_hvac', 'HVAC Solutions'),
    ('/services/electrical-distribution/', 'service_electrical', 'Electrical &amp; Power'),
    ('/services/firefighting-systems/', 'service_fire', 'Firefighting'),
    ('/services/lighting-solutions/', 'service_lighting', 'Lighting Solutions'),
    ('/services/hospital-modular-or-rooms/', 'service_or_rooms', 'Hospital Modular OR Rooms'),
    ('/services/lead-sheets-hospital/', 'service_lead_shielding', 'Lead Sheets for Hospitals'),
    ('/services/consultancy/', 'service_consultancy', 'Technical Consultancy'),
]

GUIDES = [
    ('/services/ups-sizing-guide/', 'sizing_h1', 'UPS Sizing &amp; Runtime Guide'),
    ('/services/vrla-vs-lithium-ups-batteries/', 'vrlali_h1', 'VRLA vs Lithium-Ion UPS Batteries'),
]

FEATURED_ARTICLES = [
    ('nfpa-99-compliance-saudi-hospitals', 'nfpa_post_h1', 'NFPA 99 Compliance for Saudi Hospitals: A Practical Guide'),
    ('sizing-ups-hospital-critical-branch', 'post_sizing_ups_hospital_critical_branch_h1', 'Sizing a UPS for a Hospital Critical Branch'),
    ('why-hospitals-need-isolated-power-panels', 'ipp_blog_h1', 'Why Your Hospital Needs Isolated Power Panels'),
    ('saso-requirements-ev-chargers-saudi-arabia', 'post_saso_requirements_ev_chargers_saudi_arabia_h1', 'SASO Requirements for EV Chargers in Saudi Arabia'),
    ('vrf-vrv-hvac-saudi-commercial-buildings', 'post_vrf_vrv_hvac_h1', 'VRF vs VRV: Choosing the Right Commercial HVAC System in Saudi Arabia'),
    ('fm200-vs-water-mist-suppression-saudi-arabia', 'post_fm200_vs_water_mist_h1', 'FM-200 vs Water Mist: Choosing a Suppression System for Sensitive Areas'),
]


def a(href, key, text, cls=''):
    return '<a href="%s"%s data-i18n="%s">%s</a>' % (href, (' class="%s"' % cls) if cls else '', key, text)


def nav_block(active):
    def top(name, html):
        return html
    def link(href, key, text, name, sub=None):
        cls = 'active' if active == name else ''
        li = '<li%s>' % (' class="has-sub"' if sub else '') + a(href, key, text, cls)
        if sub:
            li += '\n            <ul class="navbar__sub" role="list">\n' + ''.join(
                '              <li>%s</li>\n' % s for s in sub) + '            </ul>\n          '
        return '          ' + li + '</li>\n'

    services_sub = [a(h, k, t) for h, k, t in SERVICES]
    ind_sub = [a('/solutions/%s/' % i[0], i[1], i[2]) for i in IND]
    res_sub = [
        a('/resources/blog/', 'nav_technical_articles', 'Technical Articles'),
        a('/resources/faqs/', 'nav_faqs', 'FAQs'),
        a('/resources/case-studies/', 'nav_case_studies', 'Case Studies'),
        a('/company-profile.html', 'nav_company_profile', 'Company Profile'),
    ]
    about_sub = [
        a('/about.html', 'nav_about', 'About Us'),
        a('/certifications/', 'nav_certifications', 'Certifications'),
        a('/company-profile.html', 'nav_company_profile', 'Company Profile'),
        a('/become-a-partner.html', 'nav_partner', 'Become a Partner'),
    ]
    out = '<ul class="navbar__links" role="list">\n'
    out += link('/', 'nav_home', 'Home', 'home')
    out += link('/services.html', 'nav_services', 'Services', 'services', services_sub)
    out += link('/solutions/', 'nav_industries', 'Industries', 'industries', ind_sub)
    out += link('/resources/case-studies/', 'nav_projects', 'Projects', 'projects')
    out += link('/resources/', 'nav_resources', 'Resources', 'resources', res_sub)
    out += link('/about.html', 'nav_about', 'About', 'about', about_sub)
    out += link('/contact.html', 'nav_contact', 'Contact', 'contact')
    out += '        </ul>'
    return out


def active_for(rel):
    if rel == 'index.html':
        return 'home'
    if rel.startswith('services'):
        return 'services'
    if rel.startswith('solutions'):
        return 'industries'
    if rel.startswith('resources/case-studies'):
        return 'projects'
    if rel.startswith('resources'):
        return 'resources'
    if rel in ('about.html', 'become-a-partner.html', 'company-profile.html') or rel.startswith('certifications'):
        return 'about'
    if rel in ('contact.html', 'thank-you.html'):
        return 'contact'
    return None


NAV_RX = re.compile(r'<ul class="navbar__links" role="list">.*?</ul>\s*(?=<div class="navbar__actions">)', re.S)
NAV_RX_NESTED = re.compile(r'<ul class="navbar__links" role="list">.*?</li>\s*</ul>(?=\s*<div class="navbar__actions">)', re.S)


def update_navs():
    n = 0
    files = [f for f in glob.glob(str(ROOT / '**' / '*.html'), recursive=True)]
    for f in files:
        rel = Path(f).relative_to(ROOT).as_posix()
        if rel.startswith(('3d/', 'ar/', 'drafts/', 'company-materials/', 'contacts/', '.wrangler/', 'node_modules/')):
            continue
        s = open(f, encoding='utf-8', newline='').read()
        if 'class="navbar__links"' not in s:
            continue
        nl = '\r\n' if '\r\n' in s else '\n'
        t = s.replace('\r\n', '\n')
        block = nav_block(active_for(rel))
        # replace from the opening <ul> through the last </ul> before navbar__actions
        m = re.search(r'<ul class="navbar__links" role="list">.*?(?=\n\s*<div class="navbar__actions">)', t, re.S)
        if not m:
            print('  no match', rel)
            continue
        new = t[:m.start()] + block + t[m.end():]
        if new != t:
            open(f, 'w', encoding='utf-8', newline='').write(new.replace('\n', nl))
            n += 1
    print('navbars updated:', n)


# ---------------------------------------------------------------- hub pages
def load_template():
    return (ROOT / 'resources/case-studies/index.html').read_text('utf-8')


def make_hub(url_path, title, desc, h1_key, h1, sub_key, sub, body, active):
    s = load_template().replace('\r\n', '\n')
    full = SITE + url_path
    ar_full = SITE + '/ar' + url_path
    # head
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % desc, s, 1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % full, s, 1)
    s = re.sub(r'(<link rel="alternate" hreflang="en" href=")[^"]*(">)', r'\g<1>' + full + r'\2', s, 1)
    s = re.sub(r'(<link rel="alternate" hreflang="ar" href=")[^"]*(">)', r'\g<1>' + ar_full + r'\2', s, 1)
    s = re.sub(r'(<link rel="alternate" hreflang="x-default" href=")[^"]*(">)', r'\g<1>' + full + r'\2', s, 1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % title, s, 1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % desc, s, 1)
    s = s.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    s = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % full, s, 1)
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % title, s, 1)
    # JSON-LD: breadcrumb + CollectionPage in place of the Article block
    crumb = ('<script type="application/ld+json">\n  {\n    "@context": "https://schema.org",\n    "@type": "BreadcrumbList",\n'
             '    "itemListElement": [\n      { "@type": "ListItem", "position": 1, "name": "Home", "item": "%s/" },\n'
             '      { "@type": "ListItem", "position": 2, "name": "%s", "item": "%s" }\n    ]\n  }\n  </script>') % (SITE, h1.replace('&amp;', '&'), full)
    page_ld = ('<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "CollectionPage",\n'
               '  "name": "%s",\n  "description": "%s",\n  "inLanguage": "en",\n  "url": "%s",\n'
               '  "isPartOf": { "@type": "WebSite", "name": "Black Arrow Venture company", "url": "%s/" }\n}\n</script>') % (
        h1.replace('&amp;', '&'), desc.replace('&amp;', '&'), full, SITE)
    lds = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, re.S))
    assert len(lds) >= 2
    s = s[:lds[0].start()] + crumb + '\n  ' + page_ld + s[lds[-1].end():]
    # hero
    s = re.sub(r'<span data-i18n="cs_h1">Case Studies</span>', '<span data-i18n="%s">%s</span>' % (h1_key, h1), s, 1)
    s = re.sub(r'<h1 data-i18n="cs_h1">Case Studies</h1>', '<h1 data-i18n="%s">%s</h1>' % (h1_key, h1), s, 1)
    s = re.sub(r'<p data-i18n="cs_index_sub">.*?</p>', '<p data-i18n="%s">%s</p>' % (sub_key, sub), s, 1, flags=re.S)
    # main content
    a0 = s.index('<section class="section">')
    a1 = s.index('</main>')
    s = s[:a0] + body + '\n  ' + s[a1:]
    # language switcher + quote link of the template point at another page
    s = re.sub(r'(<a href=")[^"]*(" id="lang-en")', r'\g<1>' + url_path + r'\2', s, 1)
    s = re.sub(r'(<a href=")[^"]*(" id="lang-ar")', r'\g<1>/ar' + url_path + r'\2', s, 1)
    s = re.sub(r'<a href="/contact.html\?service=[a-z0-9_]+" class="btn btn-primary"', '<a href="/contact.html" class="btn btn-primary"', s, 1)
    return s


def industries_body():
    cards = ''
    for slug, nk, short, hk, sk, h, sub in IND:
        cards += ('          <a class="blog-card" href="/solutions/%s/">\n'
                  '            <h2 data-i18n="%s">%s</h2>\n'
                  '            <p data-i18n="%s">%s</p>\n'
                  '            <span class="blog-card__more" data-i18n="ind_hub_more">View solutions &rarr;</span>\n'
                  '          </a>\n') % (slug, hk, h, sk, sub)
    svc = ''.join('<li>%s</li>' % a(h, k, t) for h, k, t in SERVICES[:9])
    return ('<section class="section">\n      <div class="container" style="max-width:1100px;">\n'
            '        <p style="color:#b8b8b8;line-height:1.8;max-width:760px;margin-bottom:40px;" data-i18n="ind_hub_intro">'
            'Power, cooling and safety requirements differ from one type of facility to the next. Choose your sector to see the services we provide for it.</p>\n'
            '        <div class="blog-grid">\n' + cards + '        </div>\n'
            '        <h2 style="margin:56px 0 12px;font-size:1.4rem;color:#F59E0B;" data-i18n="ind_hub_services_h2">Services</h2>\n'
            '        <p style="color:#b8b8b8;line-height:1.8;max-width:760px;margin-bottom:14px;" data-i18n="ind_hub_services_p">'
            'Every sector draws on the same set of services. You can also browse all of them directly.</p>\n'
            '        <ul class="hub-links">' + svc + '</ul>\n'
            '        <p style="margin-top:28px;"><a class="btn btn-outline" href="/services.html" data-i18n="nav_services">Services</a></p>\n'
            '      </div>\n    </section>')


def resources_body():
    arts = ''.join('<li>%s</li>' % a('/resources/blog/%s/' % s, k, t) for s, k, t in FEATURED_ARTICLES)
    guides = ''.join('<li>%s</li>' % a(h, k, t) for h, k, t in GUIDES)
    h2 = 'style="margin:48px 0 12px;font-size:1.4rem;color:#F59E0B;"'
    p = 'style="color:#b8b8b8;line-height:1.8;max-width:760px;margin-bottom:14px;"'
    return ('<section class="section">\n      <div class="container" style="max-width:1100px;">\n'
            '        <p style="color:#b8b8b8;line-height:1.8;max-width:760px;margin-bottom:8px;" data-i18n="res_hub_intro">'
            'Everything we have published in one place: technical articles on standards and design, practical guides, answers to common questions and representative project accounts.</p>\n'
            '        <h2 %s data-i18n="res_hub_articles_h2">Technical Articles</h2>\n'
            '        <p %s data-i18n="res_hub_articles_p">Explainers on standards, selection and design for Saudi facilities.</p>\n'
            '        <ul class="hub-links">%s</ul>\n'
            '        <p style="margin-top:20px;"><a class="btn btn-outline" href="/resources/blog/" data-i18n="res_hub_all_articles">All articles &rarr;</a></p>\n'
            '        <h2 %s data-i18n="res_hub_guides_h2">Guides</h2>\n'
            '        <ul class="hub-links">%s</ul>\n'
            '        <h2 %s data-i18n="res_hub_faq_h2">FAQs</h2>\n'
            '        <p %s data-i18n="res_hub_faq_p">Answers to the questions we are asked most often about our services and how we work.</p>\n'
            '        <p><a class="btn btn-outline" href="/resources/faqs/" data-i18n="res_hub_faq_link">View the FAQs &rarr;</a></p>\n'
            '        <h2 %s data-i18n="res_hub_cs_h2">Case Studies</h2>\n'
            '        <p %s data-i18n="res_hub_cs_p">Representative project accounts across healthcare, commercial, hospitality and aviation.</p>\n'
            '        <p><a class="btn btn-outline" href="/resources/case-studies/" data-i18n="res_hub_cs_link">View the case studies &rarr;</a></p>\n'
            '        <h2 %s data-i18n="res_hub_dl_h2">Downloads</h2>\n'
            '        <p %s data-i18n="res_hub_dl_p">Our company profile, as a PDF or online.</p>\n'
            '        <p style="display:flex;gap:12px;flex-wrap:wrap;"><a class="btn btn-primary" href="/downloads/profile.pdf" data-i18n="res_hub_dl_pdf">Download the company profile (PDF)</a>'
            '<a class="btn btn-outline" href="/company-profile.html" data-i18n="res_hub_dl_web">View the company profile</a></p>\n'
            '      </div>\n    </section>') % (h2, p, arts, h2, guides, h2, p, h2, p, h2, p)


def write(path, s):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding='utf-8', newline='\n')


def main():
    # 1) Arabic strings
    ar_path = ROOT / 'assets/translations/ar.json'
    ar = json.loads(ar_path.read_text('utf-8'))
    ar.update(NEW_AR)
    ar_path.write_text(json.dumps(ar, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')

    # 2) hub pages
    ind = make_hub('/solutions/', 'Industries We Serve | Black Arrow Venture',
                   'Infrastructure solutions by sector in Saudi Arabia: hospitals, commercial, government, hospitality, industrial and aviation facilities.',
                   'ind_hub_h1', 'Industries We Serve', 'ind_hub_sub', 'Infrastructure solutions by type of facility',
                   industries_body(), 'industries')
    write('solutions/index.html', ind)
    res = make_hub('/resources/', 'Resources | Black Arrow Venture',
                   'Technical articles, guides, FAQs, case studies and the company profile from Black Arrow Venture.',
                   'res_hub_h1', 'Resources', 'res_hub_sub', 'Technical articles, guides, FAQs, case studies and the company profile',
                   resources_body(), 'resources')
    write('resources/index.html', res)

    # 3) manifests
    pm_path = ROOT / 'scripts/pages.json'
    raw = pm_path.read_text('utf-8')
    crlf = '\r\n' in raw
    pm = json.loads(raw)
    have = {p['url'] for p in pm['pages']}
    for src, url in (('solutions/index.html', '/solutions/'), ('resources/index.html', '/resources/')):
        if url not in have:
            pm['pages'].append({'src': src, 'url': url, 'ar': True})
    out = json.dumps(pm, ensure_ascii=False, indent=2)
    pm_path.write_text(out.replace('\n', '\r\n') if crlf else out, encoding='utf-8', newline='')

    pp_path = ROOT / 'assets/translations/ar-pages.json'
    raw = pp_path.read_text('utf-8')
    crlf = '\r\n' in raw
    pp = json.loads(raw)
    pp['solutions/index.html'] = {
        'title': 'القطاعات التي نخدمها | السهم الأسود ڤنتشر',
        'description': 'حلول البنية التحتية حسب القطاع في المملكة العربية السعودية: المستشفيات والمنشآت التجارية والحكومية والضيافة والصناعية والطيران.',
        'og_title': 'القطاعات التي نخدمها | السهم الأسود ڤنتشر',
        'og_description': 'حلول البنية التحتية حسب القطاع في المملكة العربية السعودية: المستشفيات والمنشآت التجارية والحكومية والضيافة والصناعية والطيران.',
    }
    pp['resources/index.html'] = {
        'title': 'المصادر | السهم الأسود ڤنتشر',
        'description': 'مقالات تقنية وأدلة وأسئلة شائعة ودراسات حالة وملف الشركة من السهم الأسود ڤنتشر.',
        'og_title': 'المصادر | السهم الأسود ڤنتشر',
        'og_description': 'مقالات تقنية وأدلة وأسئلة شائعة ودراسات حالة وملف الشركة من السهم الأسود ڤنتشر.',
    }
    out = json.dumps(pp, ensure_ascii=False, indent=2)
    pp_path.write_text(out.replace('\n', '\r\n') if crlf else out + '', encoding='utf-8', newline='')

    # 4) navbars
    update_navs()


if __name__ == '__main__':
    main()
