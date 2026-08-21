# -*- coding: utf-8 -*-
"""Build company-profile-document.html — the print/PDF company profile.

This is NOT company-profile.html. That one is a web page on the site, with a
generated Arabic twin and its own pre-rebrand palette (see scripts/pages.json).
This one is an A4 document you send to a client or print to PDF, and it wears
the same letterhead as the quotations that go out of the same office:

    Quotation_Q2026756_Rev01.html  ->  ink/paper/gold tokens, letterhead with
    Unified ID + VAT centred and the Vision 2030 badge right, gold banner,
    band rows, spec tables, contact line over the gold arrow band.

Every fact in here comes from the live site (index / about / services /
contact / case studies / contacts). Nothing is invented. Where the site
contradicts itself the more conservative figure is used and noted in the
handover, not silently averaged.

Images are inlined as data URIs so the file can be emailed as one file and
prints identically anywhere.

    py scripts/build_profile_doc.py

To produce the PDF that actually goes to clients, print the result to A4 with
background graphics on. From the command line:

    chrome --headless=new --no-pdf-header-footer --print-to-pdf="<out>.pdf" \n           --virtual-time-budget=8000 "file:///<abs path>/company-profile-document.html"

It must come out at exactly 10 A4 pages. If it comes out at 11, a page has
grown past the 1040px content box and is pushing its slim footer onto a sheet
of its own - shorten that page rather than shrinking the type.
"""
import io
import os
import base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'company-profile-document.html')
TOTAL_PAGES = 10
ISSUE_DATE = '21 August 2026'


def img(rel):
    """Inline a repo image as a data URI."""
    path = os.path.join(ROOT, rel.replace('/', os.sep))
    ext = os.path.splitext(rel)[1].lower()
    mime = 'image/png' if ext == '.png' else 'image/jpeg'
    with open(path, 'rb') as fh:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(fh.read()).decode('ascii'))


VISION = img('assets/images/doc/vision-2030.png')
QR_SITE = img('assets/images/doc/bav-website-qr.png')
QR_INSTA = img('assets/images/instagram-qr.png')

# (logo file, client name) — names as published in the alt text on the home page.
CLIENTS = [
    ('assets/images/clients/dallah-hospital.jpg', 'Dallah Hospital'),
    ('assets/images/clients/client_2.jpg', 'Dr Sulaiman Al Habib Medical Group'),
    ('assets/images/clients/aldara-hospital.jpg', 'Aldara Hospital'),
    ('assets/images/clients/breeze-med-care.jpg', 'Breeze Med Care'),
    ('assets/images/clients/aramco-services.png', 'Aramco Services Company'),
    ('assets/images/clients/client_0.jpg', 'Zahran Facilities Management'),
    ('assets/images/clients/client_4.jpg', 'I-TAC Industrial Trading and Contracting Group'),
    ('assets/images/clients/client_3.jpg', "Insha'at Contracting Co."),
    ('assets/images/clients/client_5.jpg', 'USG ME'),
    ('assets/images/clients/nls-logo.png', 'NLS'),
    ('assets/images/clients/client_1.jpg', 'THC'),
    ('assets/images/clients/safari.jpg', 'Safari'),
]

ARROW_SVG = ('<svg viewBox="0 0 40 40" aria-hidden="true">'
             '<polygon points="2,14 24,14 24,4 38,20 24,36 24,26 2,26" fill="var(--gold)"/></svg>')


def letterhead():
    return (
        '<header class="letterhead">\n'
        '  <div class="brand"><span class="brand-mark">' + ARROW_SVG + '</span>'
        '<div class="brand-word"><div class="b1">BLACK <span class="accent">ARROW</span></div>'
        '<div class="b2">Venture Company</div></div></div>\n'
        '  <div class="brand-center"><div class="ids">'
        '<span class="idline">UNIFIED ID: <b>7054542985</b></span>'
        '<span class="idline">VAT: <b>314841084500003</b></span></div></div>\n'
        '  <div class="vision-badge"><img class="vision-logo" src="' + VISION +
        '" alt="Vision 2030 - Kingdom of Saudi Arabia"></div>\n'
        '</header>\n')


def banner(title, sub):
    return ('<div class="banner"><h1>' + title + '</h1>'
            '<div class="sub">' + sub + '</div></div>\n')


def footer(page_no):
    return (
        '<div class="full-footer">\n'
        '  <div class="contact-line"><span>info@blackarrowksa.com</span>'
        '<span>+966 560 224 715</span></div>\n'
        '  <div class="arrow-band">WWW.BLACKARROWKSA.COM</div>\n'
        '</div>\n'
        '<div class="slim-footer"><span>Black Arrow Venture &mdash; Company Profile ' +
        ISSUE_DATE + '</span><span>Page ' + str(page_no) + ' of ' + str(TOTAL_PAGES) +
        '</span></div>\n')


def page(page_no, body):
    return ('\n<!-- ============ PAGE %d ============ -->\n' % page_no +
            '<div class="paper"><div class="paper-inner">\n' +
            letterhead() + body + footer(page_no) +
            '</div></div>\n')


def service(name, tag, desc, bullets):
    out = ['<div class="svc"><div class="top"><h4>' + name + '</h4>'
           '<span class="tag">' + tag + '</span></div>',
           '<p>' + desc + '</p><ul>']
    out += ['<li>' + b + '</li>' for b in bullets]
    out.append('</ul></div>')
    return ''.join(out) + '\n'


