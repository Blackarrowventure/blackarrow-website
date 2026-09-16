(function () {
  'use strict';

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
      if (resetForm) {
        resetForm.addEventListener('submit', function (e) {
          e.preventDefault();
          var err = document.getElementById('reset-error');
          var success = document.getElementById('reset-success');
          err.hidden = true;
          success.hidden = true;
          window.BlackArrow3DAuth.resetPassword(document.getElementById('reset-email').value).then(function () {
            success.hidden = false;
          }).catch(function (error) {
            err.textContent = error.message;
            err.hidden = false;
          });
        });
      }

      if (newpassForm) {
        newpassForm.addEventListener('submit', function (e) {
          e.preventDefault();
          var err = document.getElementById('newpass-error');
          err.hidden = true;
          window.BlackArrow3DAuth.updatePassword(document.getElementById('newpass-password').value).then(function () {
            location.hash = '';
            location.reload();
          }).catch(function (error) {
            err.textContent = error.message;
            err.hidden = false;
          });
        });
      }

      var detailsForm = document.getElementById('b3d-details-form');
      if (detailsForm) {
        detailsForm.addEventListener('submit', function (e) {
          e.preventDefault();
          if (!currentUser) return;
          window.BlackArrow3DAuth.saveProfile(currentUser.id, {
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
      }

      document.getElementById('b3d-signout-btn').addEventListener('click', function () {
        window.BlackArrow3DAuth.signOut();
      });
    });
  });
})();
