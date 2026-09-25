/* Black Arrow 3D — customer reviews of the service, with optional photos.
   Reviews and photos live in the store's Supabase project (see supabase/3d-reviews.sql).
   The site can only add a PENDING review / upload a photo, and read APPROVED reviews.

   Mount points (a section stays invisible until the reviews service answers):
     <div data-b3d-reviews="page">     full section: summary, form, all reviews (/3d/reviews/)
     <section data-b3d-reviews="teaser"> latest reviews on the homepage (hidden if there are none)
   Strings live here (EN + AR) so the form works without touching the main i18n file. */
(function () {
  'use strict';

  var STR = {
    en: {
      title: 'Latest reviews',
      teaserTitle: 'What our customers say',
      none: 'No reviews yet. Be the first to share your experience.',
      based: function (n) { return n === 1 ? 'Based on 1 review' : 'Based on ' + n + ' reviews'; },
      write: 'Write a review',
      seeAll: 'See all reviews and write yours',
      cancel: 'Cancel',
      name: 'Your name',
      nameHint: 'Shown next to your review',
      rating: 'Your rating',
      stars: function (n) { return n + (n === 1 ? ' star' : ' stars'); },
      comment: 'Your review',
      commentHint: '10 to 600 characters',
      photos: 'Add photos (optional)',
      photosHint: 'Up to 3 photos of your order. Photos appear publicly once we approve your review.',
      lang: 'Language of your review',
      langHint: 'Your review appears on both the English and Arabic site',
      submit: 'Submit review',
      sending: 'Sending…',
      note: 'Reviews appear on the site after we approve them.',
      thanks: 'Thank you! Your review was received and will appear once approved.',
      err_name: 'Please enter your name (2 to 40 characters).',
      err_rating: 'Please choose a star rating.',
      err_comment: 'Please write 10 to 600 characters.',
      err_photo: 'One of the photos could not be read. Please choose JPG, PNG or WebP images.',
      err_send: 'We could not send your review right now. Please try again later.',
      wait: 'Please wait a moment before sending another review.',
      photoOf: 'Photo from a customer review',
      written: function (l) { return 'Written in ' + (l === 'ar' ? 'Arabic' : 'English'); },
      of5: ' out of 5'
    },
    ar: {
      title: 'أحدث التقييمات',
      teaserTitle: 'ماذا يقول عملاؤنا',
      none: 'لا توجد تقييمات بعد. كن أول من يشاركنا تجربته.',
      based: function (n) { return n === 1 ? 'بناءً على تقييم واحد' : 'بناءً على ' + n + ' تقييمات'; },
      write: 'اكتب تقييمك',
      seeAll: 'عرض كل التقييمات واكتب تقييمك',
      cancel: 'إلغاء',
      name: 'اسمك',
      nameHint: 'يظهر بجانب تقييمك',
      rating: 'تقييمك',
      stars: function (n) { return n + (n === 1 ? ' نجمة' : ' نجوم'); },
      comment: 'تقييمك',
      commentHint: 'من 10 إلى 600 حرف',
      photos: 'أضف صورًا (اختياري)',
      photosHint: 'حتى 3 صور لطلبك. تظهر الصور للجميع بعد موافقتنا على تقييمك.',
      lang: 'لغة تقييمك',
      langHint: 'سيظهر تقييمك في الموقع العربي والإنجليزي',
      submit: 'إرسال التقييم',
      sending: 'جارٍ الإرسال…',
      note: 'تظهر التقييمات في الموقع بعد موافقتنا عليها.',
      thanks: 'شكرًا لك! وصلنا تقييمك وسيظهر بعد الموافقة عليه.',
      err_name: 'يرجى إدخال اسمك (من 2 إلى 40 حرفًا).',
      err_rating: 'يرجى اختيار عدد النجوم.',
      err_comment: 'يرجى كتابة من 10 إلى 600 حرف.',
      err_photo: 'تعذّرت قراءة إحدى الصور. يرجى اختيار صور بصيغة JPG أو PNG أو WebP.',
      err_send: 'تعذّر إرسال تقييمك الآن. يرجى المحاولة لاحقًا.',
      wait: 'يرجى الانتظار قليلًا قبل إرسال تقييم آخر.',
      photoOf: 'صورة من تقييم عميل',
      written: function (l) { return 'مكتوب بال' + (l === 'ar' ? 'عربية' : 'إنجليزية'); },
      of5: ' من 5'
    }
  };

  var lang = (window.BlackArrow3DI18n && window.BlackArrow3DI18n.getLang()) === 'ar' ? 'ar' : 'en';
  var S = STR[lang];
  var CFG = window.BLACK_ARROW_SUPABASE_CONFIG || null;
  var SENT_KEY = 'b3d_review_sent_at';
  var BUCKET = 'review-photos';
  var MAX_PHOTOS = 3;
  var REVIEWS_URL = lang === 'ar' ? '/3d/ar/reviews/' : '/3d/reviews/';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function ready() { return !!(CFG && CFG.url && CFG.anonKey); }

  function rpc(fn, body) {
    if (!ready()) return Promise.reject(new Error('unavailable'));
    return fetch(CFG.url + '/rest/v1/rpc/' + fn, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', apikey: CFG.anonKey, Authorization: 'Bearer ' + CFG.anonKey },
      body: JSON.stringify(body)
    }).then(function (r) {
      if (!r.ok) throw new Error('rpc');
      return r.json();
    });
  }

  function photoUrl(file) {
    return CFG.url + '/storage/v1/object/public/' + BUCKET + '/' + encodeURIComponent(file);
  }

  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    var b = new Uint8Array(16);
    crypto.getRandomValues(b);
    b[6] = (b[6] & 0x0f) | 0x40; b[8] = (b[8] & 0x3f) | 0x80;
    var h = Array.prototype.map.call(b, function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
    return h.slice(0, 8) + '-' + h.slice(8, 12) + '-' + h.slice(12, 16) + '-' + h.slice(16, 20) + '-' + h.slice(20);
  }

  // Shrink a chosen photo to a JPEG of at most 1400px, so uploads stay small and fast.
  function compress(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        try {
          var scale = Math.min(1, 1400 / Math.max(img.naturalWidth, img.naturalHeight));
          var w = Math.max(1, Math.round(img.naturalWidth * scale));
          var h = Math.max(1, Math.round(img.naturalHeight * scale));
          var c = document.createElement('canvas');
          c.width = w; c.height = h;
          var ctx = c.getContext('2d');
          ctx.fillStyle = '#fff';
          ctx.fillRect(0, 0, w, h);
          ctx.drawImage(img, 0, 0, w, h);
          c.toBlob(function (blob) {
            URL.revokeObjectURL(url);
            if (blob) resolve(blob); else reject(new Error('photo'));
          }, 'image/jpeg', 0.82);
        } catch (e) { URL.revokeObjectURL(url); reject(e); }
      };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error('photo')); };
      img.src = url;
    });
  }

  function uploadPhoto(blob) {
    var name = uuid() + '.jpg';
    return fetch(CFG.url + '/storage/v1/object/' + BUCKET + '/' + name, {
      method: 'POST',
      headers: { apikey: CFG.anonKey, Authorization: 'Bearer ' + CFG.anonKey, 'Content-Type': 'image/jpeg', 'x-upsert': 'false' },
      body: blob
    }).then(function (r) {
      if (!r.ok) throw new Error('upload');
      return name;
    });
  }

  function starsHtml(n) {
    var out = '';
    for (var i = 1; i <= 5; i++) out += '<span class="b3d-star' + (i <= n ? ' is-on' : '') + '" aria-hidden="true">★</span>';
    return '<span class="b3d-stars" role="img" aria-label="' + esc(n + S.of5) + '">' + out + '</span>';
  }

  // The owner's translation if one was added, otherwise the review as written.
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
    var photos = (r.photos || []).filter(function (f) { return /^[0-9a-f-]{36}\.jpg$/.test(f); });
    return '<article class="b3d-review">' +
      '<div class="b3d-review__head">' + starsHtml(r.rating) +
      '<strong class="b3d-review__name">' + esc(r.name) + '</strong>' +
      '<span class="b3d-review__date">' + esc(dateText(r.created_at)) + '</span></div>' +
      '<p class="b3d-review__text" dir="auto">' + esc(t.text) + '</p>' +
      (photos.length ? '<div class="b3d-review__photos">' + photos.map(function (f) {
        return '<a href="' + esc(photoUrl(f)) + '" target="_blank" rel="noopener noreferrer"><img src="' + esc(photoUrl(f)) + '" alt="' + esc(S.photoOf) + '" loading="lazy"></a>';
      }).join('') + '</div>' : '') +
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
      '<div class="b3d-rv-field"><label for="b3d-rv-photos">' + esc(S.photos) + '</label>' +
      '<input id="b3d-rv-photos" name="photos" type="file" accept="image/*" multiple>' +
      '<div class="b3d-rv-previews" data-rv-previews></div>' +
      '<small>' + esc(S.photosHint) + '</small></div>' +
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

  function buildPage(host, list) {
    host.classList.add('b3d-reviews');
    host.setAttribute('aria-labelledby', 'b3d-reviews-title');
    host.innerHTML =
      '<div class="b3d-reviews__top"><h2 id="b3d-reviews-title">' + esc(S.title) + '</h2>' +
      '<button type="button" class="btn btn-outline" data-rv-open aria-expanded="false" aria-controls="b3d-rv-form-wrap">' + esc(S.write) + '</button></div>' +
      summaryHtml(list) +
      '<div id="b3d-rv-form-wrap">' + formHtml() + '</div>' +
      '<div class="b3d-reviews__list">' + list.map(reviewHtml).join('') + '</div>';

    var form = host.querySelector('[data-rv-form]');
    var openBtn = host.querySelector('[data-rv-open]');
    var msg = host.querySelector('[data-rv-msg]');
    var fileInput = host.querySelector('#b3d-rv-photos');
    var previews = host.querySelector('[data-rv-previews]');

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
    host.querySelector('[data-rv-cancel]').addEventListener('click', function () { setOpen(false); openBtn.focus(); });
    if (/[?&]review=1\b/.test(location.search)) { setOpen(true); host.scrollIntoView(); }

    var chosen = [];
    fileInput.addEventListener('change', function () {
      chosen = Array.prototype.slice.call(fileInput.files || [], 0, MAX_PHOTOS);
      previews.innerHTML = '';
      chosen.forEach(function (f) {
        var im = document.createElement('img');
        im.alt = '';
        im.src = URL.createObjectURL(f);
        im.onload = function () { URL.revokeObjectURL(im.src); };
        previews.appendChild(im);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      if (fd.get('website')) return; // honeypot
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
      function reset() { btn.textContent = S.submit; btn.disabled = false; }
      Promise.all(chosen.map(function (f) { return compress(f).then(uploadPhoto); }))
        .then(function (files) {
          return rpc('submit_review', { p_name: name, p_rating: rating, p_comment: comment, p_lang: rvlang, p_photos: files });
        })
        .then(function (r) {
          if (!r || r.ok !== true) throw new Error('rejected');
          try { localStorage.setItem(SENT_KEY, String(Date.now())); } catch (err) {}
          form.reset();
          chosen = [];
          previews.innerHTML = '';
          showMsg(S.thanks, true);
          reset();
        })
        .catch(function (err) {
          showMsg(err && err.message === 'photo' ? S.err_photo : S.err_send, false);
          reset();
        });
    });
  }

  function buildTeaser(host, list) {
    if (!list.length) return; // nothing to show yet: the section stays hidden
    var latest = list.slice(0, 3);
    host.innerHTML =
      '<div class="section-header"><h2>' + esc(S.teaserTitle) + '</h2></div>' +
      summaryHtml(list) +
      '<div class="b3d-reviews__list b3d-reviews__list--three">' + latest.map(reviewHtml).join('') + '</div>' +
      '<div style="text-align:center;margin-top:24px;"><a class="btn btn-outline" href="' + REVIEWS_URL + '">' + esc(S.seeAll) + '</a></div>';
    host.classList.add('b3d-reviews');
    host.removeAttribute('hidden');
  }

  function init() {
    var host = document.querySelector('[data-b3d-reviews]');
    if (!host) return;
    var mode = host.getAttribute('data-b3d-reviews');
    rpc('get_reviews', {})
      .then(function (list) {
        list = Array.isArray(list) ? list : [];
        if (mode === 'teaser') buildTeaser(host, list); else buildPage(host, list);
      })
      .catch(function () {}); // service not available: show nothing
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
