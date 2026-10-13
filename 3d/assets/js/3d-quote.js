/* Black Arrow 3D — instant 3D printing quote (/3d/quote/).
   The customer picks an STL file; everything happens in the browser: the
   file is read, its size, volume and surface area are measured, a preview
   is drawn, and an estimated price is shown. Nothing is uploaded — the
   "Send on WhatsApp" button opens a chat with the details pre-filled and
   the customer attaches the file there. */
(function () {
  'use strict';

  /* ---- Pricing — edit these numbers to change every estimate ------------ */
  var PRICING = {
    setupFee: 15,            // SAR per order line (slicing, prep, plate removal)
    perGram: { PLA: 0.5, PETG: 0.6, TPU: 0.9 },   // SAR per gram of filament
    minPrice: 15,            // SAR, minimum per piece
    range: 0.2               // show the estimate as ±20%
  };
  var DENSITY = { PLA: 1.24, PETG: 1.27, TPU: 1.21 };   // g/cm³
  var WALL_CM = 0.12;        // ~1.2 mm of solid walls / top / bottom
  var MAX_BUILD_MM = 320;    // largest printer bed we run
  var MAX_FILE_MB = 60;
  var WHATSAPP = '966560224715';

  var lang = (document.documentElement.lang || 'en').slice(0, 2) === 'ar' ? 'ar' : 'en';
  var STR = {
    en: {
      drop: 'Drop your STL file here or tap to choose',
      dropHint: 'STL files up to ' + MAX_FILE_MB + ' MB. Your file stays on your device.',
      reading: 'Reading your file…',
      bad: 'We could not read this file. Please choose a valid .stl file.',
      tooBig: 'This file is larger than ' + MAX_FILE_MB + ' MB. Please send it to us on WhatsApp instead.',
      size: 'Size', volume: 'Volume', weight: 'Est. filament', triangles: 'Triangles',
      material: 'Material', color: 'Color', infill: 'Infill', qty: 'Quantity', scale: 'Scale',
      infillOpts: [['15', 'Light (15%) — decor'], ['25', 'Standard (25%)'], ['50', 'Strong (50%)'], ['100', 'Solid (100%)']],
      colors: ['Black', 'White', 'Gray', 'Red', 'Yellow', 'Orange', 'Blue', 'Green', 'Other — tell us in the chat'],
      materials: [['PLA', 'PLA+ — everyday, best detail'], ['PETG', 'PETG — tougher, heat resistant'], ['TPU', 'TPU — flexible, rubber-like']],
      estimate: 'Estimated price',
      perPiece: 'per piece', total: 'Total for', pieces: 'pieces',
      note: 'This is an instant estimate. We confirm the final price on WhatsApp after checking your file — usually within the hour during working hours.',
      tooLarge: 'This model is larger than our build plate (' + MAX_BUILD_MM + ' mm). We can scale it down or print it in parts — ask us in the chat.',
      send: 'Send on WhatsApp for a confirmed quote',
      attach: 'Please attach the STL file in the chat.',
      another: 'Choose another file',
      file: 'File', sar: 'SAR', mm: 'mm', cm3: 'cm³', g: 'g',
      msgIntro: 'Hello! I would like a 3D printing quote:'
    },
    ar: {
      drop: 'اسحب ملف STL هنا أو اضغط لاختياره',
      dropHint: 'ملفات STL حتى ' + MAX_FILE_MB + ' ميجابايت. ملفك يبقى على جهازك.',
      reading: 'جارٍ قراءة الملف…',
      bad: 'لم نتمكن من قراءة هذا الملف. اختر ملف ‎.stl صالحًا.',
      tooBig: 'هذا الملف أكبر من ' + MAX_FILE_MB + ' ميجابايت. أرسله لنا عبر واتساب بدلًا من ذلك.',
      size: 'المقاس', volume: 'الحجم', weight: 'الفلمنت التقديري', triangles: 'المثلثات',
      material: 'الخامة', color: 'اللون', infill: 'نسبة الحشو', qty: 'الكمية', scale: 'التكبير',
      infillOpts: [['15', 'خفيف (15%) — ديكور'], ['25', 'عادي (25%)'], ['50', 'قوي (50%)'], ['100', 'مصمت (100%)']],
      colors: ['أسود', 'أبيض', 'رمادي', 'أحمر', 'أصفر', 'برتقالي', 'أزرق', 'أخضر', 'لون آخر — أخبرنا في المحادثة'],
      materials: [['PLA', 'PLA+ — للاستخدام اليومي وأفضل تفاصيل'], ['PETG', 'PETG — أقوى ويتحمل الحرارة'], ['TPU', 'TPU — مرن مثل المطاط']],
      estimate: 'السعر التقديري',
      perPiece: 'للقطعة', total: 'الإجمالي لـ', pieces: 'قطع',
      note: 'هذا سعر تقديري فوري. نؤكد السعر النهائي عبر واتساب بعد مراجعة ملفك — غالبًا خلال ساعة في أوقات العمل.',
      tooLarge: 'هذا المجسم أكبر من سطح الطباعة لدينا (' + MAX_BUILD_MM + ' مم). يمكننا تصغيره أو طباعته على أجزاء — اسألنا في المحادثة.',
      send: 'أرسل عبر واتساب لتأكيد السعر',
      attach: 'من فضلك أرفق ملف STL في المحادثة.',
      another: 'اختر ملفًا آخر',
      file: 'الملف', sar: 'ريال', mm: 'مم', cm3: 'سم³', g: 'جم',
      msgIntro: 'مرحبًا! أريد عرض سعر لطباعة ثلاثية الأبعاد:'
    }
  };
  var S = STR[lang];

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function fmt(n, d) { return Number(n).toLocaleString(lang === 'ar' ? 'ar-SA' : 'en-US', { maximumFractionDigits: d || 0, minimumFractionDigits: d || 0 }); }
  function money(n) { return fmt(Math.round(n)) + ' ' + S.sar; }

  /* ---- STL parsing ------------------------------------------------------ */
  // Returns a Float32Array of triangle vertices [x0,y0,z0,x1,...] (9 per triangle).
  function parseSTL(buf) {
    var dv = new DataView(buf);
    if (buf.byteLength >= 84) {
      var n = dv.getUint32(80, true);
      if (84 + n * 50 === buf.byteLength && n > 0) {          // binary STL
        var out = new Float32Array(n * 9);
        for (var i = 0; i < n; i++) {
          var o = 84 + i * 50 + 12;
          for (var k = 0; k < 9; k++) out[i * 9 + k] = dv.getFloat32(o + k * 4, true);
        }
        return out;
      }
    }
    var text = new TextDecoder().decode(new Uint8Array(buf));  // ASCII STL
    var re = /vertex\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)/g, m, v = [];
    while ((m = re.exec(text))) v.push(+m[1], +m[2], +m[3]);
    if (v.length < 9 || v.length % 9 !== 0) return null;
    return new Float32Array(v);
  }

  function measure(t) {
    var min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
    var vol = 0, area = 0;
    for (var i = 0; i < t.length; i += 9) {
      var ax = t[i], ay = t[i + 1], az = t[i + 2], bx = t[i + 3], by = t[i + 4], bz = t[i + 5], cx = t[i + 6], cy = t[i + 7], cz = t[i + 8];
      vol += (ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)) / 6;
      var ux = bx - ax, uy = by - ay, uz = bz - az, wx = cx - ax, wy = cy - ay, wz = cz - az;
      var nx = uy * wz - uz * wy, ny = uz * wx - ux * wz, nz = ux * wy - uy * wx;
      area += Math.sqrt(nx * nx + ny * ny + nz * nz) / 2;
      for (var k = 0; k < 9; k++) {
        var a = k % 3, val = t[i + k];
        if (val < min[a]) min[a] = val;
        if (val > max[a]) max[a] = val;
      }
    }
    return { min: min, max: max, size: [max[0] - min[0], max[1] - min[1], max[2] - min[2]], volume: Math.abs(vol), area: area, tris: t.length / 9 };
  }

  /* ---- Preview: flat-shaded isometric render on a canvas ---------------- */
  function draw(canvas, t, m) {
    var dpr = window.devicePixelRatio || 1, W = canvas.clientWidth || 320, H = canvas.clientHeight || 260;
    canvas.width = W * dpr; canvas.height = H * dpr;
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    var c = [(m.min[0] + m.max[0]) / 2, (m.min[1] + m.max[1]) / 2, (m.min[2] + m.max[2]) / 2];
    var rz = -Math.PI / 4, rx = -Math.PI / 3.2;        // look from front-right, above
    var cz = Math.cos(rz), sz = Math.sin(rz), cxr = Math.cos(rx), sxr = Math.sin(rx);
    function proj(x, y, z) {
      x -= c[0]; y -= c[1]; z -= c[2];
      var x1 = x * cz - y * sz, y1 = x * sz + y * cz;
      return [x1, y1 * cxr - z * sxr, y1 * sxr + z * cxr];
    }
    var step = Math.max(1, Math.ceil(m.tris / 80000));  // keep huge files responsive
    var faces = [], lo = [Infinity, Infinity], hi = [-Infinity, -Infinity];
    for (var i = 0; i < t.length; i += 9 * step) {
      var p = [proj(t[i], t[i + 1], t[i + 2]), proj(t[i + 3], t[i + 4], t[i + 5]), proj(t[i + 6], t[i + 7], t[i + 8])];
      var ux = p[1][0] - p[0][0], uy = p[1][1] - p[0][1], uz = p[1][2] - p[0][2];
      var wx = p[2][0] - p[0][0], wy = p[2][1] - p[0][1], wz = p[2][2] - p[0][2];
      var nx = uy * wz - uz * wy, ny = uz * wx - ux * wz, nz = ux * wy - uy * wx;
      var len = Math.sqrt(nx * nx + ny * ny + nz * nz) || 1;
      var light = Math.abs((nx * 0.35 + ny * -0.45 + nz * 0.82) / len);
      faces.push({ p: p, d: p[0][1] + p[1][1] + p[2][1], l: light });
      for (var k = 0; k < 3; k++) {
        if (p[k][0] < lo[0]) lo[0] = p[k][0]; if (p[k][0] > hi[0]) hi[0] = p[k][0];
        if (p[k][2] < lo[1]) lo[1] = p[k][2]; if (p[k][2] > hi[1]) hi[1] = p[k][2];
      }
    }
    faces.sort(function (a, b) { return b.d - a.d; });   // far to near
    var s = 0.86 * Math.min(W / ((hi[0] - lo[0]) || 1), H / ((hi[1] - lo[1]) || 1));
    var ox = W / 2 - s * (lo[0] + hi[0]) / 2, oy = H / 2 + s * (lo[1] + hi[1]) / 2;
    faces.forEach(function (f) {
      var g = Math.round(70 + 150 * f.l);
      ctx.fillStyle = 'rgb(' + Math.round(g * 0.36) + ',' + Math.round(g * 0.78) + ',' + Math.round(g * 0.58) + ')';
      ctx.strokeStyle = ctx.fillStyle;
      ctx.beginPath();
      ctx.moveTo(ox + s * f.p[0][0], oy - s * f.p[0][2]);
      ctx.lineTo(ox + s * f.p[1][0], oy - s * f.p[1][2]);
      ctx.lineTo(ox + s * f.p[2][0], oy - s * f.p[2][2]);
      ctx.closePath(); ctx.fill(); ctx.stroke();
    });
  }

  /* ---- Estimate --------------------------------------------------------- */
  function estimate(m, opts) {
    var k = opts.scale / 100;
    var volCm3 = m.volume * k * k * k / 1000;
    var areaCm2 = m.area * k * k / 100;
    var shell = Math.min(volCm3, areaCm2 * WALL_CM);
    var grams = DENSITY[opts.material] * (shell + (volCm3 - shell) * opts.infill / 100);
    var piece = Math.max(PRICING.minPrice, grams * PRICING.perGram[opts.material]);
    var total = PRICING.setupFee + piece * opts.qty;
    return {
      size: m.size.map(function (d) { return d * k; }),
      volume: volCm3, grams: grams,
      low: total * (1 - PRICING.range), high: total * (1 + PRICING.range),
      pieceLow: piece * (1 - PRICING.range) + PRICING.setupFee / opts.qty, pieceHigh: piece * (1 + PRICING.range) + PRICING.setupFee / opts.qty
    };
  }

  /* ---- UI --------------------------------------------------------------- */
  function select(name, opts, val) {
    return '<select name="' + name + '">' + opts.map(function (o) {
      var v = Array.isArray(o) ? o[0] : o, t = Array.isArray(o) ? o[1] : o;
      return '<option value="' + esc(v) + '"' + (String(v) === String(val) ? ' selected' : '') + '>' + esc(t) + '</option>';
    }).join('') + '</select>';
  }

  function init() {
    var host = document.querySelector('[data-b3d-quote]');
    if (!host) return;
    host.innerHTML =
      '<label class="b3d-quote__drop" data-q-drop>' +
        '<input type="file" accept=".stl,model/stl,application/sla" data-q-file hidden>' +
        '<span class="b3d-quote__drop-icon" aria-hidden="true">⬆</span>' +
        '<strong>' + esc(S.drop) + '</strong><small>' + esc(S.dropHint) + '</small>' +
      '</label>' +
      '<p class="b3d-quote__status" data-q-status role="status"></p>' +
      '<div class="b3d-quote__result" data-q-result hidden>' +
        '<div class="b3d-quote__preview"><canvas data-q-canvas aria-hidden="true"></canvas><div class="b3d-quote__file" data-q-name></div></div>' +
        '<div class="b3d-quote__panel">' +
          '<dl class="b3d-quote__stats" data-q-stats></dl>' +
          '<form class="b3d-quote__form" data-q-form>' +
            '<label>' + esc(S.material) + select('material', S.materials, 'PLA') + '</label>' +
            '<label>' + esc(S.color) + select('color', S.colors, S.colors[0]) + '</label>' +
            '<label>' + esc(S.infill) + select('infill', S.infillOpts, '25') + '</label>' +
            '<label>' + esc(S.scale) + ' (%)<input type="number" name="scale" min="10" max="400" step="5" value="100" inputmode="numeric"></label>' +
            '<label>' + esc(S.qty) + '<input type="number" name="qty" min="1" max="500" value="1" inputmode="numeric"></label>' +
          '</form>' +
          '<div class="b3d-quote__price" data-q-price></div>' +
          '<p class="b3d-quote__warn" data-q-warn hidden>' + esc(S.tooLarge) + '</p>' +
          '<p class="b3d-quote__note">' + esc(S.note) + '</p>' +
          '<a class="btn btn-primary b3d-quote__send" data-q-send target="_blank" rel="noopener noreferrer">' + esc(S.send) + '</a>' +
          '<p class="b3d-quote__attach">' + esc(S.attach) + '</p>' +
          '<button type="button" class="b3d-quote__again" data-q-again>' + esc(S.another) + '</button>' +
        '</div>' +
      '</div>';

    var fileIn = host.querySelector('[data-q-file]'), drop = host.querySelector('[data-q-drop]');
    var status = host.querySelector('[data-q-status]'), result = host.querySelector('[data-q-result]');
    var form = host.querySelector('[data-q-form]'), tris = null, meas = null, fileName = '';

    function opts() {
      var f = form.elements;
      return {
        material: f.material.value, color: f.color.value, infill: +f.infill.value,
        scale: Math.min(400, Math.max(10, +f.scale.value || 100)), qty: Math.min(500, Math.max(1, Math.round(+f.qty.value) || 1))
      };
    }

    function update() {
      if (!meas) return;
      var o = opts(), e = estimate(meas, o);
      var dims = e.size.map(function (d) { return fmt(d, 1); }).join(' × ') + ' ' + S.mm;
      host.querySelector('[data-q-stats]').innerHTML =
        '<div><dt>' + esc(S.size) + '</dt><dd>' + dims + '</dd></div>' +
        '<div><dt>' + esc(S.volume) + '</dt><dd>' + fmt(e.volume, 1) + ' ' + S.cm3 + '</dd></div>' +
        '<div><dt>' + esc(S.weight) + '</dt><dd>~' + fmt(e.grams) + ' ' + S.g + ' / ' + esc(S.perPiece) + '</dd></div>';
      host.querySelector('[data-q-price]').innerHTML =
        '<span>' + esc(S.estimate) + '</span>' +
        '<strong>' + money(e.pieceLow) + ' – ' + money(e.pieceHigh) + '</strong> <small>' + esc(S.perPiece) + '</small>' +
        (o.qty > 1 ? '<em>' + esc(S.total) + ' ' + fmt(o.qty) + ' ' + esc(S.pieces) + ': ' + money(e.low) + ' – ' + money(e.high) + '</em>' : '');
      host.querySelector('[data-q-warn]').hidden = Math.max.apply(null, e.size) <= MAX_BUILD_MM;
      var mat = S.materials.filter(function (x) { return x[0] === o.material; })[0][1];
      var msg = [S.msgIntro, '',
        '• ' + S.file + ': ' + fileName,
        '• ' + S.size + ': ' + dims,
        '• ' + S.material + ': ' + mat,
        '• ' + S.color + ': ' + o.color,
        '• ' + S.infill + ': ' + o.infill + '%',
        '• ' + S.scale + ': ' + o.scale + '%',
        '• ' + S.qty + ': ' + fmt(o.qty),
        '• ' + S.estimate + ': ' + money(e.low) + ' – ' + money(e.high),
        '', S.attach].join('\n');
      host.querySelector('[data-q-send]').href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(msg);
    }

    function load(file) {
      if (!file) return;
      if (file.size > MAX_FILE_MB * 1048576) { status.textContent = S.tooBig; return; }
      status.textContent = S.reading;
      var r = new FileReader();
      r.onload = function () {
        var t = null;
        try { t = parseSTL(r.result); } catch (err) { t = null; }
        if (!t) { status.textContent = S.bad; result.hidden = true; return; }
        tris = t; meas = measure(t); fileName = file.name;
        if (!(meas.volume > 0)) { status.textContent = S.bad; result.hidden = true; return; }
        status.textContent = '';
        drop.hidden = true; result.hidden = false;
        host.querySelector('[data-q-name]').textContent = file.name;
        draw(host.querySelector('[data-q-canvas]'), tris, meas);
        update();
        if (window.dataLayer) window.dataLayer.push({ event: 'quote_file_loaded' });
      };
      r.onerror = function () { status.textContent = S.bad; };
      r.readAsArrayBuffer(file);
    }

    fileIn.addEventListener('change', function () { load(fileIn.files[0]); });
    ['dragenter', 'dragover'].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('is-over'); });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('is-over'); });
    });
    drop.addEventListener('drop', function (e) { load(e.dataTransfer.files[0]); });
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    host.querySelector('[data-q-again]').addEventListener('click', function () {
      result.hidden = true; drop.hidden = false; fileIn.value = ''; meas = tris = null;
    });
    host.querySelector('[data-q-send]').addEventListener('click', function () {
      if (window.dataLayer) window.dataLayer.push({ event: 'quote_whatsapp_click' });
    });
    window.addEventListener('resize', function () { if (meas) draw(host.querySelector('[data-q-canvas]'), tris, meas); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
