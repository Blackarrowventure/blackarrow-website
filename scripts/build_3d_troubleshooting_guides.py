#!/usr/bin/env python3
"""Builds the 3D printing troubleshooting guides (EN + AR) for the Black Arrow 3D
blog and lists them on both blog index pages.

The English pages reuse the layout of an existing article
(3d/blog/3d-printer-maintenance-guide/) and the Arabic pages go through the
same build_post() as every other Arabic article (scripts/generate_3d_blog_ar.py).
Safe to re-run: pages are rewritten and index cards are only added once.

Usage: python scripts/build_3d_troubleshooting_guides.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_3d_blog_ar as ar_blog  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, '3d', 'blog')
AR_BLOG = os.path.join(ROOT, '3d', 'ar', 'blog')
SITE = 'https://www.blackarrowksa.com'
TEMPLATE_SLUG = '3d-printer-maintenance-guide'
DATE = '2026-10-13'

GUIDES = [
    {
        'slug': '3d-print-stringing-fix',
        'en': {
            'headline': 'How to Fix Stringing in 3D Prints',
            'title': 'How to Fix Stringing in 3D Prints | Black Arrow 3D',
            'desc': 'Thin strings and “hairs” between the parts of a 3D print: why stringing happens and how to fix it with dry filament, lower temperature and the right retraction.',
            'meta_line': 'Troubleshooting &middot; October 13, 2026 &middot; 5 min read',
            'lead': 'Fine, cobweb-like strings between the parts of a print are one of the most common 3D printing problems. The good news: it is almost always fixed by three things, in this order.',
            'card': ('Troubleshooting', '5 min read', 'Thin strings between the parts of a print: the three fixes that solve it, in the order to try them.'),
            'body': '''
          <h2>What stringing looks like</h2>
          <p>When the nozzle travels across an open gap, a little molten plastic oozes out and stretches into a thin thread. On a finished print you see fine "hairs" or webs between towers, letters or the spikes of a model. It does not weaken the part, but it ruins the look and takes time to clean off.</p>

          <h2>1. Dry your filament first</h2>
          <p>Wet filament is the number one cause, especially in humid cities like Jeddah and Dammam. Filament absorbs moisture from the air, the water turns to steam in the hot end, and the nozzle keeps oozing. Signs of wet filament: popping or crackling sounds while printing, a rough or bubbly surface, and stringing that gets worse over a few days.</p>
          <ul>
            <li>PLA / PLA+: dry at 45–55&nbsp;°C for 4–6 hours.</li>
            <li>PETG: dry at 60–65&nbsp;°C for 6–8 hours.</li>
            <li>TPU: dry at 50–55&nbsp;°C for 6–8 hours.</li>
          </ul>
          <p>A filament dryer is best; a food dehydrator also works. After drying, store spools in a sealed bag or box with desiccant packs.</p>

          <h2>2. Lower the nozzle temperature</h2>
          <p>The hotter the plastic, the runnier it is and the more it oozes. Lower the nozzle temperature in steps of 5&nbsp;°C and print a small test after each change. Stop when stringing is gone but layers still bond well. If the print becomes weak or layers split, go back up one step. A "temperature tower" test print shows the best setting for a spool in one go.</p>

          <h2>3. Check retraction</h2>
          <p>Retraction pulls the filament back a little before each travel move so the nozzle does not drip. Most slicer profiles for popular printers already have good values, so only change retraction after drying and lowering the temperature.</p>
          <ul>
            <li>Direct-drive printers (most modern printers, including the Bambu Lab A-series): about 0.5–2&nbsp;mm.</li>
            <li>Bowden printers (long tube between extruder and hot end): about 4–6&nbsp;mm.</li>
            <li>Change it in small steps (0.2–0.5&nbsp;mm). Too much retraction can cause clogs and gaps.</li>
          </ul>

          <h2>Other settings that help</h2>
          <ul>
            <li>Turn on "avoid crossing walls" or "combing" so the nozzle travels over the part instead of across open air.</li>
            <li>Raise the travel speed so the nozzle spends less time over gaps.</li>
            <li>Turn on "wipe" if your slicer has it.</li>
          </ul>

          <h2>PETG and TPU string more</h2>
          <p>Some stringing is normal with PETG and TPU even when everything is set up well. Drying is even more important for these materials. A quick pass with a heat gun or hair dryer removes the last fine strings in seconds.</p>

          <div class="b3d-article__cta">
            <p>Start with fresh, dry filament</p>
            <a href="/3d/shop/filament/" class="btn btn-primary">Shop Filament</a>
          </div>

          <h2>Related products</h2>
          <div class="b3d-article__related">
            <a href="/3d/product/filament-pla-1kg/">PLA+ Filament 1kg</a>
            <a href="/3d/product/kingroon-petg-basic-filament/">KINGROON PETG Basic Filament</a>
            <a href="/3d/blog/pla-vs-petg-vs-abs-filament-guide/">PLA vs PETG vs ABS guide</a>
          </div>
''',
        },
        'ar': {
            'headline': 'كيف تتخلص من الخيوط الرفيعة (Stringing) في الطباعة ثلاثية الأبعاد',
            'title': 'حل مشكلة الخيوط الرفيعة في الطباعة ثلاثية الأبعاد',
            'desc': 'خيوط رفيعة بين أجزاء المطبوعة ثلاثية الأبعاد: لماذا تظهر وكيف تحلها بفلمنت جاف وحرارة أقل وإعدادات سحب صحيحة.',
            'meta_line': 'حل المشاكل &middot; 13 أكتوبر 2026 &middot; 5 دقائق قراءة',
            'lead': 'الخيوط الرفيعة التي تشبه بيت العنكبوت بين أجزاء المطبوعة من أكثر مشاكل الطباعة ثلاثية الأبعاد شيوعًا. والخبر الجيد أنها تُحل غالبًا بثلاث خطوات، بهذا الترتيب.',
            'card': ('حل المشاكل', '5 دقائق قراءة', 'خيوط رفيعة بين أجزاء المطبوعة: ثلاث خطوات تحل المشكلة، وبأي ترتيب تجربها.'),
            'body': '''
          <h2>كيف تبدو المشكلة</h2>
          <p>عندما تتحرك الفوهة فوق فراغ، يتسرب قليل من البلاستيك المنصهر ويتمدد على شكل خيط رفيع. في المطبوعة النهائية تظهر شعيرات أو شبكة رفيعة بين الأبراج أو الحروف أو أطراف المجسم. لا تُضعف القطعة، لكنها تفسد شكلها وتحتاج وقتًا لتنظيفها.</p>

          <h2>1. جفف الفلمنت أولًا</h2>
          <p>الفلمنت الرطب هو السبب الأول، خصوصًا في المدن الرطبة مثل جدة والدمام. يمتص الفلمنت الرطوبة من الهواء، فيتحول الماء إلى بخار داخل الهوت إند وتستمر الفوهة في التسريب. علامات الفلمنت الرطب: صوت فرقعة أثناء الطباعة، وسطح خشن أو فيه فقاعات، وخيوط تزيد مع الأيام.</p>
          <ul>
            <li>PLA / PLA+: جفّفه على 45–55 °م لمدة 4–6 ساعات.</li>
            <li>PETG: جفّفه على 60–65 °م لمدة 6–8 ساعات.</li>
            <li>TPU: جفّفه على 50–55 °م لمدة 6–8 ساعات.</li>
          </ul>
          <p>الأفضل استخدام مجفف فلمنت، ويمكن أيضًا استخدام مجفف الطعام. بعد التجفيف احفظ البكرات في كيس أو صندوق محكم مع أكياس مادة مجففة.</p>

          <h2>2. اخفض حرارة الفوهة</h2>
          <p>كلما زادت حرارة البلاستيك زادت سيولته وتسريبه. اخفض حرارة الفوهة بمقدار 5 °م في كل مرة واطبع اختبارًا صغيرًا بعد كل تغيير. توقف عندما تختفي الخيوط مع بقاء التصاق الطبقات قويًا. إذا ضعفت القطعة أو انفصلت الطبقات، ارجع درجة واحدة. اختبار "برج الحرارة" يُظهر أفضل إعداد للبكرة في طباعة واحدة.</p>

          <h2>3. راجع إعدادات السحب (Retraction)</h2>
          <p>السحب يعيد الفلمنت قليلًا للخلف قبل كل حركة تنقل حتى لا تقطر الفوهة. معظم ملفات الإعداد الجاهزة للطابعات المشهورة فيها قيم جيدة، لذلك لا تغيّر السحب إلا بعد التجفيف وخفض الحرارة.</p>
          <ul>
            <li>طابعات الدفع المباشر (معظم الطابعات الحديثة ومنها سلسلة A من Bambu Lab): حوالي 0.5–2 مم.</li>
            <li>طابعات Bowden (أنبوب طويل بين الإكسترودر والهوت إند): حوالي 4–6 مم.</li>
            <li>غيّر القيمة بخطوات صغيرة (0.2–0.5 مم). السحب الزائد قد يسبب انسدادًا وفراغات.</li>
          </ul>

          <h2>إعدادات أخرى تساعد</h2>
          <ul>
            <li>فعّل خيار "تجنب عبور الجدران" أو "Combing" لتتحرك الفوهة فوق القطعة بدلًا من الهواء.</li>
            <li>ارفع سرعة التنقل لتقضي الفوهة وقتًا أقل فوق الفراغات.</li>
            <li>فعّل خيار "Wipe" إن كان متوفرًا في برنامج التقطيع.</li>
          </ul>

          <h2>PETG وTPU يصنعان خيوطًا أكثر</h2>
          <p>بعض الخيوط أمر طبيعي مع PETG وTPU حتى مع الإعداد الجيد، والتجفيف أهم مع هذه الخامات. تمرير سريع بمسدس حرارة أو مجفف شعر يزيل آخر الخيوط في ثوانٍ.</p>

          <div class="b3d-article__cta">
            <p>ابدأ بفلمنت جديد وجاف</p>
            <a href="/3d/ar/shop/filament/" class="btn btn-primary">تسوّق الفلمنت</a>
          </div>

          <h2>منتجات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/filament-pla-1kg/">فلمنت PLA+ 1 كجم</a>
            <a href="/3d/ar/product/kingroon-petg-basic-filament/">فلمنت KINGROON PETG Basic</a>
            <a href="/3d/ar/blog/pla-vs-petg-vs-abs-filament-guide/">مقارنة PLA وPETG وABS</a>
          </div>
''',
        },
    },
    {
        'slug': 'clogged-3d-printer-nozzle-fix',
        'en': {
            'headline': 'Clogged 3D Printer Nozzle: How to Clear It and Stop It Happening',
            'title': 'How to Fix a Clogged 3D Printer Nozzle | Black Arrow 3D',
            'desc': 'No filament coming out, clicking extruder or thin layers? How to clear a clogged 3D printer nozzle with a cold pull, when to replace the hot end, and how to prevent clogs.',
            'meta_line': 'Troubleshooting &middot; October 13, 2026 &middot; 6 min read',
            'lead': 'A clogged nozzle is the problem that stops a print completely. Here is how to tell if you have one, how to clear it safely, and when it is quicker to swap the hot end.',
            'card': ('Troubleshooting', '6 min read', 'No filament coming out or a clicking extruder? How to clear a clog safely, and how to stop it happening again.'),
            'body': '''
          <h2>Signs of a clog</h2>
          <ul>
            <li>Little or no filament comes out, even when you extrude by hand from the printer menu.</li>
            <li>The extruder makes a clicking or knocking sound as it skips.</li>
            <li>Layers come out thin, weak or with gaps (a partial clog).</li>
            <li>Filament comes out curling sideways instead of straight down.</li>
          </ul>

          <h2>Common causes</h2>
          <ul>
            <li><b>Wet or dusty filament</b>, which leaves residue in the nozzle.</li>
            <li><b>Heat creep</b>: heat travels up above the melt zone and softens filament where it should stay solid. It happens more in a hot room or with the cooling fan blocked.</li>
            <li><b>Changing materials</b>: switching from a hotter material (PETG, ABS) to a cooler one (PLA) without purging can leave unmelted plastic behind.</li>
            <li><b>Nozzle too close to the bed</b> on the first layer, which blocks the flow and pushes back into the nozzle.</li>
            <li><b>Too much retraction</b>, which pulls soft filament up into the cold zone.</li>
          </ul>

          <h2>Fix 1: Heat and push</h2>
          <p>Heat the nozzle to the print temperature of the material that was loaded, then 10–15&nbsp;°C higher. Unload the filament, cut a clean straight end, and load it again while pushing gently. Often the extra heat and pressure is enough to push a small blockage through.</p>

          <h2>Fix 2: The cold pull</h2>
          <p>A cold pull removes the debris stuck inside the nozzle. It works best with PLA or nylon.</p>
          <ol>
            <li>Heat the nozzle to about 200–220&nbsp;°C and push filament through by hand until it flows.</li>
            <li>Let the nozzle cool to about 90–110&nbsp;°C for PLA while you keep light pressure on the filament.</li>
            <li>Pull the filament out firmly in one quick motion. The tip should come out shaped like the inside of the nozzle, with dark debris on it.</li>
            <li>Repeat until the tip comes out clean.</li>
          </ol>
          <p>The exact temperatures depend on your printer and filament, and some printers have a guided cold-pull or "clean nozzle" routine in the menu. On printers with a built-in filament path, follow the maker's steps for removing filament by hand.</p>

          <h2>Fix 3: Clean or replace the hot end</h2>
          <p>Avoid pushing hard with needles or drills into a hot nozzle: it is easy to damage the bore or burn yourself. If cold pulls do not clear it, replacing the nozzle or hot end is faster and safer. On the Bambu Lab A1 and A1 mini the hot end is a quick-swap part that takes a few minutes to change with no tools beyond what comes with the printer.</p>

          <h2>How to prevent clogs</h2>
          <ul>
            <li>Keep filament dry and stored in sealed bags with desiccant.</li>
            <li>Purge well when changing materials: push the new filament through at the higher of the two temperatures until the color and flow are clean.</li>
            <li>Keep the hot-end cooling fan clean and never block it.</li>
            <li>Set the first-layer height correctly (see our bed adhesion guide).</li>
            <li>Replace worn nozzles. Abrasive filaments such as carbon-fiber blends wear brass nozzles quickly; use a hardened nozzle for those.</li>
          </ul>

          <div class="b3d-article__cta">
            <p>Keep a spare hot end on hand</p>
            <a href="/3d/shop/accessories/" class="btn btn-primary">Shop Spare Parts</a>
          </div>

          <h2>Related products</h2>
          <div class="b3d-article__related">
            <a href="/3d/product/bambu-hotend-a1-series/">Bambu Hotend &mdash; A1 Series</a>
            <a href="/3d/product/hotend-heating-assembly-a1-series/">Hotend Heating Assembly &mdash; A1 Series</a>
            <a href="/3d/blog/3d-printer-maintenance-guide/">3D Printer Maintenance Guide</a>
          </div>
''',
        },
        'ar': {
            'headline': 'انسداد فوهة الطابعة ثلاثية الأبعاد: كيف تفتحها وتمنع تكرارها',
            'title': 'حل انسداد فوهة الطابعة ثلاثية الأبعاد | Black Arrow 3D',
            'desc': 'الفلمنت لا يخرج أو الإكسترودر يطقطق أو الطبقات رقيقة؟ كيف تفتح انسداد الفوهة بطريقة السحب البارد، ومتى تستبدل الهوت إند، وكيف تمنع الانسداد.',
            'meta_line': 'حل المشاكل &middot; 13 أكتوبر 2026 &middot; 6 دقائق قراءة',
            'lead': 'انسداد الفوهة هو المشكلة التي توقف الطباعة تمامًا. إليك كيف تعرف أن الفوهة مسدودة، وكيف تفتحها بأمان، ومتى يكون تبديل الهوت إند أسرع.',
            'card': ('حل المشاكل', '6 دقائق قراءة', 'الفلمنت لا يخرج أو الإكسترودر يطقطق؟ كيف تفتح الانسداد بأمان وتمنع تكراره.'),
            'body': '''
          <h2>علامات الانسداد</h2>
          <ul>
            <li>يخرج القليل من الفلمنت أو لا يخرج شيء، حتى عند إخراجه يدويًا من قائمة الطابعة.</li>
            <li>يصدر الإكسترودر صوت طقطقة أو ضرب أثناء تخطيه.</li>
            <li>تخرج الطبقات رقيقة أو ضعيفة أو فيها فراغات (انسداد جزئي).</li>
            <li>يخرج الفلمنت ملتويًا للجانب بدلًا من النزول بشكل مستقيم.</li>
          </ul>

          <h2>الأسباب الشائعة</h2>
          <ul>
            <li><b>فلمنت رطب أو عليه غبار</b>، فيترك بقايا داخل الفوهة.</li>
            <li><b>تسرب الحرارة للأعلى (Heat creep)</b>: تصعد الحرارة فوق منطقة الصهر وتلين الفلمنت في مكان يجب أن يبقى صلبًا. يحدث أكثر في الغرف الحارة أو عند انسداد مروحة التبريد.</li>
            <li><b>تبديل الخامات</b>: الانتقال من خامة أعلى حرارة (PETG أو ABS) إلى خامة أقل حرارة (PLA) دون تنظيف قد يترك بلاستيكًا غير منصهر.</li>
            <li><b>الفوهة قريبة جدًا من السرير</b> في الطبقة الأولى، فتسد مخرج البلاستيك ويرتد للداخل.</li>
            <li><b>سحب زائد</b> يرفع الفلمنت اللين إلى المنطقة الباردة.</li>
          </ul>

          <h2>الحل 1: التسخين والدفع</h2>
          <p>سخّن الفوهة إلى حرارة طباعة الخامة المحملة، ثم أعلى منها بـ 10–15 °م. أخرج الفلمنت، واقطع طرفه قطعًا نظيفًا مستقيمًا، ثم أعد تحميله مع دفع خفيف. غالبًا تكفي الحرارة الإضافية والضغط لدفع الانسداد الصغير.</p>

          <h2>الحل 2: السحب البارد (Cold pull)</h2>
          <p>السحب البارد يزيل البقايا العالقة داخل الفوهة، ويعمل أفضل مع PLA أو النايلون.</p>
          <ol>
            <li>سخّن الفوهة إلى حوالي 200–220 °م وادفع الفلمنت باليد حتى يتدفق.</li>
            <li>اترك الفوهة تبرد إلى حوالي 90–110 °م مع PLA وأنت تضغط على الفلمنت ضغطًا خفيفًا.</li>
            <li>اسحب الفلمنت بقوة وبحركة واحدة سريعة. يجب أن يخرج طرفه بشكل باطن الفوهة وعليه بقايا داكنة.</li>
            <li>كرر العملية حتى يخرج الطرف نظيفًا.</li>
          </ol>
          <p>تختلف درجات الحرارة الدقيقة حسب الطابعة والفلمنت، وبعض الطابعات فيها خطوات مساعدة للسحب البارد أو "تنظيف الفوهة" في القائمة. في الطابعات ذات مسار الفلمنت المدمج اتبع خطوات الشركة لإخراج الفلمنت يدويًا.</p>

          <h2>الحل 3: نظّف الهوت إند أو استبدله</h2>
          <p>تجنب الدفع بقوة بالإبر أو المثاقب داخل فوهة ساخنة، فمن السهل إتلاف الفتحة أو التعرض للحرق. إذا لم يفتح السحب البارد الانسداد، فاستبدال الفوهة أو الهوت إند أسرع وأأمن. في Bambu Lab A1 وA1 mini الهوت إند قطعة سريعة التبديل تستغرق دقائق قليلة دون أدوات غير المرفقة مع الطابعة.</p>

          <h2>كيف تمنع الانسداد</h2>
          <ul>
            <li>احفظ الفلمنت جافًا في أكياس محكمة مع مادة مجففة.</li>
            <li>نظّف جيدًا عند تبديل الخامات: ادفع الفلمنت الجديد على الحرارة الأعلى بين الخامتين حتى يصبح اللون والتدفق نظيفين.</li>
            <li>حافظ على نظافة مروحة تبريد الهوت إند ولا تسدّها أبدًا.</li>
            <li>اضبط ارتفاع الطبقة الأولى بشكل صحيح (راجع دليل التصاق الطبقة الأولى).</li>
            <li>استبدل الفوهات المتآكلة. الفلمنت الكاشط مثل المخلوط بألياف الكربون يُتلف الفوهات النحاسية بسرعة، فاستخدم فوهة مقواة معه.</li>
          </ul>

          <div class="b3d-article__cta">
            <p>احتفظ بهوت إند احتياطي</p>
            <a href="/3d/ar/shop/accessories/" class="btn btn-primary">تسوّق قطع الغيار</a>
          </div>

          <h2>منتجات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/bambu-hotend-a1-series/">هوت إند بامبو &mdash; سلسلة A1</a>
            <a href="/3d/ar/product/hotend-heating-assembly-a1-series/">مجموعة تسخين الهوت إند &mdash; سلسلة A1</a>
            <a href="/3d/ar/blog/3d-printer-maintenance-guide/">دليل صيانة الطابعة ثلاثية الأبعاد</a>
          </div>
''',
        },
    },
    {
        'slug': '3d-print-bed-adhesion-first-layer',
        'en': {
            'headline': 'First Layer Not Sticking? How to Fix 3D Print Bed Adhesion',
            'title': 'First Layer Not Sticking? Fix Bed Adhesion | Black Arrow 3D',
            'desc': 'Prints coming loose, corners lifting or spaghetti on the bed? How to fix 3D print bed adhesion: a clean plate, the right first-layer height, bed temperature and brims.',
            'meta_line': 'Troubleshooting &middot; October 13, 2026 &middot; 6 min read',
            'lead': 'Most failed prints fail in the first few minutes. If the first layer sticks well, the rest of the print usually works. Here is how to get it right every time.',
            'card': ('Troubleshooting', '6 min read', 'Prints coming loose or corners lifting? Five fixes for a first layer that sticks every time.'),
            'body': '''
          <h2>Signs of poor adhesion</h2>
          <ul>
            <li>The first lines curl up or get dragged around by the nozzle.</li>
            <li>The print comes loose halfway and turns into "spaghetti".</li>
            <li>Corners lift and the bottom of the part bends (warping).</li>
          </ul>

          <h2>1. Clean the build plate</h2>
          <p>Fingerprints and oil are the most common cause. Wash the plate with warm water and a little dish soap, rinse, and dry it with a clean paper towel. Between washes you can wipe it with isopropyl alcohol (IPA). After cleaning, hold the plate by its edges.</p>

          <h2>2. Get the first-layer height right</h2>
          <p>If the nozzle is too high, the lines are round and do not stick. If it is too close, the plastic is squashed thin, rough and see-through, and it can even block the nozzle. A good first layer is slightly flattened with lines that just touch each other.</p>
          <ul>
            <li>Run the printer's auto bed leveling or calibration before important prints, and after moving the printer.</li>
            <li>If your printer has a Z-offset setting, adjust it in small steps (0.02–0.05&nbsp;mm) while watching the first layer.</li>
          </ul>

          <h2>3. Use the right bed temperature</h2>
          <ul>
            <li>PLA / PLA+: about 55–65&nbsp;°C.</li>
            <li>PETG: about 70–80&nbsp;°C.</li>
            <li>TPU: about 40–60&nbsp;°C.</li>
            <li>ABS / ASA: about 90–100&nbsp;°C, ideally in an enclosed printer.</li>
          </ul>
          <p>Check the recommended range on your filament spool, and check your printer's maximum bed temperature.</p>

          <h2>4. Slow down the first layer and add a brim</h2>
          <p>A slower first layer (around 20–50&nbsp;mm/s) gives the plastic time to bond. For small parts, tall thin parts or parts with sharp corners, add a brim in the slicer: a thin skirt of extra lines around the base that you peel off afterwards.</p>

          <h2>5. Watch out for drafts and air conditioning</h2>
          <p>In Saudi homes and offices the printer is often near an AC vent. Cold air on the print cools it unevenly, and that is a common reason corners lift. Move the printer out of the airflow, or use a cover or enclosure, especially for PETG, ABS and ASA.</p>

          <h2>A tip for PETG</h2>
          <p>PETG can stick too well to a smooth PEI plate and pull pieces off the surface when you remove the print. Use a textured plate for PETG, or apply a thin layer of glue stick on a smooth plate as a release layer.</p>

          <div class="b3d-article__cta">
            <p>Choosing a printer with automatic bed leveling?</p>
            <a href="/3d/shop/3d-printers/" class="btn btn-primary">Shop 3D Printers</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/blog/best-3d-printer-for-beginners-saudi-arabia/">Best 3D printer for beginners</a>
            <a href="/3d/blog/3d-print-stringing-fix/">How to fix stringing</a>
            <a href="/3d/blog/clogged-3d-printer-nozzle-fix/">Clogged nozzle fix</a>
          </div>
''',
        },
        'ar': {
            'headline': 'الطبقة الأولى لا تلتصق؟ كيف تحل مشكلة التصاق الطباعة بالسرير',
            'title': 'حل مشكلة عدم التصاق الطبقة الأولى | Black Arrow 3D',
            'desc': 'المطبوعة تنفصل أو الزوايا ترتفع أو تتحول لخيوط متشابكة؟ كيف تحل التصاق الطباعة بالسرير: سطح نظيف وارتفاع صحيح للطبقة الأولى وحرارة سرير مناسبة وحافة Brim.',
            'meta_line': 'حل المشاكل &middot; 13 أكتوبر 2026 &middot; 6 دقائق قراءة',
            'lead': 'معظم الطباعات الفاشلة تفشل في الدقائق الأولى. إذا التصقت الطبقة الأولى جيدًا، تنجح بقية الطباعة غالبًا. إليك كيف تضبطها كل مرة.',
            'card': ('حل المشاكل', '6 دقائق قراءة', 'المطبوعة تنفصل أو الزوايا ترتفع؟ خمسة حلول لطبقة أولى تلتصق كل مرة.'),
            'body': '''
          <h2>علامات ضعف الالتصاق</h2>
          <ul>
            <li>تلتف الخطوط الأولى للأعلى أو تسحبها الفوهة معها.</li>
            <li>تنفصل المطبوعة في المنتصف وتتحول إلى خيوط متشابكة ("سباغيتي").</li>
            <li>ترتفع الزوايا وينحني أسفل القطعة (Warping).</li>
          </ul>

          <h2>1. نظّف سطح الطباعة</h2>
          <p>بصمات الأصابع والزيوت هي السبب الأكثر شيوعًا. اغسل السطح بماء دافئ وقليل من سائل غسيل الصحون، ثم اشطفه وجففه بمنديل نظيف. بين الغسلات يمكنك مسحه بكحول الأيزوبروبيل (IPA). بعد التنظيف أمسك السطح من أطرافه فقط.</p>

          <h2>2. اضبط ارتفاع الطبقة الأولى</h2>
          <p>إذا كانت الفوهة مرتفعة تخرج الخطوط دائرية ولا تلتصق. وإذا كانت قريبة جدًا يُضغط البلاستيك فيصبح رقيقًا وخشنًا وشفافًا، وقد يسد الفوهة. الطبقة الأولى الجيدة مسطحة قليلًا وخطوطها متلامسة بالكاد.</p>
          <ul>
            <li>شغّل التسوية أو المعايرة التلقائية للسرير قبل الطباعات المهمة، وبعد نقل الطابعة.</li>
            <li>إذا كانت طابعتك فيها إعداد Z-offset فعدّله بخطوات صغيرة (0.02–0.05 مم) وأنت تراقب الطبقة الأولى.</li>
          </ul>

          <h2>3. استخدم حرارة السرير المناسبة</h2>
          <ul>
            <li>PLA / PLA+: حوالي 55–65 °م.</li>
            <li>PETG: حوالي 70–80 °م.</li>
            <li>TPU: حوالي 40–60 °م.</li>
            <li>ABS / ASA: حوالي 90–100 °م، ويفضل في طابعة مغلقة.</li>
          </ul>
          <p>راجع النطاق الموصى به على بكرة الفلمنت، وتأكد من أقصى حرارة يدعمها سرير طابعتك.</p>

          <h2>4. أبطئ الطبقة الأولى وأضف حافة (Brim)</h2>
          <p>الطبقة الأولى الأبطأ (حوالي 20–50 مم/ث) تعطي البلاستيك وقتًا ليلتصق. للقطع الصغيرة أو الطويلة الرفيعة أو ذات الزوايا الحادة، أضف حافة Brim في برنامج التقطيع: خطوط رفيعة إضافية حول القاعدة تنزعها بعد الطباعة.</p>

          <h2>5. انتبه لتيارات الهواء والمكيف</h2>
          <p>في المنازل والمكاتب السعودية تكون الطابعة غالبًا قريبة من فتحة المكيف. الهواء البارد على المطبوعة يبردها بشكل غير متساوٍ، وهذا سبب شائع لارتفاع الزوايا. أبعد الطابعة عن تيار الهواء أو استخدم غطاءً أو حجرة مغلقة، خصوصًا مع PETG وABS وASA.</p>

          <h2>نصيحة لخامة PETG</h2>
          <p>قد يلتصق PETG بقوة زائدة بسطح PEI الأملس وينزع أجزاء من السطح عند فك المطبوعة. استخدم سطحًا محببًا مع PETG، أو ضع طبقة رقيقة من الغراء الأصبع على السطح الأملس كطبقة فاصلة.</p>

          <div class="b3d-article__cta">
            <p>تبحث عن طابعة بتسوية تلقائية للسرير؟</p>
            <a href="/3d/ar/shop/3d-printers/" class="btn btn-primary">تسوّق الطابعات</a>
          </div>

          <h2>مقالات ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/blog/best-3d-printer-for-beginners-saudi-arabia/">أفضل طابعة للمبتدئين</a>
            <a href="/3d/ar/blog/3d-print-stringing-fix/">حل مشكلة الخيوط الرفيعة</a>
            <a href="/3d/ar/blog/clogged-3d-printer-nozzle-fix/">حل انسداد الفوهة</a>
          </div>
''',
        },
    },
]


def build_en(g):
    with open(os.path.join(BLOG, TEMPLATE_SLUG, 'index.html'), encoding='utf-8') as f:
        html = f.read()
    d, slug = g['en'], g['slug']
    url = SITE + '/3d/blog/' + slug + '/'
    old_headline = re.search(r'<h1>([^<]*)</h1>', html).group(1)
    old_desc = re.search(r'<meta name="description" content="([^"]*)">', html).group(1)
    html = html.replace(old_desc, d['desc'])
    html = re.sub(r'<title>[^<]*</title>', '<title>' + d['title'] + '</title>', html, count=1)
    html = html.replace(old_headline, d['headline'])
    html = re.sub(r'"datePublished": "[^"]*"', '"datePublished": "' + DATE + '"', html, count=1)
    html = re.sub(r'"dateModified": "[^"]*"', '"dateModified": "' + DATE + '"', html, count=1)
    html = re.sub(
        r'<div class="b3d-article__meta">[^<]*</div>\s*\n\s*<h1>[^<]*</h1>\s*\n\s*<p class="b3d-article__lead">[^<]*</p>',
        lambda m: '<div class="b3d-article__meta">' + d['meta_line'] + '</div>\n          <h1>' + d['headline']
        + '</h1>\n          <p class="b3d-article__lead">' + d['lead'] + '</p>',
        html, count=1)
    html = re.sub(r'(<p class="b3d-article__lead">.*?</p>\n)(.*?)(\n\s*</article>)',
                  lambda m: m.group(1) + d['body'] + m.group(3), html, count=1, flags=re.DOTALL)
    html = html.replace(TEMPLATE_SLUG, slug)   # canonical, hreflang, og:url, JSON-LD, language toggle
    assert url in html
    out = os.path.join(BLOG, slug)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)


def card(href, meta, read, title, excerpt, read_label):
    return ('          <article class="b3d-blog-card">\n'
            '            <a class="b3d-card__stretched-link" href="' + href + '" aria-label="' + title + '"></a>\n'
            '            <span class="b3d-blog-card__meta">' + meta + ' &middot; ' + read + '</span>\n'
            '            <h2 class="b3d-blog-card__title">' + title + '</h2>\n'
            '            <span class="b3d-blog-card__excerpt">' + excerpt + '</span>\n'
            '            <span class="b3d-blog-card__read">' + read_label + '</span>\n'
            '          </article>\n')


def add_cards(index_path, lang):
    with open(index_path, encoding='utf-8') as f:
        html = f.read()
    base = '/3d/ar/blog/' if lang == 'ar' else '/3d/blog/'
    new = ''
    for g in GUIDES:
        href = base + g['slug'] + '/'
        if 'href="' + href + '"' in html:
            continue
        meta, read, excerpt = g[lang]['card']
        new += card(href, meta, read, g[lang]['headline'], excerpt, 'اقرأ المقال &rarr;' if lang == 'ar' else 'Read article &rarr;')
    if new:
        html = html.replace('<div class="b3d-blog-grid">\n', '<div class="b3d-blog-grid">\n' + new, 1)
        with open(index_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
    return new.count('<article')


def main():
    for g in GUIDES:
        build_en(g)
        a = g['ar']
        ar_blog.SEO_TITLES[g['slug']] = a['title']
        ar_blog.build_post(g['slug'], {
            'meta_description': a['desc'], 'headline': a['headline'],
            'meta_line': a['meta_line'], 'lead': a['lead'], 'body': a['body'],
        })
    print('guides built:', len(GUIDES), 'x EN + AR')
    print('index cards added: EN', add_cards(os.path.join(BLOG, 'index.html'), 'en'),
          '| AR', add_cards(os.path.join(AR_BLOG, 'index.html'), 'ar'))


if __name__ == '__main__':
    main()
