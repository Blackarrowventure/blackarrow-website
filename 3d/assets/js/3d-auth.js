/* Black Arrow 3D — customer login via Firebase Authentication (free tier).
   Nothing here talks to a payment gateway or CRM. Auth is inert until
   window.BLACK_ARROW_FIREBASE_CONFIG is filled in with a real Firebase
   project's config (see 3d/account/index.html for where that goes) —
   until then every page using this shows a clear "not connected yet"
   state instead of a broken form. */
(function () {
  'use strict';

  var CONFIG = window.BLACK_ARROW_FIREBASE_CONFIG || null;
  var firebaseReady = false;
  var auth = null;

  function loadFirebaseSdk(cb) {
    if (window.firebase && window.firebase.apps) { cb(); return; }
    var appScript = document.createElement('script');
    appScript.src = 'https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js';
    appScript.onload = function () {
      var authScript = document.createElement('script');
      authScript.src = 'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth-compat.js';
      authScript.onload = cb;
      document.head.appendChild(authScript);
    };
    document.head.appendChild(appScript);
  }

  function init(cb) {
    if (!CONFIG) { cb(false); return; }
    loadFirebaseSdk(function () {
      try {
        if (!window.firebase.apps.length) window.firebase.initializeApp(CONFIG);
        auth = window.firebase.auth();
        firebaseReady = true;
        cb(true);
      } catch (e) {
        cb(false);
      }
    });
  }

  function onAuthChange(fn) {
    if (!firebaseReady || !auth) { fn(null); return; }
    auth.onAuthStateChanged(fn);
  }

  function signUp(email, password) {
    return auth.createUserWithEmailAndPassword(email, password);
  }

  function signIn(email, password) {
    return auth.signInWithEmailAndPassword(email, password);
  }

  function signOut() {
    return auth.signOut();
  }

  window.BlackArrow3DAuth = {
    isConfigured: function () { return !!CONFIG; },
    init: init,
    onAuthChange: onAuthChange,
    signUp: signUp,
    signIn: signIn,
    signOut: signOut
  };
})();
