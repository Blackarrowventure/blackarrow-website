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
        'The best first 3D printer in Saudi Arabia by budget: A1 mini Combo, SparkX i7, A2L or an enclosed printer. Prices in SAR and what else to buy.'),
    '3d/ar/blog/best-3d-printer-for-beginners-saudi-arabia/index.html': (
        'أفضل طابعة 3D للمبتدئين في السعودية 2026: اختياراتنا',
        'أفضل طابعة ثلاثية الأبعاد أولى في السعودية حسب الميزانية: A1 ميني كومبو أو SparkX i7 أو A2L أو طابعة مغلقة، مع الأسعار بالريال وماذا تشتري معها.'),
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

    # ---- Audit 4 Nov 2026: descriptions over ~160 characters and Arabic titles over ~60 were cut off in Google ----
    '3d/blog/3d-print-bed-adhesion-first-layer/index.html': (
        'First Layer Not Sticking? Fix Bed Adhesion | Black Arrow 3D',
        'Prints coming loose, corners lifting or spaghetti on the bed? Fix bed adhesion with a clean plate, the right first layer, bed temperature and brims.'),
    '3d/blog/3d-printer-filament-price-saudi-arabia/index.html': (
        '3D Printer Filament Price in Saudi Arabia 2026 | Black Arrow 3D',
        'What 3D printer filament costs in Saudi Arabia in 2026: PLA, PLA+ and PETG prices per kg in SAR, the cost of any print, and how to spend less.'),
    '3d/blog/bambu-a1-hotend-replacement-guide/index.html': (
        'Bambu A1 / A1 mini Hot End and Nozzle Guide | Black Arrow 3D',
        'When to replace the Bambu Lab A1 or A1 mini hot end, how the tool-free swap works, and which nozzle to choose: 0.2, 0.4, 0.6 or 0.8 mm.'),
    '3d/blog/bambu-lab-a2l-combo-guide-saudi/index.html': (
        'Bambu Lab A2L Combo Guide and Price in KSA | Black Arrow 3D',
        'Bambu Lab A2L Combo in Saudi Arabia: 330 x 320 x 325 mm build volume with AMS lite, what it prints, how it compares with the A1 and P2S, and who it suits.'),
    '3d/blog/bambu-lab-h3c-tool-changer-saudi-arabia/index.html': (
        'Bambu Lab H3C Specs and Price in Saudi Arabia | Black Arrow 3D',
        'Bambu Lab H3C: 9 PrintTools, 6-second material switch, AMS 3H drying at 85 °C, full specs, vs H2C, H2D and Snapmaker U1, and its Saudi price.'),
    '3d/ar/blog/bambu-lab-h3c-tool-changer-saudi-arabia/index.html': (
        'مواصفات وسعر بامبو لاب H3C في السعودية | Black Arrow 3D',
        'بامبو لاب H3C: تسع أدوات طباعة، وتبديل المادة في 6 ثوانٍ، وAMS 3H بتجفيف حتى 85 درجة، والمواصفات كاملة، ومقارنتها بـ H2C وH2D، وسعرها في السعودية.'),
    '3d/blog/bambu-lab-printers-saudi-arabia-prices/index.html': (
        'Bambu Lab Printer Prices in Saudi Arabia | Black Arrow 3D',
        'Bambu Lab printer prices in Saudi Arabia, from the A1 mini to the H2C and the new H3C: current SAR prices, stock, who each suits, and combo vs standalone.'),
    '3d/ar/blog/bambu-lab-printers-saudi-arabia-prices/index.html': (
        'أسعار طابعات Bambu Lab في السعودية | Black Arrow 3D',
        'أسعار طابعات Bambu Lab في السعودية من A1 mini إلى H2C وH3C الجديدة: الأسعار الحالية بالريال والمخزون، ولمن تناسب كل طابعة، والكومبو أم المنفردة.'),
    '3d/blog/best-filament-for-bambu-lab-a1-ams-lite/index.html': (
        'Best Filament for Bambu Lab A1 and AMS lite | Black Arrow 3D',
        'The right filament for the Bambu Lab A1, A1 mini and A2L with AMS lite: PLA, PLA+ and PETG settings, what not to load, spool tips and multicolour advice.'),
    '3d/blog/clogged-3d-printer-nozzle-fix/index.html': (
        'How to Fix a Clogged 3D Printer Nozzle | Black Arrow 3D',
        'No filament coming out or a clicking extruder? Clear a clogged 3D printer nozzle with a cold pull, know when to replace the hot end, and prevent clogs.'),
    '3d/blog/kingroon-filament-pla-vs-petg-vs-petg-hs/index.html': (
        'KINGROON PLA vs PETG vs PETG HS Filament (KSA) | Black Arrow 3D',
        'Which KINGROON filament to buy in Saudi Arabia: PLA Basic, PETG Basic or PETG HS. Official settings, heat resistance, finish, colours and price.'),
    '3d/ar/blog/kingroon-filament-pla-vs-petg-vs-petg-hs/index.html': (
        'فيلامنت KINGROON: PLA أم PETG أم PETG HS؟ | Black Arrow 3D',
        'أي فيلامنت KINGROON تشتري في السعودية: PLA Basic أم PETG Basic أم PETG HS. الإعدادات الرسمية ومقاومة الحرارة والسطح والألوان الجديدة والسعر.'),
    '3d/blog/kingroon-petg-basic-filament-guide/index.html': (
        'KINGROON PETG Basic Filament Guide (KSA) | Black Arrow 3D',
        'KINGROON PETG Basic 1.75 mm, 1 kg in Saudi Arabia: when PETG beats PLA, settings for Bambu Lab printers, stringing fixes, drying and best uses.'),
    '3d/ar/blog/kingroon-petg-basic-filament-guide/index.html': (
        'دليل فلمنت KINGROON PETG Basic في السعودية | Black Arrow 3D',
        'فلمنت KINGROON PETG Basic بقطر 1.75 مم ووزن 1 كجم: متى يتفوق PETG على PLA، وإعدادات طابعات بامبو لاب، وحل مشكلة الخيوط، والتجفيف، وأفضل الاستخدامات.'),
    '3d/blog/kingroon-petg-hs-high-speed-filament-guide/index.html': (
        'KINGROON PETG HS High-Speed Filament (KSA) | Black Arrow 3D',
        'KINGROON PETG HS in Saudi Arabia: official settings, up to 2x the speed of standard PETG, matte finish, heat resistance, drying, colours and cost.'),
    '3d/ar/blog/kingroon-petg-hs-high-speed-filament-guide/index.html': (
        'فيلامنت KINGROON PETG HS عالي السرعة | Black Arrow 3D',
        'فيلامنت KINGROON PETG HS في السعودية: الإعدادات الرسمية، وسرعة تصل إلى ضعف PETG العادي، ولمسة مطفية، ومقاومة الحرارة، والتجفيف والألوان والتكلفة.'),
    '3d/blog/pla-vs-pla-plus-difference/index.html': (
        'PLA vs PLA+ Filament: The Real Difference | Black Arrow 3D',
        'PLA vs PLA+: what the plus really means for toughness, print temperature, finish and price, and which to buy for gifts, functional parts and beginners.'),
    '3d/business/index.html': (
        'Corporate Gifts & Bulk 3D Printing in Saudi Arabia | Black Arrow',
        'Bulk 3D printing for companies, events and schools in Saudi Arabia: logo keychains, corporate gifts, National Day giveaways and trophies. Quote on WhatsApp.'),
    '3d/ar/blog/3d-printer-filament-price-saudi-arabia/index.html': (
        'أسعار فلمنت الطباعة 3D في السعودية 2026 | Black Arrow 3D',
        'كم سعر فلمنت الطابعة ثلاثية الأبعاد في السعودية 2026: أسعار PLA وPLA+ وPETG للكيلو بالريال، وطريقة حساب تكلفة أي طبعة، وكيف تنفق أقل على الفلمنت.'),
    '3d/ar/blog/bambu-lab-a1-mini-combo-review/index.html': (
        'مراجعة Bambu Lab A1 Mini Combo وسعرها بالسعودية | Black Arrow 3D',
        'مراجعة Bambu Lab A1 mini Combo: السعر في السعودية، ماذا تتضمن باقة AMS lite، المواصفات الكاملة، لمن تناسب، ومقارنتها بـ Snapmaker U1.'),
    '3d/ar/blog/buy-3d-printer-jubail/index.html': (
        'طابعات 3D في الجبيل: الأسعار والتوصيل | Black Arrow 3D',
        'طابعات ثلاثية الأبعاد في الجبيل والأحساء: طباعة أدوات التثبيت والنماذج في رطوبة الساحل، وطابعات مغلقة للخامات الهندسية، والأسعار الحالية والتوصيل.'),
    '3d/ar/blog/buy-3d-printer-makkah/index.html': (
        'طابعات 3D في مكة المكرمة: الأسعار والتوصيل | Black Arrow 3D',
        'طابعات ثلاثية الأبعاد في مكة المكرمة: الطباعة في الغرف الحارة، والطابعة المناسبة للطلاب وصنّاع الهدايا، والأسعار الحالية بالريال، والتوصيل وطرق الدفع.'),
    '3d/ar/blog/buy-3d-printer-qassim/index.html': (
        'طابعات 3D في القصيم: الأسعار والتوصيل | Black Arrow 3D',
        'تبحث عن طابعة ثلاثية الأبعاد في بريدة أو عنيزة؟ الطباعة في صيف القصيم الحار وشتائه البارد، وطابعات للطلاب والمزارع، والأسعار والتوصيل في السعودية.'),
    '3d/ar/blog/buy-3d-printer-riyadh/index.html': (
        'طابعات 3D في الرياض: الأسعار والتوصيل | Black Arrow 3D',
        'تبحث عن طابعة ثلاثية الأبعاد في الرياض؟ الأسعار الحالية بالريال، والطابعة المناسبة للحرارة والغبار، ونصائح الفلمنت، والتوصيل وطرق الدفع في السعودية.'),
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