def figures(items):
    cells = ''.join('<div class="fig"><div class="n">%s</div><div class="l">%s</div></div>'
                    % (n, l) for n, l in items)
    return '<div class="figures">' + cells + '</div>\n'


def spec(rows):
    body = ''.join('<tr><td class="k">%s</td><td class="v">%s</td></tr>' % (k, v) for k, v in rows)
    return '<table class="spec">' + body + '</table>\n'


def sec(title):
    return '<h3 class="sec">' + title + '</h3>\n'


CSS = """
:root{--ink:#15161c;--paper:#fdfcf8;--gold:#a87a24;--gold-deep:#8a641c;--rule:#e2dbc9;--muted:#6b6a63;--band:#f6f2e6;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:#c9c6bd;}
body{font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased;color:var(--ink);}
@page{size:A4;margin:0;}
@media print{
  body{background:var(--paper);}
  .paper{box-shadow:none !important;margin:0 auto !important;page-break-after:always;}
  .paper:last-of-type{page-break-after:auto;}
}
.paper{width:794px;margin:22px auto;background:var(--paper);box-shadow:0 4px 24px rgba(0,0,0,.18);}
.paper-inner{padding:28px 40px 16px;min-height:1040px;display:flex;flex-direction:column;}

/* ---- Letterhead: BAV wordmark | centred IDs | Vision 2030 ---- */
.letterhead{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-bottom:14px;border-bottom:2px solid var(--ink);break-inside:avoid;page-break-inside:avoid;}
.brand{flex:none;display:flex;align-items:center;gap:10px;}
.brand-mark{flex:none;width:32px;height:32px;}
.brand-mark svg{width:100%;height:100%;display:block;}
.brand-word .b1{font-weight:900;font-size:18px;letter-spacing:.01em;color:var(--ink);}
.brand-word .b1 .accent{color:var(--gold);}
.brand-word .b2{font-size:9px;font-weight:700;letter-spacing:.22em;color:var(--muted);margin-top:2px;text-transform:uppercase;}
.brand-center{flex:1;text-align:center;line-height:1.5;}
.brand-center .ids{font-size:14px;color:var(--muted);font-variant-numeric:tabular-nums;letter-spacing:.02em;}
.brand-center .ids .idline{display:block;}
.brand-center .ids b{color:var(--ink);}
.vision-badge{flex:none;display:flex;align-items:center;}
.vision-logo{height:66px;width:auto;display:block;}

/* ---- Banner ---- */
.banner{background:var(--gold);color:#fff;text-align:center;padding:18px 10px;margin:18px 0 15px;border-radius:2px;break-inside:avoid;page-break-inside:avoid;}
.banner h1{margin:0;font-size:27px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;text-wrap:balance;}
.banner .sub{margin-top:5px;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#fff;opacity:.92;}

/* ---- Cover name block ---- */
.project-box{border:2px solid var(--ink);padding:20px 16px;text-align:center;margin:0 0 14px;break-inside:avoid;page-break-inside:avoid;}
.project-box .name{font-size:23px;font-weight:800;line-height:1.35;color:var(--ink);}
.project-box .name-ar{margin-top:7px;font-size:19px;font-weight:700;color:var(--gold-deep);direction:rtl;unicode-bidi:isolate;font-family:"Segoe UI","Tahoma",Arial,sans-serif;}
.band-row{background:var(--band);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:10px 12px;font-size:11px;font-weight:700;color:var(--gold-deep);margin-bottom:14px;text-align:center;break-inside:avoid;page-break-inside:avoid;}

.meta3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin:0 0 16px;}
.meta3 .box{border:1px solid var(--rule);padding:11px 12px;break-inside:avoid;page-break-inside:avoid;}
.meta3 .box .label{font-size:8.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:4px;display:block;}
.meta3 .box .value{font-size:11px;line-height:1.4;color:var(--ink);}

h3.sec{margin:16px 0 7px;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-deep);border-bottom:1px solid var(--rule);padding-bottom:4px;break-after:avoid;page-break-after:avoid;}

table.spec{width:100%;border-collapse:collapse;font-size:9.5px;margin-bottom:4px;}
table.spec tr{break-inside:avoid;page-break-inside:avoid;}
table.spec td{padding:5px 8px;border:1px solid var(--rule);}
table.spec td.k{width:26%;font-weight:700;background:var(--band);}
table.spec td.v{overflow-wrap:anywhere;}

table.grid{width:100%;border-collapse:collapse;font-size:9.5px;margin-bottom:4px;table-layout:fixed;}
table.grid thead th{text-align:left;font-size:8px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:var(--ink);padding:6px 8px;border-right:1px solid rgba(255,255,255,.28);}
table.grid thead th:last-child{border-right:none;}
table.grid tbody tr{break-inside:avoid;page-break-inside:avoid;}
table.grid tbody td{padding:6px 8px;border-bottom:1px solid var(--rule);border-right:1px solid var(--rule);vertical-align:top;line-height:1.55;overflow-wrap:anywhere;}
table.grid tbody td:last-child{border-right:none;}
table.grid tbody tr:nth-child(even){background:var(--band);}
table.grid td.k{font-weight:700;}
table.grid td.num{font-variant-numeric:tabular-nums;white-space:nowrap;}

/* ---- Prose ---- */
.prose p{font-size:10.5px;line-height:1.78;margin:0 0 9px;}
.prose p.lead{font-size:12px;line-height:1.7;font-weight:600;color:var(--ink);}
.prose p:last-child{margin-bottom:0;}

/* ---- Key figures ---- */
.figures{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:8px 0 4px;}
.fig{border:1px solid var(--rule);padding:12px 8px;text-align:center;break-inside:avoid;page-break-inside:avoid;}
.fig .n{font-size:25px;font-weight:800;color:var(--gold-deep);line-height:1;font-variant-numeric:tabular-nums;}
.fig .l{margin-top:6px;font-size:8.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);line-height:1.4;}

/* ---- Vision / mission ---- */
.vm{border:1px solid var(--rule);padding:14px 16px;margin-bottom:12px;break-inside:avoid;page-break-inside:avoid;}
.vm.gold{border:2px solid var(--gold-deep);background:var(--band);}
.vm h4{margin:0 0 7px;font-size:12px;font-weight:800;color:var(--gold-deep);letter-spacing:.09em;text-transform:uppercase;}
.vm p{margin:0;font-size:10.5px;line-height:1.7;}
.vm ul{margin:9px 0 0;padding-inline-start:17px;}
.vm li{font-size:9.5px;line-height:1.6;margin-bottom:3px;}

/* ---- Service blocks ---- */
.svc{border:1px solid var(--rule);border-inline-start:3px solid var(--gold);padding:11px 13px;margin-bottom:9px;break-inside:avoid;page-break-inside:avoid;}
.svc .top{display:flex;align-items:baseline;justify-content:space-between;gap:12px;}
.svc h4{margin:0;font-size:12.5px;font-weight:800;color:var(--ink);}
.svc .tag{flex:none;font-size:8px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--gold-deep);}
.svc p{margin:5px 0 0;font-size:9.5px;line-height:1.6;}
.svc ul{margin:6px 0 0;padding-inline-start:16px;}
.svc li{font-size:9.5px;line-height:1.55;margin-bottom:2px;}

/* ---- Contents ---- */
table.toc{width:100%;border-collapse:collapse;}
table.toc td{padding:8px 8px;border-bottom:1px solid var(--rule);vertical-align:baseline;}
table.toc td.p{width:52px;text-align:center;font-size:12px;font-weight:800;color:var(--gold-deep);font-variant-numeric:tabular-nums;}
table.toc td.t{font-size:11.5px;font-weight:700;width:38%;}
table.toc td.d{font-size:9.5px;color:var(--muted);line-height:1.5;}

/* ---- Sector chips ---- */
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:9px 0 3px;}
.chip{border:1px solid var(--gold);background:#fbf6e9;color:var(--gold-deep);font-size:9px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:5px 11px;}

/* ---- Client logos ---- */
.logo-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:9px;}
.logo-cell{border:1px solid var(--rule);background:#fff;height:76px;display:flex;align-items:center;justify-content:center;padding:9px 12px;break-inside:avoid;page-break-inside:avoid;}
.logo-cell img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;}

/* ---- Projects ---- */
.proj{border:1px solid var(--rule);padding:10px 12px;margin-bottom:8px;break-inside:avoid;page-break-inside:avoid;}
.proj .h{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:4px;}
.proj .h .n{font-size:11.5px;font-weight:800;}
.proj .h .m{flex:none;font-size:8.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--gold-deep);}
.proj p{margin:0;font-size:9.5px;line-height:1.6;}
.proj p + p{margin-top:4px;}
.proj .out b{color:var(--gold-deep);}

.note{margin-top:10px;padding:9px 11px;border:1px dashed var(--gold);border-radius:5px;background:#fbf6e9;font-size:9px;line-height:1.6;color:#5c4a1e;}
.note b{color:var(--gold-deep);}

/* ---- QR blocks ---- */
.qr-block{margin-top:22px;text-align:center;break-inside:avoid;page-break-inside:avoid;}
.qr-block img{width:136px;height:136px;display:block;margin:0 auto;border:1px solid var(--rule);padding:6px;background:#fff;}
.qr-block .cap{margin-top:6px;font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--gold-deep);}
.qr-pair{display:flex;justify-content:center;gap:44px;margin-top:10px;break-inside:avoid;page-break-inside:avoid;}
.qr-pair .qr-block{margin-top:0;}
.qr-pair .qr-block img{width:92px;height:92px;}

/* Phone numbers keep their group order whatever the surrounding text does. */
.num-ltr{direction:ltr;unicode-bidi:isolate;}

/* ---- Footers ---- */
.full-footer{margin-top:auto;padding-top:16px;}
.full-footer .contact-line{display:flex;align-items:center;justify-content:space-between;font-size:13px;font-weight:800;color:var(--ink);padding:12px 0;border-top:1px solid var(--rule);}
.arrow-band{background:var(--gold);color:#fff;text-align:center;padding:10px 0;font-size:11px;font-weight:800;letter-spacing:.14em;}
.slim-footer{display:flex;align-items:center;justify-content:space-between;padding:6px 0 0;font-size:8.5px;color:var(--muted);}
"""

