/* Google Tag Manager bootstrap, moved out of an inline <script> (as the
   service worker shim once was) because the site's Content-Security-Policy
   has no 'unsafe-inline' for script-src, so an inline script never executes.

   Loaded late on purpose (26 Nov 2026, PageSpeed): GTM + the GA4 tag are ~300 KB of
   script, three quarters of everything the store pages download, and they used to compete
   with the page's own first paint. They now start on the visitor's first scroll, tap,
   click or key press, or 4 s after the page has finished loading, whichever comes first.
   Anything pushed to dataLayer before that (e.g. add_to_cart) waits in the queue and is
   sent when GTM loads. */
(function (w, d, l, i) {
  w[l] = w[l] || [];
  var started = false;
  var events = ['scroll', 'pointerdown', 'keydown', 'touchstart'];
  function start() {
    if (started) return;
    started = true;
    events.forEach(function (e) { w.removeEventListener(e, start, { passive: true }); });
    w[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var f = d.getElementsByTagName('script')[0],
      j = d.createElement('script'),
      dl = l != 'dataLayer' ? '&l=' + l : '';
    j.async = true;
    j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
    f.parentNode.insertBefore(j, f);
  }
  // Conversion pages load it straight away, so a customer who closes the page within a few seconds
  // is still counted: the order confirmation after Paymob / Tabby (?paid= / ?tabby=) and the
  // contact-form thank-you page.
  if (/[?&](paid|tabby)=/.test(w.location.search) || /thank-you/.test(w.location.pathname)) { start(); return; }
  events.forEach(function (e) { w.addEventListener(e, start, { passive: true }); });
  function later() { setTimeout(start, 4000); }
  if (d.readyState === 'complete') later();
  else w.addEventListener('load', later);
})(window, document, 'dataLayer', 'GTM-N65CG27H');
