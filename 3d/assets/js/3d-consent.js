/* Snapchat ad pixel, loaded only after the visitor agrees (PDPL: consent before ad tracking).
   Until then nothing from Snapchat loads and no third-party cookies are set. The choice is
   remembered on this device; "No thanks" is remembered too, so the bar asks once. */
(function () {
  var KEY = 'b3dAdConsent', PIXEL_ID = '7b499b3a-0f23-49e0-a8e1-f513ab5f10e7';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function loadSnap() {
    if (window.snaptr) return;
    var a = window.snaptr = function () { a.handleRequest ? a.handleRequest.apply(a, arguments) : a.queue.push(arguments); };
    a.queue = [];
    var s = document.createElement('script'); s.async = true; s.src = 'https://sc-static.net/scevent.min.js';
    document.head.appendChild(s);
    a('init', PIXEL_ID, {});
    a('track', 'PAGE_VIEW');
  }

  var choice = get();
  if (choice === 'yes') { loadSnap(); return; }
  if (choice === 'no') return;

  var AR = (document.documentElement.lang || '').slice(0, 2) === 'ar';
  var txt = AR
    ? { msg: 'نستخدم ملف تعريف إعلاني (سناب شات) لقياس أداء إعلاناتنا، فقط بموافقتك.', more: 'سياسة الخصوصية', yes: 'موافق', no: 'لا، شكراً', href: '/ar/privacy-policy.html' }
    : { msg: 'We use an advertising cookie (Snapchat) to measure our ads, only if you agree.', more: 'Privacy policy', yes: 'Accept', no: 'No thanks', href: '/privacy-policy.html' };

  function show() {
    var bar = document.createElement('div');
    bar.className = 'b3d-consent';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', AR ? 'موافقة ملفات تعريف الارتباط' : 'Cookie consent');
    bar.innerHTML = '<p>' + txt.msg + ' <a href="' + txt.href + '">' + txt.more + '</a></p>' +
      '<div class="b3d-consent__btns"><button type="button" class="b3d-consent__no">' + txt.no + '</button>' +
      '<button type="button" class="b3d-consent__yes">' + txt.yes + '</button></div>';
    document.body.appendChild(bar);
    bar.querySelector('.b3d-consent__yes').addEventListener('click', function () { set('yes'); bar.remove(); loadSnap(); });
    bar.querySelector('.b3d-consent__no').addEventListener('click', function () { set('no'); bar.remove(); });
  }
  // Shown after the page has loaded, so it never delays the first paint.
  if (document.readyState === 'complete') setTimeout(show, 1200);
  else window.addEventListener('load', function () { setTimeout(show, 1200); }, { once: true });
})();