# ---------------------------------------------------------------- page 1: cover
p1 = (
    banner('Company Profile', 'Infrastructure &middot; Power &middot; Clean Mobility') +
    '<div class="project-box">'
    '<div class="name">Black Arrow Venture Company</div>'
    '<div class="name-ar">&#1588;&#1585;&#1603;&#1577; &#1575;&#1604;&#1587;&#1607;&#1605; '
    '&#1575;&#1604;&#1571;&#1587;&#1608;&#1583; &#1700;&#1606;&#1578;&#1588;&#1585;</div>'
    '</div>\n'
    '<div class="band-row">A Saudi trading and solutions provider &mdash; EV infrastructure, '
    'UPS and critical power, isolated power panels, HVAC, lighting, '
    'firefighting and electrical distribution</div>\n' +
    '<div class="meta3">'
    '<div class="box"><span class="label">Established</span><div class="value">2022 &middot; Dammam, KSA</div></div>'
    '<div class="box"><span class="label">Unified ID / CR</span><div class="value">7054542985</div></div>'
    '<div class="box"><span class="label">Issued</span><div class="value">' + ISSUE_DATE + ' &middot; Rev. 01</div></div>'
    '</div>\n' +
    sec('Head Office &amp; Contact') +
    spec([
        ('Head Office', 'Ad Dammam, Ash Sharqiyah 32245, Kingdom of Saudi Arabia'),
        ('Telephone / WhatsApp', '<span class="num-ltr">+966 560 224 715</span>'),
        ('Email', 'info@blackarrowksa.com'),
        ('Website', 'www.blackarrowksa.com'),
        ('Business Hours', 'Sunday &ndash; Thursday, 8:00 AM &ndash; 6:00 PM '
                           '(WhatsApp inquiries accepted 24/7)'),
    ]) +
    '<div class="qr-block"><img src="' + QR_SITE + '" alt="QR code for www.blackarrowksa.com">'
    '<div class="cap">Black Arrow Venture &mdash; www.blackarrowksa.com</div></div>\n'
)

