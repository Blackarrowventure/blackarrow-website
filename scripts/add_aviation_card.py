"""Adds the Aviation card (with photo) to the homepage services grid and the photo to the
Aviation section on services.html. Safe to re-run."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.stdout.reconfigure(encoding='utf-8')

NEW = {
    'svc_cat_aviation': ('Aviation & Airside', 'الطيران والمناطق الجانبية'),
    'avi_alt': ('Helipad on a rooftop with perimeter lighting at dusk', 'مهبط مروحيات على سطح مبنى مع إضاءة محيطية عند الغروب'),
    'service_aviation_desc_home': ('Helipad and obstruction lighting, runway and taxiway edge lighting, airside electrical distribution and UPS backup power.',
                                   'إضاءة المهابط والعوائق وإضاءة حواف المدارج والممرات والتوزيع الكهربائي للمناطق الجانبية وطاقة UPS الاحتياطية.'),
    'supply_label': ('Supply', 'التوريد'),
}
ALT_EN = NEW['avi_alt'][0]

CARD = '''
          <article class="svc-card svc-card--wide reveal">
            <div class="svc-card__img-wrap">
              <picture>
                <source srcset="/assets/images/services/aviation-solutions-768.webp" type="image/webp">
                <img src="/assets/images/services/aviation-solutions.jpg" alt="%(alt)s" class="svc-card__img" loading="lazy" width="1536" height="1152" decoding="async" data-i18n-alt="avi_alt">
              </picture>
              <span class="svc-card__img-label" data-i18n="service_aviation">Aviation</span>
            </div>
            <div class="svc-card__body">
              <div class="svc-card__category" data-i18n="svc_cat_aviation">Aviation &amp; Airside</div>
              <h3 data-i18n="service_aviation">Aviation</h3>
              <p data-i18n="service_aviation_desc_home">%(desc)s</p>
              <ul class="svc-card__benefits">
                <li data-i18n="avi_c1t">Helipad lighting</li>
                <li data-i18n="avi_c2t">Obstruction and warning lights</li>
                <li data-i18n="avi_c4t">Airside electrical distribution</li>
              </ul>
              <div class="svc-card__breadth">
                <span data-i18n="supply_label">Supply</span>
                <span data-i18n="installation">Installation</span>
              </div>
            </div>
            <div class="svc-card__footer">
              <a href="/services/aviation/" class="svc-card__stretched-link"><span data-i18n="service_learn">Learn More</span> <span aria-hidden="true">→</span></a>
              <a href="/contact.html?service=aviation" class="btn btn-primary btn-sm" data-i18n="get_quote">Get Quote</a>
            </div>
          </article>
''' % dict(alt=ALT_EN, desc=NEW['service_aviation_desc_home'][0])

CSS = '''
/* Aviation card: spans the last row of the homepage services grid */
.svc-card--wide { grid-column: 1 / -1; display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); grid-template-rows: 1fr auto; }
.svc-card--wide .svc-card__img-wrap { grid-row: 1 / 3; }
.svc-card--wide .svc-card__img-wrap { position: relative; overflow: hidden; }
.svc-card--wide .svc-card__img-wrap picture { display: block; height: 100%; }
.svc-card--wide .svc-card__img { height: 100%; min-height: 260px; }
@media (max-width: 768px) { .svc-card--wide { display: flex; flex-direction: column; } .svc-card--wide .svc-card__img-wrap picture { height: auto; } .svc-card--wide .svc-card__img { height: 200px; min-height: 0; } }
'''


def main():
    # translations
    for name, idx in (('ar.json', 1), ('en.json', 0)):
        p = ROOT / 'assets/translations' / name
        raw = p.read_text('utf-8')
        d = json.loads(raw)
        for k, v in NEW.items():
            d[k] = v[idx].replace('&amp;', '&') if idx == 0 else v[idx]
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else ''), encoding='utf-8', newline='')

    # homepage: append the card as the last one in the grid
    p = ROOT / 'index.html'
    s = p.read_text('utf-8')
    crlf = '\r\n' in s
    t = s.replace('\r\n', '\n')
    if 'svc-card--wide' not in t:
        g = t.index('<div class="services-grid">')
        end = t.index('</section>', g)
        k = t.rindex('</article>', g, end) + len('</article>')
        t = t[:k] + '\n' + CARD.rstrip('\n') + t[k:]
        p.write_text(t.replace('\n', '\r\n') if crlf else t, encoding='utf-8', newline='')

    # services.html: add the photo to the Aviation section
    p = ROOT / 'services.html'
    s = p.read_text('utf-8')
    crlf = '\r\n' in s
    t = s.replace('\r\n', '\n')
    if 'aviation-solutions' not in t:
        old = '''        <div class="service-detail__inner" style="grid-template-columns:1fr;">
          <div class="service-detail__content">
            <span class="overline" data-i18n="avi_svc_overline">'''
        new = '''        <div class="service-detail__inner">
          <div class="media-fx fx-static">
            <picture>
              <source srcset="/assets/images/services/aviation-solutions.webp" type="image/webp">
              <img src="/assets/images/services/aviation-solutions.jpg" alt="%s" class="service-detail__img" loading="lazy" width="1536" height="1152" decoding="async" data-i18n-alt="avi_alt">
            </picture>
          </div>
          <div class="service-detail__content">
            <span class="overline" data-i18n="avi_svc_overline">''' % ALT_EN
        assert old in t
        t = t.replace(old, new, 1)
        p.write_text(t.replace('\n', '\r\n') if crlf else t, encoding='utf-8', newline='')

    # css
    c = ROOT / 'assets/css/styles.css'
    t = c.read_text('utf-8')
    if 'svc-card--wide' not in t:
        nl = '\r\n' if '\r\n' in t else '\n'
        c.write_text(t.rstrip() + nl + CSS.replace('\n', nl), encoding='utf-8', newline='')
    print('ok')


if __name__ == '__main__':
    main()
