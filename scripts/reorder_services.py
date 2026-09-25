"""
Puts Aviation first and HVAC last everywhere the main site lists its services:
homepage grid, Services page (quick links + detail sections), footers; the menu
dropdown and the Industries hub follow SERVICES in build_hubs.py.
Also adds "maintenance" to the Aviation card / section copy.

    py scripts/reorder_services.py && py scripts/build_hubs.py && py scripts/build_ar.py --build
"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.stdout.reconfigure(encoding='utf-8')


def rd(p):
    s = (ROOT / p).read_text('utf-8')
    return s.replace('\r\n', '\n'), '\r\n' in s


def wr(p, t, crlf):
    (ROOT / p).write_text(t.replace('\n', '\r\n') if crlf else t, encoding='utf-8', newline='')


# ------------------------------------------------------------------ homepage grid
def home_grid():
    t, crlf = rd('index.html')
    g = t.index('<div class="services-grid">')
    end = t.index('</section>', g)
    seg = t[g:end]
    arts = list(re.finditer(r'<article class="svc-card[^"]*">.*?</article>', seg, re.S))
    texts = [m.group(0) for m in arts]

    def key(x):
        return re.search(r'<h3[^>]*>(.*?)</h3>', x).group(1)
    avi = [x for x in texts if key(x) == 'Aviation'][0]
    hvac = [x for x in texts if key(x) == 'HVAC Solutions'][0]
    rest = [x for x in texts if x is not avi and x is not hvac]
    order = [avi] + rest + [hvac]
    # rebuild: keep the text before the first article and after the last one
    head = seg[:arts[0].start()]
    tail = seg[arts[-1].end():]
    body = '\n\n          '.join(order)
    new = head + body + tail
    # maintenance in the card copy
    new = new.replace('''                <span data-i18n="supply_label">Supply</span>
                <span data-i18n="installation">Installation</span>
''', '''                <span data-i18n="supply_label">Supply</span>
                <span data-i18n="installation">Installation</span>
                <span data-i18n="maintenance">Maintenance</span>
''')
    new = new.replace('airside electrical distribution and UPS backup power.</p>', 'airside electrical distribution, UPS backup power and maintenance.</p>')
    t = t[:g] + new + t[end:]
    wr('index.html', t, crlf)


# ------------------------------------------------------------------ services page
def services_page():
    t, crlf = rd('services.html')
    # quick links: Aviation gets its own first group; HVAC goes last in the life-safety group
    btn_avi = re.search(r'\n[ \t]*<a href="/services/aviation/" class="btn btn-outline"[^\n]*</a>', t)
    if btn_avi and 'svc_cat_aviation' not in t[:btn_avi.start()][-800:]:
        line = btn_avi.group(0)
        t = t.replace(line, '', 1)
        first = t.index('<span style="display:block;text-align:center;font-size:.75rem;')
        first = t.rindex('<div>', 0, first)
        group = ('<div>\n          <span style="display:block;text-align:center;font-size:.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;'
                 'color:#F59E0B;margin-bottom:10px;" data-i18n="svc_cat_aviation">Aviation &amp; Airside</span>\n'
                 '          <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;">' + line + '\n'
                 '          </div>\n        </div>\n\n        ')
        t = t[:first] + group + t[first:]
    hv = re.search(r'\n[ \t]*<a href="/services/hvac-solutions/" class="btn btn-outline"[^\n]*</a>', t)
    if hv:
        line = hv.group(0)
        t = t.replace(line, '', 1)
        fs = t.index('/services/firefighting-systems/" class="btn btn-outline" style="color:rgba')
        after = t.index('</a>', fs) + 4
        t = t[:after] + line + t[after:]
    # detail sections: Aviation first, HVAC last
    marks = list(re.finditer(r'    <!-- ═══ [^\n]*═══ -->\n', t))
    first_sec = None
    blocks = []
    detail = [m for m in marks if 'id="' not in m.group(0)]
    starts = [m.start() for m in marks]
    # only the service-detail region (comment immediately followed by a service-detail section)
    region = []
    for i, m in enumerate(marks):
        if i + 1 < len(starts):
            nxt = starts[i + 1]
        else:
            nxt = t.index('</section>', m.start()) + len('</section>') + 2
        body = t[m.start(): nxt]
        if re.match(r'    <!-- ═══[^\n]*═══ -->\n    <section id="[a-z-]+" class="service-detail"', body):
            region.append((m.start(), nxt, body))
    if region:
        a, b = region[0][0], region[-1][1]
        bodies = [r[2] for r in region]

        def sid(x):
            return re.search(r'<section id="([a-z-]+)"', x).group(1)
        avi = [x for x in bodies if sid(x) == 'aviation'][0]
        hv = [x for x in bodies if sid(x) == 'hvac'][0]
        rest = [x for x in bodies if x is not avi and x is not hv]
        t = t[:a] + avi + ''.join(rest) + hv + t[b:]
    # copy: maintenance bullet + Offer text
    if 'avi_maint_li' not in t:
        t = t.replace('''              <li data-i18n="avi_c4t">Airside electrical distribution</li>
''', '''              <li data-i18n="avi_c4t">Airside electrical distribution</li>
              <li data-i18n="avi_maint_li">Maintenance of aviation lighting</li>
''', 1)
    t = t.replace('runway and taxiway edge lighting, airside electrical distribution and UPS backup power for aviation facilities"',
                  'runway and taxiway edge lighting, airside electrical distribution, UPS backup power and maintenance for aviation facilities"')
    wr('services.html', t, crlf)


# ------------------------------------------------------------------ footers
ORDER = ['/services/aviation/', '/services/isolated-power-panels/', '/services/ev-charging-solutions/', '/services/ups-power-backup/',
         '/services/lighting-solutions/', '/services/firefighting-systems/', '/services/electrical-distribution/',
         '/services/hospital-modular-or-rooms/', '/services/lead-sheets-hospital/', '/services/hvac-solutions/']


def footers():
    n = 0
    for f in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        rel = Path(f).relative_to(ROOT).as_posix()
        if rel.startswith(('3d/', 'ar/', 'drafts/', 'company-materials/', 'contacts/', '.wrangler/', 'node_modules/')):
            continue
        s = open(f, encoding='utf-8', newline='').read()
        if 'data-i18n="footer_services"' not in s:
            continue
        i = s.index('data-i18n="footer_services"')
        u0 = s.index('<ul>', i)
        u1 = s.index('</ul>', u0)
        items = re.findall(r'<li><a href="(/services/[^"]+)"[^>]*>[^<]*</a></li>', s[u0:u1])
        lis = {m.group(1): m.group(0) for m in re.finditer(r'<li><a href="(/services/[^"]+)"[^>]*>[^<]*</a></li>', s[u0:u1])}
        if not lis:
            continue
        indent = '\n            '
        ordered = [lis[h] for h in ORDER if h in lis] + [v for k, v in lis.items() if k not in ORDER]
        new = '<ul>' + indent + indent.join(ordered) + '\n          '
        s2 = s[:u0] + new + s[u1:]
        if s2 != s:
            open(f, 'w', encoding='utf-8', newline='').write(s2)
            n += 1
    print('footers reordered:', n)


def copy_keys():
    NEW = {'service_aviation_desc_home': ('Helipad and obstruction lighting, runway and taxiway edge lighting, airside electrical distribution, UPS backup power and maintenance.',
                                          'إضاءة المهابط والعوائق وإضاءة حواف المدارج والممرات والتوزيع الكهربائي للمناطق الجانبية وطاقة UPS الاحتياطية والصيانة.')}
    for name, idx in (('ar.json', 1), ('en.json', 0)):
        p = ROOT / 'assets/translations' / name
        raw = p.read_text('utf-8')
        d = json.loads(raw)
        for k, v in NEW.items():
            d[k] = v[idx]
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else ''), encoding='utf-8', newline='')


if __name__ == '__main__':
    home_grid()
    services_page()
    footers()
    copy_keys()
    print('ok')
