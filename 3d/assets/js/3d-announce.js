/* Black Arrow 3D announcement popup ("SUNLU PLA Classic is now available").
   Loaded by 3d-store.js on every 3D page. Shown once per visitor: closing it (x, "Maybe later",
   Esc, backdrop) or opening the product remembers the choice on this device. Not shown on the
   product page itself, cart/checkout, account, invoice, admin or returns pages, nor after END.
   To announce something else later: change ID (so everyone sees the new one once) and the text. */
(function () {
  var A = {
    id: 'sunlu-pla-classic-2026-11',
    end: '2026-12-31',
    productPath: '/3d/product/sunlu-pla-classic-filament/',
    productPathAr: '/3d/ar/product/sunlu-pla-classic-filament/',
    image: '/3d/assets/images/products/sunlu-pla-classic-white-500w.webp',
    swatches: [
      ['#f2f2ec', 'White', 'أبيض'], ['#1a1a1a', 'Black', 'أسود'], ['#8a8d90', 'Grey', 'رمادي'],
      ['#3fcf9e', 'Mint Green', 'أخضر نعناعي'], ['#e4564f', 'Cherry Red', 'أحمر كرزي'],
      ['#f3c9d4', 'Sakura Pink', 'وردي ساكورا'], ['#8fd3ea', 'Sky Blue', 'أزرق سماوي']
    ],
    en: {
      eyebrow: 'New arrival · In stock now',
      title: 'SUNLU PLA Classic is here',
      body: 'High-speed matte PLA, 1.75 mm, 1 kg spool. Clean prints at up to 300 mm/s, in 7 colours.',
      price: '75 SAR', vat: 'VAT included',
      cta: 'Shop SUNLU PLA', later: 'Maybe later', close: 'Close'
    },
    ar: {
      eyebrow: 'وصل حديثاً · متوفر الآن',
      title: 'فيلامنت SUNLU PLA Classic متوفر الآن',
      body: 'فيلامنت PLA مطفي عالي السرعة، بقطر 1.75 مم، بكرة 1 كغ. طباعة نظيفة حتى 300 مم/ث، بـ 7 ألوان.',
      price: '75 ر.س', vat: 'شامل الضريبة',
      cta: 'تسوّق SUNLU PLA', later: 'لاحقاً', close: 'إغلاق'
    }
  };

  var KEY = 'b3dAnnounceSeen:' + A.id;
  var path = location.pathname;
  if (/\/(cart|checkout|account|invoice|review-admin|returns)(\/|$)/.test(path)) return;
  if (path.indexOf('/product/sunlu-pla-classic-filament') !== -1) return;
  if (new Date() > new Date(A.end + 'T23:59:59+03:00')) return;
  try { if (localStorage.getItem(KEY)) return; } catch (e) { return; } // no storage: don't nag on every page

  var AR = (document.documentElement.lang || '').slice(0, 2) === 'ar';
  var T = AR ? A.ar : A.en;
  var href = AR ? A.productPathAr : A.productPath;

  var CSS =
    '.b3d-ann{position:fixed;inset:0;z-index:1300;display:flex;align-items:center;justify-content:center;padding:16px;' +
    'background:rgba(8,9,11,.62);opacity:0;transition:opacity .25s ease}' +
    '.b3d-ann.is-open{opacity:1}' +
    '.b3d-ann__card:focus{outline:none}.b3d-ann__card{position:relative;width:100%;max-width:420px;max-height:calc(100vh - 32px);overflow:auto;border-radius:18px;' +
    'background:#15171b;color:#f3f1ec;border:1px solid rgba(245,158,11,.35);box-shadow:0 24px 70px rgba(0,0,0,.55);' +
    'transform:translateY(14px) scale(.98);transition:transform .3s cubic-bezier(.2,.8,.2,1)}' +
    '.b3d-ann.is-open .b3d-ann__card{transform:none}' +
    '.b3d-ann__media{position:relative;display:block;background:radial-gradient(120% 90% at 50% 15%,#2c2414 0%,#16130d 70%);' +
    'border-radius:18px 18px 0 0;padding:22px 22px 8px;text-align:center}' +
    '.b3d-ann__media img{display:block;margin:0 auto;width:190px;max-width:62%;height:auto;aspect-ratio:1;object-fit:contain;filter:drop-shadow(0 14px 22px rgba(0,0,0,.5))}' +
    '.b3d-ann__badge{position:absolute;top:14px;inset-inline-start:14px;background:#F59E0B;color:#1a1a1a;font-weight:800;' +
    'font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;padding:5px 10px;border-radius:999px}' +
    '.b3d-ann__x{position:absolute;top:10px;inset-inline-end:10px;z-index:2;width:40px;height:40px;border-radius:50%;border:0;' +
    'background:rgba(0,0,0,.55);color:#fff;font-size:22px;line-height:40px;cursor:pointer;display:flex;align-items:center;justify-content:center}' +
    '.b3d-ann__x:hover{background:rgba(0,0,0,.8)}' +
    '.b3d-ann__x:focus-visible,.b3d-ann__cta:focus-visible,.b3d-ann__later:focus-visible{outline:2px solid #FBBF24;outline-offset:2px}' +
    '.b3d-ann__body{padding:14px 22px 22px}' +
    '.b3d-ann__eyebrow{color:#FBBF24;font-size:.78rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;margin:0 0 6px}' +
    '.b3d-ann__title{font-family:var(--ff-heading,"Playfair Display",Georgia,serif);font-size:1.55rem;line-height:1.2;margin:0 0 8px;color:#fff;text-wrap:balance}' +
    '.b3d-ann__text{margin:0 0 14px;color:rgba(243,241,236,.82);font-size:.95rem;line-height:1.55}' +
    '.b3d-ann__sw{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px;padding:0;list-style:none}' +
    '.b3d-ann__sw li{width:22px;height:22px;border-radius:50%;border:2px solid rgba(255,255,255,.25)}' +
    '.b3d-ann__row{display:flex;align-items:baseline;gap:8px;margin:0 0 16px}' +
    '.b3d-ann__price{font-family:var(--ff-heading,"Playfair Display",Georgia,serif);font-size:1.6rem;font-weight:800;color:#fff;font-variant-numeric:tabular-nums}' +
    '.b3d-ann__vat{font-size:.8rem;color:rgba(243,241,236,.65)}' +
    '.b3d-ann__cta{display:flex;align-items:center;justify-content:center;width:100%;min-height:48px;border-radius:10px;background:#047857;' +
    'color:#fff;font-weight:800;font-size:1rem;text-decoration:none;box-sizing:border-box}' +
    '.b3d-ann__cta:hover{background:#065f46;color:#fff}' +
    '.b3d-ann__later{display:block;margin:10px auto 0;background:none;border:0;color:rgba(243,241,236,.7);font:inherit;font-size:.9rem;' +
    'text-decoration:underline;cursor:pointer;min-height:40px;padding:0 12px}' +
    '[dir=rtl] .b3d-ann__title,[dir=rtl] .b3d-ann__price{font-family:"Noto Kufi Arabic",Tahoma,sans-serif}' +
    '@media (max-width:400px){.b3d-ann__title{font-size:1.35rem}.b3d-ann__media img{width:150px}}' +
    '@media (prefers-reduced-motion:reduce){.b3d-ann,.b3d-ann__card{transition:none}}';

  function remember() { try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function show() {
    if (document.querySelector('.b3d-ann')) return;
    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    var wrap = document.createElement('div');
    wrap.className = 'b3d-ann';
    wrap.innerHTML =
      '<div class="b3d-ann__card" tabindex="-1" role="dialog" aria-modal="true" aria-labelledby="b3d-ann-title" aria-describedby="b3d-ann-text">' +
        '<button type="button" class="b3d-ann__x" aria-label="' + esc(T.close) + '">&times;</button>' +
        '<a class="b3d-ann__media" href="' + href + '" data-ann-go tabindex="-1">' +
          '<span class="b3d-ann__badge">' + (AR ? 'جديد' : 'New') + '</span>' +
          '<img src="' + A.image + '" alt="SUNLU PLA Classic 1 kg" width="190" height="190" decoding="async">' +
        '</a>' +
        '<div class="b3d-ann__body">' +
          '<p class="b3d-ann__eyebrow">' + esc(T.eyebrow) + '</p>' +
          '<h2 class="b3d-ann__title" id="b3d-ann-title">' + esc(T.title) + '</h2>' +
          '<p class="b3d-ann__text" id="b3d-ann-text">' + esc(T.body) + '</p>' +
          '<ul class="b3d-ann__sw" aria-label="' + (AR ? 'الألوان المتوفرة' : 'Available colours') + '">' +
            A.swatches.map(function (s) { return '<li style="background:' + s[0] + '" title="' + esc(AR ? s[2] : s[1]) + '"></li>'; }).join('') +
          '</ul>' +
          '<div class="b3d-ann__row"><span class="b3d-ann__price">' + esc(T.price) + '</span><span class="b3d-ann__vat">' + esc(T.vat) + '</span></div>' +
          '<a class="b3d-ann__cta" href="' + href + '" data-ann-go>' + esc(T.cta) + '</a>' +
          '<button type="button" class="b3d-ann__later">' + esc(T.later) + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(wrap);
    var lastFocus = document.activeElement;
    var close = function () {
      remember();
      wrap.classList.remove('is-open');
      document.removeEventListener('keydown', onKey);
      setTimeout(function () { wrap.remove(); st.remove(); }, 260);
      if (lastFocus && lastFocus.focus) try { lastFocus.focus(); } catch (e) {}
    };
    var onKey = function (e) {
      if (e.key === 'Escape') close();
      if (e.key === 'Tab') { // keep focus inside the popup
        var f = wrap.querySelectorAll('button, a[href]:not([tabindex="-1"])'), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    };
    wrap.querySelector('.b3d-ann__x').addEventListener('click', close);
    wrap.querySelector('.b3d-ann__later').addEventListener('click', close);
    wrap.addEventListener('click', function (e) { if (e.target === wrap) close(); });
    [].forEach.call(wrap.querySelectorAll('[data-ann-go]'), function (a) {
      a.addEventListener('click', function () {
        remember();
        if (window.dataLayer) window.dataLayer.push({ event: 'announcement_click', announcement_id: A.id });
      });
    });
    document.addEventListener('keydown', onKey);
    requestAnimationFrame(function () { wrap.classList.add('is-open'); wrap.querySelector('.b3d-ann__card').focus({ preventScroll: true }); });
    if (window.dataLayer) window.dataLayer.push({ event: 'announcement_view', announcement_id: A.id });
  }

  // Wait until the page has loaded, then a short pause so the visitor sees the page first.
  function go() { setTimeout(show, 1500); }
  if (document.readyState === 'complete') go(); else window.addEventListener('load', go, { once: true });
})();
