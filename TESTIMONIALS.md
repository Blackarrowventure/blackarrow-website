# Client testimonials — how to collect them and how to publish them

Internal note. `.vercelignore`d, so it is never served publicly.

## The one rule

**Every quote on the site must be a real, named person who agreed to be
quoted.** No samples, no "representative" quotes, no composites, not even
temporarily. The buyers this site targets are hospital and government
facility managers; they phone each other. A single invented endorsement
would cost more trust than every quote on the page could ever earn.

This is also why the section ships commented out rather than filled with
placeholder text that someone might mistake for finished copy.

## Where the section lives

- Markup: `index.html`, between the client logo marquee and the WhatsApp
  banner, wrapped in an HTML comment with activation instructions inside it.
- Styles: `assets/css/styles.css`, section `13b. CLIENT TESTIMONIALS`.
- Heading, overline and subtitle are already translated
  (`testimonials_overline`, `testimonials_title`, `testimonials_subtitle`).

Three cards on desktop, one column under 768px. Attribution is pinned to the
bottom of each card, so quotes of different lengths still line their names up
across the row.

## Publishing a quote once you have it

1. In `index.html`, replace the `[BRACKETED]` text with the real words,
   name, job title and company. Delete any card you have no real quote for —
   three is plenty, and two strong ones beat five weak ones.
2. Delete the comment wrapper: the opening block above the section and the
   closing marker below it.
3. Add each quote to `assets/translations/ar.json` under the same keys
   (`testimonial_1_quote`, `testimonial_1_name`, `testimonial_1_role`, and so
   on). If the client gave the quote in Arabic, that Arabic is the original —
   put the English translation in `en.json` instead of the other way round.
4. `py scripts/build_ar.py --build`
5. `py scripts/check_links.py` — must report 0 unresolved.

## Who to ask

The names already on the logo wall, strongest first for this purpose:

| Client | Why this one matters |
|---|---|
| Dr Sulaiman Al Habib Medical Group | Best-known healthcare name on the wall; a quote here carries into every hospital pitch |
| Dallah Hospital / Aldara Hospital | Same segment, same weight |
| Zahran Facilities Management | FM companies buy repeatedly and refer sideways |
| Aramco Services Company | Recognised instantly Kingdom-wide |
| Insha'at Contracting Co. | Speaks to contractors, a different buyer from the FM route |
| Breeze Med Care / NLS / THC | Useful volume once the first three are in |

Ask the person who actually ran the job with you, not the head office. A
biomedical or facilities engineer will write something specific; a marketing
department will write something generic.

Aim for quotes that name a concrete problem and a concrete outcome — what was
replaced, on what timeline, with how much disruption to live operations.
"Professional and reliable" persuades nobody.

## Email template (English)

> **Subject:** A short favour — two lines about our work together
>
> Dear [Name],
>
> We are adding a section to our website where the people we have worked for
> describe the work in their own words, and I would value having [Company]
> represented there.
>
> It would be two or three sentences: what the problem was, and how the job
> went. To save you the writing, here is a draft you are welcome to change
> however you like, or replace entirely:
>
> "[Draft quote]"
>
> Nothing goes on the site until you have approved the exact wording. We
> would show it as your name, your title and [Company] — and if you would
> rather we used the title and company without your name, that is completely
> fine.
>
> With thanks,
> Afzal Adnan
> Black Arrow Venture
> +966 56 022 4715 · info@blackarrowksa.com

## Email template (Arabic)

> **الموضوع:** طلب بسيط — سطران عن العمل الذي أنجزناه معكم
>
> حضرة الأستاذ/ [الاسم] المحترم،
>
> نعمل حالياً على إضافة قسم في موقعنا الإلكتروني يعرض آراء العملاء الذين
> تشرفنا بخدمتهم بكلماتهم هم، ويسعدنا أن تكون [اسم الشركة] من بينهم.
>
> المطلوب جملتان أو ثلاث فقط: ما كانت المشكلة، وكيف سار العمل. وتسهيلاً
> عليكم، أرفقت أدناه صياغة مقترحة يمكنكم تعديلها كما ترون أو استبدالها
> بالكامل:
>
> «[الصياغة المقترحة]»
>
> لن يُنشر أي شيء على الموقع قبل موافقتكم على النص النهائي، وسيظهر الاقتباس
> باسمكم ومسماكم الوظيفي واسم [الشركة]. وإن فضّلتم الاكتفاء بالمسمى الوظيفي
> واسم الشركة دون الاسم الشخصي، فلا مانع لدينا إطلاقاً.
>
> وتفضلوا بقبول فائق الاحترام،
> أفضل عدنان
> شركة السهم الأسود ڤنتشر
> ‎+966 56 022 4715 · info@blackarrowksa.com

## WhatsApp version — shorter, and usually the one that gets answered

**English**

> Hi [Name] — we are adding a client feedback section to our website. Would
> you be willing to give us two or three sentences about the [project]? I can
> draft it and you just approve it or change it. Nothing goes live without
> your sign-off.

**Arabic**

> السلام عليكم أستاذ [الاسم]، نضيف حالياً قسم آراء العملاء على موقعنا. هل
> تسمح لنا باقتباس جملتين أو ثلاث عن مشروع [ــــ]؟ أستطيع كتابة الصياغة
> وترسلون موافقتكم أو تعديلكم عليها، ولن يُنشر شيء دون موافقتكم.

Ask in whichever language the client normally uses with you. A quote given
in Arabic is more convincing on the Arabic site than a translated one, so
Arabic originals are worth more, not less.

## Star ratings in Google results come from somewhere else

Star ratings in search results are **not** produced by review markup on your
own website. Google treats reviews a business collects and displays about
itself as self-serving, and excludes that markup from review rich results.
This is why no `Review` or `aggregateRating` schema was added here — it would
have added weight to the page and produced nothing.

Stars come from the **Google Business Profile**. That profile is currently
suspended pending video verification, so this is blocked until that clears.
Once it does:

1. Get the short review link from the profile ("Ask for reviews").
2. Send it to the same clients, after they have given the website quote —
   the second ask is easy once the first is done.
3. Reply to every review, including any negative ones. Replies are public and
   are read by the next buyer.

Reviews on the profile do double duty: they feed the map pack for searches
like "UPS maintenance Dammam", and they put the star rating next to your name
in ordinary search results. Neither can be achieved from the website alone.
