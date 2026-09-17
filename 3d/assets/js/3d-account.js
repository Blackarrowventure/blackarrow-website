(function () {
  'use strict';

  /* Supabase's own anti-abuse cooldown (not a site bug) returns a raw
     message like "For security purposes, you can only request this
     after 43 seconds." if the same form is submitted twice in a row
     (e.g. a double-click, or retrying immediately after a typo). Two
     things caused this to bite real visitors: (1) no submit button was
     ever disabled while a request was in flight, so a double-click or
     slow network fired signUp()/signIn() twice, and the second call is
     what actually gets rate-limited; (2) the raw Supabase string was
     shown as-is, reading like a broken/scary error instead of "wait a
     moment". Fixed below by guarding every form against a second
     submit while one is already running, and by turning the rate-limit
     message into a plain countdown instead of technical text. */

  function isRateLimitMessage(message) {
    return /security purposes|rate limit|too many requests/i.test(message || '');
  }

  function secondsFromMessage(message) {
    var m = (message || '').match(/(\d+)\s*second/);
    return m ? parseInt(m[1], 10) : 30;
  }

  function showError(errEl, error) {
    var message = (error && error.message) || 'Something went wrong. Please try again.';
    if (!isRateLimitMessage(message)) {
      errEl.textContent = message;
      errEl.hidden = false;
      return;
    }
    var secs = secondsFromMessage(message);
    errEl.hidden = false;
    (function tick() {
      errEl.textContent = 'Please wait ' + secs + 's before trying again — this is a short security cooldown, not a problem with your account.';
      secs -= 1;
      if (secs >= 0) { setTimeout(tick, 1000); } else { errEl.hidden = true; }
    })();
  }

  /* Wraps a form's submit handler so a second submit (double-click,
     double-tap, Enter held down, slow network + impatient retry) is
     ignored outright instead of firing a second real request, and
     disables the submit button with a busy label while the request is
     in flight. `action` returns the promise from the Supabase call. */
  function guardedSubmit(form, action) {
    if (!form) return;
    var busy = false;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (busy) return;
      busy = true;
      var btn = form.querySelector('button[type="submit"]');
      var originalLabel = btn ? btn.textContent : null;
      if (btn) { btn.disabled = true; btn.textContent = '...'; }
      action().catch(function () {}).then(function () {
        busy = false;
        if (btn) { btn.disabled = false; btn.textContent = originalLabel; }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var notConfigured = document.getElementById('b3d-auth-notconfigured');
    var signedOut = document.getElementById('b3d-auth-signedout');
    var signedIn = document.getElementById('b3d-auth-signedin');
    var newpassForm = document.getElementById('b3d-newpass-form');

    if (!window.BlackArrow3DAuth || !window.BlackArrow3DAuth.isConfigured()) {
      notConfigured.hidden = false;
      return;
    }

    // Supabase sends the visitor back here with #type=recovery in the URL
    // after they click a password-reset email link. Show the "set a new
    // password" form instead of the normal sign-in/sign-up screen.
    var isRecovery = location.hash.indexOf('type=recovery') !== -1;

    var currentUser = null;

    window.BlackArrow3DAuth.init(function (ok) {
      if (!ok) { notConfigured.hidden = false; return; }

      window.BlackArrow3DAuth.onAuthChange(function (user) {
        currentUser = user;
        if (isRecovery) {
          signedOut.hidden = true;
          signedIn.hidden = true;
          newpassForm.hidden = false;
          return;
        }
        if (user) {
          signedOut.hidden = true;
          signedIn.hidden = false;
          document.getElementById('b3d-account-email').textContent = user.email;

          var verifyNotice = document.getElementById('b3d-verify-notice');
          if (verifyNotice) verifyNotice.hidden = !!user.email_confirmed_at;

          var savedPanel = document.getElementById('b3d-saved-products-panel');
          if (savedPanel && window.BlackArrow3D) window.BlackArrow3D.renderWishlistPanel(savedPanel);

          window.BlackArrow3DAuth.getProfile(user.id).then(function (profile) {
            if (!profile) return;
            var nameField = document.getElementById('details-name');
            var phoneField = document.getElementById('details-phone');
            if (nameField && profile.name) nameField.value = profile.name;
            if (phoneField && profile.phone) phoneField.value = profile.phone;
          });
        } else {
          signedOut.hidden = false;
          signedIn.hidden = true;
        }
      });

      var tabs = document.querySelectorAll('[data-auth-tab]');
      var signinForm = document.getElementById('b3d-signin-form');
      var signupForm = document.getElementById('b3d-signup-form');
      var resetForm = document.getElementById('b3d-reset-form');
      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          tabs.forEach(function (t) { t.setAttribute('aria-pressed', 'false'); });
          tab.setAttribute('aria-pressed', 'true');
          var isSignin = tab.getAttribute('data-auth-tab') === 'signin';
          signinForm.hidden = !isSignin;
          signupForm.hidden = isSignin;
          resetForm.hidden = true;
        });
      });

      guardedSubmit(signinForm, function () {
        var err = document.getElementById('signin-error');
        err.hidden = true;
        return window.BlackArrow3DAuth.signIn(
          document.getElementById('signin-email').value,
          document.getElementById('signin-password').value
        ).catch(function (error) { showError(err, error); throw error; });
      });

      guardedSubmit(signupForm, function () {
        var err = document.getElementById('signup-error');
        var success = document.getElementById('signup-success');
        err.hidden = true;
        success.hidden = true;
        return window.BlackArrow3DAuth.signUp(
          document.getElementById('signup-email').value,
          document.getElementById('signup-password').value,
          {
            name: document.getElementById('signup-name').value,
            phone: document.getElementById('signup-phone').value
          }
        ).then(function (res) {
          // Email confirmation is on by default: a successful signUp() call
          // returns a user but no session until they click the confirmation
          // link, so the page would otherwise just sit there looking broken.
          var user = res && res.data && res.data.user;
          var session = res && res.data && res.data.session;
          if (user && !session) {
            signupForm.reset();
            success.hidden = false;
          }
        }).catch(function (error) { showError(err, error); throw error; });
      });

      var forgotLink = document.getElementById('b3d-forgot-link');
      if (forgotLink) {
        forgotLink.addEventListener('click', function () {
          signinForm.hidden = true;
          signupForm.hidden = true;
          resetForm.hidden = false;
        });
      }
      var resetCancel = document.getElementById('b3d-reset-cancel');
      if (resetCancel) {
        resetCancel.addEventListener('click', function () {
          resetForm.hidden = true;
          signinForm.hidden = false;
        });
      }
      guardedSubmit(resetForm, function () {
        var err = document.getElementById('reset-error');
        var success = document.getElementById('reset-success');
        err.hidden = true;
        success.hidden = true;
        return window.BlackArrow3DAuth.resetPassword(document.getElementById('reset-email').value).then(function () {
          success.hidden = false;
        }).catch(function (error) { showError(err, error); throw error; });
      });

      guardedSubmit(newpassForm, function () {
        var err = document.getElementById('newpass-error');
        err.hidden = true;
        return window.BlackArrow3DAuth.updatePassword(document.getElementById('newpass-password').value).then(function () {
          location.hash = '';
          location.reload();
        }).catch(function (error) { showError(err, error); throw error; });
      });

      var detailsForm = document.getElementById('b3d-details-form');
      guardedSubmit(detailsForm, function () {
        if (!currentUser) return Promise.resolve();
        return window.BlackArrow3DAuth.saveProfile(currentUser.id, {
          name: document.getElementById('details-name').value,
          phone: document.getElementById('details-phone').value
        }).then(function () {
          var success = document.getElementById('details-success');
          if (success) {
            success.hidden = false;
            setTimeout(function () { success.hidden = true; }, 2500);
          }
        });
      });

      document.getElementById('b3d-signout-btn').addEventListener('click', function () {
        window.BlackArrow3DAuth.signOut();
      });
    });
  });
})();
