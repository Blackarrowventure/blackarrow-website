#!/usr/bin/env python3
"""Adds three shared blocks to every English service page (services/<slug>/):

  1. "UPS brands we work with"  - UPS pages only. Brand names as plain text
     so search engines see them; a note makes clear Black Arrow is an
     independent provider (no partnership claim).
  2. "Maintenance and support"  - 1, 2 or 3-year contracts with emergency
     visits, worded as a general offer with no fixed response times.
  3. "Request a quote"           - Web3Forms form, sent in place by app.js
     (form[data-w3f]) to the same inbox as the contact page.

Each block sits between BEGIN/END markers, so the script is safe to re-run
(it replaces its own blocks). Run it after any script that rewrites service
pages (build_aviation.py, build_hubs.py), then run build_ar.py --build to
regenerate the Arabic twins. Arabic text for every data-i18n key below is in
assets/translations/ar.json.

Usage: python scripts/add_service_blocks.py
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICES = os.path.join(ROOT, 'services')
BEGIN = '<!-- BEGIN service-blocks (scripts/add_service_blocks.py) -->'
END = '<!-- END service-blocks -->'
ACCESS_KEY = '217e03f8-59ef-45c3-9cf8-048f27ba0586'   # same Web3Forms key as contact.html
SKIP = {'consultancy'}                                 # consultancy pages have their own builder

# Brands commonly installed in Saudi Arabia and the GCC. Plain text, never logos.
UPS_BRANDS = ['Schneider Electric (APC)', 'Eaton', 'Vertiv (Liebert)', 'Riello UPS', 'Socomec', 'Legrand',
              'ABB', 'Huawei', 'Delta Electronics', 'Kehua', 'Borri', 'Gamatronic', 'AEG Power Solutions',
              'Mitsubishi Electric', 'Toshiba', 'Fuji Electric', 'Salicru', 'INFORM', 'KSTAR', 'CyberPower']

CSS = '''<style>
  .svc-blocks{padding-block:64px;background:#f4f5f2;color:#1a1a1a;}
  .svc-blocks .container{display:flex;flex-direction:column;gap:48px;}
  .svc-blocks h2{color:#1a1a1a !important;font-size:1.6rem;margin:0 0 10px;}
  .svc-blocks__lead{color:#4a4a4a;max-width:70ch;margin:0;}
  .svc-brands__list{list-style:none;padding:0;margin:18px 0 0;display:flex;flex-wrap:wrap;gap:8px;}
  .svc-brands__list li{background:#fff;border:1px solid #dcdcd5;border-radius:999px;padding:7px 14px;font-size:.88rem;font-weight:600;color:#222;}
  .svc-brands__note{margin:12px 0 0;font-size:.78rem;color:#777;}
  .svc-support__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:20px;}
  .svc-support__card{background:#fff;border:1px solid #dcdcd5;border-radius:12px;padding:20px;}
  .svc-support__card h3{font-size:1.05rem;margin:0 0 8px;color:#1a1a1a;}
  .svc-support__card p{margin:0;color:#4a4a4a;font-size:.92rem;line-height:1.6;}
  .svc-support__note{margin:14px 0 0;font-size:.85rem;color:#666;}
  .svc-quote{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:32px;align-items:start;}
  .svc-quote__intro ul{margin:16px 0 0;padding-inline-start:20px;color:#333;line-height:1.8;}
  .svc-quote__wa{display:inline-flex;align-items:center;gap:8px;margin-top:18px;font-weight:700;color:#0f6b3a !important;}
  .svc-quote .form-card{margin:0;}
  .svc-quote__msg{display:none;margin-top:14px;padding:12px 14px;border-radius:8px;font-weight:600;}
  .svc-quote__msg--ok{background:#e6f4ea;color:#1e5e30;}
  .svc-quote__msg--err{background:#fdecea;color:#8a1c12;}
  @media (max-width:860px){.svc-support__grid,.svc-quote{grid-template-columns:1fr;}}
</style>'''


def esc(s):
    return html.escape(s, quote=True)


def brands_block():
    return ('<div class="svc-brands">'
            '<h2 data-i18n="svcb_brands_title">UPS brands we supply, install and maintain</h2>'
            '<p class="svc-blocks__lead" data-i18n="svcb_brands_lead">We work with the UPS systems commonly installed in Saudi Arabia and the GCC, '
            'so one team can supply, install and maintain the units on your site, including mixed-brand installations.</p>'
            '<ul class="svc-brands__list">' + ''.join('<li>' + esc(b) + '</li>' for b in UPS_BRANDS) + '</ul>'
            '<p class="svc-brands__note" data-i18n="svcb_brands_note">Brand names are trademarks of their respective owners. '
            'Black Arrow is an independent supplier and service provider.</p>'
            '</div>')


def support_block():
    cards = [
        ('svcb_support_c1_t', '1, 2 or 3-year maintenance contracts', 'svcb_support_c1_p',
         'Planned preventive maintenance visits, inspection and test reports, and recommendations, on a contract length that suits your site.'),
        ('svcb_support_c2_t', 'Emergency visits', 'svcb_support_c2_p',
         'Emergency call-outs are part of the maintenance contract and are handled with priority according to the criticality of your site.'),
        ('svcb_support_c3_t', 'One team for every system', 'svcb_support_c3_p',
         'We maintain every system we supply and install, and we can take over the maintenance of existing systems on your site.'),
    ]
    return ('<div class="svc-support">'
            '<h2 data-i18n="svcb_support_title">Maintenance and support after handover</h2>'
            '<p class="svc-blocks__lead" data-i18n="svcb_support_lead">Our work does not end at commissioning. We keep your systems running with a maintenance plan built around your site.</p>'
            '<div class="svc-support__grid">' + ''.join(
                '<div class="svc-support__card"><h3 data-i18n="' + kt + '">' + esc(t) + '</h3><p data-i18n="' + kp + '">' + esc(p) + '</p></div>'
                for kt, t, kp, p in cards) + '</div>'
            '<p class="svc-support__note" data-i18n="svcb_support_note">Visit frequency, emergency arrangements and spare parts are agreed with each client based on the site and the systems covered.</p>'
            '</div>')


def option(key, value, text):
    return '<option value="' + esc(value) + '" data-i18n="' + key + '">' + esc(text) + '</option>'


def quote_block(service_name):
    cities = [('svcb_city_dammam', 'Dammam'), ('svcb_city_khobar', 'Al Khobar'), ('svcb_city_dhahran', 'Dhahran'),
              ('svcb_city_jubail', 'Jubail'), ('svcb_city_ahsa', 'Al Ahsa'), ('svcb_city_riyadh', 'Riyadh'),
              ('svcb_city_jeddah', 'Jeddah'), ('svcb_city_makkah', 'Makkah'), ('svcb_city_madinah', 'Madinah'),
              ('svcb_city_other', 'Other')]
    kinds = [('svcb_type_new', 'New supply and installation'), ('svcb_type_amc', 'Maintenance contract (1, 2 or 3 years)'),
             ('svcb_type_repair', 'Repair or emergency visit'), ('svcb_type_survey', 'Site survey or assessment'),
             ('svcb_type_consult', 'Technical consultancy'), ('svcb_type_other', 'Other')]
    return (
        '<div class="svc-quote" id="request-quote">'
        '<div class="svc-quote__intro">'
        '<h2 data-i18n="svcb_quote_title">Request a quote or site survey</h2>'
        '<p class="svc-blocks__lead" data-i18n="svcb_quote_lead">Tell us about your site and what you need. An engineer will review your request and contact you to discuss it.</p>'
        '<ul><li data-i18n="svcb_quote_b1">Supply, installation and commissioning</li>'
        '<li data-i18n="svcb_quote_b2">Maintenance contracts and emergency visits</li>'
        '<li data-i18n="svcb_quote_b3">Site surveys and technical assessments</li></ul>'
        '<a class="svc-quote__wa" href="https://wa.me/966560224715" target="_blank" rel="noopener noreferrer" data-i18n="svcb_quote_wa">Prefer WhatsApp? Message us →</a>'
        '</div>'
        '<div class="form-card">'
        '<form id="quote-form" action="https://api.web3forms.com/submit" method="POST" data-w3f data-lead="quote_request"'
        ' data-success="quote-ok" data-error="quote-err" aria-label="Request a quote" data-i18n-aria-label="svcb_quote_title">'
        '<input type="hidden" name="access_key" value="' + ACCESS_KEY + '">'
        '<input type="hidden" name="subject" value="Quote request: ' + esc(service_name) + '">'
        '<input type="hidden" name="from_name" value="Black Arrow Website">'
        '<input type="hidden" name="service" value="' + esc(service_name) + '">'
        '<input type="checkbox" name="botcheck" aria-label="Leave this box empty" class="hidden" style="display:none" tabindex="-1" autocomplete="off">'
        '<div class="form-row">'
        '<div class="form-group"><label for="q-name" data-i18n="form_label_name_req">Full Name *</label>'
        '<input type="text" id="q-name" name="name" required autocomplete="name" aria-required="true"></div>'
        '<div class="form-group"><label for="q-company" data-i18n="form_company">Company Name</label>'
        '<input type="text" id="q-company" name="company" autocomplete="organization"></div>'
        '</div>'
        '<div class="form-row">'
        '<div class="form-group"><label for="q-phone" data-i18n="form_label_phone_req">Phone Number *</label>'
        '<input type="tel" id="q-phone" name="phone" placeholder="+966 5XX XXX XXXX" required autocomplete="tel" aria-required="true"></div>'
        '<div class="form-group"><label for="q-email" data-i18n="form_label_email_req">Email Address *</label>'
        '<input type="email" id="q-email" name="email" placeholder="your@email.com" required autocomplete="email" aria-required="true"></div>'
        '</div>'
        '<div class="form-row">'
        '<div class="form-group"><label for="q-city" data-i18n="svcb_city">City</label>'
        '<select id="q-city" name="city"><option value="" data-i18n="svcb_select">Select…</option>' + ''.join(option(k, v, v) for k, v in cities) + '</select></div>'
        '<div class="form-group"><label for="q-type" data-i18n="svcb_type">Type of request</label>'
        '<select id="q-type" name="request_type"><option value="" data-i18n="svcb_select">Select…</option>' + ''.join(option(k, v, v) for k, v in kinds) + '</select></div>'
        '</div>'
        '<div class="form-group"><label for="q-details" data-i18n="svcb_details">Project details</label>'
        '<textarea id="q-details" name="message" rows="4" data-i18n-placeholder="svcb_details_ph" '
        'placeholder="Site type, number or size of systems, current situation, preferred date"></textarea></div>'
        '<button type="submit" class="btn btn-primary" style="width:100%;" data-i18n="svcb_send">Send request</button>'
        '<p class="svc-quote__msg svc-quote__msg--ok" id="quote-ok" role="status" data-i18n="svcb_ok">Thank you. Your request has been sent and an engineer will contact you.</p>'
        '<p class="svc-quote__msg svc-quote__msg--err" id="quote-err" role="alert" data-i18n="svcb_err">Sorry, the request could not be sent. Please call +966 56 022 4715 or email info@blackarrowksa.com.</p>'
        '</form></div></div>')


def is_ups(slug, text):
    return 'ups' in slug or 'vrla' in slug


def main():
    done = 0
    for slug in sorted(os.listdir(SERVICES)):
        path = os.path.join(SERVICES, slug, 'index.html')
        if slug in SKIP or not os.path.isfile(path):
            continue
        with open(path, encoding='utf-8') as f:
            src = f.read()
        src = re.sub(r'\n?[ \t]*' + re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', '\n', src, flags=re.S)
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', src, re.S)
        name = html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).strip() if h1 else slug.replace('-', ' ').title()
        parts = ([brands_block()] if is_ups(slug, src) else []) + [support_block(), quote_block(name)]
        block = ('    ' + BEGIN + '\n    ' + CSS + '\n    <section class="svc-blocks" aria-label="Maintenance, support and quote request" data-i18n-aria-label="svcb_section_aria">'
                 '<div class="container">' + ''.join(parts) + '</div></section>\n    ' + END + '\n')
        anchor = src.find('<section class="wa-banner"')
        if anchor == -1:
            anchor = src.find('</main>')
        line_start = src.rfind('\n', 0, anchor) + 1
        src = src[:line_start] + block + src[line_start:]
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(src)
        done += 1
    print('service pages updated:', done)


if __name__ == '__main__':
    main()
