/* Black Arrow 3D — Arrowhead Rewards. The browser never talks to the CRM:
   it asks the site's own server (/api/rewards/*), which checks the signed-in
   website account and does the CRM call itself. Used by the rewards page
   (below) and by the cart (BlackArrow3DRewards.fetchMe / redeemForOrder). */
(function () {
  'use strict';

  function withToken(fn) {
    var auth = window.BlackArrow3DAuth;
    if (!auth || !auth.getAccessToken) return Promise.resolve(null);
    return auth.getAccessToken().then(function (token) { return token ? fn(token) : null; });
  }

  // -> { signedIn, needsPhone?, member?: {name,tier,balance,memberSince}, freeDelivery, minRedeem } | null
  function fetchMe() {
    return withToken(function (token) {
      return fetch('/api/rewards/me/', { headers: { Authorization: 'Bearer ' + token }, cache: 'no-store' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .catch(function () { return null; });
    });
  }

  // Bank-transfer orders: spend balance before the order is sent.
  // Resolves the SAR actually used; rejects if it could not be used.
  function redeemForOrder(orderId, amount) {
    return withToken(function (token) {
      return fetch('/api/rewards/redeem/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token },
        body: JSON.stringify({ orderId: orderId, amount: amount })
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (d) {
          if (!r.ok || typeof d.used !== 'number') throw new Error(d.error || 'redeem_failed');
          return d.used;
        });
      });
    }).then(function (used) {
      if (used == null) throw new Error('signed_out');
      return used;
    });
  }

  window.BlackArrow3DRewards = { fetchMe: fetchMe, redeemForOrder: redeemForOrder };

  /* --- Rewards page: only runs where its own markup exists. --- */
  document.addEventListener('DOMContentLoaded', function () {
    var liveSection = document.getElementById('b3d-rwd-live');
    var panelSignedOut = document.getElementById('b3d-rwd-panel-signedout');
    var panelNeedsPhone = document.getElementById('b3d-rwd-panel-needsphone');
    var panelError = document.getElementById('b3d-rwd-panel-error');
    if (!liveSection) return;

    function show(el) {
      [liveSection, panelSignedOut, panelNeedsPhone, panelError].forEach(function (p) {
        if (p) p.hidden = (p !== el);
      });
    }

    function renderCard(member) {
      var card = liveSection.querySelector('.b3d-rwd-card');
      card.className = 'b3d-rwd-card b3d-rwd-card--' + String(member.tier || 'Silver').toLowerCase();
      liveSection.querySelector('[data-rwd-name]').textContent = member.name;
      liveSection.querySelector('[data-rwd-tier]').textContent = member.tier;
      var since = member.memberSince ? new Date(member.memberSince) : null;
      liveSection.querySelector('[data-rwd-since]').textContent = since
        ? since.toLocaleDateString(document.documentElement.lang === 'ar' ? 'ar-SA' : 'en-GB', { year: 'numeric', month: 'short' })
        : '';
      liveSection.querySelector('[data-rwd-balance]').textContent = Number(member.balance || 0).toFixed(2);
      show(liveSection);
    }

    function load() {
      return fetchMe().then(function (me) {
        if (!me) { show(panelSignedOut); return; }
        if (!me.signedIn) { show(panelSignedOut); return; }
        if (me.needsPhone) { show(panelNeedsPhone); return; }
        if (me.member) { renderCard(me.member); return; }
        show(panelError);
      });
    }

    var currentUser = null;
    var auth = window.BlackArrow3DAuth;
    if (!auth || !auth.isConfigured()) { show(panelSignedOut); return; }
    auth.init(function (ok) {
      if (!ok) { show(panelSignedOut); return; }
      auth.onAuthChange(function (user) {
        currentUser = user;
        if (!user) { show(panelSignedOut); return; }
        load().catch(function () { show(panelError); });
      });
    });

    var joinForm = document.getElementById('b3d-rwd-join-form');
    if (joinForm) {
      joinForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var phone = document.getElementById('rwd-join-phone').value.trim();
        var err = document.getElementById('rwd-join-error');
        var btn = joinForm.querySelector('button[type="submit"]');
        if (err) err.hidden = true;
        if (!phone || !currentUser) return;
        btn.disabled = true;
        auth.saveProfile(currentUser.id, { phone: phone }).then(load).catch(function () {
          if (err) err.hidden = false;
        }).then(function () { btn.disabled = false; });
      });
    }
  });
})();
