# Google Analytics + Search Console — Setup Pack

Two separate Google tools. You need both, and they do different jobs:

| Tool | Answers |
|---|---|
| **Search Console** | How people *find* you on Google — which searches, which pages, what's broken |
| **Analytics (GA4)** | What people *do* once they arrive — pages viewed, how long, where they drop off |

**Search Console matters more right now.** The site has 55 URLs including 24
Arabic pages that Google has never been told about. Until the sitemap is
submitted, the Arabic side may sit undiscovered for months.

Everything below is free. Neither tool costs anything at this traffic level.

---

## Part 1 — Search Console (do this first, ~10 minutes)

### Step 1. Open Search Console
Go to <https://search.google.com/search-console> and sign in with the Google
account you want to own this. **Use a company account, not a personal one** —
whoever owns it controls the data, and moving it later is a hassle.

### Step 2. Add the property
Choose the **URL prefix** box (the right-hand one, not "Domain") and enter
exactly:

```
https://www.blackarrowksa.com/
```

The `www.` and the `https://` both matter. `blackarrowksa.com` without the
`www.` is treated by Google as a different site.

### Step 3. Verify ownership
Google will offer several methods. Pick **HTML tag**. It shows you a line
like:

```html
<meta name="google-site-verification" content="SOME_LONG_STRING" />
```

Send me that line and I'll install it on the site, then you click Verify.

*Alternative that needs no code:* if you control the domain's DNS at your
registrar, pick **Domain** instead and add the TXT record they give you.
That verifies every subdomain at once and never breaks.

### Step 4. Submit the sitemap
Once verified: left menu → **Sitemaps** → enter `sitemap.xml` → Submit.

That single file lists all 55 URLs, English and Arabic, and tells Google
which pages are translations of each other.

### Step 5. Check back
Nothing appears for 2–3 days; that's normal. After a week, look at
**Performance** to see the searches bringing people in, and **Pages** to
confirm the Arabic URLs are being indexed rather than skipped.

---

## Part 2 — Google Analytics 4 (~10 minutes)

### Step 1. Create the property
Go to <https://analytics.google.com> → **Admin** (bottom-left gear) →
**Create** → **Property**.

- Property name: `Black Arrow Venture`
- Time zone: **(GMT+03:00) Saudi Arabia**
- Currency: **Saudi Riyal (SAR)**

Getting the time zone right matters — otherwise your "daily" numbers are cut
at the wrong hour and never line up with your actual business day.

### Step 2. Create a web data stream
When prompted, choose **Web**, then enter:

- Website URL: `https://www.blackarrowksa.com`
- Stream name: `Main site`

### Step 3. Copy the Measurement ID
The stream page shows a **Measurement ID** in the top right. It looks like:

```
G-XXXXXXXXXX
```

**Send me that ID.** It is not a secret — it ships in the public page
source on every site that uses GA4 — so it's fine to paste in chat.

### Step 4. I switch it on
One line changes, in `assets/js/app.js`:

```js
const GA4_MEASUREMENT_ID = 'G-XXXXXXXXXX';
```

That covers all 33 pages at once. Until that string has a value, **no
analytics script loads at all** — no request to Google, no cookies. The site
ships privacy-clean by default.

---

## One thing to decide: the cookie notice

GA4 sets cookies. Saudi Arabia's Personal Data Protection Law (PDPL) expects
visitors to be told.

The site's [privacy policy](privacy-policy.html) currently does **not**
mention analytics cookies, because there are none yet. The moment GA4 goes
live that page becomes inaccurate.

Two options — tell me which you want:

1. **Update the privacy policy only** *(recommended)* — add a short
   analytics section. Low friction, no banner, standard for a B2B site
   whose visitors are businesses rather than consumers.
2. **Add a cookie consent banner too** — the stricter reading. It costs you
   some conversions, as every banner does, and it is more than most Saudi
   B2B sites in this sector run.

I'd go with option 1 and revisit if you ever start running paid ad
retargeting, which is where consent genuinely starts to bite.

---

## What to send me

1. The `google-site-verification` meta tag line (Part 1, Step 3)
2. The `G-XXXXXXXXXX` Measurement ID (Part 2, Step 3)
3. Whether you want option 1 or 2 on the cookie notice

I'll install all three and verify they're reporting before calling it done.
