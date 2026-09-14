/* Black Arrow 3D — product catalog + client-side cart.
   No backend yet: catalog comes from a static JSON file, cart lives in
   localStorage. Checkout is a placeholder until a payment gateway
   (Moyasar/Tap) is wired in. */
(function () {
  'use strict';

  var CART_KEY = 'b3d_cart_v1';
  var DATA_URL = '/assets/data/3d-products.json';

  var ICONS = {
    'printer': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="14" y="8" width="36" height="16" rx="2"/><rect x="10" y="24" width="44" height="20" rx="2"/><rect x="20" y="44" width="24" height="12" rx="1.5"/><line x1="32" y1="30" x2="32" y2="40"/><circle cx="18" cy="18" r="2" fill="currentColor" stroke="none"/></svg>',
    'printer-large': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="10" width="48" height="34" rx="2"/><line x1="32" y1="16" x2="32" y2="38"/><line x1="14" y1="27" x2="50" y2="27"/><rect x="18" y="44" width="28" height="12" rx="1.5"/><circle cx="16" cy="16" r="2" fill="currentColor" stroke="none"/><circle cx="48" cy="16" r="2" fill="currentColor" stroke="none"/></svg>',
    'printer-industrial': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="12" width="52" height="30" rx="2"/><rect x="6" y="12" width="52" height="8" rx="2" fill="currentColor" fill-opacity=".18"/><line x1="32" y1="24" x2="32" y2="38"/><line x1="20" y1="24" x2="20" y2="38"/><line x1="44" y1="24" x2="44" y2="38"/><rect x="14" y="42" width="36" height="14" rx="1.5"/><circle cx="20" cy="49" r="2.4" fill="currentColor" stroke="none"/><circle cx="44" cy="49" r="2.4" fill="currentColor" stroke="none"/></svg>',
    'resin': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 8h20v10l8 8v26a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4V26l8-8V8z"/><line x1="22" y1="8" x2="42" y2="8"/><line x1="16" y1="36" x2="48" y2="36"/><path d="M24 46l6 6 10-12" opacity=".6"/></svg>',
    'spool': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="32" r="24"/><circle cx="32" cy="32" r="9"/><path d="M12 20c8 6 32 6 40 0" opacity=".5"/><path d="M12 44c8-6 32-6 40 0" opacity=".5"/></svg>',
    'bottle': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M26 6h12v10l6 8v28a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4V24l6-8V6z"/><line x1="26" y1="6" x2="38" y2="6"/><rect x="21" y="34" width="22" height="16" opacity=".6"/></svg>'
  };

  var CART_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>';

  function icon(name) {
    return ICONS[name] || ICONS.printer;
  }

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

  function fetchProducts() {
    return fetch(DATA_URL).then(function (r) { return r.json(); }).then(function (data) {
      return data.products;
    });
  }

  function money(n, currency) {
    return n.toLocaleString('en-US') + ' <small>' + currency + '</small>';
  }

  function stockBadge(stock) {
    if (stock <= 0) return '<span class="b3d-stock-badge b3d-stock-badge--out">Out of Stock</span>';
    if (stock <= 3) return '<span class="b3d-stock-badge b3d-stock-badge--low">Only ' + stock + ' left</span>';
    return '<span class="b3d-stock-badge b3d-stock-badge--in">In Stock</span>';
  }

  function productCard(p) {
    var disabled = p.stock <= 0 ? 'disabled' : '';
    var btnLabel = p.stock <= 0 ? 'Out of Stock' : 'Add to Cart';
    return '' +
      '<article class="b3d-card" data-cat="' + p.category + '">' +
        '<a href="/3d/product/?slug=' + p.id + '" class="b3d-card__visual" aria-label="' + p.name + '">' +
          (p.sample ? '<span class="b3d-sample-badge">Sample</span>' : '') +
          stockBadge(p.stock) +
          icon(p.icon) +
        '</a>' +
        '<div class="b3d-card__body">' +
          '<div class="b3d-card__cat">' + p.category + '</div>' +
          '<h3><a href="/3d/product/?slug=' + p.id + '">' + p.name + '</a></h3>' +
          '<p>' + p.shortDesc + '</p>' +
        '</div>' +
        '<div class="b3d-card__footer">' +
          '<span class="b3d-price">' + money(p.price, p.currency) + '</span>' +
          '<button class="b3d-btn-add" data-add-id="' + p.id + '" ' + disabled + '>' + btnLabel + '</button>' +
        '</div>' +
      '</article>';
  }

  function renderGrid(products, container) {
    container.innerHTML = products.map(productCard).join('');
    container.querySelectorAll('[data-add-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        addToCart(btn.getAttribute('data-add-id'), 1);
        var original = btn.textContent;
        btn.textContent = 'Added ✓';
        setTimeout(function () { btn.textContent = original; }, 1200);
      });
    });
  }

  function renderFilters(products, pillContainer, grid) {
    var cats = ['All'].concat(Array.from(new Set(products.map(function (p) { return p.category; }))));
    pillContainer.innerHTML = cats.map(function (c, i) {
      return '<button class="b3d-filter-pill" data-cat="' + c + '" aria-pressed="' + (i === 0) + '">' + c + '</button>';
    }).join('');
    pillContainer.querySelectorAll('.b3d-filter-pill').forEach(function (pill) {
      pill.addEventListener('click', function () {
        pillContainer.querySelectorAll('.b3d-filter-pill').forEach(function (p) { p.setAttribute('aria-pressed', 'false'); });
        pill.setAttribute('aria-pressed', 'true');
        var cat = pill.getAttribute('data-cat');
        var filtered = cat === 'All' ? products : products.filter(function (p) { return p.category === cat; });
        renderGrid(filtered, grid);
        document.querySelectorAll('[data-b3d-count]').forEach(function (el) { el.textContent = filtered.length; });
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
      listEl.innerHTML = ids.map(function (id) {
        var p = byId[id];
        if (!p) return '';
        var qty = cart[id];
        var lineTotal = p.price * qty;
        subtotal += lineTotal;
        return '' +
          '<div class="b3d-cart-item" data-line-id="' + id + '">' +
            '<div class="b3d-cart-item__visual">' + icon(p.icon) + '</div>' +
            '<div>' +
              '<div class="b3d-cart-item__name">' + p.name + '</div>' +
              '<div class="b3d-cart-item__cat">' + p.category + '</div>' +
              '<button class="b3d-cart-item__remove" data-remove-id="' + id + '">Remove</button>' +
            '</div>' +
            '<div class="b3d-qty">' +
              '<button data-qty-btn="minus" data-id="' + id + '">−</button>' +
              '<input type="text" readonly value="' + qty + '" data-qty-val="' + id + '">' +
              '<button data-qty-btn="plus" data-id="' + id + '">+</button>' +
            '</div>' +
            '<div class="b3d-cart-item__price">' + money(lineTotal, p.currency) + '</div>' +
          '</div>';
      }).join('');

      summaryEl.querySelector('[data-cart-subtotal]').innerHTML = money(subtotal, 'SAR');
      summaryEl.querySelector('[data-cart-total]').innerHTML = money(subtotal, 'SAR');

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

  function renderProductDetail(container) {
    var slug = new URLSearchParams(location.search).get('slug');
    fetchProducts().then(function (products) {
      var p = products.filter(function (x) { return x.id === slug; })[0];
      if (!p) {
        container.innerHTML = '<div class="b3d-empty"><h2>Product not found</h2><p>That product doesn’t exist in the catalog. <a href="/3d/shop/" style="color:var(--clr-accent);">Back to shop</a></p></div>';
        return;
      }
      document.title = p.name + ' — Black Arrow 3D';
      var specsHtml = p.specs.map(function (row) {
        return '<tr><td>' + row[0] + '</td><td>' + row[1] + '</td></tr>';
      }).join('');
      container.innerHTML = '' +
        '<div class="b3d-pd__visual">' +
          (p.sample ? '<span class="b3d-sample-badge">Sample Product</span>' : '') +
          icon(p.icon) +
        '</div>' +
        '<div>' +
          '<div class="b3d-pd__cat">' + p.category + '</div>' +
          '<h1 class="b3d-pd__title">' + p.name + '</h1>' +
          '<div class="b3d-pd__price">' + money(p.price, p.currency) + '</div>' +
          '<div style="margin-bottom:16px;">' + stockBadge(p.stock) + '</div>' +
          '<p class="b3d-pd__desc">' + p.description + '</p>' +
          '<div class="b3d-pd__actions">' +
            '<div class="b3d-qty">' +
              '<button type="button" data-pd-qty="minus">−</button>' +
              '<input type="text" readonly value="1" data-pd-qty-val>' +
              '<button type="button" data-pd-qty="plus">+</button>' +
            '</div>' +
            '<button class="btn btn-primary" data-pd-add ' + (p.stock <= 0 ? 'disabled' : '') + '>' + (p.stock <= 0 ? 'Out of Stock' : 'Add to Cart') + '</button>' +
            '<a href="/3d/cart/" class="btn btn-outline">View Cart</a>' +
          '</div>' +
          '<table class="b3d-spec-table"><tbody>' + specsHtml + '</tbody></table>' +
        '</div>';

      var qtyInput = container.querySelector('[data-pd-qty-val]');
      container.querySelectorAll('[data-pd-qty]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var current = parseInt(qtyInput.value, 10) || 1;
          var next = btn.getAttribute('data-pd-qty') === 'plus' ? current + 1 : Math.max(1, current - 1);
          qtyInput.value = next;
        });
      });
      var addBtn = container.querySelector('[data-pd-add]');
      if (addBtn) {
        addBtn.addEventListener('click', function () {
          addToCart(p.id, parseInt(qtyInput.value, 10) || 1);
          var original = addBtn.textContent;
          addBtn.textContent = 'Added ✓';
          setTimeout(function () { addBtn.textContent = original; }, 1200);
        });
      }
    });
  }

  window.BlackArrow3D = {
    fetchProducts: fetchProducts,
    renderGrid: renderGrid,
    renderFilters: renderFilters,
    renderCartPage: renderCartPage,
    renderProductDetail: renderProductDetail,
    getCart: getCart,
    cartCount: cartCount,
    updateCartBadges: updateCartBadges,
    icon: icon,
    CART_SVG: CART_SVG
  };

  document.addEventListener('DOMContentLoaded', function () { updateCartBadges(); });
})();
