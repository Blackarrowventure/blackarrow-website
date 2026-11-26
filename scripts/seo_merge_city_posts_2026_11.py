"""Merge the nine city guides into the "Where to buy a 3D printer in Saudi Arabia" guide (26 Nov 2026).

Why: the city posts (buy-3d-printer-<city>, EN + AR) repeated the same delivery terms and printer advice,
so Google treated them as near-duplicates. They competed with each other and with the shop's 3D printers page
for "3D printer KSA / Saudi Arabia". The where-to-buy guide already ranked best of them, so it becomes the one
page for "buy a 3D printer in <city>" searches.

What this does (run once from the repo root, then the usual build chain from generate_3d_static.py on):
  1. adds a "Buying a 3D printer in your city" section (one anchored part per city: the climate tips that were
     unique to each city post) plus a delivery FAQ to the EN and AR guide;
  2. swaps the guide's "Related" links to the city posts for the 3D printers page and the printing service page;
  3. points every link to a city post at the matching #city-<slug> section of the guide;
  4. adds permanent redirects for the old URLs to vercel.json and deletes the old pages.
The source copy for the city posts stays in scripts/seo_posts_cities.py for reference; it is no longer built.
"""
import json
import os
import re
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUB = 'where-to-buy-3d-printer-saudi-arabia'
CITIES = ['riyadh', 'jeddah', 'dammam-khobar', 'jubail', 'makkah', 'madinah', 'qassim', 'abha-khamis-mushait', 'tabuk']

EN_SECTION = '''
          <h2 id="by-city">Buying a 3D printer in your city</h2>
          <p>Delivery works the same everywhere in the Kingdom. We ship from Dammam: in-stock items ordered before 4&nbsp;pm (Saudi time), Sunday to Thursday, leave the same day, otherwise the next business day. Standard delivery takes 4–5 business days (30&nbsp;SAR) and fast delivery 2–3 business days (50&nbsp;SAR), with a tracking number. Regular delivery is free on every order with a 3D printer, on 100&nbsp;SAR or more of 3D printed items, on any order from 500&nbsp;SAR, and on standard delivery to Dammam and Khobar.</p>
          <p>What changes from city to city is the climate, and that affects which printer and filament work best:</p>
          <p class="b3d-city-jump"><a href="#city-riyadh">Riyadh</a> · <a href="#city-jeddah">Jeddah</a> · <a href="#city-dammam-khobar">Dammam &amp; Khobar</a> · <a href="#city-jubail">Jubail &amp; Al Ahsa</a> · <a href="#city-makkah">Makkah</a> · <a href="#city-madinah">Madinah</a> · <a href="#city-qassim">Qassim</a> · <a href="#city-abha-khamis-mushait">Abha &amp; Khamis Mushait</a> · <a href="#city-tabuk">Tabuk</a></p>

          <h3 id="city-riyadh">Riyadh</h3>
          <p>Riyadh’s air is dry for most of the year, so opened PLA and PETG stay printable for longer than on the coast. The challenges are heat, dust and air conditioning. PLA softens at around 55–60&nbsp;°C, so never leave prints or spools in a parked car. Wipe the build plate with isopropyl alcohol and keep the printer covered against fine dust, and turn it away from AC vents, which can lift the corners of large prints. An enclosed printer such as the <a href="/3d/product/elegoo-centauri-carbon-2/">Elegoo Centauri Carbon 2</a> or <a href="/3d/product/bambu-lab-p2s/">Bambu Lab P2S</a> handles both dust and drafts.</p>

          <h3 id="city-jeddah">Jeddah</h3>
          <p>Jeddah is warm and humid for most of the year, and filament pulls moisture out of the air: an open spool of PLA can start printing badly within days, and PETG and TPU absorb water even faster. Keep spools you are not using sealed with fresh desiccant, print in an air-conditioned room, and dry filament that has been open for a while: PLA at 45–55&nbsp;°C for 4–6 hours, PETG at 60–65&nbsp;°C for 6–8 hours. The <a href="/3d/product/bambu-ams-2-pro/">AMS 2 Pro</a> dries filament at up to 65&nbsp;°C. We deliver to every part of Jeddah, including Obhur and the southern districts.</p>

          <h3 id="city-dammam-khobar">Dammam, Khobar and Dhahran</h3>
          <p>Summer on the Gulf coast brings some of the most humid air in the Kingdom. Keep opened spools sealed with desiccant, dry them before long prints, and keep the printer in an air-conditioned room; garages and balconies are the worst places in summer. We are based in Dammam, so standard delivery to Dammam and Khobar is free.</p>

          <h3 id="city-jubail">Jubail and Al Ahsa</h3>
          <p>Jubail shares the Eastern Province’s humid summers. For functional parts, PETG is the best everyday material: tougher and more heat resistant than PLA, and easy to print, but dry it at 60–65&nbsp;°C for 6–8 hours if it has been open for a while. ABS and ASA need an enclosed printer, and nylon or carbon-filled filaments need a hardened steel nozzle and a dry box. Printed parts are for prototypes and tooling aids, never for pressure, lifting or safety-critical service.</p>

          <h3 id="city-makkah">Makkah</h3>
          <p>Makkah is hot for most of the year. In a room without air conditioning, PLA can soften inside the hot end before it reaches the nozzle (heat creep) and cause clogs, so keep the printer in a cool room, and when printing PLA on an enclosed printer, open the door or lid. Keep the printer and spools away from sunny windows, and store opened spools sealed, because the air can feel humid on some days.</p>

          <h3 id="city-madinah">Madinah</h3>
          <p>Madinah is inland and mostly dry, so opened filament lasts well. The first layer is the sensitive part: a print that sticks on a warm afternoon can lift at the corners on a cool winter night or under a cold AC. Clean the plate, add a brim to large flat parts and keep the printer out of direct airflow. Our <a href="/3d/blog/3d-print-bed-adhesion-first-layer/">bed adhesion guide</a> covers the details.</p>

          <h3 id="city-qassim">Qassim: Buraidah and Unaizah</h3>
          <p>Qassim is dry all year, which is good for filament; the challenge is temperature. In summer, keep the printer in a cooled room so PLA does not soften in the hot end. In winter, print in a room that stays warm, because cold drafts make large parts lift and PETG and ABS crack between layers. Wipe the plate with isopropyl alcohol and keep the printer covered against dust. For farm and workshop parts that sit outdoors, use PETG rather than PLA.</p>

          <h3 id="city-abha-khamis-mushait">Abha and Khamis Mushait</h3>
          <p>In the Asir highlands, summers are mild, winters are cool, and fog and rain bring humid spells. A cool breeze from an open window is the main cause of warped corners and cracked layers, especially with PETG and ABS, so close nearby windows while printing or use an enclosed printer. Store spools sealed with desiccant, and dry them if prints start to string or pop.</p>

          <h3 id="city-tabuk">Tabuk</h3>
          <p>Tabuk is dry, with hot summers and genuinely cold winters. Dry air keeps filament in good shape, but cold rooms make corners lift and layers split: PLA is the most forgiving, PETG needs a warm, draft-free room, and ABS and ASA need an enclosure. A spool kept in a cold storeroom can snap as it feeds, so let it warm to room temperature before loading it, and do not point a heater or AC at the printer.</p>
'''

