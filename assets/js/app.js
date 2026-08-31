/* ==============================================
   BLACK ARROW VENTURE
   Main JavaScript — app.js
   Handles: analytics, nav, animations, form, counters
   ============================================== */

'use strict';

/* Must stay the first statement in this file.
   The .reveal* elements are opacity:0 until JS shows them, so if this file
   never runs those sections are invisible for good. The CSS only applies
   that hidden state under html.js, so marking the document here is what
   makes "JavaScript failed" degrade to "no animation" instead of
   "no content". Anything above this line risks throwing first. */
document.documentElement.classList.add('js');

/* ──────────────────────────────────────────────
   0. ANALYTICS (Google Analytics 4)
   ──────────────────────────────────────────────
   TO SWITCH ON: paste the Measurement ID between the quotes below. It
   looks like G-XXXXXXXXXX and comes from Google Analytics ->
   Admin -> Data streams -> your web stream.

   While the string is empty nothing loads: no script request, no
   cookies, no data leaves the visitor's browser. That is why this is
   safe to ship un-configured.

   It lives here rather than in a <head> snippet so one edit covers all
   33 pages instead of 33 near-identical edits that drift apart.
   ────────────────────────────────────────────── */
const GA4_MEASUREMENT_ID = 'G-MXV79G525V';

function initAnalytics() {
  if (!GA4_MEASUREMENT_ID) return;

  const tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_MEASUREMENT_ID;
  document.head.appendChild(tag);

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  // anonymize_ip trims the last octet before the hit is stored, which keeps
  // the analytics claim in the privacy policy honest.
  window.gtag('config', GA4_MEASUREMENT_ID, { anonymize_ip: true });
}

// Fires immediately rather than on DOMContentLoaded so a visitor who
// bounces within the first second is still counted.
initAnalytics();

/* ──────────────────────────────────────────────
   1. LANGUAGE
   ──────────────────────────────────────────────
   The runtime translator that used to live here has been removed.

   It fetched a 126 KB ar.json on every page load and rewrote the DOM via
   el.textContent, which destroyed any child markup inside a translated
   element (it was deleting the WhatsApp icon and the service-card arrows).
   It also produced a visible flash of English before the swap, and it only
   ever produced one URL per page -- so Google indexed the site as English
   only and none of the Arabic was ever discoverable.

   Arabic is now served as real pages under /ar/, generated at build time by
   scripts/build_ar.py from the same assets/translations/ar.json. The EN/AR
   control is now a pair of plain links to the counterpart URL, so there is
   nothing to initialise here.

   IMPORTANT: do not reintroduce a localStorage-driven setLang(). On a static
   /ar/ page it would set <html lang="en" dir="ltr"> over Arabic text, since
   applyTranslations could only ever apply a dictionary, never restore the
   original English.
   ────────────────────────────────────────────── */

/* ──────────────────────────────────────────────
   3. SCROLL REVEAL ANIMATIONS
   ────────────────────────────────────────────── */
