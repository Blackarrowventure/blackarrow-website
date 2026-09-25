/* Black Arrow 3D — customer reviews on product pages.
   Reviews are stored in the store's Supabase project (see supabase/3d-reviews.sql).
   The site can only add a PENDING review and read APPROVED ones for one product.
   Strings live here (EN + AR) so the form works without touching the main i18n file. */
(function () {
  'use strict';

  var STR = {
    en: {
      title: 'Customer reviews',
      none: 'No reviews yet. Be the first to share your experience.',
      based: function (n) { return n === 1 ? 'Based on 1 review' : 'Based on ' + n + ' reviews'; },
      write: 'Write a review',
      cancel: 'Cancel',
      name: 'Your name',
      nameHint: 'Shown next to your review',
      rating: 'Your rating',
      stars: function (n) { return n + (n === 1 ? ' star' : ' stars'); },
      comment: 'Your review',
      commentHint: '10 to 600 characters',
      lang: 'Language of your review',
      langHint: 'Your review appears on both the English and Arabic site',
      submit: 'Submit review',
      sending: 'Sending…',
      note: 'Reviews appear on the site after we approve them.',
      thanks: 'Thank you! Your review was received and will appear once approved.',
      err_name: 'Please enter your name (2 to 40 characters).',
      err_rating: 'Please choose a star rating.',
      err_comment: 'Please write 10 to 600 characters.',
      err_send: 'We could not send your review right now. Please try again later.',
      wait: 'Please wait a moment before sending another review.',
      written: function (l) { return 'Written in ' + (l === 'ar' ? 'Arabic' : 'English'); },
      of5: ' out of 5'
    },
    ar: {
      title: 'آراء العملاء',
      none: 'لا توجد تقييمات بعد. كن أول من يشاركنا تجربته.',
      based: function (n) { return n === 1 ? 'بناءً على تقييم واحد' : 'بناءً على ' + n + ' تقييمات'; },
      write: 'اكتب تقييمك',
      cancel: 'إلغاء',
      name: 'اسمك',
      nameHint: 'يظهر بجانب تقييمك',
      rating: 'تقييمك',
      stars: function (n) { return n + (n === 1 ? ' نجمة' : ' نجوم'); },
      comment: 'تقييمك',
      commentHint: 'من 10 إلى 600 حرف',
      lang: 'لغة تقييمك',
      langHint: 'سيظهر تقييمك في الموقع العربي والإنجليزي',
      submit: 'إرسال التقييم',
      sending: 'جارٍ الإرسال…',
      note: 'تظهر التقييمات في الموقع بعد موافقتنا عليها.',
      thanks: 'شكرًا لك! وصلنا تقييمك وسيظهر بعد الموافقة عليه.',
      err_name: 'يرجى إدخال اسمك (من 2 إلى 40 حرفًا).',
      err_rating: 'يرجى اختيار عدد النجوم.',
      err_comment: 'يرجى كتابة من 10 إلى 600 حرف.',
      err_send: 'تعذّر إرسال تقييمك الآن. يرجى المحاولة لاحقًا.',
      wait: 'يرجى الانتظار قليلًا قبل إرسال تقييم آخر.',
      written: function (l) { return 'مكتوب بال' + (l === 'ar' ? 'عربية' : 'إنجليزية'); },
      of5: ' من 5'
    }
  };

  var lang = (window.BlackArrow3DI18n && window.BlackArrow3DI18n.getLang()) === 'ar' ? 'ar' : 'en';
  var S = STR[lang];
  var CFG = window.BLACK_ARROW_SUPABASE_CONFIG || null;
  var SENT_KEY = 'b3d_review_sent_at';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function productSlug() {
    var m = location.pathname.match(/^\/3d\/(?:ar\/)?product\/([a-z0-9-]+)\/?$/);
    if (m) return m[1];
    var q = new URLSearchParams(location.search).get('slug');
    return q && /^[a-z0-9-]+$/.test(q) ? q : null;
  }

  function rpc(fn, body) {
    if (!CFG || !CFG.url || !CFG.anonKey) return Promise.reject(new Error('unavailable'));
    return fetch(CFG.url + '/rest/v1/rpc/' + fn, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', apikey: CFG.anonKey, Authorization: 'Bearer ' + CFG.anonKey },
      body: JSON.stringify(body)
    }).then(function (r) {
      if (!r.ok) throw new Error('rpc');
      return r.json();
    });
  }

  function starsHtml(n) {
    var out = '';
    for (var i = 1; i <= 5; i++) out += '<span class="b3d-star' + (i <= n ? ' is-on' : '') + '" aria-hidden="true">★</span>';
    return '<span class="b3d-stars" role="img" aria-label="' + esc(n + S.of5) + '">' + out + '</span>';
  }

  // The text shown for the current site language: the owner's translation if one
  // was added, otherwise the review as written.
  function textFor(r) {
    var mine = lang === 'ar' ? r.comment_ar : r.comment_en;
    if (mine) return { text: mine, original: false };
    return { text: r.comment, original: r.lang !== lang };
  }

  function dateText(iso) {
    try {
      return new Date(iso).toLocaleDateString(lang === 'ar' ? 'ar-SA-u-ca-gregory' : 'en-GB', { year: 'numeric', month: 'short', day: 'numeric' });
    } catch (e) { return ''; }
  }

  function reviewHtml(r) {
    var t = textFor(r);
    return '<article class="b3d-review">' +
      '<div class="b3d-review__head">' + starsHtml(r.rating) +
      '<strong class="b3d-review__name">' + esc(r.name) + '</strong>' +
      '<span class="b3d-review__date">' + esc(dateText(r.created_at)) + '</span></div>' +
      '<p class="b3d-review__text" dir="auto">' + esc(t.text) + '</p>' +
      (t.original ? '<span class="b3d-review__tag">' + esc(S.written(r.lang)) + '</span>' : '') +
      '</article>';
  }

  function summaryHtml(list) {
    if (!list.length) return '<p class="b3d-reviews__none">' + esc(S.none) + '</p>';
    var sum = 0;
    list.forEach(function (r) { sum += r.rating; });
    var avg = sum / list.length;
    return '<div class="b3d-reviews__summary">' +
      '<span class="b3d-reviews__avg">' + avg.toFixed(1) + '</span>' +
      starsHtml(Math.round(avg)) +
      '<span class="b3d-reviews__count">' + esc(S.based(list.length)) + '</span></div>';
  }

  function formHtml() {
    var stars = '';
    for (var i = 5; i >= 1; i--) {
      stars += '<input type="radio" name="b3d-rv-rating" id="b3d-rv-r' + i + '" value="' + i + '">' +
        '<label for="b3d-rv-r' + i + '" title="' + esc(S.stars(i)) + '"><span class="sr-only">' + esc(S.stars(i)) + '</span>★</label>';
    }
    return '<form class="b3d-reviews__form" data-rv-form novalidate hidden>' +
      '<div class="b3d-rv-field"><label for="b3d-rv-name">' + esc(S.name) + '</label>' +
      '<input id="b3d-rv-name" name="name" type="text" maxlength="40" autocomplete="name">' +
      '<small>' + esc(S.nameHint) + '</small></div>' +
      '<div class="b3d-rv-field"><span class="b3d-rv-label" id="b3d-rv-rating-label">' + esc(S.rating) + '</span>' +
      '<div class="b3d-rv-rating" role="radiogroup" aria-labelledby="b3d-rv-rating-label">' + stars + '</div></div>' +
      '<div class="b3d-rv-field"><label for="b3d-rv-comment">' + esc(S.comment) + '</label>' +
      '<textarea id="b3d-rv-comment" name="comment" rows="4" maxlength="600" dir="auto"></textarea>' +
      '<small>' + esc(S.commentHint) + '</small></div>' +
      '<fieldset class="b3d-rv-field b3d-rv-lang"><legend>' + esc(S.lang) + '</legend>' +
      '<label><input type="radio" name="rvlang" value="en"' + (lang === 'en' ? ' checked' : '') + '> English</label>' +
      '<label><input type="radio" name="rvlang" value="ar"' + (lang === 'ar' ? ' checked' : '') + '> العربية</label>' +
      '<small>' + esc(S.langHint) + '</small></fieldset>' +
      '<div class="b3d-rv-hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>' +
      '<p class="b3d-rv-msg" data-rv-msg role="alert" hidden></p>' +
      '<div class="b3d-rv-actions"><button type="submit" class="btn btn-primary" data-rv-submit>' + esc(S.submit) + '</button>' +
      '<button type="button" class="btn btn-outline" data-rv-cancel>' + esc(S.cancel) + '</button></div>' +
      '<p class="b3d-rv-note">' + esc(S.note) + '</p></form>';
  }

  function init() {
    var slug = productSlug();
    var anchor = document.querySelector('[data-b3d-related]');
    if (!slug || !anchor) return;
    // Stay invisible until the reviews service answers, so a form never shows
    // that cannot save (e.g. before the database is set up).
    rpc('get_reviews', { p_product: slug })
      .then(function (list) { build(slug, anchor, Array.isArray(list) ? list : []); })
      .catch(function () {});
  }

  function build(slug, anchor, list) {
    var sec = document.createElement('section');
    sec.className = 'b3d-reviews';
    sec.id = 'reviews';
    sec.setAttribute('aria-labelledby', 'b3d-reviews-title');
    sec.innerHTML =
      '<div class="b3d-reviews__top"><h2 id="b3d-reviews-title">' + esc(S.title) + '</h2>' +
      '<button type="button" class="btn btn-outline" data-rv-open aria-expanded="false" aria-controls="b3d-rv-form-wrap">' + esc(S.write) + '</button></div>' +
      '<div data-rv-summary></div>' +
      '<div id="b3d-rv-form-wrap">' + formHtml() + '</div>' +
      '<div class="b3d-reviews__list" data-rv-list></div>';
    anchor.parentNode.insertBefore(sec, anchor);

    var form = sec.querySelector('[data-rv-form]');
    var openBtn = sec.querySelector('[data-rv-open]');
    var msg = sec.querySelector('[data-rv-msg]');

    function setOpen(open) {
      if (open) form.removeAttribute('hidden'); else form.setAttribute('hidden', '');
      openBtn.setAttribute('aria-expanded', String(open));
      if (open) { var f = form.querySelector('#b3d-rv-name'); if (f) f.focus(); }
    }
    function showMsg(text, ok) {
      msg.textContent = text;
      msg.className = 'b3d-rv-msg' + (ok ? ' is-ok' : ' is-err');
      msg.removeAttribute('hidden');
    }

    openBtn.addEventListener('click', function () { setOpen(form.hasAttribute('hidden')); });
    sec.querySelector('[data-rv-cancel]').addEventListener('click', function () { setOpen(false); openBtn.focus(); });
    if (/[?&]review=1\b/.test(location.search)) {
      setOpen(true);
      sec.scrollIntoView();
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      if (fd.get('website')) { return; } // honeypot
      var name = String(fd.get('name') || '').trim();
      var rating = parseInt(fd.get('b3d-rv-rating'), 10);
      var comment = String(fd.get('comment') || '').trim();
      var rvlang = fd.get('rvlang') === 'ar' ? 'ar' : 'en';
      if (name.length < 2 || name.length > 40) { showMsg(S.err_name, false); return; }
      if (!(rating >= 1 && rating <= 5)) { showMsg(S.err_rating, false); return; }
      if (comment.length < 10 || comment.length > 600) { showMsg(S.err_comment, false); return; }
      try {
        var last = parseInt(localStorage.getItem(SENT_KEY) || '0', 10);
        if (Date.now() - last < 30000) { showMsg(S.wait, false); return; }
      } catch (err) {}
      var btn = form.querySelector('[data-rv-submit]');
      btn.disabled = true;
      btn.textContent = S.sending;
      rpc('submit_review', { p_product: slug, p_name: name, p_rating: rating, p_comment: comment, p_lang: rvlang })
        .then(function (r) {
          if (!r || r.ok !== true) throw new Error('rejected');
          try { localStorage.setItem(SENT_KEY, String(Date.now())); } catch (err) {}
          form.reset();
          showMsg(S.thanks, true);
          btn.textContent = S.submit;
          btn.disabled = false;
        })
        .catch(function () {
          showMsg(S.err_send, false);
          btn.textContent = S.submit;
          btn.disabled = false;
        });
    });

    sec.querySelector('[data-rv-summary]').innerHTML = summaryHtml(list);
    sec.querySelector('[data-rv-list]').innerHTML = list.map(reviewHtml).join('');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