AR_SECTION = '''
          <h2 id="by-city">شراء طابعة ثلاثية الأبعاد في مدينتك</h2>
          <p>التوصيل واحد في كل مناطق المملكة. نشحن من الدمام: المنتجات المتوفرة المطلوبة قبل الساعة 4 مساءً بتوقيت السعودية، من الأحد إلى الخميس، تُشحن في اليوم نفسه، وإلا ففي يوم العمل التالي. التوصيل العادي 4–5 أيام عمل (30 ريال) والسريع 2–3 أيام عمل (50 ريال)، مع رقم تتبع. والتوصيل العادي مجاني لكل طلب فيه طابعة ثلاثية الأبعاد، ولمنتجات مطبوعة بقيمة 100 ريال أو أكثر، ولأي طلب من 500 ريال، وللتوصيل العادي إلى الدمام والخبر.</p>
          <p>ما يختلف من مدينة إلى أخرى هو المناخ، وهو ما يحدد الطابعة والفلمنت الأنسب:</p>
          <p class="b3d-city-jump"><a href="#city-riyadh">الرياض</a> · <a href="#city-jeddah">جدة</a> · <a href="#city-dammam-khobar">الدمام والخبر</a> · <a href="#city-jubail">الجبيل والأحساء</a> · <a href="#city-makkah">مكة المكرمة</a> · <a href="#city-madinah">المدينة المنورة</a> · <a href="#city-qassim">القصيم</a> · <a href="#city-abha-khamis-mushait">أبها وخميس مشيط</a> · <a href="#city-tabuk">تبوك</a></p>

          <h3 id="city-riyadh">الرياض</h3>
          <p>هواء الرياض جاف معظم السنة، لذلك تبقى بكرات PLA وPETG المفتوحة صالحة للطباعة مدة أطول مما هي على الساحل. أما التحديات فهي الحرارة والغبار والمكيّف. يلين PLA عند نحو 55–60 درجة مئوية، فلا تترك القطع المطبوعة أو البكرات في سيارة متوقفة. امسح سرير الطباعة بالكحول الأيزوبروبيلي وغطِّ الطابعة من الغبار الناعم، وأبعدها عن فتحات المكيّف لأن تيار الهواء البارد قد يرفع زوايا القطع الكبيرة. والطابعة المغلقة مثل <a href="/3d/ar/product/elegoo-centauri-carbon-2/">Elegoo Centauri Carbon 2</a> أو <a href="/3d/ar/product/bambu-lab-p2s/">Bambu Lab P2S</a> تتعامل مع الغبار وتيارات الهواء معاً.</p>

          <h3 id="city-jeddah">جدة</h3>
          <p>جدة دافئة ورطبة معظم السنة، والفلمنت يمتص الرطوبة من الهواء: قد تبدأ بكرة PLA المفتوحة بالطباعة بشكل سيئ خلال أيام، ويمتص PETG وTPU الماء أسرع. احفظ البكرات غير المستخدمة في كيس محكم مع مادة مجففة جديدة، واطبع في غرفة مكيّفة، وجفّف الفلمنت المفتوح منذ مدة: PLA على 45–55 درجة مئوية لمدة 4–6 ساعات، وPETG على 60–65 درجة لمدة 6–8 ساعات. ويجفف <a href="/3d/ar/product/bambu-ams-2-pro/">AMS 2 Pro</a> الفلمنت حتى 65 درجة مئوية. ونوصّل إلى كل أحياء جدة، ومنها أبحر والأحياء الجنوبية.</p>

          <h3 id="city-dammam-khobar">الدمام والخبر والظهران</h3>
          <p>صيف الساحل الشرقي من أكثر الأجواء رطوبة في المملكة. احفظ البكرات المفتوحة مع مادة مجففة، وجفّفها قبل الطباعات الطويلة، وضع الطابعة في غرفة مكيّفة؛ فالكراج والبلكونة أسوأ مكان لها في الصيف. مقرنا في الدمام، لذلك التوصيل العادي إلى الدمام والخبر مجاني.</p>

          <h3 id="city-jubail">الجبيل والأحساء</h3>
          <p>تشارك الجبيل المنطقة الشرقية صيفها الرطب. للقطع العملية، PETG هي الخامة اليومية الأفضل: أقوى من PLA وأكثر تحملاً للحرارة وسهلة الطباعة، لكن جفّفها على 60–65 درجة مئوية لمدة 6–8 ساعات إذا كانت مفتوحة منذ مدة. تحتاج ABS وASA إلى طابعة مغلقة، ويحتاج النايلون والخامات المدعّمة بألياف الكربون إلى فوهة فولاذية مقسّاة وصندوق تجفيف. والقطع المطبوعة للنماذج الأولية وأدوات المساعدة فقط، وليست للضغط أو الرفع أو الاستخدامات المتعلقة بالسلامة.</p>

          <h3 id="city-makkah">مكة المكرمة</h3>
          <p>مكة حارة معظم السنة. في غرفة غير مكيّفة قد يلين PLA داخل الهوت إند قبل وصوله إلى الفوهة (ما يسمى heat creep) فيسبب انسداداً، لذلك ضع الطابعة في غرفة باردة، وعند طباعة PLA على طابعة مغلقة افتح الباب أو الغطاء. أبعد الطابعة والبكرات عن النوافذ المشمسة، واحفظ البكرات المفتوحة في كيس محكم لأن الجو قد يكون رطباً في بعض الأيام.</p>

          <h3 id="city-madinah">المدينة المنورة</h3>
          <p>المدينة المنورة داخلية وجافة في الغالب، لذلك يدوم الفلمنت المفتوح جيداً. الطبقة الأولى هي الجزء الحساس: قطعة تلتصق جيداً في عصر دافئ قد ترتفع زواياها في ليلة شتوية باردة أو تحت مكيّف بارد. نظّف السرير وأضف حافة (brim) للقطع المسطحة الكبيرة وأبعد الطابعة عن تيار الهواء المباشر. ويشرح <a href="/3d/ar/blog/3d-print-bed-adhesion-first-layer/">دليل التصاق الطبقة الأولى</a> التفاصيل.</p>

          <h3 id="city-qassim">القصيم: بريدة وعنيزة</h3>
          <p>القصيم جافة طوال السنة، وهذا جيد للفلمنت؛ أما التحدي فهو الحرارة. في الصيف ضع الطابعة في غرفة مكيّفة حتى لا يلين PLA في الهوت إند. وفي الشتاء اطبع في غرفة تبقى دافئة، لأن تيارات الهواء الباردة ترفع القطع الكبيرة وتشقق طبقات PETG وABS. امسح السرير بالكحول الأيزوبروبيلي وغطِّ الطابعة من الغبار. وللقطع التي تبقى في الخارج في المزارع والورش استخدم PETG بدل PLA.</p>

          <h3 id="city-abha-khamis-mushait">أبها وخميس مشيط</h3>
          <p>في مرتفعات عسير الصيف معتدل والشتاء بارد، والضباب والأمطار تجلب فترات رطبة. نسمة باردة من نافذة مفتوحة هي السبب الرئيسي لالتواء الزوايا وتشقق الطبقات، خاصة مع PETG وABS، لذلك أغلق النوافذ القريبة أثناء الطباعة أو استخدم طابعة مغلقة. احفظ البكرات مع مادة مجففة، وجفّفها إذا بدأت الطباعة تُخرج خيوطاً أو أصوات فرقعة.</p>

          <h3 id="city-tabuk">تبوك</h3>
          <p>تبوك جافة، صيفها حار وشتاؤها بارد فعلاً. الهواء الجاف يحفظ الفلمنت، لكن الغرف الباردة ترفع الزوايا وتشقق الطبقات: PLA الأكثر تسامحاً، وPETG يحتاج غرفة دافئة بلا تيارات هواء، وABS وASA تحتاجان طابعة مغلقة. البكرة المحفوظة في مخزن بارد قد تنكسر أثناء التغذية، فاتركها تصل إلى حرارة الغرفة قبل تركيبها، ولا توجّه مدفأة أو مكيّفاً نحو الطابعة.</p>
'''