function initScrollReveal() {
  const targets = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

  // No observer support: show everything rather than hide it.
  if (!('IntersectionObserver' in window)) {
    targets.forEach(el => el.classList.add('visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  targets.forEach(el => observer.observe(el));

  // Backstop. These elements are invisible until something adds .visible,
  // so any path where the observer never fires costs the reader the whole
  // section. Losing the animation is the cheaper failure.
  setTimeout(() => {
    targets.forEach(el => el.classList.add('visible'));
  }, 3000);
}

/* ──────────────────────────────────────────────
   4. ANIMATED COUNTERS
   ────────────────────────────────────────────── */
function animateCounter(el, target, suffix) {
  const duration = 1800;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(eased * target);
    el.textContent = localeDigits(current) + (suffix || '');
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

/* ──────────────────────────────────────────────
   NUMERALS
   ──────────────────────────────────────────────
   The Arabic pages use Arabic-Indic digits. Anything coming from ar.json
   is already converted at source, but numbers this file *renders* -- the
   animated counters and the footer year -- are built from JS at runtime
   and would otherwise stay Western on /ar/.

   This is what the `number-convertible` class was originally for. It had
   been left on the markup with nothing reading it after the old runtime
   translator was deleted, which is how the two systems drifted apart.

   Only applied when the document says it is Arabic, so the English pages
   are untouched and this file stays shared between both.
   ────────────────────────────────────────────── */
const AR_DIGITS = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];

function isArabicPage() {
  return document.documentElement.getAttribute('lang') === 'ar';
}

function localeDigits(value) {
  const s = String(value);
  if (!isArabicPage()) return s;
  return s.replace(/[0-9]/g, (d) => AR_DIGITS[+d]);
}

/* Converts what is already in the markup, counters included.

   The counters carry their starting value as text as well as in
   data-target, and they only animate once the IntersectionObserver fires.
   A reader who never scrolls that far -- or any run where the observer
   does not fire -- would otherwise be left looking at the Western digits
   sitting in the HTML. Converting up front means the page is correct
   before the animation is involved at all; animateCounter then keeps it
   correct on every frame. */
function initNumerals() {
  if (!isArabicPage()) return;
  document.querySelectorAll('.number-convertible').forEach((el) => {
    el.textContent = localeDigits(el.textContent);
  });
}

function initCounters() {
  const counters = document.querySelectorAll('.stats__num[data-target]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-target'), 10);
        const suffix = el.getAttribute('data-suffix') || '';
        animateCounter(el, target, suffix);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => observer.observe(c));
}

/* ──────────────────────────────────────────────
   5. ACTIVE NAV LINK
   ────────────────────────────────────────────── */
function setActiveNav() {
  const path = window.location.pathname;
  const file = path.split('/').filter(Boolean).pop() || 'index.html';
  document.querySelectorAll('.navbar__links a').forEach(link => {
    const href = (link.getAttribute('href') || '').split('#')[0];
    let isActive;
    if (href === '/services.html' || href === 'services.html') {
      // Folder-style service pages (e.g. /services/isolated-power-panels/) count as "Services" too
      isActive = path === '/services.html' || path.startsWith('/services/');
    } else {
      const linkFile = href.split('/').filter(Boolean).pop() || 'index.html';
      isActive = linkFile === file;
    }
    link.classList.toggle('active', isActive);
  });
}

/* ──────────────────────────────────────────────
   6. CONTACT FORM
   ────────────────────────────────────────────── */
function initForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  function showError(fieldId, message) {
    const errorEl = document.getElementById(fieldId + '-error');
    const input = document.getElementById(fieldId);
    if (errorEl) {
      errorEl.textContent = message;
      errorEl.style.cssText = 'display:block;color:#c41e3a;font-size:0.75rem;margin-top:4px;';
    }
    if (input) input.style.borderColor = '#c41e3a';
  }

  function clearError(fieldId) {
    const errorEl = document.getElementById(fieldId + '-error');
    const input = document.getElementById(fieldId);
    if (errorEl) { errorEl.textContent = ''; errorEl.style.display = 'none'; }
    if (input) input.style.borderColor = '';
  }

  function validateField(id, value, type) {
    clearError(id);
    if (!value.trim()) {
      showError(id, 'This field is required.');
      return false;
    }
    if (type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      showError(id, 'Please enter a valid email address.');
      return false;
    }
    if (type === 'tel' && !/^[\d\s\+\-\(\)]{7,15}$/.test(value)) {
      showError(id, 'Please enter a valid phone number.');
      return false;
    }
    return true;
  }

  // Real-time validation
  ['name', 'email', 'phone', 'message'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('blur', () => {
      validateField(id, el.value, el.type);
    });
    el.addEventListener('input', () => clearError(id));
  });

  // Real submission to Web3Forms.
  //
  // The previous implementation showed a green "Message Sent" state and then
  // fired a mailto: link. On mobile, or anywhere without a configured mail
  // client, that silently discarded the enquiry while telling the visitor it
  // had been sent. Every one of those leads was lost.
  //
  // The <form> carries a real action/method, so with JS disabled the browser
  // does a normal POST and Web3Forms redirects to /thank-you.html. This
  // handler only upgrades that to an inline success state.
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const phone = document.getElementById('phone');
    const message = document.getElementById('message');

    const v1 = validateField('name', name?.value || '', 'text');
    const v2 = validateField('email', email?.value || '', 'email');
    const v3 = validateField('phone', phone?.value || '', 'tel');
    const v4 = validateField('message', message?.value || '', 'text');

    if (!v1 || !v2 || !v3 || !v4) return;

    const submitBtn = form.querySelector('[type="submit"]');
    const originalText = submitBtn.textContent;
    const successEl = document.getElementById('form-success');
    const errorEl = document.getElementById('form-error');

    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    if (errorEl) errorEl.style.display = 'none';

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      });
      const result = await response.json().catch(() => ({}));

      if (response.ok && result.success !== false) {
        if (successEl) successEl.style.display = 'block';
        submitBtn.textContent = '✓ Message Sent';
        submitBtn.style.background = '#2e7d32';
        form.reset();
        successEl?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } else {
        throw new Error(result.message || 'Submission failed');
      }
    } catch (err) {
      // Never claim success we cannot confirm. Show the failure and give the
      // visitor two routes that definitely work.
      if (errorEl) {
        errorEl.style.display = 'block';
      } else {
        alert('Sorry, the message could not be sent. Please email '
            + 'info@blackarrowksa.com or call +966 560 224 715.');
      }
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
}

