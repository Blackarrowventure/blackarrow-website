# -*- coding: utf-8 -*-
"""Build company-profile-document.html — the print/PDF company profile.

This is NOT company-profile.html. That one is a web page on the site, with a
generated Arabic twin and its own pre-rebrand palette (see scripts/pages.json).
This is a 16-page A4 brochure you send to a client or print to PDF.

SHAPE: a company profile, not a form. Full-bleed photography, editorial
headlines, an ink cover and back cover. The only thing carried over from
Quotation_Q2026756_Rev01.html is the COLOUR SCHEME - ink / paper / gold /
band / rule / muted. Afzal asked for the palette, not the letterhead.

CONTENT: everything is lifted from the live site. Pages 6-13 are scraped
straight out of services/<slug>/index.html at build time - tagline, intro,
the numbered process, the standards list and the application scenarios - so
the profile cannot drift from the site without this build failing loudly.
Figures and company records come from index / about / contact / the case
studies / the contact cards.

IMAGES: the site's own service photos, cropped to the hero band and
re-encoded at build time, then inlined as data URIs so the file can be
emailed whole and prints identically anywhere.

    py scripts/build_profile_doc.py            # writes the document
    py scripts/build_profile_doc.py --probe    # height-probe copy, see below

Printing:

    chrome --headless=new --no-pdf-header-footer --print-to-pdf="<out>.pdf" \
           --virtual-time-budget=8000 "file:///<abs path>/company-profile-document.html"

Every page is a fixed 1123px box that clips, so an overlong page would be
silently cut rather than reflowing. The --probe build is the same document
with the height released; print THAT and it must come out at exactly 16
pages. If it comes out at more, a page has outgrown its sheet - shorten that
page rather than shrinking the type.
"""
import io
import os
import re
import sys
import base64

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBE = '--probe' in sys.argv
OUT = os.path.join(ROOT, 'company-profile-document.html')
if PROBE:
    OUT = os.path.join(os.environ.get('TEMP', ROOT), 'profile-probe.html')

ISSUE_DATE = '21 August 2026'
PAGE_H = 1123                 # A4 at 96dpi
BAND_W, BAND_H = 1250, 566    # hero band render size (shown at 794 x 360)


# --------------------------------------------------------------- image helpers
def data_uri(raw, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(raw).decode('ascii'))


def inline(rel):
    """Inline a repo image untouched."""
    with open(os.path.join(ROOT, rel.replace('/', os.sep)), 'rb') as fh:
        ext = os.path.splitext(rel)[1].lower()
        return data_uri(fh.read(), 'image/png' if ext == '.png' else 'image/jpeg')


def band(rel, w=BAND_W, h=BAND_H, quality=80):
    """Centre-crop a site photo to the hero band ratio and re-encode.

    The originals run 170-500 KB at up to 1815px wide; at the size they print
    here that is all waste, and eight of them inlined would make the file
    unusable as an email attachment.
    """
    im = Image.open(os.path.join(ROOT, rel.replace('/', os.sep))).convert('RGB')
    want = w / float(h)
    have = im.width / float(im.height)
    if have > want:                     # too wide - trim the sides
        new_w = int(round(im.height * want))
        left = (im.width - new_w) // 2
        im = im.crop((left, 0, left + new_w, im.height))
    else:                               # too tall - trim top and bottom
        new_h = int(round(im.width / want))
        top = (im.height - new_h) // 2
        im = im.crop((0, top, im.width, top + new_h))
    im = im.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return data_uri(buf.getvalue(), 'image/jpeg')


VISION = inline('assets/images/doc/vision-2030.png')
QR_SITE = inline('assets/images/doc/bav-website-qr.png')
QR_INSTA = inline('assets/images/instagram-qr.png')