EN_FAQ = ('          <h3>How long does delivery take to Riyadh, Jeddah or my city?</h3>\n'
          '          <p>The same everywhere in Saudi Arabia: standard delivery takes 4–5 business days (30&nbsp;SAR, free with any 3D printer) and fast delivery 2–3 business days (50&nbsp;SAR), shipped from our base in Dammam. See <a href="#by-city">buying a 3D printer in your city</a> for local tips.</p>\n')
AR_FAQ = ('          <h3>كم يستغرق التوصيل إلى الرياض أو جدة أو مدينتي؟</h3>\n'
          '          <p>المدة نفسها في كل السعودية: التوصيل العادي 4–5 أيام عمل (30 ريال، ومجاني مع أي طابعة ثلاثية الأبعاد) والسريع 2–3 أيام عمل (50 ريال)، من مقرنا في الدمام. وانظر <a href="#by-city">شراء طابعة ثلاثية الأبعاد في مدينتك</a> لنصائح كل مدينة.</p>\n')

EN_RELATED_OLD = ('            <a href="/3d/blog/buy-3d-printer-riyadh/">Buying a 3D printer in Riyadh</a>\n'
                  '            <a href="/3d/blog/buy-3d-printer-jeddah/">Buying a 3D printer in Jeddah</a>\n')
