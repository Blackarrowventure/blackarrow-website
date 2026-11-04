"""Bilingual (EN + AR) KINGROON filament posts (November 2026): the new PETG HS high-speed filament,
and a guide to choosing between KINGROON PLA Basic, PETG Basic and PETG HS.

Data only, same schema as scripts/seo_posts_products.py. Specs, settings and material values are
KINGROON's own: the PLA Basic and PETG HS Technical Data Sheets V1.0 (wiki.kingroon.com, read
4 Nov 2026). KINGROON publishes no data sheet for PETG Basic, so for PETG Basic the posts give no
temperatures and point to the spool label instead. Prices and colours are from the live store
(3d/assets/data/3d-products.json); the posts point to the product pages for current stock.
"""

EN_DATE = 'November 4, 2026'
AR_DATE = '4 نوفمبر 2026'

PLA = '/3d/product/kingroon-pla-basic-filament/'
PETG = '/3d/product/kingroon-petg-basic-filament/'
HS = '/3d/product/kingroon-petg-hs-filament/'
PLA_AR = '/3d/ar/product/kingroon-pla-basic-filament/'
PETG_AR = '/3d/ar/product/kingroon-petg-basic-filament/'
HS_AR = '/3d/ar/product/kingroon-petg-hs-filament/'
HS_POST = '/3d/blog/kingroon-petg-hs-high-speed-filament-guide/'
HS_POST_AR = '/3d/ar/blog/kingroon-petg-hs-high-speed-filament-guide/'
WHICH_POST = '/3d/blog/kingroon-filament-pla-vs-petg-vs-petg-hs/'
WHICH_POST_AR = '/3d/ar/blog/kingroon-filament-pla-vs-petg-vs-petg-hs/'

