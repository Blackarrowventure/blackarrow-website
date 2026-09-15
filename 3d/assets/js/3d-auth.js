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

  function onAuthChange(fn) {
    if (!ready || !client) { fn(null); return; }
    client.auth.getSession().then(function (res) {
      fn(res.data && res.data.session ? res.data.session.user : null);
    });
    client.auth.onAuthStateChange(function (_event, session) {
      fn(session ? session.user : null);
    });
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
    return client.auth.signUp({ email: email, password: password }).then(function (res) {
      if (res.error) throw res.error;
      var user = res.data && res.data.user;
      if (user) return upsertCustomerRow(user, extra).then(function () { return res; });
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

  window.BlackArrow3DAuth = {
    isConfigured: function () { return !!(CONFIG && CONFIG.url && CONFIG.anonKey); },
    init: init,
    onAuthChange: onAuthChange,
    signUp: signUp,
    signIn: signIn,
    signOut: signOut,
    getProfile: getProfile,
    saveProfile: saveProfile
  };
})();
