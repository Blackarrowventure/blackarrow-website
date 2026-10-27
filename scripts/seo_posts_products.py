"""Bilingual (EN + AR) product and filament posts for the Black Arrow 3D blog (October 2026).

Data only: each item in POSTS follows the same schema as GUIDES in
scripts/build_3d_troubleshooting_guides.py. Prices and stock are from the live store
(3d/assets/data/3d-products.json + CRM Website Inventory) on October 22, 2026; the posts point
to the product pages for the current price and stock rather than promising either.
"""

EN_DATE = 'October 22, 2026'
AR_DATE = '22 أكتوبر 2026'


def meta(kind_en, mins_en):
    return kind_en + ' &middot; ' + EN_DATE + ' &middot; ' + mins_en


def meta_ar(kind_ar, mins_ar):
    return kind_ar + ' &middot; ' + AR_DATE + ' &middot; ' + mins_ar


DELIVERY_EN = ('Black Arrow 3D ships from Dammam to every city in Saudi Arabia: Regular delivery takes 4–5 business days '
               '(30&nbsp;SAR) and Fast delivery 2–3 business days (50&nbsp;SAR). Regular delivery is free on every order that '
               'includes a 3D printer, and on any order from 3,000&nbsp;SAR.')
DELIVERY_AR = ('يشحن Black Arrow 3D من الدمام إلى جميع مدن المملكة: التوصيل العادي خلال 4–5 أيام عمل (30 ريالًا) '
               'والسريع خلال 2–3 أيام عمل (50 ريالًا). التوصيل العادي مجاني لكل طلب يحتوي على طابعة ثلاثية الأبعاد، '
               'ولأي طلب من 3,000 ريال.')

