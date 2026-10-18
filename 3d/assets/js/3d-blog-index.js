/* Black Arrow 3D blog index: groups the article cards into topics with filter
   buttons. The cards themselves are written into the page by the generator
   scripts as one flat grid; this only regroups them in the browser, so a
   generator run never undoes it. A card whose slug isn't listed here goes to
   "More guides". Without JavaScript the page shows the flat grid as before. */
(function () {
  'use strict';

  var CATEGORIES = [
    { id: 'buying', en: 'Buying Guides', ar: 'أدلة الشراء', slugs: [
      'best-3d-printer-for-beginners-saudi-arabia', 'best-3d-printer-for-kids-schools-saudi-arabia',
      '3d-printer-buying-checklist-saudi-arabia', 'where-to-buy-3d-printer-saudi-arabia',
      'buy-3d-printer-saudi-arabia-price-guide', 'bambu-lab-printers-saudi-arabia-prices',
      '3d-printer-installments-tabby-tamara-saudi'] },
    { id: 'reviews', en: 'Reviews & Comparisons', ar: 'مراجعات ومقارنات', slugs: [
      'bambu-lab-a1-mini-combo-review', 'snapmaker-u1-multicolor-3d-printer-review',
      'bambu-lab-a1-vs-a1-mini-vs-a2l', 'bambu-lab-vs-creality-vs-snapmaker', 'multi-color-3d-printing-explained'] },
    { id: 'filament', en: 'Filament & Materials', ar: 'الفلمنت والمواد', slugs: [
      'pla-vs-petg-vs-abs-filament-guide', 'which-filament-for-which-print', '3d-printing-filament-saudi-heat-humidity'] },
    { id: 'fixes', en: 'Setup, Maintenance & Fixes', ar: 'التشغيل والصيانة وحل المشاكل', slugs: [
      'bambu-lab-a1-mini-setup-guide', '3d-printer-maintenance-guide', 'clogged-3d-printer-nozzle-fix',
      '3d-print-stringing-fix', '3d-print-bed-adhesion-first-layer'] },
    { id: 'gifts', en: 'Gifts, Custom Printing & Business', ar: 'الهدايا والطباعة حسب الطلب والأعمال', slugs: [
      '3d-printed-gifts-saudi-occasions', '3d-printed-gifts-home-decor-saudi-arabia', 'custom-3d-printing-cost-saudi-arabia',
      'start-3d-printing-business-saudi-arabia', '3d-printing-students-engineers-saudi-arabia'] },
    { id: 'cities', en: 'Buy by City', ar: 'الشراء حسب المدينة', prefix: 'buy-3d-printer-' }
  ];
  var MORE = { id: 'more', en: 'More guides', ar: 'أدلة أخرى' };

  function init() {
    var grid = document.querySelector('main .b3d-blog-grid') || document.querySelector('.b3d-blog-grid');
    if (!grid) return;
    var ar = document.documentElement.lang === 'ar';
    var label = function (c) { return ar ? c.ar : c.en; };
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.b3d-blog-card'));
    if (!cards.length) return;

    var groups = {};
    cards.forEach(function (card) {
      var a = card.querySelector('a[href]');
      var m = a && /\/blog\/([^/]+)\/?$/.exec(a.getAttribute('href'));
      var slug = m ? m[1] : '';
      var cat = null;
      CATEGORIES.forEach(function (c) {
        if (cat) return;
        if (c.slugs && c.slugs.indexOf(slug) !== -1) cat = c;
        else if (c.prefix && slug.indexOf(c.prefix) === 0 && slug !== 'buy-3d-printer-saudi-arabia-price-guide') cat = c;
      });
      cat = cat || MORE;
      (groups[cat.id] = groups[cat.id] || { cat: cat, cards: [] }).cards.push(card);
    });
    var order = CATEGORIES.concat([MORE]).filter(function (c) { return groups[c.id]; });

    var wrap = document.createElement('div');
    wrap.className = 'b3d-blog-topics';

    var nav = document.createElement('div');
    nav.className = 'b3d-blog-filter';
    nav.setAttribute('role', 'group');
    nav.setAttribute('aria-label', ar ? 'تصفية المقالات حسب الموضوع' : 'Filter articles by topic');
    var buttons = [];
    function addButton(id, text, count) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'b3d-blog-filter__btn';
      b.setAttribute('data-topic', id);
      b.innerHTML = '<span></span><span class="b3d-blog-filter__count"></span>';
      b.firstChild.textContent = text;
      b.lastChild.textContent = count;
      nav.appendChild(b);
      buttons.push(b);
    }
    addButton('all', ar ? 'الكل' : 'All', cards.length);
    order.forEach(function (c) { addButton(c.id, label(c), groups[c.id].cards.length); });
    wrap.appendChild(nav);

    var sections = order.map(function (c) {
      var s = document.createElement('section');
      s.className = 'b3d-blog-topic';
      s.id = 'topic-' + c.id;
      s.setAttribute('data-topic', c.id);
      var h = document.createElement('h2');
      h.className = 'b3d-blog-topic__title';
      h.textContent = label(c);
      var g = document.createElement('div');
      g.className = 'b3d-blog-grid';
      groups[c.id].cards.forEach(function (card) {
        // Article titles sit under the topic heading now.
        var t = card.querySelector('h2.b3d-blog-card__title');
        if (t) { var h3 = document.createElement('h3'); h3.className = t.className; h3.innerHTML = t.innerHTML; t.parentNode.replaceChild(h3, t); }
        g.appendChild(card);
      });
      s.appendChild(h);
      s.appendChild(g);
      wrap.appendChild(s);
      return s;
    });

    function show(id) {
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-topic') === id)); });
      sections.forEach(function (s) { s.hidden = id !== 'all' && s.getAttribute('data-topic') !== id; });
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var id = b.getAttribute('data-topic');
        show(id);
        try { history.replaceState(null, '', id === 'all' ? location.pathname : '#' + id); } catch (e) {}
      });
    });

    grid.parentNode.replaceChild(wrap, grid);
    var start = (location.hash || '').replace('#', '');
    show(groups[start] ? start : 'all');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
