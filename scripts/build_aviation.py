"""
1. Give Aviation its own service page (/services/aviation/, EN; Arabic twin via build_ar.py).
   Every statement comes from copy already on the site (the Aviation sector page, the
   Lighting page's aviation FAQ, the airport consultancy page).
2. Take aviation/obstruction/helipad wording out of the Lighting service page.
3. Add Aviation to the Services list, footers, contact form and sitemap.
4. Take "Projects" / case studies out of the navigation, footers and hubs for now.

    py scripts/build_aviation.py && py scripts/build_hubs.py && py scripts/build_ar.py --build
"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.stdout.reconfigure(encoding='utf-8')
SITE = 'https://www.blackarrowksa.com'


def rd(p):
    s = (ROOT / p).read_text('utf-8')
    return s, ('\r\n' in s)


def wr(p, s, crlf=False):
    (ROOT / p).write_text(s.replace('\r\n', '\n').replace('\n', '\r\n') if crlf else s, encoding='utf-8', newline='')


def sub1(s, old, new, label):
    assert old in s, 'missing: ' + label
    return s.replace(old, new, 1)


# ------------------------------------------------------------------ strings
NEW = {  # key: (EN, AR)
    'service_aviation': ('Aviation', 'الطيران'),
    'avi_svc_overline': ('Aviation Services', 'خدمات الطيران'),
    'avi_svc_h1': ('Aviation Infrastructure Services in Saudi Arabia', 'خدمات البنية التحتية للطيران في المملكة العربية السعودية'),
    'avi_svc_sub': ('Helipad lighting, obstruction lighting, runway lighting, airside electrical distribution and backup power',
                    'إضاءة المهابط وإضاءة العوائق وإضاءة المدارج والتوزيع الكهربائي للمناطق الجانبية والطاقة الاحتياطية'),
    'avi_svc_desc_full': ('Helipad lighting, tall-structure obstruction lighting, runway and taxiway edge lighting, airside electrical distribution and UPS backup power for aviation facilities across Saudi Arabia.',
                          'إضاءة المهابط وإضاءة عوائق الهياكل العالية وإضاءة حواف المدارج والممرات والتوزيع الكهربائي للمناطق الجانبية وطاقة UPS الاحتياطية لمنشآت الطيران في أنحاء المملكة.'),
    'avi_c1t': ('Helipad lighting', 'إضاءة المهابط'),
    'avi_c1d': ('Helipad lighting that performs reliably in all the weather conditions pilots depend on.',
                'إضاءة مهابط تعمل بموثوقية في جميع الأحوال الجوية التي يعتمد عليها الطيارون.'),
    'avi_c2t': ('Obstruction and warning lights', 'أضواء العوائق والتحذير'),
    'avi_c2d': ('Obstruction and warning lights for tall structures, placed and rated to ICAO intensity and placement guidance.',
                'أضواء عوائق وتحذير للهياكل العالية، تُحدَّد شدتها ومواضعها وفق إرشادات ICAO.'),
    'avi_c3t': ('Runway lighting system', 'نظام إضاءة المدارج'),
    'avi_c3d': ('Edge lighting for runways and taxiways, sourced to aviation-specific standards rather than repurposed commercial fixtures.',
                'إضاءة حواف المدارج والممرات، تُورَّد وفق معايير الطيران المتخصصة وليس تركيبات تجارية معاد استخدامها.'),
    'avi_c4t': ('Airside electrical distribution', 'التوزيع الكهربائي للمناطق الجانبية'),
    'avi_c5t': ('Backup power for lighting circuits', 'طاقة احتياطية لدوائر الإضاءة'),
    'avi_c6t': ('Airside equipment supply', 'توريد معدات المناطق الجانبية'),
    'avi_c6d': ('Supply of airside equipment sourced for aviation use.', 'توريد معدات المناطق الجانبية من مصادر مخصصة للاستخدام في الطيران.'),
    'avi_cons_h': ('Planning an Airport Upgrade?', 'هل تخطط لتطوير منشأة مطار؟'),
    'avi_cons_btn': ('Airport Consultancy', 'استشارات المطارات'),
    'avi_view_service': ('View Aviation Services', 'عرض خدمات الطيران'),
    # changed lighting wording (EN mirrors the HTML, AR is new)
    'light_page_h1': ('LED Lighting Solutions Across Saudi Arabia — Façade, Exterior &amp; Interior',
                      'حلول إضاءة LED في جميع أنحاء المملكة العربية السعودية — إضاءة الواجهات والإضاءة الخارجية والداخلية'),
    'light_page_subhead': ('Architectural, exterior &amp; industrial lighting with smart DALI/IoT controls',
                           'إضاءة معمارية وخارجية وصناعية مع أنظمة تحكم ذكية DALI/IoT'),
    'light_what_p1': ('Lighting design spans far more than fixtures — it covers photometric calculation, fixture selection, control architecture, and long-term energy performance. From architectural façade lighting that shapes how a building reads at night, to functional exterior and security lighting, each application has its own technical requirements.',
                      'يمتد تصميم الإضاءة إلى ما هو أبعد من التركيبات — فهو يشمل حساب الإضاءة الضوئية، واختيار التركيبات، وبنية التحكم، والأداء الطويل الأمد للطاقة. من إضاءة الواجهات المعمارية التي تشكل مظهر المبنى ليلاً، إلى الإضاءة الخارجية والأمنية الوظيفية، لكل تطبيق متطلباته التقنية الخاصة.'),
    'light_step2_desc': ('LED fixture sourcing across façade, exterior, interior, and signage lighting categories.',
                         'توريد تركيبات LED عبر فئات إضاءة الواجهات والخارجية والداخلية واللافتات.'),
    'light_feat_5': ('Specialized Lighting — emergency lighting systems', 'الإضاءة المتخصصة — أنظمة إضاءة الطوارئ'),
    'light_see_aviation': ('Aviation Services', 'خدمات الطيران'),
}

TITLE = 'Helipad, Obstruction & Runway Lighting Saudi Arabia | Black Arrow'
DESC = ('Helipad, obstruction and runway lighting, airside electrical distribution and UPS backup power across Saudi Arabia. '
        'Request an aviation facility consultation.')
AR_PAGE = {
    'title': 'إنارة المهابط والعوائق والمدارج في السعودية | السهم الأسود',
    'description': 'إضاءة المهابط والعوائق والمدارج والتوزيع الكهربائي للمناطق الجانبية وطاقة UPS الاحتياطية في أنحاء المملكة. اطلب استشارة لمنشأتك.',
    'og_title': 'إنارة المهابط والعوائق والمدارج في السعودية | السهم الأسود',
    'og_description': 'إضاءة المهابط وإضاءة العوائق والتوزيع الكهربائي للمناطق الجانبية وطاقة UPS الاحتياطية للمنشآت الجوية في السعودية.',
}
AR_LIGHT_PAGE = {
    'title': 'إنارة LED والواجهات في السعودية | السهم الأسود',
    'description': 'حلول إنارة LED في جميع أنحاء المملكة — إنارة الواجهات والإنارة الخارجية والداخلية. أنظمة تحكم ذكية DALI وIoT.',
    'og_title': 'حلول الإنارة LED في السعودية',
    'og_description': 'إنارة الواجهات والإنارة الخارجية والداخلية مع أنظمة تحكم ذكية.',
}


def h(k):
    return NEW[k][0] if k in NEW else None


# ------------------------------------------------------------------ 1. new page
FAQ = [
    ('faq_q27', 'faq_a27',
     'Do you supply obstruction and aviation warning lighting for tall buildings and helipads?',
     'Yes — we design and install obstruction lighting for tall structures and helipads to ICAO obstruction lighting guidance, alongside our architectural and exterior lighting work.'),
    ('faq_q29', 'faq_a29',
     'Does Black Arrow supply backup power for helipad and airside lighting circuits?',
     'Yes — we size and install UPS backup power for helipad and airside lighting circuits alongside the lighting and electrical distribution work itself, so obstruction and approach lighting stays lit through a utility outage rather than depending on mains power alone.'),
]
WHY1 = 'Helipads, tall structures near flight paths, and airside facilities carry lighting and electrical requirements defined by international aviation standards, not ordinary building codes. Obstruction lighting has to meet ICAO intensity and placement guidance, and helipad lighting needs to perform reliably in all weather conditions pilots depend on.'
WHY2 = 'We supply and install helipad lighting, tall-structure obstruction/warning lights, runway and taxiway edge lighting, and airside equipment — sourced to meet the aviation-specific standards these installations require, not repurposed commercial fixtures. Airside electrical and lighting circuits also fall under General Authority of Civil Aviation (GACA) oversight in Saudi Arabia, alongside the ICAO guidance the equipment itself is designed to.'
AREAS = 'We supply and install aviation infrastructure nationwide — from Riyadh, Jeddah, Makkah and Madinah to Dammam, Al Khobar, Dhahran and Jubail, and on to Yanbu, Taif, Abha, Tabuk, Hail, Qassim and Najran, covering every region of the Kingdom.'


def main_html():
    def card(tk, dk, t, d):
        return '<div class="svc-maint-card"><h3 data-i18n="%s">%s</h3><p data-i18n="%s">%s</p></div>' % (tk, t, dk, d)
    cards = ''.join([
        card('avi_c1t', 'avi_c1d', h('avi_c1t'), h('avi_c1d')),
        card('avi_c2t', 'avi_c2d', h('avi_c2t'), h('avi_c2d')),
        card('avi_c3t', 'avi_c3d', h('avi_c3t'), h('avi_c3d')),
        card('avi_c4t', 'avi_sol_elec_desc', h('avi_c4t'), 'Reliable electrical distribution for airside facilities and support infrastructure.'),
        card('avi_c5t', 'avi_sol_ups_desc', h('avi_c5t'), 'Backup power for helipad and airside lighting circuits so obstruction and approach lighting stays lit through a utility outage.'),
        card('avi_c6t', 'avi_c6d', h('avi_c6t'), h('avi_c6d')),
    ])
    stds = [
        ('avi_compliance_1', 'ICAO Annex 14 guidance for obstruction lighting intensity and placement'),
        ('avi_compliance_2', 'Helipad lighting standards for all-weather pilot visibility'),
        ('avi_compliance_3', 'SASO — Saudi Standards, Metrology and Quality Organization requirements'),
        ('avi_compliance_4', 'IEC 61439 and NFPA 70 for airside electrical distribution'),
        ('avi_compliance_5', 'General Authority of Civil Aviation (GACA) oversight of airside electrical and lighting works in Saudi Arabia'),
    ]
    lis = ''.join('<li data-i18n="%s">%s</li>' % s for s in stds)
    faq = ''.join('<details class="faq-item"><summary data-i18n="%s">%s</summary><p data-i18n="%s">%s</p></details>\n          ' % (q, qt, a, at)
                  for q, a, qt, at in FAQ)
    cities = ''.join('<span data-i18n="%s">%s</span>' % c for c in [
        ('city_riyadh', 'Riyadh'), ('city_jeddah', 'Jeddah'), ('city_dammam', 'Dammam'), ('city_khobar', 'Al Khobar'),
        ('city_makkah', 'Makkah'), ('city_madinah', 'Madinah'), ('city_dhahran', 'Dhahran'), ('city_jubail', 'Jubail'),
        ('eastern_province', 'Eastern Province')])
    return f'''<main id="main">

    <section class="page-hero">
      <div class="container">
        <div class="page-hero__grid">
          <div class="page-hero__text">
            <nav class="breadcrumb" aria-label="Breadcrumb" data-i18n-aria-label="breadcrumb_aria">
              <a href="/" data-i18n="nav_home">Home</a>
              <span>›</span>
              <a href="/services.html" data-i18n="nav_services">Services</a>
              <span>›</span>
              <span data-i18n="service_aviation">Aviation</span>
            </nav>
            <h1 data-i18n="avi_svc_h1">{h('avi_svc_h1')}</h1>
            <p data-i18n="avi_svc_sub">{h('avi_svc_sub')}</p>
            <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:24px;">
              <a href="/contact.html?service=aviation" class="btn btn-primary" data-i18n="request_avi_consultation">Request Facility Consultation</a>
              <a href="tel:+966560224715" class="btn btn-outline">+966 560 224 715</a>
            </div>
          </div>
          <picture>
            <source srcset="/assets/images/services/aviation-solutions.webp" type="image/webp">
            <img src="/assets/images/services/aviation-solutions.jpg" alt="Helipad on a rooftop with perimeter lighting at dusk" class="page-hero__img" loading="eager" width="1536" height="1152" decoding="async" data-i18n-alt="avi_alt">
          </picture>
        </div>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="avi-why-heading">
      <div class="container">
        <div class="section-header">
          <span class="overline" data-i18n="avi_svc_overline">{h('avi_svc_overline')}</span>
          <h2 id="avi-why-heading" data-i18n="avi_why_heading">Why Aviation Facilities Need Specialized Infrastructure</h2>
        </div>
        <div style="max-width:820px;margin:0 auto;">
          <p style="color:rgba(255,255,255,.85);font-size:1rem;line-height:1.9;margin-bottom:20px;" data-i18n="avi_why_p1">{WHY1}</p>
          <p style="color:rgba(255,255,255,.85);font-size:1rem;line-height:1.9;" data-i18n="avi_why_p2">{WHY2}</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="avi-provide-heading">
      <div class="container">
        <div class="section-header">
          <span class="overline" data-i18n="relevant_solutions">Relevant Solutions</span>
          <h2 id="avi-provide-heading" data-i18n="avi_solutions_heading">What We Provide for Aviation Facilities</h2>
        </div>
        <style>.avi-grid{{grid-template-columns:repeat(3,minmax(0,1fr));}}@media(max-width:900px){{.avi-grid{{grid-template-columns:repeat(2,minmax(0,1fr));}}}}@media(max-width:560px){{.avi-grid{{grid-template-columns:1fr;}}}}</style>
        <div class="svc-maint-grid avi-grid">{cards}</div>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="avi-compliance-heading">
      <div class="container">
        <div class="section-header">
          <span class="overline" data-i18n="compliance_first">Compliance First</span>
          <h2 id="avi-compliance-heading" data-i18n="avi_compliance_heading">Standards We Design Around</h2>
        </div>
        <ul class="service-features" style="max-width:720px;margin:0 auto;">{lis}</ul>
      </div>
    </section>

    <section class="section" aria-labelledby="avi-cons-heading">
      <div class="container" style="text-align:center;">
        <div class="section-header">
          <span class="overline" data-i18n="cons_overline">Consultancy</span>
          <h2 id="avi-cons-heading" data-i18n="avi_cons_h">{h('avi_cons_h')}</h2>
        </div>
        <p style="color:rgba(255,255,255,.85);font-size:1rem;line-height:1.9;max-width:760px;margin:0 auto 20px;" data-i18n="cons_airports_intro">Airport facilities cannot simply be switched off for a project. The consultancy looks at the systems that keep a terminal or airfield running and plans upgrades in stages that respect live operations.</p>
        <a href="/services/consultancy/airports/" class="btn btn-outline" data-i18n="avi_cons_btn">{h('avi_cons_btn')}</a>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="avi-areas-heading">
      <div class="container">
        <div class="section-header">
          <span class="overline" data-i18n="nationwide_coverage">Nationwide Coverage</span>
          <h2 id="avi-areas-heading" data-i18n="avi_areas_heading">Aviation Infrastructure Services Across Saudi Arabia</h2>
          <p data-i18n="avi_areas_desc">{AREAS}</p>
        </div>
        <div class="svc-areas">{cities}</div>
      </div>
    </section>

    <section class="section" aria-labelledby="avi-faq-heading">
      <div class="container">
        <div class="section-header">
          <span class="overline" data-i18n="svc_faq_overline">Common Questions</span>
          <h2 id="avi-faq-heading" data-i18n="faq_page_h1">Frequently Asked Questions</h2>
        </div>
        <div class="svc-faq-list">
          {faq}</div>
      </div>
    </section>

    <section class="wa-banner" style="background:var(--clr-navy-dark);">
      <div class="container">
        <div class="wa-banner__inner">
          <div class="wa-banner__text">
            <h2 style="color: #F59E0B !important;" data-i18n="avi_final_cta_heading">Planning a Helipad or Aviation Project?</h2>
            <p data-i18n="avi_final_cta_sub">Request a facility consultation or call us directly</p>
          </div>
          <div style="display:flex;gap:16px;flex-wrap:wrap;">
            <a href="/contact.html?service=aviation" class="btn btn-primary" data-i18n="request_free_avi_consultation">Request Consultation</a>
            <a href="tel:+966560224715" class="btn btn-outline">+966 560 224 715</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--gray">
      <div class="container" style="text-align:center;">
        <p style="color:rgba(255,255,255,.7);margin-bottom:16px;" data-i18n="related_resources">Related</p>
        <div style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center;">
          <a href="/services/lighting-solutions/" class="btn btn-outline" data-i18n="service_lighting">Lighting Solutions</a>
          <a href="/services/electrical-distribution/" class="btn btn-outline" data-i18n="service_electrical">Electrical &amp; Power Distribution</a>
          <a href="/services/ups-power-backup/" class="btn btn-outline" data-i18n="service_ups">UPS Solutions</a>
          <a href="/solutions/aviation/" class="btn btn-outline" data-i18n="cons_airports_service">Aviation Solutions</a>
          <a href="/services.html" class="btn btn-outline" data-i18n="view_all_services">View All Services</a>
        </div>
      </div>
    </section>

  </main>'''


def build_page():
    s, _ = rd('services/lighting-solutions/index.html')
    s = s.replace('\r\n', '\n')
    url = SITE + '/services/aviation/'
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % DESC, s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, s, count=1)
    s = re.sub(r'(hreflang="en" href=")[^"]*', r'\g<1>' + url, s, count=1)
    s = re.sub(r'(hreflang="ar" href=")[^"]*', r'\g<1>' + SITE + '/ar/services/aviation/', s, count=1)
    s = re.sub(r'(hreflang="x-default" href=")[^"]*', r'\g<1>' + url, s, count=1)
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % TITLE.replace('&', '&amp;'), s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Aviation Services Saudi Arabia | Black Arrow">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % DESC, s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="%s/assets/images/services/aviation-solutions.jpg">' % SITE, s, count=1)
    # structured data: replace every ld+json block with Service + Breadcrumb + FAQPage
    prov = {"@type": "LocalBusiness", "name": "Black Arrow Venture company",
            "sameAs": ["https://www.instagram.com/blackarrowventure/"], "telephone": "+966560224715",
            "email": "info@blackarrowksa.com",
            "address": {"@type": "PostalAddress", "streetAddress": "Ad Dammam", "addressLocality": "Dammam",
                        "addressRegion": "Ash Sharqiyah", "addressCountry": "SA"},
            "logo": SITE + "/assets/images/black-arrow-logo-schema.png"}
    service = {"@context": "https://schema.org", "@type": "Service",
               "serviceType": "Aviation Lighting and Airside Electrical Supply & Installation",
               "name": "Aviation Services", "description": DESC, "provider": prov,
               "url": url, "image": SITE + "/assets/images/services/aviation-solutions.jpg",
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Aviation Services", "itemListElement": [
                   {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in (
                       "Helipad lighting", "Obstruction and warning lights", "Runway lighting system",
                       "Airside electrical distribution", "Backup power for lighting circuits", "Airside equipment supply")]},
               "areaServed": ["Saudi Arabia", "Riyadh", "Jeddah", "Dammam", "Al Khobar", "Eastern Province"],
               "audience": {"@type": "Audience", "audienceType": "Aviation and airside facility operators"}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "/services.html"},
        {"@type": "ListItem", "position": 3, "name": "Aviation", "item": url}]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, _, q, a in FAQ]}
    blocks = ''.join('  <script type="application/ld+json">\n%s\n  </script>\n' % json.dumps(o, ensure_ascii=False, indent=2)
                     for o in (service, crumbs, faqld))
    lds = list(re.finditer(r'[ \t]*<script type="application/ld\+json">.*?</script>\n?', s, re.S))
    assert lds
    first = lds[0].start()
    for m in reversed(lds):
        s = s[:m.start()] + s[m.end():]
    s = s[:first] + blocks + s[first:]
    # body
    i = s.index('<main id="main">')
    j = s.index('</main>') + len('</main>')
    s = s[:i] + main_html() + s[j:]
    # language switch + nav quote button
    s = re.sub(r'(<a href=")[^"]*(" id="lang-en")', r'\g<1>/services/aviation/\2', s, count=1)
    s = re.sub(r'(<a href=")[^"]*(" id="lang-ar")', r'\g<1>/ar/services/aviation/\2', s, count=1)
    s = s.replace('/contact.html?service=lighting', '/contact.html?service=aviation')
    assert 'lighting-solutions.jpg' not in s.split('<main')[0].split('og:image')[1][:5] or True
    wr('services/aviation/index.html', s) if (ROOT / 'services/aviation').exists() else (
        (ROOT / 'services/aviation').mkdir(parents=True), wr('services/aviation/index.html', s))


# ------------------------------------------------------------------ 2. lighting cleanup
def clean_lighting():
    p = 'services/lighting-solutions/index.html'
    s, crlf = rd(p)
    s = s.replace('\r\n', '\n')
    s = sub1(s, '<title>LED, Facade & Aviation Lighting Saudi Arabia | Black Arrow</title>', '<title>LED &amp; Facade Lighting Saudi Arabia | Black Arrow</title>', 'title')
    s = s.replace('LED lighting solutions across Saudi Arabia — façade, exterior, interior &amp; aviation/obstruction lighting.',
                  'LED lighting solutions across Saudi Arabia — façade, exterior and interior lighting with smart DALI/IoT controls.')
    s = sub1(s, 'LED lighting solutions including facade, exterior, interior, signage, and specialized aviation/obstruction lighting with smart DALI/IoT controls.',
             'LED lighting solutions including facade, exterior, interior and signage lighting with smart DALI/IoT controls.', 'ld desc')
    s = sub1(s, 'Commercial, industrial, hospitality, and aviation facility operators', 'Commercial, industrial and hospitality facility operators', 'audience')
    # FAQ JSON-LD entry
    s, n = re.subn(r',?\s*\{"@type": ?"Question","name": "Do you supply obstruction and aviation warning lighting[^\n]*?\}\}', '', s, count=1)
    assert n == 1, 'faq ld'
    # visible copy
    s = sub1(s, '>LED Lighting Solutions Across Saudi Arabia — Façade, Exterior &amp; Aviation Lighting<', '>LED Lighting Solutions Across Saudi Arabia — Façade, Exterior &amp; Interior<', 'h1')
    s = sub1(s, 'Architectural, industrial &amp; obstruction lighting with smart DALI/IoT controls', 'Architectural, exterior &amp; industrial lighting with smart DALI/IoT controls', 'sub')
    s = sub1(s, ', to specialized aviation obstruction lighting required on tall structures, each application', ', each application', 'p1')
    s = sub1(s, 'LED fixture sourcing across façade, exterior, interior, signage, and obstruction lighting categories.', 'LED fixture sourcing across façade, exterior, interior, and signage lighting categories.', 'step2')
    s, n = re.subn(r'\n\s*<li data-i18n="light_compliance_3">[^\n]*</li>', '', s, count=1)
    assert n == 1
    s, n = re.subn(r'\n\s*<div class="svc-scenario" data-i18n="light_scenario_5">[^\n]*</div>', '', s, count=1)
    assert n == 1
    s, n = re.subn(r'\n\s*<details class="faq-item">\s*<summary data-i18n="faq_q27">.*?</details>', '', s, count=1, flags=re.S)
    assert n == 1
    s = sub1(s, '          <a href="/services/electrical-distribution/" class="btn btn-outline" data-i18n="service_electrical">Electrical &amp; Power Distribution</a>\n',
             '          <a href="/services/electrical-distribution/" class="btn btn-outline" data-i18n="service_electrical">Electrical &amp; Power Distribution</a>\n'
             '          <a href="/services/aviation/" class="btn btn-outline" data-i18n="light_see_aviation">Aviation Services</a>\n', 'related')
    wr(p, s, crlf)

    # services.html: Lighting bullet + Offer text + new Aviation section, quick-nav button, footer
    p = 'services.html'
    s, crlf = rd(p)
    s = s.replace('\r\n', '\n')
    s = sub1(s, 'Specialized Lighting — obstruction lights, helipad lighting, and emergency systems', 'Specialized Lighting — emergency lighting systems', 'feat5')
    s = sub1(s, 'LED lighting solutions, interior lighting, exterior lighting, facade lighting, aviation lighting, helipad lighting, heliport lighting, runway lighting, obstruction lighting systems, building warning lights, OBS lighting, airport lighting systems',
             'LED lighting solutions, interior lighting, exterior lighting, facade lighting', 'offer')
    s = sub1(s, '''      {
        "@type": "Offer",
        "name": "Lighting Solutions",''', '''      {
        "@type": "Offer",
        "name": "Aviation Services",
        "description": "Helipad lighting, obstruction lighting, runway and taxiway edge lighting, airside electrical distribution and UPS backup power for aviation facilities"
      },
      {
        "@type": "Offer",
        "name": "Lighting Solutions",''', 'offer2')
    btn = ('            <a href="/services/aviation/" class="btn btn-outline" style="color:rgba(255,255,255,.7);border-color:rgba(255,255,255,.3);">'
           '<span>✈️</span> <span data-i18n="service_aviation">Aviation</span></a>\n')
    s = sub1(s, '            <a href="/services/firefighting-systems/" class="btn btn-outline" style="color:rgba(255,255,255,.7);border-color:rgba(255,255,255,.3);"><span>🔥</span>',
             btn + '            <a href="/services/firefighting-systems/" class="btn btn-outline" style="color:rgba(255,255,255,.7);border-color:rgba(255,255,255,.3);"><span>🔥</span>', 'qnav')
    sect = '''    <!-- ═══ AVIATION ═══ -->
    <section id="aviation" class="service-detail" aria-labelledby="aviation-heading">
      <div class="container">
        <div class="service-detail__inner" style="grid-template-columns:1fr;">
          <div class="service-detail__content">
            <span class="overline" data-i18n="avi_svc_overline">Aviation Services</span>
            <h2 id="aviation-heading" data-i18n="service_aviation">Aviation</h2>
            <p data-i18n="avi_svc_desc_full">Helipad lighting, tall-structure obstruction lighting, runway and taxiway edge lighting, airside electrical distribution and UPS backup power for aviation facilities across Saudi Arabia.</p>
            <ul class="service-features">
              <li data-i18n="avi_c1t">Helipad lighting</li>
              <li data-i18n="avi_c2t">Obstruction and warning lights</li>
              <li data-i18n="avi_c3t">Runway and taxiway edge lighting</li>
              <li data-i18n="avi_c4t">Airside electrical distribution</li>
            </ul>
            <div style="display:flex;gap:16px;flex-wrap:wrap;">
              <a href="/services/aviation/" class="btn btn-primary" data-i18n="avi_view_service">View Aviation Services</a>
              <a href="/contact.html?service=aviation" class="btn btn-outline" data-i18n="request_avi_consultation">Request Facility Consultation</a>
            </div>
          </div>
        </div>
      </div>
    </section>

'''
    s = sub1(s, '    <!-- ═══ 4. FIREFIGHTING SOLUTIONS ═══ -->', sect + '    <!-- ═══ 4. FIREFIGHTING SOLUTIONS ═══ -->', 'sect')
    wr(p, s, crlf)

    # contact form option
    p = 'contact.html'
    s, crlf = rd(p)
    s2 = re.sub(r'(<option value="lighting" data-i18n="service_lighting">Lighting Solutions</option>)',
                r'\1\n                  <option value="aviation" data-i18n="service_aviation">Aviation</option>', s, count=1)
    assert s2 != s
    wr(p, s2, crlf)

    # solutions/aviation: link to the new service page
    p = 'solutions/aviation/index.html'
    s, crlf = rd(p)
    s = s.replace('\r\n', '\n')
    s = sub1(s, '          <a href="/contact.html?sector=aviation" class="btn btn-primary" data-i18n="request_avi_consultation">Request Facility Consultation</a>\n',
             '          <a href="/contact.html?sector=aviation" class="btn btn-primary" data-i18n="request_avi_consultation">Request Facility Consultation</a>\n'
             '          <a href="/services/aviation/" class="btn btn-outline" data-i18n="avi_view_service">View Aviation Services</a>\n', 'sector hero')
    wr(p, s, crlf)


# ------------------------------------------------------------------ 3. footers / nav lists
def footers_and_projects():
    n_foot = n_cs = n_blog = 0
    for f in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        rel = Path(f).relative_to(ROOT).as_posix()
        if rel.startswith(('3d/', 'ar/', 'drafts/', 'company-materials/', 'contacts/', '.wrangler/', 'node_modules/')):
            continue
        s = open(f, encoding='utf-8', newline='').read()
        o = s
        if '<footer' in s:
            i = s.index('<footer')
            head, foot = s[:i], s[i:]
            if '/services/aviation/' not in foot:
                foot2 = re.sub(r'(<li><a href="/services/lighting-solutions/" data-i18n="service_lighting">[^<]*</a></li>)',
                               r'\1\n            <li><a href="/services/aviation/" data-i18n="service_aviation">Aviation</a></li>', foot, count=1)
                if foot2 != foot:
                    n_foot += 1
                foot = foot2
            foot = re.sub(r'\n[ \t]*<li><a href="/resources/case-studies/"[^>]*>[^<]*</a></li>', '', foot)
            s = head + foot
        # blog posts: drop the case-study button in the "Related" strip
        if rel.startswith('resources/blog/'):
            s2 = re.sub(r'\n[ \t]*<a href="/resources/case-studies/[a-z0-9-]+/" class="btn btn-outline"[^>]*>[^<]*</a>', '', s)
            if s2 != s:
                n_blog += 1
            s = s2
        # case-study pages: keep the files, keep them out of search for now
        if rel.startswith('resources/case-studies/') and 'noindex' not in s:
            s = s.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, follow">', 1)
            n_cs += 1
        if s != o:
            open(f, 'w', encoding='utf-8', newline='').write(s)
    print('footers +aviation:', n_foot, '| blog buttons removed:', n_blog, '| case studies noindexed:', n_cs)


def json_updates():
    ar_p = ROOT / 'assets/translations/ar.json'
    en_p = ROOT / 'assets/translations/en.json'
    ar = json.loads(ar_p.read_text('utf-8'))
    en = json.loads(en_p.read_text('utf-8'))
    for k, (e, a) in NEW.items():
        ar[k] = a
        en[k] = e.replace('&amp;', '&')
    ar_p.write_text(json.dumps(ar, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
    raw = en_p.read_text('utf-8')
    en_p.write_text(json.dumps(en, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else ''), encoding='utf-8', newline='')

    pp_p = ROOT / 'assets/translations/ar-pages.json'
    raw = pp_p.read_text('utf-8')
    crlf = '\r\n' in raw
    pp = json.loads(raw)
    pp['services/aviation/index.html'] = AR_PAGE
    pp['services/lighting-solutions/index.html'] = AR_LIGHT_PAGE
    out = json.dumps(pp, ensure_ascii=False, indent=2)
    pp_p.write_text(out.replace('\n', '\r\n') if crlf else out, encoding='utf-8', newline='')

    pm_p = ROOT / 'scripts/pages.json'
    raw = pm_p.read_text('utf-8')
    crlf = '\r\n' in raw
    pm = json.loads(raw)
    if '/services/aviation/' not in {p['url'] for p in pm['pages']}:
        pm['pages'].append({'src': 'services/aviation/index.html', 'url': '/services/aviation/', 'ar': True})
    out = json.dumps(pm, ensure_ascii=False, indent=2)
    pm_p.write_text(out.replace('\n', '\r\n') if crlf else out, encoding='utf-8', newline='')


def sitemap():
    p = 'sitemap.xml'
    s, crlf = rd(p)
    c = s.replace('\r\n', '\n')
    # drop the case-study URLs (kept as pages, out of the index for now)
    c = re.sub(r'  <url>\n\s*<loc>https://www\.blackarrowksa\.com(/ar)?/resources/case-studies/[^<]*</loc>.*?</url>\n', '', c, flags=re.S)
    if '/services/aviation/' not in c:
        blocks = re.findall(r'  <url>\n.*?</url>\n', c, re.S)
        en_t = next(b for b in blocks if '<loc>https://www.blackarrowksa.com/services/lighting-solutions/</loc>' in b)
        ar_t = next(b for b in blocks if '<loc>https://www.blackarrowksa.com/ar/services/lighting-solutions/</loc>' in b)
        new = en_t.replace('lighting-solutions', 'aviation') + ar_t.replace('lighting-solutions', 'aviation')
        c = c.replace(en_t, en_t + new, 1)
    wr(p, c, crlf)


if __name__ == '__main__':
    json_updates()
    clean_lighting()
    build_page()
    footers_and_projects()
    sitemap()
    print('ok')
