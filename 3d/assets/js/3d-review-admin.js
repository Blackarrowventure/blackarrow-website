/* Black Arrow 3D — private review approval page (/3d/review-admin/).
   Sign in with a store account whose confirmed email is listed in the
   review_admins table (supabase/3d-reviews-admin.sql). Every action is checked
   again by the database, so this page alone gives nobody any access. */
(function () {
  'use strict';

  var CFG = window.BLACK_ARROW_SUPABASE_CONFIG || null;
  var host = document.querySelector('[data-b3d-review-admin]');
  if (!host) return;

  var client = null;
  var status = 'pending';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function loadSdk(cb) {
    if (window.supabase && window.supabase.createClient) { cb(); return; }
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
    s.onload = cb; s.onerror = cb;
    document.head.appendChild(s);
  }

  function photoUrl(f) { return CFG.url + '/storage/v1/object/public/review-photos/' + encodeURIComponent(f); }

  function stars(n) {
    var o = '';
    for (var i = 1; i <= 5; i++) o += '<span class="b3d-star' + (i <= n ? ' is-on' : '') + '">★</span>';
    return '<span class="b3d-stars" role="img" aria-label="' + n + ' out of 5">' + o + '</span>';
  }

  function loginView(msg) {
    host.innerHTML =
      '<form class="b3d-reviews__form" data-ra-login novalidate style="max-width:420px">' +
      '<div class="b3d-rv-field"><label for="ra-email">Email</label><input id="ra-email" type="text" inputmode="email" autocomplete="username"></div>' +
      '<div class="b3d-rv-field"><label for="ra-pass">Password</label><input id="ra-pass" type="password" autocomplete="current-password"></div>' +
      '<p class="b3d-rv-msg is-err" role="alert"' + (msg ? '' : ' hidden') + '>' + esc(msg || '') + '</p>' +
      '<div class="b3d-rv-actions"><button type="submit" class="btn btn-primary">Sign in</button></div></form>';
    host.querySelector('[data-ra-login]').addEventListener('submit', function (e) {
      e.preventDefault();
      var email = host.querySelector('#ra-email').value.trim();
      var pass = host.querySelector('#ra-pass').value;
      client.auth.signInWithPassword({ email: email, password: pass }).then(function (res) {
        if (res.error) loginView('Sign-in failed. Check your email and password.'); else start();
      });
    });
  }

  function card(r) {
    var photos = (r.photos || []).map(function (f) {
      return '<a href="' + esc(photoUrl(f)) + '" target="_blank" rel="noopener noreferrer"><img src="' + esc(photoUrl(f)) + '" alt="Customer photo" loading="lazy"></a>';
    }).join('');
    var btns = '';
    if (r.status !== 'approved') btns += '<button class="btn btn-primary" data-act="approved">Approve</button>';
    if (r.status !== 'rejected') btns += '<button class="btn btn-outline" data-act="rejected">' + (r.status === 'approved' ? 'Hide' : 'Reject') + '</button>';
    if ((r.photos || []).length) btns += '<button class="btn btn-outline" data-act="nophotos">Remove photos</button>';
    return '<article class="b3d-review" data-id="' + r.id + '">' +
      '<div class="b3d-review__head">' + stars(r.rating) + '<strong class="b3d-review__name">' + esc(r.name) + '</strong>' +
      '<span class="b3d-review__date">' + esc(new Date(r.created_at).toLocaleString('en-GB')) + ' &middot; written in ' + (r.lang === 'ar' ? 'Arabic' : 'English') + '</span></div>' +
      '<p class="b3d-review__text" dir="auto">' + esc(r.comment) + '</p>' +
      (photos ? '<div class="b3d-review__photos">' + photos + '</div>' : '') +
      '<details class="b3d-ra-tr"><summary>Add a translation (optional)</summary>' +
      '<label>English version<textarea rows="2" data-tr="en" maxlength="600">' + esc(r.comment_en || '') + '</textarea></label>' +
      '<label>Arabic version<textarea rows="2" data-tr="ar" maxlength="600" dir="rtl">' + esc(r.comment_ar || '') + '</textarea></label>' +
      '<button type="button" class="btn btn-outline" data-ra-translate style="margin-top:6px">Auto-translate the missing side</button>' +
      '<span class="b3d-rv-msg" data-ra-tr-msg hidden></span></details>' +
      '<div class="b3d-rv-actions" style="margin-top:12px">' + btns + '</div></article>';
  }

  function listView(list) {
    var tabs = ['pending', 'approved', 'rejected'].map(function (s) {
      return '<button type="button" class="btn ' + (s === status ? 'btn-primary' : 'btn-outline') + '" data-tab="' + s + '">' + s.charAt(0).toUpperCase() + s.slice(1) + '</button>';
    }).join('');
    host.innerHTML =
      '<div class="b3d-reviews__top"><div class="b3d-rv-actions">' + tabs + '</div>' +
      '<button type="button" class="btn btn-outline" data-ra-out>Sign out</button></div>' +
      '<p class="b3d-rv-msg" data-ra-msg role="status" hidden></p>' +
      (list.length ? '<div class="b3d-reviews__list">' + list.map(card).join('') + '</div>' : '<p class="b3d-reviews__none">No ' + status + ' reviews.</p>');
    host.querySelectorAll('[data-tab]').forEach(function (b) {
      b.addEventListener('click', function () { status = b.getAttribute('data-tab'); load(); });
    });
    host.querySelector('[data-ra-out]').addEventListener('click', function () { client.auth.signOut().then(function () { loginView(''); }); });
    // Machine translation, filling only the empty side; the admin can edit before approving.
    // Free MyMemory API — no key, adequate for short customer reviews, not used for anything else on the site.
    function translate(text, from, to) {
      var url = 'https://api.mymemory.translated.net/get?q=' + encodeURIComponent(text) + '&langpair=' + from + '|' + to;
      return fetch(url).then(function (r) { return r.json(); }).then(function (j) {
        return (j.responseData && j.responseData.translatedText) || '';
      });
    }
    host.querySelectorAll('[data-ra-translate]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var art = btn.closest('article');
        var id = parseInt(art.getAttribute('data-id'), 10);
        var r = list.filter(function (x) { return x.id === id; })[0];
        var enBox = art.querySelector('[data-tr="en"]');
        var arBox = art.querySelector('[data-tr="ar"]');
        var msg = art.querySelector('[data-ra-tr-msg]');
        var original = r.lang === 'ar' ? arBox : enBox;
        if (!original.value) original.value = r.comment;
        var target = r.lang === 'ar' ? enBox : arBox;
        var fromTo = r.lang === 'ar' ? ['ar', 'en'] : ['en', 'ar'];
        btn.disabled = true; msg.hidden = false; msg.textContent = 'Translating…'; msg.className = 'b3d-rv-msg';
        translate(original.value, fromTo[0], fromTo[1]).then(function (out) {
          btn.disabled = false;
          if (out) { target.value = out; msg.textContent = 'Draft added — check it before approving.'; }
          else { msg.textContent = 'Could not translate automatically — please type it in.'; msg.className = 'b3d-rv-msg is-err'; }
        }).catch(function () {
          btn.disabled = false; msg.textContent = 'Could not translate automatically — please type it in.'; msg.className = 'b3d-rv-msg is-err';
        });
      });
    });
    host.querySelectorAll('[data-act]').forEach(function (b) {
      b.addEventListener('click', function () {
        var art = b.closest('article');
        var id = parseInt(art.getAttribute('data-id'), 10);
        var act = b.getAttribute('data-act');
        var args = { p_id: id, p_status: null, p_comment_en: art.querySelector('[data-tr="en"]').value, p_comment_ar: art.querySelector('[data-tr="ar"]').value, p_clear_photos: act === 'nophotos' };
        if (act === 'approved' || act === 'rejected') args.p_status = act;
        b.disabled = true;
        client.rpc('admin_set_review', args).then(function (res) {
          if (res.error) { var m = host.querySelector('[data-ra-msg]'); m.textContent = 'Could not save: ' + res.error.message; m.className = 'b3d-rv-msg is-err'; m.hidden = false; b.disabled = false; return; }
          load();
        });
      });
    });
  }

  function load() {
    client.rpc('admin_list_reviews', { p_status: status }).then(function (res) {
      if (res.error) {
        client.auth.getSession().then(function (s) {
          if (s.data && s.data.session) {
            host.innerHTML = '<p class="b3d-rv-msg is-err">This account is not allowed to approve reviews.</p><div class="b3d-rv-actions"><button class="btn btn-outline" data-ra-out>Sign out</button></div>';
            host.querySelector('[data-ra-out]').addEventListener('click', function () { client.auth.signOut().then(function () { loginView(''); }); });
          } else { loginView(''); }
        });
        return;
      }
      listView(res.data || []);
    });
  }

  function start() {
    client.auth.getSession().then(function (s) {
      if (s.data && s.data.session) load(); else loginView('');
    });
  }

  if (!CFG || !CFG.url || !CFG.anonKey) { host.textContent = 'Not configured.'; return; }
  loadSdk(function () {
    if (!window.supabase || !window.supabase.createClient) { host.textContent = 'Could not load. Please try again.'; return; }
    client = window.supabase.createClient(CFG.url, CFG.anonKey);
    start();
  });
})();
