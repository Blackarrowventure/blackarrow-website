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
    'accessory': '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="14" y="14" width="36" height="36" rx="6"/><path d="M24 32h16M32 24v16" /></svg>'
  };

  var CART_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>';

  function iconFor(category) {
    if (category === 'Filament') return ICONS.spool;
    if (category === 'Accessories') return ICONS.accessory;
    return ICONS.printer;
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
      btn.textContent = enabled ? 'Motion: On' : 'Motion: Off';
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
    return n.toLocaleString('en-US') + ' <small>' + (currency || 'SAR') + '</small>';
  }

  function primaryImage(p) {
    if (p.images && p.images.length) return p.images[0];
    if (p.image) return p.image;
    return null;
  }

  function visual(p) {
    var img = primaryImage(p);
    if (img) return '<img src="' + img + '" alt="' + p.name + '" loading="lazy">';
    return iconFor(p.category);
  }

  function statusBadge(p) {
    if (p.preorder) return '<span class="b3d-stock-badge b3d-stock-badge--pre">Pre-Order</span>';
    if (p.available === false) return '<span class="b3d-stock-badge b3d-stock-badge--out">Out of Stock</span>';
    return '';
  }

  function priceBlock(p) {
    if (p.onSale && p.salePrice != null) {
      return '<span class="b3d-price b3d-price--sale">' + money(p.salePrice, p.currency) +
        '</span><span class="b3d-price-was">' + money(p.price, p.currency) + '</span>';
    }
    return '<span class="b3d-price">' + money(p.price, p.currency) + '</span>';
  }

  function cornerBadges(p) {
    var out = '';
    if (p.featured) out += '<span class="b3d-corner-badge b3d-corner-badge--featured">Featured</span>';
    if (p.onSale) out += '<span class="b3d-corner-badge b3d-corner-badge--sale">Sale</span>';
    return out;
  }

  function productCard(p) {
    var disabled = (p.available === false && !p.preorder) ? 'disabled' : '';
    var btnLabel = p.preorder ? 'Pre-Order' : (p.available === false ? 'Out of Stock' : 'Add to Cart');
    var specs = (p.specs || []).slice(0, 3).map(function (row) {
      return '<li><span>' + row[0] + '</span><span>' + row[1] + '</span></li>';
    }).join('');
    return '' +
      '<article class="b3d-card" data-cat="' + p.category + '" data-brand="' + (p.brand || '') + '">' +
        '<a href="/3d/product/?slug=' + p.id + '" class="b3d-card__visual" aria-label="' + p.name + '">' +
          cornerBadges(p) +
          statusBadge(p) +
          visual(p) +
        '</a>' +
        '<div class="b3d-card__body">' +
          '<div class="b3d-card__cat">' + (p.brand ? p.brand + ' &middot; ' : '') + p.category + '</div>' +
          '<h3><a href="/3d/product/?slug=' + p.id + '">' + p.name + '</a></h3>' +
          '<p>' + (p.shortDesc || '') + '</p>' +
          (specs ? '<ul class="b3d-card__specs">' + specs + '</ul>' : '') +
        '</div>' +
        '<div class="b3d-card__footer">' +
          '<div class="b3d-price-wrap">' + priceBlock(p) + '</div>' +
          '<div class="b3d-card__actions">' +
            '<button class="b3d-btn-compare" data-compare-id="' + p.id + '" aria-label="Add to compare" title="Compare">⇄</button>' +
            '<button class="b3d-btn-wishlist" data-wishlist-id="' + p.id + '" aria-label="Save to wishlist" title="Save">♡</button>' +
            '<button class="b3d-btn-add" data-add-id="' + p.id + '" ' + disabled + '>' + btnLabel + '</button>' +
          '</div>' +
        '</div>' +
      '</article>';
  }

  function emptyCatalogHtml(reason) {
    return '<div class="b3d-empty" style="grid-column:1/-1;">' +
      '<h2 style="color:#fff;margin-bottom:10px;">' + (reason || 'No products published yet') + '</h2>' +
      '<p>Check back soon, or contact us for current availability.</p>' +
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
        btn.textContent = 'Added ✓';
        setTimeout(function () { btn.textContent = original; }, 1200);
      });
    });
    container.querySelectorAll('[data-wishlist-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        btn.classList.toggle('is-active');
        btn.textContent = btn.classList.contains('is-active') ? '♥' : '♡';
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
      priceMin: null,
      priceMax: null,
      page: 1
    };

    var params = new URLSearchParams(location.search);
    if (params.get('cat')) state.cat = params.get('cat');
    if (params.get('brand')) state.brand = params.get('brand');
    if (params.get('q')) state.q = params.get('q');

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

    if (els.categoryTabs) {
      els.categoryTabs.querySelectorAll('[data-cat]').forEach(function (tab) {
        if (tab.getAttribute('data-cat') === state.cat) tab.setAttribute('aria-pressed', 'true');
        tab.addEventListener('click', function () {
          els.categoryTabs.querySelectorAll('[data-cat]').forEach(function (t) { t.setAttribute('aria-pressed', 'false'); });
          tab.setAttribute('aria-pressed', 'true');
          state.cat = tab.getAttribute('data-cat');
          state.page = 1;
          apply();
        });
      });
    }

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
        state.page = 1;
        apply();
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
        var unit = (p.onSale && p.salePrice != null) ? p.salePrice : p.price;
        var lineTotal = unit * qty;
        subtotal += lineTotal;
        return '' +
          '<div class="b3d-cart-item" data-line-id="' + id + '">' +
            '<div class="b3d-cart-item__visual">' + visual(p) + '</div>' +
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
      });
    });
  }

  /* ---------------- Product detail ---------------- */

  function renderProductDetail(container) {
    var slug = new URLSearchParams(location.search).get('slug');
    fetchProducts().then(function (products) {
      var p = products.filter(function (x) { return x.id === slug; })[0];
      if (!p) {
        container.innerHTML = '<div class="b3d-empty"><h2 style="color:#fff;">Product not found</h2><p>That product isn’t in the catalog yet. <a href="/3d/shop/" style="color:var(--clr-accent);">Back to shop</a></p></div>';
        return;
      }
      document.title = p.name + ' — Black Arrow 3D';
      var specsHtml = (p.specs || []).map(function (row) {
        return '<tr><td>' + row[0] + '</td><td>' + row[1] + '</td></tr>';
      }).join('');
      var compatHtml = (p.compatibility && p.compatibility.length)
        ? '<div class="b3d-pd__compat"><h3>Compatibility</h3><ul>' + p.compatibility.map(function (c) { return '<li>' + c + '</li>'; }).join('') + '</ul></div>'
        : '';
      var images = (p.images && p.images.length) ? p.images : (p.image ? [p.image] : []);
      var thumbsHtml = images.length > 1
        ? '<div class="b3d-pd__thumbs">' + images.map(function (src, i) {
            return '<button class="b3d-pd__thumb' + (i === 0 ? ' is-active' : '') + '" data-thumb-src="' + src + '"><img src="' + src + '" alt=""></button>';
          }).join('') + '</div>'
        : '';
      var pdAvailable = p.available !== false;
      var mainVisual = images.length ? '<img src="' + images[0] + '" alt="' + p.name + '" data-pd-main-img>' : iconFor(p.category);

      container.innerHTML = '' +
        '<div>' +
          '<div class="b3d-pd__visual" data-pd-zoom>' +
            cornerBadges(p) +
            mainVisual +
          '</div>' +
          thumbsHtml +
        '</div>' +
        '<div>' +
          '<div class="b3d-pd__cat">' + (p.brand ? p.brand + ' &middot; ' : '') + p.category + '</div>' +
          '<h1 class="b3d-pd__title">' + p.name + '</h1>' +
          '<div class="b3d-pd__price">' + priceBlock(p) + '</div>' +
          (statusBadge(p) ? '<div style="margin-bottom:16px;">' + statusBadge(p) + '</div>' : '') +
          '<p class="b3d-pd__desc">' + (p.description || '') + '</p>' +
          '<div class="b3d-pd__actions">' +
            '<div class="b3d-qty">' +
              '<button type="button" data-pd-qty="minus">−</button>' +
              '<input type="text" readonly value="1" data-pd-qty-val>' +
              '<button type="button" data-pd-qty="plus">+</button>' +
            '</div>' +
            '<button class="btn btn-primary" data-pd-add ' + ((pdAvailable || p.preorder) ? '' : 'disabled') + '>' + (p.preorder ? 'Pre-Order' : (pdAvailable ? 'Add to Cart' : 'Out of Stock')) + '</button>' +
            '<button class="btn btn-outline" data-pd-compare="' + p.id + '">Compare</button>' +
            '<a href="/3d/cart/" class="btn btn-outline">View Cart</a>' +
          '</div>' +
          (specsHtml ? '<table class="b3d-spec-table"><tbody>' + specsHtml + '</tbody></table>' : '') +
          compatHtml +
          (p.warranty ? '<div class="b3d-pd__warranty"><h3>Warranty</h3><p>' + p.warranty + '</p></div>' : '') +
          '<div class="b3d-pd__shipreturn">' +
            '<div><strong>Shipping</strong><p>Calculated at checkout, across Saudi Arabia.</p></div>' +
            '<div><strong>Returns</strong><p>See our <a href="/terms-of-service.html">Terms of Service</a> for the return policy.</p></div>' +
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
      var compareBtn = container.querySelector('[data-pd-compare]');
      if (compareBtn) {
        compareBtn.addEventListener('click', function () {
          toggleCompare(p.id);
          compareBtn.textContent = getCompareList().indexOf(p.id) !== -1 ? 'Added to Compare' : 'Compare';
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
    host.innerHTML = '<h2 class="b3d-related__title">Related Products</h2><div class="b3d-grid">' +
      related.map(productCard).join('') + '</div>';
    host.querySelectorAll('[data-add-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        addToCart(btn.getAttribute('data-add-id'), 1);
        btn.textContent = 'Added ✓';
      });
    });
  }

  /* ---------------- Compare page ---------------- */

  function renderComparePage(container) {
    fetchProducts().then(function (products) {
      var ids = getCompareList();
      var items = ids.map(function (id) { return products.filter(function (p) { return p.id === id; })[0]; }).filter(Boolean);
      if (items.length < 2) {
        container.innerHTML = '<div class="b3d-empty"><h2 style="color:#fff;">Nothing to compare yet</h2>' +
          '<p>Add at least two published products to your comparison list from the shop — none published yet.</p>' +
          '<a href="/3d/shop/" class="btn btn-primary">Go to Shop</a></div>';
        return;
      }
      var rows = ['Price', 'Print quality', 'Printing speed', 'Build volume', 'Material capability', 'Ease of use', 'Experience level', 'Warranty & support', 'Best use case', 'Accessories & compatibility'];
      var specLookup = function (p, label) {
        var row = (p.specs || []).filter(function (r) { return r[0].toLowerCase() === label.toLowerCase(); })[0];
        return row ? row[1] : '—';
      };
      var html = '<table class="b3d-compare-table"><thead><tr><th></th>' +
        items.map(function (p) { return '<th>' + p.name + '</th>'; }).join('') + '</tr></thead><tbody>';
      html += '<tr><td>Price</td>' + items.map(function (p) { return '<td>' + money(p.price, p.currency) + '</td>'; }).join('') + '</tr>';
      rows.slice(1).forEach(function (label) {
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

    function resetTimer() {
      if (timer) clearInterval(timer);
      if (motionEnabled()) timer = setInterval(function () { go(index + 1); }, 6000);
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
    motionEnabled: motionEnabled,
    CART_SVG: CART_SVG
  };

  function autoInit() {
    updateCartBadges();
    initMotionToggle();
    initAnnouncementBar();
    initPromoSlider();

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
          pagination: document.querySelector('[data-b3d-pagination]')
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
      renderCartPage(cartList, summary, empty);
      initPaymentMethods(document.querySelector('[data-b3d-payment]'));
    }
  }

  document.addEventListener('DOMContentLoaded', autoInit);
})();