POSTS = [
    # ------------------------------------------------------------------
    # 1. KINGROON PLA Basic
    # ------------------------------------------------------------------
    {
        'slug': 'kingroon-pla-basic-filament-review',
        'en': {
            'headline': 'KINGROON PLA Basic Filament Review: Settings, Colours and Who It Suits',
            'title': 'KINGROON PLA Basic Filament Review (KSA) | Black Arrow 3D',
            'desc': 'KINGROON PLA Basic 1.75 mm, 1 kg in Saudi Arabia: print settings, colours, how it runs on Bambu Lab A1 and A1 mini, storage in Saudi humidity and price per print.',
            'meta_line': meta('Filament review', '7 min read'),
            'lead': 'KINGROON PLA Basic is an everyday 1.75 mm PLA sold in 1 kg spools. It is the filament we recommend most often for first prints, gifts, toys and household parts. Here is how to print it well, which colours to pick and what a print really costs.',
            'card': ('Filament review', '7 min read', 'Everyday 1 kg PLA in many colours: settings, Bambu Lab tips, storage and cost per print.'),
            'body': '''
          <h2>Quick answer</h2>
          <p><a href="/3d/product/kingroon-pla-basic-filament/">KINGROON PLA Basic</a> is a good default filament for most printers sold in Saudi Arabia, including the Bambu Lab A1, A1 mini, A2L and P2S. It prints at <strong>190–210&nbsp;°C</strong> on a <strong>50–70&nbsp;°C</strong> bed, needs no enclosure, has almost no smell and comes in plenty of colours. Choose it for decorative pieces, gifts, prototypes and indoor parts. Choose <a href="/3d/blog/kingroon-petg-basic-filament-guide/">PETG</a> instead for parts that sit in a hot car, outdoors or near heat.</p>

          <h2>What you get</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Spec</th><th>KINGROON PLA Basic</th></tr></thead>
              <tbody>
                <tr><td>Material</td><td>PLA</td></tr>
                <tr><td>Diameter</td><td>1.75 mm</td></tr>
                <tr><td>Weight</td><td>1 kg per spool</td></tr>
                <tr><td>Nozzle temperature</td><td>190–210&nbsp;°C</td></tr>
                <tr><td>Bed temperature</td><td>50–70&nbsp;°C</td></tr>
                <tr><td>Works with</td><td>Most FDM printers that take 1.75 mm PLA</td></tr>
              </tbody>
            </table>
          </div>
          <p>Colours on the store include black, white, red, orange, yellow, purple and pink, with more arriving as stock is restocked. The <a href="/3d/product/kingroon-pla-basic-filament/">product page</a> shows which colours are in stock right now.</p>

          <h2>Settings that work</h2>
          <ul>
            <li><strong>Bambu Lab printers:</strong> in Bambu Studio choose a <em>Generic PLA</em> profile. Run the flow calibration once for a new spool if your printer offers it.</li>
            <li><strong>Temperature:</strong> start at 200&nbsp;°C. Go towards 210&nbsp;°C if layers look weak or the surface is dull; go towards 195&nbsp;°C if you see stringing.</li>
            <li><strong>Bed:</strong> 55–60&nbsp;°C on a textured or smooth PEI plate. Clean the plate with warm water and dish soap when the first layer stops sticking. Our <a href="/3d/blog/3d-print-bed-adhesion-first-layer/">first-layer guide</a> covers the rest.</li>
            <li><strong>Cooling:</strong> part fan at full speed after the first few layers. PLA likes cooling; that is what keeps overhangs and small details sharp.</li>
            <li><strong>Speed:</strong> the default profiles of modern printers are fine. If very thin walls look rough, lower the outer wall speed rather than the whole print.</li>
          </ul>

          <h2>Saudi heat and humidity</h2>
          <p>PLA softens at roughly 55–60&nbsp;°C. That is fine inside a home or office, but a car dashboard in a Saudi summer gets much hotter, so a PLA phone holder left in the car can warp. For anything that lives in a car or outdoors, use PETG.</p>
          <p>PLA also absorbs moisture slowly from the air. In humid coastal cities like Jeddah, Dammam and Khobar, keep opened spools in a sealed box or bag with silica gel. Signs of a wet spool are popping or crackling at the nozzle, extra stringing and a rough surface. Read our <a href="/3d/blog/3d-printing-filament-saudi-heat-humidity/">filament in Saudi heat and humidity</a> guide for drying and storage.</p>

          <h2>What a print costs</h2>
          <p>A 1 kg spool at 65&nbsp;SAR works out to about <strong>0.065&nbsp;SAR per gram</strong>. Your slicer tells you the weight of each print before you start:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Print</th><th>Typical weight</th><th>Filament cost</th></tr></thead>
              <tbody>
                <tr><td>Keychain</td><td>5–10 g</td><td>under 1&nbsp;SAR</td></tr>
                <tr><td>Phone stand</td><td>40–60 g</td><td>about 2.5–4&nbsp;SAR</td></tr>
                <tr><td>Controller stand</td><td>100–150 g</td><td>about 6.5–10&nbsp;SAR</td></tr>
                <tr><td>Desk lamp shade or vase</td><td>200–300 g</td><td>about 13–20&nbsp;SAR</td></tr>
              </tbody>
            </table>
          </div>
          <p>Weights vary with size, infill and supports, so treat these as a guide. Multi-colour prints also waste some filament on colour changes. See our <a href="/3d/blog/3d-printer-filament-price-saudi-arabia/">filament price and cost-per-print guide</a> for the full method.</p>

          <h2>PLA Basic or PLA+?</h2>
          <p>The store also sells <a href="/3d/product/filament-pla-1kg/">PLA+ filament</a>. PLA+ is a modified, slightly tougher PLA: a little less brittle, a little better on parts that clip or snap together. For decorative prints and gifts, PLA Basic is all you need. Our <a href="/3d/blog/pla-vs-pla-plus-difference/">PLA vs PLA+ guide</a> explains when the upgrade is worth it.</p>

          <h2>Frequently asked questions</h2>
          <h3>Does KINGROON PLA work with the Bambu Lab A1 mini?</h3>
          <p>Yes. It is standard 1.75 mm PLA. Use a Generic PLA profile in Bambu Studio and print at around 200&nbsp;°C.</p>
          <h3>Can I use KINGROON PLA in the AMS lite?</h3>
          <p>Yes, standard 1 kg spools of PLA feed through the AMS lite. Keep the spool winding neat and the filament end clipped into the spool edge when you store it, so it does not tangle. See our <a href="/3d/blog/best-filament-for-bambu-lab-a1-ams-lite/">AMS lite filament guide</a>.</p>
          <h3>Is PLA safe for food?</h3>
          <p>Treat any 3D printed part as not food-safe: the layer lines trap bacteria and colourants are not certified. Use printed cups and plates for decoration only.</p>
          <h3>How long does a spool last?</h3>
          <p>A 1 kg spool makes around 100 small prints such as keychains and stands, or 4–5 large vases. Most hobby users finish a spool in a few weeks.</p>

          <div class="b3d-article__cta">
            <p>KINGROON PLA Basic, 1 kg, delivered across Saudi Arabia</p>
            <a href="/3d/product/kingroon-pla-basic-filament/" class="btn btn-primary">See colours and stock</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/kingroon-petg-basic-filament-guide/">KINGROON PETG Basic guide</a>
            <a href="/3d/blog/pla-vs-pla-plus-difference/">PLA vs PLA+</a>
            <a href="/3d/blog/pla-vs-petg-vs-abs-filament-guide/">PLA vs PETG vs ABS</a>
            <a href="/3d/shop/filament/">All filament</a>
          </div>
''',
        },
        'ar': {
            'headline': 'مراجعة فلمنت KINGROON PLA Basic: الإعدادات والألوان ولمن يناسب',
            'title': 'مراجعة فلمنت KINGROON PLA Basic في السعودية | Black Arrow 3D',
            'desc': 'فلمنت KINGROON PLA Basic بقطر 1.75 مم ووزن 1 كجم في السعودية: إعدادات الطباعة والألوان وأداؤه على بامبو لاب A1 وA1 ميني والتخزين في الرطوبة وتكلفة الطبعة.',
            'meta_line': meta_ar('مراجعة فلمنت', '7 دقائق قراءة'),
            'lead': 'فلمنت KINGROON PLA Basic هو فلمنت PLA يومي بقطر 1.75 مم في بكرات وزنها 1 كجم، وهو أكثر فلمنت ننصح به للطبعات الأولى والهدايا والألعاب والقطع المنزلية. إليك كيف تطبعه بجودة، وأي الألوان تختار، وكم تكلف الطبعة فعلًا.',
            'card': ('مراجعة فلمنت', '7 دقائق قراءة', 'فلمنت PLA يومي بوزن 1 كجم وألوان كثيرة: الإعدادات ونصائح بامبو لاب والتخزين وتكلفة الطبعة.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>فلمنت <a href="/3d/ar/product/kingroon-pla-basic-filament/">KINGROON PLA Basic</a> خيار افتراضي ممتاز لمعظم الطابعات المباعة في السعودية، ومنها بامبو لاب A1 وA1 ميني وA2L وP2S. يُطبع على حرارة <strong>190–210 درجة</strong> وسرير بحرارة <strong>50–70 درجة</strong>، ولا يحتاج إلى طابعة مغلقة، ورائحته تكاد تكون معدومة، ومتوفر بألوان كثيرة. اختره للقطع الديكورية والهدايا والنماذج الأولية والقطع الداخلية، واختر <a href="/3d/ar/blog/kingroon-petg-basic-filament-guide/">PETG</a> بدلًا منه للقطع التي توضع في السيارة أو في الخارج أو قرب الحرارة.</p>

          <h2>المواصفات</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>المواصفة</th><th>KINGROON PLA Basic</th></tr></thead>
              <tbody>
                <tr><td>المادة</td><td>PLA</td></tr>
                <tr><td>القطر</td><td>1.75 مم</td></tr>
                <tr><td>الوزن</td><td>1 كجم للبكرة</td></tr>
                <tr><td>حرارة الفوهة</td><td>190–210 درجة</td></tr>
                <tr><td>حرارة السرير</td><td>50–70 درجة</td></tr>
                <tr><td>التوافق</td><td>معظم طابعات FDM التي تقبل PLA بقطر 1.75 مم</td></tr>
              </tbody>
            </table>
          </div>
          <p>من الألوان المتوفرة في المتجر: الأسود والأبيض والأحمر والبرتقالي والأصفر والبنفسجي والوردي، وتصل ألوان أخرى مع كل شحنة. تعرض <a href="/3d/ar/product/kingroon-pla-basic-filament/">صفحة المنتج</a> الألوان المتوفرة حاليًا.</p>

          <h2>إعدادات مجرّبة</h2>
          <ul>
            <li><strong>طابعات بامبو لاب:</strong> اختر في Bambu Studio ملف <em>Generic PLA</em>، وشغّل معايرة التدفق مرة واحدة لكل بكرة جديدة إن كانت طابعتك تدعمها.</li>
            <li><strong>الحرارة:</strong> ابدأ بـ 200 درجة، وارفعها نحو 210 إذا كانت الطبقات ضعيفة أو السطح باهتًا، واخفضها نحو 195 إذا ظهرت خيوط رفيعة.</li>
            <li><strong>السرير:</strong> 55–60 درجة على لوح PEI محبب أو أملس. نظّف اللوح بالماء الدافئ وسائل الصحون إذا لم تعد الطبقة الأولى تلتصق. تجد التفاصيل في <a href="/3d/ar/blog/3d-print-bed-adhesion-first-layer/">دليل الطبقة الأولى</a>.</li>
            <li><strong>التبريد:</strong> مروحة القطعة على السرعة الكاملة بعد الطبقات الأولى، فالتبريد هو ما يحافظ على حدّة البروزات والتفاصيل الصغيرة.</li>
            <li><strong>السرعة:</strong> الإعدادات الافتراضية للطابعات الحديثة مناسبة. وإذا بدت الجدران الرفيعة خشنة، فاخفض سرعة الجدار الخارجي فقط.</li>
          </ul>

          <h2>الحرارة والرطوبة في السعودية</h2>
          <p>يلين PLA عند حوالي 55–60 درجة. هذا لا يؤثر داخل المنزل أو المكتب، لكن تابلوه السيارة في صيف السعودية أسخن بكثير، لذا قد يتشوه حامل جوال من PLA يُترك في السيارة. لكل ما يبقى في السيارة أو في الخارج، استخدم PETG.</p>
          <p>يمتص PLA الرطوبة ببطء من الهواء. في المدن الساحلية الرطبة مثل جدة والدمام والخبر، احفظ البكرات المفتوحة في صندوق محكم أو كيس مع السيليكا جل. علامات البكرة الرطبة: طقطقة عند الفوهة، وخيوط أكثر، وسطح خشن. اقرأ دليل <a href="/3d/ar/blog/3d-printing-filament-saudi-heat-humidity/">الفلمنت في حرارة السعودية ورطوبتها</a> لمعرفة طرق التجفيف والتخزين.</p>

          <h2>كم تكلف الطبعة؟</h2>
          <p>بكرة 1 كجم بسعر 65 ريالًا تعني حوالي <strong>0.065 ريال للغرام</strong>. يخبرك برنامج التقطيع بوزن كل طبعة قبل البدء:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الطبعة</th><th>الوزن المعتاد</th><th>تكلفة الفلمنت</th></tr></thead>
              <tbody>
                <tr><td>ميدالية مفاتيح</td><td>5–10 غرامات</td><td>أقل من ريال</td></tr>
                <tr><td>حامل جوال</td><td>40–60 غرامًا</td><td>حوالي 2.5–4 ريالات</td></tr>
                <tr><td>حامل يد تحكم</td><td>100–150 غرامًا</td><td>حوالي 6.5–10 ريالات</td></tr>
                <tr><td>غطاء مصباح أو مزهرية</td><td>200–300 غرام</td><td>حوالي 13–20 ريالًا</td></tr>
              </tbody>
            </table>
          </div>
          <p>تختلف الأوزان حسب الحجم ونسبة الحشو والدعامات، فاعتبر الأرقام تقريبية. والطبعات متعددة الألوان تهدر بعض الفلمنت عند تبديل الألوان. اقرأ <a href="/3d/ar/blog/3d-printer-filament-price-saudi-arabia/">دليل أسعار الفلمنت وتكلفة الطبعة</a> لمعرفة طريقة الحساب كاملة.</p>

          <h2>PLA Basic أم PLA+؟</h2>
          <p>يبيع المتجر أيضًا <a href="/3d/ar/product/filament-pla-1kg/">فلمنت PLA+</a>، وهو PLA معدّل أكثر متانة قليلًا وأقل هشاشة، وأفضل قليلًا للقطع التي تُركّب بالكبس. للقطع الديكورية والهدايا يكفيك PLA Basic. يشرح <a href="/3d/ar/blog/pla-vs-pla-plus-difference/">دليل PLA مقابل PLA+</a> متى تستحق الترقية.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>هل يعمل فلمنت KINGROON PLA مع بامبو لاب A1 ميني؟</h3>
          <p>نعم، فهو PLA قياسي بقطر 1.75 مم. استخدم ملف Generic PLA في Bambu Studio واطبع على حوالي 200 درجة.</p>
          <h3>هل يمكن استخدامه في AMS lite؟</h3>
          <p>نعم، بكرات PLA القياسية بوزن 1 كجم تعمل مع AMS lite. حافظ على لفّ الخيط مرتبًا وثبّت طرفه في حافة البكرة عند التخزين حتى لا يتشابك. راجع <a href="/3d/ar/blog/best-filament-for-bambu-lab-a1-ams-lite/">دليل الفلمنت لـ AMS lite</a>.</p>
          <h3>هل PLA آمن للطعام؟</h3>
          <p>اعتبر أي قطعة مطبوعة غير آمنة للطعام، فخطوط الطبقات تحتفظ بالبكتيريا والأصباغ غير معتمدة. استخدم الأكواب والأطباق المطبوعة للزينة فقط.</p>
          <h3>كم تدوم البكرة؟</h3>
          <p>تكفي بكرة 1 كجم لحوالي 100 طبعة صغيرة مثل الميداليات والحوامل، أو 4–5 مزهريات كبيرة. ينهي معظم الهواة البكرة خلال بضعة أسابيع.</p>

          <div class="b3d-article__cta">
            <p>فلمنت KINGROON PLA Basic بوزن 1 كجم مع التوصيل لجميع مدن المملكة</p>
            <a href="/3d/ar/product/kingroon-pla-basic-filament/" class="btn btn-primary">شاهد الألوان والمخزون</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/kingroon-petg-basic-filament-guide/">دليل KINGROON PETG Basic</a>
            <a href="/3d/ar/blog/pla-vs-pla-plus-difference/">PLA مقابل PLA+</a>
            <a href="/3d/ar/blog/pla-vs-petg-vs-abs-filament-guide/">PLA وPETG وABS</a>
            <a href="/3d/ar/shop/filament/">كل أنواع الفلمنت</a>
          </div>
''',
        },
    },
    # ------------------------------------------------------------------
    # 2. KINGROON PETG Basic
    # ------------------------------------------------------------------
    {
        'slug': 'kingroon-petg-basic-filament-guide',
        'en': {
            'headline': 'KINGROON PETG Basic Filament Guide: When to Use PETG and How to Print It',
            'title': 'KINGROON PETG Basic Filament Guide (KSA) | Black Arrow 3D',
            'desc': 'KINGROON PETG Basic 1.75 mm, 1 kg in Saudi Arabia: when PETG beats PLA, print settings for Bambu Lab printers, stringing fixes, drying and the best uses for car and outdoor parts.',
            'meta_line': meta('Filament guide', '7 min read'),
            'lead': 'PETG is the filament to reach for when a print has to survive heat, sunlight, water or a few knocks. Here is when KINGROON PETG Basic is the right choice over PLA, how to print it cleanly, and how to stop the stringing PETG is known for.',
            'card': ('Filament guide', '7 min read', 'When PETG beats PLA in Saudi conditions, settings that print cleanly and how to stop stringing.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>Use <a href="/3d/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a> for parts that go in a car, outdoors, in a kitchen or bathroom, or anywhere warm: phone and dashcam mounts, plant pots, hooks, brackets and covers. PETG handles heat better than PLA, bends before it snaps and shrugs off water. It prints on the same open printers as PLA, including the Bambu Lab A1 and A1 mini, with a little more care for stringing and the first layer.</p>

          <h2>PETG vs PLA in one table</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA</th><th>PETG</th></tr></thead>
              <tbody>
                <tr><td>Softens at about</td><td>55–60&nbsp;°C</td><td>75–80&nbsp;°C</td></tr>
                <tr><td>Toughness</td><td>Stiff, can snap</td><td>Bends before it breaks</td></tr>
                <tr><td>Water and sun</td><td>Fine indoors</td><td>Good outdoors and wet</td></tr>
                <tr><td>Ease of printing</td><td>Easiest</td><td>Easy, more stringing</td></tr>
                <tr><td>Surface</td><td>Matte or satin</td><td>Glossy</td></tr>
                <tr><td>Best for</td><td>Gifts, decor, prototypes</td><td>Car, outdoor and functional parts</td></tr>
              </tbody>
            </table>
          </div>

          <h2>Settings that work</h2>
          <ul>
            <li><strong>Temperature:</strong> follow the range on your spool label. For Bambu Lab printers, start with the <em>Generic PETG</em> profile and adjust in 5&nbsp;°C steps: hotter if layers split, cooler if it strings.</li>
            <li><strong>Bed:</strong> 70–80&nbsp;°C. A textured PEI plate is ideal. On a smooth PEI plate, PETG can stick <em>too</em> well; use a thin layer of glue stick as a release layer.</li>
            <li><strong>First layer:</strong> do not squash it as hard as PLA. A slightly higher first layer avoids the nozzle dragging through the plastic.</li>
            <li><strong>Cooling:</strong> lower than PLA, around 30–50% part fan. Too much cooling weakens the layer bond.</li>
            <li><strong>Speed:</strong> PETG prefers a little slower than PLA. If the profile is very fast and walls look rough, drop the outer wall speed.</li>
          </ul>

          <h2>How to stop PETG stringing</h2>
          <ol>
            <li><strong>Dry the spool.</strong> Wet PETG strings far more. KINGROON recommends 55&nbsp;°C for 8 hours if it has absorbed moisture. A filament dryer or a printer box with drying works best.</li>
            <li><strong>Lower the temperature</strong> by 5&nbsp;°C at a time.</li>
            <li><strong>Check retraction</strong> is on. The default Bambu profiles already handle this well.</li>
            <li><strong>Clean the nozzle.</strong> PETG likes to collect a blob on the nozzle; wipe it while the nozzle is hot, carefully, with a brass brush.</li>
          </ol>
          <p>Our <a href="/3d/blog/3d-print-stringing-fix/">stringing guide</a> goes step by step.</p>

          <h2>Saudi conditions</h2>
          <p>In a parked car in summer, a PLA mount can droop within a day. PETG holds its shape much better, which makes it the practical choice for phone holders, cable clips and dashcam mounts. For parts that sit in direct sun for months, choose a darker or opaque colour; transparent colours show sun damage first. In humid cities, keep PETG sealed with silica gel even more strictly than PLA.</p>

          <h2>Colours</h2>
          <p>KINGROON PETG Basic comes in many colours, including orange, yellow, green, red, gray and dark blue, with transparent and fluorescent colours as stock allows. Check the <a href="/3d/product/kingroon-petg-basic-filament/">product page</a> for the colours in stock today.</p>

          <h2>Frequently asked questions</h2>
          <h3>Can the Bambu Lab A1 mini print PETG?</h3>
          <p>Yes. The A1 mini bed reaches 80&nbsp;°C and the hot end 300&nbsp;°C, which is enough for PETG. Use the Generic PETG profile and a textured plate.</p>
          <h3>Is PETG stronger than PLA?</h3>
          <p>PETG is tougher: it bends and absorbs knocks where PLA snaps. PLA is stiffer. For clips, hinges and mounts PETG lasts longer.</p>
          <h3>Does PETG need an enclosed printer?</h3>
          <p>No. Unlike ABS and ASA, PETG prints well on open printers such as the A1 and A1 mini.</p>
          <h3>Can I put PETG and PLA in the AMS lite together?</h3>
          <p>Yes, you can load both, but print one material per part. PETG and PLA do not bond well to each other, which makes PLA a handy easy-to-remove support material under PETG.</p>

          <div class="b3d-article__cta">
            <p>KINGROON PETG Basic, 1 kg, delivered across Saudi Arabia</p>
            <a href="/3d/product/kingroon-petg-basic-filament/" class="btn btn-primary">See colours and stock</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/kingroon-pla-basic-filament-review/">KINGROON PLA Basic review</a>
            <a href="/3d/blog/3d-printing-filament-saudi-heat-humidity/">Filament in Saudi heat and humidity</a>
            <a href="/3d/blog/which-filament-for-which-print/">Which filament for which print</a>
            <a href="/3d/shop/filament/">All filament</a>
          </div>
''',
        },
        'ar': {
            'headline': 'دليل فلمنت KINGROON PETG Basic: متى تستخدم PETG وكيف تطبعه',
            'title': 'دليل فلمنت KINGROON PETG Basic في السعودية | Black Arrow 3D',
            'desc': 'فلمنت KINGROON PETG Basic بقطر 1.75 مم ووزن 1 كجم في السعودية: متى يتفوق PETG على PLA، وإعدادات الطباعة لطابعات بامبو لاب، وحل مشكلة الخيوط، والتجفيف، وأفضل الاستخدامات.',
            'meta_line': meta_ar('دليل فلمنت', '7 دقائق قراءة'),
            'lead': 'فلمنت PETG هو الخيار عندما يجب أن تتحمل الطبعة الحرارة أو الشمس أو الماء أو بعض الصدمات. إليك متى يكون KINGROON PETG Basic أفضل من PLA، وكيف تطبعه بنظافة، وكيف توقف الخيوط الرفيعة التي يشتهر بها.',
            'card': ('دليل فلمنت', '7 دقائق قراءة', 'متى يتفوق PETG على PLA في ظروف السعودية، وإعدادات طباعة نظيفة، وحل مشكلة الخيوط.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>استخدم <a href="/3d/ar/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a> للقطع التي توضع في السيارة أو في الخارج أو في المطبخ والحمام أو قرب الحرارة: حوامل الجوال وكاميرات السيارة، وأحواض النباتات، والعلاقات، والدعامات، والأغطية. يتحمل PETG الحرارة أكثر من PLA، وينحني قبل أن ينكسر، ولا يتأثر بالماء. ويُطبع على نفس الطابعات المفتوحة التي تطبع PLA، ومنها بامبو لاب A1 وA1 ميني، مع اهتمام إضافي بالخيوط والطبقة الأولى.</p>

          <h2>PETG مقابل PLA في جدول واحد</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA</th><th>PETG</th></tr></thead>
              <tbody>
                <tr><td>يلين عند حوالي</td><td>55–60 درجة</td><td>75–80 درجة</td></tr>
                <tr><td>المتانة</td><td>صلب وقد ينكسر</td><td>ينحني قبل أن ينكسر</td></tr>
                <tr><td>الماء والشمس</td><td>مناسب داخل المنزل</td><td>جيد في الخارج ومع الماء</td></tr>
                <tr><td>سهولة الطباعة</td><td>الأسهل</td><td>سهل مع خيوط أكثر</td></tr>
                <tr><td>السطح</td><td>مطفأ أو ساتان</td><td>لامع</td></tr>
                <tr><td>الأفضل لـ</td><td>الهدايا والديكور والنماذج</td><td>قطع السيارة والخارج والقطع العملية</td></tr>
              </tbody>
            </table>
          </div>

          <h2>إعدادات مجرّبة</h2>
          <ul>
            <li><strong>الحرارة:</strong> اتبع المدى المكتوب على ملصق البكرة. مع طابعات بامبو لاب ابدأ بملف <em>Generic PETG</em> وعدّل 5 درجات في كل مرة: ارفعها إذا انفصلت الطبقات، واخفضها إذا ظهرت خيوط.</li>
            <li><strong>السرير:</strong> 70–80 درجة. اللوح المحبب PEI هو الأفضل، أما على اللوح الأملس فقد يلتصق PETG أكثر من اللازم، فاستخدم طبقة رقيقة من الغراء كفاصل.</li>
            <li><strong>الطبقة الأولى:</strong> لا تضغطها بقوة كما في PLA، فطبقة أولى أعلى قليلًا تمنع الفوهة من الاحتكاك بالبلاستيك.</li>
            <li><strong>التبريد:</strong> أقل من PLA، حوالي 30–50% لمروحة القطعة، فالتبريد الزائد يضعف التصاق الطبقات.</li>
            <li><strong>السرعة:</strong> يفضّل PETG سرعة أقل قليلًا من PLA. إذا كانت الجدران خشنة فاخفض سرعة الجدار الخارجي.</li>
          </ul>

          <h2>كيف توقف خيوط PETG</h2>
          <ol>
            <li><strong>جفّف البكرة.</strong> PETG الرطب يُنتج خيوطًا أكثر بكثير. توصي KINGROON بتجفيفه على 55 درجة لمدة 8 ساعات إذا امتص الرطوبة، والأفضل استخدام مجفف فلمنت أو صندوق بخاصية التجفيف.</li>
            <li><strong>اخفض الحرارة</strong> 5 درجات في كل مرة.</li>
            <li><strong>تأكد من تفعيل السحب العكسي (Retraction)</strong>، وملفات بامبو الافتراضية تضبطه جيدًا.</li>
            <li><strong>نظّف الفوهة.</strong> يميل PETG إلى التجمع على الفوهة، فامسحه بحذر بفرشاة نحاسية والفوهة ساخنة.</li>
          </ol>
          <p>يشرح <a href="/3d/ar/blog/3d-print-stringing-fix/">دليل حل مشكلة الخيوط</a> الخطوات بالتفصيل.</p>

          <h2>ظروف السعودية</h2>
          <p>في سيارة متوقفة صيفًا قد يرتخي حامل من PLA خلال يوم، بينما يحافظ PETG على شكله أكثر بكثير، لذا فهو الخيار العملي لحوامل الجوال ومشابك الكابلات وحوامل كاميرات السيارة. للقطع التي تبقى تحت الشمس المباشرة لأشهر اختر لونًا داكنًا أو معتمًا، فالألوان الشفافة تُظهر أثر الشمس أولًا. وفي المدن الرطبة احفظ PETG مغلقًا مع السيليكا جل بحرص أكبر من PLA.</p>

          <h2>الألوان</h2>
          <p>يتوفر KINGROON PETG Basic بألوان كثيرة منها البرتقالي والأصفر والأخضر والأحمر والرمادي والأزرق الداكن، مع ألوان شفافة وفسفورية حسب المخزون. راجع <a href="/3d/ar/product/kingroon-petg-basic-filament/">صفحة المنتج</a> لمعرفة الألوان المتوفرة اليوم.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>هل تطبع بامبو لاب A1 ميني فلمنت PETG؟</h3>
          <p>نعم، يصل سرير A1 ميني إلى 80 درجة والفوهة إلى 300 درجة، وهذا يكفي لـ PETG. استخدم ملف Generic PETG ولوحًا محببًا.</p>
          <h3>هل PETG أقوى من PLA؟</h3>
          <p>PETG أكثر متانة، فهو ينحني ويتحمل الصدمات حيث ينكسر PLA، بينما PLA أكثر صلابة. للمشابك والمفصلات والحوامل يدوم PETG أطول.</p>
          <h3>هل يحتاج PETG إلى طابعة مغلقة؟</h3>
          <p>لا. على عكس ABS وASA، يُطبع PETG جيدًا على الطابعات المفتوحة مثل A1 وA1 ميني.</p>
          <h3>هل يمكن وضع PETG وPLA معًا في AMS lite؟</h3>
          <p>نعم، يمكنك تحميل الاثنين، لكن اطبع كل قطعة بمادة واحدة. لا يلتصق PETG وPLA ببعضهما جيدًا، ولذلك يصلح PLA كمادة دعامات سهلة الإزالة تحت PETG.</p>

          <div class="b3d-article__cta">
            <p>فلمنت KINGROON PETG Basic بوزن 1 كجم مع التوصيل لجميع مدن المملكة</p>
            <a href="/3d/ar/product/kingroon-petg-basic-filament/" class="btn btn-primary">شاهد الألوان والمخزون</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/kingroon-pla-basic-filament-review/">مراجعة KINGROON PLA Basic</a>
            <a href="/3d/ar/blog/3d-printing-filament-saudi-heat-humidity/">الفلمنت في حرارة السعودية ورطوبتها</a>
            <a href="/3d/ar/blog/which-filament-for-which-print/">أي فلمنت لأي طبعة</a>
            <a href="/3d/ar/shop/filament/">كل أنواع الفلمنت</a>
          </div>
''',
        },
    },
    # ------------------------------------------------------------------
    # 3. PLA vs PLA+
    # ------------------------------------------------------------------
    {
        'slug': 'pla-vs-pla-plus-difference',
        'en': {
            'headline': 'PLA vs PLA+: What Is the Difference and Which Should You Buy?',
            'title': 'PLA vs PLA+ Filament: The Real Difference | Black Arrow 3D',
            'desc': 'PLA vs PLA+ explained: what the plus actually means, toughness, print temperature, surface finish and price, and which one to buy for gifts, functional parts and beginners.',
            'meta_line': meta('Filament guide', '5 min read'),
            'lead': 'PLA+ (also sold as PLA Pro or Tough PLA) sounds like a straight upgrade, but the plus means different things from brand to brand. Here is what changes in practice and when the extra cost is worth it.',
            'card': ('Filament guide', '5 min read', 'What the plus really means, how the two print and when PLA+ is worth the extra.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>PLA+ is PLA with additives that make it <strong>less brittle and a bit tougher</strong>. It prints almost exactly like PLA, usually 5–10&nbsp;°C hotter. For decorative prints, figures, gifts and prototypes, regular PLA is all you need and costs less. Pick PLA+ for parts that are handled a lot, clip together or get dropped. If a part needs real heat resistance, neither is the answer: use <a href="/3d/blog/kingroon-petg-basic-filament-guide/">PETG</a>.</p>

          <h2>What the plus means</h2>
          <p>There is no standard for PLA+. Each manufacturer blends its own modifiers into PLA to improve impact resistance and layer bonding. The result is usually:</p>
          <ul>
            <li><strong>Less brittle:</strong> thin parts bend a little before they crack.</li>
            <li><strong>Better layer bonding:</strong> parts are less likely to split along a layer line.</li>
            <li><strong>Slightly hotter printing:</strong> often 205–225&nbsp;°C instead of 190–210&nbsp;°C.</li>
            <li><strong>Similar heat limit:</strong> it still softens at roughly the same temperature as PLA.</li>
          </ul>

          <h2>Side by side</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA</th><th>PLA+</th></tr></thead>
              <tbody>
                <tr><td>Ease of printing</td><td>Easiest</td><td>Just as easy</td></tr>
                <tr><td>Toughness</td><td>Stiff, can snap</td><td>Tougher, less brittle</td></tr>
                <tr><td>Surface</td><td>Clean, slightly glossy</td><td>Often more matte</td></tr>
                <tr><td>Heat resistance</td><td>Low</td><td>Low</td></tr>
                <tr><td>Price on our store</td><td><a href="/3d/product/kingroon-pla-basic-filament/">from 65&nbsp;SAR / kg</a></td><td><a href="/3d/product/filament-pla-1kg/">75&nbsp;SAR / kg</a></td></tr>
              </tbody>
            </table>
          </div>

          <h2>Which one for which print</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Print</th><th>Choose</th></tr></thead>
              <tbody>
                <tr><td>Figures, vases, decor, gifts</td><td>PLA</td></tr>
                <tr><td>First prints and learning</td><td>PLA</td></tr>
                <tr><td>Snap-fit boxes, clips, toys that get dropped</td><td>PLA+</td></tr>
                <tr><td>Tool holders and desk organisers used daily</td><td>PLA+</td></tr>
                <tr><td>Car mounts, outdoor parts</td><td>PETG</td></tr>
              </tbody>
            </table>
          </div>

          <h2>Printing PLA+ on Bambu Lab printers</h2>
          <p>Use a Generic PLA profile and raise the nozzle temperature by 5–10&nbsp;°C, or follow the range on the spool. Everything else, bed temperature, cooling and speed, stays the same as PLA. PLA+ goes in the AMS lite exactly like PLA.</p>

          <h2>Frequently asked questions</h2>
          <h3>Is PLA+ stronger than PLA?</h3>
          <p>It is tougher, meaning it resists cracking and impacts better. Its stiffness and heat resistance are about the same as PLA.</p>
          <h3>Can I mix PLA and PLA+ in one multi-colour print?</h3>
          <p>Yes. They bond to each other well. Print at a temperature that suits both, usually the top of the PLA range.</p>
          <h3>Is PLA+ worth it for beginners?</h3>
          <p>Not necessary. Start with regular PLA; it is cheaper and forgiving. Move to PLA+ for the functional parts you print later.</p>

          <div class="b3d-article__cta">
            <p>PLA and PLA+ filament with delivery across Saudi Arabia</p>
            <a href="/3d/shop/filament/" class="btn btn-primary">Shop filament</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/kingroon-pla-basic-filament-review/">KINGROON PLA Basic review</a>
            <a href="/3d/blog/pla-vs-petg-vs-abs-filament-guide/">PLA vs PETG vs ABS</a>
            <a href="/3d/blog/which-filament-for-which-print/">Which filament for which print</a>
          </div>
''',
        },
        'ar': {
            'headline': 'PLA مقابل PLA+: ما الفرق وأيهما تشتري؟',
            'title': 'الفرق بين فلمنت PLA وPLA+ | Black Arrow 3D',
            'desc': 'شرح الفرق بين PLA وPLA+: ماذا تعني علامة الزائد فعلًا، والمتانة، وحرارة الطباعة، وشكل السطح، والسعر، وأيهما تشتري للهدايا والقطع العملية وللمبتدئين.',
            'meta_line': meta_ar('دليل فلمنت', '5 دقائق قراءة'),
            'lead': 'يبدو PLA+ (ويُباع أيضًا باسم PLA Pro أو Tough PLA) كترقية مباشرة، لكن علامة الزائد تعني أشياء مختلفة من علامة تجارية لأخرى. إليك ما يتغير عمليًا ومتى تستحق التكلفة الإضافية.',
            'card': ('دليل فلمنت', '5 دقائق قراءة', 'ماذا تعني علامة الزائد فعلًا، وكيف يُطبع كل منهما، ومتى يستحق PLA+ السعر الإضافي.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>PLA+ هو PLA مضاف إليه مواد تجعله <strong>أقل هشاشة وأكثر متانة قليلًا</strong>. يُطبع تقريبًا مثل PLA تمامًا، وعادةً بحرارة أعلى بـ 5–10 درجات. للقطع الديكورية والمجسمات والهدايا والنماذج الأولية يكفيك PLA العادي وهو أرخص. اختر PLA+ للقطع التي تُستخدم كثيرًا أو تُركّب بالكبس أو تتعرض للسقوط. وإذا احتاجت القطعة إلى مقاومة حقيقية للحرارة فلا يناسبها أي منهما، واستخدم <a href="/3d/ar/blog/kingroon-petg-basic-filament-guide/">PETG</a>.</p>

          <h2>ماذا تعني علامة الزائد؟</h2>
          <p>لا يوجد معيار موحد لـ PLA+، فكل شركة تضيف موادها الخاصة إلى PLA لتحسين مقاومة الصدمات والتصاق الطبقات. والنتيجة عادةً:</p>
          <ul>
            <li><strong>أقل هشاشة:</strong> تنحني القطع الرفيعة قليلًا قبل أن تتشقق.</li>
            <li><strong>التصاق أفضل للطبقات:</strong> احتمال أقل لانفصال القطعة على خط طبقة.</li>
            <li><strong>حرارة طباعة أعلى قليلًا:</strong> غالبًا 205–225 درجة بدلًا من 190–210.</li>
            <li><strong>حدّ حرارة مشابه:</strong> يلين تقريبًا عند نفس حرارة PLA.</li>
          </ul>

          <h2>مقارنة جنبًا إلى جنب</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA</th><th>PLA+</th></tr></thead>
              <tbody>
                <tr><td>سهولة الطباعة</td><td>الأسهل</td><td>بنفس السهولة</td></tr>
                <tr><td>المتانة</td><td>صلب وقد ينكسر</td><td>أمتن وأقل هشاشة</td></tr>
                <tr><td>السطح</td><td>نظيف ولامع قليلًا</td><td>غالبًا أكثر مطفأً</td></tr>
                <tr><td>مقاومة الحرارة</td><td>منخفضة</td><td>منخفضة</td></tr>
                <tr><td>السعر في متجرنا</td><td><a href="/3d/ar/product/kingroon-pla-basic-filament/">من 65 ريالًا للكيلو</a></td><td><a href="/3d/ar/product/filament-pla-1kg/">75 ريالًا للكيلو</a></td></tr>
              </tbody>
            </table>
          </div>

          <h2>أيهما لأي طبعة؟</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الطبعة</th><th>الاختيار</th></tr></thead>
              <tbody>
                <tr><td>مجسمات ومزهريات وديكور وهدايا</td><td>PLA</td></tr>
                <tr><td>الطبعات الأولى والتعلّم</td><td>PLA</td></tr>
                <tr><td>علب بالكبس ومشابك وألعاب تتعرض للسقوط</td><td>PLA+</td></tr>
                <tr><td>حوامل أدوات ومنظمات مكتب تُستخدم يوميًا</td><td>PLA+</td></tr>
                <tr><td>حوامل السيارة والقطع الخارجية</td><td>PETG</td></tr>
              </tbody>
            </table>
          </div>

          <h2>طباعة PLA+ على طابعات بامبو لاب</h2>
          <p>استخدم ملف Generic PLA وارفع حرارة الفوهة 5–10 درجات، أو اتبع المدى المكتوب على البكرة. أما حرارة السرير والتبريد والسرعة فتبقى كما في PLA. ويعمل PLA+ في AMS lite تمامًا مثل PLA.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>هل PLA+ أقوى من PLA؟</h3>
          <p>هو أمتن، أي يقاوم التشقق والصدمات بشكل أفضل، لكن صلابته ومقاومته للحرارة قريبة من PLA.</p>
          <h3>هل يمكن خلط PLA وPLA+ في طبعة متعددة الألوان؟</h3>
          <p>نعم، فهما يلتصقان ببعضهما جيدًا. اطبع على حرارة تناسب الاثنين، وغالبًا أعلى مدى PLA.</p>
          <h3>هل يستحق PLA+ للمبتدئين؟</h3>
          <p>ليس ضروريًا. ابدأ بـ PLA العادي فهو أرخص وأسهل، وانتقل إلى PLA+ لاحقًا للقطع العملية.</p>

          <div class="b3d-article__cta">
            <p>فلمنت PLA وPLA+ مع التوصيل لجميع مدن المملكة</p>
            <a href="/3d/ar/shop/filament/" class="btn btn-primary">تسوّق الفلمنت</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/kingroon-pla-basic-filament-review/">مراجعة KINGROON PLA Basic</a>
            <a href="/3d/ar/blog/pla-vs-petg-vs-abs-filament-guide/">PLA وPETG وABS</a>
            <a href="/3d/ar/blog/which-filament-for-which-print/">أي فلمنت لأي طبعة</a>
          </div>
''',
        },
    },
    # ------------------------------------------------------------------
    # 4. Best filament for Bambu Lab A1 / A1 mini / AMS lite
    # ------------------------------------------------------------------
    {
        'slug': 'best-filament-for-bambu-lab-a1-ams-lite',
        'en': {
            'headline': 'Best Filament for the Bambu Lab A1, A1 mini and AMS lite',
            'title': 'Best Filament for Bambu Lab A1 and AMS lite | Black Arrow 3D',
            'desc': 'Which filament to use on the Bambu Lab A1, A1 mini and A2L with AMS lite: PLA, PLA+ and PETG settings, what not to load in the AMS lite, spool tips and multi-colour advice.',
            'meta_line': meta('Filament guide', '6 min read'),
            'lead': 'The Bambu Lab A1 series is the most popular printer family in Saudi Arabia, and most owners use the AMS lite for multi-colour prints. This guide covers which filaments work best, which ones to keep out of the AMS lite, and how to avoid feeding problems.',
            'card': ('Filament guide', '6 min read', 'PLA, PLA+ and PETG on the A1 series, what to keep out of the AMS lite and how to avoid tangles.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>For the <a href="/3d/product/bambu-lab-a1-mini/">A1 mini</a>, <a href="/3d/product/bambu-lab-a1/">A1</a> and <a href="/3d/product/bambu-lab-a2l/">A2L</a>, <strong>PLA</strong> is the best everyday filament and the easiest in the AMS lite. Add <strong>PETG</strong> for heat- and water-resistant parts and <strong>PLA+</strong> for tougher functional prints. Keep flexible TPU out of the AMS lite: feed it directly from the external spool holder. The A1 series is an open printer, so ABS and ASA are not a good match.</p>

          <h2>What the A1 series can print</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Filament</th><th>Works on A1 series?</th><th>In the AMS lite?</th><th>Notes</th></tr></thead>
              <tbody>
                <tr><td>PLA</td><td>Yes</td><td>Yes</td><td>Best choice for colours and gifts</td></tr>
                <tr><td>PLA+</td><td>Yes</td><td>Yes</td><td>Tougher everyday parts</td></tr>
                <tr><td>PETG</td><td>Yes</td><td>Yes</td><td>Heat, sun and water; dry it first</td></tr>
                <tr><td>TPU (flexible)</td><td>Yes</td><td>No</td><td>Use the external spool holder</td></tr>
                <tr><td>ABS / ASA</td><td>Not recommended</td><td>No</td><td>Needs an enclosed printer such as the <a href="/3d/product/bambu-lab-p2s/">P2S</a></td></tr>
              </tbody>
            </table>
          </div>

          <h2>Feeding tips for the AMS lite</h2>
          <ul>
            <li><strong>Neat winding:</strong> tangles cause most AMS lite jams. When you remove a spool, always clip the end into the spool edge.</li>
            <li><strong>Spool size:</strong> standard 1 kg spools fit. Very wide or very small spools may not turn freely; check before loading.</li>
            <li><strong>Cardboard spools:</strong> they can shed dust and slip on the rollers. If you use them often, a plastic spool adapter ring helps.</li>
            <li><strong>Cut the end straight</strong> with a sharp angle before loading so it does not catch inside the feeder.</li>
            <li><strong>Tell the printer what is loaded:</strong> set the material and colour for each slot in Bambu Studio or Bambu Handy so the right temperature is used.</li>
          </ul>

          <h2>Multi-colour without wasting a spool</h2>
          <p>Every colour change purges some filament. To keep waste down:</p>
          <ol>
            <li>Put colours that change most often on the same layers, and use <strong>fewer colour changes per layer</strong>.</li>
            <li>Turn on <em>flush into infill</em> or <em>flush into object</em> where the inside of the print is hidden.</li>
            <li>Use darker colours after lighter ones where you can: going from white to black purges less than black to white.</li>
          </ol>
          <p>Our <a href="/3d/blog/multi-color-3d-printing-explained/">multi-colour printing guide</a> explains purge and prime towers in more detail.</p>

          <h2>A starter set we recommend</h2>
          <p>For a new A1 or A1 mini owner: black and white <a href="/3d/product/kingroon-pla-basic-filament/">KINGROON PLA Basic</a> for most prints, two bright colours for multi-colour gifts, and one spool of <a href="/3d/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a> for parts that go in the car. Keep a spare <a href="/3d/product/bambu-hotend-a1-series/">A1 hot end</a> on hand; it is the part that wears with use.</p>

          <h2>Frequently asked questions</h2>
          <h3>Do I have to use Bambu Lab filament on an A1?</h3>
          <p>No. Any good 1.75 mm filament works. Bambu filament has RFID tags that load settings automatically; with other brands you choose the profile yourself, which takes a few seconds.</p>
          <h3>Can the AMS lite mix PLA and PETG in one print?</h3>
          <p>It can load both, but they do not bond well to each other, so use one material per part. PLA works well as an easy-release support under PETG.</p>
          <h3>Why does my AMS lite fail to load filament?</h3>
          <p>Usually a tangle on the spool, a bent filament end or a spool that does not turn freely. Re-cut the end, rewind loose loops and make sure the spool spins easily.</p>

          <div class="b3d-article__cta">
            <p>Filament for your A1 series, delivered across Saudi Arabia</p>
            <a href="/3d/shop/filament/" class="btn btn-primary">Shop filament</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/bambu-lab-a1-mini-setup-guide/">Bambu Lab A1 mini setup guide</a>
            <a href="/3d/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/">A1 vs A1 mini vs A2L</a>
            <a href="/3d/blog/bambu-a1-hotend-replacement-guide/">Replacing the A1 hot end</a>
          </div>
''',
        },
        'ar': {
            'headline': 'أفضل فلمنت لطابعات بامبو لاب A1 وA1 ميني وAMS lite',
            'title': 'أفضل فلمنت لطابعة بامبو لاب A1 وAMS lite | Black Arrow 3D',
            'desc': 'أي فلمنت تستخدم مع بامبو لاب A1 وA1 ميني وA2L ونظام AMS lite: إعدادات PLA وPLA+ وPETG، وما لا يجب تحميله في AMS lite، ونصائح البكرات والطباعة متعددة الألوان.',
            'meta_line': meta_ar('دليل فلمنت', '6 دقائق قراءة'),
            'lead': 'سلسلة بامبو لاب A1 هي أكثر الطابعات انتشارًا في السعودية، ويستخدم معظم أصحابها AMS lite للطباعة متعددة الألوان. يشرح هذا الدليل أفضل أنواع الفلمنت، وما يجب إبعاده عن AMS lite، وكيف تتجنب مشاكل التغذية.',
            'card': ('دليل فلمنت', '6 دقائق قراءة', 'PLA وPLA+ وPETG على سلسلة A1، وما لا يُحمّل في AMS lite، وكيف تتجنب تشابك الخيط.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>مع <a href="/3d/ar/product/bambu-lab-a1-mini/">A1 ميني</a> و<a href="/3d/ar/product/bambu-lab-a1/">A1</a> و<a href="/3d/ar/product/bambu-lab-a2l/">A2L</a> يكون <strong>PLA</strong> أفضل فلمنت للاستخدام اليومي والأسهل في AMS lite. أضف <strong>PETG</strong> للقطع التي تتحمل الحرارة والماء، و<strong>PLA+</strong> للقطع العملية الأكثر متانة. أبعد فلمنت TPU المرن عن AMS lite وغذّه مباشرة من حامل البكرة الخارجي. وبما أن سلسلة A1 طابعات مفتوحة، فإن ABS وASA لا يناسبانها.</p>

          <h2>ماذا تطبع سلسلة A1؟</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الفلمنت</th><th>يعمل على A1؟</th><th>في AMS lite؟</th><th>ملاحظات</th></tr></thead>
              <tbody>
                <tr><td>PLA</td><td>نعم</td><td>نعم</td><td>الأفضل للألوان والهدايا</td></tr>
                <tr><td>PLA+</td><td>نعم</td><td>نعم</td><td>قطع يومية أمتن</td></tr>
                <tr><td>PETG</td><td>نعم</td><td>نعم</td><td>للحرارة والشمس والماء، جففه أولًا</td></tr>
                <tr><td>TPU المرن</td><td>نعم</td><td>لا</td><td>استخدم حامل البكرة الخارجي</td></tr>
                <tr><td>ABS / ASA</td><td>غير مستحسن</td><td>لا</td><td>يحتاج طابعة مغلقة مثل <a href="/3d/ar/product/bambu-lab-p2s/">P2S</a></td></tr>
              </tbody>
            </table>
          </div>

          <h2>نصائح التغذية في AMS lite</h2>
          <ul>
            <li><strong>لفّ مرتب:</strong> التشابك هو سبب معظم انحشارات AMS lite. عند إخراج البكرة ثبّت طرف الخيط دائمًا في حافة البكرة.</li>
            <li><strong>حجم البكرة:</strong> البكرات القياسية بوزن 1 كجم مناسبة. البكرات العريضة جدًا أو الصغيرة جدًا قد لا تدور بحرية، فتحقق قبل التحميل.</li>
            <li><strong>البكرات الكرتونية:</strong> قد تتساقط منها أتربة وتنزلق على البكرات الدوارة. إن كنت تستخدمها كثيرًا فحلقة محوّل بلاستيكية تساعد.</li>
            <li><strong>اقطع طرف الخيط بزاوية حادة</strong> قبل التحميل حتى لا يعلق داخل وحدة التغذية.</li>
            <li><strong>أخبر الطابعة بما حمّلته:</strong> حدد المادة واللون لكل فتحة في Bambu Studio أو Bambu Handy حتى تُستخدم الحرارة الصحيحة.</li>
          </ul>

          <h2>تعدد الألوان دون إهدار بكرة</h2>
          <p>كل تبديل للون يهدر بعض الفلمنت. لتقليل الهدر:</p>
          <ol>
            <li>قلّل <strong>عدد تبديلات الألوان في الطبقة الواحدة</strong> قدر الإمكان.</li>
            <li>فعّل خيار التنظيف داخل الحشو (flush into infill) أو داخل القطعة حين يكون داخلها مخفيًا.</li>
            <li>انتقل من الألوان الفاتحة إلى الداكنة حيث أمكن، فالانتقال من الأبيض إلى الأسود يهدر أقل من العكس.</li>
          </ol>
          <p>يشرح <a href="/3d/ar/blog/multi-color-3d-printing-explained/">دليل الطباعة متعددة الألوان</a> أبراج التنظيف بالتفصيل.</p>

          <h2>مجموعة بداية ننصح بها</h2>
          <p>لمالك A1 أو A1 ميني جديد: <a href="/3d/ar/product/kingroon-pla-basic-filament/">KINGROON PLA Basic</a> بالأسود والأبيض لمعظم الطبعات، ولونان زاهيان للهدايا متعددة الألوان، وبكرة <a href="/3d/ar/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a> للقطع التي توضع في السيارة. واحتفظ بـ <a href="/3d/ar/product/bambu-hotend-a1-series/">رأس طباعة A1</a> احتياطي، فهو القطعة التي تستهلك مع الاستخدام.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>هل يجب استخدام فلمنت بامبو لاب مع A1؟</h3>
          <p>لا، أي فلمنت جيد بقطر 1.75 مم يعمل. فلمنت بامبو يحتوي على شريحة RFID تحمّل الإعدادات تلقائيًا، ومع العلامات الأخرى تختار الملف بنفسك خلال ثوانٍ.</p>
          <h3>هل يمكن خلط PLA وPETG في طبعة واحدة عبر AMS lite؟</h3>
          <p>يمكن تحميل الاثنين، لكنهما لا يلتصقان ببعضهما جيدًا، فاستخدم مادة واحدة لكل قطعة. ويصلح PLA كدعامات سهلة الإزالة تحت PETG.</p>
          <h3>لماذا يفشل AMS lite في تحميل الفلمنت؟</h3>
          <p>غالبًا بسبب تشابك على البكرة، أو طرف خيط منحنٍ، أو بكرة لا تدور بحرية. أعد قص الطرف، وأعد لفّ الحلقات المرتخية، وتأكد أن البكرة تدور بسهولة.</p>

          <div class="b3d-article__cta">
            <p>فلمنت لسلسلة A1 مع التوصيل لجميع مدن المملكة</p>
            <a href="/3d/ar/shop/filament/" class="btn btn-primary">تسوّق الفلمنت</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/bambu-lab-a1-mini-setup-guide/">دليل تشغيل بامبو لاب A1 ميني</a>
            <a href="/3d/ar/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/">مقارنة A1 وA1 ميني وA2L</a>
            <a href="/3d/ar/blog/bambu-a1-hotend-replacement-guide/">تغيير رأس طباعة A1</a>
          </div>
''',
        },
    },
    # ------------------------------------------------------------------
    # 5. Filament price + cost per print
    # ------------------------------------------------------------------
    {
        'slug': '3d-printer-filament-price-saudi-arabia',
        'en': {
            'headline': '3D Printer Filament Price in Saudi Arabia (2026) and What a Print Really Costs',
            'title': '3D Printer Filament Price in Saudi Arabia 2026 | Black Arrow 3D',
            'desc': 'How much 3D printer filament costs in Saudi Arabia in 2026: PLA, PLA+ and PETG prices per kg in SAR, how to work out the cost of any print, and how to spend less on filament.',
            'meta_line': meta('Price guide', '6 min read'),
            'lead': 'Filament is the running cost of 3D printing. Here are current prices per kilogram in Saudi Arabia, a simple way to work out what any print costs, and the habits that cut filament waste.',
            'card': ('Price guide', '6 min read', 'PLA, PLA+ and PETG prices per kg in SAR, and how to work out the cost of any print.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>In Saudi Arabia, everyday 1 kg spools of PLA and PETG cost roughly <strong>55–100&nbsp;SAR</strong>, with branded and speciality filaments higher. On our store, <a href="/3d/product/kingroon-pla-basic-filament/">KINGROON PLA Basic</a> and <a href="/3d/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a> are <strong><span data-b3d-price="kingroon-petg-basic-filament">65</span>&nbsp;SAR per 1 kg</strong> and <a href="/3d/product/filament-pla-1kg/">PLA+</a> is <strong><span data-b3d-price="filament-pla-1kg">75</span>&nbsp;SAR</strong>, VAT included. At 65&nbsp;SAR a kilo, filament costs about <strong>6.5 halalas per gram</strong>, so most small prints cost less than a cup of coffee in material.</p>

          <h2>Prices on our store</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Filament</th><th>Spool</th><th>Price (SAR, incl. VAT)</th><th>Per gram</th></tr></thead>
              <tbody>
                <tr><td><a href="/3d/product/kingroon-pla-basic-filament/">KINGROON PLA Basic</a></td><td>1 kg, 1.75 mm</td><td><span data-b3d-price="kingroon-pla-basic-filament">65</span></td><td>0.065</td></tr>
                <tr><td><a href="/3d/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a></td><td>1 kg, 1.75 mm</td><td><span data-b3d-price="kingroon-petg-basic-filament">65</span></td><td>0.065</td></tr>
                <tr><td><a href="/3d/product/filament-pla-1kg/">PLA+ Filament</a></td><td>1 kg, 1.75 mm</td><td><span data-b3d-price="filament-pla-1kg">75</span></td><td>0.075</td></tr>
              </tbody>
            </table>
          </div>
          <p>Prices and colours in stock are always current on the product pages.</p>

          <h2>How to work out the cost of a print</h2>
          <ol>
            <li>Slice the model. Bambu Studio, OrcaSlicer and other slicers show the <strong>filament weight in grams</strong> before you print.</li>
            <li>Multiply the grams by the price per gram. Example: 120 g × 0.065 = <strong>7.80&nbsp;SAR</strong>.</li>
            <li>For multi-colour prints, include the purge waste the slicer shows as well.</li>
            <li>Add a little for failed prints and electricity. A small printer uses only a few halalas of electricity per hour at Saudi home tariffs.</li>
          </ol>

          <h2>Typical prints and their filament cost</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Print</th><th>Weight</th><th>Cost at 65&nbsp;SAR/kg</th></tr></thead>
              <tbody>
                <tr><td>Keychain</td><td>5–10 g</td><td>0.33–0.65&nbsp;SAR</td></tr>
                <tr><td>Cable clips (set of 10)</td><td>15–20 g</td><td>about 1&nbsp;SAR</td></tr>
                <tr><td>Phone stand</td><td>40–60 g</td><td>2.60–3.90&nbsp;SAR</td></tr>
                <tr><td>Game controller stand</td><td>100–150 g</td><td>6.50–9.75&nbsp;SAR</td></tr>
                <tr><td>Large vase or lamp</td><td>250–400 g</td><td>16–26&nbsp;SAR</td></tr>
              </tbody>
            </table>
          </div>

          <h2>Five ways to spend less on filament</h2>
          <ol>
            <li><strong>Lower the infill.</strong> 10–15% is enough for most decorative prints.</li>
            <li><strong>Use fewer supports</strong> by rotating the model so overhangs face up.</li>
            <li><strong>Plan colour changes</strong> to cut purge waste on multi-colour prints. See our <a href="/3d/blog/best-filament-for-bambu-lab-a1-ams-lite/">AMS lite guide</a>.</li>
            <li><strong>Keep spools dry.</strong> Wet filament causes failed prints, which is the most expensive waste of all.</li>
            <li><strong>Buy in bundles</strong> of the colours you use most, and combine filament with other items to reach free delivery.</li>
          </ol>

          <h2>Delivery</h2>
          <p>''' + DELIVERY_EN + '''</p>

          <h2>Frequently asked questions</h2>
          <h3>How much is a 1 kg spool of PLA in Saudi Arabia?</h3>
          <p>Everyday PLA is roughly 55–100&nbsp;SAR per kilogram. KINGROON PLA Basic is 65&nbsp;SAR on our store, VAT included.</p>
          <h3>Is PETG more expensive than PLA?</h3>
          <p>Often slightly, but on our store KINGROON PETG Basic and PLA Basic are the same price, 65&nbsp;SAR per kg.</p>
          <h3>How many prints do I get from 1 kg?</h3>
          <p>Around 100 keychain-sized prints, 15–25 phone stands, or 3–4 large vases. Your slicer shows the exact weight for each model.</p>

          <div class="b3d-article__cta">
            <p>See every filament with live stock and SAR prices</p>
            <a href="/3d/shop/filament/" class="btn btn-primary">Shop filament</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/custom-3d-printing-cost-saudi-arabia/">Custom 3D printing cost</a>
            <a href="/3d/blog/kingroon-pla-basic-filament-review/">KINGROON PLA Basic review</a>
            <a href="/3d/blog/pla-vs-pla-plus-difference/">PLA vs PLA+</a>
          </div>
''',
        },
        'ar': {
            'headline': 'أسعار فلمنت الطابعة ثلاثية الأبعاد في السعودية 2026 وتكلفة الطبعة الفعلية',
            'title': 'أسعار فلمنت الطباعة ثلاثية الأبعاد في السعودية 2026 | Black Arrow 3D',
            'desc': 'كم سعر فلمنت الطابعة ثلاثية الأبعاد في السعودية 2026: أسعار PLA وPLA+ وPETG للكيلو بالريال، وطريقة حساب تكلفة أي طبعة، وكيف تنفق أقل على الفلمنت.',
            'meta_line': meta_ar('دليل أسعار', '6 دقائق قراءة'),
            'lead': 'الفلمنت هو التكلفة المستمرة للطباعة ثلاثية الأبعاد. إليك الأسعار الحالية للكيلو في السعودية، وطريقة بسيطة لحساب تكلفة أي طبعة، والعادات التي تقلل هدر الفلمنت.',
            'card': ('دليل أسعار', '6 دقائق قراءة', 'أسعار PLA وPLA+ وPETG للكيلو بالريال، وكيف تحسب تكلفة أي طبعة.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>في السعودية تكلّف بكرات PLA وPETG اليومية بوزن 1 كجم حوالي <strong>55–100 ريال</strong>، وأسعار العلامات المعروفة والأنواع الخاصة أعلى. في متجرنا سعر <a href="/3d/ar/product/kingroon-pla-basic-filament/">KINGROON PLA Basic</a> و<a href="/3d/ar/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a> هو <strong><span data-b3d-price="kingroon-petg-basic-filament">65</span> ريالًا للكيلو</strong>، و<a href="/3d/ar/product/filament-pla-1kg/">PLA+</a> بسعر <strong><span data-b3d-price="filament-pla-1kg">75</span> ريالًا</strong>، شاملة ضريبة القيمة المضافة. وبسعر 65 ريالًا للكيلو يكلّف الغرام حوالي <strong>6.5 هللة</strong>، أي أن مادة معظم الطبعات الصغيرة أرخص من كوب قهوة.</p>

          <h2>الأسعار في متجرنا</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الفلمنت</th><th>البكرة</th><th>السعر (ريال شامل الضريبة)</th><th>للغرام</th></tr></thead>
              <tbody>
                <tr><td><a href="/3d/ar/product/kingroon-pla-basic-filament/">KINGROON PLA Basic</a></td><td>1 كجم، 1.75 مم</td><td><span data-b3d-price="kingroon-pla-basic-filament">65</span></td><td>0.065</td></tr>
                <tr><td><a href="/3d/ar/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a></td><td>1 كجم، 1.75 مم</td><td><span data-b3d-price="kingroon-petg-basic-filament">65</span></td><td>0.065</td></tr>
                <tr><td><a href="/3d/ar/product/filament-pla-1kg/">فلمنت PLA+</a></td><td>1 كجم، 1.75 مم</td><td><span data-b3d-price="filament-pla-1kg">75</span></td><td>0.075</td></tr>
              </tbody>
            </table>
          </div>
          <p>الأسعار والألوان المتوفرة محدّثة دائمًا في صفحات المنتجات.</p>

          <h2>كيف تحسب تكلفة الطبعة</h2>
          <ol>
            <li>قطّع النموذج. يعرض Bambu Studio وOrcaSlicer وغيرهما <strong>وزن الفلمنت بالغرام</strong> قبل الطباعة.</li>
            <li>اضرب الغرامات في سعر الغرام. مثال: 120 غرامًا × 0.065 = <strong>7.80 ريال</strong>.</li>
            <li>في الطبعات متعددة الألوان أضف أيضًا هدر التنظيف الذي يعرضه البرنامج.</li>
            <li>أضف هامشًا بسيطًا للطبعات الفاشلة والكهرباء. الطابعة الصغيرة تستهلك بضع هللات فقط من الكهرباء في الساعة بتعرفة المنازل في السعودية.</li>
          </ol>

          <h2>طبعات شائعة وتكلفة فلمنتها</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الطبعة</th><th>الوزن</th><th>التكلفة بسعر 65 ريالًا للكيلو</th></tr></thead>
              <tbody>
                <tr><td>ميدالية مفاتيح</td><td>5–10 غرامات</td><td>0.33–0.65 ريال</td></tr>
                <tr><td>مشابك كابلات (10 قطع)</td><td>15–20 غرامًا</td><td>حوالي ريال</td></tr>
                <tr><td>حامل جوال</td><td>40–60 غرامًا</td><td>2.60–3.90 ريال</td></tr>
                <tr><td>حامل يد ألعاب</td><td>100–150 غرامًا</td><td>6.50–9.75 ريال</td></tr>
                <tr><td>مزهرية أو مصباح كبير</td><td>250–400 غرام</td><td>16–26 ريالًا</td></tr>
              </tbody>
            </table>
          </div>

          <h2>خمس طرق لتنفق أقل على الفلمنت</h2>
          <ol>
            <li><strong>قلّل نسبة الحشو.</strong> 10–15% تكفي لمعظم القطع الديكورية.</li>
            <li><strong>قلّل الدعامات</strong> بتدوير النموذج بحيث تتجه البروزات للأعلى.</li>
            <li><strong>خطط لتبديل الألوان</strong> لتقليل هدر التنظيف في الطبعات متعددة الألوان. راجع <a href="/3d/ar/blog/best-filament-for-bambu-lab-a1-ams-lite/">دليل AMS lite</a>.</li>
            <li><strong>احفظ البكرات جافة.</strong> الفلمنت الرطب يسبب طبعات فاشلة، وهي أغلى أنواع الهدر.</li>
            <li><strong>اشترِ مجموعات</strong> من الألوان التي تستخدمها أكثر، واجمع الفلمنت مع منتجات أخرى للوصول إلى التوصيل المجاني.</li>
          </ol>

          <h2>التوصيل</h2>
          <p>''' + DELIVERY_AR + '''</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>كم سعر بكرة PLA بوزن 1 كجم في السعودية؟</h3>
          <p>سعر PLA اليومي حوالي 55–100 ريال للكيلو، وسعر KINGROON PLA Basic في متجرنا 65 ريالًا شاملة الضريبة.</p>
          <h3>هل PETG أغلى من PLA؟</h3>
          <p>غالبًا بقليل، لكن في متجرنا سعر KINGROON PETG Basic وPLA Basic واحد، 65 ريالًا للكيلو.</p>
          <h3>كم طبعة تخرج من 1 كجم؟</h3>
          <p>حوالي 100 طبعة بحجم الميدالية، أو 15–25 حامل جوال، أو 3–4 مزهريات كبيرة. يعرض برنامج التقطيع الوزن الدقيق لكل نموذج.</p>

          <div class="b3d-article__cta">
            <p>كل أنواع الفلمنت مع المخزون والأسعار بالريال</p>
            <a href="/3d/ar/shop/filament/" class="btn btn-primary">تسوّق الفلمنت</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/custom-3d-printing-cost-saudi-arabia/">تكلفة الطباعة حسب الطلب</a>
            <a href="/3d/ar/blog/kingroon-pla-basic-filament-review/">مراجعة KINGROON PLA Basic</a>
            <a href="/3d/ar/blog/pla-vs-pla-plus-difference/">PLA مقابل PLA+</a>
          </div>
''',
        },
    },
    # ------------------------------------------------------------------
    # 6. Bambu Lab P2S Combo
    # ------------------------------------------------------------------
    {
        'slug': 'bambu-lab-p2s-combo-review-saudi',
        'en': {
            'headline': 'Bambu Lab P2S Combo in Saudi Arabia: Who It Is For and What You Get',
            'title': 'Bambu Lab P2S Combo Review and Price in KSA | Black Arrow 3D',
            'desc': 'Bambu Lab P2S Combo with AMS 2 Pro in Saudi Arabia: specs, price in SAR, how it compares with the A1 and A2L, which filaments it opens up and who should buy it.',
            'meta_line': meta('Printer guide', '7 min read'),
            'lead': 'The Bambu Lab P2S is the step up from the open A1 series: an enclosed, fast printer that handles more materials. Here is what the Combo with AMS 2 Pro includes, how it compares with the A1 and A2L, and who should spend the extra.',
            'card': ('Printer guide', '7 min read', 'Enclosed, fast and multi-material: what the P2S Combo adds over the A1 series and who it suits.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>The <a href="/3d/product/bambu-lab-p2s/">Bambu Lab P2S Combo</a> is for buyers who want an <strong>enclosed printer</strong>: for workshops, small businesses, engineering students and hobbyists who want to print more than PLA and PETG. It has a 256 × 256 × 256 mm build volume, a 300&nbsp;°C hot end, a 110&nbsp;°C bed and comes with the <strong>AMS 2 Pro</strong> for multi-colour printing. If you only print PLA gifts and decor, an <a href="/3d/product/bambu-lab-a1/">A1 Combo</a> or <a href="/3d/product/bambu-lab-a2l/">A2L Combo</a> costs less and does the job.</p>

          <h2>Key specs</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Spec</th><th>Bambu Lab P2S</th></tr></thead>
              <tbody>
                <tr><td>Build volume</td><td>256 × 256 × 256 mm</td></tr>
                <tr><td>Max hot end temperature</td><td>300&nbsp;°C</td></tr>
                <tr><td>Max bed temperature</td><td>110&nbsp;°C</td></tr>
                <tr><td>Max speed / acceleration</td><td>500 mm/s / 20,000 mm/s²</td></tr>
                <tr><td>Multi-colour</td><td>AMS 2 Pro in the Combo</td></tr>
                <tr><td>Connectivity</td><td>Wi-Fi, Bambu Handy, Bambu Studio</td></tr>
              </tbody>
            </table>
          </div>

          <h2>What the enclosure changes</h2>
          <p>An enclosure keeps the print area warm and draft-free. That matters for materials that shrink and warp as they cool, such as ABS and ASA, and it helps with large PETG parts too. It also keeps noise and dust down in an office or shop, and keeps curious hands away from the moving parts, which is useful in schools and family homes.</p>

          <h2>P2S vs A1 vs A2L</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th><a href="/3d/product/bambu-lab-a1/">A1 Combo</a></th><th><a href="/3d/product/bambu-lab-a2l/">A2L Combo</a></th><th><a href="/3d/product/bambu-lab-p2s/">P2S Combo</a></th></tr></thead>
              <tbody>
                <tr><td>Build volume</td><td>256³ mm</td><td>330 × 320 × 325 mm</td><td>256³ mm</td></tr>
                <tr><td>Enclosed</td><td>No</td><td>No</td><td>Yes</td></tr>
                <tr><td>Bed max</td><td>100&nbsp;°C</td><td>80&nbsp;°C</td><td>110&nbsp;°C</td></tr>
                <tr><td>Multi-colour unit</td><td>AMS lite</td><td>AMS lite</td><td>AMS 2 Pro</td></tr>
                <tr><td>Best for</td><td>PLA/PETG at home</td><td>Big PLA/PETG prints</td><td>More materials, business use</td></tr>
              </tbody>
            </table>
          </div>
          <p>Current prices are on each product page. For the full Bambu Lab line-up see our <a href="/3d/blog/bambu-lab-printers-saudi-arabia-prices/">Bambu Lab prices in Saudi Arabia</a> guide.</p>

          <h2>Who should buy the P2S</h2>
          <ul>
            <li><strong>Small businesses</strong> printing products to sell, where reliability and print quality across many hours matter.</li>
            <li><strong>Engineering students and makers</strong> who need tougher, heat-resistant parts.</li>
            <li><strong>Offices and schools</strong> that want the moving parts and noise behind a door.</li>
            <li><strong>Anyone upgrading</strong> from an A1 mini who keeps hitting the limits of an open printer.</li>
          </ul>

          <h2>Buying it from Black Arrow 3D</h2>
          <p>The P2S Combo is sold with the manufacturer’s warranty and set-up help in Arabic and English. Every printer order ships with <strong>free Regular delivery</strong> anywhere in Saudi Arabia, and you can pay by bank transfer, mada, card, Apple Pay, Tabby or Tamara.</p>

          <h2>Frequently asked questions</h2>
          <h3>What is the difference between the P2S and the P2S Combo?</h3>
          <p>The Combo adds the AMS 2 Pro, which holds four spools for multi-colour and multi-material printing. The printer itself is the same.</p>
          <h3>Can the P2S print ABS and ASA?</h3>
          <p>Yes. Its enclosure and 110&nbsp;°C bed make it a much better match for ABS and ASA than open printers like the A1 series.</p>
          <h3>Is the P2S good for beginners?</h3>
          <p>Yes. Calibration is automatic and it uses the same Bambu Studio and Bambu Handy apps as the A1. It costs more than a beginner usually needs to spend, though.</p>

          <div class="b3d-article__cta">
            <p>Bambu Lab P2S Combo with free delivery across Saudi Arabia</p>
            <a href="/3d/product/bambu-lab-p2s/" class="btn btn-primary">See price and stock</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/bambu-lab-a2l-combo-guide-saudi/">Bambu Lab A2L Combo guide</a>
            <a href="/3d/blog/bambu-lab-a1-combo-review-saudi/">Bambu Lab A1 Combo review</a>
            <a href="/3d/blog/start-3d-printing-business-saudi-arabia/">Start a 3D printing business</a>
          </div>
''',
        },
        'ar': {
            'headline': 'بامبو لاب P2S كومبو في السعودية: لمن تناسب وماذا تحصل عليه',
            'title': 'مراجعة وسعر بامبو لاب P2S كومبو في السعودية | Black Arrow 3D',
            'desc': 'طابعة بامبو لاب P2S كومبو مع AMS 2 Pro في السعودية: المواصفات، والسعر بالريال، والمقارنة مع A1 وA2L، والمواد التي تتيحها، ولمن تناسب.',
            'meta_line': meta_ar('دليل طابعات', '7 دقائق قراءة'),
            'lead': 'بامبو لاب P2S هي الخطوة التالية بعد سلسلة A1 المفتوحة: طابعة مغلقة وسريعة تتعامل مع مواد أكثر. إليك ما تتضمنه نسخة الكومبو مع AMS 2 Pro، ومقارنتها مع A1 وA2L، ومن يستحق أن يدفع الفرق.',
            'card': ('دليل طابعات', '7 دقائق قراءة', 'مغلقة وسريعة ومتعددة المواد: ما الذي تضيفه P2S كومبو على سلسلة A1 ولمن تناسب.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p><a href="/3d/ar/product/bambu-lab-p2s/">بامبو لاب P2S كومبو</a> مخصصة لمن يريد <strong>طابعة مغلقة</strong>: للورش والأعمال الصغيرة وطلاب الهندسة والهواة الذين يريدون الطباعة بأكثر من PLA وPETG. حجم الطباعة 256 × 256 × 256 مم، وحرارة الفوهة حتى 300 درجة، والسرير حتى 110 درجات، وتأتي مع <strong>AMS 2 Pro</strong> للطباعة متعددة الألوان. أما إذا كنت تطبع هدايا وديكورًا من PLA فقط، فإن <a href="/3d/ar/product/bambu-lab-a1/">A1 كومبو</a> أو <a href="/3d/ar/product/bambu-lab-a2l/">A2L كومبو</a> أقل تكلفة وتؤدي المهمة.</p>

          <h2>أهم المواصفات</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>المواصفة</th><th>بامبو لاب P2S</th></tr></thead>
              <tbody>
                <tr><td>حجم الطباعة</td><td>256 × 256 × 256 مم</td></tr>
                <tr><td>أقصى حرارة للفوهة</td><td>300 درجة</td></tr>
                <tr><td>أقصى حرارة للسرير</td><td>110 درجات</td></tr>
                <tr><td>أقصى سرعة / تسارع</td><td>500 مم/ث / 20,000 مم/ث²</td></tr>
                <tr><td>تعدد الألوان</td><td>AMS 2 Pro في نسخة الكومبو</td></tr>
                <tr><td>الاتصال</td><td>Wi-Fi وBambu Handy وBambu Studio</td></tr>
              </tbody>
            </table>
          </div>

          <h2>ماذا يغيّر الهيكل المغلق؟</h2>
          <p>يحافظ الهيكل المغلق على دفء منطقة الطباعة ويمنع تيارات الهواء، وهذا مهم للمواد التي تنكمش وتتشوه عند التبريد مثل ABS وASA، ويساعد أيضًا في قطع PETG الكبيرة. كما يقلل الضجيج والغبار في المكتب أو المحل، ويبعد الأيدي الفضولية عن الأجزاء المتحركة، وهو مفيد في المدارس والمنازل.</p>

          <h2>P2S مقابل A1 مقابل A2L</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th><a href="/3d/ar/product/bambu-lab-a1/">A1 كومبو</a></th><th><a href="/3d/ar/product/bambu-lab-a2l/">A2L كومبو</a></th><th><a href="/3d/ar/product/bambu-lab-p2s/">P2S كومبو</a></th></tr></thead>
              <tbody>
                <tr><td>حجم الطباعة</td><td>256³ مم</td><td>330 × 320 × 325 مم</td><td>256³ مم</td></tr>
                <tr><td>مغلقة</td><td>لا</td><td>لا</td><td>نعم</td></tr>
                <tr><td>أقصى حرارة للسرير</td><td>100 درجة</td><td>80 درجة</td><td>110 درجات</td></tr>
                <tr><td>وحدة تعدد الألوان</td><td>AMS lite</td><td>AMS lite</td><td>AMS 2 Pro</td></tr>
                <tr><td>الأفضل لـ</td><td>PLA وPETG في المنزل</td><td>طبعات PLA وPETG الكبيرة</td><td>مواد أكثر واستخدام تجاري</td></tr>
              </tbody>
            </table>
          </div>
          <p>الأسعار الحالية في صفحة كل منتج. ولمعرفة تشكيلة بامبو لاب كاملة راجع دليل <a href="/3d/ar/blog/bambu-lab-printers-saudi-arabia-prices/">أسعار بامبو لاب في السعودية</a>.</p>

          <h2>لمن تناسب P2S؟</h2>
          <ul>
            <li><strong>الأعمال الصغيرة</strong> التي تطبع منتجات للبيع، حيث تهم الموثوقية وجودة الطباعة لساعات طويلة.</li>
            <li><strong>طلاب الهندسة والصنّاع</strong> الذين يحتاجون إلى قطع أمتن وتتحمل الحرارة.</li>
            <li><strong>المكاتب والمدارس</strong> التي تريد الأجزاء المتحركة والضجيج خلف باب مغلق.</li>
            <li><strong>من يريد الترقية</strong> من A1 ميني ويصطدم باستمرار بحدود الطابعة المفتوحة.</li>
          </ul>

          <h2>شراؤها من Black Arrow 3D</h2>
          <p>تُباع P2S كومبو بضمان الشركة المصنّعة مع مساعدة في التشغيل بالعربية والإنجليزية. كل طلب طابعة يُشحن <strong>بتوصيل عادي مجاني</strong> إلى أي مكان في المملكة، ويمكنك الدفع بالتحويل البنكي أو مدى أو البطاقة أو Apple Pay أو تابي أو تمارا.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>ما الفرق بين P2S وP2S كومبو؟</h3>
          <p>تضيف نسخة الكومبو وحدة AMS 2 Pro التي تحمل أربع بكرات للطباعة متعددة الألوان والمواد، والطابعة نفسها واحدة.</p>
          <h3>هل تطبع P2S بخامات ABS وASA؟</h3>
          <p>نعم، فهيكلها المغلق وسريرها الذي يصل إلى 110 درجات يجعلانها أنسب بكثير لـ ABS وASA من الطابعات المفتوحة مثل سلسلة A1.</p>
          <h3>هل P2S مناسبة للمبتدئين؟</h3>
          <p>نعم، فالمعايرة تلقائية وتستخدم نفس تطبيقي Bambu Studio وBambu Handy مثل A1، لكن سعرها أعلى مما يحتاجه المبتدئ عادةً.</p>

          <div class="b3d-article__cta">
            <p>بامبو لاب P2S كومبو مع توصيل مجاني لجميع مدن المملكة</p>
            <a href="/3d/ar/product/bambu-lab-p2s/" class="btn btn-primary">شاهد السعر والمخزون</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/bambu-lab-a2l-combo-guide-saudi/">دليل بامبو لاب A2L كومبو</a>
            <a href="/3d/ar/blog/bambu-lab-a1-combo-review-saudi/">مراجعة بامبو لاب A1 كومبو</a>
            <a href="/3d/ar/blog/start-3d-printing-business-saudi-arabia/">ابدأ مشروع طباعة ثلاثية الأبعاد</a>
          </div>
''',
        },
    },
    # ------------------------------------------------------------------
    # 7. Bambu Lab A2L Combo
    # ------------------------------------------------------------------
    {
        'slug': 'bambu-lab-a2l-combo-guide-saudi',
        'en': {
            'headline': 'Bambu Lab A2L Combo in Saudi Arabia: Big Prints and Four Colours',
            'title': 'Bambu Lab A2L Combo Guide and Price in KSA | Black Arrow 3D',
            'desc': 'Bambu Lab A2L Combo in Saudi Arabia: 330 x 320 x 325 mm build volume with AMS lite, what you can print on it, how it compares with the A1 and P2S, and who should buy it.',
            'meta_line': meta('Printer guide', '6 min read'),
            'lead': 'The Bambu Lab A2L Combo takes the easy A1-series experience to a much larger build plate and includes the AMS lite for four-colour printing. Here is what the extra size is good for and who it suits.',
            'card': ('Printer guide', '6 min read', 'A large build plate, AMS lite included and automatic calibration: what the A2L Combo is good for.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>The <a href="/3d/product/bambu-lab-a2l/">Bambu Lab A2L Combo</a> is the printer to choose when the A1 is too small. It prints up to <strong>330 × 320 × 325 mm</strong> (about 34 litres), includes the <strong>AMS lite</strong> for up to four colours and calibrates itself, including flow dynamics. It is an open printer, so it suits PLA, PLA+ and PETG, the materials most home users and gift makers print anyway.</p>

          <h2>Key specs</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Spec</th><th>Bambu Lab A2L Combo</th></tr></thead>
              <tbody>
                <tr><td>Build volume</td><td>330 × 320 × 325 mm (~34.3 L)</td></tr>
                <tr><td>Max speed / acceleration</td><td>500 mm/s / 10,000 mm/s²</td></tr>
                <tr><td>Max hot end temperature</td><td>300&nbsp;°C</td></tr>
                <tr><td>Max bed temperature</td><td>80&nbsp;°C</td></tr>
                <tr><td>Nozzle</td><td>0.4 mm standard (0.2 / 0.6 / 0.8 mm available)</td></tr>
                <tr><td>Multi-colour</td><td>AMS lite included, up to 4 colours</td></tr>
                <tr><td>Calibration</td><td>Fully automatic, incl. flow dynamics</td></tr>
              </tbody>
            </table>
          </div>

          <h2>What the bigger plate is good for</h2>
          <ul>
            <li><strong>Large single pieces:</strong> helmets, cosplay parts, big lamps and vases, wall art and architecture models in one piece instead of glued halves.</li>
            <li><strong>Batches:</strong> a full plate of keychains, coasters or gifts in one run, useful for events and small shops.</li>
            <li><strong>Long parts:</strong> rails, organisers and storage boxes that do not fit on a 256 mm plate.</li>
          </ul>

          <h2>A2L vs A1 vs P2S</h2>
          <p>Compared with the <a href="/3d/product/bambu-lab-a1/">A1</a>, the A2L adds roughly 60% more plate area and includes the AMS lite in the Combo. Compared with the <a href="/3d/product/bambu-lab-p2s/">P2S</a>, it is open rather than enclosed, so it is not the printer for ABS or ASA. Our <a href="/3d/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/">A1 vs A1 mini vs A2L comparison</a> goes into more detail.</p>

          <h2>Tips for big prints</h2>
          <ol>
            <li><strong>Clean the plate</strong> with warm water and dish soap; large parts need a perfect first layer.</li>
            <li><strong>Use a brim</strong> on tall or thin-based parts so they do not lift at the corners.</li>
            <li><strong>Check the spool:</strong> a big print can use more than half a kilogram. Make sure the spool has enough, or load a second spool of the same colour in the AMS lite.</li>
            <li><strong>Keep air conditioning off the printer.</strong> A cold draft across a large open printer can cause warping, even with PLA.</li>
          </ol>

          <h2>Buying it from Black Arrow 3D</h2>
          <p>The A2L Combo comes with the manufacturer’s warranty and set-up help in Arabic and English. Every printer order ships with <strong>free Regular delivery</strong> across Saudi Arabia. Pay by bank transfer, mada, card, Apple Pay, Tabby or Tamara.</p>

          <h2>Frequently asked questions</h2>
          <h3>Is the A2L good for beginners?</h3>
          <p>Yes. It works like the A1 series: automatic calibration, the Bambu Handy app and ready-made profiles. Choose it if you already know you want large prints.</p>
          <h3>Can the A2L print PETG?</h3>
          <p>Yes. With an 80&nbsp;°C bed and a 300&nbsp;°C hot end, PETG prints well. Use a textured plate.</p>
          <h3>Does the A2L Combo include filament?</h3>
          <p>Check the product page for what is in the box, and add spools of <a href="/3d/shop/filament/">PLA or PETG</a> to the same order.</p>

          <div class="b3d-article__cta">
            <p>Bambu Lab A2L Combo with free delivery across Saudi Arabia</p>
            <a href="/3d/product/bambu-lab-a2l/" class="btn btn-primary">See price and stock</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/bambu-lab-p2s-combo-review-saudi/">Bambu Lab P2S Combo guide</a>
            <a href="/3d/blog/bambu-lab-a1-combo-review-saudi/">Bambu Lab A1 Combo review</a>
            <a href="/3d/blog/best-filament-for-bambu-lab-a1-ams-lite/">Best filament for the AMS lite</a>
          </div>
''',
        },
        'ar': {
            'headline': 'بامبو لاب A2L كومبو في السعودية: طبعات كبيرة وأربعة ألوان',
            'title': 'دليل وسعر بامبو لاب A2L كومبو في السعودية | Black Arrow 3D',
            'desc': 'طابعة بامبو لاب A2L كومبو في السعودية: حجم طباعة 330 × 320 × 325 مم مع AMS lite، وماذا تطبع عليها، ومقارنتها مع A1 وP2S، ولمن تناسب.',
            'meta_line': meta_ar('دليل طابعات', '6 دقائق قراءة'),
            'lead': 'تنقل بامبو لاب A2L كومبو سهولة سلسلة A1 إلى سرير طباعة أكبر بكثير، وتأتي مع AMS lite للطباعة بأربعة ألوان. إليك فائدة الحجم الإضافي ولمن تناسب.',
            'card': ('دليل طابعات', '6 دقائق قراءة', 'سرير كبير وAMS lite مضمّن ومعايرة تلقائية: ماذا تقدم A2L كومبو.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p><a href="/3d/ar/product/bambu-lab-a2l/">بامبو لاب A2L كومبو</a> هي الطابعة التي تختارها عندما تكون A1 صغيرة عليك. تطبع حتى <strong>330 × 320 × 325 مم</strong> (حوالي 34 لترًا)، وتشمل <strong>AMS lite</strong> لما يصل إلى أربعة ألوان، وتعاير نفسها تلقائيًا بما في ذلك ديناميكية التدفق. وهي طابعة مفتوحة، لذا تناسب PLA وPLA+ وPETG، وهي المواد التي يطبع بها معظم المستخدمين المنزليين وصانعي الهدايا.</p>

          <h2>أهم المواصفات</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>المواصفة</th><th>بامبو لاب A2L كومبو</th></tr></thead>
              <tbody>
                <tr><td>حجم الطباعة</td><td>330 × 320 × 325 مم (~34.3 لتر)</td></tr>
                <tr><td>أقصى سرعة / تسارع</td><td>500 مم/ث / 10,000 مم/ث²</td></tr>
                <tr><td>أقصى حرارة للفوهة</td><td>300 درجة</td></tr>
                <tr><td>أقصى حرارة للسرير</td><td>80 درجة</td></tr>
                <tr><td>الفوهة</td><td>0.4 مم قياسية (0.2 / 0.6 / 0.8 مم متوفرة)</td></tr>
                <tr><td>تعدد الألوان</td><td>AMS lite مضمّن، حتى 4 ألوان</td></tr>
                <tr><td>المعايرة</td><td>تلقائية بالكامل بما فيها ديناميكية التدفق</td></tr>
              </tbody>
            </table>
          </div>

          <h2>فائدة السرير الأكبر</h2>
          <ul>
            <li><strong>قطع كبيرة كاملة:</strong> خوذات وقطع أزياء ومصابيح ومزهريات كبيرة ولوحات جدارية ومجسمات معمارية بقطعة واحدة بدلًا من نصفين ملصوقين.</li>
            <li><strong>دفعات:</strong> سرير كامل من الميداليات أو القواعد أو الهدايا في مرة واحدة، وهذا مفيد للمناسبات والمتاجر الصغيرة.</li>
            <li><strong>قطع طويلة:</strong> مجاري ومنظمات وصناديق تخزين لا تتسع على سرير 256 مم.</li>
          </ul>

          <h2>A2L مقابل A1 مقابل P2S</h2>
          <p>مقارنة بـ <a href="/3d/ar/product/bambu-lab-a1/">A1</a> تضيف A2L حوالي 60% من مساحة السرير، وتشمل نسخة الكومبو AMS lite. ومقارنة بـ <a href="/3d/ar/product/bambu-lab-p2s/">P2S</a> فهي مفتوحة وليست مغلقة، لذا ليست الطابعة المناسبة لـ ABS أو ASA. تشرح <a href="/3d/ar/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/">مقارنة A1 وA1 ميني وA2L</a> التفاصيل.</p>

          <h2>نصائح للطبعات الكبيرة</h2>
          <ol>
            <li><strong>نظّف السرير</strong> بالماء الدافئ وسائل الصحون، فالقطع الكبيرة تحتاج طبقة أولى مثالية.</li>
            <li><strong>استخدم حافة (Brim)</strong> للقطع الطويلة أو ذات القاعدة الرفيعة حتى لا ترتفع زواياها.</li>
            <li><strong>تحقق من البكرة:</strong> قد تستهلك الطبعة الكبيرة أكثر من نصف كيلو، فتأكد أن البكرة تكفي أو حمّل بكرة ثانية من نفس اللون في AMS lite.</li>
            <li><strong>أبعد هواء المكيف عن الطابعة.</strong> تيار الهواء البارد على طابعة مفتوحة كبيرة قد يسبب التشوه حتى مع PLA.</li>
          </ol>

          <h2>شراؤها من Black Arrow 3D</h2>
          <p>تأتي A2L كومبو بضمان الشركة المصنّعة مع مساعدة في التشغيل بالعربية والإنجليزية، وكل طلب طابعة يُشحن <strong>بتوصيل عادي مجاني</strong> لجميع مدن المملكة. ادفع بالتحويل البنكي أو مدى أو البطاقة أو Apple Pay أو تابي أو تمارا.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>هل A2L مناسبة للمبتدئين؟</h3>
          <p>نعم، فهي تعمل مثل سلسلة A1: معايرة تلقائية وتطبيق Bambu Handy وملفات جاهزة. اخترها إذا كنت تعرف مسبقًا أنك تريد طبعات كبيرة.</p>
          <h3>هل تطبع A2L فلمنت PETG؟</h3>
          <p>نعم، فسريرها يصل إلى 80 درجة والفوهة إلى 300 درجة، وPETG يُطبع جيدًا عليها مع لوح محبب.</p>
          <h3>هل تأتي A2L كومبو مع فلمنت؟</h3>
          <p>راجع صفحة المنتج لمعرفة محتويات العلبة، وأضف بكرات <a href="/3d/ar/shop/filament/">PLA أو PETG</a> إلى نفس الطلب.</p>

          <div class="b3d-article__cta">
            <p>بامبو لاب A2L كومبو مع توصيل مجاني لجميع مدن المملكة</p>
            <a href="/3d/ar/product/bambu-lab-a2l/" class="btn btn-primary">شاهد السعر والمخزون</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/bambu-lab-p2s-combo-review-saudi/">دليل بامبو لاب P2S كومبو</a>
            <a href="/3d/ar/blog/bambu-lab-a1-combo-review-saudi/">مراجعة بامبو لاب A1 كومبو</a>
            <a href="/3d/ar/blog/best-filament-for-bambu-lab-a1-ams-lite/">أفضل فلمنت لـ AMS lite</a>
          </div>
''',
        },
    },
    # ------------------------------------------------------------------
    # 8. Bambu Lab A1 Combo
    # ------------------------------------------------------------------
    {
        'slug': 'bambu-lab-a1-combo-review-saudi',
        'en': {
            'headline': 'Bambu Lab A1 Combo Review: The All-Rounder for Saudi Homes',
            'title': 'Bambu Lab A1 Combo Review and Price in KSA | Black Arrow 3D',
            'desc': 'Bambu Lab A1 Combo review for Saudi Arabia: 256 mm build volume, AMS lite for four colours, what it prints well, A1 vs A1 mini, setup tips and who should buy it.',
            'meta_line': meta('Printer review', '7 min read'),
            'lead': 'The Bambu Lab A1 Combo sits between the compact A1 mini and the large A2L: a full-size 256 mm printer with the AMS lite for four-colour printing. For many homes it is the one printer that does it all.',
            'card': ('Printer review', '7 min read', 'Full-size 256 mm plate, AMS lite, automatic everything: why the A1 Combo suits most homes.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>Buy the <a href="/3d/product/bambu-lab-a1/">Bambu Lab A1 Combo</a> if you want one printer for gifts, toys, household parts and multi-colour models without thinking about size. Its <strong>256 × 256 × 256 mm</strong> build volume fits most everyday prints in one piece, the included <strong>AMS lite</strong> prints up to four colours, and calibration is automatic. Choose the <a href="/3d/product/bambu-lab-a1-mini/">A1 mini Combo</a> if space or budget is tight, or the <a href="/3d/product/bambu-lab-a2l/">A2L Combo</a> for bigger prints.</p>

          <h2>Key specs</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Spec</th><th>Bambu Lab A1</th></tr></thead>
              <tbody>
                <tr><td>Build volume</td><td>256 × 256 × 256 mm</td></tr>
                <tr><td>Max hot end / bed</td><td>300&nbsp;°C / 100&nbsp;°C</td></tr>
                <tr><td>Nozzle</td><td>0.4 mm standard (0.2 / 0.6 / 0.8 mm supported)</td></tr>
                <tr><td>Max speed / acceleration</td><td>500 mm/s / 10,000 mm/s²</td></tr>
                <tr><td>Multi-colour</td><td>AMS lite, up to 4 colours (included in the Combo)</td></tr>
                <tr><td>Filament</td><td>PLA, PETG, TPU and similar</td></tr>
              </tbody>
            </table>
          </div>

          <h2>A1 or A1 mini?</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th><a href="/3d/product/bambu-lab-a1-mini/">A1 mini Combo</a></th><th><a href="/3d/product/bambu-lab-a1/">A1 Combo</a></th></tr></thead>
              <tbody>
                <tr><td>Build volume</td><td>180 × 180 × 180 mm</td><td>256 × 256 × 256 mm</td></tr>
                <tr><td>Bed max</td><td>80&nbsp;°C</td><td>100&nbsp;°C</td></tr>
                <tr><td>Desk space</td><td>Small</td><td>Medium</td></tr>
                <tr><td>Good for</td><td>Small gifts, keychains, learning</td><td>Almost everything for the home</td></tr>
              </tbody>
            </table>
          </div>
          <p>The extra 76 mm on each side matters more than it sounds: the A1 plate has about double the area of the A1 mini, so helmets, larger stands and storage boxes fit in one piece.</p>

          <h2>What it prints well</h2>
          <ul>
            <li>Multi-colour gifts, name plates and keychains with the AMS lite.</li>
            <li>Phone and controller stands, desk organisers and household fixes.</li>
            <li>Toys and figures in PLA, and car mounts and outdoor parts in <a href="/3d/blog/kingroon-petg-basic-filament-guide/">PETG</a>.</li>
          </ul>

          <h2>Setup tips</h2>
          <ol>
            <li>Place it on a solid table; the bed moves front to back, so leave space behind and in front.</li>
            <li>Connect it to Wi-Fi with the Bambu Handy app and update the firmware first.</li>
            <li>Load PLA in the AMS lite and start with a model from MakerWorld to see it work.</li>
            <li>Keep the plate clean and the spools dry. Our <a href="/3d/blog/bambu-lab-a1-mini-setup-guide/">A1 mini setup guide</a> applies to the A1 too.</li>
          </ol>

          <h2>Buying it from Black Arrow 3D</h2>
          <p>The A1 Combo comes with the manufacturer’s warranty and help in Arabic and English. Every printer order gets <strong>free Regular delivery</strong> across Saudi Arabia. Spare <a href="/3d/product/bambu-hotend-a1-series/">A1-series hot ends</a> and <a href="/3d/shop/filament/">filament</a> are on the same store.</p>

          <h2>Frequently asked questions</h2>
          <h3>Is the Bambu Lab A1 good for beginners?</h3>
          <p>Yes. It levels, calibrates and detects problems by itself, and the app has thousands of ready-to-print models.</p>
          <h3>What is the difference between the A1 and the A1 Combo?</h3>
          <p>The Combo includes the AMS lite for four-colour printing. The printer is the same.</p>
          <h3>Can I add the AMS lite later?</h3>
          <p>Yes, but buying the Combo is usually cheaper than buying the AMS lite separately later.</p>

          <div class="b3d-article__cta">
            <p>Bambu Lab A1 Combo with free delivery across Saudi Arabia</p>
            <a href="/3d/product/bambu-lab-a1/" class="btn btn-primary">See price and stock</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/bambu-lab-a1-mini-combo-review/">Bambu Lab A1 mini Combo review</a>
            <a href="/3d/blog/bambu-lab-a2l-combo-guide-saudi/">Bambu Lab A2L Combo guide</a>
            <a href="/3d/blog/best-filament-for-bambu-lab-a1-ams-lite/">Best filament for the AMS lite</a>
          </div>
''',
        },
        'ar': {
            'headline': 'مراجعة بامبو لاب A1 كومبو: الطابعة الشاملة لمنازل السعودية',
            'title': 'مراجعة وسعر بامبو لاب A1 كومبو في السعودية | Black Arrow 3D',
            'desc': 'مراجعة بامبو لاب A1 كومبو للسعودية: حجم طباعة 256 مم وAMS lite لأربعة ألوان، وما تطبعه بجودة، والمقارنة مع A1 ميني، ونصائح التشغيل، ولمن تناسب.',
            'meta_line': meta_ar('مراجعة طابعة', '7 دقائق قراءة'),
            'lead': 'تقع بامبو لاب A1 كومبو بين A1 ميني الصغيرة وA2L الكبيرة: طابعة كاملة الحجم 256 مم مع AMS lite للطباعة بأربعة ألوان. ولكثير من المنازل هي الطابعة الواحدة التي تكفي لكل شيء.',
            'card': ('مراجعة طابعة', '7 دقائق قراءة', 'سرير كامل 256 مم وAMS lite وكل شيء تلقائي: لماذا تناسب A1 كومبو معظم المنازل.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>اشترِ <a href="/3d/ar/product/bambu-lab-a1/">بامبو لاب A1 كومبو</a> إذا أردت طابعة واحدة للهدايا والألعاب والقطع المنزلية والنماذج متعددة الألوان دون التفكير في الحجم. حجم الطباعة <strong>256 × 256 × 256 مم</strong> يتسع لمعظم الطبعات اليومية بقطعة واحدة، ووحدة <strong>AMS lite</strong> المضمّنة تطبع حتى أربعة ألوان، والمعايرة تلقائية. اختر <a href="/3d/ar/product/bambu-lab-a1-mini/">A1 ميني كومبو</a> إذا كانت المساحة أو الميزانية محدودة، أو <a href="/3d/ar/product/bambu-lab-a2l/">A2L كومبو</a> للطبعات الأكبر.</p>

          <h2>أهم المواصفات</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>المواصفة</th><th>بامبو لاب A1</th></tr></thead>
              <tbody>
                <tr><td>حجم الطباعة</td><td>256 × 256 × 256 مم</td></tr>
                <tr><td>أقصى حرارة للفوهة / السرير</td><td>300 درجة / 100 درجة</td></tr>
                <tr><td>الفوهة</td><td>0.4 مم قياسية (تدعم 0.2 / 0.6 / 0.8 مم)</td></tr>
                <tr><td>أقصى سرعة / تسارع</td><td>500 مم/ث / 10,000 مم/ث²</td></tr>
                <tr><td>تعدد الألوان</td><td>AMS lite حتى 4 ألوان (مضمّن في الكومبو)</td></tr>
                <tr><td>الفلمنت</td><td>PLA وPETG وTPU وما شابه</td></tr>
              </tbody>
            </table>
          </div>

          <h2>A1 أم A1 ميني؟</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th><a href="/3d/ar/product/bambu-lab-a1-mini/">A1 ميني كومبو</a></th><th><a href="/3d/ar/product/bambu-lab-a1/">A1 كومبو</a></th></tr></thead>
              <tbody>
                <tr><td>حجم الطباعة</td><td>180 × 180 × 180 مم</td><td>256 × 256 × 256 مم</td></tr>
                <tr><td>أقصى حرارة للسرير</td><td>80 درجة</td><td>100 درجة</td></tr>
                <tr><td>المساحة على المكتب</td><td>صغيرة</td><td>متوسطة</td></tr>
                <tr><td>مناسبة لـ</td><td>الهدايا الصغيرة والميداليات والتعلّم</td><td>تقريبًا كل احتياجات المنزل</td></tr>
              </tbody>
            </table>
          </div>
          <p>الـ 76 مم الإضافية في كل اتجاه أهم مما تبدو، فمساحة سرير A1 حوالي ضعف مساحة A1 ميني، لذا تتسع الخوذات والحوامل الأكبر وصناديق التخزين بقطعة واحدة.</p>

          <h2>ماذا تطبع بجودة؟</h2>
          <ul>
            <li>هدايا ولوحات أسماء وميداليات متعددة الألوان مع AMS lite.</li>
            <li>حوامل الجوال ويد الألعاب ومنظمات المكتب وإصلاحات المنزل.</li>
            <li>ألعاب ومجسمات من PLA، وحوامل سيارة وقطع خارجية من <a href="/3d/ar/blog/kingroon-petg-basic-filament-guide/">PETG</a>.</li>
          </ul>

          <h2>نصائح التشغيل</h2>
          <ol>
            <li>ضعها على طاولة ثابتة، فالسرير يتحرك للأمام والخلف، لذا اترك مساحة خلفها وأمامها.</li>
            <li>اربطها بشبكة Wi-Fi عبر تطبيق Bambu Handy وحدّث البرنامج الثابت أولًا.</li>
            <li>حمّل PLA في AMS lite وابدأ بنموذج من MakerWorld لترى أداءها.</li>
            <li>حافظ على نظافة السرير وجفاف البكرات. ينطبق <a href="/3d/ar/blog/bambu-lab-a1-mini-setup-guide/">دليل تشغيل A1 ميني</a> على A1 أيضًا.</li>
          </ol>

          <h2>شراؤها من Black Arrow 3D</h2>
          <p>تأتي A1 كومبو بضمان الشركة المصنّعة مع مساعدة بالعربية والإنجليزية، وكل طلب طابعة يحصل على <strong>توصيل عادي مجاني</strong> لجميع مدن المملكة. وتجد في المتجر نفسه <a href="/3d/ar/product/bambu-hotend-a1-series/">رؤوس طباعة A1 الاحتياطية</a> و<a href="/3d/ar/shop/filament/">الفلمنت</a>.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>هل بامبو لاب A1 مناسبة للمبتدئين؟</h3>
          <p>نعم، فهي تضبط الاستواء وتعاير وتكتشف المشاكل بنفسها، والتطبيق يحتوي على آلاف النماذج الجاهزة للطباعة.</p>
          <h3>ما الفرق بين A1 وA1 كومبو؟</h3>
          <p>تشمل نسخة الكومبو وحدة AMS lite للطباعة بأربعة ألوان، والطابعة نفسها واحدة.</p>
          <h3>هل يمكن إضافة AMS lite لاحقًا؟</h3>
          <p>نعم، لكن شراء الكومبو غالبًا أرخص من شراء AMS lite منفصلًا لاحقًا.</p>

          <div class="b3d-article__cta">
            <p>بامبو لاب A1 كومبو مع توصيل مجاني لجميع مدن المملكة</p>
            <a href="/3d/ar/product/bambu-lab-a1/" class="btn btn-primary">شاهد السعر والمخزون</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/bambu-lab-a1-mini-combo-review/">مراجعة بامبو لاب A1 ميني كومبو</a>
            <a href="/3d/ar/blog/bambu-lab-a2l-combo-guide-saudi/">دليل بامبو لاب A2L كومبو</a>
            <a href="/3d/ar/blog/best-filament-for-bambu-lab-a1-ams-lite/">أفضل فلمنت لـ AMS lite</a>
          </div>
''',
        },
    },
    # ------------------------------------------------------------------
    # 9. A1 hot end replacement
    # ------------------------------------------------------------------
    {
        'slug': 'bambu-a1-hotend-replacement-guide',
        'en': {
            'headline': 'Bambu Lab A1 and A1 mini Hot End: When to Replace It and Which Nozzle Size to Choose',
            'title': 'Bambu A1 / A1 mini Hot End and Nozzle Guide | Black Arrow 3D',
            'desc': 'When to replace the hot end on a Bambu Lab A1 or A1 mini, how the tool-free swap works, and which nozzle size to choose: 0.2, 0.4, 0.6 or 0.8 mm, with spare hot ends in Saudi Arabia.',
            'meta_line': meta('How-to', '6 min read'),
            'lead': 'The hot end is the part of an A1 or A1 mini that wears with use, and swapping it is also how you change nozzle size. Here are the signs it is time, how the swap works, and which size fits which job.',
            'card': ('How-to', '6 min read', 'Signs your A1 hot end is worn, how the swap works, and which nozzle size fits which job.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>On the Bambu Lab A1 and A1 mini the nozzle and hot end are one quick-swap unit. Replace it when prints show <strong>under-extrusion that cleaning does not fix</strong>, after a <strong>clog you cannot clear</strong>, or when you want a <strong>different nozzle size</strong>. The swap takes a few minutes without tools. We sell genuine <a href="/3d/product/bambu-hotend-a1-series/">Bambu A1-series hot ends</a> in 0.2, 0.4, 0.6 and 0.8 mm; they fit both the A1 and the A1 mini.</p>

          <h2>Signs the hot end needs replacing</h2>
          <ul>
            <li>Thin, gappy or weak walls even after drying the filament and running calibration.</li>
            <li>A clog that keeps coming back after a cold pull and cleaning. See our <a href="/3d/blog/clogged-3d-printer-nozzle-fix/">clogged nozzle guide</a> first.</li>
            <li>A damaged nozzle tip, for example after a crash into the plate.</li>
            <li>Heater or temperature errors that point to the hot end (check the error code in the Bambu Handy app).</li>
          </ul>

          <h2>How the swap works</h2>
          <ol>
            <li>Heat the nozzle and unload the filament from the printer screen or app.</li>
            <li>Let the hot end cool fully. Never touch a hot nozzle.</li>
            <li>Open the hot end clip on the toolhead and pull the hot end straight out.</li>
            <li>Push the new hot end in until it seats, and close the clip.</li>
            <li>Set the new nozzle size in the printer settings, then run calibration before printing.</li>
          </ol>
          <p>Bambu Lab’s own wiki has a video for each step; follow it if anything looks different on your printer.</p>

          <h2>Which nozzle size for which job</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Nozzle</th><th>Best for</th><th>Trade-off</th></tr></thead>
              <tbody>
                <tr><td>0.2 mm</td><td>Tiny detail: miniatures, small text, jewellery</td><td>Slow; clogs more easily</td></tr>
                <tr><td>0.4 mm</td><td>Everyday printing (the standard size)</td><td>Good balance of speed and detail</td></tr>
                <tr><td>0.6 mm</td><td>Stronger functional parts, faster large prints</td><td>Less fine detail</td></tr>
                <tr><td>0.8 mm</td><td>Big vases, quick drafts, very strong parts</td><td>Visible thick layers</td></tr>
              </tbody>
            </table>
          </div>

          <h2>Make it last longer</h2>
          <ul>
            <li>Keep filament dry; wet filament and dust are the most common causes of clogs.</li>
            <li>Avoid abrasive filaments such as carbon fibre or glow-in-the-dark with a standard stainless steel nozzle.</li>
            <li>Keep a spare 0.4 mm hot end at home so a clog never stops a gift or order.</li>
          </ul>

          <h2>Frequently asked questions</h2>
          <h3>Does the A1 hot end fit the A1 mini?</h3>
          <p>Yes. A1-series hot ends fit both the Bambu Lab A1 and the A1 mini.</p>
          <h3>How often should I replace the hot end?</h3>
          <p>There is no fixed schedule. With PLA and PETG a hot end can last a long time; replace it when print quality drops and cleaning no longer helps.</p>
          <h3>How much is a replacement hot end in Saudi Arabia?</h3>
          <p>On our store A1-series hot ends start from <span data-b3d-price="bambu-hotend-a1-series|0.4mm">100</span>&nbsp;SAR, VAT included. The <a href="/3d/product/bambu-hotend-a1-series/">product page</a> shows the price and stock of each size.</p>

          <div class="b3d-article__cta">
            <p>Genuine Bambu A1-series hot ends, 0.2 to 0.8 mm</p>
            <a href="/3d/product/bambu-hotend-a1-series/" class="btn btn-primary">See sizes and stock</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/clogged-3d-printer-nozzle-fix/">Fix a clogged nozzle</a>
            <a href="/3d/blog/3d-printer-maintenance-guide/">3D printer maintenance guide</a>
            <a href="/3d/shop/accessories/">All accessories</a>
          </div>
''',
        },
        'ar': {
            'headline': 'رأس طباعة بامبو لاب A1 وA1 ميني: متى تغيّره وأي مقاس فوهة تختار',
            'title': 'دليل رأس الطباعة والفوهة لـ بامبو A1 وA1 ميني | Black Arrow 3D',
            'desc': 'متى تغيّر رأس الطباعة في بامبو لاب A1 أو A1 ميني، وكيف يتم التبديل دون أدوات، وأي مقاس فوهة تختار: 0.2 أو 0.4 أو 0.6 أو 0.8 مم، مع رؤوس طباعة احتياطية في السعودية.',
            'meta_line': meta_ar('شرح عملي', '6 دقائق قراءة'),
            'lead': 'رأس الطباعة هو الجزء الذي يستهلك مع الاستخدام في A1 وA1 ميني، وتبديله هو أيضًا طريقة تغيير مقاس الفوهة. إليك علامات الحاجة إلى التغيير، وطريقة التبديل، وأي مقاس يناسب أي عمل.',
            'card': ('شرح عملي', '6 دقائق قراءة', 'علامات تآكل رأس طباعة A1، وطريقة التبديل، وأي مقاس فوهة يناسب أي عمل.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>في بامبو لاب A1 وA1 ميني تكون الفوهة ورأس الطباعة وحدة واحدة سريعة التبديل. غيّرها عندما تُظهر الطبعات <strong>نقصًا في البثق لا يحلّه التنظيف</strong>، أو بعد <strong>انسداد لا يمكن إزالته</strong>، أو عندما تريد <strong>مقاس فوهة مختلفًا</strong>. يستغرق التبديل دقائق ودون أدوات. نبيع <a href="/3d/ar/product/bambu-hotend-a1-series/">رؤوس طباعة بامبو الأصلية لسلسلة A1</a> بمقاسات 0.2 و0.4 و0.6 و0.8 مم، وتناسب A1 وA1 ميني.</p>

          <h2>علامات الحاجة إلى تغيير رأس الطباعة</h2>
          <ul>
            <li>جدران رفيعة أو متقطعة أو ضعيفة حتى بعد تجفيف الفلمنت وتشغيل المعايرة.</li>
            <li>انسداد يتكرر بعد السحب البارد والتنظيف. راجع أولًا <a href="/3d/ar/blog/clogged-3d-printer-nozzle-fix/">دليل انسداد الفوهة</a>.</li>
            <li>رأس فوهة متضرر، مثلًا بعد اصطدامه بالسرير.</li>
            <li>أخطاء في التسخين أو الحرارة تشير إلى رأس الطباعة (تحقق من رمز الخطأ في تطبيق Bambu Handy).</li>
          </ul>

          <h2>طريقة التبديل</h2>
          <ol>
            <li>سخّن الفوهة وأخرج الفلمنت من شاشة الطابعة أو التطبيق.</li>
            <li>اترك رأس الطباعة يبرد تمامًا، ولا تلمس الفوهة الساخنة أبدًا.</li>
            <li>افتح مشبك رأس الطباعة على وحدة الرأس واسحب رأس الطباعة للخارج بشكل مستقيم.</li>
            <li>أدخل رأس الطباعة الجديد حتى يستقر في مكانه وأغلق المشبك.</li>
            <li>حدد مقاس الفوهة الجديد في إعدادات الطابعة، ثم شغّل المعايرة قبل الطباعة.</li>
          </ol>
          <p>يحتوي موقع بامبو لاب الرسمي على فيديو لكل خطوة، فاتبعه إذا بدا أي شيء مختلفًا في طابعتك.</p>

          <h2>أي مقاس فوهة لأي عمل</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الفوهة</th><th>الأفضل لـ</th><th>المقابل</th></tr></thead>
              <tbody>
                <tr><td>0.2 مم</td><td>التفاصيل الدقيقة: المجسمات الصغيرة والنصوص الصغيرة والإكسسوارات</td><td>بطيئة وتنسد بسهولة أكبر</td></tr>
                <tr><td>0.4 مم</td><td>الطباعة اليومية (المقاس القياسي)</td><td>توازن جيد بين السرعة والتفاصيل</td></tr>
                <tr><td>0.6 مم</td><td>قطع عملية أمتن وطبعات كبيرة أسرع</td><td>تفاصيل أقل دقة</td></tr>
                <tr><td>0.8 مم</td><td>مزهريات كبيرة ونماذج سريعة وقطع قوية جدًا</td><td>طبقات سميكة ظاهرة</td></tr>
              </tbody>
            </table>
          </div>

          <h2>اجعله يدوم أطول</h2>
          <ul>
            <li>احفظ الفلمنت جافًا، فالرطوبة والغبار أكثر أسباب الانسداد شيوعًا.</li>
            <li>تجنب الفلمنت الكاشط مثل ألياف الكربون أو المتوهج في الظلام مع الفوهة الفولاذية القياسية.</li>
            <li>احتفظ برأس طباعة احتياطي 0.4 مم في المنزل حتى لا يوقف الانسداد هدية أو طلبًا.</li>
          </ul>

          <h2>الأسئلة الشائعة</h2>
          <h3>هل رأس طباعة A1 يناسب A1 ميني؟</h3>
          <p>نعم، رؤوس طباعة سلسلة A1 تناسب بامبو لاب A1 وA1 ميني.</p>
          <h3>متى يجب تغيير رأس الطباعة؟</h3>
          <p>لا يوجد جدول ثابت. مع PLA وPETG قد يدوم رأس الطباعة طويلًا، وغيّره عندما تنخفض جودة الطباعة ولا يعود التنظيف مفيدًا.</p>
          <h3>كم سعر رأس الطباعة البديل في السعودية؟</h3>
          <p>في متجرنا تبدأ رؤوس طباعة سلسلة A1 من 100 ريال شاملة الضريبة، وتعرض <a href="/3d/ar/product/bambu-hotend-a1-series/">صفحة المنتج</a> السعر والمخزون لكل مقاس.</p>

          <div class="b3d-article__cta">
            <p>رؤوس طباعة بامبو الأصلية لسلسلة A1 من 0.2 إلى 0.8 مم</p>
            <a href="/3d/ar/product/bambu-hotend-a1-series/" class="btn btn-primary">شاهد المقاسات والمخزون</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/clogged-3d-printer-nozzle-fix/">حل انسداد الفوهة</a>
            <a href="/3d/ar/blog/3d-printer-maintenance-guide/">دليل صيانة الطابعة</a>
            <a href="/3d/ar/shop/accessories/">كل الإكسسوارات</a>
          </div>
''',
        },
    },
]