# ------------------------------------------------------ page 2: contents + snapshot
TOC = [
    (3, 'Who We Are', 'Company overview, delivery model and the figures behind it'),
    (4, 'Vision, Mission &amp; Goals', 'What we are building toward and how Vision 2030 fits'),
    (5, 'Solutions Portfolio &mdash; I', 'Isolated power panels, EV charging, UPS and lighting'),
    (6, 'Solutions Portfolio &mdash; II', 'Firefighting, HVAC, electrical distribution and general trading'),
    (7, 'Sectors &amp; Clients', 'The sectors we work in and the organisations we have served'),
    (8, 'Project Experience', 'Representative work across healthcare, commercial and aviation'),
    (9, 'Standards &amp; Commitments', 'The codes we build to and what we commit to after handover'),
    (10, 'Registration &amp; Contacts', 'Company records and who to call for what'),
]
p2 = (
    banner('Contents', 'What is in this profile') +
    '<table class="toc">' +
    ''.join('<tr><td class="p">%02d</td><td class="t">%s</td><td class="d">%s</td></tr>'
            % (n, t, d) for n, t, d in TOC) +
    '</table>\n' +
    sec('Company Snapshot') +
    spec([
        ('Legal Name', 'Black Arrow Venture Company'),
        ('Entity Type', 'Limited Liability Company (LLC)'),
        ('Unified ID / Commercial Registration', '7054542985'),
        ('VAT Registration', '314841084500003'),
        ('Registration Status', 'Active'),
        ('Established', '2022'),
        ('Head Office', 'Ad Dammam, Ash Sharqiyah 32245, Kingdom of Saudi Arabia'),
        ('Coverage', 'Kingdom-wide &mdash; Eastern, Central and Western regions'),
        ('Solution Categories', 'Eight &mdash; isolated power panels, EV, UPS, lighting, '
                                'firefighting, HVAC, electrical distribution, general trading'),
        ('Sectors Served', 'Healthcare, government and public sector, commercial, '
                           'industrial, hospitality, aviation'),
        ('Delivery Model', 'Supply &rarr; installation &rarr; testing &amp; commissioning '
                           '&rarr; long-term maintenance'),
        ('Working Languages', 'Arabic and English'),
    ])
)

# -------------------------------------------------------------- page 3: who we are
p3 = (
    banner('Who We Are', 'Saudi-based &middot; Vision 2030 aligned &middot; Infrastructure focused') +
    '<div class="prose">'
    '<p class="lead">Black Arrow Venture is a Saudi-based trading and solutions provider '
    'dedicated to delivering comprehensive infrastructure and technology solutions across '
    'the Kingdom of Saudi Arabia.</p>'
    '<p>With a strategic focus on Electric Vehicle (EV) infrastructure, Uninterruptible '
    'Power Supply (UPS) systems, HVAC solutions and specialised engineering products, we '
    'provide complete, end-to-end services tailored to modern market demands. Our approach '
    'integrates supply, installation, testing &amp; commissioning, and long-term maintenance '
    '&mdash; ensuring reliability, efficiency and operational excellence on every project.</p>'
    '<p>We serve a wide range of sectors, including commercial, industrial, hospitality, '
    'healthcare and public infrastructure, delivering solutions that meet international '
    'standards while addressing local regulatory and operational requirements.</p>'
    '<p>Driven by innovation, quality and strong partnerships, Black Arrow Venture is '
    'committed to building resilient systems that empower businesses, enable clean mobility '
    'and support the future-ready infrastructure of Saudi Arabia.</p>'
    '</div>\n' +
    sec('By the Numbers') +
    figures([
        ('2022', 'Established'),
        ('58', 'Projects completed'),
        ('33+', 'B2B clients served'),
        ('5', 'Ongoing projects'),
        ('8', 'Solution categories'),
        ('24/7', 'Technical support'),
    ]) +
    sec('How We Work') +
    '<table class="grid">'
    '<colgroup><col style="width:150px;"><col></colgroup>'
    '<thead><tr><th>Stage</th><th>What it covers</th></tr></thead><tbody>'
    '<tr><td class="k">Supply</td><td>Sourcing and supply of equipment from established '
    'manufacturers, specified against the standards the project is held to rather than on '
    'price alone.</td></tr>'
    '<tr><td class="k">Installation</td><td>Site survey, civil works coordination and '
    'installation by our own site operations team, sequenced around live facilities where '
    'a shutdown window is not available.</td></tr>'
    '<tr><td class="k">Testing &amp; Commissioning</td><td>Functional testing, IR testing, '
    'power quality analysis and load testing, with documented handover to the client&rsquo;s '
    'engineering or biomedical team.</td></tr>'
    '<tr><td class="k">Maintenance</td><td>Preventive maintenance schedules and long-term '
    'support, including remote monitoring where the installed equipment allows it.</td></tr>'
    '</tbody></table>\n'
)

