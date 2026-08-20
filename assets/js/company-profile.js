/* ==============================================
   BLACK ARROW VENTURE
   company-profile.js — the little that page needs

   company-profile.html deliberately does not load app.js or styles.css;
   it keeps its own inline stylesheet and pre-rebrand palette by decision,
   not by oversight. That means the shared footer-year helper never runs
   there, so it runs from here instead.

   This was an inline <script> until the Content-Security-Policy went in.
   ============================================== */

'use strict';

document.querySelectorAll('[data-year]').forEach(function (el) {
  el.textContent = String(new Date().getFullYear());
});
