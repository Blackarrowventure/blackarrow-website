# Blog plan

Internal note. `.vercelignore`d, so it is never served.

## Why there are only two posts

Not a lack of things to say. A post file is 247 lines, of which **219 — 89% —
are head, nav, footer and schema identical on every post**. Publishing one by
hand also means editing `pages.json`, `ar-pages.json`, `en.json`, `ar.json`
and the blog index, then running three scripts. Miss any of it and the build
fails, or worse, the page ships without hreflang.

"One post a month" was never going to survive that. So the overhead is gone:

    py scripts/new_post.py --init saso-ev-charger-requirements
    # fill in drafts/saso-ev-charger-requirements.json
    py scripts/new_post.py --spec drafts/saso-ev-charger-requirements.json --check
    py scripts/new_post.py --spec drafts/saso-ev-charger-requirements.json --apply
    py scripts/build_ar.py --build && py scripts/build_sitemap.py --apply && py scripts/check_links.py

What is left is writing the prose in both languages, which is the part that
should cost something.

**The Arabic is not optional.** `build_ar.py` refuses the build if any
`data-i18n` key is missing from `ar.json`. That is deliberate — it is what
stops the Arabic site silently shipping English — and it means every post is
a bilingual job. Budget for it.

## What to write about

The two existing posts are aimed correctly: NFPA 99 and isolated power panels
are terms a hospital engineer searches **by name**. Keep that discipline. The
test for a topic is not "is this about our industry" but "would a facility
manager type this at 2am with a problem in front of them".

Ordered by how closely each maps to work already being sold:

| # | Working title | Who is searching, and why |
|---|---|---|
| 1 | What NFPA 99 says about line isolation monitors | Follows the two live posts; the LIM is the part people get wrong at handover |
| 2 | Sizing a UPS for a hospital critical branch | Direct commercial intent, and the healthcare UPS case study backs it |
| 3 | SASO requirements for EV chargers in Saudi Arabia | High volume, low competition, and it is a live regulatory question |
| 4 | Why your UPS batteries died in three years, not ten | Written from the failure, not the product. Heat in Dammam is the answer |
| 5 | Obstruction lighting: when GACA requires it | Nobody writes this in English for the Saudi market |
| 6 | Isolated power vs GFCI in operating theatres | The comparison a consultant actually has to justify to a client |
| 7 | Reading a UPS single-line diagram | Teaches something; earns links from people who are not buying yet |
| 8 | HVAC handover in a running hotel, floor by floor | The hospitality case study, told as method |
| 9 | What a Civil Defense inspection checks first | Read in a panic the week before an inspection |
| 10 | Selective coordination in a hospital distribution board | Narrow, technical, and it filters for serious buyers |
| 11 | Helipad lighting: what a rooftop actually needs | The high-rise case study, written as a specification |
| 12 | Commissioning an isolated power panel: the checklist | Practical, printable, and it earns bookmarks |

Two habits worth keeping:

**Write from the failure, not the product.** "Why your UPS batteries died in
three years" outperforms "our UPS maintenance service" because it matches
what someone types when they have the problem.

**Each post should name a standard, a number, or a place.** NFPA 99, SASO,
GACA, Dammam, 40°C. Vague posts rank for nothing.

## The realistic target

Twelve posts is a year. It will not move anything for the first two or three
months, and that is normal — this is the slow lever. What it eventually buys
is ranking for the terms a competitor with a fourteen-year head start on the
brand name does not own, because nobody owns "NFPA 99 Saudi Arabia".

Do not chase volume. Two good posts a quarter beats six thin ones, and thin
posts on a small site actively dilute it.
