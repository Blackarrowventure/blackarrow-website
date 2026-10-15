/* Black Arrow 3D — Arrowhead Rewards: talks to the BAV CRM's Supabase
   project (separate from the website's own account project) through the
   three narrow, anon-callable RPCs it exposes: bav3d_loyalty_get (read a
   member's own tier/balance by phone), bav3d_loyalty_signup (join, idempotent
   — safe to call again for an already-enrolled phone, used here to
   auto-enroll existing website accounts the first time they open this
   page), and bav3d_loyalty_record_order / bav3d_loyalty_redeem (not called
   from this file yet — checkout doesn't award or spend balance until the
   order flow is wired up separately).

   The CRM table itself is CEO-only at the database (see migration 0143) —
   every read/write here goes through a function that runs as its owner, so
   this works with no login into the CRM at all; the only thing identifying
   "whose balance" is the phone number the customer already typed into their
   Black Arrow 3D account. */
(function () {
  'use strict';

  var CONFIG = window.BLACK_ARROW_CRM_CONFIG || null;
  var client = null;
  var ready = false;

  function loadSupabaseSdk(cb) {
    if (window.supabase && window.supabase.createClient) { cb(); return; }
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
    script.onload = function () { cb(); };
    script.onerror = function () { cb(); };
    document.head.appendChild(script);
  }

  function init(cb) {
    if (!CONFIG || !CONFIG.url || !CONFIG.anonKey) { cb(false); return; }
    loadSupabaseSdk(function () {
      try {
        if (!window.supabase || !window.supabase.createClient) { cb(false); return; }
        client = window.supabase.createClient(CONFIG.url, CONFIG.anonKey);
        ready = true;
        cb(true);
      } catch (e) {
        cb(false);
      }
    });
  }

  function getMember(phone) {
    if (!ready) return Promise.resolve(null);
    return client.rpc('bav3d_loyalty_get', { p_phone: phone }).then(function (res) {
      var row = res.data && res.data[0];
      if (res.error || !row || !row.found) return null;
      return row;
    }).catch(function () { return null; });
  }

  function enroll(fullName, phone, dateOfBirth) {
    return client.rpc('bav3d_loyalty_signup', {
      p_full_name: fullName,
      p_phone: phone,
      p_date_of_birth: dateOfBirth || null
    }).then(function (res) {
      if (res.error) throw res.error;
      return res.data;
    });
  }

  window.BlackArrow3DRewards = {
    isConfigured: function () { return !!(CONFIG && CONFIG.url && CONFIG.anonKey); },
    init: init,
    getMember: getMember,
    enroll: enroll
  };

  /* --- Page wiring: only runs where the rewards page's own markup exists. --- */
  document.addEventListener('DOMContentLoaded', function () {
    var liveSection = document.getElementById('b3d-rwd-live');
    var panelSignedOut = document.getElementById('b3d-rwd-panel-signedout');
    var panelNeedsPhone = document.getElementById('b3d-rwd-panel-needsphone');
    var panelError = document.getElementById('b3d-rwd-panel-error');
    if (!liveSection) return; // not the rewards page

    function show(el) {
      [liveSection, panelSignedOut, panelNeedsPhone, panelError].forEach(function (p) {
        if (p) p.hidden = (p !== el);
      });
    }

    function renderCard(member) {
      var tierClass = 'b3d-rwd-card--' + member.tier.toLowerCase();
      var card = liveSection.querySelector('.b3d-rwd-card');
      card.className = 'b3d-rwd-card ' + tierClass;
      liveSection.querySelector('[data-rwd-name]').textContent = member.full_name;
      liveSection.querySelector('[data-rwd-tier]').textContent = member.tier;
      var since = member.member_since ? new Date(member.member_since) : null;
      liveSection.querySelector('[data-rwd-since]').textContent = since
        ? since.toLocaleDateString(document.documentElement.lang === 'ar' ? 'ar-SA' : 'en-GB', { year: 'numeric', month: 'short' })
        : '';
      liveSection.querySelector('[data-rwd-balance]').textContent = Number(member.reward_balance || 0).toFixed(2);
      show(liveSection);
    }

    var currentUser = null;

    function tryEnrollAndShow(user, profile) {
      var phone = profile && profile.phone;
      var name = (profile && profile.name) || (user.email ? user.email.split('@')[0] : 'Member');
      if (!phone) { show(panelNeedsPhone); return; }
      window.BlackArrow3DRewards.getMember(phone).then(function (member) {
        if (member) { renderCard(member); return; }
        // First visit with a phone on file: auto-enroll (idempotent on the
        // database side, so this is safe even if called more than once).
        return window.BlackArrow3DRewards.enroll(name, phone).then(function () {
          return window.BlackArrow3DRewards.getMember(phone);
        }).then(function (m) {
          if (m) renderCard(m); else show(panelError);
        });
      }).catch(function () { show(panelError); });
    }

    window.BlackArrow3DRewards.init(function (crmOk) {
      if (!crmOk || !window.BlackArrow3DAuth || !window.BlackArrow3DAuth.isConfigured()) {
        show(panelSignedOut);
        return;
      }
      window.BlackArrow3DAuth.init(function (authOk) {
        if (!authOk) { show(panelSignedOut); return; }
        window.BlackArrow3DAuth.onAuthChange(function (user) {
          currentUser = user;
          if (!user) { show(panelSignedOut); return; }
          window.BlackArrow3DAuth.getProfile(user.id).then(function (profile) {
            tryEnrollAndShow(user, profile);
          });
        });
      });
    });

    var joinForm = document.getElementById('b3d-rwd-join-form');
    if (joinForm) {
      joinForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var phoneInput = document.getElementById('rwd-join-phone');
        var err = document.getElementById('rwd-join-error');
        var btn = joinForm.querySelector('button[type="submit"]');
        var phone = phoneInput.value.trim();
        if (err) err.hidden = true;
        if (!phone || !currentUser) return;
        btn.disabled = true;
        window.BlackArrow3DAuth.saveProfile(currentUser.id, { phone: phone }).then(function () {
          return window.BlackArrow3DAuth.getProfile(currentUser.id);
        }).then(function (profile) {
          tryEnrollAndShow(currentUser, profile);
        }).catch(function () {
          if (err) { err.hidden = false; }
        }).then(function () { btn.disabled = false; });
      });
    }
  });
})();
