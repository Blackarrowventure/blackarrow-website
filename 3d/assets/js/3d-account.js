(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var notConfigured = document.getElementById('b3d-auth-notconfigured');
    var signedOut = document.getElementById('b3d-auth-signedout');
    var signedIn = document.getElementById('b3d-auth-signedin');

    if (!window.BlackArrow3DAuth || !window.BlackArrow3DAuth.isConfigured()) {
      notConfigured.hidden = false;
      return;
    }

    window.BlackArrow3DAuth.init(function (ok) {
      if (!ok) { notConfigured.hidden = false; return; }

      window.BlackArrow3DAuth.onAuthChange(function (user) {
        if (user) {
          signedOut.hidden = true;
          signedIn.hidden = false;
          document.getElementById('b3d-account-email').textContent = user.email;
        } else {
          signedOut.hidden = false;
          signedIn.hidden = true;
        }
      });

      var tabs = document.querySelectorAll('[data-auth-tab]');
      var signinForm = document.getElementById('b3d-signin-form');
      var signupForm = document.getElementById('b3d-signup-form');
      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          tabs.forEach(function (t) { t.setAttribute('aria-pressed', 'false'); });
          tab.setAttribute('aria-pressed', 'true');
          var isSignin = tab.getAttribute('data-auth-tab') === 'signin';
          signinForm.hidden = !isSignin;
          signupForm.hidden = isSignin;
        });
      });

      signinForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var err = document.getElementById('signin-error');
        err.hidden = true;
        window.BlackArrow3DAuth.signIn(
          document.getElementById('signin-email').value,
          document.getElementById('signin-password').value
        ).catch(function (error) {
          err.textContent = error.message;
          err.hidden = false;
        });
      });

      signupForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var err = document.getElementById('signup-error');
        err.hidden = true;
        window.BlackArrow3DAuth.signUp(
          document.getElementById('signup-email').value,
          document.getElementById('signup-password').value,
          {
            name: document.getElementById('signup-name').value,
            phone: document.getElementById('signup-phone').value
          }
        ).catch(function (error) {
          err.textContent = error.message;
          err.hidden = false;
        });
      });

      document.getElementById('b3d-signout-btn').addEventListener('click', function () {
        window.BlackArrow3DAuth.signOut();
      });
    });
  });
})();