/* ──────────────────────────────────────────────
   6b. GENERIC WEB3FORMS SUBMISSION
   For the partnership form and the footer newsletter forms, which relied on
   the browser's native POST and therefore did nothing at all. Each <form>
   carries a real action, so these still work without JavaScript; this only
   adds the inline success/error state.
   ────────────────────────────────────────────── */
function initWeb3Forms() {
  document.querySelectorAll('form[data-w3f]').forEach((form) => {
    const successEl = document.getElementById(form.dataset.success);
    const errorEl = document.getElementById(form.dataset.error);

    form.addEventListener('submit', async (e) => {
      if (!form.checkValidity()) return;   // let the browser show its own hints
      e.preventDefault();

      const btn = form.querySelector('[type="submit"]');
      const label = btn ? btn.textContent : '';
      if (btn) { btn.textContent = 'Sending...'; btn.disabled = true; }
      if (errorEl) errorEl.style.display = 'none';

      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' },
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok || data.success === false) throw new Error(data.message || 'failed');

        form.reset();
        if (successEl) {
          successEl.style.display = 'block';
        } else if (btn) {
          btn.textContent = '✓ Subscribed';
        }
        if (btn) btn.style.background = '#2e7d32';
      } catch (err) {
        if (errorEl) {
          errorEl.style.display = 'block';
        } else {
          alert('Sorry, that could not be sent. Please email info@blackarrowksa.com.');
        }
        if (btn) { btn.textContent = label; btn.disabled = false; }
      }
    });
  });
}

/* ──────────────────────────────────────────────
   7. KEYBOARD ACCESSIBILITY
   ────────────────────────────────────────────── */
function initA11y() {
  // Make seg cards keyboard-accessible
  document.querySelectorAll('.seg__card[role="button"]').forEach(card => {
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        card.click();
      }
    });
  });

  // Focus visible ring for keyboard users
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') document.body.classList.add('keyboard-nav');
  });
  document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-nav');
  });
}

/* ──────────────────────────────────────────────
   8. SMOOTH SCROLL FOR ANCHOR LINKS
   ────────────────────────────────────────────── */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const navH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h'), 10) || 80;
        const top = target.getBoundingClientRect().top + window.scrollY - navH - 20;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });
}

/* ──────────────────────────────────────────────
   8b. IMAGE SLIDER (HERO BACKGROUND)
   ────────────────────────────────────────────── */
function initHeroSlider() {
  const images = document.querySelectorAll('.hero__img');
  if (!images.length) return;

  let currentIndex = 0;

  function showImage(index) {
    images.forEach((img, i) => {
      img.classList.toggle('active', i === index);
    });
  }

  // Promote a deferred slide's data-src/data-srcset to real attributes.
  //
  // Every slide is position:absolute; inset:0, so they all sit in the initial
  // viewport and loading="lazy" would be ignored. Holding the URLs in data-*
  // is the only way to keep slides 2-7 off the critical path. Idempotent.
  function load(picture) {
    if (!picture || picture.dataset.loaded) return;
    picture.dataset.loaded = '1';
    picture.querySelectorAll('source[data-srcset]').forEach(source => {
      source.srcset = source.dataset.srcset;
      delete source.dataset.srcset;
    });
    const img = picture.querySelector('img[data-src]');
    if (img) {
      img.src = img.dataset.src;
      delete img.dataset.src;
    }
  }

  const deferred = Array.from(document.querySelectorAll('.hero__img-lazy'));

  // Show first image immediately; it is already a real <img>.
  showImage(0);

  // Only start fetching the rest once the page has finished loading, so they
  // never contend with the LCP image or the stylesheet.
  function loadRest() {
    deferred.forEach((picture, i) => {
      // Stagger slightly so seven requests don't burst at once.
      setTimeout(() => load(picture), i * 300);
    });
  }

  if (document.readyState === 'complete') {
    loadRest();
  } else {
    window.addEventListener('load', loadRest, { once: true });
  }

  // Auto-cycle every 5.5 seconds. Guarantee the next slide is loaded before
  // it is shown, in case the cycle outruns the staggered preload.
  setInterval(() => {
    currentIndex = (currentIndex + 1) % images.length;
    if (currentIndex > 0) load(deferred[currentIndex - 1]);
    load(deferred[currentIndex]);   // also warm the one after
    showImage(currentIndex);
  }, 5500);
}

/* ──────────────────────────────────────────────
   9. WHATSAPP CTA OPTIMIZATION
   ────────────────────────────────────────────── */
