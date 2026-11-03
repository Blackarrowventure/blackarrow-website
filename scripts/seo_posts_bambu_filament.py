"""Bilingual (EN + AR) guide to Bambu Lab PLA Basic and PLA Matte filament (November 2026).

Data only, same schema as scripts/seo_posts_products.py. Every spec, setting and material value
is Bambu Lab's own: the product pages on us.store.bambulab.com and the official Technical Data
Sheets V3.0 for PLA Basic and PLA Matte (read 1 Nov 2026). Price, colours, stock and the
Refill status are from the live store (3d/assets/data/3d-products.json). The post points to the
product pages for current stock rather than promising it.
"""

EN_DATE = 'November 1, 2026'
AR_DATE = '1 نوفمبر 2026'

PB = '/3d/product/bambu-lab-pla-basic-filament/'
PM = '/3d/product/bambu-lab-pla-matte-filament/'
PB_AR = '/3d/ar/product/bambu-lab-pla-basic-filament/'
PM_AR = '/3d/ar/product/bambu-lab-pla-matte-filament/'

POSTS = [
    {
        'slug': 'bambu-lab-pla-basic-vs-pla-matte-filament',
        'en': {
            'headline': 'Bambu Lab PLA Basic vs PLA Matte Filament: Settings, Colours, Spool or Refill',
            'title': 'Bambu PLA Basic vs PLA Matte Filament (KSA) | Black Arrow 3D',
            'desc': 'Bambu Lab PLA Basic and PLA Matte in Saudi Arabia: official print settings, RFID and AMS, colours with codes, spool vs refill, heat limits and cost per print.',
            'meta_line': 'Filament guide &middot; ' + EN_DATE + ' &middot; 8 min read',
            'lead': 'Bambu Lab makes its own PLA for its printers and the AMS. PLA Basic is the everyday all-rounder; PLA Matte trades a little strength for a soft, non-glossy finish that hides layer lines. Here is how they differ, the settings Bambu Lab recommends, what the RFID tag does, and whether to buy a spool or a refill.',
            'card': ('Filament guide', '8 min read', 'Bambu PLA Basic or PLA Matte? Official settings, RFID and AMS, colours, spool vs refill and cost per print.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>Pick <a href="''' + PB + '''">Bambu Lab PLA Basic</a> for most prints: toys, gifts, household parts and anything you want bright and a little tougher. Pick <a href="''' + PM + '''">Bambu Lab PLA Matte</a> for display pieces, decor, figures and architectural models, where a smooth non-glossy surface with fewer visible layer lines matters more than strength. Both are 1.75&nbsp;mm, 1&nbsp;kg, print with the same settings, and carry an RFID tag that the AMS reads to set everything up for you. Both are now available at Black Arrow 3D for <strong>140&nbsp;SAR per 1&nbsp;kg</strong>, in limited stock.</p>

          <h2>PLA Basic and PLA Matte side by side</h2>
          <p>All figures below are from Bambu Lab's official technical data sheets (V3.0). They are lab values for comparison; real parts depend on the model and settings.</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA Basic</th><th>PLA Matte</th></tr></thead>
              <tbody>
                <tr><td>Finish</td><td>Smooth surface finish</td><td>Matte, hides layer lines</td></tr>
                <tr><td>Top print speed (Bambu Lab)</td><td>up to 258&nbsp;mm/s*</td><td>up to 270&nbsp;mm/s*</td></tr>
                <tr><td>Tensile strength (X-Y / Z)</td><td>35 / 31&nbsp;MPa</td><td>30 / 22&nbsp;MPa</td></tr>
                <tr><td>Bending strength (X-Y / Z)</td><td>76 / 59&nbsp;MPa</td><td>53 / 29&nbsp;MPa</td></tr>
                <tr><td>Heat deflection (1.8 / 0.45&nbsp;MPa)</td><td>54 / 57&nbsp;°C</td><td>52 / 58&nbsp;°C</td></tr>
                <tr><td>Density</td><td>1.24&nbsp;g/cm³</td><td>1.31&nbsp;g/cm³</td></tr>
                <tr><td>Diameter</td><td colspan="2">1.75&nbsp;mm ± 0.03&nbsp;mm</td></tr>
                <tr><td>Net weight</td><td colspan="2">1&nbsp;kg</td></tr>
                <tr><td>Emissions</td><td colspan="2">UL GREENGUARD certified (UL 2904)</td></tr>
                <tr><td>Odour</td><td colspan="2">Odourless</td></tr>
              </tbody>
            </table>
          </div>
          <p><small>* Bambu Lab's figure with a 0.4&nbsp;mm nozzle, 0.4&nbsp;mm line width and 0.2&nbsp;mm layer height.</small></p>
          <p>The short version: PLA Basic is the stronger of the two, especially between layers (the Z values), so it is the better choice for clips, brackets and anything that takes a load. PLA Matte is about looks.</p>

          <h2>Official print settings</h2>
          <p>On a Bambu Lab printer with an AMS you do not need to type any of this in: the RFID tag on the spool tells the printer and Bambu Studio which filament and colour it is. For other printers, or to check your profile, these are Bambu Lab's recommended settings for both filaments:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Setting</th><th>Bambu Lab recommendation</th></tr></thead>
              <tbody>
                <tr><td>Nozzle temperature</td><td>190–230&nbsp;°C</td></tr>
                <tr><td>Bed temperature</td><td>35–45&nbsp;°C</td></tr>
                <tr><td>Build plate</td><td>Cool Plate, High Temperature Plate or Textured PEI Plate</td></tr>
                <tr><td>Bed preparation</td><td>Glue</td></tr>
                <tr><td>Part cooling fan</td><td>On</td></tr>
                <tr><td>Print speed</td><td>under 300&nbsp;mm/s</td></tr>
                <tr><td>Nozzle sizes</td><td>0.2, 0.4, 0.6 and 0.8&nbsp;mm</td></tr>
                <tr><td>Retraction</td><td>0.6–1.0&nbsp;mm at 20–40&nbsp;mm/s</td></tr>
                <tr><td>Max overhang / bridge</td><td>55° / 30&nbsp;mm</td></tr>
                <tr><td>Supports</td><td>Bambu Support for PLA</td></tr>
              </tbody>
            </table>
          </div>
          <p>Bambu Lab printed its own test pieces at 220&nbsp;°C on a 35&nbsp;°C bed at 200&nbsp;mm/s, a sensible starting point if you are setting up a profile by hand. If the first layer will not stick, clean the plate first; our <a href="/3d/blog/3d-print-bed-adhesion-first-layer/">first-layer guide</a> covers the rest.</p>

          <h2>RFID and the AMS</h2>
          <p>Every Bambu Lab spool has an RFID tag with the print settings stored on it. Load it into any AMS (AMS lite, AMS 2 Pro or AMS HT) and the printer reads the material, colour and settings automatically, so the right profile is used and the slicer shows the right colour. Bambu Lab lists both filaments as <em>All AMS Series Compatible</em>. That is the main reason to buy Bambu filament for a Bambu printer: multi-colour prints just work without setting up each slot. If you are new to multi-colour, read <a href="/3d/blog/multi-color-3d-printing-explained/">multi-colour 3D printing explained</a>.</p>

          <h2>Filament with spool or refill?</h2>
          <p>Bambu Lab sells each colour two ways:</p>
          <ul>
            <li><strong>Filament with spool:</strong> the filament comes wound on Bambu Lab's own spool, ready to load. The spool is ABS, rated to 70&nbsp;°C, 200&nbsp;mm across and 67&nbsp;mm high.</li>
            <li><strong>Refill:</strong> the same filament without a spool. Bambu Lab's own note: <em>the refill needs to be used with a spool.</em> You fit it onto an empty Bambu Lab spool you already have, so there is less plastic to throw away each time.</li>
          </ul>
          <p>If this is your first Bambu Lab filament, buy it <strong>with a spool</strong>. Once you have an empty spool, a refill is the tidier way to buy the next kilo. On our store you choose <em>With spool</em> or <em>Refill</em> under the colour on the <a href="''' + PB + '''">PLA Basic</a> and <a href="''' + PM + '''">PLA Matte</a> pages; refills are listed but not available yet.</p>

          <h2>Colours we are bringing in</h2>
          <p>Bambu Lab gives every colour a code, which is also how Bambu Studio and the AMS name it:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Filament</th><th>Colours (Bambu Lab code)</th></tr></thead>
              <tbody>
                <tr><td>PLA Basic</td><td>Cyan (10603), Blue (10601), Purple (10700), Yellow (10400), Red (10200), Gray (10103), Silver (10102), and Solar Breeze (10901) from the PLA Basic Gradient line</td></tr>
                <tr><td>PLA Matte</td><td>Sakura Pink (11201), Grass Green (11500)</td></tr>
              </tbody>
            </table>
          </div>
          <p>Solar Breeze is a gradient: the colour changes gradually along the filament, so a vase or figure shifts colour from bottom to top without any multi-colour setup.</p>

          <h2>Saudi heat and humidity</h2>
          <p>Both filaments start to soften in the mid-50s&nbsp;°C (heat deflection 54&nbsp;°C for PLA Basic, 52&nbsp;°C for PLA Matte at 1.8&nbsp;MPa). That is fine indoors, but a car in a Saudi summer gets far hotter, so do not leave PLA prints on a dashboard. For car and outdoor parts use PETG; see <a href="/3d/blog/pla-vs-petg-vs-abs-filament-guide/">PLA vs PETG vs ABS</a>.</p>
          <p>Bambu Lab recommends printing and storing these filaments below <strong>20% relative humidity</strong>, sealed with desiccant. In Jeddah, Dammam and Khobar the air is far wetter than that, so keep opened spools in the AMS with fresh desiccant or in a sealed box. If a spool has taken on moisture, Bambu Lab's drying setting is <strong>50&nbsp;°C for 8 hours</strong> in a forced-air drying oven, kept away from the heater. Bambu Lab warns against using a microwave or kitchen oven, which can damage the filament. Our <a href="/3d/blog/3d-printing-filament-saudi-heat-humidity/">heat and humidity guide</a> has more on storage.</p>

          <h2>What a print costs</h2>
          <p>At 140&nbsp;SAR per kilo, Bambu Lab PLA works out to <strong>0.14&nbsp;SAR per gram</strong>. Your slicer shows the weight of a print before you start:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Print</th><th>Typical weight</th><th>Filament cost</th></tr></thead>
              <tbody>
                <tr><td>Keychain</td><td>5–10 g</td><td>about 0.70–1.40&nbsp;SAR</td></tr>
                <tr><td>Phone stand</td><td>40–60 g</td><td>about 5.60–8.40&nbsp;SAR</td></tr>
                <tr><td>Controller stand</td><td>100–150 g</td><td>about 14–21&nbsp;SAR</td></tr>
                <tr><td>Vase or lamp shade</td><td>200–300 g</td><td>about 28–42&nbsp;SAR</td></tr>
              </tbody>
            </table>
          </div>
          <p>Weights depend on size, infill and supports, so treat these as a guide. If cost matters more than the RFID convenience, <a href="/3d/blog/kingroon-pla-basic-filament-review/">KINGROON PLA Basic</a> is our lower-priced everyday PLA; our <a href="/3d/blog/3d-printer-filament-price-saudi-arabia/">filament price guide</a> compares the options.</p>

          <h2>Frequently asked questions</h2>
          <h3>What is the difference between Bambu PLA Basic and PLA Matte?</h3>
          <p>The finish and the strength. PLA Matte has a non-glossy surface that hides layer lines and suits decor and display pieces. PLA Basic is stronger, with higher tensile and bending strength in Bambu Lab's data sheets, and suits everyday and functional prints. Both use the same print settings.</p>
          <h3>Does Bambu Lab filament work in the AMS lite?</h3>
          <p>Yes. Bambu Lab lists PLA Basic and PLA Matte as compatible with all AMS series, including the AMS lite on the A1 and A1 mini. The AMS reads the RFID tag and sets the filament type and colour for you.</p>
          <h3>Can I use a refill without a spool?</h3>
          <p>No. Bambu Lab says the refill needs to be used with a spool. Buy your first kilo with a spool, keep the empty spool, and fit refills onto it after that.</p>
          <h3>What temperature should I print Bambu PLA at?</h3>
          <p>Bambu Lab recommends a nozzle temperature of 190–230&nbsp;°C and a bed temperature of 35–45&nbsp;°C, with the cooling fan on. On a Bambu Lab printer with an AMS the RFID tag sets this automatically.</p>
          <h3>Do Bambu Lab filaments work on other printers?</h3>
          <p>They are standard 1.75&nbsp;mm PLA, so they print on other FDM printers that take 1.75&nbsp;mm filament; use the settings above. Only the RFID auto-setup needs a Bambu Lab AMS.</p>
          <h3>How much is Bambu Lab filament in Saudi Arabia?</h3>
          <p>Bambu Lab PLA Basic and PLA Matte are now available at Black Arrow 3D for 140&nbsp;SAR per 1&nbsp;kg spool, VAT included, with delivery across Saudi Arabia. Stock is limited, so check the product page for the colours still in stock.</p>

          <div class="b3d-article__cta">
            <p>Bambu Lab PLA Basic and PLA Matte, now available at 140 SAR per kilo. Limited stock.</p>
            <a href="''' + PB + '''" class="btn btn-primary">See PLA Basic colours</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="''' + PM + '''">Bambu Lab PLA Matte</a>
            <a href="/3d/blog/best-filament-for-bambu-lab-a1-ams-lite/">Best filament for the A1 and AMS lite</a>
            <a href="/3d/blog/pla-vs-pla-plus-difference/">PLA vs PLA+</a>
            <a href="/3d/blog/which-filament-for-which-print/">Which filament for which print</a>
            <a href="/3d/shop/filament/">All filament</a>
          </div>
''',
        },
        'ar': {
            'headline': 'فلمنت بامبو لاب PLA Basic مقابل PLA Matte: الإعدادات والألوان، مع بكرة أم تعبئة',
            'title': 'فلمنت بامبو لاب PLA Basic وPLA Matte في السعودية | Black Arrow 3D',
            'desc': 'فلمنت بامبو لاب PLA Basic وPLA Matte في السعودية: إعدادات الطباعة الرسمية وRFID ونظام AMS والألوان برموزها، والفرق بين البكرة والتعبئة، وحدود الحرارة وتكلفة الطبعة.',
            'meta_line': 'دليل الفلمنت &middot; ' + AR_DATE + ' &middot; 8 دقائق قراءة',
            'lead': 'تصنع بامبو لاب فلمنت PLA خاصًا بطابعاتها ونظام AMS. فلمنت PLA Basic هو الخيار اليومي لكل الاستخدامات، أما PLA Matte فيمنح سطحًا ناعمًا غير لامع يخفي خطوط الطبقات مقابل قوة أقل قليلًا. إليك الفرق بينهما، والإعدادات التي توصي بها بامبو لاب، ووظيفة شريحة RFID، وهل تشتري الفلمنت مع بكرة أم تعبئة.',
            'card': ('دليل الفلمنت', '8 دقائق قراءة', 'PLA Basic أم PLA Matte من بامبو لاب؟ الإعدادات الرسمية وRFID ونظام AMS والألوان، والبكرة أم التعبئة، وتكلفة الطبعة.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>اختر <a href="''' + PB_AR + '''">بامبو لاب PLA Basic</a> لمعظم الطبعات: الألعاب والهدايا والقطع المنزلية وكل ما تريده بألوان زاهية وقوة أعلى قليلًا. واختر <a href="''' + PM_AR + '''">بامبو لاب PLA Matte</a> لقطع العرض والديكور والمجسمات والنماذج المعمارية، حيث يهم السطح الناعم غير اللامع وقلة خطوط الطبقات الظاهرة أكثر من القوة. كلاهما بقطر 1.75 مم ووزن 1 كجم، ويُطبعان بالإعدادات نفسها، وعليهما شريحة RFID يقرؤها نظام AMS ليضبط كل شيء تلقائيًا. وكلاهما متوفر الآن في Black Arrow 3D بسعر <strong>140 ريالًا لكل 1 كجم</strong>، والكمية محدودة.</p>

          <h2>مقارنة PLA Basic وPLA Matte</h2>
          <p>جميع الأرقام أدناه من أوراق البيانات الفنية الرسمية لبامبو لاب (الإصدار 3.0). وهي قيم مخبرية للمقارنة، أما القطع الفعلية فتعتمد على المجسم والإعدادات.</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA Basic</th><th>PLA Matte</th></tr></thead>
              <tbody>
                <tr><td>السطح</td><td>سطح نهائي ناعم</td><td>مطفي يخفي خطوط الطبقات</td></tr>
                <tr><td>أعلى سرعة طباعة (بامبو لاب)</td><td>حتى 258 مم/ث*</td><td>حتى 270 مم/ث*</td></tr>
                <tr><td>مقاومة الشد (X-Y / Z)</td><td>35 / 31 ميجاباسكال</td><td>30 / 22 ميجاباسكال</td></tr>
                <tr><td>مقاومة الانحناء (X-Y / Z)</td><td>76 / 59 ميجاباسكال</td><td>53 / 29 ميجاباسكال</td></tr>
                <tr><td>درجة الانحراف الحراري (1.8 / 0.45 ميجاباسكال)</td><td>54 / 57 درجة</td><td>52 / 58 درجة</td></tr>
                <tr><td>الكثافة</td><td>1.24 جم/سم³</td><td>1.31 جم/سم³</td></tr>
                <tr><td>القطر</td><td colspan="2">1.75 مم ± 0.03 مم</td></tr>
                <tr><td>الوزن الصافي</td><td colspan="2">1 كجم</td></tr>
                <tr><td>الانبعاثات</td><td colspan="2">حاصل على شهادة UL GREENGUARD (UL 2904)</td></tr>
                <tr><td>الرائحة</td><td colspan="2">بدون رائحة</td></tr>
              </tbody>
            </table>
          </div>
          <p><small>* رقم بامبو لاب مع فوهة 0.4 مم وعرض خط 0.4 مم وارتفاع طبقة 0.2 مم.</small></p>
          <p>باختصار: PLA Basic هو الأقوى بين الاثنين، خاصة بين الطبقات (قيم Z)، لذا فهو الخيار الأفضل للمشابك والحوامل وكل ما يتحمل وزنًا. أما PLA Matte فاختياره من أجل الشكل.</p>

          <h2>إعدادات الطباعة الرسمية</h2>
          <p>على طابعة بامبو لاب مع نظام AMS لا تحتاج إلى إدخال أي من هذه الإعدادات: شريحة RFID على البكرة تخبر الطابعة وبرنامج Bambu Studio بنوع الفلمنت ولونه. أما للطابعات الأخرى، أو للتحقق من ملف الإعدادات، فهذه توصيات بامبو لاب للفلمنتين:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الإعداد</th><th>توصية بامبو لاب</th></tr></thead>
              <tbody>
                <tr><td>حرارة الفوهة</td><td>190–230 درجة</td></tr>
                <tr><td>حرارة السرير</td><td>35–45 درجة</td></tr>
                <tr><td>لوح الطباعة</td><td>Cool Plate أو High Temperature Plate أو Textured PEI Plate</td></tr>
                <tr><td>تجهيز السرير</td><td>غراء</td></tr>
                <tr><td>مروحة التبريد</td><td>تشغيل</td></tr>
                <tr><td>سرعة الطباعة</td><td>أقل من 300 مم/ث</td></tr>
                <tr><td>أحجام الفوهة</td><td>0.2 و0.4 و0.6 و0.8 مم</td></tr>
                <tr><td>السحب العكسي</td><td>0.6–1.0 مم بسرعة 20–40 مم/ث</td></tr>
                <tr><td>أقصى زاوية بروز / جسر</td><td>55° / 30 مم</td></tr>
                <tr><td>الدعامات</td><td>Bambu Support for PLA</td></tr>
              </tbody>
            </table>
          </div>
          <p>طبعت بامبو لاب عينات الاختبار الخاصة بها على 220 درجة وسرير بحرارة 35 درجة وسرعة 200 مم/ث، وهي نقطة بداية مناسبة إذا كنت تضبط الإعدادات يدويًا. إذا لم تلتصق الطبقة الأولى فنظّف اللوح أولًا، ودليلنا عن <a href="/3d/ar/blog/3d-print-bed-adhesion-first-layer/">الطبقة الأولى</a> يشرح الباقي.</p>

          <h2>شريحة RFID ونظام AMS</h2>
          <p>كل بكرة من بامبو لاب عليها شريحة RFID مخزنة فيها إعدادات الطباعة. ضعها في أي نظام AMS (‏AMS lite أو AMS 2 Pro أو AMS HT) فتقرأ الطابعة نوع المادة ولونها وإعداداتها تلقائيًا، فيُستخدم ملف الإعدادات الصحيح ويظهر اللون الصحيح في برنامج التقطيع. وتصنّف بامبو لاب الفلمنتين بأنهما <em>متوافقان مع جميع أنظمة AMS</em>. وهذا هو السبب الرئيسي لشراء فلمنت بامبو لطابعة بامبو: الطباعة متعددة الألوان تعمل مباشرة دون ضبط كل خانة. إذا كنت جديدًا على الطباعة الملونة فاقرأ <a href="/3d/ar/blog/multi-color-3d-printing-explained/">شرح الطباعة ثلاثية الأبعاد متعددة الألوان</a>.</p>

          <h2>فلمنت مع بكرة أم تعبئة؟</h2>
          <p>تبيع بامبو لاب كل لون بطريقتين:</p>
          <ul>
            <li><strong>فلمنت مع بكرة:</strong> يأتي الفلمنت ملفوفًا على بكرة بامبو لاب الأصلية وجاهزًا للتركيب. البكرة من مادة ABS تتحمل حتى 70 درجة، وقطرها 200 مم وارتفاعها 67 مم.</li>
            <li><strong>تعبئة:</strong> الفلمنت نفسه بدون بكرة. وملاحظة بامبو لاب: <em>يجب استخدام التعبئة مع بكرة.</em> تركّبها على بكرة بامبو لاب فارغة لديك، فيقل البلاستيك الذي تتخلص منه في كل مرة.</li>
          </ul>
          <p>إذا كان هذا أول فلمنت لك من بامبو لاب فاشترِه <strong>مع بكرة</strong>. وبعد أن تصبح لديك بكرة فارغة، تكون التعبئة الطريقة الأنظف لشراء الكيلو التالي. في متجرنا تختار <em>مع بكرة</em> أو <em>تعبئة</em> تحت اللون في صفحتي <a href="''' + PB_AR + '''">PLA Basic</a> و<a href="''' + PM_AR + '''">PLA Matte</a>، والتعبئة معروضة لكنها غير متوفرة بعد.</p>

          <h2>الألوان القادمة</h2>
          <p>تعطي بامبو لاب كل لون رمزًا، وهو الاسم الذي يظهر في Bambu Studio ونظام AMS:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الفلمنت</th><th>الألوان (رمز بامبو لاب)</th></tr></thead>
              <tbody>
                <tr><td>PLA Basic</td><td>سماوي (10603)، أزرق (10601)، بنفسجي (10700)، أصفر (10400)، أحمر (10200)، رمادي (10103)، فضي (10102)، وSolar Breeze ‏(10901) من فئة PLA Basic Gradient</td></tr>
                <tr><td>PLA Matte</td><td>وردي ساكورا (11201)، أخضر عشبي (11500)</td></tr>
              </tbody>
            </table>
          </div>
          <p>لون Solar Breeze متدرّج: يتغير اللون تدريجيًا على طول الفلمنت، فتتبدل ألوان المزهرية أو المجسم من الأسفل إلى الأعلى دون أي إعداد للطباعة متعددة الألوان.</p>

          <h2>حرارة السعودية والرطوبة</h2>
          <p>يبدأ الفلمنتان في اللين عند منتصف الخمسينات تقريبًا (درجة الانحراف الحراري 54 درجة لـ PLA Basic و52 درجة لـ PLA Matte عند 1.8 ميجاباسكال). هذا مناسب داخل المنزل، لكن السيارة في صيف السعودية أشد حرارة بكثير، فلا تترك مطبوعات PLA على لوحة القيادة. للقطع المخصصة للسيارة أو للخارج استخدم PETG، واقرأ <a href="/3d/ar/blog/pla-vs-petg-vs-abs-filament-guide/">مقارنة PLA وPETG وABS</a>.</p>
          <p>توصي بامبو لاب بالطباعة والتخزين برطوبة نسبية <strong>أقل من 20%</strong> مع إحكام الإغلاق ومادة مجففة. وفي جدة والدمام والخبر الهواء أرطب من ذلك بكثير، لذا احفظ البكرات المفتوحة داخل AMS مع مادة مجففة جديدة أو في صندوق محكم. وإذا امتصت البكرة الرطوبة فإعداد التجفيف لدى بامبو لاب هو <strong>50 درجة لمدة 8 ساعات</strong> في فرن تجفيف بالهواء الساخن، بعيدًا عن عنصر التسخين. وتحذّر بامبو لاب من استخدام الميكروويف أو فرن المطبخ لأنهما قد يتلفان الفلمنت. دليلنا عن <a href="/3d/ar/blog/3d-printing-filament-saudi-heat-humidity/">الحرارة والرطوبة</a> فيه المزيد عن التخزين.</p>

          <h2>تكلفة الطبعة</h2>
          <p>بسعر 140 ريالًا للكيلو، تكلفة فلمنت بامبو لاب PLA هي <strong>0.14 ريال للجرام</strong>. ويعرض لك برنامج التقطيع وزن الطبعة قبل أن تبدأ:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الطبعة</th><th>الوزن المعتاد</th><th>تكلفة الفلمنت</th></tr></thead>
              <tbody>
                <tr><td>ميدالية مفاتيح</td><td>5–10 جم</td><td>حوالي 0.70–1.40 ريال</td></tr>
                <tr><td>حامل جوال</td><td>40–60 جم</td><td>حوالي 5.60–8.40 ريال</td></tr>
                <tr><td>حامل يد تحكم</td><td>100–150 جم</td><td>حوالي 14–21 ريالًا</td></tr>
                <tr><td>مزهرية أو غطاء مصباح</td><td>200–300 جم</td><td>حوالي 28–42 ريالًا</td></tr>
              </tbody>
            </table>
          </div>
          <p>تختلف الأوزان حسب الحجم ونسبة الحشو والدعامات، فاعتبرها تقديرية. وإذا كانت التكلفة أهم لك من ميزة RFID، فإن <a href="/3d/ar/blog/kingroon-pla-basic-filament-review/">KINGROON PLA Basic</a> هو فلمنت PLA اليومي الأقل سعرًا لدينا، ودليل <a href="/3d/ar/blog/3d-printer-filament-price-saudi-arabia/">أسعار الفلمنت</a> يقارن بين الخيارات.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>ما الفرق بين بامبو PLA Basic وPLA Matte؟</h3>
          <p>السطح والقوة. سطح PLA Matte غير لامع ويخفي خطوط الطبقات ويناسب الديكور وقطع العرض. أما PLA Basic فهو أقوى، بمقاومة شد وانحناء أعلى في أوراق بيانات بامبو لاب، ويناسب الطبعات اليومية والعملية. ويُطبع الاثنان بالإعدادات نفسها.</p>
          <h3>هل يعمل فلمنت بامبو لاب في AMS lite؟</h3>
          <p>نعم. تصنّف بامبو لاب فلمنت PLA Basic وPLA Matte بأنهما متوافقان مع جميع أنظمة AMS، ومنها AMS lite في طابعتي A1 وA1 ميني. ويقرأ نظام AMS شريحة RFID ويضبط نوع الفلمنت ولونه تلقائيًا.</p>
          <h3>هل يمكن استخدام التعبئة بدون بكرة؟</h3>
          <p>لا. تقول بامبو لاب إن التعبئة يجب أن تُستخدم مع بكرة. اشترِ أول كيلو مع بكرة، واحتفظ بالبكرة الفارغة، وركّب عليها التعبئة بعد ذلك.</p>
          <h3>ما درجة الحرارة المناسبة لطباعة بامبو PLA؟</h3>
          <p>توصي بامبو لاب بحرارة فوهة 190–230 درجة وحرارة سرير 35–45 درجة مع تشغيل مروحة التبريد. وعلى طابعة بامبو لاب مع AMS تضبط شريحة RFID ذلك تلقائيًا.</p>
          <h3>هل يعمل فلمنت بامبو لاب على طابعات أخرى؟</h3>
          <p>هو فلمنت PLA قياسي بقطر 1.75 مم، فيُطبع على طابعات FDM الأخرى التي تقبل فلمنت 1.75 مم باستخدام الإعدادات أعلاه. فقط الضبط التلقائي عبر RFID يحتاج إلى نظام AMS من بامبو لاب.</p>
          <h3>كم سعر فلمنت بامبو لاب في السعودية؟</h3>
          <p>فلمنت بامبو لاب PLA Basic وPLA Matte متوفر الآن في Black Arrow 3D بسعر 140 ريالًا لبكرة 1 كجم شامل الضريبة، مع التوصيل لجميع مناطق السعودية. الكمية محدودة، لذا راجع صفحة المنتج لمعرفة الألوان المتوفرة.</p>

          <div class="b3d-article__cta">
            <p>بامبو لاب PLA Basic وPLA Matte، متوفر الآن بسعر 140 ريالًا للكيلو. الكمية محدودة.</p>
            <a href="''' + PB_AR + '''" class="btn btn-primary">ألوان PLA Basic</a>
          </div>

          <h2>مقالات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="''' + PM_AR + '''">بامبو لاب PLA Matte</a>
            <a href="/3d/ar/blog/best-filament-for-bambu-lab-a1-ams-lite/">أفضل فلمنت لطابعة A1 ونظام AMS lite</a>
            <a href="/3d/ar/blog/pla-vs-pla-plus-difference/">الفرق بين PLA وPLA+</a>
            <a href="/3d/ar/blog/which-filament-for-which-print/">أي فلمنت لأي طبعة</a>
            <a href="/3d/ar/shop/filament/">كل الفلمنت</a>
          </div>
''',
        },
    },
]