POSTS = [
    {
        'slug': 'kingroon-petg-hs-high-speed-filament-guide',
        'en': {
            'headline': 'KINGROON PETG HS High-Speed Filament: Settings, Strength and Who It Suits',
            'title': 'KINGROON PETG HS High-Speed Filament Guide (KSA) | Black Arrow 3D',
            'desc': 'KINGROON PETG HS in Saudi Arabia: official print settings, up to 2x the speed of standard PETG, matte finish, heat resistance vs PLA, drying, colours and cost per print.',
            'meta_line': 'Filament guide &middot; ' + EN_DATE + ' &middot; 7 min read',
            'lead': 'KINGROON PETG HS is PETG made for fast printers. KINGROON says it prints up to twice as fast as standard PETG by default, with less stringing and a matte finish. Here are the official settings, how it compares with PLA, and where it earns its place in Saudi heat.',
            'card': ('Filament guide', '7 min read', 'High-speed PETG with a matte finish: official settings, strength vs PLA, heat, drying and colours.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>Choose <a href="''' + HS + '''">KINGROON PETG HS</a> when you want PETG's toughness and heat resistance but print on a fast machine such as a Bambu Lab A1, P2S or a Snapmaker U1. KINGROON says its default print speed is <strong>up to twice as fast as standard PETG</strong>, with less oozing, stringing and clumping, and a <strong>matte finish</strong> that stays even when the speed changes. It prints at <strong>230–260&nbsp;°C</strong> on a <strong>65–75&nbsp;°C</strong> bed. At Black Arrow 3D it costs <strong>65&nbsp;SAR per 1&nbsp;kg</strong> in Silver, Brown, Green, Orange and Yellow.</p>

          <h2>What HS means</h2>
          <p>HS stands for high speed. Ordinary PETG is happiest printed a little slower than PLA: push it fast and it strings, blobs and shows glossy bands wherever the speed changes. KINGROON reformulated PETG HS to flow and cool fast enough for modern high-speed printers, rating it for print speeds under 300&nbsp;mm/s. The matte surface is part of the same idea: KINGROON says it removes the uneven gloss shifts you get with standard PETG during speed changes, so walls look uniform.</p>

          <h2>Official print settings</h2>
          <p>These are KINGROON's recommended settings from the PETG HS Technical Data Sheet V1.0:</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Setting</th><th>KINGROON recommendation</th></tr></thead>
              <tbody>
                <tr><td>Nozzle temperature</td><td>230–260&nbsp;°C</td></tr>
                <tr><td>Bed temperature</td><td>65–75&nbsp;°C</td></tr>
                <tr><td>Build plate</td><td>Smooth PEI or Textured PEI plate</td></tr>
                <tr><td>Bed preparation</td><td>Glue</td></tr>
                <tr><td>Part cooling fan</td><td>0–60%</td></tr>
                <tr><td>Print speed</td><td>under 300&nbsp;mm/s</td></tr>
                <tr><td>Nozzle sizes</td><td>0.2, 0.4, 0.6 and 0.8&nbsp;mm</td></tr>
                <tr><td>Retraction</td><td>0.8–1.4&nbsp;mm at 30–60&nbsp;mm/s</td></tr>
                <tr><td>Chamber temperature</td><td>35–50&nbsp;°C</td></tr>
                <tr><td>Max overhang / bridge</td><td>70° / 30&nbsp;mm</td></tr>
                <tr><td>Supports</td><td>Support for PETG</td></tr>
                <tr><td>Drying before printing</td><td>65&nbsp;°C for 8 hours</td></tr>
                <tr><td>Storage</td><td>under 20% RH, sealed with desiccant</td></tr>
              </tbody>
            </table>
          </div>
          <p>KINGROON printed its own test pieces at 255&nbsp;°C on a 70&nbsp;°C bed, which is a good starting point. On a Bambu Lab printer, start from a <em>Generic PETG</em> profile in Bambu Studio and set the nozzle and bed temperatures above. Glue on a smooth PEI plate matters with PETG: it acts as a release layer as well as an adhesive, so the part does not bond too hard to the plate.</p>

          <h2>PETG HS against PLA Basic</h2>
          <p>Both figures come from KINGROON's own data sheets, tested on standard samples. They are for comparison; real parts depend on the model and settings.</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA Basic</th><th>PETG HS</th></tr></thead>
              <tbody>
                <tr><td>Heat deflection (1.8 / 0.45&nbsp;MPa)</td><td>54 / 57&nbsp;°C</td><td>62 / 69&nbsp;°C</td></tr>
                <tr><td>Softening (Vicat)</td><td>57&nbsp;°C</td><td>70&nbsp;°C</td></tr>
                <tr><td>Impact strength (X-Y)</td><td>26.6&nbsp;kJ/m²</td><td>31.5&nbsp;kJ/m²</td></tr>
                <tr><td>Tensile strength (X-Y / Z)</td><td>35 / 31&nbsp;MPa</td><td>34 / 23&nbsp;MPa</td></tr>
                <tr><td>Bending strength (X-Y / Z)</td><td>76 / 59&nbsp;MPa</td><td>64 / 48&nbsp;MPa</td></tr>
                <tr><td>Stiffness (bending modulus X-Y)</td><td>2750&nbsp;MPa</td><td>2050&nbsp;MPa</td></tr>
                <tr><td>Density</td><td>1.24&nbsp;g/cm³</td><td>1.28&nbsp;g/cm³</td></tr>
                <tr><td>Nozzle / bed</td><td>190–230 / 35–45&nbsp;°C</td><td>230–260 / 65–75&nbsp;°C</td></tr>
              </tbody>
            </table>
          </div>
          <p>The pattern is the usual PLA vs PETG one. PLA is stiffer and bonds layers more strongly. PETG HS takes more heat before it softens and absorbs knocks better, so it is the one for parts that get warm or get handled roughly.</p>

          <h2>Saudi heat</h2>
          <p>PETG HS starts to soften at about 62–70&nbsp;°C, against about 54–57&nbsp;°C for PLA. That makes it the safer choice for things that sit near a window, in a hot store room or outside in the shade, and for cable clips, brackets and hooks. A car parked in the summer sun is harder: a dashboard can get hotter than both, so keep printed parts out of direct sun on the dash, or choose a darker, thicker design and test it first.</p>

          <h2>Drying and storage</h2>
          <p>PETG picks up moisture from the air, and wet PETG strings and pops. KINGROON recommends drying it at <strong>65&nbsp;°C for 8 hours</strong> in a forced-air oven or filament dryer before printing, and keeping it below 20% relative humidity, sealed with desiccant. Do not use a kitchen oven or microwave: KINGROON warns they can damage the filament. In Jeddah, Dammam and Khobar, store opened spools in a sealed box with silica gel. Our <a href="/3d/blog/3d-printing-filament-saudi-heat-humidity/">Saudi heat and humidity guide</a> has more.</p>

          <h2>Colours and price</h2>
          <p>KINGROON PETG HS is <strong>65&nbsp;SAR per 1&nbsp;kg spool</strong> at Black Arrow 3D, VAT included, in <strong>Silver, Brown, Green, Orange and Yellow</strong>. The spool is ABS, 200&nbsp;mm across and 67&nbsp;mm wide. At 65&nbsp;SAR a kilo, filament costs about <strong>0.065&nbsp;SAR per gram</strong>, so a 50&nbsp;g phone stand is about 3.25&nbsp;SAR of filament. Stock is limited; the <a href="''' + HS + '''">product page</a> shows the colours in stock.</p>

          <h2>FAQ</h2>
          <h3>Is KINGROON PETG HS faster than normal PETG?</h3>
          <p>KINGROON says its default print speed is up to twice as fast as standard PETG, rated for print speeds under 300&nbsp;mm/s, with less oozing, stringing and clumping at speed.</p>
          <h3>What temperature should I print KINGROON PETG HS at?</h3>
          <p>KINGROON recommends a nozzle temperature of 230–260&nbsp;°C and a bed temperature of 65–75&nbsp;°C, on a smooth or textured PEI plate with glue, with the part fan at 0–60%.</p>
          <h3>Is PETG HS glossy?</h3>
          <p>No. KINGROON PETG HS has a matte finish, which also hides the gloss bands that ordinary PETG shows where the print speed changes.</p>
          <h3>Is PETG HS better than PLA?</h3>
          <p>For heat and impact, yes: in KINGROON's data it softens at a higher temperature and absorbs more impact. PLA is stiffer, bonds layers more strongly and is easier to print, so it is still the better choice for decor, gifts and display pieces.</p>
          <h3>Does it work on Bambu Lab printers?</h3>
          <p>Yes, it is standard 1.75&nbsp;mm filament. Start from a Generic PETG profile and set KINGROON's temperatures. There is no RFID tag, so set the filament type and colour in the slicer yourself.</p>
          <h3>How much is KINGROON PETG HS in Saudi Arabia?</h3>
          <p>65&nbsp;SAR per 1&nbsp;kg spool at Black Arrow 3D, VAT included, with delivery across Saudi Arabia.</p>

          <div class="b3d-article__cta">
            <p>KINGROON PETG HS, 65 SAR per kilo, in Silver, Brown, Green, Orange and Yellow.</p>
            <a href="''' + HS + '''" class="btn btn-primary">See PETG HS colours</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="''' + WHICH_POST + '''">KINGROON PLA vs PETG vs PETG HS</a>
            <a href="/3d/blog/kingroon-petg-basic-filament-guide/">KINGROON PETG Basic guide</a>
            <a href="/3d/blog/kingroon-pla-basic-filament-review/">KINGROON PLA Basic review</a>
            <a href="/3d/blog/3d-print-stringing-fix/">How to fix stringing</a>
            <a href="/3d/shop/filament/">All filament</a>
          </div>
''',
        },
        'ar': {
            'headline': 'فيلامنت KINGROON PETG HS عالي السرعة: الإعدادات والقوة ولمن يناسب',
            'title': 'دليل فيلامنت KINGROON PETG HS عالي السرعة في السعودية | Black Arrow 3D',
            'desc': 'فيلامنت KINGROON PETG HS في السعودية: إعدادات الطباعة الرسمية، وسرعة تصل إلى ضعف PETG العادي، ولمسة مطفية، ومقاومة الحرارة مقارنة بـ PLA، والتجفيف والألوان وتكلفة الطبعة.',
            'meta_line': 'دليل الفيلامنت &middot; ' + AR_DATE + ' &middot; 7 دقائق قراءة',
            'lead': 'فيلامنت KINGROON PETG HS هو PETG مصنوع للطابعات السريعة. تقول KINGROON إن سرعة طباعته الافتراضية تصل إلى ضعف PETG العادي، مع خيوط أقل ولمسة مطفية. إليك الإعدادات الرسمية ومقارنته بـ PLA وأين يستحق مكانه في حرارة السعودية.',
            'card': ('دليل الفيلامنت', '7 دقائق قراءة', 'PETG عالي السرعة بلمسة مطفية: الإعدادات الرسمية والقوة مقارنة بـ PLA والحرارة والتجفيف والألوان.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <p>اختر <a href="''' + HS_AR + '''">KINGROON PETG HS</a> عندما تريد متانة PETG ومقاومته للحرارة لكنك تطبع على طابعة سريعة مثل بامبو لاب A1 أو P2S أو Snapmaker U1. تقول KINGROON إن سرعة طباعته الافتراضية <strong>تصل إلى ضعف PETG العادي</strong>، مع تسريب وخيوط وتكتل أقل، و<strong>لمسة مطفية</strong> تبقى متجانسة عند تغيّر السرعة. يُطبع على حرارة <strong>230–260 درجة</strong> وسرير بحرارة <strong>65–75 درجة</strong>. سعره في Black Arrow 3D <strong>65 ريالًا للكيلو</strong> بألوان الفضي والبني والأخضر والبرتقالي والأصفر.</p>

          <h2>ماذا تعني HS؟</h2>
          <p>HS اختصار لـ High Speed أي السرعة العالية. يفضّل PETG العادي أن يُطبع أبطأ قليلًا من PLA، وإذا أسرعت به ظهرت الخيوط والكتل وخطوط لامعة حيث تتغير السرعة. أعادت KINGROON تركيب PETG HS ليتدفق ويبرد بسرعة تناسب الطابعات الحديثة عالية السرعة، بسرعة طباعة أقل من 300 مم/ث. واللمسة المطفية جزء من الفكرة نفسها: تقول KINGROON إنها تزيل تفاوت اللمعان الذي يظهر في PETG العادي عند تغيّر السرعة، فتبدو الجدران متجانسة.</p>

          <h2>إعدادات الطباعة الرسمية</h2>
          <p>هذه هي الإعدادات الموصى بها من KINGROON في ورقة البيانات الفنية لـ PETG HS (الإصدار 1.0):</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الإعداد</th><th>توصية KINGROON</th></tr></thead>
              <tbody>
                <tr><td>حرارة الفوهة</td><td>230–260 درجة</td></tr>
                <tr><td>حرارة السرير</td><td>65–75 درجة</td></tr>
                <tr><td>لوح الطباعة</td><td>لوح PEI أملس أو محبب</td></tr>
                <tr><td>تجهيز السرير</td><td>غراء</td></tr>
                <tr><td>مروحة التبريد</td><td>0–60%</td></tr>
                <tr><td>سرعة الطباعة</td><td>أقل من 300 مم/ث</td></tr>
                <tr><td>أحجام الفوهة</td><td>0.2 و0.4 و0.6 و0.8 مم</td></tr>
                <tr><td>السحب العكسي</td><td>0.8–1.4 مم بسرعة 30–60 مم/ث</td></tr>
                <tr><td>حرارة الحجرة</td><td>35–50 درجة</td></tr>
                <tr><td>أقصى زاوية بروز / جسر</td><td>70° / 30 مم</td></tr>
                <tr><td>الدعامات</td><td>دعامات مخصصة لـ PETG</td></tr>
                <tr><td>التجفيف قبل الطباعة</td><td>65 درجة لمدة 8 ساعات</td></tr>
                <tr><td>التخزين</td><td>رطوبة أقل من 20% مع إحكام الإغلاق ومادة مجففة</td></tr>
              </tbody>
            </table>
          </div>
          <p>طبعت KINGROON عينات الاختبار على 255 درجة وسرير بحرارة 70 درجة، وهي نقطة بداية جيدة. على طابعة بامبو لاب ابدأ من ملف <em>Generic PETG</em> في Bambu Studio واضبط حرارة الفوهة والسرير كما في الجدول. الغراء على لوح PEI الأملس مهم مع PETG: فهو طبقة فاصلة تمنع التصاق القطعة باللوح أكثر من اللازم.</p>

          <h2>مقارنة PETG HS مع PLA Basic</h2>
          <p>الأرقام من أوراق البيانات الرسمية لـ KINGROON على عينات قياسية، وهي للمقارنة فقط؛ القطع الفعلية تعتمد على المجسم والإعدادات.</p>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA Basic</th><th>PETG HS</th></tr></thead>
              <tbody>
                <tr><td>درجة الانحراف الحراري (1.8 / 0.45 ميجاباسكال)</td><td>54 / 57 درجة</td><td>62 / 69 درجة</td></tr>
                <tr><td>درجة التليّن (فيكات)</td><td>57 درجة</td><td>70 درجة</td></tr>
                <tr><td>مقاومة الصدمات (X-Y)</td><td>26.6 كيلوجول/م²</td><td>31.5 كيلوجول/م²</td></tr>
                <tr><td>مقاومة الشد (X-Y / Z)</td><td>35 / 31 ميجاباسكال</td><td>34 / 23 ميجاباسكال</td></tr>
                <tr><td>مقاومة الانحناء (X-Y / Z)</td><td>76 / 59 ميجاباسكال</td><td>64 / 48 ميجاباسكال</td></tr>
                <tr><td>الصلابة (معامل الانحناء X-Y)</td><td>2750 ميجاباسكال</td><td>2050 ميجاباسكال</td></tr>
                <tr><td>الكثافة</td><td>1.24 جم/سم³</td><td>1.28 جم/سم³</td></tr>
                <tr><td>الفوهة / السرير</td><td>190–230 / 35–45 درجة</td><td>230–260 / 65–75 درجة</td></tr>
              </tbody>
            </table>
          </div>
          <p>النتيجة هي المعتادة بين PLA وPETG: PLA أكثر صلابة وترابطًا بين الطبقات، أما PETG HS فيتحمل حرارة أعلى قبل أن يلين ويمتص الصدمات أفضل، فهو الخيار للقطع التي تسخن أو تتعرض للاستخدام القاسي.</p>

          <h2>حرارة السعودية</h2>
          <p>يبدأ PETG HS في اللين عند حوالي 62–70 درجة، مقابل 54–57 درجة تقريبًا لـ PLA. لذلك هو الخيار الأكثر أمانًا للقطع القريبة من النوافذ أو في المستودعات الحارة أو في الظل خارج المنزل، ولمشابك الكابلات والحوامل والخطافات. أما السيارة المتوقفة تحت شمس الصيف فأصعب: قد يصبح التابلوه أسخن من الاثنين، فأبعد القطع المطبوعة عن الشمس المباشرة على التابلوه، أو اختر تصميمًا أسمك بلون داكن وجرّبه أولًا.</p>

          <h2>التجفيف والتخزين</h2>
          <p>يمتص PETG الرطوبة من الهواء، وPETG الرطب يُخرج خيوطًا وفرقعة. توصي KINGROON بتجفيفه على <strong>65 درجة لمدة 8 ساعات</strong> في فرن بتيار هواء أو مجفف فيلامنت قبل الطباعة، وحفظه برطوبة أقل من 20% مع إحكام الإغلاق ومادة مجففة. لا تستخدم فرن المطبخ أو الميكروويف، فـ KINGROON تحذّر من أنهما قد يتلفان الفيلامنت. في جدة والدمام والخبر احفظ البكرات المفتوحة في صندوق محكم مع السيليكا جل. اقرأ <a href="/3d/ar/blog/3d-printing-filament-saudi-heat-humidity/">دليل الحرارة والرطوبة في السعودية</a> للمزيد.</p>

          <h2>الألوان والسعر</h2>
          <p>سعر KINGROON PETG HS في Black Arrow 3D هو <strong>65 ريالًا لبكرة 1 كجم</strong> شامل الضريبة، بألوان <strong>الفضي والبني والأخضر والبرتقالي والأصفر</strong>. البكرة من ABS بقطر 200 مم وعرض 67 مم. بسعر 65 ريالًا للكيلو تكون تكلفة الفيلامنت حوالي <strong>0.065 ريال للجرام</strong>، أي إن حامل جوال وزنه 50 جم يكلف حوالي 3.25 ريال من الفيلامنت. الكمية محدودة، وتعرض <a href="''' + HS_AR + '''">صفحة المنتج</a> الألوان المتوفرة.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>هل KINGROON PETG HS أسرع من PETG العادي؟</h3>
          <p>تقول KINGROON إن سرعة طباعته الافتراضية تصل إلى ضعف PETG العادي، بسرعة طباعة أقل من 300 مم/ث، مع تسريب وخيوط وتكتل أقل عند السرعة العالية.</p>
          <h3>ما درجة الحرارة المناسبة لطباعة KINGROON PETG HS؟</h3>
          <p>توصي KINGROON بحرارة فوهة 230–260 درجة وحرارة سرير 65–75 درجة، على لوح PEI أملس أو محبب مع الغراء، ومروحة تبريد بين 0 و60%.</p>
          <h3>هل PETG HS لامع؟</h3>
          <p>لا. سطح KINGROON PETG HS مطفي، وهذا يخفي أيضًا الخطوط اللامعة التي تظهر في PETG العادي عند تغيّر سرعة الطباعة.</p>
          <h3>هل PETG HS أفضل من PLA؟</h3>
          <p>في الحرارة والصدمات نعم: حسب بيانات KINGROON يلين عند حرارة أعلى ويمتص صدمات أكثر. أما PLA فأكثر صلابة وترابطًا بين الطبقات وأسهل في الطباعة، فيبقى الخيار الأفضل للديكور والهدايا وقطع العرض.</p>
          <h3>هل يعمل على طابعات بامبو لاب؟</h3>
          <p>نعم، هو فيلامنت قياسي بقطر 1.75 مم. ابدأ من ملف Generic PETG واضبط حرارة KINGROON. لا توجد عليه شريحة RFID، لذا اختر نوع الفيلامنت ولونه في برنامج التقطيع بنفسك.</p>
          <h3>كم سعر KINGROON PETG HS في السعودية؟</h3>
          <p>65 ريالًا لبكرة 1 كجم في Black Arrow 3D شامل الضريبة، مع التوصيل لجميع مناطق السعودية.</p>

          <div class="b3d-article__cta">
            <p>KINGROON PETG HS بسعر 65 ريالًا للكيلو، بألوان الفضي والبني والأخضر والبرتقالي والأصفر.</p>
            <a href="''' + HS_AR + '''" class="btn btn-primary">ألوان PETG HS</a>
          </div>

          <h2>مقالات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="''' + WHICH_POST_AR + '''">KINGROON PLA أم PETG أم PETG HS</a>
            <a href="/3d/ar/blog/kingroon-petg-basic-filament-guide/">دليل KINGROON PETG Basic</a>
            <a href="/3d/ar/blog/kingroon-pla-basic-filament-review/">مراجعة KINGROON PLA Basic</a>
            <a href="/3d/ar/blog/3d-print-stringing-fix/">حل مشكلة الخيوط</a>
            <a href="/3d/ar/shop/filament/">كل الفيلامنت</a>
          </div>
''',
        },
    },
    {
        'slug': 'kingroon-filament-pla-vs-petg-vs-petg-hs',
        'en': {
            'headline': 'KINGROON PLA vs PETG vs PETG HS: Which KINGROON Filament Should You Buy?',
            'title': 'KINGROON PLA vs PETG vs PETG HS Filament (KSA) | Black Arrow 3D',
            'desc': 'Which KINGROON filament to buy in Saudi Arabia: PLA Basic, PETG Basic or PETG HS. Official settings, heat resistance, finish, colours including the new arrivals, and price.',
            'meta_line': 'Filament guide &middot; ' + EN_DATE + ' &middot; 6 min read',
            'lead': 'KINGROON makes three everyday filaments we stock: PLA Basic, PETG Basic and the new PETG HS high-speed. All three are 1.75 mm, 1 kg and 65 SAR. Here is what separates them, which one suits which print, and the colours that just arrived.',
            'card': ('Filament guide', '6 min read', 'PLA Basic, PETG Basic or PETG HS? Settings, heat, finish, new colours and which to pick for each print.'),
            'body': '''
          <h2>Quick answer</h2>
          <ul>
            <li><strong><a href="''' + PLA + '''">PLA Basic</a></strong> for most prints: gifts, toys, figures, decor and prototypes. Easiest to print, stiffest, most colours.</li>
            <li><strong><a href="''' + PETG + '''">PETG Basic</a></strong> for parts that get warm, wet or knocked: clips, hooks, plant pots, covers. Glossy finish, lots of colours including transparent.</li>
            <li><strong><a href="''' + HS + '''">PETG HS</a></strong> for the same jobs as PETG, printed fast and with a matte finish. Best on high-speed printers.</li>
          </ul>
          <p>All three are <strong>65&nbsp;SAR per 1&nbsp;kg spool</strong> at Black Arrow 3D, VAT included.</p>

          <h2>The three side by side</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA Basic</th><th>PETG Basic</th><th>PETG HS</th></tr></thead>
              <tbody>
                <tr><td>Best for</td><td>Decor, gifts, prototypes</td><td>Functional, warm or wet parts</td><td>Functional parts, printed fast</td></tr>
                <tr><td>Finish</td><td>Smooth</td><td>Glossy</td><td>Matte</td></tr>
                <tr><td>Ease of printing</td><td>Easiest</td><td>Easy, can string</td><td>Easy, made for speed</td></tr>
                <tr><td>Nozzle temperature</td><td>190–230&nbsp;°C</td><td>See spool label</td><td>230–260&nbsp;°C</td></tr>
                <tr><td>Bed temperature</td><td>35–45&nbsp;°C</td><td>See spool label</td><td>65–75&nbsp;°C</td></tr>
                <tr><td>Print speed</td><td>under 300&nbsp;mm/s</td><td>slower than PLA</td><td>under 300&nbsp;mm/s</td></tr>
                <tr><td>Heat deflection (1.8&nbsp;MPa)</td><td>54&nbsp;°C</td><td>higher than PLA</td><td>62&nbsp;°C</td></tr>
                <tr><td>Drying</td><td>50&nbsp;°C, 8&nbsp;h</td><td>dry if it strings</td><td>65&nbsp;°C, 8&nbsp;h</td></tr>
                <tr><td>Price</td><td colspan="3">65&nbsp;SAR per 1&nbsp;kg</td></tr>
              </tbody>
            </table>
          </div>
          <p><small>PLA Basic and PETG HS figures are from KINGROON's Technical Data Sheets V1.0. KINGROON does not publish a data sheet for PETG Basic, so follow the range printed on its spool label.</small></p>

          <h2>Which one for which print</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Print</th><th>Pick</th><th>Why</th></tr></thead>
              <tbody>
                <tr><td>Keychains, figures, gifts</td><td>PLA Basic</td><td>Sharp detail, most colours</td></tr>
                <tr><td>Vases, lamps, decor</td><td>PLA Basic</td><td>Clean surface, easy to print</td></tr>
                <tr><td>Prototypes and test fits</td><td>PLA Basic</td><td>Stiff and quick</td></tr>
                <tr><td>Cable clips, hooks, brackets</td><td>PETG HS or PETG Basic</td><td>Bend before they snap</td></tr>
                <tr><td>Plant pots, bathroom or kitchen parts</td><td>PETG Basic or PETG HS</td><td>Handle water and warmth</td></tr>
                <tr><td>Functional parts on a fast printer</td><td>PETG HS</td><td>Made for high speed, matte walls</td></tr>
                <tr><td>Clear or see-through parts</td><td>PETG Basic</td><td>Comes in transparent colours</td></tr>
              </tbody>
            </table>
          </div>
          <p>Not sure between PLA and PETG in general? Read <a href="/3d/blog/pla-vs-petg-vs-abs-filament-guide/">PLA vs PETG vs ABS</a>.</p>

          <h2>New colours</h2>
          <p>Our latest KINGROON delivery added:</p>
          <ul>
            <li><strong>PLA Basic:</strong> Midnight Brown, Wood, Vibrant Orange and Retro Red, joining black, white, gray, silver, red, orange, yellow, green, blue, sky blue, purple, pink, brown, transparent, skin and gold.</li>
            <li><strong>PETG Basic:</strong> White and Black, joining a wide range that includes transparent and fluorescent colours.</li>
            <li><strong>PETG HS:</strong> Silver, Brown, Green, Orange and Yellow.</li>
          </ul>
          <p>Stock moves fast and some colours are single spools, so check each product page for what is in stock today.</p>

          <h2>Printing KINGROON on a Bambu Lab printer</h2>
          <p>KINGROON spools have no RFID tag, so the AMS will not set them up automatically. In Bambu Studio, pick the filament type and colour for the slot yourself: <em>Generic PLA</em> for PLA Basic and <em>Generic PETG</em> for both PETG types, then set KINGROON's temperatures. If you want the automatic RFID setup, see our guide to <a href="/3d/blog/bambu-lab-pla-basic-vs-pla-matte-filament/">Bambu Lab PLA Basic and PLA Matte</a>.</p>

          <h2>FAQ</h2>
          <h3>What is the difference between KINGROON PETG Basic and PETG HS?</h3>
          <p>PETG HS is KINGROON's high-speed PETG: KINGROON says it prints up to twice as fast as standard PETG by default, with less stringing, and it has a matte finish instead of PETG Basic's gloss.</p>
          <h3>Which KINGROON filament is best for beginners?</h3>
          <p>PLA Basic. It prints at lower temperatures, sticks easily on a 35–45&nbsp;°C bed and forgives most mistakes.</p>
          <h3>Which KINGROON filament handles Saudi heat best?</h3>
          <p>Either PETG. In KINGROON's data PETG HS deflects at 62&nbsp;°C against 54&nbsp;°C for PLA Basic. No common filament is safe on a dashboard in direct summer sun, though.</p>
          <h3>How much is KINGROON filament in Saudi Arabia?</h3>
          <p>PLA Basic, PETG Basic and PETG HS are all 65&nbsp;SAR per 1&nbsp;kg spool at Black Arrow 3D, VAT included, with delivery across Saudi Arabia.</p>

          <div class="b3d-article__cta">
            <p>KINGROON PLA Basic, PETG Basic and PETG HS, 65 SAR per kilo.</p>
            <a href="/3d/shop/filament/" class="btn btn-primary">Shop all filament</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="''' + HS_POST + '''">KINGROON PETG HS guide</a>
            <a href="/3d/blog/kingroon-pla-basic-filament-review/">KINGROON PLA Basic review</a>
            <a href="/3d/blog/kingroon-petg-basic-filament-guide/">KINGROON PETG Basic guide</a>
            <a href="/3d/blog/3d-printer-filament-price-saudi-arabia/">Filament prices in Saudi Arabia</a>
            <a href="/3d/blog/which-filament-for-which-print/">Which filament for which print</a>
          </div>
''',
        },
        'ar': {
            'headline': 'KINGROON PLA أم PETG أم PETG HS: أي فيلامنت من KINGROON تشتري؟',
            'title': 'فيلامنت KINGROON: PLA أم PETG أم PETG HS في السعودية | Black Arrow 3D',
            'desc': 'أي فيلامنت KINGROON تشتري في السعودية: PLA Basic أم PETG Basic أم PETG HS. الإعدادات الرسمية ومقاومة الحرارة والسطح والألوان ومنها الألوان الجديدة والسعر.',
            'meta_line': 'دليل الفيلامنت &middot; ' + AR_DATE + ' &middot; 6 دقائق قراءة',
            'lead': 'نوفّر ثلاثة أنواع يومية من فيلامنت KINGROON: ‏PLA Basic وPETG Basic والجديد PETG HS عالي السرعة. كلها بقطر 1.75 مم ووزن 1 كجم وسعر 65 ريالًا. إليك ما يفرق بينها وأيها يناسب كل طبعة والألوان التي وصلت حديثًا.',
            'card': ('دليل الفيلامنت', '6 دقائق قراءة', 'PLA Basic أم PETG Basic أم PETG HS؟ الإعدادات والحرارة والسطح والألوان الجديدة وأيها تختار لكل طبعة.'),
            'body': '''
          <h2>الإجابة المختصرة</h2>
          <ul>
            <li><strong><a href="''' + PLA_AR + '''">PLA Basic</a></strong> لمعظم الطبعات: الهدايا والألعاب والمجسمات والديكور والنماذج الأولية. الأسهل في الطباعة والأكثر صلابة والأكثر ألوانًا.</li>
            <li><strong><a href="''' + PETG_AR + '''">PETG Basic</a></strong> للقطع التي تسخن أو تتعرض للماء أو الصدمات: المشابك والخطافات وأحواض النباتات والأغطية. سطح لامع وألوان كثيرة منها الشفاف.</li>
            <li><strong><a href="''' + HS_AR + '''">PETG HS</a></strong> لنفس استخدامات PETG لكن بطباعة سريعة وسطح مطفي. الأفضل على الطابعات عالية السرعة.</li>
          </ul>
          <p>الأنواع الثلاثة بسعر <strong>65 ريالًا لبكرة 1 كجم</strong> في Black Arrow 3D شامل الضريبة.</p>

          <h2>مقارنة الأنواع الثلاثة</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>PLA Basic</th><th>PETG Basic</th><th>PETG HS</th></tr></thead>
              <tbody>
                <tr><td>الأفضل لـ</td><td>الديكور والهدايا والنماذج الأولية</td><td>القطع الوظيفية والمعرضة للحرارة أو الماء</td><td>القطع الوظيفية بطباعة سريعة</td></tr>
                <tr><td>السطح</td><td>ناعم</td><td>لامع</td><td>مطفي</td></tr>
                <tr><td>سهولة الطباعة</td><td>الأسهل</td><td>سهل، قد يُخرج خيوطًا</td><td>سهل، مصنوع للسرعة</td></tr>
                <tr><td>حرارة الفوهة</td><td>190–230 درجة</td><td>راجع ملصق البكرة</td><td>230–260 درجة</td></tr>
                <tr><td>حرارة السرير</td><td>35–45 درجة</td><td>راجع ملصق البكرة</td><td>65–75 درجة</td></tr>
                <tr><td>سرعة الطباعة</td><td>أقل من 300 مم/ث</td><td>أبطأ من PLA</td><td>أقل من 300 مم/ث</td></tr>
                <tr><td>الانحراف الحراري (1.8 ميجاباسكال)</td><td>54 درجة</td><td>أعلى من PLA</td><td>62 درجة</td></tr>
                <tr><td>التجفيف</td><td>50 درجة، 8 ساعات</td><td>جففه إذا ظهرت خيوط</td><td>65 درجة، 8 ساعات</td></tr>
                <tr><td>السعر</td><td colspan="3">65 ريالًا للكيلو</td></tr>
              </tbody>
            </table>
          </div>
          <p><small>أرقام PLA Basic وPETG HS من أوراق البيانات الفنية الرسمية لـ KINGROON (الإصدار 1.0). لا تنشر KINGROON ورقة بيانات لـ PETG Basic، فاتبع النطاق المطبوع على ملصق البكرة.</small></p>

          <h2>أي نوع لأي طبعة</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الطبعة</th><th>الاختيار</th><th>السبب</th></tr></thead>
              <tbody>
                <tr><td>الميداليات والمجسمات والهدايا</td><td>PLA Basic</td><td>تفاصيل دقيقة وألوان أكثر</td></tr>
                <tr><td>المزهريات والإضاءة والديكور</td><td>PLA Basic</td><td>سطح نظيف وطباعة سهلة</td></tr>
                <tr><td>النماذج الأولية واختبار المقاسات</td><td>PLA Basic</td><td>صلب وسريع</td></tr>
                <tr><td>مشابك الكابلات والخطافات والحوامل</td><td>PETG HS أو PETG Basic</td><td>تنثني قبل أن تنكسر</td></tr>
                <tr><td>أحواض النباتات وقطع الحمام والمطبخ</td><td>PETG Basic أو PETG HS</td><td>تتحمل الماء والحرارة</td></tr>
                <tr><td>قطع وظيفية على طابعة سريعة</td><td>PETG HS</td><td>مصنوع للسرعة العالية وجدرانه مطفية</td></tr>
                <tr><td>قطع شفافة</td><td>PETG Basic</td><td>متوفر بألوان شفافة</td></tr>
              </tbody>
            </table>
          </div>
          <p>محتار بين PLA وPETG عمومًا؟ اقرأ <a href="/3d/ar/blog/pla-vs-petg-vs-abs-filament-guide/">PLA أم PETG أم ABS</a>.</p>

          <h2>الألوان الجديدة</h2>
          <p>أضافت آخر شحنة من KINGROON:</p>
          <ul>
            <li><strong>PLA Basic:</strong> البني الداكن والخشبي والبرتقالي الزاهي والأحمر الريترو، إلى جانب الأسود والأبيض والرمادي والفضي والأحمر والبرتقالي والأصفر والأخضر والأزرق والسماوي والبنفسجي والوردي والنحاسي والشفاف والبيج والذهبي.</li>
            <li><strong>PETG Basic:</strong> الأبيض والأسود، إلى جانب تشكيلة واسعة منها الألوان الشفافة والفسفورية.</li>
            <li><strong>PETG HS:</strong> الفضي والبني والأخضر والبرتقالي والأصفر.</li>
          </ul>
          <p>المخزون يتحرك بسرعة وبعض الألوان بكرة واحدة فقط، فراجع صفحة كل منتج لمعرفة المتوفر اليوم.</p>

          <h2>طباعة KINGROON على طابعة بامبو لاب</h2>
          <p>بكرات KINGROON لا تحمل شريحة RFID، لذا لن يضبطها نظام AMS تلقائيًا. في Bambu Studio اختر نوع الفيلامنت ولونه للخانة بنفسك: <em>Generic PLA</em> لـ PLA Basic و<em>Generic PETG</em> لنوعي PETG، ثم اضبط حرارة KINGROON. وإذا أردت الضبط التلقائي عبر RFID فاقرأ دليلنا عن <a href="/3d/ar/blog/bambu-lab-pla-basic-vs-pla-matte-filament/">بامبو لاب PLA Basic وPLA Matte</a>.</p>

          <h2>الأسئلة الشائعة</h2>
          <h3>ما الفرق بين KINGROON PETG Basic وPETG HS؟</h3>
          <p>PETG HS هو PETG عالي السرعة من KINGROON: تقول KINGROON إن سرعة طباعته الافتراضية تصل إلى ضعف PETG العادي مع خيوط أقل، وسطحه مطفي بدلًا من لمعان PETG Basic.</p>
          <h3>أي فيلامنت KINGROON أفضل للمبتدئين؟</h3>
          <p>PLA Basic. يُطبع على حرارة أقل ويلتصق بسهولة على سرير بحرارة 35–45 درجة ويتسامح مع معظم الأخطاء.</p>
          <h3>أي فيلامنت KINGROON يتحمل حرارة السعودية أكثر؟</h3>
          <p>أي نوع من PETG. حسب بيانات KINGROON ينحرف PETG HS حراريًا عند 62 درجة مقابل 54 درجة لـ PLA Basic. لكن لا يوجد فيلامنت شائع آمن على تابلوه السيارة تحت شمس الصيف المباشرة.</p>
          <h3>كم سعر فيلامنت KINGROON في السعودية؟</h3>
          <p>‏PLA Basic وPETG Basic وPETG HS كلها بسعر 65 ريالًا لبكرة 1 كجم في Black Arrow 3D شامل الضريبة، مع التوصيل لجميع مناطق السعودية.</p>

          <div class="b3d-article__cta">
            <p>KINGROON PLA Basic وPETG Basic وPETG HS بسعر 65 ريالًا للكيلو.</p>
            <a href="/3d/ar/shop/filament/" class="btn btn-primary">تسوق كل الفيلامنت</a>
          </div>

          <h2>مقالات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="''' + HS_POST_AR + '''">دليل KINGROON PETG HS</a>
            <a href="/3d/ar/blog/kingroon-pla-basic-filament-review/">مراجعة KINGROON PLA Basic</a>
            <a href="/3d/ar/blog/kingroon-petg-basic-filament-guide/">دليل KINGROON PETG Basic</a>
            <a href="/3d/ar/blog/3d-printer-filament-price-saudi-arabia/">أسعار الفيلامنت في السعودية</a>
            <a href="/3d/ar/blog/which-filament-for-which-print/">أي فيلامنت لأي طبعة</a>
          </div>
''',
        },
    },
]