const WHATSAPP_NUMBER = '966560224715';
const SERVICE_MESSAGES = {
  'ev-solutions': 'Hello! I\'m interested in your EV Charger Solutions (AC/DC chargers, POS systems, maintenance)',
  'ups-solutions': 'Hello! I\'m interested in your UPS Solutions (turnkey systems, batteries, maintenance)',
  'lighting-solutions': 'Hello! I\'m interested in your Lighting Solutions (facade, exterior, interior, signage)',
  'firefighting-systems': 'Hello! I\'m interested in your Firefighting Systems (detection, suppression, maintenance)',
  'hvac-solutions': 'Hello! I\'m interested in your HVAC Solutions (climate control, installation, maintenance)',
  'electrical-power': 'Hello! I\'m interested in your Electrical & Power Distribution solutions (switchgear, panels)',
  'hospital-modular-or-rooms': 'Hello! I\'m interested in your Hospital Modular OR Room solutions (design, build, commissioning)',
  'lead-sheets-hospital': 'Hello! I\'m interested in your Lead Sheet Radiation Shielding for hospitals (X-ray, CT, radiotherapy rooms)',
  'partnership': 'Hello! I\'m interested in partnership opportunities with Black Arrow Company',
  'default': 'Hello! I\'m interested in your services. Can you help me?'
};

function getWhatsAppLink(serviceKey = 'default') {
  const message = SERVICE_MESSAGES[serviceKey] || SERVICE_MESSAGES['default'];
  const encodedMsg = encodeURIComponent(message);
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodedMsg}`;
}

// Footer copyright year. Kept in JS so the year never goes stale in 33 files.
function initFooterYear() {
  const year = localeDigits(new Date().getFullYear());
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = year;
  });
}

function initWhatsAppLinks() {
  document.querySelectorAll('[data-whatsapp-service]').forEach(el => {
    const serviceKey = el.getAttribute('data-whatsapp-service');
    const url = getWhatsAppLink(serviceKey);
    if (el.tagName === 'A') {
      el.href = url;
    } else {
      // 'noopener' in the features argument, not just the target. Browsers
      // apply implicit noopener to target="_blank" on anchors, but NOT to
      // window.open - without it the WhatsApp tab keeps a live handle back
      // to this page through window.opener.
      el.onclick = () => window.open(url, '_blank', 'noopener');
    }
  });

  // Update floating WhatsApp button based on page context
  const waFloat = document.querySelector('.wa-float');
  if (waFloat) {
    const pageService = document.querySelector('[data-service-id]')?.getAttribute('data-service-id');
    if (pageService) {
      waFloat.href = getWhatsAppLink(pageService);
    }
  }
}

/* ──────────────────────────────────────────────
   9b. SERVICE WORKER SHIM
   ──────────────────────────────────────────────
   The service worker was retired, but visitors who loaded the site while
   it was live still have the old one installed and it would keep serving
   them stale pages forever. /service-worker.js is now a shim whose only
   job is to unregister itself, so this has to keep running until we can
   assume every previous visitor has come back at least once.

   Moved here from an inline <script> in index.html when the
   Content-Security-Policy went in.
   ────────────────────────────────────────────── */
function initServiceWorker() {
  if (!('serviceWorker' in navigator)) return;
  navigator.serviceWorker.register('/service-worker.js').catch(() => {});
}

/* ──────────────────────────────────────────────
   9c. CLICKABLE CARDS
   ──────────────────────────────────────────────
   The "Who We Serve" cards were divs carrying onclick="location.href=..."
   which the Content-Security-Policy blocks. They now declare their target
   as data-href and this delegated listener navigates.

   They also carry role="button" and tabindex="0" but never had a key
   handler, so a keyboard user could focus one and press Enter to no
   effect at all. Handling keydown here fixes that at the same time -
   a control that announces itself as a button has to behave like one.
   ────────────────────────────────────────────── */
function initClickableCards() {
  const go = (el) => {
    const href = el.getAttribute('data-href');
    if (href) window.location.href = href;
  };

  document.addEventListener('click', (e) => {
    const card = e.target.closest('[data-href]');
    if (card) go(card);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') return;
    const card = e.target.closest('[data-href]');
    if (!card) return;
    e.preventDefault();          // stop Space scrolling the page
    go(card);
  });
}

/* ──────────────────────────────────────────────
   10. INIT ALL
   ────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initServiceWorker();
  initClickableCards();
  initHeroSlider();
  initScrollReveal();
  initNumerals();
  initCounters();
  setActiveNav();
  initForm();
  initWeb3Forms();
  initA11y();
  initSmoothScroll();
  initWhatsAppLinks();
  initFooterYear();
});

// Expose WhatsApp functions globally for inline use
window.getWhatsAppLink = getWhatsAppLink;
