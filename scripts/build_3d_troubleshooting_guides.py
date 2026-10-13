#!/usr/bin/env python3
"""Builds the 3D printing troubleshooting and how-to guides (EN + AR) for the Black Arrow 3D
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
    {
        'slug': 'bambu-lab-a1-mini-setup-guide',
        'en': {
            'headline': 'Bambu Lab A1 and A1 mini Setup Guide: Your First Day',
            'title': 'Bambu Lab A1 / A1 mini Setup Guide | Black Arrow 3D',
            'desc': 'Set up a Bambu Lab A1 or A1 mini step by step: unboxing, calibration, Wi-Fi and the Bambu Handy app, loading filament and your first print.',
            'meta_line': 'Getting Started &middot; October 13, 2026 &middot; 6 min read',
            'lead': 'Just got your A1 or A1 mini? Follow these steps in order and you will have your first print running in under an hour.',
            'card': ('Getting Started', '6 min read', 'From unboxing to your first print: calibration, Wi-Fi, the Bambu Handy app and loading filament.'),
            'body': '''
          <h2>1. Pick a good spot</h2>
          <p>Put the printer on a sturdy, level table with space around it, because the bed moves back and forth while printing. Keep it away from AC vents, direct sun and dust. You need a normal wall socket and a Wi-Fi signal.</p>

          <h2>2. Unbox and remove the packaging</h2>
          <p>Take out all the foam, cable ties and tape, and remove any transport fixings shown in the Quick Start Guide that comes in the box. Do not skip this: a locked axis will make the calibration fail. Keep the box for a few weeks in case you need to move or return the printer.</p>

          <h2>3. Assemble and connect</h2>
          <ul>
            <li>Fit the spool holder, or the AMS lite if you have the Combo, as shown in the Quick Start Guide.</li>
            <li>Make sure the build plate sits flat and lined up on the bed.</li>
            <li>Connect the power cable and switch the printer on.</li>
          </ul>

          <h2>4. Run the first calibration</h2>
          <p>On first start the screen walks you through setup. Let the printer run its full automatic calibration (bed leveling, vibration compensation and motor checks). It is noisy and takes a while; this is normal. Do not touch the bed while it runs.</p>

          <h2>5. Connect Wi-Fi and the app</h2>
          <ul>
            <li>Install the <b>Bambu Handy</b> app on your phone and create a Bambu Lab account.</li>
            <li>Connect the printer to your Wi-Fi from the screen, then bind it to your account in the app.</li>
            <li>Install a firmware update if the printer offers one.</li>
            <li>On a computer, install <b>Bambu Studio</b> to slice your own models.</li>
          </ul>

          <h2>6. Load filament</h2>
          <p>Start with PLA or PLA+: it is the easiest material to print. Cut the filament end at an angle, feed it in, and use the load option on the screen. With an AMS lite, place up to four spools and load each one. Set the correct material type and color so the printer uses the right temperatures.</p>

          <h2>7. Your first print</h2>
          <p>Print one of the models stored on the printer, or pick a popular model on MakerWorld from the Bambu Handy app and send it to the printer. Watch the first layer: it should be flat, even and well stuck to the plate.</p>

          <h2>Tips for the first week</h2>
          <ul>
            <li>Keep the build plate clean: wash it with dish soap and water and hold it by the edges.</li>
            <li>Store filament sealed with desiccant, especially in humid cities.</li>
            <li>If something goes wrong, see our guides on stringing, clogged nozzles and first-layer adhesion.</li>
          </ul>

          <div class="b3d-article__cta">
            <p>Need filament or a spare hotend?</p>
            <a href="/3d/deals/" class="btn btn-primary">See Kits &amp; Deals</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/product/bambu-lab-a1-mini-starter-kit/">Bambu Lab A1 mini Starter Kit</a>
            <a href="/3d/blog/3d-print-bed-adhesion-first-layer/">First layer not sticking?</a>
            <a href="/3d/blog/which-filament-for-which-print/">Which filament for which print</a>
          </div>
''',
        },
        'ar': {
            'headline': 'دليل تشغيل بامبو لاب A1 وA1 mini: يومك الأول',
            'title': 'دليل تشغيل بامبو لاب A1 وA1 mini | Black Arrow 3D',
            'desc': 'شغّل طابعة بامبو لاب A1 أو A1 mini خطوة بخطوة: الفتح والمعايرة والواي فاي وتطبيق Bambu Handy وتحميل الفلمنت وأول طباعة.',
            'meta_line': 'البداية &middot; 13 أكتوبر 2026 &middot; 6 دقائق قراءة',
            'lead': 'وصلتك A1 أو A1 mini؟ اتبع هذه الخطوات بالترتيب وستبدأ أول طباعة لك في أقل من ساعة.',
            'card': ('البداية', '6 دقائق قراءة', 'من فتح الصندوق إلى أول طباعة: المعايرة والواي فاي وتطبيق Bambu Handy وتحميل الفلمنت.'),
            'body': '''
          <h2>1. اختر مكانًا مناسبًا</h2>
          <p>ضع الطابعة على طاولة ثابتة ومستوية مع مساحة حولها، لأن السرير يتحرك للأمام والخلف أثناء الطباعة. أبعدها عن فتحات المكيف وأشعة الشمس المباشرة والغبار. تحتاج مقبس كهرباء عاديًا وإشارة واي فاي.</p>

          <h2>2. افتح الصندوق وأزل التغليف</h2>
          <p>أخرج كل الفلين وروابط الأسلاك والأشرطة، وأزل أي مثبتات للنقل موضحة في دليل البدء السريع داخل الصندوق. لا تتجاوز هذه الخطوة، فالمحور المثبت سيُفشل المعايرة. احتفظ بالصندوق لبضعة أسابيع في حال احتجت لنقل الطابعة أو إرجاعها.</p>

          <h2>3. التركيب والتوصيل</h2>
          <ul>
            <li>ركّب حامل البكرة، أو وحدة AMS lite إن كانت لديك نسخة الكومبو، كما في دليل البدء السريع.</li>
            <li>تأكد أن سطح الطباعة مستوٍ ومثبت في مكانه على السرير.</li>
            <li>وصّل كابل الكهرباء وشغّل الطابعة.</li>
          </ul>

          <h2>4. شغّل المعايرة الأولى</h2>
          <p>عند التشغيل الأول ترشدك الشاشة خطوة بخطوة. اترك الطابعة تكمل المعايرة التلقائية كاملة (تسوية السرير وتعويض الاهتزاز وفحص المحركات). تصدر صوتًا وتستغرق وقتًا، وهذا طبيعي. لا تلمس السرير أثناءها.</p>

          <h2>5. اربط الواي فاي والتطبيق</h2>
          <ul>
            <li>ثبّت تطبيق <b>Bambu Handy</b> على جوالك وأنشئ حساب Bambu Lab.</li>
            <li>اربط الطابعة بالواي فاي من الشاشة، ثم اربطها بحسابك من التطبيق.</li>
            <li>ثبّت تحديث البرنامج الثابت إن ظهر لك.</li>
            <li>على الكمبيوتر ثبّت برنامج <b>Bambu Studio</b> لتجهيز مجسماتك الخاصة.</li>
          </ul>

          <h2>6. حمّل الفلمنت</h2>
          <p>ابدأ بـ PLA أو PLA+ لأنه أسهل خامة للطباعة. اقطع طرف الفلمنت بشكل مائل وأدخله ثم استخدم خيار التحميل من الشاشة. مع AMS lite ضع حتى أربع بكرات وحمّل كل واحدة. اختر نوع الخامة واللون الصحيحين لتستخدم الطابعة الحرارة المناسبة.</p>

          <h2>7. أول طباعة</h2>
          <p>اطبع أحد المجسمات المحفوظة في الطابعة، أو اختر مجسمًا مشهورًا من MakerWorld عبر تطبيق Bambu Handy وأرسله للطابعة. راقب الطبقة الأولى: يجب أن تكون مستوية ومتساوية وملتصقة جيدًا بالسطح.</p>

          <h2>نصائح للأسبوع الأول</h2>
          <ul>
            <li>حافظ على نظافة سطح الطباعة: اغسله بالماء وسائل الصحون وأمسكه من الأطراف.</li>
            <li>احفظ الفلمنت في كيس محكم مع مادة مجففة، خصوصًا في المدن الرطبة.</li>
            <li>إذا واجهت مشكلة، راجع أدلتنا عن الخيوط الرفيعة وانسداد الفوهة والتصاق الطبقة الأولى.</li>
          </ul>

          <div class="b3d-article__cta">
            <p>تحتاج فلمنت أو هوت إند احتياطي؟</p>
            <a href="/3d/ar/deals/" class="btn btn-primary">شاهد الأطقم والعروض</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/bambu-lab-a1-mini-starter-kit/">طقم البداية بامبو لاب A1 mini</a>
            <a href="/3d/ar/blog/3d-print-bed-adhesion-first-layer/">الطبقة الأولى لا تلتصق؟</a>
            <a href="/3d/ar/blog/which-filament-for-which-print/">أي فلمنت لأي طباعة</a>
          </div>
''',
        },
    },
    {
        'slug': 'which-filament-for-which-print',
        'en': {
            'headline': 'Which Filament for Which Print? A Guide for Saudi Arabia',
            'title': 'Which 3D Printer Filament for Which Print? | Black Arrow 3D',
            'desc': 'PLA+, PETG, TPU or ABS/ASA? Which filament to use for gifts, phone stands, car parts, outdoor items and flexible parts, with tips for Saudi heat.',
            'meta_line': 'Materials &middot; October 13, 2026 &middot; 5 min read',
            'lead': 'The right filament depends on where the part will live. A gift on a desk, a holder in a hot car and a flexible case each need something different. Here is a quick way to choose.',
            'card': ('Materials', '5 min read', 'Gifts, car parts, outdoor items or flexible cases: which filament to use, with tips for Saudi heat.'),
            'body': '''
          <h2>Quick answer</h2>
          <ul>
            <li><b>Decor, figures, gifts, keychains, prototypes:</b> PLA or PLA+.</li>
            <li><b>Functional parts, holders, brackets, things that get warm:</b> PETG.</li>
            <li><b>Flexible parts (phone cases, bumpers, grips, seals):</b> TPU.</li>
            <li><b>Car interiors, outdoor parts in full sun:</b> ASA (or ABS), on an enclosed printer.</li>
          </ul>

          <h2>PLA and PLA+: the everyday choice</h2>
          <p>PLA is the easiest material to print, with the sharpest detail and the widest range of colors. PLA+ is a tougher, less brittle version that prints just as easily. Use it for anything that stays indoors at room temperature: figures, desk items, signs, toys and gifts.</p>
          <p><b>Watch out in Saudi summer:</b> PLA starts to soften at around 55–60&nbsp;°C. The inside of a parked car in summer gets much hotter than that, so a PLA phone holder or dashboard part can bend. Use PETG or ASA for anything that lives in a car.</p>

          <h2>PETG: tougher and more heat resistant</h2>
          <p>PETG is stronger and more flexible than PLA and handles more heat (it softens at around 75–80&nbsp;°C). It is a good choice for functional parts: hooks, brackets, organizers, plant pots and parts that get warm. It strings a little more than PLA, so dry it well (see our stringing guide).</p>

          <h2>TPU: flexible like rubber</h2>
          <p>TPU bends and springs back. Use it for phone cases, bumpers, grips, feet for furniture and seals. Print it slowly, and keep it very dry. On printers with an AMS, check whether your TPU is suitable for the AMS before loading it there.</p>

          <h2>ABS and ASA: for heat and sun</h2>
          <p>ABS and ASA handle higher temperatures than PETG, and ASA also resists UV light, so it is the best choice for outdoor parts that sit in direct sun. Both shrink as they cool, so they need an enclosed printer and good ventilation. They are best on enclosed printers such as the Bambu Lab P2S and H2C or the Elegoo Centauri Carbon 2.</p>

          <h2>Simple rules</h2>
          <ul>
            <li>Indoors at room temperature: PLA+.</li>
            <li>Gets warm, takes force, or lives in a car: PETG at least, ASA for full sun.</li>
            <li>Needs to bend: TPU.</li>
            <li>Not sure? Ask us on WhatsApp what you want to print and where it will be used.</li>
          </ul>

          <div class="b3d-article__cta">
            <p>Stock up with a multi-pack</p>
            <a href="/3d/deals/" class="btn btn-primary">See Filament Deals</a>
          </div>

          <h2>Related</h2>
          <div class="b3d-article__related">
            <a href="/3d/product/filament-pla-1kg/">PLA+ Filament 1kg</a>
            <a href="/3d/product/kingroon-petg-basic-filament/">KINGROON PETG Basic</a>
            <a href="/3d/blog/pla-vs-petg-vs-abs-filament-guide/">PLA vs PETG vs ABS in detail</a>
          </div>
''',
        },
        'ar': {
            'headline': 'أي فلمنت لأي طباعة؟ دليل مناسب لأجواء السعودية',
            'title': 'أي فلمنت تختار لكل طباعة؟ | Black Arrow 3D',
            'desc': 'PLA+ أم PETG أم TPU أم ABS/ASA؟ أي فلمنت تستخدم للهدايا وحوامل الجوال وقطع السيارة والقطع الخارجية والمرنة، مع نصائح لحرارة السعودية.',
            'meta_line': 'الخامات &middot; 13 أكتوبر 2026 &middot; 5 دقائق قراءة',
            'lead': 'الفلمنت المناسب يعتمد على المكان الذي ستعيش فيه القطعة. هدية على مكتب، وحامل في سيارة حارة، وغطاء مرن، كل منها يحتاج خامة مختلفة. إليك طريقة سريعة للاختيار.',
            'card': ('الخامات', '5 دقائق قراءة', 'هدايا أو قطع سيارة أو قطع خارجية أو أغطية مرنة: أي فلمنت تستخدم، مع نصائح لحرارة السعودية.'),
            'body': '''
          <h2>الإجابة السريعة</h2>
          <ul>
            <li><b>الديكور والمجسمات والهدايا والميداليات والنماذج الأولية:</b> PLA أو PLA+.</li>
            <li><b>القطع الوظيفية والحوامل والمثبتات والأشياء التي تسخن:</b> PETG.</li>
            <li><b>القطع المرنة (أغطية الجوال والمصدات والمقابض والحشوات):</b> TPU.</li>
            <li><b>داخل السيارة والقطع الخارجية تحت الشمس:</b> ASA (أو ABS) على طابعة مغلقة.</li>
          </ul>

          <h2>PLA وPLA+: الخيار اليومي</h2>
          <p>‏PLA أسهل خامة للطباعة، وأدقها تفاصيل، وألوانه الأكثر تنوعًا. أما PLA+ فنسخة أقوى وأقل هشاشة وبنفس سهولة الطباعة. استخدمه لكل ما يبقى داخل المنزل بحرارة الغرفة: المجسمات وقطع المكتب واللوحات والألعاب والهدايا.</p>
          <p><b>انتبه في صيف السعودية:</b> يبدأ PLA باللين عند حوالي 55–60 °م، وداخل السيارة المتوقفة صيفًا أحر من ذلك بكثير، فقد ينحني حامل الجوال أو قطعة لوحة القيادة المطبوعة بـ PLA. استخدم PETG أو ASA لأي قطعة تبقى في السيارة.</p>

          <h2>PETG: أقوى ويتحمل حرارة أعلى</h2>
          <p>‏PETG أقوى وأكثر مرونة من PLA ويتحمل حرارة أعلى (يلين عند حوالي 75–80 °م). خيار جيد للقطع الوظيفية: العلاقات والمثبتات والمنظمات وأحواض النباتات والقطع التي تسخن. يصنع خيوطًا رفيعة أكثر قليلًا من PLA، فجففه جيدًا (راجع دليل الخيوط الرفيعة).</p>

          <h2>TPU: مرن مثل المطاط</h2>
          <p>‏TPU ينثني ويعود لشكله. استخدمه لأغطية الجوال والمصدات والمقابض وأرجل الأثاث والحشوات. اطبعه ببطء واحفظه جافًا جدًا. في الطابعات المزودة بوحدة AMS، تأكد أن نوع TPU لديك مناسب للتحميل فيها قبل استخدامها.</p>

          <h2>ABS وASA: للحرارة والشمس</h2>
          <p>يتحمل ABS وASA حرارة أعلى من PETG، ويقاوم ASA الأشعة فوق البنفسجية أيضًا، فهو الأفضل للقطع الخارجية تحت الشمس المباشرة. كلاهما ينكمش عند التبريد، لذلك يحتاجان طابعة مغلقة وتهوية جيدة، والأنسب لهما الطابعات المغلقة مثل Bambu Lab P2S وH2C أو Elegoo Centauri Carbon 2.</p>

          <h2>قواعد بسيطة</h2>
          <ul>
            <li>داخل المنزل بحرارة الغرفة: PLA+.</li>
            <li>تسخن أو تتحمل قوة أو تبقى في السيارة: PETG على الأقل، وASA للشمس المباشرة.</li>
            <li>تحتاج أن تنثني: TPU.</li>
            <li>لست متأكدًا؟ أخبرنا عبر واتساب ماذا تريد أن تطبع وأين ستستخدمه.</li>
          </ul>

          <div class="b3d-article__cta">
            <p>وفّر مع باقات الفلمنت</p>
            <a href="/3d/ar/deals/" class="btn btn-primary">شاهد عروض الفلمنت</a>
          </div>

          <h2>ذات صلة</h2>
          <div class="b3d-article__related">
            <a href="/3d/ar/product/filament-pla-1kg/">فلمنت PLA+ 1 كجم</a>
            <a href="/3d/ar/product/kingroon-petg-basic-filament/">فلمنت KINGROON PETG Basic</a>
            <a href="/3d/ar/blog/pla-vs-petg-vs-abs-filament-guide/">مقارنة PLA وPETG وABS بالتفصيل</a>
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
