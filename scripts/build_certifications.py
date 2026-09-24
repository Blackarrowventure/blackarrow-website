"""
Build /certifications/ (EN + AR twin via build_ar.py) from the three ISO
certificates already published on the site.

Every value below is read off the certificate images in
assets/images/certifications/ (issued by Magnitude Management Services Pvt. Ltd.,
EGAC CAB #011805).  Nothing is added that is not printed on them.

    py scripts/build_certifications.py
    py scripts/build_ar.py --build
"""
import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding='utf-8')
from build_hubs import make_hub, write, ROOT, nav_block  # noqa: E402

CERTS = [
    dict(std='ISO 9001:2015', tkey='cert_9001_title', dkey='cert_9001_desc', desc='Quality Management System',
         no='26MEQXX39', slug='iso-9001-2015', accr='QMS Certification'),
    dict(std='ISO 14001:2015', tkey='cert_14001_title', dkey='cert_14001_desc', desc='Environmental Management System',
         no='26MEEXS37', slug='iso-14001-2015', accr='EMS Certification'),
    dict(std='ISO 45001:2018', tkey='cert_45001_title', dkey='cert_45001_desc', desc='Occupational Health &amp; Safety Management System',
         no='26MEOXM34', slug='iso-45001-2018', accr='OHSMS Certification'),
]

SCOPE = ('Construction of residential, government, and airport buildings; electrical, HVAC, plumbing, gas, lift, '
         'firefighting, security, telecom, network, satellite, and CCTV installation and maintenance; HV/MV cable laying '
         'and lighting; technical testing and inspection; and wholesale of water tanks, furniture, appliances, and electronic parts.')

NEW_AR = {
    'nav_certifications': 'الشهادات',
    'cert_hub_h1': 'الشهادات',
    'cert_hub_sub': 'شهادات ISO 9001 وISO 14001 وISO 45001 الصادرة للشركة',
    'cert_hub_intro': 'هذه هي شهادات التسجيل الصادرة للشركة، بأرقامها وتواريخ إصدارها وانتهائها ونطاقها كما وردت في الشهادات نفسها. يمكن تحميل كل شهادة بصيغة PDF وإرفاقها بعروض الأسعار أو مستندات المناقصات.',
    'cert_lbl_standard': 'المعيار',
    'cert_lbl_body': 'جهة المنح',
    'cert_lbl_number': 'رقم الشهادة',
    'cert_lbl_issue': 'تاريخ الإصدار',
    'cert_lbl_expiry': 'تاريخ الانتهاء',
    'cert_lbl_survey': 'مواعيد المراجعة الدورية',
    'cert_lbl_scope': 'النطاق',
    'cert_lbl_holder': 'حامل الشهادة',
    'cert_date_issue': '16 سبتمبر 2026',
    'cert_date_expiry': '15 سبتمبر 2029',
    'cert_date_survey': '16 أغسطس 2027 و16 أغسطس 2028',
    'cert_holder_value': 'شركة السهم الأسود ڤنتشر (Black Arrow Venture Company)، مبنى رقم 7833، شارع 13أ، حي غماطة، الدمام، المملكة العربية السعودية',
    'cert_body_value': 'شركة Magnitude Management Services Pvt. Ltd. (MMS)، معتمدة من EGAC (رقم CAB 011805) وعضو في اتفاقية الاعتراف المتعدد الأطراف التابعة للمنتدى الدولي للاعتماد (IAF)',
    'cert_download_pdf': 'تحميل الشهادة (PDF)',
    'cert_verify_link': 'التحقق من الشهادة لدى جهة المنح',
    'cert_scope_note': 'نص النطاق أعلاه كما ورد في الشهادات وهو باللغة الإنجليزية. شهادات ISO تخص أنظمة الإدارة في الشركة، ولا تخص منتجاً أو مشروعاً بعينه.',
    'cert_hub_link': 'عرض جميع الشهادات وتفاصيلها',
}


