"""November 2026 SEO refresh, batch 3: the Bambu Lab A1-family posts with the most Search Console impressions.

Moved here from older sources so they get live prices and a fresh dateModified:
- bambu-lab-a1-vs-a1-mini-vs-a2l   (EN was hand-written; AR came from generate_3d_blog_ar.POSTS)
- bambu-lab-a1-mini-combo-review   (hand-written EN + AR)
- bambu-lab-a1-mini-setup-guide    (was in build_3d_troubleshooting_guides.GUIDES)
'published' keeps each post's first publish date. Specs from 3d/assets/data/3d-products.json.
"""

POSTS = [
    # ------------------------------------------------------------------
    # 1. REFRESH: A1 vs A1 mini vs A2L
    # ------------------------------------------------------------------
    {
        'slug': 'bambu-lab-a1-vs-a1-mini-vs-a2l',
        'published': '2026-09-15',
        'en': {
            'headline': 'Bambu Lab A1 vs A1 mini vs A2L: Which One Should You Buy?',
            'title': 'Bambu Lab A1 vs A1 mini vs A2L: Differences &amp; Which to Buy',
            'desc': 'Bambu Lab A1 mini vs A1 vs A2L side by side: build size, footprint, bed temperature, AMS lite Combos and prices in SAR, so you buy the right Bambu Lab printer the first time.',
            'meta_line': 'Comparison &middot; Updated November 10, 2026 &middot; 7 min read',
            'lead': 'All three are open-frame Bambu Lab printers with the same easy app, automatic calibration and AMS lite for 4-color printing. The real decision is how big your prints are, how much desk space you have, and your budget.',
            'card': ('Comparison', '7 min read', 'A1 mini vs A1 vs A2L: build size, footprint, Combos and prices in SAR, and which Bambu Lab printer to buy.'),
            'body': '''
          <h2>Quick answer</h2>
          <ul>
            <li><b>A1 mini</b> if most of what you print fits in an 18&nbsp;cm cube, or desk space is tight. The <a href="/3d/product/bambu-lab-a1-mini/">A1 mini Combo</a> is <span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span>&nbsp;SAR.</li>
            <li><b>A2L</b> if you print helmets, cosplay parts, storage boxes or several items per plate. The <a href="/3d/product/bambu-lab-a2l/">A2L</a> is <span data-b3d-price="bambu-lab-a2l|Standalone (printer only)">3,350</span>&nbsp;SAR, or <span data-b3d-price="bambu-lab-a2l|Combo (printer + AMS lite)">4,300</span>&nbsp;SAR as a Combo.</li>
            <li><b>A1</b> sits in between at 256&nbsp;mm per side. Check its stock line below: when it is out of stock, the A2L is the next size up.</li>
          </ul>

          <h2>Side by side</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>A1 mini</th><th>A1</th><th>A2L</th></tr></thead>
              <tbody>
                <tr><td>Build volume</td><td>180 x 180 x 180 mm</td><td>256 x 256 x 256 mm</td><td>330 x 320 x 325 mm (~34.3 L)</td></tr>
                <tr><td>Printer size</td><td>347 x 315 x 365 mm</td><td>465 x 410 x 430 mm</td><td>544 x 529 x 505 mm</td></tr>
                <tr><td>Weight</td><td>5.5 kg</td><td>8.3 kg</td><td>12.8 kg</td></tr>
                <tr><td>Max speed / acceleration</td><td>500 mm/s / 10,000 mm/s&sup2;</td><td>500 mm/s / 10,000 mm/s&sup2;</td><td>500 mm/s / 10,000 mm/s&sup2;</td></tr>
                <tr><td>Hot end / bed</td><td>300 &deg;C / 80 &deg;C</td><td>300 &deg;C / 100 &deg;C</td><td>300 &deg;C / 80 &deg;C</td></tr>
                <tr><td>Multi-color</td><td>AMS lite, 4 colors (Combo)</td><td>AMS lite, 4 colors (Combo)</td><td>AMS lite, 4 colors (Combo)</td></tr>
                <tr><td>Printer only (SAR)</td><td><span data-b3d-price="bambu-lab-a1-mini|Standalone (printer only)">1,799</span><br><small><span data-b3d-stock="bambu-lab-a1-mini|Standalone (printer only)">Out of stock</span></small></td><td><span data-b3d-price="bambu-lab-a1|Standalone (printer only)">2,700</span><br><small><span data-b3d-stock="bambu-lab-a1|Standalone (printer only)">Out of stock</span></small></td><td><span data-b3d-price="bambu-lab-a2l|Standalone (printer only)">3,350</span><br><small><span data-b3d-stock="bambu-lab-a2l|Standalone (printer only)">In stock</span></small></td></tr>
                <tr><td>Combo with AMS lite (SAR)</td><td><span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span><br><small><span data-b3d-stock="bambu-lab-a1-mini|Combo (printer + AMS lite)">In stock</span></small></td><td><span data-b3d-price="bambu-lab-a1|Combo (printer + AMS Lite)">3,449</span><br><small><span data-b3d-stock="bambu-lab-a1|Combo (printer + AMS Lite)">Out of stock</span></small></td><td><span data-b3d-price="bambu-lab-a2l|Combo (printer + AMS lite)">4,300</span><br><small><span data-b3d-stock="bambu-lab-a2l|Combo (printer + AMS lite)">In stock</span></small></td></tr>
              </tbody>
            </table>
          </div>
          <p>Prices include 15% VAT. Regular delivery is free on every order that includes a 3D printer, and every printer has a 1-year warranty from Black Arrow 3D.</p>

          <h2>What all three have in common</h2>
          <ul>
            <li>Fully automatic calibration: bed leveling, vibration compensation and flow calibration, so there is nothing to tune by hand.</li>
            <li>An all-metal hot end up to 300&nbsp;&deg;C, with quick-swap nozzles from 0.2 to 0.8&nbsp;mm.</li>
            <li>The same software: Bambu Studio on a computer and the Bambu Handy app, with free models on MakerWorld.</li>
            <li>An open frame. They are made for PLA, PETG and TPU. For ABS or ASA choose an enclosed printer such as the <a href="/3d/product/bambu-lab-p1s/">P1S</a> or the <a href="/3d/product/elegoo-centauri-carbon-2/">Elegoo Centauri Carbon 2</a>.</li>
          </ul>

          <h2>Bambu Lab A1 mini: smallest footprint, lowest price</h2>
          <p>The <a href="/3d/product/bambu-lab-a1-mini/">A1 mini</a> fits on a normal desk and covers most first projects: keychains, phone stands, figurines, organisers and gifts. Its 180&nbsp;mm limit is the trade-off: helmets, large vases and long parts need splitting into pieces. Read our <a href="/3d/blog/bambu-lab-a1-mini-combo-review/">A1 mini Combo review</a>.</p>

          <h2>Bambu Lab A1: the middle size</h2>
          <p>The <a href="/3d/product/bambu-lab-a1/">A1</a> gives you a 256&nbsp;mm cube, the same build size as the enclosed P1S and P2S, with a 100&nbsp;&deg;C bed. It is the balanced choice for household parts and medium cosplay props when it is in stock.</p>

          <h2>Bambu Lab A2L: for genuinely large prints</h2>
          <p>The <a href="/3d/product/bambu-lab-a2l/">A2L</a> prints up to 330 x 320 x 325&nbsp;mm, about twice the volume of the A1, with a built-in filament cutter. It suits full helmets, large storage boxes and batch production. It needs a sturdy table about 55&nbsp;cm square. See our <a href="/3d/blog/bambu-lab-a2l-combo-guide-saudi/">A2L Combo guide</a>.</p>

          <h2>Printer only or Combo?</h2>
          <p>The Combo adds the <b>AMS lite</b>, which holds 4 spools and switches between them during a print. Choose it if you want multi-color gifts, signs or figurines. If you only ever print one color at a time, the printer alone is enough, and you can still change filament by hand. Learn more in <a href="/3d/blog/multi-color-3d-printing-explained/">multi-color 3D printing explained</a>.</p>

          <h2>FAQ</h2>
          <h3>What is the difference between the A1 and A1 mini?</h3>
          <p>Size. The A1 prints up to 256&nbsp;mm per side and the A1 mini up to 180&nbsp;mm. The A1 also has a hotter bed (100&nbsp;&deg;C vs 80&nbsp;&deg;C). Speed, software and the AMS lite are the same.</p>
          <h3>Is the A2L bigger than the A1?</h3>
          <p>Yes. The A2L prints up to 330 x 320 x 325&nbsp;mm, against 256 x 256 x 256&nbsp;mm on the A1.</p>
          <h3>Which Bambu Lab printer is best for beginners?</h3>
          <p>The A1 mini Combo, for most people. See <a href="/3d/blog/best-3d-printer-for-beginners-saudi-arabia/">the best 3D printer for beginners</a>.</p>
          <h3>Can these printers print ABS?</h3>
          <p>They are open-frame printers, so ABS and ASA are not recommended. Use an enclosed printer for those materials.</p>

          <div class="b3d-article__cta">
            <p>Compare all three with live specs</p>
            <a href="/3d/compare/" class="btn btn-primary">Open compare tool</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/product/bambu-lab-a1-mini/">Bambu Lab A1 mini</a>
            <a href="/3d/product/bambu-lab-a1/">Bambu Lab A1</a>
            <a href="/3d/product/bambu-lab-a2l/">Bambu Lab A2L</a>
          </div>
''',
        },
        'ar': {
            'headline': 'بامبو لاب A1 مقابل A1 ميني مقابل A2L: أيهما تشتري؟',
            'title': 'بامبو لاب A1 أو A1 ميني أو A2L: ما الفرق وأيها تشتري؟',
            'desc': 'مقارنة بامبو لاب A1 ميني وA1 وA2L جنبًا إلى جنب: حجم الطباعة ومقاس الطابعة وحرارة السرير وباقات AMS lite والأسعار بالريال، لتختار الطابعة الصحيحة من أول مرة.',
            'meta_line': 'مقارنة &middot; تحديث 10 نوفمبر 2026 &middot; 7 دقائق قراءة',
            'lead': 'الطابعات الثلاث مفتوحة من بامبو لاب، بنفس التطبيق السهل والمعايرة التلقائية ووحدة AMS lite للطباعة بأربعة ألوان. القرار الحقيقي هو حجم مطبوعاتك، ومساحة مكتبك، وميزانيتك.',
            'card': ('مقارنة', '7 دقائق قراءة', 'A1 ميني مقابل A1 مقابل A2L: حجم الطباعة والمقاس والباقات والأسعار بالريال، وأي طابعة بامبو لاب تشتري.'),
            'body': '''
          <h2>الإجابة السريعة</h2>
          <ul>
            <li><b>A1 ميني</b> إذا كانت معظم مطبوعاتك ضمن مكعب 18 سم أو كانت مساحة مكتبك محدودة. سعر <a href="/3d/ar/product/bambu-lab-a1-mini/">A1 ميني كومبو</a> هو <span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span> ريال.</li>
            <li><b>A2L</b> إذا كنت تطبع خوذات أو قطع كوسبلاي أو صناديق تخزين أو عدة قطع في لوح واحد. سعر <a href="/3d/ar/product/bambu-lab-a2l/">A2L</a> هو <span data-b3d-price="bambu-lab-a2l|Standalone (printer only)">3,350</span> ريال، أو <span data-b3d-price="bambu-lab-a2l|Combo (printer + AMS lite)">4,300</span> ريال كباقة كومبو.</li>
            <li><b>A1</b> في المنتصف بحجم 256 ملم لكل جهة. راجع سطر التوفر أدناه: عندما تكون غير متوفرة، فإن A2L هي الحجم التالي.</li>
          </ul>

          <h2>مقارنة جنبًا إلى جنب</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>A1 ميني</th><th>A1</th><th>A2L</th></tr></thead>
              <tbody>
                <tr><td>حجم الطباعة</td><td>180×180×180 ملم</td><td>256×256×256 ملم</td><td>330×320×325 ملم (~34.3 لتر)</td></tr>
                <tr><td>مقاس الطابعة</td><td>347×315×365 ملم</td><td>465×410×430 ملم</td><td>544×529×505 ملم</td></tr>
                <tr><td>الوزن</td><td>5.5 كجم</td><td>8.3 كجم</td><td>12.8 كجم</td></tr>
                <tr><td>السرعة / التسارع</td><td>500 ملم/ث / 10,000 ملم/ث²</td><td>500 ملم/ث / 10,000 ملم/ث²</td><td>500 ملم/ث / 10,000 ملم/ث²</td></tr>
                <tr><td>رأس الطباعة / السرير</td><td>300 °م / 80 °م</td><td>300 °م / 100 °م</td><td>300 °م / 80 °م</td></tr>
                <tr><td>الألوان المتعددة</td><td>AMS lite، 4 ألوان (كومبو)</td><td>AMS lite، 4 ألوان (كومبو)</td><td>AMS lite، 4 ألوان (كومبو)</td></tr>
                <tr><td>الطابعة فقط (ريال)</td><td><span data-b3d-price="bambu-lab-a1-mini|Standalone (printer only)">1,799</span><br><small><span data-b3d-stock="bambu-lab-a1-mini|Standalone (printer only)">غير متوفر</span></small></td><td><span data-b3d-price="bambu-lab-a1|Standalone (printer only)">2,700</span><br><small><span data-b3d-stock="bambu-lab-a1|Standalone (printer only)">غير متوفر</span></small></td><td><span data-b3d-price="bambu-lab-a2l|Standalone (printer only)">3,350</span><br><small><span data-b3d-stock="bambu-lab-a2l|Standalone (printer only)">متوفر</span></small></td></tr>
                <tr><td>كومبو مع AMS lite (ريال)</td><td><span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span><br><small><span data-b3d-stock="bambu-lab-a1-mini|Combo (printer + AMS lite)">متوفر</span></small></td><td><span data-b3d-price="bambu-lab-a1|Combo (printer + AMS Lite)">3,449</span><br><small><span data-b3d-stock="bambu-lab-a1|Combo (printer + AMS Lite)">غير متوفر</span></small></td><td><span data-b3d-price="bambu-lab-a2l|Combo (printer + AMS lite)">4,300</span><br><small><span data-b3d-stock="bambu-lab-a2l|Combo (printer + AMS lite)">متوفر</span></small></td></tr>
              </tbody>
            </table>
          </div>
          <p>الأسعار شاملة ضريبة القيمة المضافة 15%. التوصيل العادي مجاني لكل طلب يتضمن طابعة ثلاثية الأبعاد، ولكل طابعة ضمان لمدة سنة من بلاك آرو 3D.</p>

          <h2>ما تشترك فيه الثلاث</h2>
          <ul>
            <li>معايرة تلقائية بالكامل: تسوية السرير وتعويض الاهتزاز ومعايرة التدفق، فلا شيء تضبطه يدويًا.</li>
            <li>هوت إند معدني بالكامل حتى 300 °م، مع فوهات سريعة التبديل من 0.2 إلى 0.8 ملم.</li>
            <li>البرامج نفسها: Bambu Studio على الكمبيوتر وتطبيق Bambu Handy، مع مجسمات مجانية على MakerWorld.</li>
            <li>هيكل مفتوح، فهي مصممة لـ PLA وPETG وTPU. أما ABS وASA فاختر لهما طابعة مغلقة مثل <a href="/3d/ar/product/bambu-lab-p1s/">P1S</a> أو <a href="/3d/ar/product/elegoo-centauri-carbon-2/">Elegoo Centauri Carbon 2</a>.</li>
          </ul>

          <h2>بامبو لاب A1 ميني: أصغر مساحة وأقل سعر</h2>
          <p>‏<a href="/3d/ar/product/bambu-lab-a1-mini/">A1 ميني</a> تتسع على مكتب عادي وتغطي معظم المشاريع الأولى: ميداليات المفاتيح وحوامل الجوال والمجسمات والمنظمات والهدايا. حدها 180 ملم هو المقابل، فالخوذات والمزهريات الكبيرة والقطع الطويلة تحتاج إلى تقسيم. اقرأ <a href="/3d/ar/blog/bambu-lab-a1-mini-combo-review/">مراجعة A1 ميني كومبو</a>.</p>

          <h2>بامبو لاب A1: الحجم المتوسط</h2>
          <p>‏<a href="/3d/ar/product/bambu-lab-a1/">A1</a> تمنحك مكعب 256 ملم، وهو حجم الطباعة نفسه في الطابعتين المغلقتين P1S وP2S، مع سرير حتى 100 °م. هي الخيار المتوازن للقطع المنزلية وإكسسوارات الكوسبلاي المتوسطة عندما تكون متوفرة.</p>

          <h2>بامبو لاب A2L: للمطبوعات الكبيرة فعلًا</h2>
          <p>‏<a href="/3d/ar/product/bambu-lab-a2l/">A2L</a> تطبع حتى 330×320×325 ملم، أي نحو ضعف حجم A1، مع قاطع خيط مدمج. تناسب الخوذات الكاملة وصناديق التخزين الكبيرة والإنتاج بالدفعات، وتحتاج إلى طاولة متينة بمساحة 55 سم تقريبًا لكل جهة. راجع <a href="/3d/ar/blog/bambu-lab-a2l-combo-guide-saudi/">دليل A2L كومبو</a>.</p>

          <h2>الطابعة فقط أم الكومبو؟</h2>
          <p>تضيف باقة الكومبو وحدة <b>AMS lite</b> التي تحمل 4 بكرات وتبدّل بينها أثناء الطباعة. اخترها إذا أردت هدايا أو لوحات أو مجسمات متعددة الألوان. أما إذا كنت تطبع بلون واحد دائمًا فالطابعة وحدها تكفي، ويمكنك تغيير الخيط يدويًا. اعرف المزيد في <a href="/3d/ar/blog/multi-color-3d-printing-explained/">شرح الطباعة متعددة الألوان</a>.</p>

          <h2>أسئلة شائعة</h2>
          <h3>ما الفرق بين A1 وA1 ميني؟</h3>
          <p>الحجم. تطبع A1 حتى 256 ملم لكل جهة، وA1 ميني حتى 180 ملم. كما أن سرير A1 أسخن (100 °م مقابل 80 °م). أما السرعة والبرامج ووحدة AMS lite فهي نفسها.</p>
          <h3>هل A2L أكبر من A1؟</h3>
          <p>نعم. تطبع A2L حتى 330×320×325 ملم، مقابل 256×256×256 ملم في A1.</p>
          <h3>أي طابعة بامبو لاب أفضل للمبتدئين؟</h3>
          <p>‏A1 ميني كومبو لمعظم الناس. راجع <a href="/3d/ar/blog/best-3d-printer-for-beginners-saudi-arabia/">أفضل طابعة ثلاثية الأبعاد للمبتدئين</a>.</p>
          <h3>هل تطبع هذه الطابعات ABS؟</h3>
          <p>هي طابعات مفتوحة، لذا لا يُنصح بـ ABS وASA عليها. استخدم طابعة مغلقة لهذه الخامات.</p>

          <div class="b3d-article__cta">
            <p>قارن الثلاث بمواصفات مباشرة</p>
            <a href="/3d/compare/" class="btn btn-primary">افتح أداة المقارنة</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/bambu-lab-a1-mini/">بامبو لاب A1 ميني</a>
            <a href="/3d/ar/product/bambu-lab-a1/">بامبو لاب A1</a>
            <a href="/3d/ar/product/bambu-lab-a2l/">بامبو لاب A2L</a>
          </div>
''',
        },
    },

    # ------------------------------------------------------------------
    # 2. REFRESH: A1 mini Combo review
    # ------------------------------------------------------------------
    {
        'slug': 'bambu-lab-a1-mini-combo-review',
        'published': '2026-10-11',
        'en': {
            'headline': 'Bambu Lab A1 mini Combo Review: Price &amp; Specs in Saudi Arabia',
            'title': 'Bambu Lab A1 mini Combo Review &amp; Price in Saudi Arabia',
            'desc': 'Bambu Lab A1 mini Combo review for Saudi buyers: price in SAR, what is in the box, AMS lite 4-color printing, full specs, limits, and how it compares with the SparkX i7, A2L and Snapmaker U1.',
            'meta_line': 'Review &middot; Updated November 10, 2026 &middot; 8 min read',
            'lead': 'The A1 mini Combo pairs Bambu Lab&#39;s compact, self-calibrating printer with the AMS lite, so it prints in up to 4 colors from day one. Here is what you get in Saudi Arabia, what it does well, where it falls short, and what to compare it with.',
            'card': ('Review', '8 min read', 'Bambu Lab A1 mini Combo in Saudi Arabia: price, what is in the box, AMS lite, specs, limits and alternatives.'),
            'body': '''
          <h2>Quick answer</h2>
          <p>The <a href="/3d/product/bambu-lab-a1-mini/">Bambu Lab A1 mini Combo</a> is our top pick for a first 3D printer. At <span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span>&nbsp;SAR you get a printer that calibrates itself, prints PLA, PETG and TPU reliably, and switches between 4 spools for multi-color prints. Its limits are the 180&nbsp;mm build size and the open frame, which rules out ABS and ASA.</p>

          <h2>Price in Saudi Arabia</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Option</th><th>Price (SAR)</th><th>Stock</th></tr></thead>
              <tbody>
                <tr><td>A1 mini Combo (printer + AMS lite)</td><td><span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span></td><td><span data-b3d-stock="bambu-lab-a1-mini|Combo (printer + AMS lite)">In stock</span></td></tr>
                <tr><td>A1 mini (printer only)</td><td><span data-b3d-price="bambu-lab-a1-mini|Standalone (printer only)">1,799</span></td><td><span data-b3d-stock="bambu-lab-a1-mini|Standalone (printer only)">Out of stock</span></td></tr>
              </tbody>
            </table>
          </div>
          <p>Prices include 15% VAT, with free regular delivery across Saudi Arabia and a 1-year warranty from Black Arrow 3D.</p>

          <h2>What is in the box</h2>
          <ul>
            <li>Bambu Lab A1 mini printer, build plate, spool holder and purge wiper</li>
            <li>Stainless steel nozzle, PTFE tube and an accessory box</li>
            <li>Bambu filament samples (20&nbsp;g, random color)</li>
            <li><b>Combo adds:</b> the AMS lite body and stand, 4 rotary spool holders and 3 PTFE tubes</li>
          </ul>
          <p>Filament is not included beyond the samples. Plan for at least 2 or 3 spools: see our <a href="/3d/shop/filament/">filament range</a> and <a href="/3d/blog/best-filament-for-bambu-lab-a1-ams-lite/">the best filament for the A1 and AMS lite</a>.</p>

          <h2>Specifications</h2>
          <div class="b3d-table-wrap">
            <table>
              <tbody>
                <tr><td>Build volume</td><td>180 x 180 x 180 mm</td></tr>
                <tr><td>Max speed / acceleration</td><td>500 mm/s / 10,000 mm/s&sup2;</td></tr>
                <tr><td>Hot end / bed</td><td>All-metal, up to 300 &deg;C / up to 80 &deg;C</td></tr>
                <tr><td>Nozzle</td><td>Stainless steel 0.4 mm (0.2 / 0.6 / 0.8 mm optional)</td></tr>
                <tr><td>Chassis</td><td>Steel and extruded aluminum</td></tr>
                <tr><td>Materials</td><td>PLA, PETG, TPU, PVA</td></tr>
                <tr><td>Multi-color (Combo)</td><td>AMS lite, 4 spools</td></tr>
                <tr><td>Screen / connectivity</td><td>2.4-inch touchscreen / Wi-Fi, microSD</td></tr>
                <tr><td>Size / weight</td><td>347 x 315 x 365 mm / 5.5 kg</td></tr>
                <tr><td>Power</td><td>100-240 V, 150 W max</td></tr>
              </tbody>
            </table>
          </div>

          <h2>What it does well</h2>
          <ul>
            <li><b>No manual tuning.</b> It levels the bed, compensates for vibration and calibrates flow on its own, which removes the main cause of failed first prints.</li>
            <li><b>Multi-color from day one.</b> The AMS lite switches between 4 spools automatically, so 2- to 4-color keychains, name plates and figurines need no extra work.</li>
            <li><b>Easy software.</b> Pick a model on MakerWorld in the Bambu Handy app and print it from your phone, or slice your own in Bambu Studio.</li>
            <li><b>Small and light.</b> At 5.5&nbsp;kg it fits on a desk or a shelf, and it is quiet enough for a home office.</li>
            <li><b>Reliability features</b>: filament run-out sensor, tangle detection and power-loss recovery.</li>
          </ul>

          <h2>Limits to know</h2>
          <ul>
            <li><b>180&nbsp;mm per side.</b> Big parts need splitting. If that is most of your printing, look at the <a href="/3d/product/bambu-lab-a2l/">A2L</a>.</li>
            <li><b>Open frame, 80&nbsp;&deg;C bed.</b> Not for ABS or ASA. Choose an enclosed printer for car parts that sit in the sun.</li>
            <li><b>Color changes create purge waste.</b> Every switch purges a little filament, so very color-heavy prints use more material and take longer.</li>
            <li><b>The AMS lite is open.</b> Spools sit in the room air, so in humid cities such as Jeddah, Dammam and Khobar store spools sealed when you are not printing.</li>
          </ul>

          <h2>How it compares</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>A1 mini Combo</th><th>SparkX i7 Combo</th><th>A2L Combo</th></tr></thead>
              <tbody>
                <tr><td>Price (SAR)</td><td><span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span></td><td><span data-b3d-price="creality-sparkx-i7|SparkX i7 Combo">2,650</span></td><td><span data-b3d-price="bambu-lab-a2l|Combo (printer + AMS lite)">4,300</span></td></tr>
                <tr><td>Build volume</td><td>180 x 180 x 180 mm</td><td>260 x 260 x 255 mm</td><td>330 x 320 x 325 mm</td></tr>
                <tr><td>Multi-color</td><td>AMS lite, 4</td><td>CFS Lite, 4</td><td>AMS lite, 4</td></tr>
                <tr><td>Weight</td><td>5.5 kg</td><td>9.12 kg</td><td>12.8 kg</td></tr>
              </tbody>
            </table>
          </div>
          <ul>
            <li><b><a href="/3d/blog/creality-sparkx-i7-review-saudi-arabia/">Creality SparkX i7</a></b>: a bigger plate for similar money, with less mature software. Sold on pre-order.</li>
            <li><b><a href="/3d/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/">Bambu Lab A2L</a></b>: the same Bambu Lab experience with almost twice the size per side, for more money and more desk space.</li>
            <li><b><a href="/3d/product/snapmaker-u1/">Snapmaker U1</a></b> (<span data-b3d-price="snapmaker-u1">5,699</span>&nbsp;SAR): 4 separate toolheads instead of one, so far less purge waste on color-heavy work. Worth it if you print in many colors every day. See <a href="/3d/blog/multi-color-3d-printing-explained/">AMS vs CANVAS vs SnapSwap</a>.</li>
          </ul>

          <h2>Verdict</h2>
          <p>If you want your first prints to work, and to print in color without learning to tune a printer, the A1 mini Combo is the safest buy in Saudi Arabia today. Get the A2L if you know you will print large, and an enclosed printer if you need ABS or ASA. Once it arrives, follow our <a href="/3d/blog/bambu-lab-a1-mini-setup-guide/">7-step setup guide</a>.</p>

          <h2>FAQ</h2>
          <h3>How much is the Bambu Lab A1 mini Combo in Saudi Arabia?</h3>
          <p>At Black Arrow 3D it is <span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span>&nbsp;SAR including VAT, with free delivery.</p>
          <h3>What does the AMS lite do?</h3>
          <p>It holds 4 spools and feeds them into the printer automatically, so one print can use up to 4 colors or materials.</p>
          <h3>Is the A1 mini good for beginners?</h3>
          <p>Yes. It calibrates itself and prints from the phone app, which makes it one of the easiest printers to start with.</p>
          <h3>Can the A1 mini print PETG and TPU?</h3>
          <p>Yes. It prints PLA, PETG, TPU and PVA. ABS and ASA are not recommended because it is an open-frame printer.</p>

          <div class="b3d-article__cta">
            <p>Order the A1 mini Combo</p>
            <a href="/3d/product/bambu-lab-a1-mini/" class="btn btn-primary">See price &amp; stock</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/product/bambu-lab-a1-mini/">Bambu Lab A1 mini Combo</a>
            <a href="/3d/blog/bambu-lab-a1-mini-setup-guide/">A1 mini setup guide</a>
            <a href="/3d/blog/best-3d-printer-for-beginners-saudi-arabia/">Best 3D printer for beginners</a>
          </div>
''',
        },
        'ar': {
            'headline': 'مراجعة Bambu Lab A1 mini Combo: السعر والمواصفات في السعودية',
            'title': 'مراجعة Bambu Lab A1 Mini Combo وسعرها بالسعودية | Black Arrow 3D',
            'desc': 'مراجعة Bambu Lab A1 mini Combo للمشترين في السعودية: السعر بالريال، ومحتويات الصندوق، والطباعة بأربعة ألوان مع AMS lite، والمواصفات، والحدود، ومقارنتها مع SparkX i7 وA2L وSnapmaker U1.',
            'meta_line': 'مراجعة &middot; تحديث 10 نوفمبر 2026 &middot; 8 دقائق قراءة',
            'lead': 'تجمع A1 mini Combo طابعة بامبو لاب الصغيرة ذاتية المعايرة مع وحدة AMS lite، فتطبع بحتى 4 ألوان من اليوم الأول. إليك ما تحصل عليه في السعودية، وما تجيده، وأين تقصر، وما تقارنها به.',
            'card': ('مراجعة', '8 دقائق قراءة', 'Bambu Lab A1 mini Combo في السعودية: السعر ومحتويات الصندوق وAMS lite والمواصفات والحدود والبدائل.'),
            'body': '''
          <h2>الإجابة السريعة</h2>
          <p>‏<a href="/3d/ar/product/bambu-lab-a1-mini/">Bambu Lab A1 mini Combo</a> هي اختيارنا الأول كأول طابعة ثلاثية الأبعاد. بسعر <span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span> ريال تحصل على طابعة تعاير نفسها، وتطبع PLA وPETG وTPU بثبات، وتبدّل بين 4 بكرات للطباعة متعددة الألوان. حدودها هي حجم الطباعة 180 ملم والهيكل المفتوح الذي لا يناسب ABS وASA.</p>

          <h2>السعر في السعودية</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>الخيار</th><th>السعر (ريال)</th><th>التوفر</th></tr></thead>
              <tbody>
                <tr><td>A1 mini كومبو (الطابعة + AMS lite)</td><td><span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span></td><td><span data-b3d-stock="bambu-lab-a1-mini|Combo (printer + AMS lite)">متوفر</span></td></tr>
                <tr><td>A1 mini (الطابعة فقط)</td><td><span data-b3d-price="bambu-lab-a1-mini|Standalone (printer only)">1,799</span></td><td><span data-b3d-stock="bambu-lab-a1-mini|Standalone (printer only)">غير متوفر</span></td></tr>
              </tbody>
            </table>
          </div>
          <p>الأسعار شاملة ضريبة القيمة المضافة 15%، مع توصيل عادي مجاني لجميع مناطق المملكة وضمان لمدة سنة من بلاك آرو 3D.</p>

          <h2>محتويات الصندوق</h2>
          <ul>
            <li>طابعة بامبو لاب A1 mini، ولوح الطباعة، وحامل البكرة، وماسحة التنظيف</li>
            <li>فوهة من الفولاذ المقاوم للصدأ، وأنبوب PTFE، وعلبة ملحقات</li>
            <li>عينات خيوط من بامبو (20 جم، لون عشوائي)</li>
            <li><b>يضيف الكومبو:</b> جسم وحدة AMS lite وحاملها، و4 حوامل بكرات دوّارة، و3 أنابيب PTFE</li>
          </ul>
          <p>لا تأتي خيوط غير العينات، فاحسب بكرتين أو ثلاثًا على الأقل: راجع <a href="/3d/ar/shop/filament/">تشكيلة الخيوط</a> و<a href="/3d/ar/blog/best-filament-for-bambu-lab-a1-ams-lite/">أفضل خيوط لـ A1 وAMS lite</a>.</p>

          <h2>المواصفات</h2>
          <div class="b3d-table-wrap">
            <table>
              <tbody>
                <tr><td>حجم الطباعة</td><td>180×180×180 ملم</td></tr>
                <tr><td>السرعة / التسارع</td><td>500 ملم/ث / 10,000 ملم/ث²</td></tr>
                <tr><td>رأس الطباعة / السرير</td><td>معدني بالكامل حتى 300 °م / حتى 80 °م</td></tr>
                <tr><td>الفوهة</td><td>فولاذ مقاوم للصدأ 0.4 ملم (0.2 / 0.6 / 0.8 ملم اختياري)</td></tr>
                <tr><td>الهيكل</td><td>فولاذ وألومنيوم مبثوق</td></tr>
                <tr><td>الخامات</td><td>PLA وPETG وTPU وPVA</td></tr>
                <tr><td>الألوان المتعددة (كومبو)</td><td>AMS lite، 4 بكرات</td></tr>
                <tr><td>الشاشة / الاتصال</td><td>شاشة لمس 2.4 بوصة / Wi-Fi وبطاقة microSD</td></tr>
                <tr><td>المقاس / الوزن</td><td>347×315×365 ملم / 5.5 كجم</td></tr>
                <tr><td>الطاقة</td><td>100-240 فولت، 150 واط كحد أقصى</td></tr>
              </tbody>
            </table>
          </div>

          <h2>ما تجيده</h2>
          <ul>
            <li><b>لا ضبط يدوي.</b> تسوّي السرير وتعوّض الاهتزاز وتعاير التدفق بنفسها، وهذا يزيل السبب الأول لفشل الطباعات الأولى.</li>
            <li><b>ألوان متعددة من اليوم الأول.</b> تبدّل AMS lite بين 4 بكرات تلقائيًا، فميداليات المفاتيح ولوحات الأسماء والمجسمات بلونين إلى أربعة لا تحتاج جهدًا إضافيًا.</li>
            <li><b>برامج سهلة.</b> اختر مجسمًا من MakerWorld في تطبيق Bambu Handy واطبعه من جوالك، أو جهّز مجسماتك في Bambu Studio.</li>
            <li><b>صغيرة وخفيفة.</b> بوزن 5.5 كجم تتسع على مكتب أو رف، وهادئة بما يكفي لمكتب منزلي.</li>
            <li><b>ميزات موثوقية</b>: حساس انتهاء الخيط، وكشف تشابك الخيط، واستئناف الطباعة بعد انقطاع الكهرباء.</li>
          </ul>

          <h2>حدود يجب معرفتها</h2>
          <ul>
            <li><b>180 ملم لكل جهة.</b> القطع الكبيرة تحتاج إلى تقسيم. إذا كانت هذه معظم طباعتك فانظر إلى <a href="/3d/ar/product/bambu-lab-a2l/">A2L</a>.</li>
            <li><b>هيكل مفتوح وسرير 80 °م.</b> لا تناسب ABS أو ASA. اختر طابعة مغلقة لقطع السيارات التي تتعرض للشمس.</li>
            <li><b>تغيير الألوان يُنتج هدرًا.</b> كل تبديل يُخرج قليلًا من الخيط، فالمطبوعات كثيرة الألوان تستهلك خامة أكثر ووقتًا أطول.</li>
            <li><b>وحدة AMS lite مكشوفة.</b> تبقى البكرات في هواء الغرفة، لذا في المدن الرطبة مثل جدة والدمام والخبر احفظ البكرات في أكياس محكمة عندما لا تطبع.</li>
          </ul>

          <h2>المقارنة</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th></th><th>A1 mini كومبو</th><th>SparkX i7 كومبو</th><th>A2L كومبو</th></tr></thead>
              <tbody>
                <tr><td>السعر (ريال)</td><td><span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span></td><td><span data-b3d-price="creality-sparkx-i7|SparkX i7 Combo">2,650</span></td><td><span data-b3d-price="bambu-lab-a2l|Combo (printer + AMS lite)">4,300</span></td></tr>
                <tr><td>حجم الطباعة</td><td>180×180×180 ملم</td><td>260×260×255 ملم</td><td>330×320×325 ملم</td></tr>
                <tr><td>الألوان المتعددة</td><td>AMS lite، 4</td><td>CFS Lite، 4</td><td>AMS lite، 4</td></tr>
                <tr><td>الوزن</td><td>5.5 كجم</td><td>9.12 كجم</td><td>12.8 كجم</td></tr>
              </tbody>
            </table>
          </div>
          <ul>
            <li><b><a href="/3d/ar/blog/creality-sparkx-i7-review-saudi-arabia/">Creality SparkX i7</a></b>: لوح أكبر بسعر مقارب، مع برامج أقل نضجًا. تُباع بالطلب المسبق.</li>
            <li><b><a href="/3d/ar/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/">Bambu Lab A2L</a></b>: تجربة بامبو لاب نفسها بحجم يقارب الضعف لكل جهة، بسعر أعلى ومساحة أكبر.</li>
            <li><b><a href="/3d/ar/product/snapmaker-u1/">Snapmaker U1</a></b> (<span data-b3d-price="snapmaker-u1">5,699</span> ريال): 4 رؤوس طباعة منفصلة بدل رأس واحد، فهدر أقل بكثير في المطبوعات كثيرة الألوان. تستحق إذا كنت تطبع بألوان كثيرة يوميًا. راجع <a href="/3d/ar/blog/multi-color-3d-printing-explained/">AMS مقابل CANVAS مقابل SnapSwap</a>.</li>
          </ul>

          <h2>الخلاصة</h2>
          <p>إذا أردت أن تنجح طباعاتك الأولى، وأن تطبع بالألوان دون تعلّم ضبط الطابعة، فإن A1 mini Combo هي الشراء الأضمن في السعودية اليوم. اختر A2L إذا كنت تعرف أنك ستطبع قطعًا كبيرة، وطابعة مغلقة إذا احتجت ABS أو ASA. وعند وصولها اتبع <a href="/3d/ar/blog/bambu-lab-a1-mini-setup-guide/">دليل التشغيل في 7 خطوات</a>.</p>

          <h2>أسئلة شائعة</h2>
          <h3>كم سعر Bambu Lab A1 mini Combo في السعودية؟</h3>
          <p>لدى بلاك آرو 3D سعرها <span data-b3d-price="bambu-lab-a1-mini|Combo (printer + AMS lite)">2,699</span> ريال شاملة الضريبة، مع توصيل مجاني.</p>
          <h3>ماذا تفعل وحدة AMS lite؟</h3>
          <p>تحمل 4 بكرات وتغذي الطابعة بها تلقائيًا، فتستخدم الطبعة الواحدة حتى 4 ألوان أو خامات.</p>
          <h3>هل A1 mini مناسبة للمبتدئين؟</h3>
          <p>نعم. تعاير نفسها وتطبع من تطبيق الجوال، ما يجعلها من أسهل الطابعات للبدء.</p>
          <h3>هل تطبع A1 mini خامتي PETG وTPU؟</h3>
          <p>نعم. تطبع PLA وPETG وTPU وPVA. أما ABS وASA فلا يُنصح بهما لأنها طابعة مفتوحة.</p>

          <div class="b3d-article__cta">
            <p>اطلب A1 mini Combo</p>
            <a href="/3d/ar/product/bambu-lab-a1-mini/" class="btn btn-primary">السعر والتوفر</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/bambu-lab-a1-mini/">Bambu Lab A1 mini Combo</a>
            <a href="/3d/ar/blog/bambu-lab-a1-mini-setup-guide/">دليل تشغيل A1 mini</a>
            <a href="/3d/ar/blog/best-3d-printer-for-beginners-saudi-arabia/">أفضل طابعة للمبتدئين</a>
          </div>
''',
        },
    },

    # ------------------------------------------------------------------
    # 3. REFRESH: A1 / A1 mini setup guide (moved from build_3d_troubleshooting_guides.GUIDES)
    # ------------------------------------------------------------------
    {
        'slug': 'bambu-lab-a1-mini-setup-guide',
        'published': '2026-10-13',
        'en': {
            'headline': 'Bambu Lab A1 and A1 mini Setup Guide: Your First Day',
            'title': 'Bambu Lab A1 / A1 mini Setup Guide | Black Arrow 3D',
            'desc': 'Set up a Bambu Lab A1 or A1 mini step by step: unboxing, transport screws, calibration, Wi-Fi and the Bambu Handy app, loading the AMS lite, your first print and first-day fixes.',
            'meta_line': 'Getting Started &middot; Updated November 10, 2026 &middot; 8 min read',
            'lead': 'Just got your A1 or A1 mini? Follow these 7 steps in order and you will have your first print running in under an hour. At the end are fixes for the problems new owners hit most on day one.',
            'card': ('Getting Started', '8 min read', 'From unboxing to your first print: calibration, Wi-Fi, the Bambu Handy app, loading filament and first-day fixes.'),
            'body': '''
          <h2>Before you start</h2>
          <ul>
            <li>About 45 to 60 minutes, most of it the printer calibrating itself.</li>
            <li>A phone with the <b>Bambu Handy</b> app, and your Wi-Fi name and password.</li>
            <li>A sturdy table: about 50&nbsp;cm deep for the A1 mini, more for the A1, because the bed moves front to back.</li>
            <li>At least one spool of PLA. The box only has small samples.</li>
          </ul>

          <h2>1. Pick a good spot</h2>
          <p>Put the printer on a sturdy, level table with space around it, because the bed moves back and forth while printing. Keep it away from AC vents, direct sun and dust. Cold air blowing across the bed is a common cause of warped corners. You need a normal wall socket and a Wi-Fi signal.</p>

          <h2>2. Unbox and remove the packaging</h2>
          <p>Take out all the foam, cable ties and tape, and remove the transport screws and fixings shown in the Quick Start Guide that comes in the box. Do not skip this: a locked axis will make the calibration fail. Keep the box for a few weeks in case you need to move or return the printer.</p>

          <h2>3. Assemble and connect</h2>
          <ul>
            <li>Fit the spool holder, or the AMS lite if you have the Combo, as shown in the Quick Start Guide. Connect the AMS lite PTFE tubes and cable before the first start.</li>
            <li>Make sure the build plate sits flat and lined up on the bed.</li>
            <li>Connect the power cable and switch the printer on.</li>
          </ul>

          <h2>4. Run the first calibration</h2>
          <p>On first start the screen walks you through setup. Let the printer run its full automatic calibration (bed leveling, vibration compensation and motor checks). It is noisy and takes a while; this is normal. Do not touch the bed or table while it runs.</p>

          <h2>5. Connect Wi-Fi and the app</h2>
          <ul>
            <li>Install the <b>Bambu Handy</b> app on your phone and create a Bambu Lab account.</li>
            <li>Connect the printer to your Wi-Fi from the screen, then bind it to your account in the app. If the printer cannot see your network, check that your router&#39;s 2.4&nbsp;GHz band is switched on.</li>
            <li>Install a firmware update if the printer offers one, and do not switch it off during the update.</li>
            <li>On a computer, install <b>Bambu Studio</b> to slice your own models.</li>
          </ul>

          <h2>6. Load filament</h2>
          <p>Start with PLA or PLA+: it is the easiest material to print. Cut the filament end at an angle, feed it in, and use the load option on the screen. With an AMS lite, place up to four spools and load each one. Set the correct material type and color for each slot so the printer uses the right temperatures. Bambu Lab spools with RFID tags are detected automatically; for other brands, pick the material in the app.</p>

          <h2>7. Your first print</h2>
          <p>Print one of the models stored on the printer, or pick a popular model on MakerWorld from the Bambu Handy app and send it to the printer. Watch the first layer: it should be flat, even and well stuck to the plate. When it finishes, let the plate cool for a minute, then flex it gently to release the print.</p>

          <h2>First-day problems and quick fixes</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>Problem</th><th>What to do</th></tr></thead>
              <tbody>
                <tr><td>Calibration stops with an error</td><td>Check that every transport screw, tie and piece of foam is removed, then run calibration again.</td></tr>
                <tr><td>Printer cannot find your Wi-Fi</td><td>Switch on the router&#39;s 2.4&nbsp;GHz band, move closer to the router, and check the password.</td></tr>
                <tr><td>Filament will not load</td><td>Cut a clean, angled tip, straighten the first 10&nbsp;cm, and push until the extruder grips it.</td></tr>
                <tr><td>First layer not sticking</td><td>Wash the plate with dish soap and water, do not touch the print surface, and keep AC air off the bed. See <a href="/3d/blog/3d-print-bed-adhesion-first-layer/">first layer not sticking</a>.</td></tr>
                <tr><td>Thin strings between parts</td><td>Usually damp filament. Dry the spool and see <a href="/3d/blog/3d-print-stringing-fix/">how to fix stringing</a>.</td></tr>
                <tr><td>Nothing comes out of the nozzle</td><td>See <a href="/3d/blog/clogged-3d-printer-nozzle-fix/">how to clear a clogged nozzle</a>.</td></tr>
              </tbody>
            </table>
          </div>

          <h2>Tips for the first week</h2>
          <ul>
            <li>Keep the build plate clean: wash it with dish soap and water and hold it by the edges.</li>
            <li>Store filament sealed with desiccant, especially in humid cities like Jeddah, Dammam and Khobar. The AMS lite is open to room air.</li>
            <li>Keep a spare nozzle: the <a href="/3d/product/bambu-hotend-a1-series/">A1-series hotend</a> swaps in under a minute, with a hardened-steel option for abrasive filaments.</li>
          </ul>

          <h2>FAQ</h2>
          <h3>How long does it take to set up a Bambu Lab A1 mini?</h3>
          <p>About 45 to 60 minutes from opening the box to your first print. Most of that time is the automatic calibration.</p>
          <h3>Do I need a computer to use the A1 mini?</h3>
          <p>No. You can print models from MakerWorld with the Bambu Handy app on your phone. A computer with Bambu Studio is useful when you want to slice your own models.</p>
          <h3>Which filament should I start with?</h3>
          <p>PLA. It is the easiest to print and right for most first projects. See <a href="/3d/blog/which-filament-for-which-print/">which filament for which print</a>.</p>
          <h3>Does this guide work for the A1 as well?</h3>
          <p>Yes. The A1 and A1 mini set up the same way; the A1 is simply bigger.</p>

          <div class="b3d-article__cta">
            <p>Need filament or a spare hotend?</p>
            <a href="/3d/shop/filament/" class="btn btn-primary">Shop filament</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/bambu-lab-a1-mini-combo-review/">A1 mini Combo review</a>
            <a href="/3d/product/bambu-hotend-a1-series/">Bambu Hotend &mdash; A1 Series</a>
            <a href="/3d/blog/best-filament-for-bambu-lab-a1-ams-lite/">Best filament for the A1 and AMS lite</a>
          </div>
''',
        },
        'ar': {
            'headline': 'دليل تشغيل بامبو لاب A1 وA1 mini: يومك الأول',
            'title': 'دليل تشغيل بامبو لاب A1 وA1 mini | Black Arrow 3D',
            'desc': 'شغّل طابعة بامبو لاب A1 أو A1 mini خطوة بخطوة: الفتح وبراغي النقل والمعايرة والواي فاي وتطبيق Bambu Handy وتحميل AMS lite وأول طباعة وحلول مشكلات اليوم الأول.',
            'meta_line': 'البداية &middot; تحديث 10 نوفمبر 2026 &middot; 8 دقائق قراءة',
            'lead': 'وصلتك A1 أو A1 mini؟ اتبع هذه الخطوات السبع بالترتيب وستبدأ أول طباعة لك في أقل من ساعة. وفي النهاية حلول لأكثر المشكلات التي يواجهها الملاك الجدد في اليوم الأول.',
            'card': ('البداية', '8 دقائق قراءة', 'من فتح الصندوق إلى أول طباعة: المعايرة والواي فاي وتطبيق Bambu Handy وتحميل الفلمنت وحلول اليوم الأول.'),
            'body': '''
          <h2>قبل أن تبدأ</h2>
          <ul>
            <li>نحو 45 إلى 60 دقيقة، معظمها والطابعة تعاير نفسها.</li>
            <li>جوال عليه تطبيق <b>Bambu Handy</b>، واسم شبكة الواي فاي وكلمة مرورها.</li>
            <li>طاولة متينة: بعمق 50 سم تقريبًا لـ A1 mini وأكثر لـ A1، لأن السرير يتحرك للأمام والخلف.</li>
            <li>بكرة PLA واحدة على الأقل، فالصندوق فيه عينات صغيرة فقط.</li>
          </ul>

          <h2>1. اختر مكانًا مناسبًا</h2>
          <p>ضع الطابعة على طاولة ثابتة ومستوية مع مساحة حولها، لأن السرير يتحرك للأمام والخلف أثناء الطباعة. أبعدها عن فتحات المكيف وأشعة الشمس المباشرة والغبار، فالهواء البارد على السرير سبب شائع لالتواء الزوايا. تحتاج مقبس كهرباء عاديًا وإشارة واي فاي.</p>

          <h2>2. افتح الصندوق وأزل التغليف</h2>
          <p>أخرج كل الفلين وروابط الأسلاك والأشرطة، وأزل براغي ومثبتات النقل الموضحة في دليل البدء السريع داخل الصندوق. لا تتجاوز هذه الخطوة، فالمحور المثبت سيُفشل المعايرة. احتفظ بالصندوق لبضعة أسابيع في حال احتجت لنقل الطابعة أو إرجاعها.</p>

          <h2>3. التركيب والتوصيل</h2>
          <ul>
            <li>ركّب حامل البكرة، أو وحدة AMS lite إن كانت لديك نسخة الكومبو، كما في دليل البدء السريع. وصّل أنابيب PTFE وكابل AMS lite قبل التشغيل الأول.</li>
            <li>تأكد أن سطح الطباعة مستوٍ ومثبت في مكانه على السرير.</li>
            <li>وصّل كابل الكهرباء وشغّل الطابعة.</li>
          </ul>

          <h2>4. شغّل المعايرة الأولى</h2>
          <p>عند التشغيل الأول ترشدك الشاشة خطوة بخطوة. اترك الطابعة تكمل المعايرة التلقائية كاملة (تسوية السرير وتعويض الاهتزاز وفحص المحركات). تصدر صوتًا وتستغرق وقتًا، وهذا طبيعي. لا تلمس السرير أو الطاولة أثناءها.</p>

          <h2>5. اربط الواي فاي والتطبيق</h2>
          <ul>
            <li>ثبّت تطبيق <b>Bambu Handy</b> على جوالك وأنشئ حساب Bambu Lab.</li>
            <li>اربط الطابعة بالواي فاي من الشاشة، ثم اربطها بحسابك من التطبيق. إذا لم تظهر شبكتك فتأكد أن نطاق 2.4 جيجاهرتز مفعّل في الراوتر.</li>
            <li>ثبّت تحديث البرنامج الثابت إن ظهر لك، ولا تطفئ الطابعة أثناء التحديث.</li>
            <li>على الكمبيوتر ثبّت برنامج <b>Bambu Studio</b> لتجهيز مجسماتك الخاصة.</li>
          </ul>

          <h2>6. حمّل الفلمنت</h2>
          <p>ابدأ بـ PLA أو PLA+ لأنه أسهل خامة للطباعة. اقطع طرف الفلمنت بشكل مائل وأدخله ثم استخدم خيار التحميل من الشاشة. مع AMS lite ضع حتى أربع بكرات وحمّل كل واحدة. اختر نوع الخامة واللون الصحيحين لكل خانة لتستخدم الطابعة الحرارة المناسبة. بكرات بامبو لاب ذات شريحة RFID تُكتشف تلقائيًا، أما العلامات الأخرى فاختر خامتها من التطبيق.</p>

          <h2>7. أول طباعة</h2>
          <p>اطبع أحد المجسمات المحفوظة في الطابعة، أو اختر مجسمًا مشهورًا من MakerWorld عبر تطبيق Bambu Handy وأرسله للطابعة. راقب الطبقة الأولى: يجب أن تكون مستوية ومتساوية وملتصقة جيدًا بالسطح. وعند الانتهاء اترك اللوح يبرد دقيقة ثم اثنِه بلطف لتحرير القطعة.</p>

          <h2>مشكلات اليوم الأول وحلولها السريعة</h2>
          <div class="b3d-table-wrap">
            <table>
              <thead><tr><th>المشكلة</th><th>ماذا تفعل</th></tr></thead>
              <tbody>
                <tr><td>المعايرة تتوقف بخطأ</td><td>تأكد من إزالة كل براغي النقل والروابط والفلين، ثم أعد المعايرة.</td></tr>
                <tr><td>الطابعة لا تجد الواي فاي</td><td>فعّل نطاق 2.4 جيجاهرتز في الراوتر، واقترب منه، وتحقق من كلمة المرور.</td></tr>
                <tr><td>الفلمنت لا يُحمَّل</td><td>اقطع طرفًا نظيفًا مائلًا، وافرد أول 10 سم، وادفعه حتى يمسكه الإكسترودر.</td></tr>
                <tr><td>الطبقة الأولى لا تلتصق</td><td>اغسل اللوح بالماء وسائل الصحون، ولا تلمس سطح الطباعة، وأبعد هواء المكيف عن السرير. راجع <a href="/3d/ar/blog/3d-print-bed-adhesion-first-layer/">الطبقة الأولى لا تلتصق</a>.</td></tr>
                <tr><td>خيوط رفيعة بين الأجزاء</td><td>غالبًا بسبب رطوبة الفلمنت. جفف البكرة وراجع <a href="/3d/ar/blog/3d-print-stringing-fix/">حل مشكلة الخيوط الرفيعة</a>.</td></tr>
                <tr><td>لا يخرج شيء من الفوهة</td><td>راجع <a href="/3d/ar/blog/clogged-3d-printer-nozzle-fix/">كيف تفك انسداد الفوهة</a>.</td></tr>
              </tbody>
            </table>
          </div>

          <h2>نصائح للأسبوع الأول</h2>
          <ul>
            <li>حافظ على نظافة سطح الطباعة: اغسله بالماء وسائل الصحون وأمسكه من الأطراف.</li>
            <li>احفظ الفلمنت في كيس محكم مع مادة مجففة، خصوصًا في المدن الرطبة مثل جدة والدمام والخبر، فوحدة AMS lite مكشوفة لهواء الغرفة.</li>
            <li>احتفظ بفوهة احتياطية: <a href="/3d/ar/product/bambu-hotend-a1-series/">هوت إند سلسلة A1</a> يُبدَّل في أقل من دقيقة، ويتوفر بخيار فولاذ مقسّى للخيوط الكاشطة.</li>
          </ul>

          <h2>أسئلة شائعة</h2>
          <h3>كم يستغرق تشغيل بامبو لاب A1 mini؟</h3>
          <p>نحو 45 إلى 60 دقيقة من فتح الصندوق إلى أول طباعة، ومعظم هذا الوقت للمعايرة التلقائية.</p>
          <h3>هل أحتاج إلى كمبيوتر لاستخدام A1 mini؟</h3>
          <p>لا. يمكنك طباعة مجسمات MakerWorld عبر تطبيق Bambu Handy على جوالك. والكمبيوتر مع Bambu Studio مفيد عندما تريد تجهيز مجسماتك الخاصة.</p>
          <h3>بأي فلمنت أبدأ؟</h3>
          <p>‏PLA، فهو الأسهل طباعة ومناسب لمعظم المشاريع الأولى. راجع <a href="/3d/ar/blog/which-filament-for-which-print/">أي فلمنت لأي طباعة</a>.</p>
          <h3>هل يصلح هذا الدليل لطابعة A1 أيضًا؟</h3>
          <p>نعم. يتم تشغيل A1 وA1 mini بالطريقة نفسها، وA1 أكبر حجمًا فقط.</p>

          <div class="b3d-article__cta">
            <p>تحتاج فلمنت أو هوت إند احتياطي؟</p>
            <a href="/3d/ar/shop/filament/" class="btn btn-primary">تسوّق الفلمنت</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/bambu-lab-a1-mini-combo-review/">مراجعة A1 mini كومبو</a>
            <a href="/3d/ar/product/bambu-hotend-a1-series/">هوت إند بامبو &mdash; سلسلة A1</a>
            <a href="/3d/ar/blog/best-filament-for-bambu-lab-a1-ams-lite/">أفضل خيوط لـ A1 وAMS lite</a>
          </div>
''',
        },
    },
]