# ------------------------------------------------------ scrape the service pages
def clean(s):
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = (s.replace('&amp;', '&').replace('&nbsp;', ' ')
          .replace('&mdash;', '—').replace('&ndash;', '–')
          .replace('&rsquo;', '’').replace('&quot;', '"'))
    s = re.sub(r'&[a-z#0-9]+;', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def scrape(slug):
    path = os.path.join(ROOT, 'services', slug, 'index.html')
    s = io.open(path, encoding='utf-8').read()

    # <p(?:\s[^>]*)?> (not <p[^>]*>) so this doesn't also swallow <picture>,
    # <path> or <polygon> tags as if they were <p> - any of those sitting
    # before the real paragraph corrupts the pairing with the next </p>.
    m = re.search(r'(?is)<h1[^>]*>.*?</h1>\s*<p(?:\s[^>]*)?>(.*?)</p>', s)
    tagline = clean(m.group(1)) if m else ''

    paras = [clean(x) for x in re.findall(r'(?is)<p(?:\s[^>]*)?>(.*?)</p>', s)]
    intro = [x for x in paras if len(x) > 180][:2]

    # Slice between item starts; the closing divs nest and defeat a lazy match.
    starts = [m.start() for m in
              re.finditer(r'(?is)<div class="[a-z0-9-]*breakdown__item"', s)]
    steps = []
    for blk in [s[a:b] for a, b in zip(starts, starts[1:] + [len(s)])]:
        h = re.search(r'(?is)<h3[^>]*>(.*?)</h3>', blk)
        p = re.search(r'(?is)<p[^>]*>(.*?)</p>', blk)
        if h:
            steps.append((clean(h.group(1)), clean(p.group(1)) if p else ''))

    m = re.search(r'(?is)<ul class="service-features"[^>]*>(.*?)</ul>', s)
    standards = ([clean(x) for x in re.findall(r'(?is)<li[^>]*>(.*?)</li>', m.group(1))]
                 if m else [])

    scenarios = [clean(x) for x in
                 re.findall(r'(?is)<div class="[a-z0-9-]*scenario"[^>]*>(.*?)</div>', s)]

    maint = []
    for blk in re.findall(r'(?is)<div class="svc-maint-card"[^>]*>(.*?)</div>', s):
        h = re.search(r'(?is)<h3[^>]*>(.*?)</h3>', blk)
        d = re.search(r'(?is)<p[^>]*>(.*?)</p>', blk)
        if h and d:
            maint.append((clean(h.group(1)), clean(d.group(1))))

    assert tagline, '%s: no tagline found' % slug
    assert intro, '%s: no intro prose found' % slug
    assert len(steps) >= 5, '%s: found %d process steps, expected 5+' % (slug, len(steps))
    assert len(standards) >= 3, '%s: found %d standards, expected 3+' % (slug, len(standards))
    return {'tagline': tagline, 'intro': intro, 'steps': steps,
            'standards': standards, 'scenarios': scenarios, 'maint': maint}


# slug, page title, eyebrow, image, label over the numbered block
SERVICES = [
    ('isolated-power-panels', 'Isolated Power Panels', 'Critical care power',
     'assets/images/services/isolated-power-panels.jpg',
     'From supply to long-term support'),
    ('ev-charging-solutions', 'EV Charging Solutions', 'Clean mobility',
     'assets/images/services/ev-solutions.jpg',
     'From site survey to network support'),
    ('ups-power-backup', 'UPS &amp; Power Backup', 'Power continuity',
     'assets/images/services/ups-solutions.jpg',
     'From load assessment to long-term support'),
    ('lighting-solutions', 'Lighting Solutions', 'Illumination',
     'assets/images/services/lighting-solutions.jpg',
     'From photometric design to relamping'),
    ('firefighting-systems', 'Firefighting Systems', 'Life safety',
     'assets/images/services/firefighting-solutions.jpg',
     'From risk assessment to periodic maintenance'),
    ('hvac-solutions', 'HVAC Solutions', 'Climate control',
     'assets/images/services/hvac-solutions.jpg',
     'From load calculation to ongoing maintenance'),
    ('electrical-distribution', 'Electrical &amp; Power Distribution', 'Power infrastructure',
     'assets/images/services/electrical-power.jpg',
     'From load study to corrective maintenance'),
    ('hospital-modular-or-rooms', 'Hospital Modular OR Rooms', 'Surgical infrastructure',
     'assets/images/services/hospital-modular-or-rooms.jpg',
     'From design to commissioning'),
    ('lead-sheets-hospital', 'Lead Sheets for Hospitals', 'Radiation shielding',
     'assets/images/services/lead-sheets-hospital.jpg',
     'From shielding survey to compliance verification'),
]

DATA = {slug: scrape(slug) for slug, _, _, _, _ in SERVICES}


# ------------------------------------------------------------------- components
ARROW = ('<svg class="mark" viewBox="0 0 40 40" aria-hidden="true">'
         '<polygon points="2,14 24,14 24,4 38,20 24,36 24,26 2,26" fill="currentColor"/></svg>')

PAGES = []          # (running-head section name, body html, dark cover?)


def add(section, body, dark=False):
    PAGES.append((section, body, dark))


def opener(eyebrow, title, standfirst=''):
    out = ['<div class="opener">',
           '<div class="eyebrow">' + eyebrow + '</div>',
           '<h2>' + title + '</h2>']
    if standfirst:
        out.append('<p class="standfirst">' + standfirst + '</p>')
    out.append('</div>')
    return ''.join(out)


def chips(items):
    return ('<div class="chips">' +
            ''.join('<span class="chip">%s</span>' % esc(i) for i in items) +
            '</div>')


SIDE_LABEL = {}


def service_page(slug, title, eyebrow, image, steps_label):
    d = DATA[slug]
    portrait = Image.open(os.path.join(ROOT, image.replace('/', os.sep))).width < 800

    if portrait:
        # The IPP asset is a 374x600 product shot on white. Cropped into a
        # full-bleed band it would lose the subject and be upscaled well past
        # its resolution, so it gets a product plate instead.
        hero = ('<div class="hero-plate">'
                '<div class="hero-plate__img"><img src="' + inline(image) + '" alt="' +
                esc(clean(title)) + '"></div>'
                '<div class="hero-plate__txt">'
                '<div class="eyebrow">' + eyebrow + '</div>'
                '<h2 class="svc-title">' + title + '</h2>'
                '<p class="tagline">' + esc(d['tagline']) + '</p>'
                + ''.join('<p class="lead">' + esc(x) + '</p>' for x in d['intro'][:2]) +
                '</div></div>')
    else:
        hero = ('<figure class="hero-band">'
                '<img src="' + band(image) + '" alt="' + esc(clean(title)) + '">'
                '<figcaption><div class="eyebrow light">' + eyebrow + '</div>'
                '<h2 class="svc-title">' + title + '</h2></figcaption></figure>'
                '<div class="pad"><p class="tagline">' + esc(d['tagline']) + '</p>'
                '<p class="lead">' + esc(d['intro'][0]) + '</p></div>')

    cols = ['<div class="pad"><div class="svc-cols">', '<div class="svc-col">',
            '<h3 class="rule-head">' + steps_label + '</h3>', '<ol class="steps">']
    for i, (t, desc) in enumerate(d['steps'][:6], 1):
        cols.append('<li><span class="n">%02d</span><div><b>%s</b>%s</div></li>'
                    % (i, esc(t), '<span>' + esc(desc) + '</span>' if desc else ''))
    cols.append('</ol></div>')

    cols.append('<div class="svc-col svc-col--side">')
    cols.append('<h3 class="rule-head">%s</h3>'
                % SIDE_LABEL.get(slug, 'Standards &amp; compliance'))
    cols.append('<ul class="ticks">' +
                ''.join('<li>%s</li>' % esc(x) for x in d['standards']) + '</ul>')
    if d['scenarios']:
        cols.append('<h3 class="rule-head">Where it is used</h3>')
        cols.append(chips(d['scenarios']))
    cols.append('</div></div>')

    # The IPP page carries a portrait plate rather than a 360px band and only
    # three standards, so it runs short. Its maintenance plans fill it out.
    if portrait and d['maint']:
        cols.append('<h3 class="rule-head">Maintenance plans</h3><div class="commits">')
        cols += ['<div class="commit"><b>%s</b><span>%s</span></div>' % (esc(t), esc(x))
                 for t, x in d['maint'][:4]]
        cols.append('</div>')
    cols.append('</div>')

    return hero + ''.join(cols)


# ------------------------------------------------------------------ page 1 cover
add('', (
    '<div class="cover">'
    '<div class="cover__top">'
    '<div class="cover__brand">' + ARROW +
    '<div><div class="cover__b1">BLACK <span>ARROW</span></div>'
    '<div class="cover__b2">Venture Company</div></div></div>'
    '<img class="cover__vision" src="' + VISION + '" alt="Vision 2030 - Kingdom of Saudi Arabia">'
    '</div>'
    '<div class="cover__mid">'
    '<div class="cover__kicker">Company Profile &middot; ' + ISSUE_DATE + '</div>'
    '<h1 class="cover__name">BLACK<br><span>ARROW</span><br>VENTURE</h1>'
    '<p class="cover__ar">&#1588;&#1585;&#1603;&#1577; &#1575;&#1604;&#1587;&#1607;&#1605; '
    '&#1575;&#1604;&#1571;&#1587;&#1608;&#1583; &#1700;&#1606;&#1578;&#1588;&#1585;</p>'
    '<p class="cover__line">Infrastructure that has to <em>keep working.</em></p>'
    '<p class="cover__sub">Isolated power, EV charging, UPS, lighting, firefighting, HVAC, '
    'electrical distribution, modular OR rooms and radiation shielding &mdash; supplied, '
    'installed, commissioned and maintained across the Kingdom of Saudi Arabia.</p>'
    '</div>'
    '<div class="cover__foot">'
    '<div><div class="cover__lbl">Established</div>'
    '<div class="cover__val">2022 &middot; Dammam</div></div>'
    '<div><div class="cover__lbl">Unified ID</div>'
    '<div class="cover__val">7054542985</div></div>'
    '<div><div class="cover__lbl">VAT</div>'
    '<div class="cover__val">314841084500003</div></div>'
    '<img class="cover__qr" src="' + QR_SITE + '" alt="QR code for www.blackarrowksa.com">'
    '</div>'
    '<div class="cover__band">WWW.BLACKARROWKSA.COM</div>'
    '</div>'), dark=True)


# --------------------------------------------------------------- page 2 contents
TOC = [
    (3, 'Who we are', 'The company, how it works, and the figures behind it'),
    (4, 'Vision &amp; mission', 'What we are building toward, and how Vision 2030 fits'),
    (5, 'Sectors we serve', 'Six sectors and what each one actually needs'),
    (6, 'Isolated power panels', 'NFPA 99 power for operating theatres and wet procedure locations'),
    (7, 'EV charging solutions', 'AC and DC charging, OCPP-managed across multiple sites'),
    (8, 'UPS &amp; power backup', '1 kVA to 1 MVA, sized against the load and the runtime'),
    (9, 'Lighting solutions', 'Fa&ccedil;ade, obstruction, helipad and DALI-controlled systems'),
    (10, 'Firefighting systems', 'Detection, suppression and evacuation integration'),
    (11, 'HVAC solutions', 'AHUs, VRF/VRV systems and BMS-integrated controls'),
    (12, 'Electrical &amp; power distribution', 'Switchgear, boards, control panels and testing'),
    (13, 'Hospital modular OR rooms', 'Cleanroom-grade operating theatres, design to commissioning'),
    (14, 'Lead sheets for hospitals', 'Radiation shielding for X-ray, CT and radiotherapy rooms'),
    (15, 'Project experience', 'Representative work, with the constraints that shaped it'),
    (16, 'Standards &amp; commitments', 'What we build to, and what happens after handover'),
    (17, 'Contact', 'Company records and who to call for what'),
]
add('Contents', '<div class="pad">' +
    opener('Company Profile', 'Contents') +
    '<ul class="toc">' +
    ''.join('<li><span class="n">%02d</span><span class="t">%s</span>'
            '<span class="d">%s</span></li>' % t for t in TOC) +
    '</ul></div>')


# ------------------------------------------------------------- page 3 who we are
add('Who we are', '<div class="pad">' +
    opener('01 &mdash; The company', 'Who we are',
           'Black Arrow Venture is a Saudi-based trading and solutions provider delivering '
           'infrastructure and technology solutions across the Kingdom.') +
    '<div class="two-col">'
    '<p>With a strategic focus on Electric Vehicle (EV) infrastructure, Uninterruptible '
    'Power Supply (UPS) systems, HVAC solutions and specialised engineering products, we '
    'provide complete, end-to-end services tailored to modern market demands. Our approach '
    'integrates supply, installation, testing &amp; commissioning, and long-term maintenance '
    '&mdash; ensuring reliability, efficiency and operational excellence on every project.</p>'
    '<p>We serve commercial, industrial, hospitality, healthcare and public infrastructure '
    'clients, delivering solutions that meet international standards while addressing local '
    'regulatory and operational requirements. Driven by innovation, quality and strong '
    'partnerships, we build resilient systems that empower businesses, enable clean mobility '
    'and support the future-ready infrastructure of Saudi Arabia.</p>'
    '</div>'
    '<div class="figures">' +
    ''.join('<div class="fig"><div class="n">%s</div><div class="l">%s</div></div>' % f for f in [
        ('2022', 'Established'), ('58', 'Projects completed'), ('33+', 'B2B clients served'),
        ('5', 'Ongoing projects'), ('9', 'Solution categories'), ('24/7', 'Technical support'),
    ]) + '</div>'
    '<h3 class="rule-head">How we work</h3>'
    '<div class="flow">'
    '<div class="flow__step"><span class="n">01</span><div><b>Supply</b>'
    '<span>Equipment sourced from established manufacturers and specified against the '
    'standards the project is held to, not on price alone.</span></div></div>'
    '<div class="flow__step"><span class="n">02</span><div><b>Installation</b>'
    '<span>Site survey, civil works coordination and installation by our own operations '
    'team, sequenced around live facilities where no shutdown window exists.</span></div></div>'
    '<div class="flow__step"><span class="n">03</span><div><b>Testing &amp; commissioning</b>'
    '<span>Functional testing, IR testing, power quality analysis and load testing, with '
    'documented handover to the client&rsquo;s engineering or biomedical team.</span></div></div>'
    '<div class="flow__step"><span class="n">04</span><div><b>Maintenance</b>'
    '<span>Preventive schedules and long-term support, including remote monitoring where '
    'the installed equipment allows it.</span></div></div>'
    '</div>'
    '<h3 class="rule-head">Why clients choose us</h3>'
    '<div class="commits">'
    '<div class="commit"><b>Innovation first</b><span>We integrate current technologies to '
    'deliver future-ready solutions rather than repeating a specification that already '
    'worked once.</span></div>'
    '<div class="commit"><b>Reliable performance</b><span>Every system we deliver is '
    'engineered for uptime and operational excellence.</span></div>'
    '<div class="commit"><b>Vision 2030 aligned</b><span>Our solutions actively contribute '
    'to Saudi Arabia&rsquo;s national transformation.</span></div>'
    '<div class="commit"><b>End-to-end service</b><span>Supply, installation, testing, '
    'commissioning and long-term maintenance from a single accountable party.</span></div>'
    '</div></div>')


# ----------------------------------------------------- page 4 vision and mission
add('Vision &amp; mission', '<div class="pad">' +
    opener('02 &mdash; Foundation', 'Vision &amp; mission') +
    '<div class="statement statement--gold">'
    '<div class="statement__lbl">Our vision</div>'
    '<p>To become a leading Saudi trading and solutions provider driving the Kingdom&rsquo;s '
    'transition toward sustainable energy, resilient infrastructure and smart technologies '
    '&mdash; in full alignment with Saudi Vision 2030.</p>'
    '<ul class="ticks"><li>Contribute to EV infrastructure growth across the Kingdom</li>'
    '<li>Support mission-critical sectors with reliable power solutions</li>'
    '<li>Enhance building efficiency through advanced HVAC and smart systems</li>'
    '<li>Deliver integrated solutions meeting international standards</li></ul></div>'
    '<div class="statement">'
    '<div class="statement__lbl">Our mission</div>'
    '<p>To deliver innovative, sustainable and reliable solutions that empower businesses, '
    'support critical infrastructure, and contribute to Saudi Arabia&rsquo;s vision for a '
    'technologically advanced and environmentally responsible future.</p>'
    '<ul class="ticks"><li>Supply, installation, testing and commissioning on every project</li>'
    '<li>Long-term maintenance ensuring ongoing reliability</li>'
    '<li>Partnerships built on trust, quality and innovation</li>'
    '<li>Full compliance with international and local standards</li></ul></div>'
    '<h3 class="rule-head">Where we meet Vision 2030</h3>'
    '<div class="tri">'
    '<div class="tri__c"><b>Sustainable energy</b><span>EV charging infrastructure and '
    'energy-efficient lighting and HVAC that cut consumption on existing building stock.</span></div>'
    '<div class="tri__c"><b>Smart infrastructure</b><span>OCPP-managed charging networks, '
    'BMS-integrated controls and monitored power systems that report their own condition.</span></div>'
    '<div class="tri__c"><b>Economic growth</b><span>Supply, installation and maintenance '
    'capability built inside the Kingdom, serving healthcare, government and industry.</span></div>'
    '</div></div>')


# ---------------------------------------------------------------- page 5 sectors
SECTORS = [
    ('Healthcare', 'Hospitals and clinics',
     'Isolated power for operating theatres, modular OR rooms, lead shielding for X-ray and '
     'CT suites, UPS on critical branches, HVAC and compliant electrical distribution '
     '&mdash; governed by NFPA 99 and reviewed at accreditation.'),
    ('Government &amp; public sector', 'Public infrastructure and municipalities',
     'Power continuity, lighting and life-safety systems for facilities that cannot be '
     'taken offline for convenience.'),
    ('Commercial', 'Offices, retail and mixed-use',
     'EV charging, fa&ccedil;ade lighting, HVAC and power distribution &mdash; usually '
     'inside an electrical capacity that was sized before any of it existed.'),
    ('Industrial', 'Factories, warehouses and plants',
     'Switchgear, control panels, power quality testing and firefighting systems built for '
     'continuous operation.'),
    ('Hospitality', 'Hotels and hospitality properties',
     'HVAC upgrades, guest-comfort controls, lighting and backup power, staged so the '
     'property keeps trading.'),
    ('Aviation', 'High-rise and aviation-adjacent',
     'Obstruction lighting, helipad lighting and airside products, monitored so a failed '
     'fixture is known about before an inspection finds it.'),
]
add('Sectors we serve', '<div class="pad">' +
    opener('03 &mdash; Market', 'Sectors we serve',
           'We tailor each solution to the compliance and operational reality of the sector '
           'it lands in.') +
    '<div class="sectors">' +
    ''.join('<div class="sector"><div class="sector__n">%02d</div>'
            '<div><b>%s</b><i>%s</i><span>%s</span></div></div>'
            % (i, n, sub, d) for i, (n, sub, d) in enumerate(SECTORS, 1)) +
    '</div></div>'
    '<div class="coverband"><div class="coverband__in">'
    '<div class="coverband__head">'
    '<div><div class="eyebrow amber">Coverage</div>'
    '<h3>Across the Kingdom</h3></div>'
    '<p>We supply, install and maintain nationwide from our base in Dammam, working '
    'across the Eastern, Central and Western regions.</p>'
    '</div>'
    '<div class="coverage">' +
    ''.join('<div class="cov"><b>%s</b><i>%s</i></div>' % c for c in [
        ('Dammam', 'Head office'), ('Al Khobar', 'Eastern Province'),
        ('Eastern Province', 'Province-wide'), ('Riyadh', 'Central Region'),
        ('Jeddah', 'Western Region'),
    ]) +
    '</div></div></div>')


# ------------------------------------------------------- pages 6-13 the services
for _slug, _title, _eyebrow, _image, _label in SERVICES:
    add(clean(_title), service_page(_slug, _title, _eyebrow, _image, _label))


# ---------------------------------------------------- page 14 project experience
PROJECTS = [
    ('Isolated power for a hospital operating theatre suite',
     'Healthcare &middot; Eastern Province',
     'A private hospital expanding its surgical capacity needed the new theatres to satisfy '
     'NFPA&nbsp;99 for wet procedure locations. Line isolation monitors in the adjoining wing '
     'had never been recalibrated, and accreditation would have assessed the suite as a whole.',
     'We surveyed the whole suite before quoting, installed isolated power panels with '
     'integrated monitors in the new theatres, and recalibrated and re-documented the '
     'existing ones &mdash; working between surgical lists rather than closing the suite.',
     'One documented maintenance schedule now covers every theatre in the suite.'),
    ('UPS replacement on a healthcare critical branch',
     'Healthcare &middot; Western Region',
     'UPS units were past end of life, batteries no longer held rated autonomy, and spare '
     'parts were becoming difficult to source.',
     'We replaced the units on the critical branch with no shutdown window, working around '
     'live clinical operations.',
     'Full rated autonomy restored on supported equipment, with clinical operations '
     'uninterrupted throughout.'),
    ('EV charging rollout across a commercial retail complex',
     'Commercial &middot; Central Region',
     'A mixed retail and office development wanted EV charging in its parking structure. '
     'Tenant demand drove it; the existing electrical infrastructure constrained it.',
     'We sized a mix of AC and DC charging to the supply already present, and laid the '
     'distribution out ahead of demand.',
     'Live within the existing supply, avoiding the substation upgrade the original brief '
     'implied, and expandable without repeating the civil works.'),
    ('Obstruction and helipad lighting for a high-rise',
     'Aviation &middot; Saudi Arabia',
     'A high-rise required aviation obstruction lighting to mark the structure, plus '
     'lighting for a rooftop helipad intended for emergency medical access.',
     'We supplied and installed the obstruction and helipad lighting with monitored, '
     'alarmed fixtures.',
     'The structure is marked to aviation requirements and the helipad is lit for night '
     'operations; failures are reported when they happen, not at inspection.'),
    ('HVAC upgrade for a hospitality property',
     'Hospitality &middot; Eastern Province',
     'An operating hotel had recurring complaints about inconsistent room temperatures '
     '&mdash; some floors ran cold, others could not hold setpoint through the afternoon peak.',
     'We upgraded floor by floor with BMS-integrated zone control, keeping the property '
     'open and trading.',
     'Setpoint holds across floors through the peak, with per-zone visibility through the '
     'BMS and only one floor of inventory out at a time.'),
]
add('Project experience', '<div class="pad">' +
    opener('04 &mdash; Evidence', 'Project experience',
           'Representative accounts of work we carry out. Client names and identifying '
           'details are withheld under the confidentiality terms agreed with each client.') +
    ''.join('<div class="proj"><div class="proj__h"><b>%s</b><i>%s</i></div>'
            '<div class="proj__g">'
            '<div><span class="k">Challenge</span><p>%s</p></div>'
            '<div><span class="k">What we did</span><p>%s</p></div>'
            '<div><span class="k">Outcome</span><p class="o">%s</p></div>'
            '</div></div>' % p for p in PROJECTS) +
    '<p class="fineprint">Scope descriptions are accurate, and we have deliberately not '
    'published performance figures we cannot evidence publicly.</p>'
    '</div>')


# ----------------------------------------------- page 15 standards & commitments
STANDARDS = [
    ('NFPA 99', 'Health Care Facilities Code &mdash; isolated power and line isolation '
                'monitoring for wet procedure locations.'),
    ('NFPA 70', 'National Electrical Code &mdash; healthcare and general electrical '
                'installation provisions.'),
    ('IEC 62040', 'Uninterruptible power systems &mdash; performance and safety requirements.'),
    ('IEC 61851', 'Conductive charging systems for electric vehicles.'),
    ('OCPP', 'Open Charge Point Protocol &mdash; vendor-neutral management of multi-site '
             'EV networks.'),
    ('SASO', 'Saudi Standards, Metrology and Quality Organization conformity for installed '
             'equipment.'),
    ('Saudi Building Code', 'Electrical, mechanical and fire-safety provisions.'),
    ('ASHRAE', 'HVAC design, ventilation and indoor air quality standards.'),
    ('DALI', 'Digital addressable lighting interface for controllable, monitored luminaires.'),
    ('ISO 14644', 'Cleanroom classification for modular operating room construction.'),
    ('NCRP / IAEA', 'Radiation shielding calculation and lead sheet installation for X-ray, '
                    'CT and radiotherapy rooms.'),
]
COMMITMENTS = [
    ('24/7 support', 'Round-the-clock assistance for operational needs on systems we have '
                     'supplied or maintain.'),
    ('45-minute response', 'Response within 45 minutes during business hours, Sunday to '
                           'Thursday, 8:00 AM to 6:00 PM.'),
    ('One business day', 'Every inquiry answered within one business day. WhatsApp '
                         'inquiries accepted 24/7.'),
    ('Warranty', 'Coverage as per factory and manufacturer terms, confirmed in writing on '
                 'each quotation.'),
]
add('Standards &amp; commitments', '<div class="pad">' +
    opener('05 &mdash; Assurance', 'Standards &amp; commitments',
           'The codes our work is built to, and what we hold ourselves to after handover.') +
    '<h3 class="rule-head">Codes and standards</h3>'
    '<div class="stds">' +
    ''.join('<div class="std"><b>%s</b><span>%s</span></div>' % s for s in STANDARDS) +
    '</div>'
    '<h3 class="rule-head">Service commitments</h3>'
    '<div class="commits">' +
    ''.join('<div class="commit"><b>%s</b><span>%s</span></div>' % c for c in COMMITMENTS) +
    '</div>'
    '<p class="fineprint">Commercial Registration, VAT registration and equipment conformity '
    'certificates are provided with any quotation, or on request to info@blackarrowksa.com.</p>'
    '</div>')


# ------------------------------------------------------------- page 16 back cover
add('', (
    '<div class="cover back">'
    '<div class="cover__top">'
    '<div class="cover__brand">' + ARROW +
    '<div><div class="cover__b1">BLACK <span>ARROW</span></div>'
    '<div class="cover__b2">Venture Company</div></div></div>'
    '<img class="cover__vision" src="' + VISION + '" alt="Vision 2030 - Kingdom of Saudi Arabia">'
    '</div>'
    '<div class="back__mid">'
    '<div class="cover__kicker">Contact</div>'
    '<h1 class="back__h">Tell us the constraints<br>you are working within.</h1>'
    '<div class="back__grid">'
    '<div><div class="cover__lbl">Telephone / WhatsApp</div>'
    '<div class="back__val num-ltr">+966 560 224 715</div></div>'
    '<div><div class="cover__lbl">Email</div>'
    '<div class="back__val">info@blackarrowksa.com</div></div>'
    '<div><div class="cover__lbl">Head office</div>'
    '<div class="back__val">Ad Dammam, Ash Sharqiyah 32245<br>Kingdom of Saudi Arabia</div></div>'
    '<div><div class="cover__lbl">Business hours</div>'
    '<div class="back__val">Sunday &ndash; Thursday, 8:00 AM &ndash; 6:00 PM<br>'
    'WhatsApp accepted 24/7</div></div>'
    '</div>'
    '<div class="back__what"><div class="cover__lbl">What we do</div>' +
    '<div class="chips">' +
    ''.join('<span class="chip chip--dark">%s</span>' % t for _s, t, _e, _i, _l in SERVICES) +
    '</div></div>'
    '<div class="back__qr">'
    '<figure><img src="' + QR_SITE + '" alt="QR code for www.blackarrowksa.com">'
    '<figcaption>blackarrowksa.com</figcaption></figure>'
    '<figure><img src="' + QR_INSTA + '" alt="QR code for instagram.com/blackarrowventure">'
    '<figcaption>@blackarrowventure</figcaption></figure>'
    '<div class="back__ids"><div>Unified ID <b>7054542985</b></div>'
    '<div>VAT <b>314841084500003</b></div>'
    '<div>Established <b>2022</b></div></div>'
    '</div>'
    '</div>'
    '<div class="cover__band">WWW.BLACKARROWKSA.COM</div>'
    '</div>'), dark=True)


# ------------------------------------------------------------------------ styles
CSS = """
:root{
  /* Carried over from the quotation. Nothing else is. */
  --ink:#15161c; --paper:#fdfcf8; --gold:#a87a24; --gold-deep:#8a641c;
  --rule:#e2dbc9; --muted:#6b6a63; --band:#f6f2e6;
  /* The website's accent, used only in the coverage band. */
  --amber:#F59E0B; --amber-dark:#D97706;
  --sans:"Segoe UI","Helvetica Neue",Arial,sans-serif;
  --serif:Georgia,"Times New Roman",serif;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:#c9c6bd;}
body{font-family:var(--sans);-webkit-font-smoothing:antialiased;color:var(--ink);}
@page{size:A4;margin:0;}
@media print{
  body{background:var(--paper);}
  .sheet{box-shadow:none !important;margin:0 auto !important;page-break-after:always;}
  .sheet:last-of-type{page-break-after:auto;}
}

/* A fixed sheet, not a min-height: an overlong page is then a visible clip
   rather than a silent reflow onto an extra sheet. --probe releases it. */
.sheet{position:relative;width:794px;height:PAGEHEIGHTpx;overflow:hidden;
  margin:22px auto;background:var(--paper);box-shadow:0 4px 24px rgba(0,0,0,.18);
  display:flex;flex-direction:column;}
.sheet--dark{background:var(--ink);color:var(--paper);}
.pad{padding:0 52px;}

/* ---- running head / foot ---- */
.rhead{display:flex;align-items:center;justify-content:space-between;
  margin:26px 52px 0;padding-bottom:9px;border-bottom:1px solid var(--rule);
  font-size:8px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;
  color:var(--muted);flex:none;}
.rhead .b{display:flex;align-items:center;gap:7px;color:var(--ink);}
.rhead .mark{width:13px;height:13px;color:var(--gold);flex:none;}
.rfoot{margin:auto 52px 24px;padding-top:9px;border-top:1px solid var(--rule);
  display:flex;align-items:baseline;justify-content:space-between;flex:none;
  font-size:8px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);}
.rfoot .pg{font-size:15px;font-weight:800;letter-spacing:0;color:var(--gold-deep);
  font-variant-numeric:tabular-nums;}

/* ---- section opener ---- */
.opener{margin:34px 0 24px;}
.eyebrow{font-size:9px;font-weight:800;letter-spacing:.24em;text-transform:uppercase;
  color:var(--gold-deep);margin-bottom:11px;}
.eyebrow.light{color:#e9d8ae;}
.opener h2{margin:0;font-size:42px;font-weight:700;letter-spacing:-.022em;line-height:1.06;
  text-wrap:balance;}
.standfirst{margin:14px 0 0;max-width:56ch;font-family:var(--serif);font-size:14px;
  line-height:1.62;color:#3b3c44;}
h3.rule-head{margin:26px 0 12px;font-size:9px;font-weight:800;letter-spacing:.2em;
  text-transform:uppercase;color:var(--gold-deep);padding-bottom:7px;
  border-bottom:1px solid var(--rule);}

/* ---- body copy ---- */
p{margin:0 0 10px;}
.two-col{columns:2;column-gap:34px;margin-bottom:6px;}
.two-col p{font-size:10px;line-height:1.8;margin:0 0 10px;break-inside:avoid;}

/* ---- figures ---- */
.figures{display:grid;grid-template-columns:repeat(6,1fr);margin:20px 0 4px;
  border-top:2px solid var(--ink);border-bottom:1px solid var(--rule);}
.fig{padding:14px 6px 13px;text-align:center;border-right:1px solid var(--rule);}
.fig:last-child{border-right:none;}
.fig .n{font-size:26px;font-weight:700;letter-spacing:-.02em;color:var(--gold-deep);
  line-height:1;font-variant-numeric:tabular-nums;}
.fig .l{margin-top:7px;font-size:7.5px;font-weight:800;letter-spacing:.11em;
  text-transform:uppercase;color:var(--muted);line-height:1.4;}

/* ---- numbered flow ---- */
.flow{display:grid;grid-template-columns:1fr 1fr;gap:16px 30px;}
.flow__step{display:grid;grid-template-columns:26px 1fr;gap:10px;align-items:start;}
.flow__step .n{font-size:14px;font-weight:800;color:var(--gold);
  font-variant-numeric:tabular-nums;padding-top:1px;}
.flow__step b{display:block;font-size:11px;font-weight:800;}
.flow__step div span{display:block;font-size:9px;line-height:1.65;color:#45464e;
  margin-top:3px;}

/* ---- contents ---- */
.toc{list-style:none;margin:0;padding:0;}
.toc li{display:grid;grid-template-columns:46px 232px 1fr;align-items:baseline;gap:12px;
  padding:11px 0;border-bottom:1px solid var(--rule);}
.toc .n{font-size:13px;font-weight:800;color:var(--gold);font-variant-numeric:tabular-nums;}
.toc .t{font-size:13px;font-weight:700;letter-spacing:-.01em;}
.toc .d{font-size:9.5px;line-height:1.5;color:var(--muted);}

/* ---- statements ---- */
.statement{border-top:2px solid var(--ink);padding:15px 0 17px;margin-bottom:4px;}
.statement--gold{border-top-color:var(--gold);}
.statement__lbl{font-size:9px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gold-deep);margin-bottom:9px;}
.statement p{font-family:var(--serif);font-size:14.5px;line-height:1.6;margin:0 0 11px;
  max-width:64ch;}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}
.tri__c b{display:block;font-size:11px;font-weight:800;margin-bottom:5px;}
.tri__c span{display:block;font-size:9.5px;line-height:1.65;color:#45464e;}

/* ---- tick lists ---- */
.ticks{list-style:none;margin:0;padding:0;}
.ticks li{position:relative;padding-left:16px;font-size:9.5px;line-height:1.6;
  margin-bottom:6px;color:#3b3c44;}
.ticks li:before{content:"";position:absolute;left:0;top:6px;width:6px;height:6px;
  background:var(--gold);}

/* ---- sectors ---- */
.sectors{display:grid;grid-template-columns:1fr 1fr;gap:40px 30px;}
.sector{display:grid;grid-template-columns:34px 1fr;gap:10px;padding-top:16px;
  border-top:1px solid var(--rule);}
.sector__n{font-size:14px;font-weight:700;color:var(--gold);font-variant-numeric:tabular-nums;}
.sector b{display:block;font-size:14.5px;font-weight:800;letter-spacing:-.01em;}
.sector i{display:block;font-style:normal;font-size:8.5px;font-weight:800;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);margin:3px 0 6px;}
.sector span{display:block;font-size:10.5px;line-height:1.75;color:#45464e;}
.coverband{width:794px;margin-top:auto;background:var(--ink);color:var(--paper);
  border-top:3px solid var(--amber);}
.coverband + .rfoot{margin-top:0;}
.coverband__in{padding:48px 52px 52px;}
.coverband__head{display:flex;align-items:flex-end;justify-content:space-between;gap:40px;
  padding-bottom:26px;margin-bottom:30px;border-bottom:1px solid #303138;}
.eyebrow.amber{color:var(--amber);margin-bottom:8px;}
.coverband__head h3{margin:0;font-size:34px;font-weight:700;letter-spacing:-.022em;
  line-height:1.1;color:var(--paper);}
.coverband__head p{margin:0;max-width:44ch;font-family:var(--serif);font-size:11.5px;
  line-height:1.72;color:#b6b3ab;}
.coverage{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;}
.cov{border-top:2px solid var(--amber);padding-top:16px;}
.cov b{display:block;font-size:16px;font-weight:800;letter-spacing:-.012em;
  color:var(--paper);line-height:1.15;min-height:2.3em;}
.cov i{display:block;font-style:normal;font-size:8.5px;font-weight:800;letter-spacing:.12em;
  text-transform:uppercase;color:var(--amber-dark);margin-top:8px;}

/* ---- service pages ---- */
.hero-band{position:relative;margin:0;width:794px;height:360px;overflow:hidden;flex:none;}
.hero-band img{width:100%;height:100%;object-fit:cover;display:block;}
.hero-band figcaption{position:absolute;inset:auto 0 0 0;padding:88px 52px 26px;
  background:linear-gradient(to top,rgba(21,22,28,.93) 12%,rgba(21,22,28,.58) 52%,
    rgba(21,22,28,0));}
.svc-title{margin:0;font-size:36px;font-weight:700;letter-spacing:-.024em;line-height:1.08;
  color:#fff;text-wrap:balance;}
.hero-plate{display:grid;grid-template-columns:212px 1fr;gap:30px;align-items:start;
  padding:30px 52px 0;}
.hero-plate__img{background:var(--band);border:1px solid var(--rule);padding:16px;
  display:flex;align-items:center;justify-content:center;height:352px;}
.hero-plate__img img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;}
.hero-plate .svc-title{color:var(--ink);font-size:31px;margin-bottom:2px;}
.tagline{margin:22px 0 0;font-size:12.5px;font-weight:700;color:var(--gold-deep);
  letter-spacing:-.005em;max-width:62ch;}
.hero-plate .tagline{margin-top:12px;}
.lead{margin:10px 0 0;font-family:var(--serif);font-size:12px;line-height:1.68;
  color:#3b3c44;max-width:74ch;}
.svc-cols{display:grid;grid-template-columns:1.32fr 1fr;gap:34px;margin-top:4px;}
.steps{list-style:none;margin:0;padding:0;}
.steps li{display:grid;grid-template-columns:26px 1fr;gap:10px;padding:9px 0;
  border-bottom:1px solid var(--rule);}
.steps li:last-child{border-bottom:none;}
.steps .n{font-size:11px;font-weight:800;color:var(--gold);font-variant-numeric:tabular-nums;
  padding-top:1px;}
.steps b{display:block;font-size:10.5px;font-weight:800;}
.steps span{display:block;font-size:9px;line-height:1.6;color:#4c4d55;margin-top:3px;}
.svc-col--side .ticks li{font-size:9px;}
.chips{display:flex;flex-wrap:wrap;gap:6px;}
.chip{border:1px solid var(--rule);background:var(--band);color:var(--gold-deep);
  font-size:8.5px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;padding:5px 9px;}

/* ---- projects ---- */
.proj{padding:13px 0;border-top:1px solid var(--rule);}
.proj:first-of-type{border-top:2px solid var(--ink);}
.proj__h{display:flex;align-items:baseline;justify-content:space-between;gap:16px;
  margin-bottom:8px;}
.proj__h b{font-size:12.5px;font-weight:800;letter-spacing:-.012em;}
.proj__h i{flex:none;font-style:normal;font-size:8px;font-weight:800;letter-spacing:.11em;
  text-transform:uppercase;color:var(--gold-deep);}
.proj__g{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;}
.proj__g .k{display:block;font-size:7.5px;font-weight:800;letter-spacing:.14em;
  text-transform:uppercase;color:var(--muted);margin-bottom:4px;}
.proj__g p{font-size:8.8px;line-height:1.6;margin:0;color:#45464e;}
.proj__g p.o{color:var(--ink);font-weight:600;}
.fineprint{margin-top:16px;font-size:8.5px;line-height:1.6;color:var(--muted);}

/* ---- standards ---- */
.stds{display:grid;grid-template-columns:1fr 1fr;gap:11px 30px;}
.std b{display:block;font-size:10.5px;font-weight:800;color:var(--ink);}
.std span{display:block;font-size:9px;line-height:1.6;color:#4c4d55;margin-top:2px;}
.commits{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;}
.commit b{display:block;font-size:11px;font-weight:800;color:var(--gold-deep);margin-bottom:5px;}
.commit span{display:block;font-size:9px;line-height:1.62;color:#45464e;}

/* ---- cover / back cover ---- */
.cover{display:flex;flex-direction:column;height:100%;}
.cover__top{display:flex;align-items:center;justify-content:space-between;padding:40px 52px 0;}
.cover__brand{display:flex;align-items:center;gap:12px;color:var(--gold);}
.cover__brand .mark{width:34px;height:34px;flex:none;}
.cover__b1{font-size:19px;font-weight:900;letter-spacing:.01em;color:var(--paper);}
.cover__b1 span{color:var(--gold);}
.cover__b2{font-size:8.5px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;
  color:#9a978f;margin-top:3px;}
.cover__vision{height:58px;width:auto;background:#fff;padding:5px 7px;border-radius:2px;}
.cover__mid{padding:0 52px;margin-top:56px;}
.cover__kicker{font-size:9px;font-weight:800;letter-spacing:.26em;text-transform:uppercase;
  color:var(--gold);margin-bottom:26px;}
.cover h1{margin:0;color:var(--paper);}
.cover h1.cover__name{font-size:104px;font-weight:800;line-height:.94;letter-spacing:-.038em;}
.cover h1.cover__name span{color:var(--gold);}
.cover__line{margin:30px 0 0;font-size:27px;font-weight:700;line-height:1.25;
  letter-spacing:-.016em;color:#d8d5cd;max-width:22ch;}
.cover__line em{font-style:normal;color:var(--gold);}
.cover__ar{margin:20px 0 0;font-size:21px;font-weight:700;color:#c8a24e;
  direction:rtl;unicode-bidi:isolate;text-align:left;}
.cover__sub{margin:22px 0 0;max-width:52ch;font-family:var(--serif);font-size:12.5px;
  line-height:1.72;color:#b6b3ab;}
.cover__foot{margin-top:auto;display:flex;align-items:flex-end;gap:40px;padding:0 52px 26px;}
.cover__lbl{font-size:7.5px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;
  color:#8d8a82;margin-bottom:6px;}
.cover__val{font-size:12px;font-weight:700;color:var(--paper);font-variant-numeric:tabular-nums;}
.cover__qr{margin-left:auto;width:92px;height:92px;background:#fff;padding:5px;}
.cover__band{background:var(--gold);color:#fff;text-align:center;padding:12px 0;
  font-size:10.5px;font-weight:800;letter-spacing:.2em;}
.back__mid{padding:0 52px;margin-top:64px;flex:1;display:flex;flex-direction:column;}
.cover h1.back__h{margin:0 0 54px;font-size:42px;font-weight:700;line-height:1.14;
  letter-spacing:-.024em;color:var(--paper);}
.back__grid{display:grid;grid-template-columns:1fr 1fr;gap:34px 40px;padding-bottom:34px;
  border-bottom:1px solid #33343c;}
.back__val{font-size:15px;font-weight:600;line-height:1.6;color:var(--paper);}
.back__qr{display:flex;align-items:flex-end;gap:22px;margin-top:44px;}
.back__what{margin-top:34px;}
.back__what .chips{margin-top:9px;}
.chip--dark{border-color:#3a3b44;background:transparent;color:#c8a24e;
  font-size:9.5px;padding:7px 12px;}
.back__qr figure{margin:0;text-align:center;}
.back__qr img{width:94px;height:94px;background:#fff;padding:5px;display:block;}
.back__qr figcaption{margin-top:6px;font-size:7.5px;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;color:#8d8a82;}
.back__ids{margin-left:auto;text-align:right;font-size:9.5px;line-height:1.9;color:#8d8a82;}
.back__ids b{color:var(--paper);font-variant-numeric:tabular-nums;}

/* Phone numbers keep their group order whatever surrounds them. */
.num-ltr{direction:ltr;unicode-bidi:isolate;}
"""
CSS = CSS.replace('PAGEHEIGHT', str(PAGE_H))
if PROBE:
    # Release the clip so an overlong page spills onto an extra printed sheet
    # and the page count tells on it.
    CSS += ('\n.sheet{height:auto !important;min-height:%dpx;overflow:visible !important;}\n'
            % PAGE_H)


# ---------------------------------------------------------------------- assemble
def render(i, section, body, dark):
    n = i + 1
    cls = 'sheet sheet--dark' if dark else 'sheet'
    if dark:
        return '\n<!-- page %d -->\n<div class="%s">\n%s\n</div>\n' % (n, cls, body)
    head = ('<div class="rhead"><span class="b">' + ARROW +
            'Black Arrow Venture</span><span>' + section + '</span></div>\n')
    foot = ('<div class="rfoot"><span>blackarrowksa.com</span>'
            '<span class="pg">%02d</span></div>\n' % n)
    return '\n<!-- page %d -->\n<div class="%s">\n%s%s%s</div>\n' % (n, cls, head, body, foot)


html = (
    '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="robots" content="noindex, nofollow">\n'
    '<meta name="description" content="Black Arrow Venture company profile - isolated power '
    'panels, EV charging, UPS, lighting, firefighting, HVAC, electrical distribution, '
    'modular OR rooms and radiation shielding across Saudi Arabia.">\n'
    '<title>Company Profile &mdash; Black Arrow Venture</title>\n'
    '<style>' + CSS + '</style></head>\n<body>\n' +
    ''.join(render(i, s, b, d) for i, (s, b, d) in enumerate(PAGES)) +
    '\n</body></html>\n'
)

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(html)

print('wrote %s' % OUT)
print('  %d pages, %.1f KB%s' % (len(PAGES), len(html.encode('utf-8')) / 1024.0,
                                 '  (height probe)' if PROBE else ''))