# ---------------------------------------------------- page 4: vision, mission, goals
p4 = (
    banner('Vision, Mission &amp; Goals', 'Our foundation') +
    '<div class="vm gold"><h4>Our Vision</h4>'
    '<p>To become a leading Saudi trading and solutions provider driving the Kingdom&rsquo;s '
    'transition toward sustainable energy, resilient infrastructure and smart technologies '
    '&mdash; in full alignment with Saudi Vision 2030.</p>'
    '<ul>'
    '<li>Contribute to EV infrastructure growth across the Kingdom</li>'
    '<li>Support mission-critical sectors with reliable power solutions</li>'
    '<li>Enhance building efficiency through advanced HVAC and smart systems</li>'
    '<li>Deliver integrated, high-performance solutions meeting international standards</li>'
    '</ul></div>\n'
    '<div class="vm"><h4>Our Mission</h4>'
    '<p>To deliver innovative, sustainable and reliable solutions that empower businesses, '
    'support critical infrastructure, and contribute to Saudi Arabia&rsquo;s vision for a '
    'technologically advanced and environmentally responsible future.</p>'
    '<ul>'
    '<li>Supply, installation, testing and commissioning on every project</li>'
    '<li>Long-term maintenance ensuring ongoing reliability</li>'
    '<li>Partnerships built on trust, quality and innovation</li>'
    '<li>Full compliance with international and local standards</li>'
    '</ul></div>\n' +
    sec('Alignment with Saudi Vision 2030') +
    '<table class="grid">'
    '<colgroup><col style="width:170px;"><col></colgroup>'
    '<thead><tr><th>Vision 2030 theme</th><th>How our work contributes</th></tr></thead><tbody>'
    '<tr><td class="k">Sustainable Energy</td><td>EV charging infrastructure and energy-efficient '
    'lighting and HVAC systems that reduce consumption on existing building stock.</td></tr>'
    '<tr><td class="k">Smart Infrastructure</td><td>OCPP-managed charging networks, BMS-integrated '
    'HVAC and lighting controls, and monitored power systems that report their own condition.</td></tr>'
    '<tr><td class="k">Economic Growth</td><td>Local supply, installation and maintenance capability '
    'built inside the Kingdom, serving healthcare, government, industrial and hospitality clients.</td></tr>'
    '</tbody></table>\n' +
    sec('Why Clients Choose Us') +
    '<table class="grid">'
    '<colgroup><col style="width:170px;"><col></colgroup>'
    '<thead><tr><th>Advantage</th><th>What it means in practice</th></tr></thead><tbody>'
    '<tr><td class="k">Innovation First</td><td>We integrate current technologies to deliver '
    'future-ready solutions rather than repeating a specification that already worked once.</td></tr>'
    '<tr><td class="k">Reliable Performance</td><td>Every system we deliver is engineered for '
    'uptime and operational excellence.</td></tr>'
    '<tr><td class="k">Vision 2030 Aligned</td><td>Our solutions actively contribute to Saudi '
    'Arabia&rsquo;s national transformation.</td></tr>'
    '<tr><td class="k">End-to-End Service</td><td>Supply, installation, testing, commissioning '
    'and long-term maintenance from a single accountable party.</td></tr>'
    '</tbody></table>\n'
)

