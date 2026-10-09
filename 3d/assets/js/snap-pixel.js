/* Snap Pixel — base install + page view.
   Add-to-cart, start-checkout and purchase events are fired from
   3d-store.js at the real moments those happen (see pushSnapEvent). */
(function (e, t, n) {
  if (e.snaptr) return;
  var a = e.snaptr = function () {
    a.handleRequest ? a.handleRequest.apply(a, arguments) : a.queue.push(arguments);
  };
  a.queue = [];
  var s = 'script';
  var r = t.createElement(s);
  r.async = true;
  r.src = n;
  var u = t.getElementsByTagName(s)[0];
  u.parentNode.insertBefore(r, u);
})(window, document, 'https://sc-static.net/scevent.min.js');

snaptr('init', '7b499b3a-0f23-49e0-a8e1-f513ab5f10e7');
snaptr('track', 'PAGE_VIEW');