def cards():
    out = ''
    for c in CERTS:
        rows = (
            ('cert_lbl_standard', 'Standard', '<span data-i18n="%s">%s</span> &mdash; <span data-i18n="%s">%s</span>' % (c['tkey'], c['std'], c['dkey'], c['desc'])),
            ('cert_lbl_body', 'Certification body', '<span data-i18n="cert_body_value">Magnitude Management Services Pvt. Ltd. (MMS) &mdash; EGAC-accredited (CAB #011805, %s) and a member of the IAF Multilateral Recognition Arrangement</span>' % c['accr']),
            ('cert_lbl_number', 'Certificate number', '<bdi dir="ltr">%s</bdi>' % c['no']),
            ('cert_lbl_issue', 'Issue date', '<span data-i18n="cert_date_issue">16 September 2026</span>'),
            ('cert_lbl_expiry', 'Expiry date', '<span data-i18n="cert_date_expiry">15 September 2029</span>'),
            ('cert_lbl_survey', 'Surveillance audits due', '<span data-i18n="cert_date_survey">16 August 2027 and 16 August 2028</span>'),
            ('cert_lbl_scope', 'Scope', '<span lang="en" dir="ltr" class="cert-scope">%s</span>' % SCOPE),
        )
        dl = ''.join('<div><dt data-i18n="%s">%s</dt><dd>%s</dd></div>' % r for r in rows)
        out += ('          <article class="cert-detail" id="%(slug)s">\n'
                '            <a class="cert-detail__img" href="/assets/documents/black-arrow-venture-%(slug)s.pdf" target="_blank" rel="noopener" aria-label="Open %(std)s certificate PDF">\n'
                '              <picture><source srcset="/assets/images/certifications/%(slug)s.webp" type="image/webp"><img src="/assets/images/certifications/%(slug)s.jpg" alt="%(std)s Certificate of Registration &mdash; Black Arrow Venture company" loading="lazy" width="1309" height="1853" decoding="async"></picture>\n'
                '            </a>\n'
                '            <div class="cert-detail__body">\n'
                '              <h2><span data-i18n="%(tkey)s">%(std)s</span></h2>\n'
                '              <dl>%(dl)s</dl>\n'
                '              <p class="cert-detail__actions"><a class="btn btn-primary" href="/assets/documents/black-arrow-venture-%(slug)s.pdf" target="_blank" rel="noopener" data-i18n="cert_download_pdf">Download certificate (PDF)</a></p>\n'
                '            </div>\n'
                '          </article>\n') % dict(c, dl=dl)
    return out


def body():
    return ('<section class="section">\n      <div class="container" style="max-width:1100px;">\n'
            '        <p style="color:#b8b8b8;line-height:1.8;max-width:820px;margin-bottom:12px;" data-i18n="cert_hub_intro">'
            'These are the registration certificates issued to the company, with the certificate number, issue and expiry dates and scope exactly as printed on them. '
            'Each can be downloaded as a PDF for quotations and tender documents.</p>\n'
            '        <p style="color:#b8b8b8;line-height:1.8;max-width:820px;margin-bottom:32px;"><strong style="color:#fff;" data-i18n="cert_lbl_holder">Certificate holder</strong>: '
            '<span data-i18n="cert_holder_value">Black Arrow Venture Company, Building No. 7833, St 13A, Ghimatah District, Dammam, Kingdom of Saudi Arabia</span></p>\n'
            '        <div class="cert-detail-list">\n' + cards() + '        </div>\n'
            '        <p class="cs-note" data-i18n="cert_scope_note">The scope wording above is reproduced as it appears on the certificates. ISO certification applies to the company&rsquo;s management systems, not to an individual product or project.</p>\n'
            '        <p style="margin-top:12px;"><a href="http://www.mmscertification.com/activeclients.aspx" target="_blank" rel="noopener noreferrer" data-i18n="cert_verify_link">Verify a certificate with the certification body</a></p>\n'
            '      </div>\n    </section>')


CSS = '''
/* /certifications/ detail cards */
.cert-detail-list { display: grid; gap: 28px; }
.cert-detail { display: grid; grid-template-columns: minmax(180px, 260px) 1fr; gap: 28px; padding: 22px; background: rgba(255,255,255,.04); border: 1px solid rgba(245,158,11,.22); border-radius: 14px; }
.cert-detail__img { display: block; background: #fff; border-radius: 8px; overflow: hidden; align-self: start; }
.cert-detail__img img { display: block; width: 100%; height: auto; }
.cert-detail h2 { margin: 0 0 12px; font-size: 1.5rem; color: #F59E0B; }
.cert-detail dl { margin: 0; display: grid; gap: 10px; }
.cert-detail dl > div { display: grid; grid-template-columns: 190px 1fr; gap: 14px; }
.cert-detail dt { color: #9a9a9a; font-size: .9rem; }
.cert-detail dd { margin: 0; color: #eee; line-height: 1.6; }
.cert-scope { font-size: .9rem; color: #cfcfcf; }
.cert-detail__actions { margin: 18px 0 0; }
@media (max-width: 720px) {
  .cert-detail { grid-template-columns: 1fr; padding: 16px; }
  .cert-detail__img { max-width: 260px; }
  .cert-detail dl > div { grid-template-columns: 1fr; gap: 2px; }
}
'''