# ------------------------------------------------------------ page 5: solutions I
p5 = (
    banner('Solutions Portfolio', 'Part 1 of 2 &mdash; Critical power &amp; clean mobility') +
    service(
        'Isolated Power Panels (IPP)', 'Critical care power',
        'Hospital-grade isolated power systems for operating rooms and critical care areas, '
        'keeping equipment energised through a single ground fault while the fault is detected '
        'and alarmed &mdash; engineered to meet NFPA&nbsp;99 requirements for wet procedure locations.',
        ['Isolated Power Systems &mdash; supply and integration of hospital-grade isolated power '
         'panels for operating rooms and wet procedure locations',
         'Line Isolation Monitoring &mdash; continuous ground-fault detection (LIM) that alarms on '
         'a single fault without interrupting power to life-critical equipment',
         'Compliance-Driven Design &mdash; engineered to NFPA&nbsp;99 and NFPA&nbsp;70 requirements '
         'for healthcare wet procedure locations']) +
    service(
        'EV Solutions', 'Clean mobility',
        'AC and DC fast chargers with integrated payment systems, smart monitoring and full '
        'installation support &mdash; safe, compliant and high-efficiency charging infrastructure '
        'tailored to diverse operational environments across Saudi Arabia.',
        ['EV Charging Stations &mdash; AC Level&nbsp;2 (7&ndash;22&nbsp;kW) and DC fast chargers '
         '(50&ndash;350&nbsp;kW)',
         'OCPP-compliant network management for multi-site operations',
         'Site survey, civil works coordination and commissioning services']) +
    service(
        'UPS Solutions', 'Power continuity',
        'Advanced UPS systems and battery solutions engineered for high efficiency, stability and '
        'long-term performance &mdash; from supply and installation to testing and maintenance, '
        'ensuring zero downtime for mission-critical systems.',
        ['UPS Turnkey Solutions &mdash; online double-conversion, line-interactive and standby '
         'systems (1&nbsp;kVA&ndash;1&nbsp;MVA)',
         'Remote monitoring and SNMP / Modbus connectivity',
         'Compliance with IEC&nbsp;62040 and SASO standards']) +
    service(
        'Lighting Solutions', 'Illumination',
        'Lighting systems engineered for optimal illumination, durability and energy efficiency '
        '&mdash; from architectural fa&ccedil;ade lighting to customised signage and specialised '
        'applications, reducing energy consumption while enhancing aesthetics and safety.',
        ['Fa&ccedil;ade Lighting &mdash; architectural LED systems, RGB colour control and dynamic effects',
         'Specialised Lighting &mdash; obstruction lights, helipad lighting and emergency systems',
         'Smart controls, DALI and IoT-integrated lighting management systems'])
)

# ----------------------------------------------------------- page 6: solutions II
p6 = (
    banner('Solutions Portfolio', 'Part 2 of 2 &mdash; Life safety, climate &amp; supply') +
    service(
        'Firefighting Solutions', 'Life safety',
        'Advanced firefighting systems designed to protect lives and assets across commercial, '
        'industrial and public facilities &mdash; detection, suppression and integrated safety '
        'controls engineered for reliability and rapid response in critical situations.',
        ['Detection Systems &mdash; addressable fire alarm panels, smoke, heat and gas detectors',
         'Suppression Systems &mdash; sprinkler networks, FM-200, CO&#8322; and water mist systems',
         'Integration with BMS and emergency evacuation systems']) +
    service(
        'HVAC Solutions', 'Climate control',
        'Advanced HVAC solutions designed for efficient climate control, energy optimisation and '
        'indoor air quality &mdash; supply, installation and maintenance of air handling units, '
        'ductwork and smart controls for commercial, industrial and public facilities.',
        ['Air Handling Units (AHU) &mdash; central plant, split and VRF/VRV systems',
         'Smart Controls &mdash; BMS integration, temperature zones and energy optimisation',
         'ASHRAE, SASO and Saudi Building Code compliant designs']) +
    service(
        'Electrical &amp; Power Distribution', 'Power infrastructure',
        'Electrical and power distribution solutions designed to ensure safe, reliable and '
        'efficient energy delivery across all facility types &mdash; switchgear, distribution '
        'boards, control panels and integrated systems supporting uninterrupted operations in '
        'critical environments.',
        ['Switchgear &amp; Distribution Boards &mdash; MDB, SMDB, SSMDB and DB panels',
         'Control Panels &mdash; MCC, PLC and SCADA-integrated automation panels',
         'Testing &amp; Commissioning &mdash; IR testing, power quality analysis and load testing']) +
    service(
        'General Trading', 'Diversified supply',
        'We operate as a general trading company serving the Saudi market across industrial and '
        'diversified sectors, supplying quality equipment, technical solutions and specialised '
        'products for infrastructure, commercial and institutional projects.',
        ['Industrial Sector &mdash; machinery, tools, consumables and spare parts',
         'Safety Sector &mdash; PPE, safety equipment and compliance products',
         'Aviation Sector &mdash; obstruction lights, helipad equipment and airside products'])
)

# ------------------------------------------------------- page 7: sectors & clients
SECTORS = [
    ('Healthcare', 'Hospitals and clinics &mdash; isolated power for operating theatres, UPS on '
                   'critical branches, HVAC and compliant electrical distribution.'),
    ('Government &amp; Public Sector', 'Public infrastructure, municipalities and government '
                                       'facilities &mdash; power continuity, lighting and life-safety systems.'),
    ('Commercial', 'Office buildings, retail and mixed-use developments &mdash; EV charging, '
                   'fa&ccedil;ade lighting, HVAC and power distribution.'),
    ('Industrial', 'Factories, warehouses and plants &mdash; switchgear, control panels, power '
                   'quality testing and firefighting systems.'),
    ('Hospitality', 'Hotels and hospitality properties &mdash; HVAC upgrades, guest-comfort '
                    'controls, lighting and backup power.'),
    ('Aviation', 'Obstruction lighting, helipad lighting and airside products for high-rise '
                 'and aviation-adjacent projects.'),
]
p7 = (
    banner('Sectors &amp; Clients', 'Who we serve') +
    '<div class="chips">' +
    ''.join('<span class="chip">%s</span>' % s.replace('&amp;', '&amp;') for s, _ in SECTORS) +
    '</div>\n' +
    sec('Sector Expertise') +
    '<table class="grid">'
    '<colgroup><col style="width:170px;"><col></colgroup>'
    '<thead><tr><th>Sector</th><th>What we deliver</th></tr></thead><tbody>' +
    ''.join('<tr><td class="k">%s</td><td>%s</td></tr>' % (s, d) for s, d in SECTORS) +
    '</tbody></table>\n' +
    sec('Organisations We Have Served') +
    '<div class="logo-grid">' +
    ''.join('<div class="logo-cell"><img src="%s" alt="%s"></div>' % (img(f), n)
            for f, n in CLIENTS) +
    '</div>\n' +
    '<div class="note"><b>Note:</b> Logos are shown to identify organisations for whom Black '
    'Arrow Venture has supplied equipment or carried out works. Their inclusion does not imply '
    'endorsement. Project-specific references are available on request, subject to the '
    'confidentiality terms agreed with each client.</div>\n'
)

