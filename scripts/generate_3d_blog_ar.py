#!/usr/bin/env python3
"""Generates Arabic mirrors of the /3d/blog/ articles under /3d/ar/blog/,
plus the AR blog index. Reuses the same chrome-translation helpers as
generate_3d_static.py (nav/footer text + internal hrefs); article body
copy is a hand-written faithful translation (not machine-generated),
using the exact product-name transliterations already established in
3d-products.json's name_ar fields, so terminology matches the rest of
the site. Prices, units and specs are left as-is — only the surrounding
language is translated, nothing about a product's facts changes.

DRAFT translation, like every other piece of AR copy in this project:
flagged for Afzal's review, not treated as final/legal-approved text.

Usage: python scripts/generate_3d_blog_ar.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_3d_static import (
    ROOT, SITE, translate_static_chrome, localize_ar_hrefs, lang_toggle_link, write
)

BLOG_ROOT = os.path.join(ROOT, '3d', 'blog')
AR_BLOG_ROOT = os.path.join(ROOT, '3d', 'ar', 'blog')

POSTS = {
    '3d-printer-maintenance-guide': {
        'meta_description': 'أكثر القطع عرضة للتلف في طابعة FDM ثلاثية الأبعاد — الهوت إند، والإكسترودر، وذراع قاطع الفلمنت — وظيفتها، ومتى يجب استبدالها.',
        'headline': 'دليل صيانة الطابعة ثلاثية الأبعاد: حافظ على استمرار عمل طابعتك',
        'meta_line': 'الصيانة &middot; 15 سبتمبر 2026 &middot; 5 دقائق قراءة',
        'lead': 'معظم مشاكل الطابعات ثلاثية الأبعاد ليست خطأ الطابعة نفسها — بل قطعة تآكلت وكان يجب استبدالها منذ أسابيع. إليك ما يجب فحصه.',
        'body': '''
          <h2>الهوت إند هو أول ما يتآكل</h2>
          <p>كل عملية طباعة تدفع الفلمنت عبر الفوهة، والمواد الكاشطة (خاصة الفلمنت المقوى بألياف الكربون أو الزجاج) توسّع فتحة الفوهة تدريجياً مع الوقت، مما يؤدي إلى ضعف الطباعة وخشونة في سطح المطبوع. إذا كنت تطبع مواد هندسية بانتظام، احتفظ بفوهة احتياطية بدلاً من انتظار عطل في منتصف المشروع &mdash; منتجنا <a href="/3d/ar/product/bambu-hotend-a1-series/">هوت إند بامبو &mdash; سلسلة A1</a> متوفر بأربعة أحجام فوهة (0.2/0.4/0.6/0.8&nbsp;مم) لطابعتي A1 وA1 ميني.</p>

          <h2>تروس الإكسترودر تفقد قبضتها مع الوقت</h2>
          <p>التروس التي تمسك الفلمنت وتدفعه نحو الهوت إند تتآكل أيضاً، خاصة مع المواد الأصعب، مما يؤدي إلى طباعة غير منتظمة وتخطي خطوات تسمعها كصوت طقطقة. <a href="/3d/ar/product/a1-series-extruder-unit/">وحدة إكسترودر &mdash; سلسلة A1</a> تستخدم تروسًا مزدوجة من الفولاذ المقسّى مصممة خصيصاً لمقاومة هذا النوع من التآكل.</p>

          <h2>ذراع قاطع الفلمنت قطعة صغيرة لكنها تسبب مشاكل كبيرة</h2>
          <p>في الطابعات المزودة بقاطع فلمنت تلقائي، الذراع الذي يثبّت القاطع ومغناطيس استشعار القطع هو قطعة ميكانيكية بسيطة قد تتشقق بعد الاستخدام المتكرر. عند حدوث ذلك، إما أن تفشل الطابعة في قطع الفلمنت بشكل نظيف أو تُظهر أخطاء استشعار قطع وهمية. إصلاحها رخيص وسريع &mdash; راجع <a href="/3d/ar/product/filament-cutter-lever/">ذراع قاطع الفلمنت</a> لدينا.</p>

          <h2>علامات تدل على حاجتك لفحص القطع</h2>
          <ul>
            <li>ضعف في الطباعة أو طبقات رقيقة وهشة في مطبوعات كانت تخرج سليمة من قبل</li>
            <li>أصوات طقطقة أو تخطي من محرك الإكسترودر أثناء الطباعة</li>
            <li>أخطاء في قطع الفلمنت أو طابعة لا تبدّل الألوان بشكل موثوق</li>
            <li>سطح طباعة أخشن مما اعتدت عليه بنفس الإعدادات</li>
          </ul>

          <p>معظم هذه الإصلاحات لا تستغرق أكثر من 10 دقائق إذا انتبهت لها مبكراً، وتكلفتها أقل بكثير من طابعة متوقفة عن العمل بسبب عطل بسيط.</p>

          <div class="b3d-article__cta">
            <p>جهّز قطع الغيار قبل أن تحتاجها</p>
            <a href="/3d/ar/shop/accessories/" class="btn btn-primary">تسوّق الملحقات</a>
          </div>

          <h2>منتجات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/bambu-hotend-a1-series/">هوت إند بامبو &mdash; سلسلة A1</a>
            <a href="/3d/ar/product/a1-series-extruder-unit/">وحدة إكسترودر &mdash; سلسلة A1</a>
            <a href="/3d/ar/product/filament-cutter-lever/">ذراع قاطع الفلمنت</a>
          </div>
        ''',
    },
    'bambu-lab-a1-vs-a1-mini-vs-a2l': {
        'meta_description': 'مقارنة حجم الطباعة والسعر وخيارات الباقات بين طابعات بامبو لاب A1 ميني وA1 وA2L لمساعدتك على اختيار الطابعة المناسبة لمشاريعك.',
        'headline': 'بامبو لاب A1 مقابل A1 ميني مقابل A2L: أيهما يجب أن تشتري؟',
        'meta_line': 'مقارنة &middot; 15 سبتمبر 2026 &middot; 6 دقائق قراءة',
        'lead': 'الطابعات الثلاث تشترك في نفس منصة بامبو لاب سهلة الاستخدام. القرار الحقيقي يعتمد على حجم مطبوعاتك المطلوب وميزانيتك.',
        'body': '''
          <table>
            <tr><th></th><th>A1 ميني</th><th>A1</th><th>A2L</th></tr>
            <tr><td>حجم الطباعة</td><td>180 &times; 180 &times; 180&nbsp;مم</td><td>256 &times; 256 &times; 256&nbsp;مم</td><td>330 &times; 320 &times; 325&nbsp;مم</td></tr>
            <tr><td>السرعة القصوى</td><td>500&nbsp;مم/ث</td><td>500&nbsp;مم/ث</td><td>500&nbsp;مم/ث</td></tr>
            <tr><td>تعدد الألوان</td><td>AMS lite (باقة)</td><td>AMS Lite (باقة)</td><td>AMS / AMS Lite (باقة)</td></tr>
            <tr><td>سعر الطابعة منفردة</td><td>1,699&nbsp;ريال</td><td>2,699&nbsp;ريال</td><td>3,699&nbsp;ريال</td></tr>
            <tr><td>سعر الباقة</td><td>2,799&nbsp;ريال</td><td>3,530&nbsp;ريال</td><td>4,650&nbsp;ريال</td></tr>
          </table>

          <h2>بامبو لاب A1 ميني &mdash; أصغر مساحة على المكتب وأقل سعر</h2>
          <p><a href="/3d/ar/product/bambu-lab-a1-mini/">A1 ميني</a> هو الخيار الأنسب إذا كانت مساحة مكتبك محدودة أو كنت تطبع غالباً قطعاً صغيرة &mdash; تماثيل، إكسسوارات هواتف، حوامل صغيرة. بحجم 180&nbsp;مم لكل ضلع، هي الأصغر بين الثلاث والأرخص للدخول إلى منظومة بامبو لاب.</p>

          <h2>بامبو لاب A1 &mdash; الخيار المتوازن في المنتصف</h2>
          <p><a href="/3d/ar/product/bambu-lab-a1/">A1</a> يقفز إلى حجم طباعة 256&nbsp;مم مكعب &mdash; كافٍ لمعظم إكسسوارات الكوسبلاي والقطع المنزلية الأكبر والمطبوعات متعددة الأجزاء دون تقسيم النموذج. نفس سرعة الطباعة مثل A1 ميني، ونفس خيار باقة AMS Lite، مع مساحة أكبر.</p>

          <h2>بامبو لاب A2L &mdash; للمطبوعات كبيرة الحجم فعلاً</h2>
          <p><a href="/3d/ar/product/bambu-lab-a2l/">A2L</a> مصممة للحجم الكبير: 330 &times; 320 &times; 325&nbsp;مم (حوالي 34.3&nbsp;لتر)، مناسبة للأغلفة الكبيرة والإنتاج بالدفعات، أو المطبوعات كبيرة الحجم التي لا تناسب أي طابعة أخرى في المجموعة. حالياً هي متاحة للطلب المسبق في كتالوجنا.</p>

          <h2>الخلاصة</h2>
          <p>اشترِ A1 ميني إذا كنت مبتدئاً أو مساحتك محدودة، وA1 إذا أردت طابعة متعددة الاستخدامات فعلاً للاستخدام اليومي، وA2L إذا كانت مشاريعك عادةً أكبر من مكعب 256&nbsp;مم.</p>

          <div class="b3d-article__cta">
            <p>قارن الثلاث جنباً إلى جنب بمواصفات مباشرة</p>
            <a href="/3d/compare/" class="btn btn-primary">افتح أداة المقارنة</a>
          </div>

          <h2>منتجات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/bambu-lab-a1-mini/">بامبو لاب A1 ميني</a>
            <a href="/3d/ar/product/bambu-lab-a1/">بامبو لاب A1</a>
            <a href="/3d/ar/product/bambu-lab-a2l/">بامبو لاب A2L</a>
          </div>
        ''',
    },
    'best-3d-printer-for-beginners-saudi-arabia': {
        'meta_description': 'ما هي الطابعة ثلاثية الأبعاد المناسبة للمشتري لأول مرة في السعودية؟ نقارن بين بامبو لاب A1 ميني وكرياليتي سباركس آي 7 من حيث السعر وسهولة الاستخدام ومحتويات الصندوق.',
        'headline': 'أفضل طابعة ثلاثية الأبعاد للمبتدئين في السعودية (دليل 2026)',
        'meta_line': 'دليل الشراء &middot; 15 سبتمبر 2026 &middot; 7 دقائق قراءة',
        'lead': 'إذا كنت تشتري أول طابعة ثلاثية الأبعاد لك، فأهم شيئين هما مدى سهولة الحصول على طباعة جيدة من اليوم الأول، وكم تكلفة ذلك. إليك كيف تقارن الطابعات المناسبة للمبتدئين في كتالوجنا.',
        'body': '''
          <h2>ما الذي يهم فعلاً في أول طابعة</h2>
          <p>تجاوز تفاصيل جداول المواصفات المعقدة. بالنسبة لأول جهاز، هناك أربعة أمور تحدد ما إذا كنت ستستمتع بالهواية أو تتخلى عنها بعد أسبوع:</p>
          <ul>
            <li><strong>المعايرة التلقائية للسرير</strong> &mdash; المعايرة اليدوية هي السبب الأول لفشل الطبقة الأولى لدى المبتدئين.</li>
            <li><strong>هوت إند معدني بالكامل</strong> &mdash; يتيح لك طباعة PETG وTPU لاحقاً، وليس فقط PLA.</li>
            <li><strong>حجم طباعة معقول</strong> &mdash; أي شيء من 180&nbsp;مم إلى 260&nbsp;مم لكل ضلع يغطي غالبية مطبوعات الهواة (حوامل هواتف، حوامل، تماثيل، قطع غيار).</li>
            <li><strong>مساحة للتطور</strong> &mdash; مسار ترقية عبر الباقة/AMS حتى لا تبقى عالقاً في الطباعة أحادية اللون للأبد.</li>
          </ul>

          <h2>اختيارنا للمبتدئين تماماً: بامبو لاب A1 ميني</h2>
          <p><a href="/3d/ar/product/bambu-lab-a1-mini/">بامبو لاب A1 ميني</a> هي أسهل طابعة في كتالوجنا للحصول على أول طباعة ناجحة. تحتوي على معايرة تلقائية للسرير، وهوت إند معدني بالكامل يتحمل حتى 300 درجة مئوية، وحساس نفاد الفلمنت، واستعادة الطباعة عند انقطاع الكهرباء &mdash; بحيث لا يفسد انقطاع التيار المفاجئ العمل في منتصف الطباعة. حجم الطباعة 180 &times; 180 &times; 180&nbsp;مم، وهو كافٍ لمعظم مشاريع المبتدئين.</p>
          <p>تبدأ بسعر 1,699 ريال منفردة، أو 2,799 ريال كباقة مع وحدة AMS lite إذا أردت الطباعة متعددة الألوان من اليوم الأول.</p>

          <h2>أفضل بديل من حيث القيمة: كرياليتي سباركس آي 7</h2>
          <p><a href="/3d/ar/product/creality-sparkx-i7/">كرياليتي سباركس آي 7</a> هي الأقل سعراً في كتالوجنا بسعر 2,090 ريال، وتدعم بالفعل الطباعة متعددة الألوان عبر CFS Lite والاتصال بسحابة Creality Cloud. خيار جيد لمشاريع PLA وPETG إذا أردت البدء ببساطة والحفاظ على ميزانية محدودة، مع باقة متاحة بسعر 2,650 ريال.</p>

          <h2>متى تفكر في باقة بدلاً من الطابعة المنفردة</h2>
          <p>إذا كانت الطباعة متعددة الألوان هي سبب دخولك عالم الطباعة ثلاثية الأبعاد &mdash; هدايا، قطع بعلامة تجارية، تماثيل متعددة الألوان &mdash; فالأفضل دفع الفرق للحصول على الباقة من البداية بدلاً من شراء وحدة AMS بشكل منفصل لاحقاً. كل من A1 ميني وسباركس آي 7 يقدمان هذا كخيار باقة.</p>

          <div class="b3d-article__cta">
            <p>مستعد لاختيار أول طابعة لك؟</p>
            <a href="/3d/ar/shop/3d-printers/" class="btn btn-primary">تسوّق الطابعات ثلاثية الأبعاد</a>
          </div>

          <h2>منتجات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/bambu-lab-a1-mini/">بامبو لاب A1 ميني</a>
            <a href="/3d/ar/product/creality-sparkx-i7/">كرياليتي سباركس آي 7</a>
            <a href="/3d/ar/product/filament-pla-1kg/">فلمنت PLA 1 كجم</a>
          </div>
        ''',
    },
    'buy-3d-printer-saudi-arabia-price-guide': {
        'meta_description': 'كل طابعة ثلاثية الأبعاد نوفرها في السعودية، مع أسعار حالية بالريال، وما يجب فحصه قبل الشراء محلياً مقابل الاستيراد &mdash; الضمان، مدة التوصيل، وخدمة ما بعد البيع.',
        'headline': 'أين تشتري طابعة ثلاثية الأبعاد في السعودية (دليل أسعار 2026 بالريال)',
        'meta_line': 'دليل الأسعار &middot; 15 سبتمبر 2026 &middot; 6 دقائق قراءة',
        'lead': 'شراء طابعة ثلاثية الأبعاد في السعودية عادة يعني الاختيار بين الاستيراد بنفسك أو الشراء من مورد محلي. إليك ما يتغير فعلياً، وكل الأسعار في كتالوجنا الحالي.',
        'body': '''
          <h2>الشراء المحلي مقابل الاستيراد: ما الذي يتغير فعلياً</h2>
          <p>الطلب مباشرة من الخارج قد يبدو أرخص من حيث السعر المعلن، لكنه عادة يأتي مع مقايضات حقيقية عند احتساب الصورة الكاملة:</p>
          <ul>
            <li><strong>الجمارك ووقت الشحن</strong> &mdash; الطلبات الدولية قد تستغرق أسابيع، ومعاملة الجمارك غير متوقعة.</li>
            <li><strong>دعم الضمان</strong> &mdash; الطابعة التي تتعطل بعد شراء خارجي غالباً تعني إعادة شحنها خارج البلاد، أو عدم وجود دعم إطلاقاً.</li>
            <li><strong>دعم بالعربية والإنجليزية</strong> &mdash; المشترون المحليون يحصلون على دعم بلغتهم ومنطقتهم الزمنية، وليس عبر طابور تذاكر دعم خارجي.</li>
            <li><strong>وضوح الأسعار وضريبة القيمة المضافة</strong> &mdash; الأسعار المحلية معلنة بالريال مع احتساب الضريبة مسبقاً، دون رسوم استيراد مفاجئة عند التوصيل.</li>
          </ul>
          <p>بالنسبة للهاوي الذي يشتري طابعة واحدة، قد ينجح الاستيراد إذا كنت مرتاحاً للانتظار والتعامل مع أي مشاكل بنفسك. أما للشركات وورش العمل والمدارس التي تشتري عدة وحدات &mdash; أو أي شخص يريد طابعة تعمل وجهة دعم حقيقية عند حدوث مشكلة &mdash; فالشراء المحلي عادة هو الخيار الأكثر أماناً.</p>

          <h2>كل طابعة ثلاثية الأبعاد في كتالوجنا، مرتبة حسب السعر</h2>
          <table>
            <tr><th>الطابعة</th><th>العلامة التجارية</th><th>السعر</th></tr>
            <tr><td><a href="/3d/ar/product/flashforge-adventurer-5m/">فلاش فورج أدفنتشرر 5M</a></td><td>فلاش فورج</td><td>1,559 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/bambu-lab-a1-mini/">بامبو لاب A1 ميني</a></td><td>بامبو لاب</td><td>1,699 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/creality-sparkx-i7/">كرياليتي سباركس آي 7</a></td><td>كرياليتي</td><td>2,090 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/bambu-lab-a1/">بامبو لاب A1</a></td><td>بامبو لاب</td><td>2,699 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/anycubic-kobra-3-max/">أنيكيوبك كوبرا 3 ماكس</a></td><td>أنيكيوبك</td><td>3,090 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/elegoo-centauri-carbon-2/">إليجو سنتوري كاربون 2</a></td><td>إليجو</td><td>3,180 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/bambu-lab-a2l/">بامبو لاب A2L</a></td><td>بامبو لاب</td><td>3,699 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/bambu-lab-p2s/">بامبو لاب P2S</a></td><td>بامبو لاب</td><td>4,499 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/flashforge-creator-5-pro/">فلاش فورج كرييتر 5 برو</a></td><td>فلاش فورج</td><td>5,630 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/snapmaker-u1/">سنابميكر U1</a></td><td>سنابميكر</td><td>5,690 ريال</td></tr>
            <tr><td><a href="/3d/ar/product/bambu-lab-h2c-combo/">بامبو لاب H2C</a></td><td>بامبو لاب</td><td>15,990 ريال</td></tr>
          </table>
          <p><em>الأسعار معروضة بالريال السعودي وصحيحة وقت النشر. بعض الطرازات متاحة للطلب المسبق أو لديها باقات بأسعار مختلفة &mdash; راجع صفحة كل منتج لمعرفة التوفر الحالي.</em></p>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/best-3d-printer-for-beginners-saudi-arabia/">أفضل طابعة للمبتدئين</a>
            <a href="/3d/ar/blog/bambu-lab-a1-vs-a1-mini-vs-a2l/">بامبو لاب A1 مقابل A1 ميني مقابل A2L</a>
            <a href="/3d/ar/shop/3d-printers/">تسوّق كل الطابعات</a>
          </div>
        ''',
    },
    'multi-color-3d-printing-explained': {
        'meta_description': 'كيف تعمل أنظمة الطباعة متعددة الألوان: AMS من بامبو لاب، وCANVAS من إليجو، وSnapSwap من سنابميكر، وأي نهج يناسب أسلوب عملك أكثر.',
        'headline': 'شرح الطباعة ثلاثية الأبعاد متعددة الألوان: AMS مقابل CANVAS مقابل SnapSwap',
        'meta_line': 'كيف يعمل &middot; 15 سبتمبر 2026 &middot; 6 دقائق قراءة',
        'lead': 'لا توجد طريقة واحدة للطباعة بألوان متعددة. كتالوجنا يضم ثلاثة أنظمة مختلفة &mdash; إليك كيف تختلف فعلياً.',
        'body': '''
          <h2>AMS / AMS Lite (بامبو لاب) &mdash; تبديل الفلمنت</h2>
          <p>نظام AMS من بامبو لاب يغذي رأس الطباعة الواحد من عدة بكرات، ويبدّل الفلمنت حسب الحاجة أثناء الطباعة. وهو الأنضج من بين الأنظمة الثلاثة هنا، ومتاح كباقة مع <a href="/3d/ar/product/bambu-lab-a1-mini/">A1 ميني</a>، و<a href="/3d/ar/product/bambu-lab-a1/">A1</a>، و<a href="/3d/ar/product/bambu-lab-a2l/">A2L</a>، و<a href="/3d/ar/product/bambu-lab-p2s/">P2S</a>. المقايضة: تبديل الفلمنت يهدر بعض مادة التنظيف بين تغييرات الألوان.</p>

          <h2>CANVAS (إليجو) &mdash; حتى 4 فلمنتات</h2>
          <p><a href="/3d/ar/product/elegoo-centauri-carbon-2/">إليجو سنتوري كاربون 2</a> تستخدم نظام CANVAS من إليجو، ويدعم أيضاً حتى 4 فلمنتات تغذي رأس طباعة واحد، مقترناً بهوت إند يصل إلى 350 درجة مئوية بحيث لا تقتصر الطباعة متعددة الألوان على PLA فقط.</p>

          <h2>SnapSwap (سنابميكر) &mdash; رؤوس طباعة مستقلة بدلاً من التبديل</h2>
          <p><a href="/3d/ar/product/snapmaker-u1/">سنابميكر U1</a> تتبنى نهجاً مختلفاً تماماً: 4 رؤوس طباعة مستقلة عبر نظام SnapSwap، بدلاً من رأس واحد يتنقل بين الفلمنتات. هذا يقلل من هدر مادة التنظيف الذي تنتجه أنظمة تبديل الفلمنت، على حساب جهاز أكبر وأكثر تعقيداً.</p>

          <h2>فلاش فورج كرييتر 5 برو &mdash; 4 رؤوس طباعة مستقلة بمستوى هندسي</h2>
          <p>بالمثل، تستخدم <a href="/3d/ar/product/flashforge-creator-5-pro/">فلاش فورج كرييتر 5 برو</a> 4 رؤوس طباعة مستقلة، مقترنة بغلاف مُدفّأ وهوت إند يصل إلى 320 درجة مئوية &mdash; مصممة للطباعة متعددة الألوان بمواد أقوى وأكثر مقاومة للحرارة وليس فقط PLA.</p>

          <h2>أيهما يجب أن تحصل عليه؟</h2>
          <ul>
            <li><strong>تريد فقط تجربة الطباعة متعددة الألوان بميزانية محدودة:</strong> باقة AMS Lite مع A1 ميني أو A1.</li>
            <li><strong>تريد هدراً أقل للفلمنت ولا تمانع جهازاً أكبر:</strong> سنابميكر U1 أو فلاش فورج كرييتر 5 برو.</li>
            <li><strong>تحتاج تعدد ألوان بالإضافة لمواد هندسية أقوى:</strong> فلاش فورج كرييتر 5 برو أو إليجو سنتوري كاربون 2.</li>
          </ul>

          <div class="b3d-article__cta">
            <p>شاهد كل طابعة متعددة الألوان لدينا</p>
            <a href="/3d/ar/shop/3d-printers/" class="btn btn-primary">تسوّق الطابعات ثلاثية الأبعاد</a>
          </div>

          <h2>منتجات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/snapmaker-u1/">سنابميكر U1</a>
            <a href="/3d/ar/product/elegoo-centauri-carbon-2/">إليجو سنتوري كاربون 2</a>
            <a href="/3d/ar/product/flashforge-creator-5-pro/">فلاش فورج كرييتر 5 برو</a>
          </div>
        ''',
    },
    'pla-vs-petg-vs-abs-filament-guide': {
        'meta_description': 'مقارنة عملية بين فلمنت PLA وPETG وABS للطباعة ثلاثية الأبعاد FDM &mdash; القوة، مقاومة الحرارة، سهولة الطباعة، وأي الطابعات في كتالوجنا تتعامل مع كل مادة بشكل أفضل.',
        'headline': 'PLA مقابل PETG مقابل ABS: أي فلمنت طباعة ثلاثية الأبعاد يجب أن تستخدم؟',
        'meta_line': 'دليل المواد &middot; 15 سبتمبر 2026 &middot; 6 دقائق قراءة',
        'lead': 'اختيار الفلمنت الخاطئ للمهمة هو أكثر خطأ شائع لدى المبتدئين بعد معايرة السرير. إليك ما تصلح له كل مادة فعلياً.',
        'body': '''
          <h2>PLA &mdash; الخيار الافتراضي، ولسبب وجيه</h2>
          <p>يُطبع PLA بدرجات حرارة أقل، وبالكاد يتقوّس، ولا يحتاج غلافاً أو حجرة مدفأة ليخرج نظيفاً. إنه الخيار المناسب للتماثيل والنماذج الأولية والهدايا ومعظم الأشياء التي لن تكون في سيارة ساخنة أو تتعرض لصدمة قوية. <a href="/3d/ar/product/filament-pla-1kg/">فلمنت PLA 1 كجم</a> لدينا متوفر بـ 8 ألوان ويعمل على كل طابعة FDM نبيعها.</p>

          <h2>PETG &mdash; أكثر متانة، ويتعامل مع الرطوبة والأشعة فوق البنفسجية بشكل أفضل</h2>
          <p>PETG يمثل خطوة أعلى في المتانة ومقاومة الحرارة مقارنة بـ PLA، مع مقاومة أفضل للطقس والرطوبة، على حساب كونه أصعب قليلاً في الطباعة (تسييل خيوط أكثر إذا لم تكن الإعدادات مضبوطة). إنه خيار جيد للقطع الوظيفية &mdash; حوامل، تركيبات خارجية، حاويات.</p>

          <h2>ABS والمواد الهندسية &mdash; عندما تحتاج مقاومة حرارة حقيقية</h2>
          <p>تحتاج مواد ABS وASA وPC والفلمنت المقوى بألياف الكربون/الزجاج درجات حرارة أعلى للفوهة والسرير، ويُفضّل وجود حجرة مغلقة ومدفأة لتجنب التقوّس وانفصال الطبقات. هنا تظهر أهمية الجهاز: <a href="/3d/ar/product/elegoo-centauri-carbon-2/">إليجو سنتوري كاربون 2</a> تسخّن فوهتها حتى 350 درجة مئوية وسريرها حتى 110 درجة مئوية، و<a href="/3d/ar/product/flashforge-creator-5-pro/">فلاش فورج كرييتر 5 برو</a> تضيف حجرة مدفأة حتى 65 درجة مئوية بهوت إند 320 درجة مئوية خصيصاً لدعم مواد ABS وASA وPC والألياف الكربونية/الزجاجية.</p>

          <table>
            <tr><th>المادة</th><th>الأنسب لـ</th><th>تحتاج</th></tr>
            <tr><td>PLA</td><td>تماثيل، نماذج أولية، هدايا، قطع منخفضة الإجهاد</td><td>لا حاجة لغلاف</td></tr>
            <tr><td>PETG</td><td>قطع وظيفية، استخدام خارجي، تعرض للرطوبة</td><td>درجة حرارة فوهة أعلى قليلاً</td></tr>
            <tr><td>ABS / ASA / PC</td><td>قطع مقاومة للحرارة وذات متطلبات ميكانيكية</td><td>سرير مدفأ، ويُفضّل غلاف</td></tr>
          </table>

          <h2>استبدال الفوهة مهم أيضاً</h2>
          <p>المواد الكاشطة (ألياف الكربون، فلمنت الألياف الزجاجية) تُتلف فوهات النحاس بسرعة. إذا كنت تطبع مواد هندسية بانتظام، احتفظ بهوت إند احتياطي &mdash; <a href="/3d/ar/product/bambu-hotend-a1-series/">هوت إند بامبو &mdash; سلسلة A1</a> لدينا متوفر بأربعة أحجام فوهة لهذا الغرض بالتحديد.</p>

          <div class="b3d-article__cta">
            <p>تحتاج فلمنت أو فوهة احتياطية؟</p>
            <a href="/3d/ar/shop/filament/" class="btn btn-primary">تسوّق الفلمنت</a>
          </div>

          <h2>منتجات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/filament-pla-1kg/">فلمنت PLA 1 كجم</a>
            <a href="/3d/ar/product/elegoo-centauri-carbon-2/">إليجو سنتوري كاربون 2</a>
            <a href="/3d/ar/product/flashforge-creator-5-pro/">فلاش فورج كرييتر 5 برو</a>
          </div>
        ''',
    },
}

BLOG_INDEX_CARDS = [
    ('buy-3d-printer-saudi-arabia-price-guide', 'دليل الأسعار', '6 دقائق قراءة',
     'أين تشتري طابعة ثلاثية الأبعاد في السعودية (دليل أسعار 2026 بالريال)',
     'كل طابعة ثلاثية الأبعاد نوفرها، مع أسعار حالية بالريال، وما يجب فحصه قبل الشراء محلياً مقابل الاستيراد.'),
    ('best-3d-printer-for-beginners-saudi-arabia', 'دليل الشراء', '7 دقائق قراءة',
     'أفضل طابعة ثلاثية الأبعاد للمبتدئين في السعودية (دليل 2026)',
     'ما هي الطابعة المناسبة للمشتري لأول مرة؟ نقارن بامبو لاب A1 ميني وكرياليتي سباركس آي 7 من حيث السعر وسهولة الاستخدام ومحتويات الصندوق.'),
    ('pla-vs-petg-vs-abs-filament-guide', 'دليل المواد', '6 دقائق قراءة',
     'PLA مقابل PETG مقابل ABS: أي فلمنت طباعة ثلاثية الأبعاد يجب أن تستخدم؟',
     'مقارنة عملية بين PLA وPETG وABS &mdash; القوة، مقاومة الحرارة، سهولة الطباعة، وأي الطابعات تتعامل مع كل مادة بشكل أفضل.'),
    ('bambu-lab-a1-vs-a1-mini-vs-a2l', 'مقارنة', '6 دقائق قراءة',
     'بامبو لاب A1 مقابل A1 ميني مقابل A2L: أيهما يجب أن تشتري؟',
     'مقارنة حجم الطباعة والسعر وخيارات الباقات بين الطرازات الثلاثة لمساعدتك على الاختيار الصحيح.'),
    ('multi-color-3d-printing-explained', 'كيف يعمل', '6 دقائق قراءة',
     'شرح الطباعة ثلاثية الأبعاد متعددة الألوان: AMS مقابل CANVAS مقابل SnapSwap',
     'كيف تعمل أنظمة AMS من بامبو لاب، وCANVAS من إليجو، وSnapSwap من سنابميكر، وأي نهج يناسبك.'),
    ('3d-printer-maintenance-guide', 'الصيانة', '5 دقائق قراءة',
     'دليل صيانة الطابعة ثلاثية الأبعاد: حافظ على استمرار عمل طابعتك',
     'أكثر القطع عرضة للتلف &mdash; الهوت إند، والإكسترودر، وذراع قاطع الفلمنت &mdash; ومتى يجب استبدالها.'),
]


def build_post(slug, data):
    src = os.path.join(BLOG_ROOT, slug, 'index.html')
    with open(src, encoding='utf-8') as f:
        html = f.read()

    en_url = SITE + '/3d/blog/' + slug + '/'
    ar_url = SITE + '/3d/ar/blog/' + slug + '/'

    m = re.search(r'"name": "([^"]*)", "item": "https://www\.blackarrowksa\.com/3d/blog/' + re.escape(slug) + '/"', html)
    en_headline = m.group(1) if m else None

    html = html.replace('<html lang="en" dir="ltr">', '<html lang="ar" dir="rtl">')
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="' + data['meta_description'] + '">', html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">',
                  '<meta property="og:title" content="' + data['headline'] + '">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">',
                  '<meta property="og:description" content="' + data['meta_description'] + '">', html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*">',
                  '<meta property="og:url" content="' + ar_url + '">', html, count=1)
    html = re.sub(r'<link rel="canonical" href="[^"]*">',
                  '<link rel="canonical" href="' + ar_url + '">'
                  + '\n  <link rel="alternate" hreflang="en" href="' + en_url + '">'
                  + '\n  <link rel="alternate" hreflang="ar" href="' + ar_url + '">'
                  + '\n  <link rel="alternate" hreflang="x-default" href="' + en_url + '">',
                  html, count=1)
    html = re.sub(r'<title>[^<]*</title>', '<title>' + data['headline'] + ' | Black Arrow 3D</title>', html, count=1)

    # BreadcrumbList + Article JSON-LD: translate name/headline/description, keep dates structural
    if en_headline:
        html = html.replace(
            '"name": "' + en_headline + '", "item": "https://www.blackarrowksa.com/3d/blog/' + slug + '/" }',
            '"name": "' + data['headline'] + '", "item": "' + ar_url + '" }'
        )
    html = re.sub(r'("headline": ")[^"]*(")', r'\1' + data['headline'] + r'\2', html, count=1)
    html = re.sub(r'("description": ")[^"]*(",\s*\n\s*"image")', r'\1' + data['meta_description'] + r'\2', html, count=1)
    html = html.replace(
        '"mainEntityOfPage": { "@type": "WebPage", "@id": "https://www.blackarrowksa.com/3d/blog/' + slug + '/" }',
        '"mainEntityOfPage": { "@type": "WebPage", "@id": "' + ar_url + '" }'
    )
    html = html.replace(
        '{ "@type": "ListItem", "position": 3, "name": "Blog", "item": "https://www.blackarrowksa.com/3d/blog/" },',
        '{ "@type": "ListItem", "position": 3, "name": "المدونة", "item": "' + SITE + '/3d/ar/blog/" },'
    )

    # Breadcrumb nav (not data-i18n, hand-built per page)
    old_crumb = ('<a href="/3d/">Black Arrow 3D</a>\n          <span>&rsaquo;</span>\n          <a href="/3d/blog/">Blog</a>\n'
                 '          <span>&rsaquo;</span>')
    new_crumb = ('<a href="/3d/ar/">Black Arrow 3D</a>\n          <span>&rsaquo;</span>\n          <a href="/3d/ar/blog/">'
                 'المدونة</a>\n          <span>&rsaquo;</span>')
    html = html.replace(old_crumb, new_crumb)
    html = re.sub(r'<span>[^<]*</span>\n        </nav>\n\n        <article',
                  '<span>' + data['headline'] + '</span>\n        </nav>\n\n        <article', html, count=1)

    # Article body
    html = re.sub(
        r'<div class="b3d-article__meta">[^<]*</div>\s*\n\s*<h1>[^<]*</h1>\s*\n\s*<p class="b3d-article__lead">[^<]*</p>',
        '<div class="b3d-article__meta">' + data['meta_line'] + '</div>\n          <h1>' + data['headline']
        + '</h1>\n          <p class="b3d-article__lead">' + data['lead'] + '</p>',
        html, count=1
    )
    html = re.sub(
        r'(<p class="b3d-article__lead">.*?</p>\n)(.*?)(\n\s*</article>)',
        lambda m: m.group(1) + data['body'] + m.group(3),
        html, count=1, flags=re.DOTALL
    )

    html = translate_static_chrome(html, 'ar')
    html = localize_ar_hrefs(html, 'ar')
    html = lang_toggle_link(html, 'ar', '/3d/blog/' + slug + '/')

    write(os.path.join(AR_BLOG_ROOT, slug, 'index.html'), html)


def build_index():
    src = os.path.join(BLOG_ROOT, 'index.html')
    with open(src, encoding='utf-8') as f:
        html = f.read()

    html = html.replace('<html lang="en" dir="ltr">', '<html lang="ar" dir="rtl">')
    meta_desc = 'أدلة شراء ومقارنات ودروس صيانة للطابعات ثلاثية الأبعاد والفلمنت والإكسسوارات — مكتوبة من كتالوج Black Arrow 3D.'
    og_title = 'أدلة ودروس الطباعة ثلاثية الأبعاد | Black Arrow 3D'
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="' + meta_desc + '">', html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">',
                  '<meta property="og:title" content="' + og_title + '">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">',
                  '<meta property="og:description" content="' + meta_desc + '">', html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*">',
                  '<meta property="og:url" content="' + SITE + '/3d/ar/blog/">', html, count=1)
    html = re.sub(r'<link rel="canonical" href="[^"]*">',
                  '<link rel="canonical" href="' + SITE + '/3d/ar/blog/">'
                  + '\n  <link rel="alternate" hreflang="en" href="' + SITE + '/3d/blog/">'
                  + '\n  <link rel="alternate" hreflang="ar" href="' + SITE + '/3d/ar/blog/">'
                  + '\n  <link rel="alternate" hreflang="x-default" href="' + SITE + '/3d/blog/">',
                  html, count=1)
    html = re.sub(r'<title>[^<]*</title>', '<title>' + og_title + '</title>', html, count=1)
    html = html.replace(
        '{ "@type": "ListItem", "position": 3, "name": "Blog", "item": "https://www.blackarrowksa.com/3d/blog/" }',
        '{ "@type": "ListItem", "position": 3, "name": "المدونة", "item": "' + SITE + '/3d/ar/blog/" }'
    )
    html = html.replace('"name": "Black Arrow 3D Blog",', '"name": "مدونة Black Arrow 3D",')
    html = html.replace('"url": "https://www.blackarrowksa.com/3d/blog/",', '"url": "' + SITE + '/3d/ar/blog/",')
    html = html.replace(
        '"description": "3D printing buyer\'s guides, comparisons and maintenance tutorials from Black Arrow 3D."',
        '"description": "أدلة شراء ومقارنات ودروس صيانة للطباعة ثلاثية الأبعاد من Black Arrow 3D."'
    )

    html = html.replace(
        '<a href="/3d/">Black Arrow 3D</a>\n          <span>&rsaquo;</span>\n          <span>Blog</span>',
        '<a href="/3d/ar/">Black Arrow 3D</a>\n          <span>&rsaquo;</span>\n          <span>المدونة</span>'
    )
    html = html.replace(
        '<h1 style="color:#fff;font-size:2rem;margin-bottom:6px;">3D Printing Guides &amp; Tutorials</h1>',
        '<h1 style="color:#fff;font-size:2rem;margin-bottom:6px;">أدلة ودروس الطباعة ثلاثية الأبعاد</h1>'
    )
    html = html.replace(
        '<p style="color:rgba(255,255,255,.7);max-width:640px;">Buyer\'s guides, comparisons and maintenance tips for 3D printers, filament and accessories &mdash; written from our own catalog.</p>',
        '<p style="color:rgba(255,255,255,.7);max-width:640px;">أدلة شراء ومقارنات ونصائح صيانة للطابعات والفلمنت والإكسسوارات &mdash; مكتوبة من كتالوجنا الخاص.</p>'
    )

    cards_html = ''
    for slug, meta, read, title, excerpt in BLOG_INDEX_CARDS:
        cards_html += (
            '          <article class="b3d-blog-card">\n'
            '            <a class="b3d-card__stretched-link" href="/3d/ar/blog/' + slug + '/" aria-label="' + title + '"></a>\n'
            '            <span class="b3d-blog-card__meta">' + meta + ' &middot; ' + read + '</span>\n'
            '            <h2 class="b3d-blog-card__title">' + title + '</h2>\n'
            '            <span class="b3d-blog-card__excerpt">' + excerpt + '</span>\n'
            '            <span class="b3d-blog-card__read">اقرأ المقال &rarr;</span>\n'
            '          </article>\n'
        )
    html = re.sub(r'(<div class="b3d-blog-grid">\n)(.*?)(\n\s*</div>\n\s*</div>\n\s*</section>)',
                  lambda m: m.group(1) + cards_html + m.group(3), html, count=1, flags=re.DOTALL)

    html = translate_static_chrome(html, 'ar')
    html = localize_ar_hrefs(html, 'ar')
    html = lang_toggle_link(html, 'ar', '/3d/blog/')

    write(os.path.join(AR_BLOG_ROOT, 'index.html'), html)


def main():
    for slug, data in POSTS.items():
        build_post(slug, data)
    print('generated', len(POSTS), 'AR blog posts')
    build_index()
    print('generated AR blog index')


if __name__ == '__main__':
    main()
