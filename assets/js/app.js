/* ==============================================
   EIGHT STARS EASTERN COMPANY
   Main JavaScript — app.js
   Handles: i18n, nav, animations, form, counters
   ============================================== */

'use strict';

/* ──────────────────────────────────────────────
   1. LANGUAGE / i18n
   ────────────────────────────────────────────── */
const translations = {};

// Convert English numerals to Arabic numerals
function convertNumbersToArabic(text) {
  if (!text) return text;
  const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return String(text).replace(/\d/g, d => arabicNumbers[d]);
}

// Convert Arabic numerals to English numerals
function convertNumbersToEnglish(text) {
  if (!text) return text;
  const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  let result = String(text);
  arabicNumbers.forEach((char, index) => {
    result = result.replace(new RegExp(char, 'g'), index);
  });
  return result;
}

async function loadTranslations(lang) {
  if (translations[lang]) {
    console.log(`Using cached ${lang} translations`);
    return translations[lang];
  }
  try {
    const res = await fetch(`assets/translations/${lang}.json`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    translations[lang] = await res.json();
    console.log(`Loaded ${lang} translations:`, Object.keys(translations[lang]).length, 'keys');
    return translations[lang];
  } catch (e) {
    console.error(`Failed to load ${lang} translations:`, e);
    return null;
  }
}

async function applyTranslations(lang) {
  console.log(`Applying ${lang} translations...`);
  const t = await loadTranslations(lang);

  if (!t || Object.keys(t).length === 0) {
    console.warn(`No translations found for ${lang}`);
    return;
  }

  let updated = 0;
  // Update text content
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = t[key];
      } else {
        el.textContent = t[key];
      }
      updated++;
    }
  });
  console.log(`Updated ${updated} elements with ${lang} translations`);

  // Update placeholder attributes
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (t[key]) el.placeholder = t[key];
  });

  // Update document title with lang suffix
  if (lang === 'ar') {
    document.title = document.title.replace('Eight Stars Eastern', 'ثمانية نجوم الشرقية');

    // Convert all numbers to Arabic numerals
    document.querySelectorAll('.number-convertible').forEach(el => {
      el.textContent = convertNumbersToArabic(el.textContent);
    });
  } else {
    // Convert back to English numerals
    document.querySelectorAll('.number-convertible').forEach(el => {
      el.textContent = convertNumbersToEnglish(el.textContent);
    });
  }
}

function setLang(lang) {
  const html = document.documentElement;
  const isAr = lang === 'ar';

  html.setAttribute('lang', lang);
  html.setAttribute('dir', isAr ? 'rtl' : 'ltr');

  // Update switcher buttons
  const enBtn = document.getElementById('lang-en');
  const arBtn = document.getElementById('lang-ar');
  if (enBtn) enBtn.classList.toggle('active', !isAr);
  if (arBtn) arBtn.classList.toggle('active', isAr);

  // Load and apply translations
  applyTranslations(lang);

  // Persist preference
  try { localStorage.setItem('lang', lang); } catch (e) {}
}

function initLang() {
  let lang = 'en';
  try {
    lang = localStorage.getItem('lang') || 'en';
  } catch (e) {}

  // Auto-detect Arabic browser preference
  if (!localStorage.getItem('lang')) {
    const browserLang = navigator.language || navigator.userLanguage || '';
    if (browserLang.startsWith('ar')) lang = 'ar';
  }

  setLang(lang);
}

// Expose globally for inline onclick handlers
window.setLang = setLang;

/* ──────────────────────────────────────────────
   2. MOBILE NAVIGATION
   ────────────────────────────────────────────── */
function initNav() {
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobile-nav');
  if (!hamburger || !mobileNav) return;

  function toggleMenu(open) {
    hamburger.classList.toggle('open', open);
    mobileNav.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', open.toString());
    document.body.style.overflow = open ? 'hidden' : '';
  }

  hamburger.addEventListener('click', () => {
    const isOpen = mobileNav.classList.contains('open');
    toggleMenu(!isOpen);
  });

  // Close on link click
  mobileNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => toggleMenu(false));
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !mobileNav.contains(e.target)) {
      toggleMenu(false);
    }
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') toggleMenu(false);
  });
}

/* ──────────────────────────────────────────────
   3. SCROLL REVEAL ANIMATIONS
   ────────────────────────────────────────────── */
function initScrollReveal() {
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

  document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
    observer.observe(el);
  });
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
    el.textContent = current + (suffix || '');
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
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
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navbar__links a, .mobile-nav a').forEach(link => {
    const href = link.getAttribute('href') || '';
    const linkPage = href.split('/').pop().split('#')[0] || 'index.html';
    link.classList.toggle('active', linkPage === path);
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
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    // Compose mailto link as fallback (since no server backend)
    const service = document.getElementById('service')?.value || '';
    const company = document.getElementById('company')?.value || '';
    const subject = encodeURIComponent(`Inquiry from ${name.value} - ${service || 'General'}`);
    const body = encodeURIComponent(
      `Name: ${name.value}\nCompany: ${company}\nPhone: ${phone.value}\nService: ${service}\n\n${message.value}`
    );

    // Try to open WhatsApp with message as alternative
    const waMsg = encodeURIComponent(
      `Hello, I'm ${name.value} from ${company || 'my company'}. I'm interested in ${service || 'your services'}. ${message.value}`
    );

    // Show success and redirect to email
    setTimeout(() => {
      const successEl = document.getElementById('form-success');
      if (successEl) successEl.style.display = 'block';
      submitBtn.textContent = '✓ Message Sent';
      submitBtn.style.background = '#2e7d32';
      form.reset();
      // Open email client
      window.location.href = `mailto:info@blackarrowksa.com?subject=${subject}&body=${body}`;
    }, 800);
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

  // Show first image
  showImage(0);

  // Auto-cycle every 5.5 seconds
  setInterval(() => {
    currentIndex = (currentIndex + 1) % images.length;
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
  'general-trading': 'Hello! I\'m interested in your General Trading services (industrial, safety, aviation, oil & gas)',
  'partnership': 'Hello! I\'m interested in partnership opportunities with Black Arrow Company',
  'default': 'Hello! I\'m interested in your services. Can you help me?'
};

function getWhatsAppLink(serviceKey = 'default') {
  const message = SERVICE_MESSAGES[serviceKey] || SERVICE_MESSAGES['default'];
  const encodedMsg = encodeURIComponent(message);
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodedMsg}`;
}

function initWhatsAppLinks() {
  document.querySelectorAll('[data-whatsapp-service]').forEach(el => {
    const serviceKey = el.getAttribute('data-whatsapp-service');
    const url = getWhatsAppLink(serviceKey);
    if (el.tagName === 'A') {
      el.href = url;
    } else {
      el.onclick = () => window.open(url, '_blank');
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
   10. INIT ALL
   ────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initLang();
  initNav();
  initHeroSlider();
  initScrollReveal();
  initCounters();
  setActiveNav();
  initForm();
  initA11y();
  initSmoothScroll();
  initWhatsAppLinks();
});

// Expose WhatsApp functions globally for inline use
window.getWhatsAppLink = getWhatsAppLink;