# ------------------------------------------------------ page 8: project experience
PROJECTS = [
    ('Isolated Power for a Hospital Operating Theatre Suite',
     'Healthcare &middot; Eastern Province',
     'A private hospital expanding its surgical capacity needed new operating theatres to satisfy '
     'NFPA&nbsp;99 for wet procedure locations. Existing theatres in the adjoining wing had line '
     'isolation monitors that had never been recalibrated, and an accreditation review would have '
     'looked at the suite as a whole.',
     'We surveyed the whole suite before quoting, supplied and installed isolated power panels with '
     'integrated line isolation monitors for the new theatres, and recalibrated and re-documented '
     'the existing ones. Work was sequenced between surgical lists rather than closing the suite.',
     'The suite now runs on one documented maintenance schedule covering every theatre.'),
    ('UPS Replacement on a Healthcare Critical Branch',
     'Healthcare &middot; Western Region',
     'A healthcare facility was running UPS units past end of life, with batteries no longer holding '
     'rated autonomy and spare parts becoming difficult to source.',
     'We replaced the units on the critical branch without a shutdown window, working around live '
     'clinical operations.',
     'Full rated autonomy restored on current-generation equipment with a supported spare parts '
     'path. Clinical operations continued throughout.'),
    ('EV Charging Rollout Across a Commercial Retail Complex',
     'Commercial &middot; Central Region',
     'A mixed retail and office development wanted EV charging in its parking structure. Tenant '
     'demand and Vision 2030 alignment drove it; the existing electrical infrastructure constrained it.',
     'We sized a mix of AC and DC charging to the supply that was already there, and laid the '
     'distribution out ahead of demand.',
     'Live within the existing electrical supply, avoiding the substation upgrade the original '
     'brief would have required, and expandable without repeating the civil works.'),
    ('Obstruction and Helipad Lighting for a High-Rise Development',
     'Aviation &amp; Commercial &middot; Saudi Arabia',
     'A high-rise development required aviation obstruction lighting to mark the structure, plus '
     'lighting for a rooftop helipad intended for emergency medical access.',
     'We supplied and installed the obstruction and helipad lighting with monitored, alarmed '
     'fixtures.',
     'The structure is marked in line with aviation requirements and the helipad is lit for night '
     'operations; failed fixtures are reported when they fail, not at inspection.'),
    ('HVAC Upgrade for a Hospitality Property',
     'Hospitality &middot; Eastern Province',
     'An operating hotel had recurring guest complaints about inconsistent room temperatures &mdash; '
     'some floors ran cold, others could not hold setpoint through the afternoon peak.',
     'We upgraded the system floor by floor with BMS-integrated zone control, keeping the property '
     'open and trading.',
     'Setpoint holds consistently across floors through the afternoon peak, with per-zone visibility '
     'through the BMS. Only one floor of inventory was out at any time.'),
]
p8 = (
    banner('Project Experience', 'Representative work') +
    ''.join(
        '<div class="proj"><div class="h"><span class="n">%s</span><span class="m">%s</span></div>'
        '<p><b>Challenge.</b> %s</p><p><b>What we did.</b> %s</p>'
        '<p class="out"><b>Outcome.</b> %s</p></div>' % p for p in PROJECTS) + '\n' +
    '<div class="note"><b>Confidentiality:</b> Client names and identifying project details are '
    'withheld under the confidentiality terms agreed with each client. These are representative '
    'accounts of work we carry out; scope descriptions are accurate, and we have deliberately not '
    'published performance figures we cannot evidence publicly.</div>\n'
)

