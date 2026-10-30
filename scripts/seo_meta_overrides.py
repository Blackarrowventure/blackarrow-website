#!/usr/bin/env python3
"""Search-result titles and descriptions picked from Google Search Console data.

Pages listed here rank on Google's first page but got few clicks (Oct 2026: e.g. the MDB/SMDB/DB
article, 4,000+ impressions at position 6 with a 0.4% click rate), so their <title> and
description are rewritten around what people actually searched for. Runs last in every build
(sync_crm_prices.py calls it) so a regenerated page keeps these; editing a page's text elsewhere
does not change what is set here.

Each entry: path -> (title, description). Titles stay under ~60 characters and descriptions under
~155 so Google shows them whole. Only promise what the page really covers.

Usage: python scripts/seo_meta_overrides.py
"""
import html
import io
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

OVERRIDES = {
    # ---- Black Arrow (main site) ----
    'resources/blog/mdb-smdb-db-electrical-distribution-explained/index.html': (
        'MDB vs SMDB vs DB: Full Forms & Differences | Black Arrow',
        'MDB, SMDB and DB full forms and how power flows from the main board to each circuit, plus the panel sizing mistakes that cause nuisance trips years later.'),
    'ar/resources/blog/mdb-smdb-db-electrical-distribution-explained/index.html': (
        'ما معنى MDB وSMDB وDB؟ الفرق بين لوحات التوزيع | السهم الأسود',
        'معنى MDB وSMDB وDB والفرق بينها: كيف تنتقل الكهرباء من اللوحة الرئيسية إلى كل دائرة نهائية، وأخطاء تحجيم اللوحات التي تسبب الفصل المتكرر بعد سنوات.'),
    'resources/blog/nfpa-99-line-isolation-monitors/index.html': (
        'Line Isolation Monitor: NFPA 99 5 mA Alarm Explained',
        'What a line isolation monitor really measures, why NFPA 99 sets the alarm at 5 mA with a 3.7 mA floor, what a red lamp means, and the test most hospitals skip.'),
    'ar/resources/blog/nfpa-99-line-isolation-monitors/index.html': (
        'جهاز مراقبة العزل LIM: شرح إنذار 5 مللي أمبير في NFPA 99',
        'ماذا يقيس جهاز مراقبة العزل فعلاً، ولماذا يحدد NFPA 99 الإنذار عند 5 مللي أمبير مع حد أدنى 3.7، ومعنى المصباح الأحمر، والاختبار الذي تتجاهله معظم المستشفيات.'),
    'resources/blog/why-hospitals-need-isolated-power-panels/index.html': (
        'Isolated Power Panels in Hospitals: Why ORs Need Them',
        'Why operating rooms and wet procedure areas use isolated power panels: the shock and outage risk they remove, how an IPP works, and when NFPA 99 requires one.'),
    'ar/resources/blog/why-hospitals-need-isolated-power-panels/index.html': (
        'لوحات الطاقة المعزولة في المستشفيات: لماذا تحتاجها غرف العمليات',
        'لماذا تستخدم غرف العمليات والمناطق الرطبة لوحات الطاقة المعزولة: خطر الصعق وانقطاع الكهرباء الذي تمنعه، وكيف تعمل لوحة IPP، ومتى يشترطها NFPA 99.'),

    # ---- Black Arrow 3D ----
    '3d/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/index.html': (
        'Bambu Lab A1 vs A1 mini vs A2L: Differences & Which to Buy',
        'A2L vs A1 vs A1 mini side by side: build size, speed, multicolor AMS options and who each one suits, so you buy the right Bambu Lab printer the first time.'),
    '3d/ar/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/index.html': (
        'بامبو لاب A1 أو A1 ميني أو A2L: ما الفرق وأيها تشتري؟',
        'مقارنة A2L وA1 وA1 ميني جنباً إلى جنب: حجم الطباعة والسرعة وخيارات الألوان المتعددة AMS ولمن تناسب كل طابعة، لتختار طابعة بامبو لاب الصحيحة من أول مرة.'),
    '3d/blog/best-3d-printer-for-beginners-saudi-arabia/index.html': (
        'Best 3D Printer for Beginners in Saudi Arabia: 2026 Top Picks',
        'Buying your first 3D printer in Saudi Arabia? Our top pick for complete beginners, the best value alternative, and when a combo bundle is worth the extra.'),
    '3d/ar/blog/best-3d-printer-for-beginners-saudi-arabia/index.html': (
        'أفضل طابعة 3D للمبتدئين في السعودية 2026: اختياراتنا',
        'تشتري أول طابعة ثلاثية الأبعاد في السعودية؟ أفضل طابعة للمبتدئين تماماً، والبديل الأوفر سعراً، ومتى تستحق باقة الكومبو الإضافة.'),
    '3d/blog/bambu-lab-a1-mini-setup-guide/index.html': (
        'Bambu Lab A1 mini Setup: 7 Steps to Your First Print',
        'Set up a Bambu Lab A1 or A1 mini in 7 steps: unboxing, assembly, first calibration, Wi-Fi and the Bambu Handy app, loading filament and your first print.'),
    '3d/ar/blog/bambu-lab-a1-mini-setup-guide/index.html': (
        'تشغيل بامبو لاب A1 ميني: 7 خطوات لأول طباعة',
        'جهّز طابعة بامبو لاب A1 أو A1 ميني في 7 خطوات: فتح الصندوق والتركيب والمعايرة الأولى والواي فاي وتطبيق Bambu Handy وتركيب الفلمنت وأول طباعة.'),
    '3d/blog/where-to-buy-3d-printer-saudi-arabia/index.html': (
        'Where to Buy a 3D Printer in KSA: Local, Online or Import?',
        'Local store, Amazon/Noon or overseas? Where to buy a 3D printer in Saudi Arabia, and what to check on stock, plug, warranty and delivery before you pay.'),
    '3d/3d-printing-service-saudi-arabia/index.html': (
        '3D Printing Service in Saudi Arabia: Riyadh, Jeddah, Dammam',
        'Custom 3D printing anywhere in Saudi Arabia: send a file, a MakerWorld link or just an idea. Get a quote online or on WhatsApp, delivered to your door.'),
    '3d/ar/3d-printing-service-saudi-arabia/index.html': (
        'خدمة الطباعة ثلاثية الأبعاد في السعودية: الرياض وجدة والدمام',
        'طباعة ثلاثية الأبعاد حسب الطلب في كل السعودية: أرسل ملفك أو رابط MakerWorld أو فكرتك فقط، واحصل على عرض سعر أونلاين أو عبر واتساب مع التوصيل لباب بيتك.'),
}


def set_meta(text, title, desc):
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    text = re.sub(r'<title>[^<]*</title>', '<title>' + t + '</title>', text, count=1)
    for attr, key, val in (('name', 'description', d), ('property', 'og:title', t), ('property', 'og:description', d),
                           ('name', 'twitter:title', t), ('name', 'twitter:description', d)):
        text = re.sub(r'(<meta ' + attr + r'="' + re.escape(key) + r'" content=")[^"]*(")',
                      lambda m: m.group(1) + val + m.group(2), text, count=1)
    return text


def main():
    changed = 0
    for rel, (title, desc) in OVERRIDES.items():
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            print('missing:', rel)
            continue
        with io.open(path, encoding='utf-8', newline='') as f:
            old = f.read()
        new = set_meta(old, title, desc)
        if new != old:
            with io.open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(new)
            changed += 1
    print('seo_meta_overrides:', changed, 'pages updated of', len(OVERRIDES))


if __name__ == '__main__':
    main()