def main():
    ar_path = ROOT / 'assets/translations/ar.json'
    ar = json.loads(ar_path.read_text('utf-8'))
    ar.update(NEW_AR)
    ar_path.write_text(json.dumps(ar, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')

    page = make_hub('/certifications/', 'ISO 9001, 14001 & 45001 Certifications | Black Arrow Venture',
                    'ISO 9001:2015, ISO 14001:2015 and ISO 45001:2018 certificates of Black Arrow Venture: certificate numbers, issue and expiry dates, scope and PDF downloads.',
                    'cert_hub_h1', 'Certifications', 'cert_hub_sub',
                    'ISO 9001, ISO 14001 and ISO 45001 certificates issued to the company', body(), 'about')
    write('certifications/index.html', page)

    # manifests
    pm_path = ROOT / 'scripts/pages.json'
    raw = pm_path.read_text('utf-8')
    crlf = '\r\n' in raw
    pm = json.loads(raw)
    if '/certifications/' not in {p['url'] for p in pm['pages']}:
        pm['pages'].append({'src': 'certifications/index.html', 'url': '/certifications/', 'ar': True})
    out = json.dumps(pm, ensure_ascii=False, indent=2)
    pm_path.write_text(out.replace('\n', '\r\n') if crlf else out, encoding='utf-8', newline='')

    pp_path = ROOT / 'assets/translations/ar-pages.json'
    raw = pp_path.read_text('utf-8')
    crlf = '\r\n' in raw
    pp = json.loads(raw)
    d = 'شهادات ISO 9001:2015 وISO 14001:2015 وISO 45001:2018 الصادرة للسهم الأسود ڤنتشر: أرقام الشهادات وتواريخ الإصدار والانتهاء والنطاق وتحميل PDF.'
    pp['certifications/index.html'] = {'title': 'شهادات ISO 9001 و14001 و45001 | السهم الأسود ڤنتشر', 'description': d,
                                       'og_title': 'شهادات ISO 9001 و14001 و45001 | السهم الأسود ڤنتشر', 'og_description': d}
    out = json.dumps(pp, ensure_ascii=False, indent=2)
    pp_path.write_text(out.replace('\n', '\r\n') if crlf else out, encoding='utf-8', newline='')

    # CSS (append once)
    css = ROOT / 'assets/css/styles.css'
    t = css.read_text('utf-8')
    if '.cert-detail-list' not in t:
        nl = '\r\n' if '\r\n' in t else '\n'
        css.write_text(t.rstrip() + nl + CSS.replace('\n', nl), encoding='utf-8', newline='')

    # footer quick link + homepage button
    n = 0
    for f in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        rel = Path(f).relative_to(ROOT).as_posix()
        if rel.startswith(('3d/', 'ar/', 'drafts/', 'company-materials/', 'contacts/', '.wrangler/', 'node_modules/')):
            continue
        s = open(f, encoding='utf-8', newline='').read()
        if '/resources/case-studies/" data-i18n="nav_case_studies">' not in s or 'href="/certifications/"' in s:
            continue
        s2 = re.sub(r'(<li><a href="/resources/case-studies/" data-i18n="nav_case_studies">[^<]*</a></li>)',
                    r'\1\n            <li><a href="/certifications/" data-i18n="nav_certifications">Certifications</a></li>', s, count=1)
        if s2 != s:
            open(f, 'w', encoding='utf-8', newline='').write(s2)
            n += 1
    print('footers updated:', n)

    idx = ROOT / 'index.html'
    s = idx.read_text('utf-8')
    if 'data-i18n="cert_hub_link"' not in s:
        marker = '          </div>\n        </div>\n      </div>\n    </section>\n\n\n    <!-- ═══════════════════════════════════════\n         CLIENT TESTIMONIALS'
        crlf = '\r\n' in s
        t = s.replace('\r\n', '\n')
        i = t.index('<div class="cert-grid">')
        j = t.index('</section>', i)
        btn = '        <p class="reveal" style="text-align:center;margin-top:28px;"><a class="btn btn-outline" href="/certifications/" data-i18n="cert_hub_link">View all certificates and details</a></p>\n      </div>\n    '
        # insert before the closing </div> of the container that precedes </section>
        k = t.rindex('</div>', i, j)
        t = t[:k] + btn.replace('      </div>\n    ', '') + '      ' + t[k:]
        idx.write_text(t.replace('\n', '\r\n') if crlf else t, encoding='utf-8', newline='')


if __name__ == '__main__':
    main()