# --------------------------------------------------- page 9: standards & commitments
STANDARDS = [
    ('NFPA 99', 'Health Care Facilities Code &mdash; isolated power and line isolation monitoring '
                'for wet procedure locations.'),
    ('NFPA 70', 'National Electrical Code &mdash; healthcare electrical installation requirements.'),
    ('IEC 62040', 'Uninterruptible power systems &mdash; performance and test requirements.'),
    ('SASO', 'Saudi Standards, Metrology and Quality Organization conformity for supplied equipment.'),
    ('Saudi Building Code', 'Electrical, mechanical and fire-safety provisions.'),
    ('ASHRAE', 'HVAC design, ventilation and indoor air quality standards.'),
    ('OCPP', 'Open Charge Point Protocol &mdash; vendor-neutral management of multi-site EV networks.'),
    ('DALI', 'Digital addressable lighting interface for controllable and monitored luminaires.'),
    ('Data Protection', 'Handling of client and personal data in line with GDPR principles and '
                        'Saudi data protection requirements.'),
]
p9 = (
    banner('Standards &amp; Commitments', 'What we build to, and what happens after handover') +
    sec('Codes, Standards &amp; Compliance') +
    '<table class="grid">'
    '<colgroup><col style="width:160px;"><col></colgroup>'
    '<thead><tr><th>Standard</th><th>Where it applies in our work</th></tr></thead><tbody>' +
    ''.join('<tr><td class="k">%s</td><td>%s</td></tr>' % (s, d) for s, d in STANDARDS) +
    '</tbody></table>\n' +
    sec('Service Commitments') +
    '<table class="grid">'
    '<colgroup><col style="width:160px;"><col></colgroup>'
    '<thead><tr><th>Commitment</th><th>Detail</th></tr></thead><tbody>'
    '<tr><td class="k">24/7 Support</td><td>Round-the-clock assistance for operational needs on '
    'systems we have supplied or maintain.</td></tr>'
    '<tr><td class="k">Fast Response</td><td>Response within 15 minutes during business hours '
    '(Sunday&ndash;Thursday, 8:00 AM&ndash;6:00 PM).</td></tr>'
    '<tr><td class="k">Inquiry Turnaround</td><td>All inquiries answered within one business day. '
    'WhatsApp inquiries accepted 24/7.</td></tr>'
    '<tr><td class="k">Warranty</td><td>Warranty coverage as per factory / manufacturer terms, '
    'confirmed in writing on each quotation.</td></tr>'
    '<tr><td class="k">Regulatory Compliance</td><td>Fully compliant with Saudi Arabian regulations '
    'and applicable industry standards.</td></tr>'
    '</tbody></table>\n' +
    '<div class="note"><b>Certificates on request.</b> Commercial Registration, VAT registration '
    'and equipment conformity certificates are provided with any quotation or on request to '
    'info@blackarrowksa.com.</div>\n'
)

# ------------------------------------------------- page 10: registration & contacts
TEAM = [
    ('Adnan Afzal', 'Sales Team Head &mdash; Saudi Arabia', 'sales@blackarrowksa.com', '+966 560 224 715'),
    ('Zayn Mohammad', 'Head of Business Development', 'businessdevelopment@blackarrowksa.com', '+966 546 104 313'),
    ('Talha Ahmed', 'Head of Projects', 'projects@blackarrowksa.com', '+966 531 125 329'),
    ('Shahzad Ahmed', 'Head of Site Operations', 'operations@blackarrowksa.com', '+966 500 378 664'),
    ('Asad Muhammad', 'Client Relations Officer', 'crs@blackarrowksa.com', '+966 551 954 925'),
]
p10 = (
    banner('Registration &amp; Contacts', 'Company records and who to call') +
    sec('Company Registration') +
    spec([
        ('Legal Name', 'Black Arrow Venture Company'),
        ('Entity Type', 'Limited Liability Company (LLC)'),
        ('Unified ID / Commercial Registration (CR)', '7054542985'),
        ('VAT Registration Number', '314841084500003'),
        ('Registration Status', 'Active'),
        ('Established', '2022'),
        ('Registered Address', 'Ad Dammam, Ash Sharqiyah 32245, Kingdom of Saudi Arabia'),
    ]) +
    sec('Key Contacts') +
    '<table class="grid">'
    '<colgroup><col style="width:130px;"><col style="width:150px;"><col><col style="width:112px;"></colgroup>'
    '<thead><tr><th>Name</th><th>Role</th><th>Email</th><th>Direct</th></tr></thead><tbody>' +
    ''.join('<tr><td class="k">%s</td><td>%s</td><td>%s</td>'
            '<td class="num"><span class="num-ltr">%s</span></td></tr>' % t for t in TEAM) +
    '</tbody></table>\n' +
    sec('General Enquiries') +
    spec([
        ('Telephone / WhatsApp', '<span class="num-ltr">+966 560 224 715</span>'),
        ('Email', 'info@blackarrowksa.com'),
        ('Website', 'www.blackarrowksa.com'),
        ('Instagram', '@blackarrowventure'),
        ('Business Hours', 'Sunday &ndash; Thursday, 8:00 AM &ndash; 6:00 PM. '
                           'Friday &amp; Saturday closed. WhatsApp accepted 24/7.'),
    ]) +
    '<div class="qr-pair">'
    '<div class="qr-block"><img src="' + QR_SITE + '" alt="QR code for www.blackarrowksa.com">'
    '<div class="cap">Website</div></div>'
    '<div class="qr-block"><img src="' + QR_INSTA + '" alt="QR code for instagram.com/blackarrowventure">'
    '<div class="cap">Instagram</div></div>'
    '</div>\n'
)

PAGES = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]

html = (
    '<!DOCTYPE html>\n'
    '<html lang="en"><head><meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="robots" content="noindex, nofollow">\n'
    '<meta name="description" content="Black Arrow Venture Company Profile - Saudi trading and '
    'solutions provider for isolated power panels, EV charging, UPS, lighting, firefighting, HVAC '
    'and electrical distribution.">\n'
    '<title>Company Profile &mdash; Black Arrow Venture</title>\n'
    '<style>' + CSS + '</style></head>\n<body>\n' +
    ''.join(page(i + 1, body) for i, body in enumerate(PAGES)) +
    '\n</body></html>\n'
)

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(html)

print('wrote %s' % OUT)
print('  %d pages, %.1f KB' % (TOTAL_PAGES, len(html.encode('utf-8')) / 1024.0))
