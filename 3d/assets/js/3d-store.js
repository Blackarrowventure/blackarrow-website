/* Black Arrow 3D — product catalog + client-side cart.
   No backend yet: catalog comes from a static JSON file, cart lives in
   localStorage. Checkout/payment is a placeholder until Moyasar is
   approved and wired in. Login uses Firebase Authentication once
   configured in 3d-auth.js — this file never depends on it directly. */
(function () {
  'use strict';

  var CART_KEY = 'b3d_cart_v1';
  var MOTION_KEY = 'b3d_motion_v1';
  var DATA_URL = '/3d/assets/data/3d-products.json';
  var PAGE_SIZE = 12;

  var ICONS = {
    'printer': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="14" y="8" width="36" height="16" rx="2"/><rect x="10" y="24" width="44" height="20" rx="2"/><rect x="20" y="44" width="24" height="12" rx="1.5"/><line x1="32" y1="30" x2="32" y2="40"/><circle cx="18" cy="18" r="2" fill="currentColor" stroke="none"/></svg>',
    'spool': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="32" r="24"/><circle cx="32" cy="32" r="9"/><path d="M12 20c8 6 32 6 40 0" opacity=".5"/><path d="M12 44c8-6 32-6 40 0" opacity=".5"/></svg>',
    'accessory': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="14" y="14" width="36" height="36" rx="6"/><path d="M24 32h16M32 24v16" /></svg>',
    'artwork': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M32 8c9 0 16 7 16 15 0 6-4 8-9 8h-3c-2 0-3 1.5-3 3.5S34 38 34 40c0 8-6 16-14 16A16 16 0 0 1 4 40a16 16 0 0 1 4-10.6"/><circle cx="20" cy="20" r="2" fill="currentColor" stroke="none"/><circle cx="30" cy="14" r="2" fill="currentColor" stroke="none"/><circle cx="42" cy="22" r="2" fill="currentColor" stroke="none"/><circle cx="14" cy="34" r="2" fill="currentColor" stroke="none"/></svg>'
  };

  var CART_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>';

  var WHATSAPP_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>';

  /* Official Saudi Riyal symbol (SAMA, approved by royal decree Feb 2025;
     Unicode 17.0 encodes it at U+20C1, but font support for that code
     point is not yet reliable, so the government's own SVG shape is
     inlined here instead — same source file saved at
     3d/assets/images/icons/saudi-riyal-symbol.svg for reference). */
  var RIYAL_SVG = '<svg viewBox="0 0 395 432" xmlns="http://www.w3.org/2000/svg"><path d="M240.555 382.706C233.658 398 229.098 414.597 227.352 432.003L373.316 400.974C380.214 385.684 384.769 369.083 386.52 351.678L240.555 382.706Z"/><path d="M373.316 308.014C380.213 292.723 384.772 276.123 386.519 258.717L272.817 282.9V236.412L373.312 215.056C380.21 199.765 384.769 183.165 386.516 165.759L272.814 189.921V22.7383C255.391 32.5206 239.918 45.5419 227.341 60.9013V199.59L181.868 209.256V0C164.445 9.77887 148.972 22.8036 136.394 38.1631V218.917L34.6481 240.538C27.7506 255.829 23.1878 272.43 21.4376 289.835L136.394 265.405V323.948L13.1957 350.128C6.29825 365.418 1.73891 382.019 -0.0078125 399.424L128.947 372.02C139.444 369.837 148.467 363.63 154.333 355.089L177.982 320.028V320.021C180.437 316.393 181.868 312.02 181.868 307.309V255.74L227.341 246.074V339.049L373.312 308.007L373.316 308.014Z"/></svg>';

  function whatsappCardLink(p) {
    var msg = 'Hello! I have a question about ' + L(p, 'name') + '.';
    return 'https://wa.me/966560224715?text=' + encodeURIComponent(msg);
  }

  function iconFor(category) {
    if (category === 'Filament') return ICONS.spool;
    if (category === 'Accessories') return ICONS.accessory;
    if (category === '3D Artwork') return ICONS.artwork;
    return ICONS.printer;
  }

  /* ---------------- i18n helpers ---------------- */

  function T(key) {
    return (window.BlackArrow3DI18n && window.BlackArrow3DI18n.t(key)) || key;
  }

  function isAr() {
    return !!(window.BlackArrow3DI18n && window.BlackArrow3DI18n.getLang() === 'ar');
  }

  function L(p, field) {
    if (isAr() && p[field + '_ar']) return p[field + '_ar'];
    return p[field];
  }

  function LSpecs(p) {
    if (isAr() && p.specs_ar && p.specs_ar.length) return p.specs_ar;
    return p.specs || [];
  }

  function LCompat(p) {
    if (isAr() && p.compatibility_ar && p.compatibility_ar.length) return p.compatibility_ar;
    return p.compatibility || [];
  }

  function LVariant(v) {
    if (isAr() && v.label_ar) return v.label_ar;
    return v.label;
  }

  function categoryLabel(cat) {
    if (cat === '3D Printers') return T('nav_3d_printers');
    if (cat === 'Filament') return T('nav_filaments');
    if (cat === 'Accessories') return T('nav_accessories');
    if (cat === '3D Artwork') return T('nav_gaming_accessories');
    return cat;
  }

  /* ---------------- Motion control ---------------- */

  function motionEnabled() {
    try {
      var stored = localStorage.getItem(MOTION_KEY);
      if (stored === 'off') return false;
      if (stored === 'on') return true;
    } catch (e) {}
    return !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function applyMotionState(enabled) {
    document.documentElement.setAttribute('data-b3d-motion', enabled ? 'on' : 'off');
    document.querySelectorAll('[data-motion-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(!enabled));
      var label = btn.querySelector('[data-i18n-motion]') || btn;
      label.textContent = (window.BlackArrow3DI18n ? window.BlackArrow3DI18n.t(enabled ? 'js_motion_on' : 'js_motion_off') : (enabled ? 'Motion: On' : 'Motion: Off'));
    });
  }

  function initMotionToggle() {
    var enabled = motionEnabled();
    applyMotionState(enabled);
    document.querySelectorAll('[data-motion-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        enabled = !enabled;
        try { localStorage.setItem(MOTION_KEY, enabled ? 'on' : 'off'); } catch (e) {}
        applyMotionState(enabled);
      });
    });
  }

  /* ---------------- Cart ---------------- */

  function getCart() {
    try {
      var raw = localStorage.getItem(CART_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) { return {}; }
  }

  function saveCart(cart) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (e) {}
    updateCartBadges(cart);
  }

  function cartCount(cart) {
    var n = 0;
    for (var id in cart) n += cart[id];
    return n;
  }

  function updateCartBadges(cart) {
    cart = cart || getCart();
    var count = cartCount(cart);
    document.querySelectorAll('[data-b3d-cart-count]').forEach(function (el) {
      el.textContent = count;
      el.hidden = count === 0;
    });
  }

  function addToCart(id, qty) {
    qty = qty || 1;
    var cart = getCart();
    cart[id] = (cart[id] || 0) + qty;
    saveCart(cart);
  }

  function setQty(id, qty) {
    var cart = getCart();
    if (qty <= 0) { delete cart[id]; } else { cart[id] = qty; }
    saveCart(cart);
  }

  function removeFromCart(id) {
    var cart = getCart();
    delete cart[id];
    saveCart(cart);
  }

  /* ---------------- Data ---------------- */

  function fetchProducts() {
    return fetch(DATA_URL).then(function (r) { return r.json(); }).then(function (data) {
      return data.products || [];
    });
  }

  function money(n, currency) {
    if ((currency || 'SAR') === 'SAR') {
      return n.toLocaleString('en-US') + ' <small class="b3d-riyal" aria-hidden="true">' + RIYAL_SVG + '</small><span class="sr-only"> SAR</span>';
    }
    return n.toLocaleString('en-US') + ' <small>' + currency + '</small>';
  }

  function primaryImage(p) {
    if (p.cardImage) return p.cardImage;
    if (p.images && p.images.length) return p.images[0];
    if (p.image) return p.image;
    return null;
  }

  /* Clean, crawlable product URLs (/3d/product/<id>/) replaced the old
     query-string form (/3d/product/?slug=<id>) so search engines can
     index each product at its own address — see
     scripts/generate-3d-static-pages.js, which pre-renders the actual
     HTML for these URLs. Every link this file builds should point at
     the clean form; the old query-string page still works (read via
     renderProductDetail's fallback below) and is 301-redirected at the
     edge (vercel.json) for anyone with an old link bookmarked. */
  function isArPage() {
    return location.pathname.indexOf('/3d/ar/') === 0;
  }

  function productUrl(p) {
    return (isArPage() ? '/3d/ar' : '/3d') + '/product/' + p.id + '/';
  }

  /* Native pixel width of each product image that has a matching -500w.webp
     variant generated alongside it (see scripts/optimize_images.py history) —
     needed so the srcset width descriptor is accurate, not just a guess. */
  var IMG_NATIVE_WIDTH = {
    'a1-extruder-unit-01.webp': 1200, 'anycubic-kobra3max-01.webp': 600,
    'bambu-a1-01.webp': 900, 'bambu-a1-02.webp': 1024,
    'bambu-a1-mini-ams-combo.webp': 1144, 'bambu-a1-mini-main.webp': 599,
    'bambu-a2l-01.webp': 1200, 'bambu-a2l-04.webp': 1200,
    'bambu-h2c-01.webp': 763, 'bambu-hotend-a1-01.webp': 1200,
    'bambu-p2s-01.webp': 892, 'bambu-p2s-04.webp': 1200,
    'creality-sparkx-i7-01.webp': 1200, 'elegoo-cc2-01.webp': 1024,
    'filament-cutter-lever-01.webp': 1200, 'flashforge-adv5m-01.webp': 1200,
    'flashforge-c5pro-01.webp': 1200, 'flmnt-pla-black.webp': 1200,
    'flmnt-pla-blue.webp': 1024, 'flmnt-pla-gray.webp': 1024,
    'flmnt-pla-green.webp': 1024, 'flmnt-pla-orange.webp': 1200,
    'flmnt-pla-red.webp': 1024, 'flmnt-pla-white.webp': 1200,
    'flmnt-pla-yellow.webp': 1024, 'hotend-heating-a1-01.webp': 1200,
    'snapmaker-u1-01.webp': 1037
  };

  function visual(p) {
    var img = primaryImage(p);
    if (!img) return '<div class="b3d-card__visual-placeholder">' + T('js_product_image') + '</div>';
    var basename = img.split('/').pop();
    var nativeWidth = IMG_NATIVE_WIDTH[basename];
    var srcsetAttr = '';
    if (nativeWidth) {
      var small = img.replace(/\.webp$/, '-500w.webp');
      srcsetAttr = ' srcset="' + small + ' 500w, ' + img + ' ' + nativeWidth + 'w" sizes="(max-width: 480px) 90vw, 300px"';
    }
    return '<img src="' + img + '"' + srcsetAttr + ' alt="' + L(p, 'name') + '" loading="lazy" width="400" height="400">';
  }

  function statusBadge(p) {
    if (p.preorder) return '<span class="b3d-stock-badge b3d-stock-badge--pre">' + T('js_pre_order') + '</span>';
    if (p.available === false) return '<span class="b3d-stock-badge b3d-stock-badge--out">' + T('js_out_of_stock') + '</span>';
    return '';
  }

  function priceBlock(p) {
    if (p.variants && p.variants.length) {
      var prices = p.variants.map(function (v) { return v.price; });
      var min = Math.min.apply(null, prices);
      var allSame = prices.every(function (pr) { return pr === min; });
      if (allSame) return '<span class="b3d-price">' + money(min, p.currency) + '</span>';
      return '<span class="b3d-price-was" style="text-decoration:none;display:block;cursor:help;" title="' + T('js_from_tooltip') + '">' + T('js_from') + '</span><span class="b3d-price">' + money(min, p.currency) + '</span>';
    }
    if (p.onSale && p.salePrice != null) {
      return '<span class="b3d-price b3d-price--sale">' + money(p.salePrice, p.currency) +
        '</span><span class="b3d-price-was">' + money(p.price, p.currency) + '</span>';
    }
    return '<span class="b3d-price">' + money(p.price, p.currency) + '</span>';
  }

  function lineId(productId, variantIndex) {
    return variantIndex == null ? productId : productId + '::' + variantIndex;
  }

  function parseLineId(id) {
    var parts = id.split('::');
    return { productId: parts[0], variantIndex: parts.length > 1 ? parseInt(parts[1], 10) : null };
  }

  function cornerBadges(p) {
    var out = '';
    if (p.featured) out += '<span class="b3d-corner-badge b3d-corner-badge--featured">' + T('shop_featured') + '</span>';
    if (p.onSale) out += '<span class="b3d-corner-badge b3d-corner-badge--sale">' + T('js_sale_badge') + '</span>';
    if (p.newArrival) out += '<span class="b3d-corner-badge b3d-corner-badge--new">' + T('shop_new_badge') + '</span>';
    return out;
  }

  function productCard(p) {
    /* A single "View Product" action everywhere a card appears — direct
       Add to Cart / View Options used to compete with each other across
       cards. Actual purchase happens on the product page, which already
       has the full variant picker and quantity control. */
    var href = productUrl(p);
    /* Colour products (filament): show every colour by name on the card, mark
       the ones out of stock, and let the shopper add the chosen colour
       straight to the cart. */
    var colorProduct = !!(p.variants && p.variants.length && p.variants.every(function (v) { return v.swatch; }));
    var colorIdx = 0;
    if (colorProduct) {
      for (var ci = 0; ci < p.variants.length; ci++) { if (p.variants[ci].available !== false) { colorIdx = ci; break; } }
    }
    var colorsHtml = '';
    if (colorProduct) {
      colorsHtml = '<div class="b3d-card__colors" data-card-colors="' + p.id + '" role="group" aria-label="' + T('js_colour') + '">' +
        p.variants.map(function (v, i) {
          var out = v.available === false;
          return '<button type="button" class="b3d-color-chip' + (out ? ' is-out' : '') + '" data-card-color="' + i + '" aria-pressed="' + (i === colorIdx) + '"' +
            ' data-out="' + (out ? '1' : '0') + '"' + (v.image ? ' data-img="' + v.image + '"' : '') + '>' +
            '<span class="b3d-color-chip__dot" style="background:' + v.swatch + ';"></span>' +
            '<span class="b3d-color-chip__name">' + LVariant(v) + (out ? ' <em>' + T('js_out_of_stock') + '</em>' : '') + '</span></button>';
        }).join('') + '</div>';
    }
    var colorOut = colorProduct && p.variants[colorIdx].available === false;
    var actionBtn = colorProduct
      ? '<button type="button" class="b3d-btn-add" data-card-add="' + p.id + '" data-variant-idx="' + colorIdx + '"' + (colorOut ? ' disabled' : '') + '>' + (colorOut ? T('js_out_of_stock') : T('js_add_to_cart')) + '</button>'
      : null;
    if (actionBtn === null) actionBtn = '<a href="' + href + '" class="b3d-btn-add" aria-label="' + T('js_view_product') + ' — ' + L(p, 'name') + '">' + T('js_view_product') + '</a>';
    var isArt = p.category === '3D Artwork';
    var specs = isArt ? '' : LSpecs(p).slice(0, 3).map(function (row) {
      return '<li><span>' + row[0] + '</span><span>' + row[1] + '</span></li>';
    }).join('');
    return '' +
      '<article class="b3d-card' + (isArt ? ' b3d-card--art' : '') + '" data-cat="' + p.category + '" data-brand="' + (p.brand || '') + '">' +
        '<a href="' + href + '" class="b3d-card__stretched-link" aria-label="' + L(p, 'name') + '"></a>' +
        '<div class="b3d-card__visual">' +
          cornerBadges(p) +
          statusBadge(p) +
          visual(p) +
        '</div>' +
        '<div class="b3d-card__body">' +
          '<div class="b3d-card__cat">' + (p.brand ? p.brand + ' &middot; ' : '') + categoryLabel(p.category) + '</div>' +
          '<h3>' + L(p, 'name') + '</h3>' +
          (isArt ? '' : '<p>' + (L(p, 'shortDesc') || '') + '</p>') +
          (specs ? '<ul class="b3d-card__specs">' + specs + '</ul>' : '') +
          colorsHtml +
          '<div class="b3d-card__meta-line"><span>' + T('js_card_delivery') + '</span>' + (isArt ? '' : '<span>' + T('js_card_warranty') + '</span>') + '</div>' +
        '</div>' +
        '<div class="b3d-card__footer">' +
          '<div class="b3d-price-wrap">' +
            '<div class="b3d-price-block">' + priceBlock(p) + '</div>' +
            '<a href="' + whatsappCardLink(p) + '" target="_blank" rel="noopener noreferrer" class="b3d-card__whatsapp" aria-label="' + T('js_ask_whatsapp') + ' — ' + L(p, 'name') + '" title="' + T('js_ask_whatsapp') + '">' + WHATSAPP_SVG + '</a>' +
          '</div>' +
          '<div class="b3d-card__actions">' +
            (p.category === '3D Artwork' ? '' : '<button class="b3d-btn-compare" data-compare-id="' + p.id + '" aria-label="' + T('js_compare_btn') + ' — ' + L(p, 'name') + '" title="' + T('js_compare_btn') + '">⇄</button>') +
            '<button class="b3d-btn-wishlist' + (isWishlisted(p.id) ? ' is-active' : '') + '" data-wishlist-id="' + p.id + '" aria-label="' + (isWishlisted(p.id) ? 'Remove from wishlist' : 'Save to wishlist') + ' — ' + L(p, 'name') + '" title="Save">' + (isWishlisted(p.id) ? '♥' : '♡') + '</button>' +
            actionBtn +
          '</div>' +
        '</div>' +
      '</article>';
  }

  /* Colour chips + Add to Cart on product cards (delegated, so it works in every grid). */
  if (!window.__b3dCardColors) {
    window.__b3dCardColors = true;
    document.addEventListener('click', function (e) {
      var chip = e.target.closest && e.target.closest('[data-card-color]');
      if (chip) {
        var card = chip.closest('.b3d-card');
        card.querySelectorAll('[data-card-color]').forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
        var out = chip.getAttribute('data-out') === '1';
        var btn = card.querySelector('[data-card-add]');
        if (btn) {
          btn.setAttribute('data-variant-idx', chip.getAttribute('data-card-color'));
          btn.disabled = out;
          btn.textContent = out ? T('js_out_of_stock') : T('js_add_to_cart');
        }
        var src = chip.getAttribute('data-img');
        var img = card.querySelector('.b3d-card__visual img');
        if (src && img) { img.removeAttribute('srcset'); img.removeAttribute('sizes'); img.src = src; }
        return;
      }
      var add = e.target.closest && e.target.closest('[data-card-add]');
      if (add && !add.disabled) {
        addToCart(lineId(add.getAttribute('data-card-add'), parseInt(add.getAttribute('data-variant-idx'), 10)), 1);
        var label = T('js_add_to_cart');
        add.textContent = T('js_added');
        setTimeout(function () { if (!add.disabled) add.textContent = label; }, 1200);
      }
    });
  }

  function emptyCatalogHtml(reason) {
    return '<div class="b3d-empty" style="grid-column:1/-1;">' +
      '<h2 style="color:#fff;margin-bottom:10px;">' + (reason || T('js_no_products_published')) + '</h2>' +
      '<p>' + T('js_check_back_soon') + '</p>' +
      '</div>';
  }

  function renderGrid(products, container) {
    if (!products.length) {
      container.innerHTML = emptyCatalogHtml();
      return;
    }
    container.innerHTML = products.map(productCard).join('');
    container.querySelectorAll('[data-add-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        addToCart(btn.getAttribute('data-add-id'), 1);
        var original = btn.textContent;
        btn.textContent = T('js_added');
        setTimeout(function () { btn.textContent = original; }, 1200);
      });
    });
    container.querySelectorAll('[data-wishlist-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var nowSaved = toggleWishlist(btn.getAttribute('data-wishlist-id'));
        btn.classList.toggle('is-active', nowSaved);
        btn.textContent = nowSaved ? '♥' : '♡';
      });
    });
    container.querySelectorAll('[data-compare-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        toggleCompare(btn.getAttribute('data-compare-id'));
        btn.classList.toggle('is-active');
      });
    });
  }

  /* ---------------- Shop: filters, sort, pagination ---------------- */

  var WISHLIST_KEY = 'b3d_wishlist_v1';

  function getWishlist() {
    try {
      var raw = localStorage.getItem(WISHLIST_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
  }

  function isWishlisted(id) {
    return getWishlist().indexOf(id) !== -1;
  }

  function toggleWishlist(id) {
    var list = getWishlist();
    var idx = list.indexOf(id);
    if (idx === -1) { list.push(id); } else { list.splice(idx, 1); }
    try { localStorage.setItem(WISHLIST_KEY, JSON.stringify(list)); } catch (e) {}
    return idx === -1;
  }

  var COMPARE_KEY = 'b3d_compare_v1';

  function getCompareList() {
    try {
      var raw = localStorage.getItem(COMPARE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
  }

  function toggleCompare(id) {
    var list = getCompareList();
    var idx = list.indexOf(id);
    if (idx === -1) { list.push(id); } else { list.splice(idx, 1); }
    try { localStorage.setItem(COMPARE_KEY, JSON.stringify(list.slice(-4))); } catch (e) {}
  }

  function injectItemListSeo(products, scriptId, listName) {
    var itemListLd = {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      'itemListElement': products.map(function (p, i) {
        return {
          '@type': 'ListItem',
          'position': i + 1,
          'url': 'https://www.blackarrowksa.com' + productUrl(p),
          'name': L(p, 'name')
        };
      })
    };
    if (listName) itemListLd.name = listName;
    var script = document.getElementById(scriptId);
    if (!script) {
      script = document.createElement('script');
      script.type = 'application/ld+json';
      script.id = scriptId;
      document.head.appendChild(script);
    }
    script.textContent = JSON.stringify(itemListLd);
  }

  function specValue(p, labelPattern) {
    var row = (p.specs || []).filter(function (r) { return labelPattern.test(r[0]); })[0];
    return row ? row[1] : null;
  }

  function buildVolumeBucket(p) {
    var val = specValue(p, /^build volume$/i);
    if (!val) return null;
    var m = val.match(/(\d+(\.\d+)?)/);
    if (!m) return null;
    var n = parseFloat(m[1]);
    if (n < 220) return 'Compact';
    if (n <= 300) return 'Standard';
    return 'Large';
  }

  function filamentMaterialOf(p) {
    return specValue(p, /^material$/i);
  }

  function initShopPage(products, els) {
    var state = {
      cat: 'All',
      brand: 'All',
      q: '',
      sort: 'default',
      inStockOnly: false,
      featuredOnly: false,
      preorderOnly: false,
      saleOnly: false,
      printerType: 'All',
      buildVolume: 'All',
      filamentMaterial: 'All',
      accessoryCompat: 'All',
      priceMin: null,
      priceMax: null,
      page: 1
    };

    var params = new URLSearchParams(location.search);
    if (params.get('cat')) state.cat = params.get('cat');
    if (params.get('brand')) state.brand = params.get('brand');
    if (params.get('q')) state.q = params.get('q');

    function populateDynamicFilters() {
      if (els.brandSelect) {
        brandList().forEach(function (b) {
          var opt = document.createElement('option');
          opt.value = b;
          opt.textContent = b;
          els.brandSelect.appendChild(opt);
        });
      }
      function fillSelect(selectEl, fieldsetSelector, values, labelFn) {
        if (!selectEl) return;
        var distinct = [];
        values.forEach(function (v) { if (v && distinct.indexOf(v) === -1) distinct.push(v); });
        distinct.forEach(function (v) {
          var opt = document.createElement('option');
          opt.value = v;
          opt.textContent = labelFn ? labelFn(v) : v;
          selectEl.appendChild(opt);
        });
        var fieldset = fieldsetSelector ? document.querySelector(fieldsetSelector) : null;
        if (fieldset && distinct.length > 0) fieldset.removeAttribute('hidden');
      }
      fillSelect(els.printerTypeSelect, '[data-filter-group="printerType"]',
        products.filter(function (p) { return p.category === '3D Printers'; }).map(function (p) { return p.printerType; }));
      fillSelect(els.buildVolumeSelect, '[data-filter-group="buildVolume"]',
        products.map(buildVolumeBucket),
        function (v) { return T(v === 'Compact' ? 'filter_bv_compact' : v === 'Standard' ? 'filter_bv_standard' : 'filter_bv_large'); });
      fillSelect(els.filamentMaterialSelect, '[data-filter-group="filamentMaterial"]',
        products.filter(function (p) { return p.category === 'Filament'; }).map(filamentMaterialOf));
      fillSelect(els.accessoryCompatSelect, '[data-filter-group="accessoryCompat"]',
        products.filter(function (p) { return p.category === 'Accessories'; }).reduce(function (acc, p) { return acc.concat(p.compatibility || []); }, []));
    }
    populateDynamicFilters();

    function apply() {
      var list = products.slice();
      if (state.cat !== 'All') list = list.filter(function (p) { return p.category === state.cat; });
      if (state.brand !== 'All') list = list.filter(function (p) { return (p.brand || '').toLowerCase() === state.brand.toLowerCase(); });
      if (state.q) {
        var q = state.q.toLowerCase();
        list = list.filter(function (p) {
          return (p.name || '').toLowerCase().indexOf(q) !== -1 ||
                 (p.brand || '').toLowerCase().indexOf(q) !== -1 ||
                 (p.category || '').toLowerCase().indexOf(q) !== -1;
        });
      }
      if (state.inStockOnly) list = list.filter(function (p) { return p.available !== false; });
      if (state.featuredOnly) list = list.filter(function (p) { return !!p.featured; });
      if (state.preorderOnly) list = list.filter(function (p) { return !!p.preorder; });
      if (state.saleOnly) list = list.filter(function (p) { return !!p.onSale; });
      if (state.printerType !== 'All') list = list.filter(function (p) { return p.printerType === state.printerType; });
      if (state.buildVolume !== 'All') list = list.filter(function (p) { return buildVolumeBucket(p) === state.buildVolume; });
      if (state.filamentMaterial !== 'All') list = list.filter(function (p) { return filamentMaterialOf(p) === state.filamentMaterial; });
      if (state.accessoryCompat !== 'All') list = list.filter(function (p) { return (p.compatibility || []).indexOf(state.accessoryCompat) !== -1; });
      if (state.priceMin != null) list = list.filter(function (p) { return p.price >= state.priceMin; });
      if (state.priceMax != null) list = list.filter(function (p) { return p.price <= state.priceMax; });

      if (state.sort === 'price-asc') list.sort(function (a, b) { return a.price - b.price; });
      if (state.sort === 'price-desc') list.sort(function (a, b) { return b.price - a.price; });
      if (state.sort === 'name-asc') list.sort(function (a, b) { return a.name.localeCompare(b.name); });

      var totalPages = Math.max(1, Math.ceil(list.length / PAGE_SIZE));
      if (state.page > totalPages) state.page = totalPages;
      var pageItems = list.slice((state.page - 1) * PAGE_SIZE, state.page * PAGE_SIZE);

      renderGrid(pageItems, els.grid);
      if (els.count) els.count.textContent = list.length;
      if (els.filterToggle) {
        var activeCount = [
          state.inStockOnly, state.preorderOnly, state.featuredOnly, state.saleOnly,
          state.printerType !== 'All', state.buildVolume !== 'All',
          state.filamentMaterial !== 'All', state.accessoryCompat !== 'All',
          state.priceMin != null, state.priceMax != null
        ].filter(Boolean).length;
        var countEl = els.filterToggle.querySelector('[data-b3d-filter-count]');
        if (countEl) {
          countEl.hidden = activeCount === 0;
          countEl.textContent = activeCount ? '(' + activeCount + ')' : '';
        }
        els.filterToggle.classList.toggle('has-active-filters', activeCount > 0);
      }
      if (els.pagination) renderPagination(els.pagination, state.page, totalPages, function (p) {
        state.page = p;
        apply();
        els.grid.scrollIntoView({ behavior: motionEnabled() ? 'smooth' : 'auto', block: 'start' });
      });
    }

    function renderPagination(container, page, totalPages, onGo) {
      if (totalPages <= 1) { container.innerHTML = ''; return; }
      var html = '';
      for (var i = 1; i <= totalPages; i++) {
        html += '<button class="b3d-page-btn' + (i === page ? ' is-active' : '') + '" data-page="' + i + '">' + i + '</button>';
      }
      container.innerHTML = html;
      container.querySelectorAll('[data-page]').forEach(function (btn) {
        btn.addEventListener('click', function () { onGo(parseInt(btn.getAttribute('data-page'), 10)); });
      });
    }

    function setCategory(cat) {
      state.cat = cat;
      state.page = 1;
      if (els.categoryTabs) {
        els.categoryTabs.querySelectorAll('[data-cat]').forEach(function (t) {
          t.setAttribute('aria-pressed', String(t.getAttribute('data-cat') === cat));
        });
      }
      apply();
    }

    if (els.categoryTabs) {
      els.categoryTabs.querySelectorAll('[data-cat]').forEach(function (tab) {
        if (tab.getAttribute('data-cat') === state.cat) tab.setAttribute('aria-pressed', 'true');
        tab.addEventListener('click', function () { setCategory(tab.getAttribute('data-cat')); });
      });
    }

    document.querySelectorAll('[data-cat-shortcut]').forEach(function (btn) {
      btn.addEventListener('click', function () { setCategory(btn.getAttribute('data-cat-shortcut')); });
    });

    if (els.brandSelect) {
      els.brandSelect.value = state.brand;
      els.brandSelect.addEventListener('change', function () {
        state.brand = els.brandSelect.value;
        state.page = 1;
        apply();
      });
    }

    if (els.searchInput) {
      els.searchInput.value = state.q;
      els.searchInput.addEventListener('input', function () {
        state.q = els.searchInput.value.trim();
        state.page = 1;
        apply();
      });
    }

    if (els.sortSelect) {
      els.sortSelect.addEventListener('change', function () {
        state.sort = els.sortSelect.value;
        apply();
      });
    }

    if (els.filterForm) {
      els.filterForm.addEventListener('change', function () {
        state.inStockOnly = !!els.filterForm.querySelector('[name="f-instock"]').checked;
        state.featuredOnly = !!els.filterForm.querySelector('[name="f-featured"]').checked;
        state.preorderOnly = !!els.filterForm.querySelector('[name="f-preorder"]').checked;
        state.saleOnly = !!els.filterForm.querySelector('[name="f-sale"]').checked;
        var minVal = els.filterForm.querySelector('[name="f-price-min"]').value;
        var maxVal = els.filterForm.querySelector('[name="f-price-max"]').value;
        state.priceMin = minVal ? parseFloat(minVal) : null;
        state.priceMax = maxVal ? parseFloat(maxVal) : null;
        if (els.printerTypeSelect) state.printerType = els.printerTypeSelect.value;
        if (els.buildVolumeSelect) state.buildVolume = els.buildVolumeSelect.value;
        if (els.filamentMaterialSelect) state.filamentMaterial = els.filamentMaterialSelect.value;
        if (els.accessoryCompatSelect) state.accessoryCompat = els.accessoryCompatSelect.value;
        state.page = 1;
        apply();
      });
    }

    if (els.filterClear) {
      els.filterClear.addEventListener('click', function () {
        els.filterForm.reset();
        if (els.brandSelect) els.brandSelect.value = 'All';
        state.brand = 'All';
        state.inStockOnly = false;
        state.featuredOnly = false;
        state.preorderOnly = false;
        state.saleOnly = false;
        state.priceMin = null;
        state.priceMax = null;
        state.printerType = 'All';
        state.buildVolume = 'All';
        state.filamentMaterial = 'All';
        state.accessoryCompat = 'All';
        state.page = 1;
        apply();
      });
    }

    if (els.filterApply && els.filterPanel && els.filterToggle) {
      els.filterApply.addEventListener('click', function () {
        els.filterPanel.setAttribute('hidden', '');
        els.filterToggle.setAttribute('aria-expanded', 'false');
      });
    }

    if (els.filterToggle && els.filterPanel) {
      els.filterToggle.addEventListener('click', function () {
        var open = els.filterPanel.hasAttribute('hidden');
        if (open) { els.filterPanel.removeAttribute('hidden'); } else { els.filterPanel.setAttribute('hidden', ''); }
        els.filterToggle.setAttribute('aria-expanded', String(open));
      });
    }

    apply();
  }

  /* ---------------- Cart page ---------------- */

  var lastOrderSummaryText = '';
  var lastSubtotal = 0;
  var shippingPlaceholderText = null;

  var COUPON_KEY = 'b3d_coupon';
  var appliedCoupon = null; // { code, amount }

  // Codes live in Supabase (table not readable by the site); the site can only
  // ask "is this code valid?" and "use it up", one code at a time.
  function couponRpc(fn, code, subtotal) {
    var cfg = window.BLACK_ARROW_SUPABASE_CONFIG;
    if (!cfg || !cfg.url || !cfg.anonKey) return Promise.resolve({ ok: false, reason: 'unavailable' });
    return fetch(cfg.url + '/rest/v1/rpc/' + fn, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', apikey: cfg.anonKey, Authorization: 'Bearer ' + cfg.anonKey },
      body: JSON.stringify({ p_code: code, p_subtotal: subtotal })
    }).then(function (r) {
      if (!r.ok) throw new Error('rpc');
      return r.json();
    }).catch(function () { return { ok: false, reason: 'unavailable' }; });
  }

  function checkCoupon(code, subtotal) {
    return couponRpc('check_coupon', code.trim(), subtotal).then(function (r) {
      if (r.ok) r.code = code.trim().toUpperCase();
      return r;
    });
  }

  // Called at checkout: uses the code up for real. Resolves true if the order
  // may go ahead (no coupon, or redeemed). A redemption id is kept so a retry
  // after a failed send doesn't burn a second use.
  function redeemAppliedCoupon() {
    if (!appliedCoupon || appliedCoupon.redemption) return Promise.resolve({ ok: true });
    return couponRpc('redeem_coupon', appliedCoupon.code, lastSubtotal).then(function (r) {
      if (r.ok) {
        appliedCoupon = { code: appliedCoupon.code, amount: r.amount, redemption: r.redemption };
        updateOrderTotals();
      }
      return r;
    });
  }

  function couponDiscount() {
    return appliedCoupon ? Math.min(appliedCoupon.amount, lastSubtotal) : 0;
  }

  function initCoupon(summaryEl) {
    var box = summaryEl && summaryEl.querySelector('[data-b3d-coupon]');
    if (!box) return;
    var input = box.querySelector('[data-b3d-coupon-input]');
    var applyBtn = box.querySelector('[data-b3d-coupon-apply]');
    var msg = box.querySelector('[data-b3d-coupon-msg]');
    var removeBtn = summaryEl.querySelector('[data-b3d-coupon-remove]');

    function say(text, ok) {
      msg.textContent = text || '';
      msg.className = 'b3d-coupon__msg' + (text ? (ok ? ' is-ok' : ' is-err') : '');
    }
    function store(code) {
      try { if (code) sessionStorage.setItem(COUPON_KEY, code); else sessionStorage.removeItem(COUPON_KEY); } catch (e) {}
    }
    function failText(r) {
      if (r.reason === 'expired') return T('coupon_expired');
      if (r.reason === 'used') return T('coupon_used');
      if (r.reason === 'unavailable') return T('coupon_unavailable');
      if (r.reason === 'min') return T('coupon_min').replace('{n}', r.min);
      return T('coupon_invalid');
    }
    function apply(code, quiet) {
      return checkCoupon(code, lastSubtotal).then(function (r) {
        if (!r.ok) {
          appliedCoupon = null; store('');
          if (!quiet) say(failText(r), false);
        } else {
          appliedCoupon = { code: r.code, amount: r.amount };
          store(r.code); input.value = '';
          say('', true);
        }
        updateOrderTotals();
      });
    }

    applyBtn.addEventListener('click', function () {
      if (!input.value.trim()) { say(T('coupon_invalid'), false); return; }
      apply(input.value, false);
    });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); applyBtn.click(); }
    });
    if (removeBtn) removeBtn.addEventListener('click', function () {
      appliedCoupon = null; store(''); say('', true); updateOrderTotals();
    });

    // Re-check on every cart render (quantities change the subtotal / min-order).
    summaryEl._recheckCoupon = function () {
      var saved = null;
      try { saved = sessionStorage.getItem(COUPON_KEY); } catch (e) {}
      if (appliedCoupon && appliedCoupon.redemption) updateOrderTotals();
      else if (saved) apply(saved, false); else updateOrderTotals();
    };
  }

  function updateOrderTotals() {
    var summaryEl = document.querySelector('[data-b3d-cart-summary]');
    var checkout = document.querySelector('[data-b3d-checkout]');
    if (!summaryEl) return;
    var shippingEl = summaryEl.querySelector('[data-cart-shipping]');
    var totalEl = summaryEl.querySelector('[data-cart-total]');
    if (shippingPlaceholderText === null && shippingEl) shippingPlaceholderText = shippingEl.textContent;

    var discount = couponDiscount();
    var discountRow = summaryEl.querySelector('[data-b3d-discount-row]');
    if (discountRow) {
      discountRow.hidden = !discount;
      if (discount) {
        summaryEl.querySelector('[data-b3d-discount-code]').textContent = appliedCoupon.code;
        summaryEl.querySelector('[data-cart-discount]').innerHTML = '\u2212' + money(discount, 'SAR');
      }
    }
    var couponForm = summaryEl.querySelector('[data-b3d-coupon]');
    if (couponForm) couponForm.hidden = !!discount;
    var couponField = document.querySelector('[data-b3d-coupon-field]');
    if (couponField) couponField.value = discount ? appliedCoupon.code + (appliedCoupon.redemption ? ' / ' + appliedCoupon.redemption : '') : '';
    var discountLine = discount ? '\nDiscount (' + appliedCoupon.code + (appliedCoupon.redemption ? ', redemption ' + appliedCoupon.redemption : '') + '): -' + discount + ' SAR' : '';
    var after = lastSubtotal - discount;

    var showShipping = checkout && !checkout.hidden;
    if (!showShipping) {
      if (shippingEl) shippingEl.textContent = shippingPlaceholderText;
      if (totalEl) totalEl.innerHTML = money(after, 'SAR');
      return;
    }

    var checkedRadio = checkout.querySelector('input[name="shipping_choice"]:checked');
    var price = checkedRadio ? parseInt(checkedRadio.getAttribute('data-shipping-price'), 10) : 0;
    var label = checkedRadio ? checkedRadio.getAttribute('data-shipping-label') : '';
    if (shippingEl) shippingEl.innerHTML = money(price, 'SAR');
    if (totalEl) totalEl.innerHTML = money(after + price, 'SAR');

    var shipField = checkout.querySelector('[data-b3d-shipping-field]');
    if (shipField) shipField.value = label + ' — ' + price + ' SAR';
    var summaryField = checkout.querySelector('[data-b3d-order-summary]');
    if (summaryField) {
      summaryField.value = lastOrderSummaryText + discountLine +
        '\nShipping: ' + label + ' — ' + price + ' SAR' +
        '\nGrand Total: ' + (after + price).toLocaleString('en-US') + ' SAR';
    }
  }

  function updateCheckoutFields(method) {
    var checkout = document.querySelector('[data-b3d-checkout]');
    if (!checkout) return;
    var purchasable = method === 'cod' || method === 'bank';
    checkout.hidden = !purchasable;
    if (purchasable) {
      var payField = checkout.querySelector('[data-b3d-order-payment]');
      if (payField) payField.value = method === 'cod' ? 'Cash on Delivery' : 'Bank Transfer';
    }
    updateOrderTotals();
  }

  function initShippingMethods(root) {
    if (!root) return;
    root.querySelectorAll('input[name="shipping_choice"]').forEach(function (radio) {
      radio.addEventListener('change', updateOrderTotals);
    });
  }

  function initCheckoutAuth(root) {
    if (!root || !window.BlackArrow3DAuth || !window.BlackArrow3DAuth.isConfigured()) return;
    var loginRow = root.querySelector('[data-b3d-checkout-login]');
    var signedInRow = root.querySelector('[data-b3d-checkout-signedin]');
    var emailEl = root.querySelector('[data-b3d-checkout-email]');
    var saveCheckbox = root.querySelector('[data-b3d-save-info]');
    var form = root.querySelector('#b3d-checkout-form');
    var currentUser = null;

    window.BlackArrow3DAuth.init(function (ok) {
      if (!ok) return;
      window.BlackArrow3DAuth.onAuthChange(function (user) {
        currentUser = user;
        if (loginRow) loginRow.hidden = !!user;
        if (signedInRow) signedInRow.hidden = !user;
        if (user && emailEl) emailEl.textContent = user.email;
        if (user) {
          var checkoutEmailField = form && form.querySelector('[data-b3d-field="email"]');
          if (checkoutEmailField && !checkoutEmailField.value) checkoutEmailField.value = user.email;
          window.BlackArrow3DAuth.getProfile(user.id).then(function (profile) {
            if (!profile || !form) return;
            var addr = profile.last_address || {};
            Object.keys(addr).forEach(function (key) {
              var field = form.querySelector('[data-b3d-field="' + key + '"]');
              if (field && !field.value) field.value = addr[key];
            });
            var phoneField = form.querySelector('[data-b3d-field="phone"]');
            if (phoneField && !phoneField.value && profile.phone) phoneField.value = profile.phone;
          });
        }
      });
    });

    if (form) {
      form.addEventListener('submit', function () {
        if (!saveCheckbox || !saveCheckbox.checked || !currentUser) return;
        var addr = {};
        form.querySelectorAll('[data-b3d-field]').forEach(function (field) {
          addr[field.getAttribute('data-b3d-field')] = field.value;
        });
        window.BlackArrow3DAuth.saveProfile(currentUser.id, {
          phone: addr.phone,
          last_address: addr
        });
      });
    }
  }

  function loadEmailJsSdk(cb) {
    if (window.emailjs) { cb(true); return; }
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js';
    script.onload = function () { cb(!!window.emailjs); };
    script.onerror = function () { cb(false); };
    document.head.appendChild(script);
  }

  function sendCustomerConfirmation(form) {
    var cfg = window.BLACK_ARROW_EMAILJS_CONFIG;
    if (!cfg || !cfg.publicKey || !cfg.serviceId || !cfg.templateId) return;

    var field = function (name) {
      var el = form.querySelector('[name="' + name + '"]');
      return el ? el.value : '';
    };
    var toEmail = field('email');
    if (!toEmail) return;

    var payField = form.querySelector('[data-b3d-order-payment]');
    var shipField = form.querySelector('[data-b3d-shipping-field]');
    var summaryField = form.querySelector('[data-b3d-order-summary]');

    var params = {
      to_email: toEmail,
      to_name: (field('customer_first_name') + ' ' + field('customer_last_name')).trim(),
      order_summary: summaryField ? summaryField.value : '',
      shipping_method: shipField ? shipField.value : '',
      payment_method: payField ? payField.value : '',
      order_total: document.querySelector('[data-cart-total]') ? document.querySelector('[data-cart-total]').textContent : ''
    };

    loadEmailJsSdk(function (ok) {
      if (!ok) { console.warn('Black Arrow 3D: EmailJS SDK failed to load, customer confirmation not sent'); return; }
      try {
        window.emailjs.init({ publicKey: cfg.publicKey });
        window.emailjs.send(cfg.serviceId, cfg.templateId, params).catch(function (err) {
          console.warn('Black Arrow 3D: customer confirmation email failed', err);
        });
      } catch (e) {
        console.warn('Black Arrow 3D: customer confirmation email failed', e);
      }
    });
  }

  function showThankYou(form, mailOn) {
    var view = document.querySelector('[data-b3d-thanks]');
    if (!view) return;
    var val = function (sel) { var el = form.querySelector(sel); return el ? el.value : ''; };
    var summary = val('[data-b3d-order-summary]');
    var linesEl = view.querySelector('[data-b3d-thanks-lines]');
    linesEl.textContent = '';
    var grand = '';
    summary.split('\n').forEach(function (line) {
      if (!line) return;
      if (line.indexOf('Grand Total:') === 0) { grand = line.replace('Grand Total:', '').trim(); return; }
      if (line.indexOf('Shipping:') === 0) return;
      if (line.indexOf('Total:') === 0) return;
      var row = document.createElement('div');
      row.textContent = line;
      linesEl.appendChild(row);
    });
    view.querySelector('[data-b3d-thanks-payment]').textContent = val('[data-b3d-order-payment]');
    view.querySelector('[data-b3d-thanks-shipping]').textContent = val('[data-b3d-shipping-field]');
    view.querySelector('[data-b3d-thanks-total]').textContent = grand;
    var lead = view.querySelector('[data-b3d-thanks-lead]');
    var emailEl = view.querySelector('[data-b3d-thanks-email]');
    if (mailOn) {
      lead.setAttribute('data-i18n', 'thanks_p_email');
      lead.textContent = T('thanks_p_email');
      emailEl.textContent = val('[name="email"]');
    } else {
      emailEl.textContent = '';
    }
    ['[data-b3d-cart-header]', '[data-b3d-cart-empty]'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (el) el.hidden = true;
    });
    var layout = document.querySelector('.b3d-cart-layout');
    if (layout) layout.style.display = 'none';
    view.hidden = false;
    window.scrollTo(0, 0);
  }

  function initCheckoutSubmit(form) {
    if (!form) return;
    var successEl = document.getElementById('b3d-checkout-success');
    var errorEl = document.getElementById('b3d-checkout-error');
    var submitBtn = form.querySelector('[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }

      var label = submitBtn ? submitBtn.textContent : '';
      if (submitBtn) { submitBtn.textContent = '...'; submitBtn.disabled = true; }
      if (errorEl) errorEl.hidden = true;
      if (successEl) successEl.hidden = true;

      redeemAppliedCoupon().then(function (r) {
        if (!r.ok) {
          appliedCoupon = null;
          try { sessionStorage.removeItem(COUPON_KEY); } catch (e) {}
          updateOrderTotals();
          var cm = document.querySelector('[data-b3d-coupon-msg]');
          if (cm) { cm.textContent = T('coupon_gone'); cm.className = 'b3d-coupon__msg is-err'; }
          throw new Error('coupon');
        }
        return fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' }
        });
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          if (!res.ok || data.success === false) throw new Error(data.message || 'failed');
          var mailCfg = window.BLACK_ARROW_EMAILJS_CONFIG;
          var mailOn = !!(mailCfg && mailCfg.publicKey && mailCfg.serviceId && mailCfg.templateId);
          showThankYou(form, mailOn);
          sendCustomerConfirmation(form);
          saveCart({});
        });
      }).catch(function (err) {
        if (errorEl && !(err && err.message === 'coupon')) errorEl.hidden = false;
      }).then(function () {
        if (submitBtn) { submitBtn.textContent = label; submitBtn.disabled = false; }
      });
    });
  }

  function renderCartPage(listEl, summaryEl, emptyEl) {
    fetchProducts().then(function (products) {
      var cart = getCart();
      var ids = Object.keys(cart);
      if (ids.length === 0) {
        listEl.hidden = true;
        summaryEl.hidden = true;
        emptyEl.hidden = false;
        return;
      }
      emptyEl.hidden = true;
      listEl.hidden = false;
      summaryEl.hidden = false;

      var byId = {};
      products.forEach(function (p) { byId[p.id] = p; });

      var subtotal = 0;
      var summaryLines = [];
      listEl.innerHTML = ids.map(function (id) {
        var parsed = parseLineId(id);
        var p = byId[parsed.productId];
        if (!p) return '';
        var variant = parsed.variantIndex != null && p.variants ? p.variants[parsed.variantIndex] : null;
        var qty = cart[id];
        var unit = variant ? variant.price : ((p.onSale && p.salePrice != null) ? p.salePrice : p.price);
        var lineTotal = unit * qty;
        subtotal += lineTotal;
        var displayName = L(p, 'name') + (variant ? ' — ' + LVariant(variant) : '');
        summaryLines.push(displayName + ' x' + qty + ' — ' + lineTotal.toLocaleString('en-US') + ' ' + (p.currency || 'SAR'));
        return '' +
          '<div class="b3d-cart-item" data-line-id="' + id + '">' +
            '<div class="b3d-cart-item__visual">' + visual(p) + '</div>' +
            '<div>' +
              '<div class="b3d-cart-item__name">' + displayName + '</div>' +
              '<div class="b3d-cart-item__cat">' + categoryLabel(p.category) + '</div>' +
              '<button class="b3d-cart-item__remove" data-remove-id="' + id + '">' + T('js_remove') + '</button>' +
            '</div>' +
            '<div class="b3d-qty">' +
              '<button data-qty-btn="minus" data-id="' + id + '" aria-label="' + T('js_qty_decrease') + '">−</button>' +
              '<input type="text" readonly value="' + qty + '" data-qty-val="' + id + '" aria-label="' + T('js_qty_label') + '">' +
              '<button data-qty-btn="plus" data-id="' + id + '" aria-label="' + T('js_qty_increase') + '">+</button>' +
            '</div>' +
            '<div class="b3d-cart-item__price">' + money(lineTotal, p.currency) + '</div>' +
          '</div>';
      }).join('');

      summaryEl.querySelector('[data-cart-subtotal]').innerHTML = money(subtotal, 'SAR');

      lastSubtotal = subtotal;
      lastOrderSummaryText = summaryLines.join('\n') + '\nTotal: ' + subtotal.toLocaleString('en-US') + ' SAR';
      if (summaryEl._recheckCoupon) summaryEl._recheckCoupon(); else updateOrderTotals();

      listEl.querySelectorAll('[data-remove-id]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          removeFromCart(btn.getAttribute('data-remove-id'));
          renderCartPage(listEl, summaryEl, emptyEl);
        });
      });
      listEl.querySelectorAll('[data-qty-btn]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var id = btn.getAttribute('data-id');
          var current = getCart()[id] || 0;
          var next = btn.getAttribute('data-qty-btn') === 'plus' ? current + 1 : current - 1;
          setQty(id, next);
          renderCartPage(listEl, summaryEl, emptyEl);
        });
      });
    });
  }

  function initPaymentMethods(root) {
    if (!root) return;
    root.querySelectorAll('[data-pm]').forEach(function (el) {
      el.addEventListener('click', function () {
        if (el.hasAttribute('disabled')) return;
        root.querySelectorAll('[data-pm]').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        el.setAttribute('aria-pressed', 'true');
        var method = el.getAttribute('data-pm');
        root.querySelectorAll('[data-pm-detail]').forEach(function (d) {
          d.hidden = d.getAttribute('data-pm-detail') !== method;
        });
        updateCheckoutFields(method);
      });
    });
  }

  /* ---------------- Product detail ---------------- */

  function absUrl(path) {
    if (!path) return '';
    return path.indexOf('http') === 0 ? path : 'https://www.blackarrowksa.com' + path;
  }

  function updateProductSeo(p) {
    var name = L(p, 'name');
    var desc = L(p, 'shortDesc') || L(p, 'description') || '';
    var img = primaryImage(p) || '';
    var pageUrl = 'https://www.blackarrowksa.com' + productUrl(p);

    // Pre-rendered product pages already carry a keyword-rich title/description; only fill them in on the generic template.
    var generic = document.title.indexOf('Product') === 0;
    var metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc && generic) metaDesc.setAttribute('content', desc);

    var ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle && generic) ogTitle.setAttribute('content', name + ' — Black Arrow 3D');
    var ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogDesc && generic) ogDesc.setAttribute('content', desc);
    var ogUrl = document.querySelector('meta[property="og:url"]');
    if (ogUrl) ogUrl.setAttribute('content', pageUrl);
    var ogImg = document.querySelector('meta[property="og:image"]');
    if (ogImg && img) ogImg.setAttribute('content', absUrl(img));

    var canonical = document.querySelector('link[rel="canonical"]');
    if (canonical) canonical.setAttribute('href', pageUrl);

    var priceValue = (p.variants && p.variants.length) ? p.variants[0].price : p.price;
    var returnPolicy = {
      '@type': 'MerchantReturnPolicy',
      'applicableCountry': 'SA',
      'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow',
      'merchantReturnDays': 3,
      'merchantReturnLink': 'https://www.blackarrowksa.com/3d/returns/',
      'returnMethod': 'https://schema.org/ReturnByMail',
      'returnFees': 'https://schema.org/FreeReturn'
    };
    function shipOption(label, price, lo, hi) {
      return {
        '@type': 'OfferShippingDetails',
        'shippingLabel': label,
        'shippingRate': { '@type': 'MonetaryAmount', 'value': price, 'currency': 'SAR' },
        'shippingDestination': { '@type': 'DefinedRegion', 'addressCountry': 'SA' },
        'deliveryTime': { '@type': 'ShippingDeliveryTime', 'transitTime': { '@type': 'QuantitativeValue', 'minValue': lo, 'maxValue': hi, 'unitCode': 'DAY' } }
      };
    }
    var shippingDetails = [shipOption('Standard shipping', 30, 4, 5), shipOption('Fast shipping', 50, 2, 3)];
    var offers = (p.variants && p.variants.length)
      ? p.variants.map(function (v) {
          return {
            '@type': 'Offer',
            'price': v.price,
            'priceCurrency': p.currency || 'SAR',
            'availability': v.available === false ? 'https://schema.org/OutOfStock' : 'https://schema.org/InStock',
            'itemCondition': 'https://schema.org/NewCondition',
            'url': pageUrl,
            'hasMerchantReturnPolicy': returnPolicy,
            'shippingDetails': shippingDetails
          };
        })
      : {
          '@type': 'Offer',
          'price': priceValue,
          'priceCurrency': p.currency || 'SAR',
          'availability': p.available === false ? 'https://schema.org/OutOfStock' : 'https://schema.org/InStock',
          'itemCondition': 'https://schema.org/NewCondition',
          'url': pageUrl,
          'hasMerchantReturnPolicy': returnPolicy,
          'shippingDetails': shippingDetails
        };

    var jsonLd = {
      '@context': 'https://schema.org',
      '@type': 'Product',
      'name': name,
      'description': desc,
      'url': pageUrl,
      'sku': p.sku || p.id,
      'brand': { '@type': 'Brand', 'name': p.brand || 'Black Arrow 3D' },
      'image': (p.images || []).map(absUrl),
      'offers': offers
    };

    var breadcrumbLd = {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      'itemListElement': [
        { '@type': 'ListItem', 'position': 1, 'name': 'Black Arrow Venture', 'item': 'https://www.blackarrowksa.com/' },
        { '@type': 'ListItem', 'position': 2, 'name': 'Black Arrow 3D', 'item': 'https://www.blackarrowksa.com/3d/' },
        { '@type': 'ListItem', 'position': 3, 'name': 'Shop', 'item': 'https://www.blackarrowksa.com/3d/shop/' },
        { '@type': 'ListItem', 'position': 4, 'name': name, 'item': pageUrl }
      ]
    };

    var script = document.getElementById('pd-jsonld-product');
    if (!script) {
      script = document.createElement('script');
      script.type = 'application/ld+json';
      script.id = 'pd-jsonld-product';
      document.head.appendChild(script);
    }
    script.textContent = JSON.stringify(jsonLd);

    var bscript = document.getElementById('pd-jsonld-breadcrumb');
    if (!bscript) {
      bscript = document.createElement('script');
      bscript.type = 'application/ld+json';
      bscript.id = 'pd-jsonld-breadcrumb';
      document.head.appendChild(bscript);
    }
    bscript.textContent = JSON.stringify(breadcrumbLd);
  }

  function openImageZoom(src, name) {
    var overlay = document.querySelector('[data-b3d-zoom-overlay]');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'b3d-zoom-overlay';
      overlay.setAttribute('data-b3d-zoom-overlay', '');
      overlay.hidden = true;
      overlay.innerHTML = '<button type="button" class="b3d-zoom-overlay__close" aria-label="Close">&times;</button><img alt="">';
      document.body.appendChild(overlay);
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay || e.target.closest('.b3d-zoom-overlay__close')) closeImageZoom();
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !overlay.hidden) closeImageZoom();
      });
    }
    overlay.querySelector('img').src = src;
    overlay.querySelector('img').alt = name || '';
    overlay.hidden = false;
  }

  function closeImageZoom() {
    var overlay = document.querySelector('[data-b3d-zoom-overlay]');
    if (overlay) overlay.hidden = true;
  }

  function renderProductDetail(container) {
    var slug = new URLSearchParams(location.search).get('slug');
    if (!slug) {
      var pathMatch = location.pathname.match(/\/product\/([^\/]+)\/?$/);
      if (pathMatch) slug = decodeURIComponent(pathMatch[1]);
    }
    fetchProducts().then(function (products) {
      var p = products.filter(function (x) { return x.id === slug; })[0];
      if (!p) {
        container.innerHTML = '<div class="b3d-empty"><h2 style="color:#fff;">' + T('js_product_not_found') + '</h2><p>' + T('js_product_not_found_desc') + ' <a href="/3d/shop/" style="color:var(--clr-accent);">' + T('js_back_to_shop') + '</a></p></div>';
        return;
      }
      updateProductSeo(p);
      if (document.title.indexOf('Product') === 0) document.title = L(p, 'name') + ' — Black Arrow 3D';
      var crumbEl = document.querySelector('[data-b3d-crumb]');
      if (crumbEl) crumbEl.textContent = L(p, 'name');
      var specsHtml = LSpecs(p).map(function (row) {
        return '<tr><td>' + row[0] + '</td><td>' + row[1] + '</td></tr>';
      }).join('');
      var compatList = LCompat(p);
      var compatHtml = compatList.length
        ? '<div class="b3d-pd__compat"><h2>' + T('js_compatibility_heading') + '</h2><ul>' + compatList.map(function (c) { return '<li>' + c + '</li>'; }).join('') + '</ul></div>'
        : '';
      var images = (p.images && p.images.length) ? p.images : (p.image ? [p.image] : []);
      var heroImg = p.cardImage || (images.length ? images[0] : null);
      var thumbsHtml = images.length > 1
        ? '<div class="b3d-pd__thumbs">' + images.map(function (src, i) {
            var thumbLabel = T('js_view_image') + ' ' + (i + 1) + ' — ' + L(p, 'name');
            return '<button class="b3d-pd__thumb' + (src === heroImg ? ' is-active' : '') + '" data-thumb-src="' + src + '" aria-label="' + thumbLabel + '"><img src="' + src + '" alt="' + thumbLabel + '"></button>';
          }).join('') + '</div>'
        : '';
      var pdAvailable = p.available !== false;
      var mainVisual = heroImg ? '<img src="' + heroImg + '" alt="' + L(p, 'name') + '" data-pd-main-img>' : '<div class="b3d-card__visual-placeholder">' + T('js_product_image') + '</div>';

      var hasVariants = !!(p.variants && p.variants.length);
      var hasSwatches = hasVariants && p.variants.some(function (v) { return !!v.swatch; });
      var selectedVariant = 0;
      var variantSelectorHtml = hasVariants
        ? '<div class="b3d-pd__variants' + (hasSwatches ? ' b3d-pd__swatches' : '') + '" data-pd-variants style="display:flex;gap:' + (hasSwatches ? '10px' : '8px') + ';flex-wrap:wrap;margin-bottom:20px;align-items:center;">' +
            p.variants.map(function (v, i) {
              if (v.swatch) {
                return '<button type="button" class="b3d-swatch' + (v.available === false ? ' is-unavailable' : '') + '" data-variant-idx="' + i + '" aria-pressed="' + (i === 0) + '" title="' + LVariant(v) + (v.available === false ? ' (' + T('js_out_of_stock') + ')' : '') + '" style="background:' + v.swatch + ';"></button>';
              }
              return '<button type="button" class="b3d-quick-pill" data-variant-idx="' + i + '" aria-pressed="' + (i === 0) + '">' + LVariant(v) + '</button>';
            }).join('') +
          '</div>' +
          (hasSwatches ? '<div class="b3d-pd__swatch-label" data-pd-swatch-label style="color:rgba(255,255,255,.75);font-size:.85rem;margin:-12px 0 20px;">' + LVariant(p.variants[0]) + '</div>' : '')
        : '';
      var initialPriceHtml = hasVariants
        ? '<span class="b3d-price">' + money(p.variants[0].price, p.currency) + '</span>'
        : priceBlock(p);

      container.innerHTML = '' +
        '<div>' +
          '<div class="b3d-pd__visual' + (p.category === '3D Artwork' ? ' b3d-pd__visual--art' : '') + '" data-pd-zoom>' +
            cornerBadges(p) +
            mainVisual +
          '</div>' +
          thumbsHtml +
        '</div>' +
        '<div>' +
          '<div class="b3d-pd__cat">' + (p.brand ? p.brand + ' &middot; ' : '') + categoryLabel(p.category) + '</div>' +
          '<h1 class="b3d-pd__title">' + L(p, 'name') + '</h1>' +
          '<div class="b3d-pd__price" data-pd-price>' + initialPriceHtml + '</div>' +
          variantSelectorHtml +
          (statusBadge(p) ? '<div style="margin-bottom:16px;">' + statusBadge(p) + '</div>' : '') +
          '<p class="b3d-pd__desc">' + (L(p, 'description') || '') + '</p>' +
          '<div class="b3d-pd__actions">' +
            '<div class="b3d-qty">' +
              '<button type="button" data-pd-qty="minus" aria-label="' + T('js_qty_decrease') + '">−</button>' +
              '<input type="text" readonly value="1" data-pd-qty-val aria-label="' + T('js_qty_label') + '">' +
              '<button type="button" data-pd-qty="plus" aria-label="' + T('js_qty_increase') + '">+</button>' +
            '</div>' +
            '<button class="btn btn-primary" data-pd-add ' + ((pdAvailable || p.preorder) ? '' : 'disabled') + '>' + (p.preorder ? T('js_pre_order') : (pdAvailable ? T('js_add_to_cart') : T('js_out_of_stock'))) + '</button>' +
            (p.category === '3D Artwork' ? '' : '<button class="btn btn-outline" data-pd-compare="' + p.id + '">' + T('js_compare_btn') + '</button>') +
            '<a href="/3d/cart/" class="btn btn-outline">' + T('js_view_cart') + '</a>' +
          '</div>' +
          '<div class="b3d-pd__contact-actions">' +
            '<a href="https://wa.me/966560224715?text=' + encodeURIComponent('Hello! I have a question about ' + L(p, 'name') + '.') + '" target="_blank" rel="noopener noreferrer" class="btn btn-outline">' + T('js_ask_whatsapp') + '</a>' +
          '</div>' +
          (specsHtml ? '<table class="b3d-spec-table"><tbody>' + specsHtml + '</tbody></table>' : '') +
          compatHtml +
          (L(p, 'warranty') ? '<div class="b3d-pd__warranty"><h2>' + T('js_warranty_heading') + '</h2><p>' + L(p, 'warranty') + '</p></div>' : '') +
          '<div class="b3d-pd__shipreturn">' +
            '<div><strong>' + T('js_shipping_heading') + '</strong><p>' + T('js_shipping_desc') + '</p></div>' +
            '<div><strong>' + T('js_returns_heading') + '</strong><p>' + T('js_returns_desc_prefix') + ' <a href="/3d/returns/">' + T('footer_returns') + '</a> ' + T('js_returns_desc_suffix') + '</p></div>' +
          '</div>' +
        '</div>';

      container.querySelectorAll('[data-thumb-src]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          container.querySelectorAll('[data-thumb-src]').forEach(function (b) { b.classList.remove('is-active'); });
          btn.classList.add('is-active');
          var mainImg = container.querySelector('[data-pd-main-img]');
          if (mainImg) mainImg.src = btn.getAttribute('data-thumb-src');
        });
      });

      var zoomTarget = container.querySelector('[data-pd-zoom]');
      var mainImgEl = container.querySelector('[data-pd-main-img]');
      if (zoomTarget && mainImgEl) {
        zoomTarget.classList.add('is-zoomable');
        zoomTarget.setAttribute('role', 'button');
        zoomTarget.setAttribute('tabindex', '0');
        zoomTarget.setAttribute('aria-label', T('js_zoom_image'));
        var openZoom = function () { openImageZoom(mainImgEl.src, L(p, 'name')); };
        zoomTarget.addEventListener('click', openZoom);
        zoomTarget.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openZoom(); }
        });
      }

      var qtyInput = container.querySelector('[data-pd-qty-val]');
      container.querySelectorAll('[data-pd-qty]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var current = parseInt(qtyInput.value, 10) || 1;
          var next = btn.getAttribute('data-pd-qty') === 'plus' ? current + 1 : Math.max(1, current - 1);
          qtyInput.value = next;
        });
      });
      if (hasVariants) {
        container.querySelectorAll('[data-variant-idx]').forEach(function (btn) {
          btn.addEventListener('click', function () {
            container.querySelectorAll('[data-variant-idx]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
            btn.setAttribute('aria-pressed', 'true');
            selectedVariant = parseInt(btn.getAttribute('data-variant-idx'), 10);
            var v = p.variants[selectedVariant];
            container.querySelector('[data-pd-price]').innerHTML = '<span class="b3d-price">' + money(v.price, p.currency) + '</span>';
            var swatchLabel = container.querySelector('[data-pd-swatch-label]');
            if (swatchLabel) swatchLabel.textContent = LVariant(v);
            if (v.image) {
              var mainImg = container.querySelector('[data-pd-main-img]');
              if (mainImg) mainImg.src = v.image;
              container.querySelectorAll('[data-thumb-src]').forEach(function (t) {
                t.classList.toggle('is-active', t.getAttribute('data-thumb-src') === v.image);
              });
            }
          });
        });
      }

      var addBtn = container.querySelector('[data-pd-add]');
      if (addBtn) {
        addBtn.addEventListener('click', function () {
          var cartId = hasVariants ? lineId(p.id, selectedVariant) : p.id;
          addToCart(cartId, parseInt(qtyInput.value, 10) || 1);
          if (p.preorder) {
            location.href = '/3d/cart/';
            return;
          }
          var original = addBtn.textContent;
          addBtn.textContent = T('js_added');
          setTimeout(function () { addBtn.textContent = original; }, 1200);
        });
      }
      var compareBtn = container.querySelector('[data-pd-compare]');
      if (compareBtn) {
        compareBtn.addEventListener('click', function () {
          toggleCompare(p.id);
          compareBtn.textContent = getCompareList().indexOf(p.id) !== -1 ? T('js_added_to_compare') : T('js_compare_btn');
        });
      }

      renderRelated(container, products, p);
    });
  }

  function renderRelated(container, products, current) {
    var related = products.filter(function (p) {
      return p.id !== current.id && (p.category === current.category || p.brand === current.brand);
    }).slice(0, 4);
    var host = document.querySelector('[data-b3d-related]');
    if (!host) return;
    if (!related.length) { host.innerHTML = ''; return; }
    host.innerHTML = '<h2 class="b3d-related__title">' + T('js_related_products') + '</h2><div class="b3d-grid">' +
      related.map(productCard).join('') + '</div>';
    host.querySelectorAll('[data-add-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        addToCart(btn.getAttribute('data-add-id'), 1);
        btn.textContent = T('js_added');
      });
    });
  }

  /* ---------------- Homepage: "Which printer is right for you?" ----------------
     Curated persona -> product mapping. The persona copy is editorial judgment
     grounded in each product's own real specs/price (see 3d-i18n.js picker_why_*
     for the reasoning), not a claim about anything not already in the catalog
     data. Product names/prices are pulled live from fetchProducts() so this
     never drifts out of sync if pricing changes. */
  /* Reduced to the 4 clearest, non-overlapping use cases (was 7 — an
     uneven second row that repeated most of the catalog already shown
     elsewhere on the homepage). A "Compare All 3D Printers" link below
     covers visitors who want the full lineup side by side. */
  var PRINTER_PICKER = [
    { id: 'bambu-lab-a1-mini', tagKey: 'picker_tag_1', whyKey: 'picker_why_1' },
    { id: 'creality-sparkx-i7', tagKey: 'picker_tag_2', whyKey: 'picker_why_2' },
    { id: 'bambu-lab-a2l', tagKey: 'picker_tag_4', whyKey: 'picker_why_4' },
    { id: 'bambu-lab-h2c-combo', tagKey: 'picker_tag_7', whyKey: 'picker_why_7' }
  ];

  function renderPrinterPicker(container) {
    if (!container) return;
    fetchProducts().then(function (products) {
      var byId = {};
      products.forEach(function (p) { byId[p.id] = p; });
      var matched = PRINTER_PICKER.map(function (item) { return byId[item.id]; }).filter(Boolean);
      container.innerHTML = PRINTER_PICKER.map(function (item) {
        var p = byId[item.id];
        if (!p) return '';
        var img = primaryImage(p);
        return '' +
          '<div class="b3d-picker-card">' +
            (img ? '<div class="b3d-picker-card__visual"><img src="' + img + '" alt="' + L(p, 'name') + '" loading="lazy" width="300" height="300"></div>' : '') +
            '<div class="b3d-picker-card__body">' +
              '<span class="b3d-picker-card__tag">' + T(item.tagKey) + '</span>' +
              '<h3>' + L(p, 'name') + '</h3>' +
              '<p>' + T(item.whyKey) + '</p>' +
              '<div class="b3d-picker-card__meta">' + priceBlock(p) + '</div>' +
              '<a href="' + productUrl(p) + '" class="btn btn-outline">' + T('js_view_product') + '</a>' +
            '</div>' +
          '</div>';
      }).join('');
      injectItemListSeo(matched, 'home-jsonld-picker', 'Which Printer Is Right for You?');

      var compareAllBtn = document.querySelector('[data-b3d-compare-all]');
      if (compareAllBtn) {
        compareAllBtn.addEventListener('click', function () {
          try { localStorage.setItem(COMPARE_KEY, JSON.stringify(matched.map(function (p) { return p.id; }))); } catch (e) {}
        });
      }
    });
  }

  /* ---------------- Wishlist panel (account page) ---------------- */

  function renderWishlistPanel(container) {
    if (!container) return;
    var ids = getWishlist();
    if (!ids.length) return;
    fetchProducts().then(function (products) {
      var items = ids.map(function (id) { return products.filter(function (p) { return p.id === id; })[0]; }).filter(Boolean);
      if (!items.length) return;
      container.innerHTML = '<div class="b3d-grid">' + items.map(productCard).join('') + '</div>';
      container.querySelectorAll('[data-wishlist-id]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          toggleWishlist(btn.getAttribute('data-wishlist-id'));
          renderWishlistPanel(container);
        });
      });
      container.querySelectorAll('[data-compare-id]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          toggleCompare(btn.getAttribute('data-compare-id'));
          btn.classList.toggle('is-active');
        });
      });
      container.querySelectorAll('[data-add-id]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          addToCart(btn.getAttribute('data-add-id'), 1);
          var original = btn.textContent;
          btn.textContent = T('js_added');
          setTimeout(function () { btn.textContent = original; }, 1200);
        });
      });
    });
  }

  /* ---------------- Compare page ---------------- */

  function renderComparePage(container) {
    fetchProducts().then(function (products) {
      var ids = getCompareList();
      var items = ids.map(function (id) { return products.filter(function (p) { return p.id === id; })[0]; }).filter(Boolean);
      if (items.length < 2) {
        container.innerHTML = '<div class="b3d-empty"><h2 style="color:#fff;">' + T('js_nothing_to_compare_h2') + '</h2>' +
          '<p>' + T('js_nothing_to_compare_p') + '</p>' +
          '<a href="/3d/shop/" class="btn btn-primary">' + T('cart_go_shop') + '</a></div>';
        return;
      }

      function availabilityLabel(p) {
        if (p.preorder) return T('promo_preorder_badge');
        if (p.available === false) return T('js_out_of_stock');
        return T('promo_instock_badge');
      }

      // Build the row list from the specs each product actually has,
      // instead of a fixed list of labels that rarely match real spec
      // keys (which left most rows blank). A spec appears as a row if
      // at least one compared item has it.
      var specLabels = [];
      items.forEach(function (p) {
        LSpecs(p).forEach(function (row) {
          if (specLabels.indexOf(row[0]) === -1) specLabels.push(row[0]);
        });
      });

      function specLookup(p, label) {
        var row = LSpecs(p).filter(function (r) { return r[0] === label; })[0];
        return row ? row[1] : '—';
      }

      var html = '<table class="b3d-compare-table"><thead><tr><th></th>' +
        items.map(function (p) {
          return '<th><a href="' + productUrl(p) + '" style="color:#fff;">' + L(p, 'name') + '</a></th>';
        }).join('') + '</tr></thead><tbody>';

      html += '<tr><td>' + T('js_cmp_price') + '</td>' + items.map(function (p) { return '<td>' + money(p.price, p.currency) + '</td>'; }).join('') + '</tr>';
      html += '<tr><td>' + T('js_cmp_availability') + '</td>' + items.map(function (p) { return '<td>' + availabilityLabel(p) + '</td>'; }).join('') + '</tr>';
      html += '<tr><td>' + T('js_cmp_brand') + '</td>' + items.map(function (p) { return '<td>' + (p.brand || '—') + '</td>'; }).join('') + '</tr>';

      specLabels.forEach(function (label) {
        html += '<tr><td>' + label + '</td>' + items.map(function (p) { return '<td>' + specLookup(p, label) + '</td>'; }).join('') + '</tr>';
      });

      html += '</tbody></table>';
      container.innerHTML = html;
    });
  }

  /* ---------------- Announcement bar ---------------- */

  function initAnnouncementBar() {
    var bar = document.querySelector('[data-b3d-announce]');
    if (!bar) return;
    var track = bar.querySelector('[data-b3d-announce-track]');
    if (!track) return;
    if (!motionEnabled()) { bar.setAttribute('data-paused', 'true'); }
    document.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('[data-motion-toggle]')) {
        bar.setAttribute('data-paused', motionEnabled() ? 'false' : 'true');
      }
    });
  }

  /* ---------------- Promo slider ---------------- */

  /* Adds one slide per product flagged "newArrival": true in
     3d-products.json to the hero slider, so uploading a new product and
     setting that flag is enough to get it on the homepage slider — no
     HTML edit required. The first (workshop photo) slide already in the
     markup is left as a permanent brand anchor and never removed. */
  function populateHeroSlider() {
    var slider = document.querySelector('.b3d-slider--hero[data-b3d-slider]');
    if (!slider) return Promise.resolve();
    var track = slider.querySelector('[data-slider-track]');
    return fetchProducts().then(function (products) {
      var picks = products.filter(function (p) {
        return p.newArrival && p.available !== false;
      }).reverse().slice(0, 7);
      picks.forEach(function (p) {
        var img = primaryImage(p);
        if (!img) return;
        var slide = document.createElement('div');
        slide.className = 'b3d-slide b3d-slide--img-only';
        slide.setAttribute('data-slide', '');
        var alt = ((p.name || 'New arrival') + ' — new arrival').replace(/"/g, '&quot;');
        slide.innerHTML = '<a href="' + productUrl(p) + '"><img src="' + img + '" alt="' + alt + '" width="700" height="700" loading="lazy"></a>';
        track.appendChild(slide);
      });
    }).catch(function () {});
  }

  function initPromoSlider() {
    var slider = document.querySelector('[data-b3d-slider]');
    if (!slider) return;
    var track = slider.querySelector('[data-slider-track]');
    var slides = Array.prototype.slice.call(slider.querySelectorAll('[data-slide]'));
    var dotsWrap = slider.querySelector('[data-slider-dots]');
    if (!slides.length) return;
    var index = 0;
    var timer = null;

    dotsWrap.innerHTML = slides.map(function (_, i) {
      return '<button class="b3d-slider__dot' + (i === 0 ? ' is-active' : '') + '" data-dot="' + i + '" aria-label="Go to slide ' + (i + 1) + '"></button>';
    }).join('');

    function go(i) {
      index = (i + slides.length) % slides.length;
      track.style.transform = 'translateX(-' + (index * 100) + '%)';
      dotsWrap.querySelectorAll('[data-dot]').forEach(function (d, di) {
        d.classList.toggle('is-active', di === index);
      });
    }

    slider.querySelector('[data-slider-prev]').addEventListener('click', function () { go(index - 1); resetTimer(); });
    slider.querySelector('[data-slider-next]').addEventListener('click', function () { go(index + 1); resetTimer(); });
    dotsWrap.querySelectorAll('[data-dot]').forEach(function (d) {
      d.addEventListener('click', function () { go(parseInt(d.getAttribute('data-dot'), 10)); resetTimer(); });
    });

    slider.setAttribute('tabindex', '0');
    slider.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { go(index - 1); resetTimer(); }
      if (e.key === 'ArrowRight') { go(index + 1); resetTimer(); }
    });

    var startX = null;
    slider.addEventListener('pointerdown', function (e) { startX = e.clientX; });
    slider.addEventListener('pointerup', function (e) {
      if (startX == null) return;
      var dx = e.clientX - startX;
      if (Math.abs(dx) > 40) { go(dx < 0 ? index + 1 : index - 1); resetTimer(); }
      startX = null;
    });

    var paused = false;
    var interacting = false;

    function resetTimer() {
      /* Autoplay is gated on paused (the play/pause button) and interacting
         (hover/focus, below) but never permanently disabled by
         prefers-reduced-motion — a visitor with that preference still has
         a working play button, they just don't get an unrequested start. */
      if (timer) clearInterval(timer);
      if (paused || interacting) return;
      timer = setInterval(function () { go(index + 1); }, 3200);
    }

    slider.addEventListener('mouseenter', function () { interacting = true; resetTimer(); });
    slider.addEventListener('mouseleave', function () { interacting = false; resetTimer(); });
    slider.addEventListener('focusin', function () { interacting = true; resetTimer(); });
    slider.addEventListener('focusout', function () { interacting = false; resetTimer(); });

    var playPauseBtn = slider.querySelector('[data-slider-playpause]');
    if (playPauseBtn) {
      playPauseBtn.addEventListener('click', function () {
        paused = !paused;
        playPauseBtn.setAttribute('aria-pressed', String(paused));
        playPauseBtn.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
        playPauseBtn.innerHTML = paused ? '&#9654;' : '&#10074;&#10074;';
        if (paused) { if (timer) clearInterval(timer); } else { resetTimer(); }
      });
    }

    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      paused = true;
      if (playPauseBtn) {
        playPauseBtn.setAttribute('aria-pressed', 'true');
        playPauseBtn.setAttribute('aria-label', 'Play slideshow');
        playPauseBtn.innerHTML = '&#9654;';
      }
    }

    resetTimer();
  }

  window.BlackArrow3D = {
    fetchProducts: fetchProducts,
    renderGrid: renderGrid,
    renderCartPage: renderCartPage,
    renderProductDetail: renderProductDetail,
    renderComparePage: renderComparePage,
    initShopPage: initShopPage,
    getCart: getCart,
    cartCount: cartCount,
    updateCartBadges: updateCartBadges,
    getCompareList: getCompareList,
    toggleCompare: toggleCompare,
    getWishlist: getWishlist,
    isWishlisted: isWishlisted,
    toggleWishlist: toggleWishlist,
    renderWishlistPanel: renderWishlistPanel,
    motionEnabled: motionEnabled,
    CART_SVG: CART_SVG
  };

  function brandList() {
    return (window.BlackArrow3DBrands && window.BlackArrow3DBrands.length) ? window.BlackArrow3DBrands : [];
  }

  function initBrandNavMenu() {
    var menu = document.querySelector('[data-b3d-brand-menu]');
    if (!menu) return;
    var html = menu.innerHTML;
    brandList().forEach(function (brand) {
      html += '<a href="/3d/shop/?brand=' + encodeURIComponent(brand) + '">' + brand + '</a>';
    });
    menu.innerHTML = html;
  }

  function autoInit() {
    updateCartBadges();
    initMotionToggle();
    initAnnouncementBar();
    populateHeroSlider().then(initPromoSlider);
    initBrandNavMenu();

    var pickerGrid = document.querySelector('[data-b3d-picker-grid]');
    if (pickerGrid) renderPrinterPicker(pickerGrid);

    var featuredGrid = document.querySelector('[data-b3d-featured-grid]');
    if (featuredGrid) {
      fetchProducts().then(function (products) {
        var available = products.filter(function (p) { return p.available !== false; });
        var pinned = available.filter(function (p) { return !!p.featured; });
        var fresh = available.filter(function (p) { return !p.featured && p.newArrival; }).reverse();
        var rest = available.filter(function (p) { return !p.featured && !p.newArrival; });
        var featured = pinned.concat(fresh, rest).slice(0, 8);
        renderGrid(featured, featuredGrid);
        injectItemListSeo(featured, 'home-jsonld-featured', 'Featured Products');
      });
    }

    var searchForm = document.querySelector('[data-b3d-search-form]');
    if (searchForm) {
      searchForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var val = searchForm.querySelector('input').value.trim();
        location.href = '/3d/shop/' + (val ? '?q=' + encodeURIComponent(val) : '');
      });
    }

    var grid = document.querySelector('[data-b3d-grid]');
    if (grid) {
      fetchProducts().then(function (products) {
        injectItemListSeo(products, 'shop-jsonld-itemlist', 'Black Arrow 3D — Shop');
        initShopPage(products, {
          grid: grid,
          count: document.querySelector('[data-b3d-count]'),
          categoryTabs: document.querySelector('[data-b3d-cat-tabs]'),
          brandSelect: document.querySelector('[data-b3d-brand-select]'),
          searchInput: document.querySelector('[data-b3d-shop-search]'),
          sortSelect: document.querySelector('[data-b3d-sort]'),
          filterForm: document.querySelector('[data-b3d-filter-form]'),
          filterToggle: document.querySelector('[data-b3d-filter-toggle]'),
          filterPanel: document.querySelector('[data-b3d-filter-panel]'),
          filterApply: document.querySelector('[data-b3d-filter-apply]'),
          filterClear: document.querySelector('[data-b3d-filter-clear]'),
          pagination: document.querySelector('[data-b3d-pagination]'),
          printerTypeSelect: document.querySelector('[data-b3d-printer-type]'),
          buildVolumeSelect: document.querySelector('[data-b3d-build-volume]'),
          filamentMaterialSelect: document.querySelector('[data-b3d-filament-material]'),
          accessoryCompatSelect: document.querySelector('[data-b3d-accessory-compat]')
        });
      });
    }

    var productContainer = document.querySelector('[data-b3d-product]');
    if (productContainer) renderProductDetail(productContainer);

    var compareContainer = document.querySelector('[data-b3d-compare]');
    if (compareContainer) renderComparePage(compareContainer);

    var cartList = document.querySelector('[data-b3d-cart-list]');
    if (cartList) {
      var summary = document.querySelector('[data-b3d-cart-summary]');
      var empty = document.querySelector('[data-b3d-cart-empty]');
      initCoupon(summary);
      renderCartPage(cartList, summary, empty);
      initPaymentMethods(document.querySelector('[data-b3d-payment]'));
      initShippingMethods(document.querySelector('[data-b3d-checkout]'));
      initCheckoutAuth(document.querySelector('[data-b3d-checkout]'));
      initCheckoutSubmit(document.querySelector('#b3d-checkout-form'));
    }
  }

  document.addEventListener('DOMContentLoaded', autoInit);
})();
