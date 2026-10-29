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
    pushAddToCartEvent(id, qty);
  }

  /* GA4/GTM ecommerce event — best-effort: if the product isn't in the
     local cache yet (fetchProducts() hasn't resolved), it's skipped rather
     than guessed at. */
  function pushAddToCartEvent(id, qty) {
    try {
      var parsed = parseLineId(id);
      var product = __b3dProductsById[parsed.productId];
      if (!product) return;
      var variant = (parsed.variantIndex != null && product.variants) ? product.variants[parsed.variantIndex] : null;
      var price = variant ? variant.price : currentPrice(product);
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'add_to_cart',
        ecommerce: {
          currency: product.currency || 'SAR',
          value: price * qty,
          items: [{
            item_id: parsed.productId,
            item_name: L(product, 'name'),
            item_variant: variant ? LVariant(variant) : undefined,
            item_brand: product.brand,
            item_category: product.category,
            price: price,
            quantity: qty
          }]
        }
      });
      pushSnapEvent('ADD_CART', {
        price: price * qty,
        currency: product.currency || 'SAR',
        item_ids: [parsed.productId],
        item_category: product.category,
        number_items: qty
      });
    } catch (e) {}
  }

  // Builds the Snap Pixel item list from whatever is still in the cart —
  // called right before the cart is cleared, on every successful checkout path.
  function snapCartPayload() {
    var cart = getCart();
    var ids = Object.keys(cart);
    var price = 0, items = 0, itemIds = [], category = null;
    ids.forEach(function (id) {
      var parsed = parseLineId(id);
      var product = __b3dProductsById[parsed.productId];
      if (!product) return;
      var variant = (parsed.variantIndex != null && product.variants) ? product.variants[parsed.variantIndex] : null;
      var unit = variant ? variant.price : currentPrice(product);
      var qty = cart[id];
      price += unit * qty;
      items += qty;
      itemIds.push(parsed.productId);
      if (!category) category = product.category;
    });
    return { price: price, currency: 'SAR', item_ids: itemIds, item_category: category, number_items: items };
  }

  // Snap Pixel — mirrors the GA4/GTM push above, best-effort (never blocks
  // the cart/checkout flow if the pixel script failed to load or is blocked).
  function pushSnapEvent(name, params) {
    try { if (window.snaptr) window.snaptr('track', name, params || {}); } catch (e) {}
  }

  function pushLeadEvent(leadType) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'generate_lead', lead_type: leadType, page_path: location.pathname });
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

  /* ---------------- Pick-your-own bundles ----------------
     A bundle product (p.bundlePick = { count, fromIds }) has no real
     variants — the buyer picks N other catalog products on its product
     page instead. Picks are kept separately from the cart (which only
     stores lineId -> qty) in their own localStorage key, keyed by the
     bundle's product id. */
  var BUNDLE_PICKS_KEY = 'b3d_bundle_picks_v1';

  function getAllBundlePicks() {
    try {
      var raw = localStorage.getItem(BUNDLE_PICKS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) { return {}; }
  }

  function getBundlePicks(productId) {
    return getAllBundlePicks()[productId] || [];
  }

  function setBundlePicks(productId, ids) {
    var all = getAllBundlePicks();
    all[productId] = ids;
    try { localStorage.setItem(BUNDLE_PICKS_KEY, JSON.stringify(all)); } catch (e) {}
  }

  /* ---------------- Data ---------------- */

  var __b3dProductsById = {};
  // Stock from the CRM's Website Inventory tab. Once a product has any row
  // there, the CRM decides every option of it: in stock only if listed with
  // quantity above 0 (or blank) and not switched off. Products with no rows,
  // or a failed lookup, keep the catalog's own flags.
  function fetchCrmStock() {
    return fetch('/api/availability/').then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { return (d && d.rows) || []; })
      .catch(function () { return []; });
  }

  // Same rules as api/_lib/crm-catalog.js (what checkout charges): a row's
  // price replaces the catalog price; its old price is the crossed-out one.
  function applyCrmStock(rows) {
    var byProduct = {};
    rows.forEach(function (row) {
      var key = String(row.variant || '').trim().toLowerCase();
      (byProduct[row.id] = byProduct[row.id] || {})[key] = row;
    });
    Object.keys(byProduct).forEach(function (id) {
      var p = __b3dProductsById[id];
      if (!p) return;
      var crm = byProduct[id];
      var whole = crm[''];
      if (p.variants && p.variants.length) {
        p.variants.forEach(function (v) {
          var key = String(v.label || '').trim().toLowerCase();
          var row = crm[key];
          v.available = row ? row.available !== false : !!(whole && whole.available !== false);
          if (row && row.price != null) {
            v.price = row.price;
            if (row.oldPrice != null && row.oldPrice > row.price) v.oldPrice = row.oldPrice;
            else delete v.oldPrice;
          }
        });
        p.available = !(whole && whole.available === false) && p.variants.some(function (v) { return v.available !== false; });
        // Pre-order (CRM: none in hand). The whole product reads Pre-order when every option
        // you can buy is pre-order; otherwise only the picked option's button says so.
        p.variants.forEach(function (v) {
          var row = crm[String(v.label || '').trim().toLowerCase()];
          v.preorder = !!(row ? row.preorder : whole && whole.preorder);
        });
        var buyable = p.variants.filter(function (v) { return v.available !== false; });
        if (buyable.length && buyable.every(function (v) { return v.preorder; })) p.preorder = true;
      } else {
        p.available = !!(whole && whole.available !== false);
        if (whole && whole.preorder) p.preorder = true;
        if (whole && whole.price != null) {
          if (whole.oldPrice != null && whole.oldPrice > whole.price) {
            p.price = whole.oldPrice; p.onSale = true; p.salePrice = whole.price;
          } else {
            p.price = whole.price; p.onSale = false; delete p.salePrice;
          }
        }
      }
    });
    // Same as the server: a shop product missing from the CRM's Website Inventory is out of
    // stock (3D Artwork is printed to order; kits and pick-bundles follow their parts).
    if (rows.length) {
      Object.keys(__b3dProductsById).forEach(function (id) {
        var p = __b3dProductsById[id];
        if (byProduct[id] || p.category === '3D Artwork' || p.kit || p.bundlePick) return;
        p.available = false;
        p.preorder = false;
        (p.variants || []).forEach(function (v) { v.available = false; });
      });
    }
  }

  function fetchProducts() {
    return Promise.all([
      fetch(DATA_URL).then(function (r) { return r.json(); }),
      fetchCrmStock()
    ]).then(function (res) {
      var data = res[0];
      var list = data.products || [];
      list.forEach(function (p) { __b3dProductsById[p.id] = p; });
      applyCrmStock(res[1]);
      // A kit is only in stock while every part of it is.
      list.forEach(function (p) {
        if (!p.kit) return;
        var ok = p.kit.every(function (it) {
          var c = __b3dProductsById[it.id];
          if (!c || c.available === false) return false;
          if (it.variant != null) return !!(c.variants && c.variants[it.variant] && c.variants[it.variant].available !== false);
          return true;
        });
        if (!ok) p.available = false;
      });
      return list;
    });
  }

  function money(n, currency) {
    if ((currency || 'SAR') === 'SAR') {
      return n.toLocaleString('en-US') + ' <small class="b3d-riyal" aria-hidden="true">' + RIYAL_SVG + '</small><span class="sr-only"> SAR</span>';
    }
    return n.toLocaleString('en-US') + ' <small>' + currency + '</small>';
  }

  /* The first option the buyer can actually pick (not out of stock) with a photo:
     its photo leads the card and product page, so an unavailable option never sets the picture. */
  function firstAvailableVariantImage(p) {
    if (!p.variants || !p.variants.length) return null;
    for (var i = 0; i < p.variants.length; i++) {
      if (p.variants[i].available !== false && p.variants[i].image) return p.variants[i].image;
    }
    return null;
  }

  function primaryImage(p) {
    if (p.cardImage) return p.cardImage;
    var vImg = firstAvailableVariantImage(p);
    if (vImg) return vImg;
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

  /* Size of every product photo that has small copies (<name>-500w.webp and
     <name>-160w.webp) made by scripts/build_3d_image_sizes.py — so srcset
     describes real widths and the browser can pick the smallest file it needs. */
  /* BEGIN IMG_SIZES (generated by scripts/build_3d_image_sizes.py) */
  var IMG_SIZES = {'a1-extruder-unit-01.webp': [1200, 1200], 'a1-extruder-unit-02.webp': [1200, 1200], 'air-filter-lamp-01.webp': [1100, 1466], 'air-filter-lamp-02.webp': [1100, 1466], 'air-filter-lamp-03.webp': [1100, 1466], 'air-filter-lamp-04.webp': [1100, 1466], 'anycubic-kobra3max-01.webp': [600, 600], 'anycubic-kobra3max-02.webp': [1100, 1100], 'anycubic-kobra3max-03.webp': [1100, 1100], 'anycubic-kobra3max-04.webp': [1100, 1100], 'anycubic-kobra3max-05.webp': [1100, 1100], 'anycubic-kobra3max-06.webp': [1100, 1100], 'anycubic-kobra3max-combo.webp': [1100, 1100], 'bambu-a1-01.webp': [900, 900], 'bambu-a1-02.webp': [1024, 1024], 'bambu-a1-03.webp': [1200, 1200], 'bambu-a1-04.webp': [1063, 1063], 'bambu-a1-05.webp': [1200, 1200], 'bambu-a1-06.webp': [1200, 1200], 'bambu-a1-mini-ams-combo.webp': [1144, 926], 'bambu-a1-mini-lifestyle.webp': [700, 700], 'bambu-a1-mini-main.webp': [599, 800], 'bambu-a1-mini-nozzle-light.webp': [1200, 1200], 'bambu-a1-mini-screen.webp': [1000, 1000], 'bambu-a2l-01.webp': [1200, 1200], 'bambu-a2l-02.webp': [1200, 1200], 'bambu-a2l-03.webp': [1200, 1200], 'bambu-a2l-04.webp': [1200, 1200], 'bambu-a2l-05.webp': [1040, 1040], 'bambu-a2l-06.webp': [1200, 1200], 'bambu-a2l-07.webp': [1200, 1122], 'bambu-a2l-08.webp': [1200, 1200], 'bambu-ams-2-pro-01.webp': [1200, 1200], 'bambu-ams-2-pro-02.webp': [1200, 1200], 'bambu-ams-2-pro-03.webp': [1200, 1200], 'bambu-ams-2-pro-04.webp': [1200, 1200], 'bambu-ams-ht-01.webp': [1200, 1200], 'bambu-ams-ht-02.webp': [1200, 1200], 'bambu-ams-ht-03.webp': [1200, 1200], 'bambu-ams-ht-04.webp': [1200, 1200], 'bambu-ams-lite-01.webp': [1200, 1200], 'bambu-ams-lite-02.webp': [1200, 1200], 'bambu-ams-lite-03.webp': [1200, 1200], 'bambu-h2c-01.webp': [763, 759], 'bambu-h2c-02.webp': [810, 881], 'bambu-h2c-03.webp': [890, 897], 'bambu-h2c-04.webp': [744, 851], 'bambu-h2d-01.webp': [1200, 1200], 'bambu-h2d-02.webp': [1200, 1200], 'bambu-h2d-03.webp': [1200, 1200], 'bambu-h2d-04.webp': [1200, 1200], 'bambu-h2d-05.webp': [1200, 1200], 'bambu-h2d-06.webp': [1200, 1200], 'bambu-h2d-07.webp': [1200, 1200], 'bambu-h2s-01.webp': [1200, 1200], 'bambu-h2s-02.webp': [1200, 1200], 'bambu-h2s-03.webp': [1200, 1200], 'bambu-h2s-04.webp': [1200, 1200], 'bambu-h2s-05.webp': [1200, 1200], 'bambu-h2s-06.webp': [1200, 1200], 'bambu-h2s-07.webp': [1200, 1200], 'bambu-hotend-a1-01.webp': [1200, 1200], 'bambu-hotend-a1-02.webp': [1200, 1200], 'bambu-hotend-a1-03.webp': [1200, 1200], 'bambu-hotend-a1-04.webp': [1200, 1200], 'bambu-hotend-a1-05.webp': [1200, 1200], 'bambu-hotend-a1-06.webp': [1200, 446], 'bambu-hotend-a1-07.webp': [1200, 520], 'bambu-p1s-01.webp': [800, 800], 'bambu-p1s-02.webp': [800, 800], 'bambu-p1s-03.webp': [800, 800], 'bambu-p1s-04.webp': [800, 800], 'bambu-p1s-05.webp': [800, 800], 'bambu-p2s-01.webp': [892, 864], 'bambu-p2s-02.webp': [832, 905], 'bambu-p2s-03.webp': [1200, 1200], 'bambu-p2s-04.webp': [1200, 1200], 'bambu-p2s-05.webp': [1200, 1200], 'bambu-x1e-01.webp': [1200, 1200], 'bambu-x1e-02.webp': [1200, 1200], 'bambu-x1e-03.webp': [1200, 1200], 'bambu-x1e-04.webp': [1200, 1200], 'bambu-x1e-05.webp': [1200, 1200], 'bambu-x2d-01.webp': [1200, 1200], 'bambu-x2d-02.webp': [1200, 1200], 'bambu-x2d-03.webp': [1200, 1200], 'bambu-x2d-04.webp': [1200, 1200], 'bambu-x2d-05.webp': [1200, 1200], 'bambu-x2d-06.webp': [1200, 1200], 'bambu-x2d-07.webp': [1200, 1200], 'bambu-x2d-08.webp': [1200, 1200], 'creality-sparkx-i7-01.webp': [1200, 1200], 'creality-sparkx-i7-02.webp': [1200, 1200], 'creality-sparkx-i7-03.webp': [1200, 1200], 'creality-sparkx-i7-04.webp': [1200, 1200], 'creality-sparkx-i7-05.webp': [1200, 1200], 'creality-sparkx-i7-06.webp': [1200, 1200], 'creality-sparkx-i7-combo.webp': [1100, 445], 'custom-3d-artwork-promo.webp': [1062, 965], 'elegoo-cc2-01.webp': [1024, 1024], 'elegoo-cc2-02.webp': [1200, 1200], 'elegoo-cc2-03.webp': [1024, 1126], 'elegoo-cc2-04.webp': [1050, 1050], 'elegoo-cc2-05.webp': [933, 933], 'elegoo-cc2-06.webp': [1024, 1024], 'elegoo-cc2-07.webp': [1128, 1200], 'elegoo-cc2-08.webp': [1200, 1200], 'elegoo-cc2-09.webp': [1200, 1150], 'f1-car-3d-model-01.webp': [900, 900], 'f1-car-3d-model-02.webp': [900, 900], 'filament-cutter-lever-01.webp': [1200, 1200], 'filament-cutter-lever-02.webp': [1200, 1200], 'flashforge-adv5m-01.webp': [1200, 1200], 'flashforge-c5pro-01.webp': [1200, 1200], 'flmnt-pla-black.webp': [1200, 1200], 'flmnt-pla-blue.webp': [1024, 1024], 'flmnt-pla-gray.webp': [1024, 1024], 'flmnt-pla-green.webp': [1024, 1024], 'flmnt-pla-orange.webp': [1200, 1200], 'flmnt-pla-red.webp': [1024, 1024], 'flmnt-pla-white.webp': [1200, 1200], 'flmnt-pla-yellow.webp': [1024, 1024], 'green-knit-cap-01.webp': [543, 724], 'green-knit-cap-02.webp': [543, 724], 'gta-vi-duo-statue-01.webp': [1198, 896], 'gta-vi-ps5-controller-stand-02.webp': [880, 1187], 'gta-vi-ps5-controller-stand-studio.webp': [1196, 896], 'hotend-heating-a1-01.webp': [1200, 1200], 'hotend-heating-a1-02.webp': [800, 800], 'infinity-cube-fidget-toy-promo.webp': [1200, 1500], 'kingroon-petg-basic-blue.webp': [713, 713], 'kingroon-petg-basic-green.webp': [713, 713], 'kingroon-petg-basic-orange.webp': [713, 713], 'kingroon-petg-basic-red.webp': [713, 713], 'kingroon-petg-basic-yellow.webp': [713, 713], 'kingroon-petg-dark-blue.webp': [969, 899], 'kingroon-petg-fluorescent-blue.webp': [933, 900], 'kingroon-petg-fluorescent-yellow.webp': [968, 899], 'kingroon-petg-gray.webp': [1028, 899], 'kingroon-petg-pink.webp': [901, 900], 'kingroon-petg-silver.webp': [1010, 900], 'kingroon-petg-sky-blue.webp': [848, 899], 'kingroon-petg-transparent-green.webp': [900, 900], 'kingroon-petg-transparent-pink.webp': [900, 900], 'kingroon-petg-transparent-red.webp': [949, 899], 'kingroon-petg-transparent.webp': [888, 899], 'kingroon-pla-black.webp': [1083, 899], 'kingroon-pla-blue.webp': [978, 900], 'kingroon-pla-brown.webp': [900, 900], 'kingroon-pla-gold.webp': [881, 899], 'kingroon-pla-gray.webp': [949, 896], 'kingroon-pla-green.webp': [900, 900], 'kingroon-pla-orange.webp': [1051, 899], 'kingroon-pla-pink.webp': [980, 900], 'kingroon-pla-purple.webp': [1079, 900], 'kingroon-pla-red.webp': [1120, 900], 'kingroon-pla-silver.webp': [974, 899], 'kingroon-pla-skin.webp': [880, 899], 'kingroon-pla-sky-blue.webp': [1007, 899], 'kingroon-pla-transparent.webp': [1132, 900], 'kingroon-pla-white.webp': [884, 899], 'kingroon-pla-yellow.webp': [1057, 899], 'leonidas-kick-edge-display-01.webp': [1000, 750], 'leonidas-kick-edge-display-02.webp': [1000, 1333], 'leonidas-kick-edge-display-03.webp': [1000, 1333], 'luffy-keychain-promo.webp': [1120, 960], 'man-push-ps5-controller-stand-01.webp': [1000, 1000], 'man-push-ps5-controller-stand-02.webp': [1000, 1000], 'mustang-gt-black.webp': [1254, 1254], 'mustang-gt-green.webp': [1254, 1254], 'mustang-gt-promo.webp': [1254, 1254], 'mustang-gt-red.webp': [1254, 1254], 'mustang-gt-yellow.webp': [1254, 1254], 'naruto-leaf-keychain-promo.webp': [1200, 1200], 'naruto-portrait-plaque-black.webp': [1254, 1254], 'naruto-portrait-plaque-green.webp': [1254, 1254], 'naruto-portrait-plaque-red.webp': [1254, 1254], 'naruto-portrait-plaque-yellow.webp': [1254, 1254], 'national-day-key-holder-promo.webp': [1254, 1254], 'one-piece-jolly-roger-keychain-01.webp': [960, 720], 'one-piece-jolly-roger-keychain-02.webp': [1000, 1500], 'one-piece-luffy-silhouette-lamp.webp': [896, 1174], 'one-piece-sanji-silhouette-lamp.webp': [896, 1198], 'one-piece-sword-keychain-group.webp': [1043, 1400], 'one-piece-sword-keychain-luffy.webp': [1254, 1254], 'one-piece-sword-keychain-sanji.webp': [1254, 1254], 'one-piece-sword-keychain-zoro.webp': [1254, 1254], 'one-piece-zoro-silhouette-lamp.webp': [896, 1196], 'oni-controller-stand-01.webp': [1280, 960], 'oni-controller-stand-02.webp': [1280, 960], 'oni-controller-stand-03.webp': [1280, 960], 'oni-controller-stand-04.webp': [1280, 960], 'oni-controller-stand-05.webp': [1280, 960], 'oni-controller-stand-06.webp': [1280, 960], 'oni-controller-stand-07-promo.webp': [1254, 1254], 'oni-mask-v2-ps5-controller-stand-1.webp': [1007, 847], 'oni-mask-v2-ps5-controller-stand-2.webp': [946, 840], 'oni-mask-v2-ps5-controller-stand-3.webp': [975, 802], 'overthing-01.webp': [1000, 1000], 'pillow-controller-stand-both.webp': [1447, 1087], 'pillow-controller-stand-grey.webp': [727, 1027], 'pillow-controller-stand-orange.webp': [610, 950], 'ps-symbols-controller-stand-01.webp': [1000, 1000], 'ps-symbols-controller-stand-02.webp': [1000, 1000], 'ps5-dual-football-stand-01.webp': [1200, 1200], 'question-block-stand-01.webp': [1050, 1400], 'question-block-stand-02.webp': [1254, 1254], 'saudi-map-decor-promo.webp': [1254, 1254], 'saudi-map-hanging-decor-black.webp': [1254, 1254], 'saudi-map-hanging-decor-red.webp': [1254, 1254], 'saudi-map-hanging-decor-white.webp': [1254, 1254], 'saudi-map-hanging-decor-yellow.webp': [1254, 1254], 'saudi-map-keychain-black.webp': [1254, 1254], 'saudi-map-keychain-promo.webp': [1254, 1254], 'saudi-map-keychain-red.webp': [1254, 1254], 'saudi-map-keychain-white.webp': [1254, 1254], 'saudi-map-keychain-yellow.webp': [1254, 1254], 'saudi-palm-swords-keychain-promo.webp': [1254, 1254], 'saudi-palm-swords-keychain-red.webp': [1254, 1254], 'saudi-palm-swords-keychain-yellow.webp': [1254, 1254], 'saudi-riyal-keychain-promo.webp': [1254, 1254], 'saudi-riyal-keychain-red.webp': [1254, 1254], 'saudi-riyal-keychain-yellow.webp': [1254, 1254], 'snapmaker-u1-01.webp': [1037, 1037], 'snapmaker-u1-02.webp': [900, 900], 'snapmaker-u1-03.webp': [900, 900], 'snapmaker-u1-04.webp': [900, 900], 'snapmaker-u1-05.webp': [900, 900], 'snapmaker-u1-06.webp': [900, 900], 'snapmaker-u1-07.webp': [900, 900], 'snapmaker-u1-08.webp': [900, 900], 'snapmaker-u1-09.webp': [900, 900], 'snapmaker-u1-10.webp': [900, 900], 'snapmaker-u1-11.webp': [900, 900], 'snapmaker-u1-12.webp': [1200, 728], 'spiderman-mask-pen-holder-black.webp': [1254, 1254], 'spiderman-mask-pen-holder-gray.webp': [1254, 1254], 'sports-duffel-bag-keychain-black.webp': [1000, 750], 'sports-duffel-bag-keychain-group.webp': [1000, 750], 'sports-duffel-bag-keychain-pink.webp': [1000, 750], 'sports-duffel-bag-keychain-purple.webp': [1000, 750], 'straw-hat-controller-stand-01.webp': [1100, 1100], 'straw-hat-controller-stand-02.webp': [1100, 1100], 'synapse-usb-lamp-01.webp': [1000, 1249], 'toji-edge-sitter-figure-01.webp': [659, 1133], 'toji-edge-sitter-figure-02.webp': [1070, 795], 'uchiha-keychain-01.webp': [600, 600], 'uchiha-keychain-02.webp': [600, 600], 'uchiha-keychain-03.webp': [600, 600], 'uchiha-keychain-04.webp': [600, 600], 'uchiha-keychain-05.webp': [600, 600], 'uchiha-keychain-06.webp': [600, 600], 'uchiha-keychain-07.webp': [600, 600], 'uchiha-keychain-08.webp': [600, 600], 'uchiha-keychain-09.webp': [600, 600]};
  /* END IMG_SIZES */
  function imgSize(src) { return src ? IMG_SIZES[src.split('/').pop()] : null; }
  function smallImg(src, w) { return src.replace(/\.(webp|jpe?g|png)$/i, '-' + w + 'w.webp'); }
  function imgSrcset(src) {
    var d = imgSize(src);
    return d ? smallImg(src, 500) + ' 500w, ' + src + ' ' + d[0] + 'w' : '';
  }
  function setMainImg(el, src) {
    var set = imgSrcset(src), d = imgSize(src);
    if (set) el.setAttribute('srcset', set); else el.removeAttribute('srcset');
    if (d) { el.setAttribute('width', d[0]); el.setAttribute('height', d[1]); } else { el.removeAttribute('width'); el.removeAttribute('height'); }
    el.src = src;
  }
  function thumbSrc(src) { return imgSize(src) ? smallImg(src, 160) : src; }

  function visual(p) {
    var img = primaryImage(p);
    if (!img) return '<div class="b3d-card__visual-placeholder">' + T('js_product_image') + '</div>';
    var set = imgSrcset(img);
    var srcsetAttr = set ? ' srcset="' + set + '" sizes="(max-width: 480px) 90vw, 300px"' : '';
    return '<img src="' + img + '"' + srcsetAttr + ' alt="' + L(p, 'name') + '" loading="lazy" decoding="async" width="400" height="400">';
  }

  // Stock badge for the product, or for the option currently picked (v), so the picture never says
  // In Stock while the chosen option is out of stock.
  function stockState(p, v) {
    if (p.preorder || (v && v.preorder && v.available !== false)) return 'pre';
    if (p.available === false || (v && v.available === false)) return 'out';
    return 'in';
  }
  var STOCK_LABEL = { pre: 'js_pre_order', out: 'js_out_of_stock', in: 'js_in_stock' };
  function statusBadge(p, v) {
    var st = stockState(p, v);
    return '<span class="b3d-stock-badge b3d-stock-badge--' + st + '">' + T(STOCK_LABEL[st]) + '</span>';
  }
  function syncStockBadge(scope, p, v) {
    var badge = scope && p && scope.querySelector('.b3d-stock-badge');
    if (!badge) return;
    var st = stockState(p, v);
    badge.className = 'b3d-stock-badge b3d-stock-badge--' + st;
    badge.textContent = T(STOCK_LABEL[st]);
  }

  // A variant may carry `oldPrice` (the pre-offer price): it renders as an
  // offer, with the old price struck through next to the new one.
  function variantPriceHtml(v, p) {
    if (v.oldPrice && v.oldPrice > v.price) {
      return '<span class="b3d-price b3d-price--sale">' + money(v.price, p.currency) +
        '</span><span class="b3d-price-was">' + money(v.oldPrice, p.currency) + '</span>';
    }
    return '<span class="b3d-price">' + money(v.price, p.currency) + '</span>';
  }

  // The price a customer actually pays for the product's base listing.
  function currentPrice(p) {
    if (p.variants && p.variants.length) {
      var ok = p.variants.filter(function (v) { return v.available !== false; });
      return Math.min.apply(null, (ok.length ? ok : p.variants).map(function (v) { return v.price; }));
    }
    return (p.onSale && p.salePrice != null) ? p.salePrice : p.price;
  }

  /* Prices written into page text (blog posts, guides, tables) are marked
     <span data-b3d-price="product-id|Option label">2,699</span> (option optional). They show the
     live price - the CRM's Website Inventory price when it sets one - as soon as the page loads.
     scripts/sync_crm_prices.py writes the same price into the HTML every night, so the page
     source (what Google reads) matches. Same rule there: an option's price, else the product's
     lowest option, else its sale or normal price. */
  function livePriceOf(key) {
    var cut = key.indexOf('|');
    var p = __b3dProductsById[cut < 0 ? key : key.slice(0, cut)];
    if (!p) return null;
    var label = cut < 0 ? '' : key.slice(cut + 1).trim().toLowerCase();
    if (label) {
      var v = (p.variants || []).filter(function (x) { return String(x.label || '').trim().toLowerCase() === label; })[0];
      return v ? v.price : null;
    }
    if (p.variants && p.variants.length) return Math.min.apply(null, p.variants.map(function (x) { return x.price; }));
    return (p.onSale && p.salePrice != null) ? p.salePrice : p.price;
  }

  function paintLivePrices(els) {
    Array.prototype.forEach.call(els, function (el) {
      var n = livePriceOf(el.getAttribute('data-b3d-price') || '');
      if (typeof n !== 'number' || !isFinite(n)) return;
      el.textContent = n % 1 ? n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : n.toLocaleString('en-US');
    });
  }

  function priceBlock(p) {
    if (p.variants && p.variants.length) {
      // Price only from options the buyer can pick; an out-of-stock option never sets the price shown.
      var pool = p.variants.filter(function (v) { return v.available !== false; });
      if (!pool.length) pool = p.variants;
      var prices = pool.map(function (v) { return v.price; });
      var min = Math.min.apply(null, prices);
      var allSame = prices.every(function (pr) { return pr === min; });
      if (allSame) return variantPriceHtml(pool[0], p);
      return '<span class="b3d-price-was" style="text-decoration:none;display:block;cursor:help;" title="' + T('js_from_tooltip') + '">' + T('js_from') + '</span><span class="b3d-price">' + money(min, p.currency) + '</span>';
    }
    if (p.onSale && p.salePrice != null) {
      return '<span class="b3d-price b3d-price--sale">' + money(p.salePrice, p.currency) +
        '</span><span class="b3d-price-was">' + money(p.price, p.currency) + '</span>';
    }
    return '<span class="b3d-price">' + money(p.price, p.currency) + '</span>';
  }

  // Real per-category fact, not a blanket claim: only the printers themselves carry a
  // manufacturer's factory warranty; everything Black Arrow prints or supplies otherwise
  // is replaced if it arrives damaged (see /3d/returns/), never described as "warrantied".
  function trustRowHtml(p) {
    var middle = p.category === '3D Printers'
      ? '<span>&#128737;&#65039; ' + T('trust_warranty') + '</span>'
      : '<span>&#128260; ' + T('trust_damaged_replace') + '</span>';
    return '<div class="b3d-pd__trust">' +
      '<span>&#128666; ' + T('trust_delivery') + '</span>' + middle +
      '<span>&#128274; ' + T('trust_payment') + '</span>' +
    '</div>';
  }

  // The actual SAR amount saved, from the real old/new prices already in the data — never a made-up percentage.
  function saveAmountHtml(was, now, currency) {
    if (!(was > now)) return '';
    var diff = Math.round((was - now) * 100) / 100;
    return '<span class="b3d-pd__save">' + T('js_you_save') + ' ' + money(diff, currency) + '</span>';
  }

  function lineId(productId, variantIndex) {
    return variantIndex == null ? productId : productId + '::' + variantIndex;
  }

  function parseLineId(id) {
    var parts = id.split('::');
    return { productId: parts[0], variantIndex: parts.length > 1 ? parseInt(parts[1], 10) : null };
  }

  function bestSellerLabel(rank) {
    if (rank === 1) return T('js_best_seller_badge');
    if (rank === 2) return T('js_best_seller_badge_2');
    return T('js_best_seller_badge_n').replace('{n}', rank);
  }

  /* Tabby "pay in 4": only shown where checkout really allows it (75–10,000 SAR,
     the limits in api/tabby/create-session.js). */
  var TABBY_MIN = 75, TABBY_MAX = 10000;
  function bnplOk(price) { return price >= TABBY_MIN && price <= TABBY_MAX; }
  function bnplQuarter(price) { return Math.round(price / 4 * 100) / 100; }
  // Instalments always show two decimals when they have any (674.75, 1,387.50).
  function bnplMoney(price, currency) {
    var q = bnplQuarter(price);
    var whole = q.toLocaleString('en-US');
    return q % 1 ? money(q, currency).replace(whole, q.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })) : money(q, currency);
  }
  var TABBY_MARK = '<span class="b3d-bnpl__tabby"><img src="/3d/assets/images/payment/tabby.png" alt="" width="16" height="16">tabby</span>';
  var TAMARA_MARK = '<img class="b3d-bnpl__tamara" src="/3d/assets/images/payment/tamara.png" alt="tamara" width="62" height="20">';
  function bnplHtml(price, currency) {
    if (!bnplOk(price)) return '';
    return '<p class="b3d-bnpl">' + T('js_bnpl_prefix') + ' <b>' + bnplMoney(price, currency) + '</b> ' + T('js_bnpl_with') + ' <span class="b3d-bnpl__marks">' + TABBY_MARK + TAMARA_MARK + '</span></p>';
  }
  function bnplCardHtml(price, currency) {
    if (!bnplOk(price)) return '';
    return '<span class="b3d-bnpl-card">' + T('js_bnpl_card') + ' ' + bnplMoney(price, currency) + ' <span class="b3d-bnpl__marks">' + TABBY_MARK + TAMARA_MARK + '</span></span>';
  }

  /* Delivery estimate, counted in Saudi business days (Sun–Thu) in Riyadh time.
     Stock items: dispatched the same day if ordered before 4 pm on a business day,
     otherwise the next business day; then standard shipping 4–5 business days.
     3D printed items: made to order in 3–5 days, then 4–5 days (Shipping Policy). */
  var ETA_CUTOFF_HOUR = 16;
  function riyadhNow() {
    var parts = {};
    try {
      new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Riyadh', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', hourCycle: 'h23' })
        .formatToParts(new Date()).forEach(function (x) { parts[x.type] = x.value; });
      return { date: new Date(Date.UTC(+parts.year, +parts.month - 1, +parts.day)), hour: +parts.hour };
    } catch (e) { var d = new Date(); return { date: new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())), hour: d.getHours() }; }
  }
  function isBusinessDay(d) { var wd = d.getUTCDay(); return wd !== 5 && wd !== 6; }
  function dispatchDate() {
    var now = riyadhNow();
    return isBusinessDay(now.date) && now.hour < ETA_CUTOFF_HOUR ? now.date : addBusinessDays(now.date, 1);
  }
  function addBusinessDays(date, n) {
    var d = new Date(date.getTime());
    while (n > 0) {
      d.setUTCDate(d.getUTCDate() + 1);
      var wd = d.getUTCDay();
      if (wd !== 5 && wd !== 6) n--;   // Friday and Saturday are the weekend
    }
    return d;
  }
  function etaDate(d) {
    var loc = isAr() ? 'ar-SA-u-ca-gregory-nu-latn' : 'en-GB';
    try { return d.toLocaleDateString(loc, { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' }); }
    catch (e) { return d.toISOString().slice(0, 10); }
  }
  function etaHtml(p) {
    var art = p.category === '3D Artwork';
    var lo = (art ? 3 : 0) + 4, hi = (art ? 5 : 0) + 5;
    var today = dispatchDate();
    return '<p class="b3d-eta"><span aria-hidden="true">&#128230;</span> <span>' + T('js_eta_by') + ' ' + T('js_eta_between') +
      ' <b>' + etaDate(addBusinessDays(today, lo)) + '</b> ' + T('js_eta_and') + ' <b>' + etaDate(addBusinessDays(today, hi)) + '</b> ' +
      T('js_eta_std') + (art ? ' ' + T('js_eta_made') : '') + '</span></p>';
  }

  var WA_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.8 2.3.9 2.5c.1.2 1.6 2.5 4 3.5 1.5.6 2.1.7 2.8.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.4-.2z"/></svg>';
  function waHref(p, variant) {
    var url = 'https://www.blackarrowksa.com' + productUrl(p);
    var text = T('js_wa_msg') + ' ' + L(p, 'name') + (variant ? ' (' + LVariant(variant) + ')' : '') + '\n' + url;
    return 'https://wa.me/966560224715?text=' + encodeURIComponent(text);
  }
  function waLabel(p) {
    return p.category === '3D Printers' ? T('js_wa_printer') : p.category === 'Filament' ? T('js_wa_filament') : T('js_wa_item');
  }

  /* Official Bambu Lab wiki page per printer model - installation, usage and
     maintenance guides, straight from the manufacturer (wiki.bambulab.com),
     plus their official YouTube channel for video tutorials. */
  var BAMBU_WIKI_URL = {
    'bambu-lab-a1-mini': 'https://wiki.bambulab.com/en/a1-mini',
    'bambu-lab-a1': 'https://wiki.bambulab.com/en/a1',
    'bambu-lab-a2l': 'https://wiki.bambulab.com/en/a2l',
    'bambu-lab-h2c-combo': 'https://wiki.bambulab.com/en/h2c',
    'bambu-lab-p2s': 'https://wiki.bambulab.com/en/p2s'
  };
  var BAMBU_YOUTUBE_URL = 'https://www.youtube.com/@bambulab';
  function guidesHtml(p) {
    var wikiUrl = BAMBU_WIKI_URL[p.id];
    if (!wikiUrl) return '';
    return '<div class="b3d-pd__guides"><h2>' + T('js_guides_heading') + '</h2><ul>' +
      '<li><a href="' + wikiUrl + '" target="_blank" rel="noopener noreferrer">' + T('js_guides_official_wiki') + '</a></li>' +
      '<li><a href="' + BAMBU_YOUTUBE_URL + '" target="_blank" rel="noopener noreferrer">' + T('js_guides_official_youtube') + '</a></li>' +
      '</ul></div>';
  }

  /* Kits: contents with thumbnails, and the saving against buying each part. */
  function kitBoxHtml(p) {
    if (!p.kit) return '';
    var sep = 0, hasFilament = false;
    var rows = p.kit.map(function (it) {
      var c = __b3dProductsById[it.id];
      if (!c) return '';
      var v = it.variant != null && c.variants ? c.variants[it.variant] : null;
      var unitP = v ? v.price : ((c.onSale && c.salePrice != null) ? c.salePrice : c.price);
      sep += unitP * it.qty;
      if (c.category === 'Filament') hasFilament = true;
      var img = primaryImage(c);
      return '<li><a href="' + productUrl(c) + '">' + (img ? '<img src="' + img + '" alt="" width="48" height="48" loading="lazy">' : '') +
        '<span><b>' + (it.qty > 1 ? it.qty + ' × ' : '') + L(c, 'name') + '</b>' + (v ? '<small>' + LVariant(v) + '</small>' : '') + '</span></a>' +
        '<span class="b3d-kit__unit">' + money(unitP * it.qty, p.currency) + '</span></li>';
    }).join('');
    var kitP = (p.onSale && p.salePrice != null) ? p.salePrice : p.price;
    return '<div class="b3d-kit">' +
      '<h2>' + T('js_kit_title') + '</h2><ul class="b3d-kit__list">' + rows + '</ul>' +
      '<dl class="b3d-kit__sum"><div><dt>' + T('js_kit_separately') + '</dt><dd><s>' + money(sep, p.currency) + '</s></dd></div>' +
      '<div><dt>' + T('js_kit_price') + '</dt><dd>' + money(kitP, p.currency) + '</dd></div>' +
      (sep > kitP ? '<div class="is-save"><dt>' + T('js_kit_save') + '</dt><dd>' + money(sep - kitP, p.currency) + '</dd></div>' : '') + '</dl>' +
      (hasFilament ? '<p class="b3d-kit__note">' + T('js_kit_colors') + '</p>' : '') +
    '</div>';
  }
  /* On a product that is part of a kit: link to the kit and its saving. */
  function kitUpsellHtml(p, products) {
    var kits = products.filter(function (k) {
      return k.kit && k.available !== false && k.id !== p.id && k.kit[0] && k.kit[0].id === p.id;
    });
    return kits.map(function (k) {
      var kitP = (k.onSale && k.salePrice != null) ? k.salePrice : k.price;
      var save = k.price - kitP;
      if (!(save > 0)) return '';
      return '<a class="b3d-kit-upsell" href="' + productUrl(k) + '"><span aria-hidden="true">&#127873;</span><span>' +
        T('js_kit_upsell').replace('{n}', '<b>' + money(save, k.currency) + '</b>') + ' <b>' + L(k, 'name') + '</b></span><span aria-hidden="true">&rarr;</span></a>';
    }).join('');
  }

  function vatNoteHtml(p) {
    return p.vatIncluded ? '<span class="b3d-vat-note">' + T('js_vat_included') + '</span>' : '';
  }

  // All of a card's badges in one wrapping row: deal badges on the left, stock on the right.
  // When the card is too narrow for both they wrap to a new line instead of overlapping.
  function badgesHtml(p, v) {
    return '<div class="b3d-badges">' + cornerBadges(p) + statusBadge(p, v) + '</div>';
  }

  function cornerBadges(p) {
    var out = '';
    if (p.bestSeller) out += '<span class="b3d-corner-badge b3d-corner-badge--bestseller">' + bestSellerLabel(p.bestSeller) + '</span>';
    if (p.featured) out += '<span class="b3d-corner-badge b3d-corner-badge--featured">' + T('shop_featured') + '</span>';
    if (p.onSale) out += '<span class="b3d-corner-badge b3d-corner-badge--sale">' + T('js_sale_badge') + '</span>';
    return out;
  }

  function cardActionLabel(p, disabled) {
    if (p.preorder) return T('js_pre_order');
    return disabled ? T('js_out_of_stock') : T('js_add_to_cart');
  }

  function productCard(p) {
    /* Add to Cart directly on every card, everywhere one appears — opening the
       product page is now optional, not required, to buy. Three shapes:
       - every variant has a swatch (colour products): colour chips + Add to Cart (unchanged).
       - variants exist but aren't colours (e.g. a printer's Standalone/Combo, a
         nozzle's mm size): inline pills pick the variant right on the card,
         never a guessed default, then Add to Cart for the picked one.
       - no variants at all: Add to Cart straight away. */
    var href = productUrl(p);
    // Combo-builder products (p.bundlePick) model their tier pricing as real
    // variants for trusted checkout pricing, but the tier is picked via the
    // product-page combo builder, not card pills — suppress the pill/colour UI here.
    var hasVariants = !!(p.variants && p.variants.length) && !p.bundlePick;
    var colorProduct = hasVariants && p.variants.every(function (v) { return v.swatch; });
    var pillProduct = hasVariants && !colorProduct;

    var colorIdx = 0;
    if (colorProduct) {
      for (var ci = 0; ci < p.variants.length; ci++) { if (p.variants[ci].available !== false) { colorIdx = ci; break; } }
    }
    var colorsHtml = '';
    if (colorProduct) {
      // Compact colour dots (name on hover / in the label above), in-stock colours first, so a
      // filament with 15 colours keeps the same card height as everything else in the row.
      var order = p.variants.map(function (v, i) { return i; }).sort(function (a, b) {
        return (p.variants[a].available === false) - (p.variants[b].available === false) || a - b;
      });
      var labelOf = function (v) { return LVariant(v) + (v.available === false ? ' · ' + T('js_out_of_stock') : ''); };
      colorsHtml = '<p class="b3d-card__color-label" data-card-color-label>' + T('js_colour') + ': <strong>' + labelOf(p.variants[colorIdx]) + '</strong></p>' +
        '<div class="b3d-card__colors b3d-card__colors--dots" data-card-colors="' + p.id + '" role="group" aria-label="' + T('js_colour') + '">' +
        order.map(function (i) {
          var v = p.variants[i];
          var out = v.available === false;
          return '<button type="button" class="b3d-color-chip b3d-color-chip--dot' + (out ? ' is-out' : '') + '" data-card-color="' + i + '" aria-pressed="' + (i === colorIdx) + '"' +
            ' data-out="' + (out ? '1' : '0') + '" data-label="' + labelOf(v).replace(/"/g, '&quot;') + '" title="' + labelOf(v).replace(/"/g, '&quot;') + '" aria-label="' + labelOf(v).replace(/"/g, '&quot;') + '"' + (v.image ? ' data-img="' + v.image + '"' : '') + '>' +
            '<span class="b3d-color-chip__dot" style="background:' + v.swatch + ';"></span></button>';
        }).join('') + '</div>';
    }
    var colorOut = colorProduct && p.variants[colorIdx].available === false;

    var pillIdx = 0;
    if (pillProduct) {
      for (var pi = 0; pi < p.variants.length; pi++) { if (p.variants[pi].available !== false) { pillIdx = pi; break; } }
    }
    var pillsHtml = '';
    if (pillProduct) {
      pillsHtml = '<div class="b3d-card__pills" data-card-pills="' + p.id + '" role="group" aria-label="' + T('js_options') + '">' +
        p.variants.map(function (v, i) {
          var out = v.available === false;
          return '<button type="button" class="b3d-quick-pill' + (out ? ' is-out' : '') + '" data-card-pill="' + i + '" aria-pressed="' + (i === pillIdx) + '"' +
            (out ? ' data-out="1"' : '') + '>' + LVariant(v) + (out ? ' (' + T('js_out_of_stock') + ')' : '') + '</button>';
        }).join('') + '</div>';
    }
    var pillOut = pillProduct && (p.available === false || p.variants[pillIdx].available === false);

    var priceHtml = pillProduct ? variantPriceHtml(p.variants[pillIdx], p) : priceBlock(p);
    var simpleOut = !hasVariants && p.available === false;

    var actionBtn;
    if (p.bundlePick) {
      actionBtn = '<a href="' + href + '" class="b3d-btn-add">' + T('js_bundle_pick_cta') + '</a>';
    } else if (colorProduct) {
      actionBtn = '<button type="button" class="b3d-btn-add" data-card-add="' + p.id + '" data-variant-idx="' + colorIdx + '"' + (colorOut ? ' disabled' : '') + '>' + (colorOut ? T('js_out_of_stock') : T('js_add_to_cart')) + '</button>';
    } else if (pillProduct) {
      actionBtn = '<button type="button" class="b3d-btn-add" data-card-add="' + p.id + '" data-variant-idx="' + pillIdx + '"' + ((pillOut && !p.preorder) ? ' disabled' : '') + '>' + cardActionLabel(p, pillOut) + '</button>';
    } else {
      actionBtn = '<button type="button" class="b3d-btn-add" data-card-add="' + p.id + '"' + ((simpleOut && !p.preorder) ? ' disabled' : '') + '>' + cardActionLabel(p, simpleOut) + '</button>';
    }
    var isArt = p.category === '3D Artwork';
    var specs = isArt ? '' : LSpecs(p).slice(0, 3).map(function (row) {
      return '<li><span>' + row[0] + '</span><span>' + row[1] + '</span></li>';
    }).join('');
    return '' +
      '<article class="b3d-card' + (isArt ? ' b3d-card--art' : '') + '" data-cat="' + p.category + '" data-brand="' + (p.brand || '') + '">' +
        '<a href="' + href + '" class="b3d-card__stretched-link" aria-label="' + L(p, 'name') + '"></a>' +
        '<div class="b3d-card__visual">' +
          badgesHtml(p, colorProduct ? p.variants[colorIdx] : pillProduct ? p.variants[pillIdx] : null) +
          visual(p) +
        '</div>' +
        '<div class="b3d-card__body">' +
          '<div class="b3d-card__cat">' + (p.brand ? p.brand + ' &middot; ' : '') + categoryLabel(p.category) + '</div>' +
          '<h3>' + L(p, 'name') + '</h3>' +
          (isArt ? '' : '<p>' + (L(p, 'shortDesc') || '') + '</p>') +
          (specs ? '<ul class="b3d-card__specs">' + specs + '</ul>' : '') +
          colorsHtml +
          pillsHtml +
          '<div class="b3d-card__meta-line"><span>' + T('js_card_delivery') + '</span>' + (isArt ? '' : '<span>' + T('js_card_warranty') + '</span>') + '</div>' +
        '</div>' +
        '<div class="b3d-card__footer">' +
          '<div class="b3d-price-wrap">' +
            '<div class="b3d-price-col">' +
              '<div class="b3d-price-block" data-card-price="' + p.id + '">' + priceHtml + '</div>' + vatNoteHtml(p) +
              (p.category === '3D Printers' && !pillOut && !simpleOut ? '<div data-card-bnpl>' + bnplCardHtml(pillProduct ? p.variants[pillIdx].price : currentPrice(p), p.currency) + '</div>' : '') +
            '</div>' +
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

  /* Colour chips, option pills and Add to Cart on product cards (delegated,
     so it works in every grid this card renders into, no per-container binding needed). */
  if (!window.__b3dCardColors) {
    window.__b3dCardColors = true;
    document.addEventListener('click', function (e) {
      var chip = e.target.closest && e.target.closest('[data-card-color]');
      if (chip) {
        var card = chip.closest('.b3d-card');
        card.querySelectorAll('[data-card-color]').forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
        var colorLabel = card.querySelector('[data-card-color-label] strong');
        if (colorLabel && chip.getAttribute('data-label')) colorLabel.textContent = chip.getAttribute('data-label');
        var cProduct = __b3dProductsById && __b3dProductsById[chip.closest('[data-card-colors]').getAttribute('data-card-colors')];
        if (cProduct) syncStockBadge(card, cProduct, cProduct.variants[parseInt(chip.getAttribute('data-card-color'), 10)]);
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
      var pill = e.target.closest && e.target.closest('[data-card-pill]');
      if (pill) {
        var pid = pill.closest('[data-card-pills]').getAttribute('data-card-pills');
        var pCard = pill.closest('.b3d-card');
        var pIdx = parseInt(pill.getAttribute('data-card-pill'), 10);
        var product = __b3dProductsById && __b3dProductsById[pid];
        pCard.querySelectorAll('[data-card-pill]').forEach(function (c) { c.setAttribute('aria-pressed', c === pill ? 'true' : 'false'); });
        var pOut = pill.getAttribute('data-out') === '1' || !!(product && product.available === false);
        if (product) syncStockBadge(pCard, product, product.variants[pIdx]);
        var pBtn = pCard.querySelector('[data-card-add]');
        if (pBtn) {
          pBtn.setAttribute('data-variant-idx', pIdx);
          pBtn.disabled = pOut && !(product && product.preorder);
          pBtn.textContent = product ? cardActionLabel(product, pOut) : (pOut ? T('js_out_of_stock') : T('js_add_to_cart'));
        }
        var priceEl = pCard.querySelector('[data-card-price]');
        if (priceEl && product) priceEl.innerHTML = variantPriceHtml(product.variants[pIdx], product);
        var bnplEl = pCard.querySelector('[data-card-bnpl]');
        if (bnplEl && product) bnplEl.innerHTML = bnplCardHtml(product.variants[pIdx].price, product.currency);
        var pv = product && product.variants[pIdx];
        var pImg = pCard.querySelector('.b3d-card__visual img');
        if (pv && pv.image && pImg) { pImg.removeAttribute('srcset'); pImg.removeAttribute('sizes'); pImg.src = pv.image; }
        return;
      }
      var add = e.target.closest && e.target.closest('[data-card-add]');
      if (add && !add.disabled) {
        var viRaw = add.getAttribute('data-variant-idx');
        addToCart(lineId(add.getAttribute('data-card-add'), viRaw === null ? null : parseInt(viRaw, 10)), 1);
        var label = add.textContent;
        add.textContent = T('js_added');
        setTimeout(function () { if (!add.disabled) add.textContent = label; }, 1200);
      }
    });
  }

  /* Lead tracking (GTM / GA4) — delegated, so it works site-wide without
     binding to every WhatsApp/phone link individually. */
  if (!window.__b3dLeadTracking) {
    window.__b3dLeadTracking = true;
    document.addEventListener('click', function (e) {
      var wa = e.target.closest && e.target.closest('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
      if (wa) { pushLeadEvent('whatsapp'); return; }
      var tel = e.target.closest && e.target.closest('a[href^="tel:"]');
      if (tel) { pushLeadEvent('phone'); }
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

  // Bambu Lab printer lines, read from the model name: A1 mini/A1/A2L -> A, P1S/P2S -> P,
  // X1E/X2D -> X, H2C/H2S/H2D -> H.
  var SERIES_ORDER = ['A', 'P', 'X', 'H'];
  function seriesOf(p) {
    if (p.brand !== 'Bambu Lab' || p.category !== '3D Printers') return null;
    var m = /^Bambu Lab ([A-Z])\d/.exec(p.name || '');
    return m ? m[1] : null;
  }

  // "Bambu Lab series: All · A Series · P Series ..." chips for a product list; null when the
  // list holds fewer than two series. onPick gets 'All' or the series letter.
  function seriesBar(list, current, onPick) {
    var found = SERIES_ORDER.filter(function (s) { return list.some(function (p) { return seriesOf(p) === s; }); });
    if (found.length < 2) return null;
    var ar = isAr();
    var bar = document.createElement('div');
    bar.className = 'b3d-cat-tabs b3d-series';
    bar.setAttribute('role', 'group');
    bar.setAttribute('aria-label', ar ? 'سلاسل طابعات Bambu Lab' : 'Bambu Lab series');
    bar.innerHTML = '<span class="b3d-series__label">' + (ar ? 'سلاسل Bambu Lab' : 'Bambu Lab series') + '</span>' +
      ['All'].concat(found).map(function (s) {
        var label = s === 'All' ? (ar ? 'الكل' : 'All') : (ar ? 'سلسلة ' + s : s + ' Series');
        return '<button type="button" data-series="' + s + '" aria-pressed="' + (s === current) + '">' + label + '</button>';
      }).join('');
    bar.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-series]');
      if (!btn) return;
      bar.querySelectorAll('[data-series]').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
      onPick(btn.getAttribute('data-series'));
    });
    return bar;
  }

  // A grid with the series chips above it (brand and category pages).
  function renderGridWithSeries(list, grid) {
    var bar = seriesBar(list, 'All', function (s) {
      renderGrid(s === 'All' ? list : list.filter(function (p) { return seriesOf(p) === s; }), grid);
    });
    if (bar) grid.parentNode.insertBefore(bar, grid);
    renderGrid(list, grid);
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
      series: 'All',
      priceMin: null,
      priceMax: null,
      page: 1
    };
    var seriesEl = null;

    var params = new URLSearchParams(location.search);
    if (params.get('cat')) state.cat = params.get('cat');
    if (params.get('brand')) state.brand = params.get('brand');
    if (params.get('q')) state.q = params.get('q');
    if (params.get('material')) state.filamentMaterial = params.get('material');
    if (params.get('series')) state.series = params.get('series').charAt(0).toUpperCase();

    // Filtered views are for visitors, not the search index (the server also
    // sends X-Robots-Tag: noindex for these); the clean /shop/<category>/ and
    // /brands/<brand>/ pages are the indexable ones.
    if (location.search.length > 1) {
      var robotsMeta = document.querySelector('meta[name="robots"]');
      if (!robotsMeta) { robotsMeta = document.createElement('meta'); robotsMeta.name = 'robots'; document.head.appendChild(robotsMeta); }
      robotsMeta.setAttribute('content', 'noindex, follow');
    }

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
      if (els.filamentMaterialSelect && state.filamentMaterial !== 'All') els.filamentMaterialSelect.value = state.filamentMaterial;
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
      if (state.priceMin != null) list = list.filter(function (p) { return currentPrice(p) >= state.priceMin; });
      if (state.priceMax != null) list = list.filter(function (p) { return currentPrice(p) <= state.priceMax; });

      if (seriesEl) seriesEl.remove();
      seriesEl = seriesBar(list, state.series, function (s) { state.series = s; state.page = 1; apply(); });
      if (seriesEl) els.grid.parentNode.insertBefore(seriesEl, els.grid);
      else state.series = 'All';
      if (state.series !== 'All') list = list.filter(function (p) { return seriesOf(p) === state.series; });

      if (state.sort === 'price-asc') list.sort(function (a, b) { return currentPrice(a) - currentPrice(b); });
      if (state.sort === 'price-desc') list.sort(function (a, b) { return currentPrice(b) - currentPrice(a); });
      if (state.sort === 'name-asc') list.sort(function (a, b) { return a.name.localeCompare(b.name); });
      if (state.sort === 'best-seller') list.sort(function (a, b) { return (a.bestSeller || Infinity) - (b.bestSeller || Infinity); });
      // Featured order: 3D Artwork newest first (new products are added at the end of the
      // catalog), keeping the same slots in the list so printers and parts stay where they are.
      if (state.sort === 'default') {
        var art = list.filter(function (p) { return p.category === '3D Artwork'; }).reverse();
        list = list.map(function (p) { return p.category === '3D Artwork' ? art.shift() : p; });
      }

      var totalPages = Math.max(1, Math.ceil(list.length / PAGE_SIZE));
      if (state.page > totalPages) state.page = totalPages;
      var pageItems = list.slice((state.page - 1) * PAGE_SIZE, state.page * PAGE_SIZE);

      renderGrid(pageItems, els.grid);
      // Nothing matches the chosen category / filters / search: say so, with a way back to
      // everything ("No products published yet" is only for an empty catalogue).
      if (!list.length && products.length) {
        var ar = isAr();
        els.grid.innerHTML = '<div class="b3d-empty" style="grid-column:1/-1;">' +
          '<h2 style="margin-bottom:10px;">' + (ar ? 'لا توجد منتجات تطابق هذا الاختيار' : 'No products match this selection') + '</h2>' +
          '<p>' + (ar ? 'جرّب فئة أخرى أو امسح الفلاتر والبحث.' : 'Try another category, or clear the filters and search.') + '</p>' +
          '<button type="button" class="btn btn-primary" data-b3d-show-all style="margin-top:14px;">' + (ar ? 'عرض كل المنتجات' : 'Show all products') + '</button>' +
          '</div>';
        els.grid.querySelector('[data-b3d-show-all]').addEventListener('click', function () {
          if (els.filterClear) els.filterClear.click();
          state.q = '';
          if (els.searchInput) els.searchInput.value = '';
          setCategory('All');
        });
      }
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
        tab.setAttribute('aria-pressed', String(tab.getAttribute('data-cat') === state.cat));
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
        state.series = 'All';
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
  // Free delivery thresholds: either qualifies the whole order.
  var FREE_SHIP_ARTWORK_MIN = 100;
  var FREE_SHIP_PRINTER_MIN = 3000;
  var lastFreeShipping = false;

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

  /* Black Arrow Loyalty Rewards in the cart: signed-in members can use their balance
     (4 SAR minimum) and Gold/Platinum get free Regular delivery. The server
     re-checks all of it (api/_lib/rewards.js); this is only the display. */
  var REWARDS_MIN = 4;
  var rewardsState = null; // { member, freeDelivery, use, redeemed: { orderId, used } }
  var lastArtworkSubtotal = 0;

  function rewardsUsable() {
    return !!(rewardsState && rewardsState.member && rewardsState.member.balance >= REWARDS_MIN);
  }
  function rewardsDiscount() {
    if (!rewardsState) return 0;
    if (rewardsState.redeemed) return rewardsState.redeemed.used;
    if (!rewardsState.use || !rewardsUsable()) return 0;
    var room = Math.max(0, lastSubtotal - couponDiscount());
    return Math.min(Math.floor(rewardsState.member.balance * 100) / 100, room);
  }
  function memberFreeDelivery() {
    return !!(rewardsState && rewardsState.freeDelivery);
  }

  function renderRewardsRow(summaryEl) {
    var row = summaryEl.querySelector('[data-b3d-rewards-row]');
    if (!row) {
      row = document.createElement('div');
      row.className = 'b3d-cart-summary__row b3d-rewards-row';
      row.setAttribute('data-b3d-rewards-row', '');
      row.innerHTML = '<label class="b3d-rewards-row__label"><input type="checkbox" data-b3d-rewards-use> <span data-b3d-rewards-text></span></label><span data-b3d-rewards-amount></span>';
      var totalRow = summaryEl.querySelector('.b3d-cart-summary__total');
      summaryEl.insertBefore(row, totalRow);
      row.querySelector('[data-b3d-rewards-use]').addEventListener('change', function (e) {
        if (!rewardsState || rewardsState.redeemed) return;
        rewardsState.use = e.target.checked;
        updateOrderTotals();
      });
    }
    var ar = isAr();
    var box = row.querySelector('[data-b3d-rewards-use]');
    var text = row.querySelector('[data-b3d-rewards-text]');
    var amount = row.querySelector('[data-b3d-rewards-amount]');
    if (!rewardsState || !rewardsState.member) {
      var signedOutHint = !rewardsState && window.BlackArrow3DAuth && window.BlackArrow3DAuth.isConfigured();
      row.hidden = !signedOutHint;
      box.hidden = true;
      amount.textContent = '';
      text.innerHTML = ar
        ? '<a href="/3d/ar/rewards/">سجّل الدخول لتكسب وتستخدم مكافآت ولاء بلاك آرو</a>'
        : '<a href="/3d/rewards/">Sign in to earn and use Black Arrow Loyalty Rewards</a>';
      return;
    }
    var m = rewardsState.member;
    var bal = m.balance.toFixed(2);
    row.hidden = false;
    if (!rewardsUsable()) {
      box.hidden = true;
      amount.textContent = '';
      text.textContent = ar
        ? 'رصيد مكافآت ولاء بلاك آرو: ' + bal + ' ريال (يُستخدم من 4 ريال)'
        : 'Black Arrow Loyalty Rewards: ' + bal + ' SAR (usable from 4 SAR)';
      return;
    }
    box.hidden = false;
    box.checked = !!rewardsState.use || !!rewardsState.redeemed;
    box.disabled = !!rewardsState.redeemed;
    text.textContent = ar
      ? 'استخدم رصيد مكافآت ولاء بلاك آرو (' + bal + ' ريال)'
      : 'Use my Black Arrow Loyalty Rewards balance (' + bal + ' SAR)';
    var d = rewardsDiscount();
    amount.innerHTML = d ? '−' + money(d, 'SAR') : '';
  }

  function loadCartRewards() {
    if (!window.BlackArrow3DRewards) return;
    window.BlackArrow3DRewards.fetchMe().then(function (me) {
      if (!me || !me.signedIn || !me.member) {
        rewardsState = me && me.signedIn ? { member: null } : null;
      } else {
        rewardsState = { member: me.member, freeDelivery: !!me.freeDelivery, use: rewardsState ? rewardsState.use !== false : true, redeemed: rewardsState && rewardsState.redeemed };
      }
      if (memberFreeDelivery() && !lastFreeShipping) {
        lastFreeShipping = true;
        updateFreeShippingUi(lastArtworkSubtotal, lastSubtotal);
      }
      updateOrderTotals();
    });
  }

  // Sequential order numbers (BAV-3D-5001, ...) come from a Supabase sequence
  // so two checkouts can't collide. If Supabase is unreachable, falls back to
  // a timestamp-based id so checkout never blocks on this.
  function nextOrderId() {
    var cfg = window.BLACK_ARROW_SUPABASE_CONFIG;
    if (!cfg || !cfg.url || !cfg.anonKey) return Promise.resolve('BAV-3D-' + Date.now());
    return fetch(cfg.url + '/rest/v1/rpc/next_order_id', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', apikey: cfg.anonKey, Authorization: 'Bearer ' + cfg.anonKey },
      body: '{}'
    }).then(function (r) {
      if (!r.ok) throw new Error('rpc');
      return r.json();
    }).catch(function () { return 'BAV-3D-' + Date.now(); });
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

  /* Same progress shown at the top of the cart summary, where people decide
     what to add (the note above lives inside the checkout form). */
  function renderCartShipProgress(text, pct, unlocked) {
    var summary = document.querySelector('[data-b3d-cart-summary]');
    if (!summary) return;
    var box = summary.querySelector('[data-b3d-ship-progress]');
    if (text == null) { if (box) box.hidden = true; return; }
    if (!box) {
      box = document.createElement('div');
      box.className = 'b3d-ship-progress';
      box.setAttribute('data-b3d-ship-progress', '');
      summary.insertBefore(box, summary.firstChild);
    }
    pct = Math.max(0, Math.min(100, Math.round(pct)));
    box.className = 'b3d-ship-progress' + (unlocked ? ' is-unlocked' : '');
    box.innerHTML = '<p>' + (unlocked ? '&#10003; ' : '&#128666; ') + text + '</p>' +
      '<div class="b3d-ship-bar' + (pct >= 100 ? ' is-full' : '') + '" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '"><span class="b3d-ship-bar__fill" style="width:' + pct + '%"></span></div>';
    box.hidden = false;
  }

  function updateFreeShippingUi(artworkSubtotal, orderSubtotal) {
    // The free-delivery threshold only ever waives Regular shipping — Fast
    // shipping always keeps its fee, so only that option's price gets overridden.
    var priceEls = document.querySelectorAll('[data-ship-price-display="regular"]');
    priceEls.forEach(function (el) {
      if (el.dataset.originalHtml === undefined) el.dataset.originalHtml = el.innerHTML;
      el.innerHTML = lastFreeShipping ? T('js_free_ship_label') : el.dataset.originalHtml;
    });
    var noteEl = document.querySelector('[data-b3d-shipping-note]');
    if (!noteEl) noteEl = document.createElement('p');
    if (!noteEl.parentNode) { noteEl.hidden = true; document.createDocumentFragment().appendChild(noteEl); }
    // Progress bar right under the note: how close this cart is to free delivery.
    var bar = document.querySelector('[data-b3d-ship-bar]');
    if (!bar) {
      bar = document.createElement('div');
      bar.className = 'b3d-ship-bar';
      bar.setAttribute('data-b3d-ship-bar', '');
      bar.setAttribute('role', 'progressbar');
      bar.setAttribute('aria-valuemin', '0');
      bar.setAttribute('aria-valuemax', '100');
      bar.innerHTML = '<span class="b3d-ship-bar__fill"></span>';
      noteEl.parentNode.insertBefore(bar, noteEl.nextSibling);
    }
    function setBar(pct) {
      pct = Math.max(0, Math.min(100, Math.round(pct)));
      bar.querySelector('.b3d-ship-bar__fill').style.width = pct + '%';
      bar.setAttribute('aria-valuenow', String(pct));
      bar.classList.toggle('is-full', pct >= 100);
      bar.hidden = false;
    }
    if (lastFreeShipping) {
      noteEl.textContent = T('js_free_ship_unlocked');
      noteEl.className = 'b3d-shipping-note is-unlocked';
      noteEl.hidden = false;
      setBar(100);
      renderCartShipProgress(T('js_free_ship_unlocked'), 100, true);
      return;
    }
    var remainArt = FREE_SHIP_ARTWORK_MIN - artworkSubtotal;
    var remainOrder = FREE_SHIP_PRINTER_MIN - orderSubtotal;
    if (artworkSubtotal > 0 && remainArt > 0 && orderSubtotal < FREE_SHIP_PRINTER_MIN) {
      noteEl.textContent = T('js_free_ship_progress_artwork').replace('{n}', Math.ceil(remainArt * 100) / 100);
      noteEl.className = 'b3d-shipping-note';
      noteEl.hidden = false;
      setBar(artworkSubtotal / FREE_SHIP_ARTWORK_MIN * 100);
      renderCartShipProgress(noteEl.textContent, artworkSubtotal / FREE_SHIP_ARTWORK_MIN * 100, false);
    } else if (orderSubtotal > 0 && remainOrder > 0) {
      noteEl.textContent = T('js_free_ship_progress_printer').replace('{n}', Math.ceil(remainOrder * 100) / 100);
      noteEl.className = 'b3d-shipping-note';
      noteEl.hidden = false;
      setBar(orderSubtotal / FREE_SHIP_PRINTER_MIN * 100);
      renderCartShipProgress(noteEl.textContent, orderSubtotal / FREE_SHIP_PRINTER_MIN * 100, false);
    } else {
      noteEl.hidden = true;
      bar.hidden = true;
      renderCartShipProgress(null);
    }
  }

  // Pay-later (Tabby / Tamara) service fee, per order: 100 SAR with a printer,
  // 50 SAR for filament with no printed items, otherwise none. The server
  // (api/paymob/create-intention.js, api/tabby/create-session.js) charges the same.
  var currentPayMethod = '';
  function bnplFee() {
    var cart = getCart();
    var cats = {};
    Object.keys(cart).forEach(function (id) {
      var p = __b3dProductsById[parseLineId(id).productId];
      if (p) cats[p.category] = true;
    });
    if (cats['3D Printers']) return 100;
    if (cats['Filament'] && !cats['3D Artwork']) return 50;
    return 0;
  }

  // Bank transfer saving: 1% off the items (after coupon / rewards, before delivery). Shown to
  // the customer only as the amount saved. The server (api/bank-order.js) works out the same.
  var BANK_SAVE_RATE = 0.01;
  function bankSaving() {
    var base = lastSubtotal - couponDiscount() - rewardsDiscount();
    return base > 0 ? Math.round(base * BANK_SAVE_RATE * 100) / 100 : 0;
  }

  var TAG_ICON = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.59 13.41 13.42 20.58a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><circle cx="7" cy="7" r="1.5"/></svg>';

  // Bank transfer discount, shown as an amount (never a percentage): a banner above the payment
  // methods, a chip on the Bank Transfer button, and a confirmation once it is picked.
  function updateBankSaveUi(saving) {
    var ar = isAr();
    var amount = '<strong>' + money(saving, 'SAR') + '</strong>';
    var methods = document.querySelector('.b3d-payment-methods');
    if (methods) {
      var promo = document.querySelector('[data-b3d-bank-promo]');
      if (!promo) {
        promo = document.createElement('button');
        promo.type = 'button';
        promo.className = 'b3d-bank-promo';
        promo.setAttribute('data-b3d-bank-promo', '');
        promo.addEventListener('click', function () { var b = document.querySelector('[data-pm="bank"]'); if (b) b.click(); });
        methods.parentNode.insertBefore(promo, methods);
      }
      promo.hidden = !saving || currentPayMethod === 'bank';
      promo.innerHTML = TAG_ICON + '<span>' + (ar
        ? 'ادفع بالتحويل البنكي واحصل على خصم ' + amount + ' فورًا'
        : 'Pay by bank transfer and get ' + amount + ' off instantly') + '</span>';
    }
    var btn = document.querySelector('[data-pm="bank"]');
    if (btn) {
      var chip = btn.querySelector('[data-b3d-save-chip]');
      if (!chip) {
        chip = document.createElement('span');
        chip.className = 'b3d-save-chip';
        chip.setAttribute('data-b3d-save-chip', '');
        btn.appendChild(chip);
      }
      chip.hidden = !saving;
      chip.innerHTML = (ar ? 'خصم ' : 'Get ') + money(saving, 'SAR') + (ar ? '' : ' off');
    }
    var detail = document.querySelector('[data-pm-detail="bank"]');
    if (detail) {
      var note = detail.querySelector('[data-b3d-bank-save-note]');
      if (!note) {
        note = document.createElement('p');
        note.className = 'b3d-bank-saved';
        note.setAttribute('data-b3d-bank-save-note', '');
        var h = detail.querySelector('h4');
        detail.insertBefore(note, h ? h.nextSibling : detail.firstChild);
      }
      note.hidden = !saving;
      note.innerHTML = TAG_ICON + '<span>' + (ar
        ? 'رائع! وفّرت ' + amount + ' بالدفع بالتحويل البنكي، وتم خصمها من الإجمالي.'
        : 'Nice! You save ' + amount + ' with bank transfer. Already taken off your total.') + '</span>';
    }
  }

  function updateBnplUi(fee) {
    var ar = isAr();
    ['tabby', 'tamara'].forEach(function (m) {
      var detail = document.querySelector('[data-pm-detail="' + m + '"]');
      if (!detail) return;
      var note = detail.querySelector('[data-b3d-bnpl-note]');
      if (!note) {
        note = document.createElement('p');
        note.className = 'b3d-bnpl-note';
        note.setAttribute('data-b3d-bnpl-note', '');
        detail.appendChild(note);
      }
      note.hidden = !fee;
      note.textContent = ar
        ? 'تُضاف رسوم خدمة الدفع لاحقًا بقيمة ' + fee + ' ريال على هذا الطلب. لا تُضاف هذه الرسوم عند الدفع بالبطاقة أو Apple Pay أو التحويل البنكي.'
        : 'A pay-later service fee of ' + fee + ' SAR is added to this order. Card, Apple Pay and bank transfer have no extra fee.';
    });
    ['card', 'applepay'].forEach(function (m) {
      var btn = document.querySelector('[data-pm="' + m + '"]');
      if (!btn) return;
      var chip = btn.querySelector('[data-b3d-save-chip]');
      if (!chip) {
        chip = document.createElement('span');
        chip.className = 'b3d-save-chip';
        chip.setAttribute('data-b3d-save-chip', '');
        btn.appendChild(chip);
      }
      chip.hidden = !fee;
      chip.textContent = ar ? 'بدون رسوم الدفع لاحقًا (' + fee + ' ريال)' : 'No pay-later fee (' + fee + ' SAR)';
    });
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
    var feeAmount = bnplFee();
    updateBnplUi(feeAmount);
    var fee = (currentPayMethod === 'tabby' || currentPayMethod === 'tamara') ? feeAmount : 0;
    var feeRow = summaryEl.querySelector('[data-b3d-bnpl-row]');
    if (!feeRow) {
      feeRow = document.createElement('div');
      feeRow.className = 'b3d-cart-summary__row';
      feeRow.setAttribute('data-b3d-bnpl-row', '');
      feeRow.innerHTML = '<span></span><span></span>';
      var totalRow = summaryEl.querySelector('.b3d-cart-summary__total');
      summaryEl.insertBefore(feeRow, totalRow);
    }
    feeRow.hidden = !fee;
    feeRow.firstChild.textContent = isAr() ? 'رسوم خدمة الدفع لاحقًا' : 'Pay-later service fee';
    feeRow.lastChild.innerHTML = money(fee, 'SAR');
    var feeLine = fee ? '\nPay-later service fee: ' + fee + ' SAR' : '';
    renderRewardsRow(summaryEl);
    var rewardsUsed = rewardsDiscount();
    var rewardsLine = rewardsUsed ? '\nBlack Arrow Loyalty Rewards balance used: -' + rewardsUsed + ' SAR' : '';
    discountLine += rewardsLine;
    var savingAmount = bankSaving();
    updateBankSaveUi(savingAmount);
    var saving = currentPayMethod === 'bank' ? savingAmount : 0;
    var saveRow = summaryEl.querySelector('[data-b3d-bank-save-row]');
    if (!saveRow) {
      saveRow = document.createElement('div');
      saveRow.className = 'b3d-cart-summary__row';
      saveRow.setAttribute('data-b3d-bank-save-row', '');
      saveRow.innerHTML = '<span></span><span></span>';
      summaryEl.insertBefore(saveRow, summaryEl.querySelector('.b3d-cart-summary__total'));
    }
    saveRow.hidden = !saving;
    saveRow.firstChild.textContent = isAr() ? 'خصم التحويل البنكي' : 'Bank transfer discount';
    saveRow.lastChild.innerHTML = '−' + money(saving, 'SAR');
    if (saving) discountLine += '\nBank transfer saving: -' + saving + ' SAR';
    var after = Math.round((lastSubtotal - discount - rewardsUsed + fee - saving) * 100) / 100;

    var showShipping = checkout && !checkout.hidden;
    if (!showShipping) {
      if (shippingEl) shippingEl.textContent = shippingPlaceholderText;
      if (totalEl) totalEl.innerHTML = money(after, 'SAR');
      return;
    }

    var checkedRadio = checkout.querySelector('input[name="shipping_choice"]:checked');
    // Free delivery only ever waives Regular shipping — Fast shipping keeps its fee
    // even once the order qualifies, so the override is gated on the chosen method too.
    var shipFree = lastFreeShipping && checkedRadio && checkedRadio.value === 'regular';
    var price = shipFree ? 0 : (checkedRadio ? parseInt(checkedRadio.getAttribute('data-shipping-price'), 10) : 0);
    var label = checkedRadio ? checkedRadio.getAttribute('data-shipping-label') : '';
    if (shippingEl) shippingEl.innerHTML = shipFree ? T('js_free_ship_label') : money(price, 'SAR');
    if (totalEl) totalEl.innerHTML = money(after + price, 'SAR');

    var shipField = checkout.querySelector('[data-b3d-shipping-field]');
    if (shipField) shipField.value = label + ' — ' + (shipFree ? T('js_free_ship_label') : price + ' SAR');
    var summaryField = checkout.querySelector('[data-b3d-order-summary]');
    if (summaryField) {
      summaryField.value = lastOrderSummaryText + discountLine + feeLine +
        '\nShipping: ' + label + ' — ' + (shipFree ? T('js_free_ship_label') : price + ' SAR') +
        '\nGrand Total: ' + (after + price).toLocaleString('en-US') + ' SAR';
    }
    renderCheckoutRecap(summaryEl, checkout);
  }

  // A copy of the order summary right above "Place Order", so after filling in the address and
  // picking delivery the buyer sees the final amounts without scrolling back up.
  function renderCheckoutRecap(summaryEl, checkout) {
    var submit = checkout.querySelector('button[type="submit"]');
    if (!submit) return;
    var recap = checkout.querySelector('[data-b3d-checkout-recap]');
    if (!recap) {
      recap = document.createElement('div');
      recap.className = 'b3d-checkout-recap';
      recap.setAttribute('data-b3d-checkout-recap', '');
      recap.setAttribute('aria-live', 'polite');
      submit.parentNode.insertBefore(recap, submit);
    }
    var html = '<h4 class="b3d-checkout-recap__title">' + (isAr() ? 'ملخص الطلب' : 'Order summary') + '</h4>';
    summaryEl.querySelectorAll('.b3d-cart-summary__row').forEach(function (row) {
      if (row.hidden || row.children.length < 2) return;
      if (row.hasAttribute('data-b3d-rewards-row')) {
        var used = rewardsDiscount();
        if (used) html += '<div class="b3d-checkout-recap__row"><span>' + (isAr() ? 'مكافآت الولاء المستخدمة' : 'Loyalty Rewards used') + '</span><span>−' + money(used, 'SAR') + '</span></div>';
        return;
      }
      var labelEl = row.children[0].cloneNode(true);
      labelEl.querySelectorAll('button').forEach(function (b) { b.remove(); });
      var label = labelEl.textContent.replace(/\s+/g, ' ').replace(/\(\s+/g, '(').replace(/\s+\)/g, ')').trim();
      html += '<div class="b3d-checkout-recap__row"><span>' + label + '</span><span>' + row.children[row.children.length - 1].innerHTML + '</span></div>';
    });
    var total = summaryEl.querySelector('.b3d-cart-summary__total');
    if (total && total.children.length >= 2) {
      html += '<div class="b3d-checkout-recap__row b3d-checkout-recap__total"><span>' + total.children[0].textContent + '</span><span>' + total.children[1].innerHTML + '</span></div>';
    }
    recap.innerHTML = html;
  }

  var __snapCheckoutFired = false;
  function updateCheckoutFields(method) {
    var checkout = document.querySelector('[data-b3d-checkout]');
    if (!checkout) return;
    var purchasable = method === 'bank' || method === 'card' || method === 'applepay' || method === 'tabby' || method === 'tamara';
    checkout.hidden = !purchasable;
    currentPayMethod = method;
    if (purchasable) {
      var payField = checkout.querySelector('[data-b3d-order-payment]');
      if (payField) payField.value = method === 'card' ? 'Card (Paymob)' : method === 'applepay' ? 'Apple Pay (Paymob)' : method === 'tabby' ? 'Tabby (Pay in 4)' : method === 'tamara' ? 'Tamara (Pay Later)' : 'Bank Transfer';
      if (!__snapCheckoutFired) {
        __snapCheckoutFired = true;
        pushSnapEvent('START_CHECKOUT', snapCartPayload());
      }
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
        if (user) loadCartRewards();
        else { rewardsState = null; updateOrderTotals(); }
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

  // Catches obvious placeholder/test addresses (a@b.co, test@test.com, foo@example.com, ...):
  // a single-letter name and/or domain, or a handful of known fake/example domains.
  function isPlaceholderEmail(email) {
    var m = /^([^@]+)@([^@]+)$/.exec(String(email).trim().toLowerCase());
    if (!m) return false;
    var local = m[1], domain = m[2];
    if (local.length <= 1 || domain.replace(/\.[a-z.]+$/, '').length <= 1) return true;
    var fakeDomains = ['example.com', 'example.org', 'example.net', 'test.com', 'test.co', 'a.com', 'b.com', 'asdf.com', 'mailinator.com'];
    return fakeDomains.indexOf(domain) !== -1;
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
    // Placeholder addresses used while testing checkout (a@b.co, test@test.com, ...) are
    // syntactically valid so the browser's own email check passes them, but they don't exist -
    // sending to them fails days later and Gmail bounces the "Mail Delivery Subsystem" notice
    // back into the shop's inbox. Skip the send for those; the order itself still goes through
    // to Black Arrow either way, only the customer's own confirmation copy is skipped.
    if (isPlaceholderEmail(toEmail)) return;

    var payField = form.querySelector('[data-b3d-order-payment]');
    var shipField = form.querySelector('[data-b3d-shipping-field]');
    var summaryField = form.querySelector('[data-b3d-order-summary]');

    var params = {
      to_email: toEmail,
      to_name: (field('customer_first_name') + ' ' + field('customer_last_name')).trim(),
      order_id: field('order_id'),
      order_summary: summaryField ? summaryField.value : '',
      shipping_method: shipField ? shipField.value : '',
      payment_method: payField ? payField.value : '',
      order_total: document.querySelector('[data-cart-total]') ? document.querySelector('[data-cart-total]').textContent : ''
    };
    sendEmailJs(params);
  }

  function sendEmailJs(params) {
    var cfg = window.BLACK_ARROW_EMAILJS_CONFIG;
    if (!cfg || !cfg.publicKey || !cfg.serviceId || !cfg.templateId) return;
    if (!params.to_email || isPlaceholderEmail(params.to_email)) return;
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

  // Online payments (card, Apple Pay, Tamara, Tabby): before leaving for the
  // gateway the checkout saves the order details in sessionStorage. Once the
  // server confirms the payment, the shop and the customer each get an
  // "order confirmed" email with every item, colour and quantity.
  var PENDING_ORDER_KEY = 'b3d-pending-order';

  // Kept in both sessionStorage and localStorage, so a return in another tab
  // (or a later visit, see resumePendingOrder) can still send the emails.
  function readPendingOrder() {
    var o = null;
    try { o = JSON.parse(sessionStorage.getItem(PENDING_ORDER_KEY) || 'null'); } catch (e) {}
    if (!o) { try { o = JSON.parse(localStorage.getItem(PENDING_ORDER_KEY) || 'null'); } catch (e) {} }
    return o;
  }
  function savePendingOrder(o) {
    var json = JSON.stringify(o);
    try { sessionStorage.setItem(PENDING_ORDER_KEY, json); } catch (e) {}
    try { localStorage.setItem(PENDING_ORDER_KEY, json); } catch (e) {}
  }
  function clearPendingOrder() {
    try { sessionStorage.removeItem(PENDING_ORDER_KEY); } catch (e) {}
    try { localStorage.removeItem(PENDING_ORDER_KEY); } catch (e) {}
  }
  var W3F_ACCESS_KEY = '217e03f8-59ef-45c3-9cf8-048f27ba0586';

  // The server sends the "Order CONFIRMED" emails itself once the gateway
  // confirms the payment (api/_lib/order-emails.js). This waits a few seconds
  // for it, and only if the server did not send them does the browser send
  // them instead (e.g. server emails not set up yet).
  function confirmWhenServerDone(ref, method, emailsSent, statusUrl) {
    if (emailsSent) { confirmOnlineOrder(ref, method, true); return; }
    var n = 0;
    (function again() {
      n++;
      setTimeout(function () {
        fetch(statusUrl).then(function (r) { return r.json(); }).catch(function () { return {}; }).then(function (d) {
          if (d.emailsSent) confirmOnlineOrder(ref, method, true);
          else if (n < 3) again();
          else confirmOnlineOrder(ref, method, false);
        });
      }, 2500);
    })();
  }

  // The shop's Web3Forms order email (full order, customer, address) always
  // goes out once the payment is confirmed. The customer's own confirmation
  // is sent from here only if the server did not already send it.
  function confirmOnlineOrder(ref, method, serverHandled) {
    var sentKey = 'b3d-confirmed-' + ref;
    try { if (localStorage.getItem(sentKey)) return; } catch (e) {}
    var o = readPendingOrder();
    if (!o || o.ref !== ref || !o.fields) {
      if (serverHandled) { try { localStorage.setItem(sentKey, '1'); } catch (e) {} clearPendingOrder(); }
      return;
    }
    var f = o.fields;
    if (confirmOnlineOrder._busy) return;
    confirmOnlineOrder._busy = true;

    var fd = new FormData();
    Object.keys(f).forEach(function (k) { fd.append(k, f[k]); });
    fd.set('access_key', W3F_ACCESS_KEY);
    fd.set('subject', 'Order CONFIRMED - paid by ' + method + ' - ' + ref);
    fd.set('order_id', ref);
    fd.set('payment_status', 'PAID - payment confirmed by ' + method + '. Amount: ' + o.total + ' SAR. Ready to prepare and ship.');
    // Only marked as sent once Web3Forms accepts it, so a failed send is retried
    // on the next visit (resumePendingOrder).
    fetch('https://api.web3forms.com/submit', { method: 'POST', body: fd, headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return r.ok && d.success !== false; }); })
      .catch(function () { return false; })
      .then(function (ok) {
        confirmOnlineOrder._busy = false;
        if (!ok) return;
        try { localStorage.setItem(sentKey, '1'); } catch (e) {}
        clearPendingOrder();
      });

    if (!serverHandled) sendEmailJs({
      to_email: f.email || '',
      to_name: ((f.customer_first_name || '') + ' ' + (f.customer_last_name || '')).trim(),
      order_id: ref,
      order_summary: f.order_summary || '',
      shipping_method: f.shipping_method || '',
      payment_method: method + ' (paid)',
      order_total: o.total != null ? o.total + ' SAR' : ''
    });
  }

  function showOnlineThanks(view) {
    ['[data-b3d-cart-header]', '[data-b3d-cart-empty]'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (el) el.hidden = true;
    });
    var layout = document.querySelector('.b3d-cart-layout');
    if (layout) layout.style.display = 'none';
    view.hidden = false;
    window.scrollTo(0, 0);
  }

  function fillOnlineThanks(view, ref) {
    var o = readPendingOrder();
    if (!o || o.ref !== ref || !o.fields) return;
    var linesEl = view.querySelector('[data-b3d-thanks-lines]');
    if (linesEl) {
      linesEl.textContent = '';
      String(o.fields.order_summary || '').split('\n').forEach(function (line) {
        if (!line || /^(Grand Total|Total|Shipping):/.test(line)) return;
        var row = document.createElement('div');
        row.textContent = line;
        linesEl.appendChild(row);
      });
    }
    var shipEl = view.querySelector('[data-b3d-thanks-shipping]');
    if (shipEl) shipEl.textContent = o.fields.shipping_method || '';
    var totEl = view.querySelector('[data-b3d-thanks-total]');
    if (totEl && o.total != null) totEl.textContent = o.total + ' SAR';
    var emailEl = view.querySelector('[data-b3d-thanks-email]');
    if (emailEl) emailEl.textContent = o.fields.email || '';
  }

  // A paid order whose confirmation emails were not sent yet (tab closed on the
  // gateway, slow webhook, failed send): check once on the next cart visit.
  function resumePendingOrder() {
    var params = new URLSearchParams(window.location.search);
    if (params.get('paid') || params.get('tabby')) return;
    var o = readPendingOrder();
    if (!o || !o.ref || !/^[a-f0-9]{24}$/.test(o.ref)) return;
    if (o.at && Date.now() - o.at > 14 * 864e5) { clearPendingOrder(); return; }
    var url = o.gateway === 'tabby' ? '/api/tabby/verify?ref=' : '/api/paymob/status?ref=';
    fetch(url + o.ref).then(function (r) { return r.json(); }).catch(function () { return {}; }).then(function (d) {
      if (d.status === 'paid') { confirmWhenServerDone(o.ref, o.method || 'Online payment', d.emailsSent, url + o.ref); }
      else if (d.status === 'failed') { clearPendingOrder(); }
    });
  }

  // Paymob (card, Apple Pay, Tamara) sends the customer back with ?paid=<ref>
  // on success and on failure alike, so the page asks the server, which only
  // trusts the signed webhook, before calling the order confirmed.
  function showCardReturn() {
    var params = new URLSearchParams(window.location.search);
    var ref = params.get('paid');
    if (!ref || !/^[a-f0-9]{24}$/.test(ref)) return;
    var pm = params.get('pm');
    var isTamara = pm === 'tamara';
    var method = isTamara ? 'Tamara (Pay Later)' : pm === 'applepay' ? 'Apple Pay (Paymob)' : 'Card (Paymob)';
    var view = document.querySelector('[data-b3d-thanks]');
    if (!view) return;
    view.querySelector('[data-b3d-thanks-order-id]').textContent = ref;
    view.querySelector('[data-b3d-thanks-payment]').textContent = method;
    fillOnlineThanks(view, ref);
    var lead = view.querySelector('[data-b3d-thanks-lead]');
    lead.removeAttribute('data-i18n');
    var ar = document.documentElement.lang === 'ar';
    lead.textContent = ar ? 'جارٍ تأكيد الدفع…' : 'Confirming your payment…';
    showOnlineThanks(view);

    // Pass on Paymob's signed result (id, success, hmac...) so the server can
    // confirm the payment even if Paymob's webhook hasn't reached it.
    var statusQs = new URLSearchParams(window.location.search);
    statusQs.delete('paid'); statusQs.delete('pm'); statusQs.set('ref', ref);
    var statusUrl = '/api/paymob/status/?' + statusQs.toString();
    var tries = 0;
    var check = function () {
      tries++;
      fetch(statusUrl).then(function (r) { return r.json(); }).catch(function () { return {}; }).then(function (d) {
        if (d.status === 'paid') {
          lead.textContent = ar
            ? 'تم تأكيد طلبك ودفعتك. أرسلنا تأكيد الطلب إلى بريدك الإلكتروني.'
            : 'Your order is confirmed and your payment is received. We have emailed you the order confirmation.';
          var snapPayload = snapCartPayload();
          snapPayload.transaction_id = ref;
          snapPayload.success = 1;
          pushSnapEvent('PURCHASE', snapPayload);
          saveCart({});
          confirmWhenServerDone(ref, method, d.emailsSent, '/api/paymob/status?ref=' + ref);
        } else if (d.status === 'failed') {
          lead.textContent = ar
            ? 'لم تكتمل عملية الدفع ولم يتم تقديم الطلب. ما زالت سلتك محفوظة، يرجى المحاولة مرة أخرى أو اختيار طريقة دفع أخرى.'
            : 'Your payment was not completed, so the order has not been placed. Your cart is still saved. Please try again or choose another payment method.';
          var layout = document.querySelector('.b3d-cart-layout');
          if (layout) layout.style.display = '';
          var hdr = document.querySelector('[data-b3d-cart-header]');
          if (hdr) hdr.hidden = false;
        } else if (tries < 40) {
          if (tries === 8) {
            lead.textContent = ar
              ? 'شكرًا لطلبك. ما زلنا نؤكد الدفع، وسنرسل لك بريدًا إلكترونيًا فور اكتماله.'
              : 'Thank you for your order. We are still confirming your payment and will email you as soon as it is complete.';
          }
          setTimeout(check, tries < 8 ? 2500 : 10000);
        }
      });
    };
    check();
  }

  // Tabby sends the customer back with ?tabby=<order ref>. The server checks the
  // payment with Tabby before anything is shown as paid.
  function showTabbyReturn() {
    var ref = new URLSearchParams(window.location.search).get('tabby');
    if (!ref || !/^[a-f0-9]{24}$/.test(ref)) return;
    var view = document.querySelector('[data-b3d-thanks]');
    if (!view) return;
    var lead = view.querySelector('[data-b3d-thanks-lead]');
    lead.removeAttribute('data-i18n');
    fetch('/api/tabby/verify?ref=' + encodeURIComponent(ref)).then(function (res) {
      return res.json().catch(function () { return {}; });
    }).then(function (data) {
      var status = data.status;
      if (status === 'failed') {
        lead.textContent = isAr()
          ? 'لم تكتمل عملية الدفع عبر تابي ولم يتم تقديم الطلب. ما زالت سلتك محفوظة، يرجى المحاولة مرة أخرى أو اختيار طريقة دفع أخرى.'
          : 'Your Tabby payment was not completed. Your order has not been placed. Your cart is still saved. Please try again or choose another payment method.';
        view.querySelector('[data-b3d-thanks-order-id]').textContent = ref;
        view.hidden = false;
        window.scrollTo(0, 0);
        return;
      }
      view.querySelector('[data-b3d-thanks-order-id]').textContent = ref;
      view.querySelector('[data-b3d-thanks-payment]').textContent = 'Tabby (Pay in 4)';
      var snapPayload = snapCartPayload();
      try {
        var sum = JSON.parse(sessionStorage.getItem('b3d-tabby-summary') || 'null');
        if (sum) {
          var totEl = view.querySelector('[data-b3d-thanks-total]');
          if (totEl && sum.total != null) totEl.textContent = sum.total;
          var shipEl = view.querySelector('[data-b3d-thanks-shipping]');
          if (shipEl && sum.shipping) shipEl.textContent = sum.shipping;
          if (sum.total != null) snapPayload.price = sum.total;
          sessionStorage.removeItem('b3d-tabby-summary');
        }
      } catch (e) {}
      if (status === 'paid') {
        snapPayload.transaction_id = ref;
        snapPayload.success = 1;
        pushSnapEvent('PURCHASE', snapPayload);
        saveCart({});
        fillOnlineThanks(view, ref);
        confirmWhenServerDone(ref, 'Tabby (Pay in 4)', data.emailsSent, '/api/tabby/verify?ref=' + encodeURIComponent(ref));
      }
      lead.textContent = status === 'paid'
        ? 'Thank you for your order. Your Tabby payment is confirmed. You will receive a confirmation email shortly.'
        : 'Thank you for your order. We are confirming your Tabby payment and will email you once it is complete.';
      ['[data-b3d-cart-header]', '[data-b3d-cart-empty]'].forEach(function (sel) {
        var el = document.querySelector(sel);
        if (el) el.hidden = true;
      });
      var layout = document.querySelector('.b3d-cart-layout');
      if (layout) layout.style.display = 'none';
      view.hidden = false;
      window.scrollTo(0, 0);
    }).catch(function () {
      lead.textContent = 'We could not confirm your Tabby payment just now. Please check your email or contact us on WhatsApp.';
      view.hidden = false;
    });
  }

  function showThankYou(form, mailOn) {
    var view = document.querySelector('[data-b3d-thanks]');
    if (!view) return;
    var val = function (sel) { var el = form.querySelector(sel); return el ? el.value : ''; };
    var snapPayload = snapCartPayload();
    snapPayload.transaction_id = val('[data-b3d-order-id]');
    snapPayload.success = 1;
    pushSnapEvent('PURCHASE', snapPayload);
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
    view.querySelector('[data-b3d-thanks-order-id]').textContent = val('[data-b3d-order-id]');
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
    renderGoogleCustomerReviewsOptIn(val('[data-b3d-order-id]'), val('[name="email"]'));
  }

  // Google Customer Reviews opt-in: shows Google's own survey prompt after
  // checkout so customers can agree to be asked for a seller rating later.
  // Loaded lazily, only once an order actually succeeds.
  var GOOGLE_MERCHANT_ID = 5863134037;

  function renderGoogleCustomerReviewsOptIn(orderId, email) {
    if (!orderId || !email) return;
    var deliveryDate = new Date();
    deliveryDate.setDate(deliveryDate.getDate() + 5); // matches the site's "4-5 business days" shipping copy
    var yyyy = deliveryDate.getFullYear();
    var mm = String(deliveryDate.getMonth() + 1).padStart(2, '0');
    var dd = String(deliveryDate.getDate()).padStart(2, '0');

    window.renderOptIn = function () {
      window.gapi.load('surveyoptin', function () {
        window.gapi.surveyoptin.render({
          merchant_id: GOOGLE_MERCHANT_ID,
          order_id: orderId,
          email: email,
          delivery_country: 'SA',
          estimated_delivery_date: yyyy + '-' + mm + '-' + dd
        });
      });
    };

    if (window.gapi && window.gapi.surveyoptin) { window.renderOptIn(); return; }
    if (document.getElementById('b3d-gcr-optin-script')) return;
    var script = document.createElement('script');
    script.id = 'b3d-gcr-optin-script';
    script.src = 'https://apis.google.com/js/platform.js?onload=renderOptIn';
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  }

  // Card (Paymob) and Tabby share this flow; only the endpoint differs.
  // A bank transfer order also goes to the CRM's Online Orders inbox, where it waits to be
  // confirmed (as an unpaid invoice) or rejected. Fire and forget: the order email has already
  // gone, so a failure here never troubles the customer.
  function sendBankOrderToCrm(form, orderId) {
    try {
      var cart = getCart();
      var items = Object.keys(cart).map(function (id) {
        var parsed = parseLineId(id);
        return { productId: parsed.productId, variantIndex: parsed.variantIndex, qty: cart[id] };
      });
      var get = function (name) { var el = form.querySelector('[name="' + name + '"]'); return el ? el.value : ''; };
      var shipping = form.querySelector('input[name="shipping_choice"]:checked');
      var shipFree = lastFreeShipping && shipping && shipping.value === 'regular';
      var shipPrice = shipFree ? 0 : (shipping ? parseInt(shipping.getAttribute('data-shipping-price'), 10) || 0 : 0);
      // The server checks the coupon, rewards and member delivery itself (by account and redemption).
      var tokenP = rewardsState && rewardsState.member && window.BlackArrow3DAuth
        ? Promise.resolve(window.BlackArrow3DAuth.getAccessToken()).catch(function () { return null; }) : Promise.resolve(null);
      tokenP.then(function (token) { return fetch('/api/bank-order/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        keepalive: true,
        body: JSON.stringify({
          orderId: orderId,
          authToken: token || undefined,
          couponRedemption: appliedCoupon && appliedCoupon.redemption ? appliedCoupon.redemption : '',
          items: items,
          shipping: shipping ? shipping.value : 'regular',
          shippingPrice: shipPrice,
          couponCode: appliedCoupon ? appliedCoupon.code : '',
          couponDiscount: couponDiscount(),
          rewardsUsed: rewardsDiscount(),
          bankSaving: bankSaving(),
          billing: {
            firstName: get('customer_first_name'),
            lastName: get('customer_last_name'),
            email: get('email'),
            phone: get('customer_phone'),
            city: get('customer_city'),
            street: get('customer_national_address'),
            building: get('customer_building'),
            apartment: get('customer_apartment'),
            postalCode: get('customer_postal_code')
          }
        })
      }); }).catch(function () {});
    } catch (e) { /* never block the order */ }
  }

  function startCardPayment(form, btn, errorEl, endpoint, extraBody) {
    var cm = document.querySelector('[data-b3d-coupon-msg]');
    if (appliedCoupon) {
      if (cm) { cm.textContent = 'Online payment does not support coupons yet. Remove the code or pay by bank transfer.'; cm.className = 'b3d-coupon__msg is-err'; }
      return;
    }
    var cart = getCart();
    var items = Object.keys(cart).map(function (id) {
      var parsed = parseLineId(id);
      var product = __b3dProductsById[parsed.productId];
      var item = { productId: parsed.productId, variantIndex: parsed.variantIndex, qty: cart[id] };
      if (product && product.bundlePick) {
        var picks = getBundlePicks(product.id);
        var expectedPickCount = product.bundlePick.min + (parsed.variantIndex || 0);
        if (picks.length === expectedPickCount) {
          item.bundlePicks = picks.map(function (pid) { var bp = __b3dProductsById[pid]; return bp ? L(bp, 'name') : pid; });
        }
      }
      return item;
    });
    var shipping = form.querySelector('input[name="shipping_choice"]:checked');
    var get = function (name) { var el = form.querySelector('[name="' + name + '"]'); return el ? el.value : ''; };
    var label = btn ? btn.textContent : '';
    if (btn) { btn.textContent = '...'; btn.disabled = true; }
    if (errorEl) errorEl.hidden = true;
    var payload = {
      items: items,
      shipping: shipping ? shipping.value : 'regular',
      lang: document.documentElement.lang === 'ar' ? 'ar' : 'en',
      billing: {
        firstName: get('customer_first_name'),
        lastName: get('customer_last_name'),
        email: get('email'),
        phone: get('customer_phone'),
        city: get('customer_city'),
        street: get('customer_national_address'),
        building: get('customer_building'),
        apartment: get('customer_apartment'),
        postalCode: get('customer_postal_code')
      }
    };
    if (extraBody) { for (var k in extraBody) { payload[k] = extraBody[k]; } }
    // Members: the server checks the account itself and applies their balance
    // (if ticked) and Gold/Platinum free delivery to the real charge.
    payload.useRewards = rewardsDiscount() > 0;
    var tokenP = rewardsState && rewardsState.member && window.BlackArrow3DAuth
      ? window.BlackArrow3DAuth.getAccessToken() : Promise.resolve(null);
    tokenP.then(function (token) {
      if (token) payload.authToken = token;
      return fetch(endpoint || '/api/paymob/create-intention', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (!res.ok || !data.checkoutUrl) throw new Error(data.error || 'failed');
        try { sessionStorage.setItem('b3d-tabby-summary', JSON.stringify({ total: data.amount_sar, shipping: (form.querySelector('[data-b3d-shipping-field]') || {}).value || '' })); } catch (e) {}
        // No email is sent here on purpose: a customer who starts checkout but
        // never finishes paying (closes the gateway tab, card declined, abandons
        // Tabby/Tamara) should never generate an order notification. The order
        // is only saved locally (so the confirmed-payment flow below can find it
        // again) and the shop/customer emails only fire from confirmOnlineOrder(),
        // once the gateway has actually confirmed the payment.
        try {
          var fd = new FormData(form);
          var method = (form.querySelector('[data-b3d-order-payment]') || {}).value || 'Online payment';
          var keep = {};
          fd.forEach(function (v, k) { if (k !== 'access_key' && k !== 'botcheck' && typeof v === 'string') keep[k] = v; });
          keep.order_id = data.orderRef;
          savePendingOrder({ ref: data.orderRef, total: data.amount_sar, method: method, gateway: endpoint && endpoint.indexOf('tabby') !== -1 ? 'tabby' : 'paymob', at: Date.now(), fields: keep });
        } catch (e) {}
        window.location.href = data.checkoutUrl;
      });
    }).catch(function () {
      if (errorEl) errorEl.hidden = false;
      if (btn) { btn.textContent = label; btn.disabled = false; }
    });
  }

  // National Address short code (4 letters + 4 numbers, e.g. RRRD2929) and the 4-number building
  // number: tidied as typed (capitals, no spaces; English digits) and checked with a clear message.
  function toLatinDigits(v) {
    return String(v || '').replace(/[\u0660-\u0669]/g, function (d) { return String(d.charCodeAt(0) - 0x0660); })
      .replace(/[\u06F0-\u06F9]/g, function (d) { return String(d.charCodeAt(0) - 0x06F0); });
  }
  function initAddressChecks(form) {
    var rules = [
      { name: 'customer_national_address', tidy: function (v) { return toLatinDigits(v).toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 8); }, ok: /^[A-Z]{4}[0-9]{4}$/, msg: 'checkout_national_invalid' },
      { name: 'customer_building', tidy: function (v) { return toLatinDigits(v).replace(/[^0-9]/g, '').slice(0, 4); }, ok: /^[0-9]{4}$/, msg: 'checkout_building_invalid' }
    ];
    rules.forEach(function (r) {
      var el = form.querySelector('[name="' + r.name + '"]');
      if (!el) return;
      var check = function () {
        var tidy = r.tidy(el.value);
        if (tidy !== el.value) el.value = tidy;
        el.setCustomValidity(!tidy || r.ok.test(tidy) ? '' : T(r.msg));
      };
      el.addEventListener('input', check);
      el.addEventListener('blur', check);
      el._b3dCheck = check;
    });
    return function () { rules.forEach(function (r) { var el = form.querySelector('[name="' + r.name + '"]'); if (el && el._b3dCheck) el._b3dCheck(); }); };
  }

  function initCheckoutSubmit(form) {
    if (!form) return;
    var checkAddress = initAddressChecks(form);
    var successEl = document.getElementById('b3d-checkout-success');
    var errorEl = document.getElementById('b3d-checkout-error');
    var submitBtn = form.querySelector('[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      checkAddress();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var payField = form.querySelector('[data-b3d-order-payment]');
      if (payField && payField.value === 'Card (Paymob)') { startCardPayment(form, submitBtn, errorEl); return; }
      if (payField && payField.value === 'Tabby (Pay in 4)') { startCardPayment(form, submitBtn, errorEl, '/api/tabby/create-session'); return; }
      if (payField && payField.value === 'Apple Pay (Paymob)') { startCardPayment(form, submitBtn, errorEl, '/api/paymob/create-intention', { channel: 'applepay' }); return; }
      if (payField && payField.value === 'Tamara (Pay Later)') { startCardPayment(form, submitBtn, errorEl, '/api/paymob/create-intention', { channel: 'tamara' }); return; }

      var label = submitBtn ? submitBtn.textContent : '';
      if (submitBtn) { submitBtn.textContent = '...'; submitBtn.disabled = true; }
      if (errorEl) errorEl.hidden = true;
      if (successEl) successEl.hidden = true;

      // A retry after a failed send keeps the same order id, so rewards
      // balance already spent on it is reused instead of spent twice.
      var orderIdP = rewardsState && rewardsState.redeemed
        ? Promise.resolve(rewardsState.redeemed.orderId) : nextOrderId();
      var orderId = null;
      orderIdP.then(function (id) {
        orderId = id;
        var orderIdField = form.querySelector('[data-b3d-order-id]');
        if (orderIdField) orderIdField.value = orderId;
        return redeemAppliedCoupon();
      }).then(function (r) {
        if (!r.ok) {
          appliedCoupon = null;
          try { sessionStorage.removeItem(COUPON_KEY); } catch (e) {}
          updateOrderTotals();
          var cm = document.querySelector('[data-b3d-coupon-msg]');
          if (cm) { cm.textContent = T('coupon_gone'); cm.className = 'b3d-coupon__msg is-err'; }
          throw new Error('coupon');
        }
        var wanted = rewardsDiscount();
        if (!wanted || rewardsState.redeemed) return null;
        return window.BlackArrow3DRewards.redeemForOrder(orderId, wanted).then(function (used) {
          rewardsState.redeemed = { orderId: orderId, used: used };
          updateOrderTotals();
        }, function () {
          rewardsState.use = false;
          updateOrderTotals();
          var cm = document.querySelector('[data-b3d-coupon-msg]');
          if (cm) {
            cm.textContent = isAr()
              ? 'تعذّر استخدام رصيد المكافآت الآن، فأزلناه من الطلب. راجع المجموع ثم أرسل الطلب مرة أخرى.'
              : 'Your rewards balance could not be used just now, so it was removed from this order. Check the total and place the order again.';
            cm.className = 'b3d-coupon__msg is-err';
          }
          throw new Error('coupon');
        });
      }).then(function () {
        return fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' }
        });
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          if (!res.ok || data.success === false) throw new Error(data.message || 'failed');
          sendBankOrderToCrm(form, orderId);
          var mailCfg = window.BLACK_ARROW_EMAILJS_CONFIG;
          var mailOn = !!(mailCfg && mailCfg.publicKey && mailCfg.serviceId && mailCfg.templateId);
          showThankYou(form, mailOn);
          sendCustomerConfirmation(form);
          saveCart({});
          if (rewardsState && rewardsState.redeemed) {
            rewardsState.member.balance = Math.max(0, rewardsState.member.balance - rewardsState.redeemed.used);
            rewardsState.redeemed = null;
          }
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
      var artworkSubtotal = 0;
      var summaryLines = [];
      var hasPreorder = false;
      listEl.innerHTML = ids.map(function (id) {
        var parsed = parseLineId(id);
        var p = byId[parsed.productId];
        if (!p) return '';
        var variant = parsed.variantIndex != null && p.variants ? p.variants[parsed.variantIndex] : null;
        var qty = cart[id];
        var unit = variant ? variant.price : ((p.onSale && p.salePrice != null) ? p.salePrice : p.price);
        var lineTotal = unit * qty;
        subtotal += lineTotal;
        if (p.category === '3D Artwork') artworkSubtotal += lineTotal;
        if (p.preorder) hasPreorder = true;
        var displayName = L(p, 'name') + (variant ? ' — ' + LVariant(variant) : '');
        var bundleLineHtml = '';
        var pickNames = null;
        if (p.bundlePick) {
          var picks = getBundlePicks(p.id);
          var expectedCount = p.bundlePick.min + (parsed.variantIndex || 0);
          if (picks.length === expectedCount) {
            pickNames = picks.map(function (pid) { var bp = byId[pid]; return bp ? L(bp, 'name') : pid; });
            bundleLineHtml = '<div class="b3d-cart-item__bundle">' + pickNames.join(', ') + '</div>';
          } else {
            bundleLineHtml = '<div class="b3d-cart-item__bundle b3d-cart-item__bundle--warn">' + T('js_cart_bundle_missing') + '</div>';
          }
          bundleLineHtml += '<a class="b3d-cart-item__bundle-edit" href="' + productUrl(p) + '">' + T('js_cart_bundle_edit') + '</a>';
        }
        var summaryLine = displayName + ' x' + qty + ' — ' + lineTotal.toLocaleString('en-US') + ' ' + (p.currency || 'SAR');
        if (pickNames) summaryLine += ' (' + pickNames.join(', ') + ')';
        summaryLines.push(summaryLine);
        return '' +
          '<div class="b3d-cart-item" data-line-id="' + id + '">' +
            '<div class="b3d-cart-item__visual">' + visual(p) + '</div>' +
            '<div>' +
              '<div class="b3d-cart-item__name">' + displayName + '</div>' +
              '<div class="b3d-cart-item__cat">' + categoryLabel(p.category) + (p.preorder ? ' · <span class="b3d-cart-item__preorder">' + T('js_pre_order') + '</span>' : '') + '</div>' +
              bundleLineHtml +
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

      var preorderNotice = document.querySelector('[data-b3d-preorder-notice]');
      if (preorderNotice) preorderNotice.hidden = !hasPreorder;

      var crosssell = document.querySelector('[data-b3d-cart-crosssell]');
      if (crosssell) {
        var inCartIds = ids.map(function (id) { return parseLineId(id).productId; });
        var hasPrinter = inCartIds.some(function (pid) { var p = byId[pid]; return p && p.category === '3D Printers'; });
        if (hasPrinter) {
          var picks = products.filter(function (p) {
            return p.category === '3D Artwork' && p.available !== false && currentPrice(p) <= 60 &&
              inCartIds.indexOf(p.id) === -1;
          }).slice(0, 4);
          if (picks.length) {
            var crosssellGrid = crosssell.querySelector('[data-b3d-cart-crosssell-grid]');
            renderGrid(picks, crosssellGrid);
            if (!crosssellGrid._b3dBound) {
              crosssellGrid._b3dBound = true;
              crosssellGrid.addEventListener('click', function (e) {
                if (e.target.closest && e.target.closest('[data-card-add]')) {
                  setTimeout(function () { renderCartPage(listEl, summaryEl, emptyEl); }, 50);
                }
              });
            }
            crosssell.hidden = false;
          } else {
            crosssell.hidden = true;
          }
        } else {
          crosssell.hidden = true;
        }
      }

      lastSubtotal = subtotal;
      lastArtworkSubtotal = artworkSubtotal;
      // Free Regular delivery with any 3D printer in the order (same rule as api/_lib/pricing.js).
      var hasPrinter = Object.keys(cart).some(function (id) { var pp = __b3dProductsById[parseLineId(id).productId]; return !!pp && pp.category === '3D Printers'; });
      lastFreeShipping = hasPrinter || artworkSubtotal >= FREE_SHIP_ARTWORK_MIN || subtotal >= FREE_SHIP_PRINTER_MIN || memberFreeDelivery();
      updateFreeShippingUi(artworkSubtotal, subtotal);
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
    // Apple Pay is only offered where the device can actually use it.
    var applePayBtn = root.querySelector('[data-b3d-applepay]');
    if (applePayBtn) {
      try { applePayBtn.hidden = !(window.ApplePaySession && window.ApplePaySession.canMakePayments()); } catch (e) { applePayBtn.hidden = true; }
    }
    var methods = root.querySelectorAll('[data-pm]');
    function select(el) {
      if (el.hasAttribute('disabled')) return;
      methods.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
      el.setAttribute('aria-pressed', 'true');
      var method = el.getAttribute('data-pm');
      root.querySelectorAll('[data-pm-detail]').forEach(function (d) {
        d.hidden = d.getAttribute('data-pm-detail') !== method;
      });
      updateCheckoutFields(method);
    }
    methods.forEach(function (el) {
      el.addEventListener('click', function () { select(el); });
    });
    // Bank Transfer is the only method now, so there's no real "choice" to
    // make — pre-select it instead of hiding the checkout form behind an
    // extra click.
    if (methods.length === 1) select(methods[0]);
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

    var priceValue = currentPrice(p);
    // Unused printers and filament: 7 days; everything else: defects / wrong item / shipping damage within 3 days.
    var sevenDay = p.category === '3D Printers' || p.category === 'Filament';
    var returnPolicy = {
      '@type': 'MerchantReturnPolicy',
      'applicableCountry': 'SA',
      'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow',
      'merchantReturnDays': sevenDay ? 7 : 3,
      'merchantReturnLink': 'https://www.blackarrowksa.com/3d/returns/',
      'returnMethod': 'https://schema.org/ReturnByMail',
      'returnFees': sevenDay ? 'https://schema.org/ReturnShippingFees' : 'https://schema.org/FreeReturn'
    };
    var stockUrl = function (unavailable) {
      return unavailable ? 'https://schema.org/OutOfStock' : (p.preorder ? 'https://schema.org/PreOrder' : 'https://schema.org/InStock');
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
            'availability': stockUrl(v.available === false),
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
          'availability': stockUrl(p.available === false),
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
      var heroImg = p.cardImage || firstAvailableVariantImage(p) || (images.length ? images[0] : null);
      var thumbsHtml = images.length > 1
        ? '<div class="b3d-pd__thumbs">' + images.map(function (src, i) {
            var thumbLabel = T('js_view_image') + ' ' + (i + 1) + ' — ' + L(p, 'name');
            return '<button class="b3d-pd__thumb' + (src === heroImg ? ' is-active' : '') + '" data-thumb-src="' + src + '" aria-label="' + thumbLabel + '"><img src="' + thumbSrc(src) + '" alt="' + thumbLabel + '" loading="lazy" decoding="async" width="80" height="80"></button>';
          }).join('') + '</div>'
        : '';
      var pdAvailable = p.available !== false;
      var heroSet = heroImg ? imgSrcset(heroImg) : '', heroDim = imgSize(heroImg);
      var mainVisual = heroImg ? '<img src="' + heroImg + '"' + (heroSet ? ' srcset="' + heroSet + '" sizes="(max-width: 860px) 92vw, 560px"' : '') +
        (heroDim ? ' width="' + heroDim[0] + '" height="' + heroDim[1] + '"' : '') + ' fetchpriority="high" decoding="async" alt="' + L(p, 'name') + '" data-pd-main-img>' : '<div class="b3d-card__visual-placeholder">' + T('js_product_image') + '</div>';

      var hasVariants = !!(p.variants && p.variants.length);
      var hasSwatches = hasVariants && p.variants.some(function (v) { return !!v.swatch; });
      var firstOk = hasVariants ? p.variants.findIndex(function (v) { return v.available !== false; }) : 0;
      if (firstOk < 0) firstOk = 0;
      var selectedVariant = firstOk;
      var initV = hasVariants ? p.variants[firstOk] : null;
      var variantSelectorHtml = hasVariants
        ? '<div class="b3d-pd__variants' + (hasSwatches ? ' b3d-pd__swatches' : '') + '" data-pd-variants style="display:flex;gap:' + (hasSwatches ? '10px' : '8px') + ';flex-wrap:wrap;margin-bottom:20px;align-items:center;">' +
            p.variants.map(function (v, i) {
              if (v.swatch) {
                return '<button type="button" class="b3d-swatch' + (v.available === false ? ' is-unavailable' : '') + '" data-variant-idx="' + i + '" aria-pressed="' + (i === firstOk) + '" title="' + LVariant(v) + (v.available === false ? ' (' + T('js_out_of_stock') + ')' : '') + '" style="background:' + v.swatch + ';"></button>';
              }
              var pOut = v.available === false;
              return '<button type="button" class="b3d-quick-pill' + (pOut ? ' is-out' : '') + '" data-variant-idx="' + i + '" aria-pressed="' + (i === firstOk) + '">' + LVariant(v) + (pOut ? ' (' + T('js_out_of_stock') + ')' : '') + '</button>';
            }).join('') +
          '</div>' +
          (hasSwatches ? '<div class="b3d-pd__swatch-label" data-pd-swatch-label style="color:rgba(255,255,255,.75);font-size:.85rem;margin:-12px 0 20px;">' + LVariant(initV) + '</div>' : '')
        : '';
      // Combo-builder products pick their tier by how many items are added
      // below, not from the raw variant pills — the tiers are still real
      // variants underneath (for trusted, correct checkout pricing).
      if (p.bundlePick) variantSelectorHtml = '';
      function buyState(v) {
        var out = !pdAvailable || !!(v && v.available === false);
        var pre = p.preorder || !!(v && v.preorder && !out);
        return { disabled: out && !p.preorder, label: pre ? T('js_pre_order') : (out ? T('js_out_of_stock') : T('js_add_to_cart')) };
      }
      var initBuy = buyState(initV);

      var bundleItems = p.bundlePick ? p.bundlePick.fromIds.map(function (id) {
        return products.filter(function (x) { return x.id === id; })[0];
      }).filter(Boolean) : [];
      var bundleMin = p.bundlePick ? p.bundlePick.min : 0;
      var bundleMax = p.bundlePick ? (bundleMin + p.variants.length - 1) : 0;
      var bundleSelected = p.bundlePick ? getBundlePicks(p.id).filter(function (id) {
        return bundleItems.some(function (b) { return b.id === id; });
      }).slice(0, bundleMax) : [];
      function bundleTierPrice(count) {
        return p.variants[Math.max(0, Math.min(count, bundleMax) - bundleMin)].price;
      }
      function bundleSeparateTotal(ids) {
        return ids.reduce(function (sum, id) {
          var it = bundleItems.filter(function (b) { return b.id === id; })[0];
          return sum + (it ? currentPrice(it) : 0);
        }, 0);
      }
      function bundlePriceRowHtml(selectedIds) {
        if (selectedIds.length < bundleMin) return '';
        var comboPrice = bundleTierPrice(selectedIds.length);
        var separate = bundleSeparateTotal(selectedIds);
        var save = separate - comboPrice;
        return '<div class="b3d-bundle-pick__price-row" data-bundle-price-row>' +
          '<span>' + T('js_bundle_pick_you_pay') + ' <b>' + money(comboPrice, p.currency) + '</b></span>' +
          (save > 0 ? '<span class="b3d-bundle-pick__save">' + T('js_bundle_pick_save') + ' ' + money(save, p.currency) + '</span>' : '') +
          '</div>';
      }
      if (p.bundlePick && bundleSelected.length >= bundleMin) {
        selectedVariant = bundleSelected.length - bundleMin;
        initV = p.variants[selectedVariant];
      }
      var bundlePickHtml = p.bundlePick
        ? '<div class="b3d-bundle-pick" data-bundle-pick>' +
            '<h2>' + T('js_bundle_pick_title') + ' <span class="b3d-bundle-pick__count" data-bundle-count>' + bundleSelected.length + ' ' + T('js_bundle_pick_selected') + '</span></h2>' +
            '<p class="b3d-bundle-pick__hint">' + T('js_bundle_pick_hint') + '</p>' +
            '<div class="b3d-bundle-pick__grid">' +
              bundleItems.map(function (b) {
                var isSel = bundleSelected.indexOf(b.id) !== -1;
                var img = primaryImage(b);
                return '<button type="button" class="b3d-bundle-pick__item' + (isSel ? ' is-selected' : '') + '" data-bundle-item="' + b.id + '" aria-pressed="' + isSel + '">' +
                  (img ? '<img src="' + img + '" alt="" loading="lazy">' : '') +
                  '<span class="b3d-bundle-pick__name">' + L(b, 'name') + '</span>' +
                  '<span class="b3d-bundle-pick__check" aria-hidden="true">&#10003;</span>' +
                '</button>';
              }).join('') +
            '</div>' +
            '<div data-bundle-price-row-wrap>' + bundlePriceRowHtml(bundleSelected) + '</div>' +
          '</div>'
        : '';
      /* Out of stock right now? (whole product, or the option currently picked) */
      function selectionOut() {
        if (p.preorder || p.bundlePick) return false;
        return !pdAvailable || !!(hasVariants && p.variants[selectedVariant] && p.variants[selectedVariant].available === false);
      }

      /* Back-in-stock alert: shown only while the current selection is out of stock. */
      var restockHtml = p.bundlePick ? '' :
        '<div class="b3d-restock" data-restock' + (selectionOut() ? '' : ' hidden') + '>' +
          '<button type="button" class="b3d-restock__open" data-restock-open><span aria-hidden="true">&#128276;</span> ' + T('js_restock_btn') + '</button>' +
          '<form class="b3d-restock__form" data-restock-form hidden novalidate>' +
            '<label for="b3d-restock-contact">' + T('js_restock_title') + '</label>' +
            '<div class="b3d-restock__row">' +
              '<input id="b3d-restock-contact" type="text" inputmode="email" autocomplete="email" maxlength="80" placeholder="' + T('js_restock_placeholder') + '">' +
              '<button type="submit" class="btn btn-primary">' + T('js_restock_submit') + '</button>' +
            '</div>' +
            '<p class="b3d-restock__msg" data-restock-msg role="status"></p>' +
          '</form>' +
        '</div>';

      /* Frequently bought together: ids (or "id::variantIndex") listed in p.boughtTogether.
         Anything out of stock is left out automatically. */
      var fbtItems = p.bundlePick ? [] : (p.boughtTogether || []).map(function (ref) {
        var parts = String(ref).split('::');
        var bp = products.filter(function (x) { return x.id === parts[0]; })[0];
        if (!bp || bp.available === false || bp.bundlePick) return null;
        var vi = null;
        if (bp.variants && bp.variants.length) {
          vi = parts.length > 1 ? parseInt(parts[1], 10) : bp.variants.findIndex(function (v) { return v.available !== false; });
          if (vi < 0 || !bp.variants[vi] || bp.variants[vi].available === false) return null;
        }
        return { p: bp, vi: vi, price: vi == null ? currentPrice(bp) : bp.variants[vi].price };
      }).filter(Boolean).slice(0, 3);
      function mainPrice() { return hasVariants ? p.variants[selectedVariant].price : currentPrice(p); }
      var fbtHtml = fbtItems.length ?
        '<div class="b3d-fbt" data-fbt>' +
          '<h2>' + T('js_fbt_title') + '</h2>' +
          '<ul class="b3d-fbt__list">' +
            '<li><label class="b3d-fbt__item"><input type="checkbox" data-fbt-main' + (selectionOut() ? ' disabled' : ' checked') + '>' +
              (primaryImage(p) ? '<img src="' + primaryImage(p) + '" alt="" loading="lazy" width="56" height="56">' : '') +
              '<span class="b3d-fbt__name"><small>' + T('js_fbt_this') + '</small>' + L(p, 'name') + '</span>' +
              '<span class="b3d-fbt__price" data-fbt-main-price>' + money(mainPrice(), p.currency) + '</span></label></li>' +
            fbtItems.map(function (it, i) {
              var img = (it.vi != null && it.p.variants[it.vi].image) || primaryImage(it.p);
              return '<li><label class="b3d-fbt__item"><input type="checkbox" data-fbt-idx="' + i + '" checked>' +
                (img ? '<img src="' + img + '" alt="" loading="lazy" width="56" height="56">' : '') +
                '<span class="b3d-fbt__name"><a href="' + productUrl(it.p) + '">' + L(it.p, 'name') + '</a>' +
                (it.vi != null ? '<small>' + LVariant(it.p.variants[it.vi]) + '</small>' : '') + '</span>' +
                '<span class="b3d-fbt__price">' + money(it.price, it.p.currency) + '</span></label></li>';
            }).join('') +
          '</ul>' +
          '<div class="b3d-fbt__foot"><span>' + T('js_fbt_total') + ': <b data-fbt-total></b></span>' +
            '<button type="button" class="btn btn-primary" data-fbt-add>' + T('js_fbt_add') + '</button></div>' +
        '</div>' : '';

      var initialPriceHtml = hasVariants
        ? variantPriceHtml(initV, p)
        : priceBlock(p);
      var initialSaveHtml = hasVariants
        ? (initV.oldPrice ? saveAmountHtml(initV.oldPrice, initV.price, p.currency) : '')
        : ((p.onSale && p.salePrice != null) ? saveAmountHtml(p.price, p.salePrice, p.currency) : '');

      container.innerHTML = '' +
        '<div>' +
          '<div class="b3d-pd__visual' + (p.category === '3D Artwork' ? ' b3d-pd__visual--art' : '') + '" data-pd-zoom>' +
            badgesHtml(p, hasVariants ? initV : null) +
            mainVisual +
          '</div>' +
          thumbsHtml +
        '</div>' +
        '<div>' +
          '<div class="b3d-pd__cat">' + (p.brand ? p.brand + ' &middot; ' : '') + categoryLabel(p.category) + '</div>' +
          '<h1 class="b3d-pd__title">' + L(p, 'name') + '</h1>' +
          '<a class="b3d-pd__rating" href="#b3d-pd-reviews" data-pd-rating hidden></a>' +
          '<div class="b3d-pd__price-row"><div class="b3d-pd__price" data-pd-price>' + initialPriceHtml + '</div><span data-pd-save>' + initialSaveHtml + '</span></div>' + vatNoteHtml(p) +
          '<div data-pd-bnpl>' + (selectionOut() ? '' : bnplHtml(hasVariants ? initV.price : currentPrice(p), p.currency)) + '</div>' +
          variantSelectorHtml +
          trustRowHtml(p) +
          '<div data-pd-eta>' + (selectionOut() || p.preorder ? '' : etaHtml(p)) + '</div>' +
          '<p class="b3d-pd__desc">' + (L(p, 'description') || '') + '</p>' +
          kitBoxHtml(p) +
          kitUpsellHtml(p, products) +
          bundlePickHtml +
          '<div class="b3d-pd__actions">' +
            '<div class="b3d-qty">' +
              '<button type="button" data-pd-qty="minus" aria-label="' + T('js_qty_decrease') + '">−</button>' +
              '<input type="text" readonly value="1" data-pd-qty-val aria-label="' + T('js_qty_label') + '">' +
              '<button type="button" data-pd-qty="plus" aria-label="' + T('js_qty_increase') + '">+</button>' +
            '</div>' +
            '<button class="btn btn-primary b3d-pd__buy" data-pd-add ' + ((p.bundlePick ? bundleSelected.length < bundleMin : initBuy.disabled) ? 'disabled' : '') + '>' + (p.bundlePick ? T('js_add_to_cart') : initBuy.label) + '</button>' +
          '</div>' +
          (p.bundlePick ? '<p class="b3d-bundle-pick__disabled-hint" data-bundle-hint' + (bundleSelected.length >= bundleMin ? ' hidden' : '') + '>' + T('js_bundle_pick_disabled_hint') + '</p>' : '') +
          restockHtml +
          '<a class="b3d-pd__wa" data-pd-wa href="' + waHref(p, hasVariants ? initV : null) + '" target="_blank" rel="noopener noreferrer">' + WA_ICON + '<span>' + waLabel(p) + '</span></a>' +
          '<div class="b3d-pd__contact-actions">' +
            '<a href="/3d/cart/">' + T('js_view_cart') + '</a>' +
            (p.category === '3D Artwork' ? '' : '<button type="button" data-pd-compare="' + p.id + '">' + T('js_compare_btn') + '</button>') +
          '</div>' +
          fbtHtml +
          (specsHtml ? '<table class="b3d-spec-table"><tbody>' + specsHtml + '</tbody></table>' : '') +
          compatHtml +
          (L(p, 'warranty') ? '<div class="b3d-pd__warranty"><h2>' + T('js_warranty_heading') + '</h2><p>' + L(p, 'warranty') + '</p></div>' : '') +
          guidesHtml(p) +
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
          if (mainImg) setMainImg(mainImg, btn.getAttribute('data-thumb-src'));
        });
      });

      var zoomTarget = container.querySelector('[data-pd-zoom]');
      var mainImgEl = container.querySelector('[data-pd-main-img]');
      // near-square or wide artwork (marketing renders with text) is shown whole instead of cropped to the 4:5 frame
      var fitFrame = function () {
        if (mainImgEl && mainImgEl.naturalHeight) mainImgEl.parentNode.classList.toggle('is-wide', mainImgEl.naturalWidth / mainImgEl.naturalHeight > 0.85);
      };
      if (mainImgEl) { mainImgEl.addEventListener('load', fitFrame); fitFrame(); }
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
            container.querySelector('[data-pd-price]').innerHTML = variantPriceHtml(v, p);
            var saveEl = container.querySelector('[data-pd-save]');
            if (saveEl) saveEl.innerHTML = v.oldPrice ? saveAmountHtml(v.oldPrice, v.price, p.currency) : '';
            var swatchLabel = container.querySelector('[data-pd-swatch-label]');
            if (swatchLabel) swatchLabel.textContent = LVariant(v) + (v.available === false ? ' (' + T('js_out_of_stock') + ')' : '');
            var buyBtn = container.querySelector('[data-pd-add]');
            if (buyBtn) { var bs = buyState(v); buyBtn.disabled = bs.disabled; buyBtn.textContent = bs.label; }
            refreshStockUi();
            if (v.image) {
              var mainImg = container.querySelector('[data-pd-main-img]');
              if (mainImg) setMainImg(mainImg, v.image);
              container.querySelectorAll('[data-thumb-src]').forEach(function (t) {
                t.classList.toggle('is-active', t.getAttribute('data-thumb-src') === v.image);
              });
            }
          });
        });
      }

      if (p.bundlePick) {
        var picked = bundleSelected.slice();
        var countEl = container.querySelector('[data-bundle-count]');
        var hintEl = container.querySelector('[data-bundle-hint]');
        var priceRowWrap = container.querySelector('[data-bundle-price-row-wrap]');
        var addBtnEl = container.querySelector('[data-pd-add]');
        var pdPriceEl = container.querySelector('[data-pd-price]');
        function refreshBundleUi() {
          if (countEl) countEl.textContent = picked.length + ' ' + T('js_bundle_pick_selected');
          var ok = picked.length >= bundleMin;
          if (addBtnEl) addBtnEl.disabled = !ok;
          if (hintEl) hintEl.hidden = ok;
          if (priceRowWrap) priceRowWrap.innerHTML = bundlePriceRowHtml(picked);
          if (ok) {
            selectedVariant = picked.length - bundleMin;
            if (pdPriceEl) pdPriceEl.innerHTML = variantPriceHtml(p.variants[selectedVariant], p);
            var bnplWrapB = container.querySelector('[data-pd-bnpl]');
            if (bnplWrapB) bnplWrapB.innerHTML = bnplHtml(p.variants[selectedVariant].price, p.currency);
          }
        }
        container.querySelectorAll('[data-bundle-item]').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var id = btn.getAttribute('data-bundle-item');
            var idx = picked.indexOf(id);
            if (idx !== -1) {
              picked.splice(idx, 1);
              btn.classList.remove('is-selected');
              btn.setAttribute('aria-pressed', 'false');
            } else {
              if (picked.length >= bundleMax) return;
              picked.push(id);
              btn.classList.add('is-selected');
              btn.setAttribute('aria-pressed', 'true');
            }
            refreshBundleUi();
          });
        });
      }

      /* --- restock alert + bought-together: keep in step with the selected option --- */
      var restockEl = container.querySelector('[data-restock]');
      var fbtEl = container.querySelector('[data-fbt]');
      function refreshFbt() {
        if (!fbtEl) return;
        var mainBox = fbtEl.querySelector('[data-fbt-main]');
        var out = selectionOut();
        if (out) mainBox.checked = false;
        else if (mainBox.disabled) mainBox.checked = true;   // back in stock option picked: include it again
        mainBox.disabled = out;
        fbtEl.querySelector('[data-fbt-main-price]').innerHTML = money(mainPrice(), p.currency);
        var total = mainBox.checked ? mainPrice() : 0, any = mainBox.checked;
        fbtEl.querySelectorAll('[data-fbt-idx]').forEach(function (box) {
          if (box.checked) { total += fbtItems[+box.getAttribute('data-fbt-idx')].price; any = true; }
        });
        fbtEl.querySelector('[data-fbt-total]').innerHTML = money(Math.round(total * 100) / 100, p.currency);
        fbtEl.querySelector('[data-fbt-add]').disabled = !any;
      }
      function refreshStockUi() {
        syncStockBadge(container.querySelector('.b3d-pd__visual'), p, hasVariants ? p.variants[selectedVariant] : null);
        if (restockEl) restockEl.hidden = !selectionOut();
        var etaWrap = container.querySelector('[data-pd-eta]');
        if (etaWrap) etaWrap.innerHTML = (selectionOut() || p.preorder) ? '' : etaHtml(p);
        var waBtn = container.querySelector('[data-pd-wa]');
        if (waBtn && hasVariants) waBtn.href = waHref(p, p.variants[selectedVariant]);
        var bnplWrap = container.querySelector('[data-pd-bnpl]');
        if (bnplWrap) bnplWrap.innerHTML = selectionOut() ? '' : bnplHtml(mainPrice(), p.currency);
        refreshFbt();
      }
      if (fbtEl) {
        fbtEl.addEventListener('change', refreshFbt);
        var fbtAdd = fbtEl.querySelector('[data-fbt-add]');
        fbtAdd.addEventListener('click', function () {
          if (fbtEl.querySelector('[data-fbt-main]').checked) addToCart(hasVariants ? lineId(p.id, selectedVariant) : p.id, 1);
          fbtEl.querySelectorAll('[data-fbt-idx]').forEach(function (box) {
            if (!box.checked) return;
            var it = fbtItems[+box.getAttribute('data-fbt-idx')];
            addToCart(lineId(it.p.id, it.vi), 1);
          });
          fbtAdd.textContent = T('js_fbt_added');
          setTimeout(function () { fbtAdd.textContent = T('js_fbt_add'); }, 1500);
        });
        refreshFbt();
      }
      if (restockEl) {
        var rsForm = restockEl.querySelector('[data-restock-form]');
        var rsMsg = restockEl.querySelector('[data-restock-msg]');
        restockEl.querySelector('[data-restock-open]').addEventListener('click', function () {
          rsForm.hidden = false;
          this.hidden = true;
          rsForm.querySelector('input').focus();
        });
        rsForm.addEventListener('submit', function (e) {
          e.preventDefault();
          var contact = normalizeContact(rsForm.querySelector('input').value);
          if (!contact) { rsMsg.textContent = T('js_restock_invalid'); return; }
          var variantLabel = hasVariants ? (p.variants[selectedVariant].label || '') : '';
          var btn = rsForm.querySelector('button');
          btn.disabled = true;
          submitRestockAlert(p.id, variantLabel, contact).then(function (ok) {
            if (ok) {
              rsForm.innerHTML = '<p class="b3d-restock__msg is-done">' + T('js_restock_done') + '</p>';
              if (window.dataLayer) window.dataLayer.push({ event: 'restock_alert', item_id: p.id });
              return;
            }
            // Service not set up / offline: hand the request over on WhatsApp instead.
            var text = 'Hello! Please notify me when ' + p.name + (variantLabel ? ' (' + variantLabel + ')' : '') + ' is back in stock. My contact: ' + contact;
            rsMsg.innerHTML = '<a class="btn btn-outline" href="https://wa.me/966560224715?text=' + encodeURIComponent(text) + '" target="_blank" rel="noopener noreferrer">' + T('js_ask_whatsapp') + '</a>';
            btn.disabled = false;
          });
        });
      }

      paintRatingBadge(container);
      document.addEventListener('b3d:reviews', function () { paintRatingBadge(container); });

      var addBtn = container.querySelector('[data-pd-add]');
      if (addBtn) {
        addBtn.addEventListener('click', function () {
          if (addBtn.disabled) return;
          if (p.bundlePick) {
            if (picked.length < bundleMin) return;
            setBundlePicks(p.id, picked);
          }
          var cartId = hasVariants ? lineId(p.id, selectedVariant) : p.id;
          addToCart(cartId, parseInt(qtyInput.value, 10) || 1);
          if (p.preorder) {
            location.href = '/3d/cart/';
            return;
          }
          var original = addBtn.textContent;
          addBtn.textContent = T('js_added');
          setTimeout(function () { if (!addBtn.disabled) addBtn.textContent = original; }, 1200);
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

  /* Restock alerts: a Saudi mobile (05…, 5…, 9665…, +9665…) becomes 9665XXXXXXXX; emails are kept as typed. */
  function normalizeContact(raw) {
    var v = String(raw || '').trim();
    if (v.indexOf('@') !== -1) return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? v.toLowerCase() : null;
    var d = v.replace(/[^0-9٠-٩]/g, '').replace(/[٠-٩]/g, function (c) { return String(c.charCodeAt(0) - 0x0660); });
    if (/^009665\d{8}$/.test(d)) d = d.slice(2);
    if (/^05\d{8}$/.test(d)) d = '966' + d.slice(1);
    if (/^5\d{8}$/.test(d)) d = '966' + d;
    return /^9665\d{8}$/.test(d) ? d : null;
  }

  function submitRestockAlert(productId, variant, contact) {
    var cfg = window.BLACK_ARROW_SUPABASE_CONFIG;
    if (!cfg || !cfg.url || !cfg.anonKey) return Promise.resolve(false);
    return fetch(cfg.url + '/rest/v1/rpc/submit_restock_alert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', apikey: cfg.anonKey, Authorization: 'Bearer ' + cfg.anonKey },
      body: JSON.stringify({ p_product_id: productId, p_variant: variant, p_contact: contact, p_lang: isAr() ? 'ar' : 'en' })
    }).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { return !!(j && j.ok); })
      .catch(function () { return false; });
  }

  /* Store rating next to the product title, from the approved customer
     reviews that 3d-reviews.js loads (it fires "b3d:reviews" when ready). */
  function paintRatingBadge(container) {
    var el = container.querySelector('[data-pd-rating]');
    var st = window.__b3dReviewStats;
    if (!el || !st || !st.count) return;
    var full = Math.round(st.avg);
    el.innerHTML = '<span class="b3d-pd__stars" aria-hidden="true">' + '★★★★★'.slice(0, full) + '<span>' + '★★★★★'.slice(full) + '</span></span>' +
      '<b>' + st.avg.toFixed(1) + '</b> · ' + st.count + ' ' + T('js_rating_reviews');
    el.setAttribute('aria-label', st.avg.toFixed(1) + ' / 5 — ' + st.count + ' ' + T('js_rating_reviews'));
    el.hidden = false;
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

      html += '<tr><td>' + T('js_cmp_price') + '</td>' + items.map(function (p) { return '<td>' + money(currentPrice(p), p.currency) + '</td>'; }).join('') + '</tr>';
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
    // Running ticker: the messages repeat end to end and the track slides by
    // exactly half its length, so the loop never shows a gap or a jump.
    var msg = T('announce_1');
    if (msg && msg !== 'announce_1') {
      var parts = msg.split(' · ');
      track.textContent = '';
      track.classList.add('b3d-announce__track--run');
      for (var c = 0; c < 12; c++) {
        parts.forEach(function (text) {
          var item = document.createElement('span');
          item.textContent = text;
          track.appendChild(item);
        });
      }
    }
    // The ticker keeps running even when the OS asks for reduced motion; it
    // only stops if the visitor switches the site's own Motion toggle off.
    var tickerOff = false;
    try { tickerOff = localStorage.getItem(MOTION_KEY) === 'off'; } catch (e) {}
    if (tickerOff) { bar.setAttribute('data-paused', 'true'); }
    // The slide is driven from script rather than a CSS animation, so no
    // browser/OS "reduce animations" setting or extension can freeze it.
    if (track.classList.contains('b3d-announce__track--run')) {
      var rtl = document.documentElement.getAttribute('dir') === 'rtl';
      var pos = 0, last = null, speed = 70;
      var step = function (now) {
        if (last === null) last = now;
        var dt = Math.min((now - last) / 1000, 0.1);
        last = now;
        if (bar.getAttribute('data-paused') !== 'true') {
          var half = track.scrollWidth / 2;
          pos += (rtl ? 1 : -1) * speed * dt;
          if (half > 0 && Math.abs(pos) >= half) pos += (rtl ? -half : half);
          track.style.transform = 'translateX(' + pos + 'px)';
        }
        window.requestAnimationFrame(step);
      };
      window.requestAnimationFrame(step);
    }
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

  // Brands with no products (or our own / generic labels) are not listed.
  // A brand with a full landing page links there; a single-product brand goes
  // straight to that product, so the menu never points at a thin filter URL.
  var BRAND_PAGES = { 'Bambu Lab': 'bambu-lab' };
  var BRAND_PAGE_MIN = 3;

  // Logo files for the brand dropdown: [file, width, height]. Brands without a file show the name only.
  var BRAND_LOGOS = {
    'Bambu Lab': ['bambu-lab.svg', 62, 18],
    'Creality': ['creality.svg', 400, 92],
    'Elegoo': ['elegoo.webp', 372, 70],
    'Anycubic': ['anycubic.png', 187, 48],
    'Snapmaker': ['snapmaker.svg', 125, 24],
    'Flashforge': ['flashforge.png', 600, 120],
    'KINGROON': ['kingroon.png', 530, 120]
  };

  function initMobileNav() {
    var toggle = document.querySelector('[data-b3d-nav-toggle]');
    var links = document.getElementById('b3d-navbar-links');
    if (!toggle || !links) return;

    function close() {
      links.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
    function open() {
      links.classList.add('is-open');
      toggle.setAttribute('aria-expanded', 'true');
    }

    toggle.addEventListener('click', function () {
      if (links.classList.contains('is-open')) close(); else open();
    });

    document.addEventListener('click', function (e) {
      if (!links.classList.contains('is-open')) return;
      if (links.contains(e.target) || toggle.contains(e.target)) return;
      close();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });

    // A real navigation (not the Brands <details> toggle) closes the panel
    // the same way clicking outside it would.
    links.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]');
      if (a) close();
    });
  }

  // Below 560px the AR/EN pill shrinks to an icon-only control (CSS) so it
  // can stay in the header instead of being tucked inside the hamburger
  // panel — mark it so CSS can target it without relying on an attribute
  // that generated Arabic pages' plain-link version doesn't carry.
  function markLangPill() {
    var right = document.querySelector('.navbar__right');
    if (!right) return;
    var langPill = right.querySelector('.navbar__pill:not([aria-label])');
    if (langPill) langPill.classList.add('navbar__pill--lang');
  }

  function initBrandNavMenu() {
    var menu = document.querySelector('[data-b3d-brand-menu]');
    if (!menu) return;
    var base = isArPage() ? '/3d/ar' : '/3d';
    fetchProducts().then(function (products) {
      var html = menu.innerHTML;
      brandList().forEach(function (brand) {
        if (brand === 'Black Arrow' || brand === 'Generic') return;
        // Every brand we sell is listed, in stock or not (the shop shows out-of-stock items too).
        var items = products.filter(function (p) { return p.brand === brand; });
        if (!items.length) return;
        var href;
        if (BRAND_PAGES[brand] && items.length >= BRAND_PAGE_MIN) href = base + '/brands/' + BRAND_PAGES[brand] + '/';
        else if (items.length === 1) href = productUrl(items[0]);
        else href = base + '/shop/?brand=' + encodeURIComponent(brand);
        var logo = BRAND_LOGOS[brand];
        html += '<a href="' + href + '">' + '<span>' + brand + '</span>' +
          (logo ? '<img class="navbar__brand-logo" src="/3d/assets/images/brands/' + logo[0] + '" alt="" width="' + logo[1] + '" height="' + logo[2] + '" loading="lazy">' : '') + '</a>';
      });
      menu.innerHTML = html;
    });
  }

  function autoInit() {
    updateCartBadges();
    initMotionToggle();
    initAnnouncementBar();
    populateHeroSlider().then(initPromoSlider);
    initBrandNavMenu();
    initMobileNav();
    markLangPill();

    var livePrices = document.querySelectorAll('[data-b3d-price]');
    if (livePrices.length) fetchProducts().then(function () { paintLivePrices(livePrices); });

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

    var printersGrid = document.querySelector('[data-b3d-printers-grid]');
    if (printersGrid) {
      fetchProducts().then(function (products) {
        var printers = products.filter(function (p) { return p.category === '3D Printers' && p.available !== false; }).slice(0, 8);
        renderGrid(printers, printersGrid);
      });
    }

    var giftsGrid = document.querySelector('[data-b3d-gifts-grid]');
    if (giftsGrid) {
      fetchProducts().then(function (products) {
        var gifts = products.filter(function (p) {
          return p.category === '3D Artwork' && p.available !== false && currentPrice(p) <= 50;
        }).slice(0, 8);
        renderGrid(gifts, giftsGrid);
      });
    }

    // Category and brand landing pages (/3d/shop/<category>/, /3d/brands/<brand>/): swap the
    // plain crawlable links for the real interactive card, so Add to Cart works without
    // opening the product page — the links above stay in the initial HTML for SEO and no-JS.
    document.querySelectorAll('[data-b3d-cat-grid]').forEach(function (grid) {
      var cat = grid.getAttribute('data-b3d-cat-grid');
      fetchProducts().then(function (products) {
        renderGridWithSeries(products.filter(function (p) { return p.category === cat; }), grid);
      });
    });
    document.querySelectorAll('[data-b3d-ids]').forEach(function (grid) {
      var ids = grid.getAttribute('data-b3d-ids').split(',');
      fetchProducts().then(function (products) {
        renderGrid(ids.map(function (id) {
          return products.filter(function (p) { return p.id === id; })[0];
        }).filter(Boolean), grid);
      });
    });
    document.querySelectorAll('[data-b3d-brand-grid]').forEach(function (grid) {
      var brand = grid.getAttribute('data-b3d-brand-grid');
      fetchProducts().then(function (products) {
        renderGridWithSeries(products.filter(function (p) { return p.brand === brand; }), grid);
      });
    });

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
      showCardReturn();
      showTabbyReturn();
      resumePendingOrder();
    }
  }

  document.addEventListener('DOMContentLoaded', autoInit);
})();
