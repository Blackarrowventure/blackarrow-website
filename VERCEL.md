# vercel.json — why it says what it says

`vercel.json` cannot hold comments. **JSON has no comment syntax, and Vercel
rejects any property it does not recognise**, so a `"_comment_..."` key does
not sit there harmlessly — it fails schema validation and the deployment is
refused outright:

```
Invalid request: should NOT have additional property `_comment_trailingSlash`.
Please remove it.
```

That is not a warning. The build does not run, the old version keeps
serving, and the dashboard shows no new production deployment. It cost this
site **21 hours of silently un-deployed commits** on 7–8 Aug 2026 — every
change looked pushed, GitHub had it all, and none of it was live.

**So: no comment keys in `vercel.json`. Ever.** Explanations belong here.

---

## `"trailingSlash": true`

**Must stay true.** The site's entire URL convention uses trailing slashes:
every canonical tag, every hreflang alternate and all 64 sitemap entries are
the `/path/` form, and that is what Google has indexed.

Setting it to `false` — or omitting it, since Vercel's default also strips —
makes every one of those URLs 308-redirect, so each canonical points at a
redirect instead of a page.

It only affects extensionless directory paths. `/about.html` and friends are
untouched either way.

## `"cleanUrls": false`

The root pages are real `.html` files and are linked, canonicalised and
listed in the sitemap that way. `cleanUrls: true` would start serving them
at extensionless paths as well, giving every root page two live URLs.

## `headers`

- **Asset caching is deliberately short-fresh + long-stale.** Filenames here
  carry no content hash — `styles.css` is always `styles.css` — so a plain
  `max-age` is a promise the browser will *ignore new deploys* for exactly
  that long. It was 7 days on CSS/JS, which meant a returning visitor kept
  the old stylesheet for a week no matter how many times we shipped.

  That is not theoretical: on 10 Aug 2026 the footer logo was reported as
  huge and blurry, and it was — in a **week-old cached stylesheet** still
  carrying `height: 180px` (an 8:1 wordmark at that height is 1443px wide).
  Production was correct the whole time and a clean-cache fetch proved it.
  Several rounds of resizing were reviewed against a stale file.

  So: `max-age=600, stale-while-revalidate=604800` on CSS/JS/translations,
  and `max-age=86400, stale-while-revalidate=2592000` on images. The page
  still paints instantly from cache; the browser revalidates in the
  background and picks changes up on the next visit rather than next week.

  Images need the same treatment because assets are **replaced in place** —
  `black-arrow-wordmark.png` was swapped for a 3x version under the same
  name, so a 30-day image cache would have pinned returning visitors to the
  old low-resolution logo for a month.

  If a build step ever adds content-hashed filenames, these can go back to
  a year and `immutable`.
- `service-worker.js` is `max-age=0, must-revalidate`. An earlier service
  worker pinned returning visitors to stale assets; it has been replaced by
  a self-unregistering shim, and that shim is useless if it is itself
  cached.
- `X-Robots-Tag: noindex` on `/contacts/`, `PREVIEW_*`, `COLOR_*`,
  `business-card-*`, and both `/thank-you.html` and `/ar/thank-you.html`.
  The Arabic one matters: the `/ar/` forms redirect there after submission.
- The catch-all block is ordinary security hardening (nosniff, frame
  options, referrer policy, permissions policy, HSTS).

## Checking a config change before pushing

`vercel.json` is validated server-side, so local JSON parsing proves only
that it is *valid JSON*, not that Vercel will accept it:

```bash
python -c "import json; json.load(open('vercel.json')); print('valid JSON')"
```

After any `vercel.json` change, confirm the deploy actually landed rather
than assuming it did:

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://www.blackarrowksa.com/
curl -s -I https://www.blackarrowksa.com/ | grep -i age
```

A large `Age:` with nothing newly deployed means production is still serving
an old build.