EN_RELATED_NEW = ('            <a href="/3d/shop/3d-printers/">3D printers in Saudi Arabia: all models and prices</a>\n'
                  '            <a href="/3d/3d-printing-service-saudi-arabia/">3D printing service in Saudi Arabia</a>\n')
AR_RELATED_OLD = ('            <a href="/3d/ar/blog/buy-3d-printer-riyadh/">شراء طابعة ثلاثية الأبعاد في الرياض</a>\n'
                  '            <a href="/3d/ar/blog/buy-3d-printer-jeddah/">شراء طابعة ثلاثية الأبعاد في جدة</a>\n')
AR_RELATED_NEW = ('            <a href="/3d/ar/shop/3d-printers/">الطابعات ثلاثية الأبعاد في السعودية: كل الموديلات والأسعار</a>\n'
                  '            <a href="/3d/ar/3d-printing-service-saudi-arabia/">خدمة الطباعة ثلاثية الأبعاد في السعودية</a>\n')

CITY_RX = re.compile(r'/3d/(ar/)?blog/buy-3d-printer-(' + '|'.join(CITIES) + r')/')


def rd(p):
    with open(os.path.join(ROOT, p), encoding='utf-8', newline='') as f:
        return f.read()


def wr(p, s):
    with open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def nl(s, ref):
    """Match the target file's line endings."""
    return s.replace('\n', '\r\n') if '\r\n' in ref else s


