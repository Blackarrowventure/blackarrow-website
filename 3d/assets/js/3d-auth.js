/* Black Arrow 3D — customer login + CRM via Supabase.
   Auth is inert until window.BLACK_ARROW_SUPABASE_CONFIG is filled in
   (see 3d-supabase-config.js) — until then every page using this shows a
   clear "not connected yet" state instead of a broken form.

   On sign-up, we also write a row into the public.customers table (the
   CRM record) alongside the auth.users entry Supabase creates for login.
   That table and its Row Level Security policies must be created once in
   the Supabase SQL editor — see the SQL handed to the site owner
   alongside this file; nothing here can create tables itself (the
   publishable key intentionally can't run schema changes). */
(function () {
  'use strict';

  var CONFIG = window.BLACK_ARROW_SUPABASE_CONFIG || null;
  var ready = false;
  var client = null;

  function loadSupabaseSdk(cb) {
    if (window.supabase && window.supabase.createClient) { cb(); return; }
    // Called once: on load, on error, or after 12s if the CDN never answers (a hung
    // request would otherwise leave the account page blank).
    var done = false;
    var finish = function () { if (!done) { done = true; cb(); } };
    setTimeout(finish, 12000);
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.118.0';
    script.onload = finish;
    script.onerror = finish;
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

  function onAuthChange(fn) {
    if (!ready || !client) { fn(null); return; }
    client.auth.getSession().then(function (res) {
      var user = res.data && res.data.session ? res.data.session.user : null;
      if (user) finishSignupProfile(user);
      fn(user);
    });
    client.auth.onAuthStateChange(function (_event, session) {
      if (session && session.user) finishSignupProfile(session.user);
      fn(session ? session.user : null);
    });
  }

  // "05XXXXXXXX", "5XXXXXXXX", "+966 5X...", "009665X..." -> valid Saudi mobile?
  function validSaudiMobile(p) {
    var d = String(p || '').replace(/[^0-9]/g, '');
    if (d.indexOf('00') === 0) d = d.slice(2);
    if (d.length === 10 && d.indexOf('05') === 0) d = '966' + d.slice(1);
    if (d.length === 9 && d.charAt(0) === '5') d = '966' + d;
    return /^9665[0-9]{8}$/.test(d);
  }

  // Sign-up details (name, phone, date of birth) travel on the account itself
  // (user_metadata), because with email confirmation there is no session at
  // sign-up and the customer row can't be written yet. On the first signed-in
  // visit they fill the customer record (blanks only, never overwriting later
  // edits) and the date of birth goes to the rewards card for the birthday
  // reward. Runs once per account (profile_saved).
  var profileRunning = {};
  function finishSignupProfile(user) {
    var meta = (user && user.user_metadata) || {};
    if (!user || meta.profile_saved || profileRunning[user.id]) return;
    if (!meta.full_name && !meta.phone && !meta.dob) return;
    profileRunning[user.id] = true;
    getProfile(user.id).then(function (p) {
      var row = { id: user.id, email: user.email, source: '3d-site' };
      if (meta.full_name && !(p && p.name)) row.name = meta.full_name;
      if (meta.phone && !(p && p.phone)) row.phone = meta.phone;
      return client.from('customers').upsert(row);
    }).then(function (res) {
      if (res && res.error) throw res.error;
      if (!meta.dob) return null;
      return getAccessToken().then(function (token) {
        if (!token) return null;
        return fetch('/api/rewards/me/', {
          method: 'POST',
          headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
          body: JSON.stringify({ dob: meta.dob })
        }).catch(function () { return null; });
      });
    }).then(function () {
      return client.auth.updateUser({ data: { profile_saved: true } });
    }).catch(function (e) {
      console.warn('Black Arrow 3D: could not save sign-up details yet', e);
    }).then(function () { profileRunning[user.id] = false; });
  }

  function upsertCustomerRow(user, extra) {
    return client.from('customers').upsert({
      id: user.id,
      email: user.email,
      name: (extra && extra.name) || null,
      phone: (extra && extra.phone) || null,
      source: '3d-site'
    }).then(function (res) {
      if (res.error) {
        // Don't fail the whole sign-up over a CRM write hiccup (e.g. the
        // table not existing yet) -- the account itself still works.
        console.warn('Black Arrow 3D: could not write customer record', res.error);
      }
      return res;
    });
  }

  function signUp(email, password, extra) {
    var meta = {};
    if (extra && extra.name) meta.full_name = extra.name;
    if (extra && extra.phone) meta.phone = extra.phone;
    if (extra && extra.dob) meta.dob = extra.dob;
    return client.auth.signUp({ email: email, password: password, options: { data: meta } }).then(function (res) {
      if (res.error) throw res.error;
      var user = res.data && res.data.user;
      // Supabase hides "this email already has an account": it answers with a user that has no
      // identities and sends no email. Say so, instead of "check your email" for a mail that never comes.
      if (user && !res.data.session && Array.isArray(user.identities) && user.identities.length === 0) {
        throw new Error('User already registered');
      }
      // Only possible when there is already a session (email confirmation off);
      // otherwise finishSignupProfile() writes the record on the first sign-in.
      if (user && res.data.session) return upsertCustomerRow(user, extra).then(function () { return res; });
      return res;
    });
  }

  function signIn(email, password) {
    return client.auth.signInWithPassword({ email: email, password: password }).then(function (res) {
      if (res.error) throw res.error;
      return res;
    });
  }

  function signOut() {
    return client.auth.signOut();
  }

  function resetPassword(email) {
    return client.auth.resetPasswordForEmail(email, {
      redirectTo: window.location.origin + '/3d/account/'
    }).then(function (res) {
      if (res.error) throw res.error;
      return res;
    });
  }

  // Sends the sign-up confirmation email again (for customers who never got it or lost it).
  function resendConfirmation(email) {
    return client.auth.resend({ type: 'signup', email: email, options: { emailRedirectTo: window.location.origin + '/3d/account/' } }).then(function (res) {
      if (res.error) throw res.error;
      return res;
    });
  }

  function updatePassword(newPassword) {
    return client.auth.updateUser({ password: newPassword }).then(function (res) {
      if (res.error) throw res.error;
      return res;
    });
  }

  // Short-lived token the site's own server uses to check who is signed in
  // (Black Arrow Loyalty Rewards); never sent anywhere else.
  function getAccessToken() {
    if (!ready || !client) return Promise.resolve(null);
    return client.auth.getSession().then(function (res) {
      return res.data && res.data.session ? res.data.session.access_token : null;
    }).catch(function () { return null; });
  }

  function getProfile(userId) {
    if (!ready || !client) return Promise.resolve(null);
    return client.from('customers').select('name, phone, last_address').eq('id', userId).single().then(function (res) {
      return res.error ? null : res.data;
    }).catch(function () { return null; });
  }

  function saveProfile(userId, fields) {
    if (!ready || !client) return Promise.resolve();
    var row = { id: userId };
    if (fields.name != null) row.name = fields.name;
    if (fields.phone != null) row.phone = fields.phone;
    if (fields.last_address != null) row.last_address = fields.last_address;
    return client.from('customers').upsert(row).then(function (res) {
      if (res.error) console.warn('Black Arrow 3D: could not save profile', res.error);
      return res;
    });
  }

  // Is the signed-in user allowed to approve reviews? (the database decides;
  // ordinary customers get false and never see anything about it)
  function reviewAdminInfo() {
    if (!ready || !client) return Promise.resolve({ isAdmin: false, pending: 0 });
    return client.rpc('is_review_admin').then(function (res) {
      if (res.error || res.data !== true) return { isAdmin: false, pending: 0 };
      return client.rpc('admin_list_reviews', { p_status: 'pending' }).then(function (r2) {
        return { isAdmin: true, pending: (r2.data || []).length };
      });
    }).catch(function () { return { isAdmin: false, pending: 0 }; });
  }

  window.BlackArrow3DAuth = {
    isConfigured: function () { return !!(CONFIG && CONFIG.url && CONFIG.anonKey); },
    init: init,
    onAuthChange: onAuthChange,
    signUp: signUp,
    signIn: signIn,
    signOut: signOut,
    resetPassword: resetPassword,
    resendConfirmation: resendConfirmation,
    updatePassword: updatePassword,
    getAccessToken: getAccessToken,
    getProfile: getProfile,
    saveProfile: saveProfile,
    reviewAdminInfo: reviewAdminInfo,
    validSaudiMobile: validSaudiMobile
  };
})();