def merge_hub(lang):
    p = ('3d/ar/blog/' if lang == 'ar' else '3d/blog/') + HUB + '/index.html'
    s = rd(p)
    if 'id="by-city"' in s:
        return p + ': already merged'
    sec, faq, old, new = (AR_SECTION, AR_FAQ, AR_RELATED_OLD, AR_RELATED_NEW) if lang == 'ar' else (EN_SECTION, EN_FAQ, EN_RELATED_OLD, EN_RELATED_NEW)
    anchor = '<h2>أين يقع Black Arrow 3D بين هذه الخيارات</h2>' if lang == 'ar' else '<h2>Where Black Arrow 3D fits</h2>'
    i = s.index(anchor)
    i = s.rindex('\n', 0, i) + 1
    s = s[:i] + nl(sec.lstrip('\n') + '\n', s) + s[i:]
    # delivery question goes last in the FAQ, just before the CTA box
    j = s.index('<div class="b3d-article__cta">', s.index('<h2>' + ('الأسئلة الشائعة' if lang == 'ar' else 'Frequently asked questions') + '</h2>'))
    j = s.rindex('\n', 0, j)
    j = s.rindex('\n', 0, j) + 1  # before the blank line above the CTA
    s = s[:j] + nl(faq, s) + s[j:]
    assert nl(old, s) in s, p + ': related links not found'
    s = s.replace(nl(old, s), nl(new, s))
    wr(p, s)
    return p + ': merged'


def relink():
    """Every remaining link to a city post goes to that city's section of the guide."""
    files = subprocess.run(['git', 'ls-files', '*.html', '*.txt', '*.py'], cwd=ROOT, capture_output=True, text=True).stdout.split()
    skip = {'scripts/seo_posts_cities.py', 'scripts/seo_merge_city_posts_2026_11.py', 'scripts/seo_meta_overrides.py'}
    changed = []
    for p in files:
        if p in skip or re.match(r'3d/(ar/)?blog/buy-3d-printer-(' + '|'.join(CITIES) + r')/', p):
            continue
        s = rd(p)
        t = CITY_RX.sub(lambda m: '/3d/' + (m.group(1) or '') + 'blog/' + HUB + '/#city-' + m.group(2), s)
        if t != s:
            wr(p, t)
            changed.append(p)
    return changed


def drop_index_cards():
    """Remove the city cards from both blog index pages."""
    out = []
    for p in ('3d/blog/index.html', '3d/ar/blog/index.html'):
        s = rd(p)
        t = re.sub(r'[ \t]*<article class="b3d-blog-card">\s*<a class="b3d-card__stretched-link" href="/3d/(?:ar/)?blog/'
                   + HUB + r'/#city-[a-z-]+".*?</article>\r?\n', '', s, flags=re.S)
        if t != s:
            wr(p, t)
        out.append(p + ': ' + str(s.count('<article class="b3d-blog-card">') - t.count('<article class="b3d-blog-card">')) + ' cards removed')
    return out


def add_redirects():
    """Insert the redirects as text at the top of the "redirects" list, keeping the file's formatting."""
    p = 'vercel.json'
    s = rd(p)
    have = {r['source'] for r in json.loads(s).get('redirects', [])}
    eol = '\r\n' if '\r\n' in s else '\n'
    items = []
    for c in CITIES:
        for pre in ('/3d/blog/', '/3d/ar/blog/'):
            for src in (pre + 'buy-3d-printer-' + c + '/', pre + 'buy-3d-printer-' + c):
                if src not in have:
                    items.append('    {' + eol + '      "source": "' + src + '",' + eol + '      "destination": "' + pre + HUB + '/",'
                                 + eol + '      "permanent": true' + eol + '    },' + eol)
    key = '"redirects": [' + eol
    s = s.replace(key, key + ''.join(items), 1)
    json.loads(s)  # still valid JSON
    wr(p, s)
    return len(json.loads(s)['redirects'])


def delete_pages():
    gone = []
    for c in CITIES:
        for pre in ('3d/blog/', '3d/ar/blog/'):
            d = os.path.join(ROOT, pre + 'buy-3d-printer-' + c)
            if os.path.isdir(d):
                shutil.rmtree(d)
                gone.append(pre + 'buy-3d-printer-' + c)
    return gone


if __name__ == '__main__':
    print(merge_hub('en'))
    print(merge_hub('ar'))
    print('relinked:', relink())
    print(drop_index_cards())
    print('redirects total:', add_redirects())
    print('deleted:', len(delete_pages()), 'pages')
