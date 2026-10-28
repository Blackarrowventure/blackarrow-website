// UPS inspection report tool. Kept in its own file: the site CSP blocks inline scripts.
  (function () {
    'use strict';
    var KEY = 'bav_ups_report_draft_v1';
    var form = document.getElementById('report');

    var CHECKS = [
      ['UPS cabinet clean, no dust build-up', 'نظافة الكابينة'],
      ['Cooling fans running, no noise', 'مراوح التبريد'],
      ['Air filters clean', 'فلاتر الهواء'],
      ['Power and control terminals tight (torque checked)', 'إحكام الأطراف'],
      ['Cables and busbars: no heat discoloration', 'الكابلات وقضبان التوصيل'],
      ['DC and AC capacitors: no bulging or leaks', 'المكثفات'],
      ['Display, LEDs and alarms reviewed', 'الشاشة والإنذارات'],
      ['Event / alarm log reviewed and cleared', 'سجل الأحداث'],
      ['Input / output / bypass breakers condition', 'القواطع'],
      ['Maintenance bypass switch operation', 'مفتاح التجاوز للصيانة'],
      ['Emergency power off (EPO) circuit intact', 'دائرة الإيقاف الطارئ'],
      ['Earthing / grounding connections', 'التأريض'],
      ['Battery cabinet / rack clean and ventilated', 'كابينة البطاريات'],
      ['Battery terminals: no corrosion, covers fitted', 'أطراف البطاريات'],
      ['Batteries: no swelling, cracks or leaks', 'سلامة البطاريات'],
      ['Labels and single-line diagram present', 'الملصقات والمخطط'],
      ['Remote monitoring / SNMP / BMS communication', 'المراقبة عن بعد']
    ];
    var TESTS = [
      ['Transfer to static bypass and back to inverter', 'التحويل إلى التجاوز والعودة'],
      ['Mains failure simulation (transfer to battery)', 'محاكاة انقطاع الكهرباء'],
      ['Battery discharge / autonomy test', 'اختبار تفريغ البطارية'],
      ['Alarm and buzzer test', 'اختبار الإنذار'],
      ['Clock / date and firmware checked', 'الساعة وإصدار البرنامج']
    ];
    var MEAS = [
      ['Input voltage (L-N)', 'V'], ['Input current', 'A'], ['Bypass voltage (L-N)', 'V'],
      ['Output voltage (L-N)', 'V'], ['Output current', 'A'], ['Output load per phase', '%']
    ];

    function statusCell(name, opts) {
      return '<div class="status">' + opts.map(function (o) {
        return '<label><input type="radio" name="' + name + '" value="' + o[0] + '"> ' + o[1] + '</label>';
      }).join('') + '</div>';
    }
    var S4 = [['ok', 'OK'], ['attn', 'Attention'], ['fail', 'Fail'], ['na', 'N/A']];
    var S3 = [['ok', 'Pass'], ['fail', 'Fail'], ['na', 'Not done']];
    document.querySelector('#checks tbody').innerHTML = CHECKS.map(function (c, i) {
      return '<tr><td>' + c[0] + '<br><small style="color:#5d656b">' + c[1] + '</small></td><td>' + statusCell('chk' + i, S4) + '</td><td><input name="chk' + i + '_note"></td></tr>';
    }).join('');
    document.querySelector('#tests tbody').innerHTML = TESTS.map(function (c, i) {
      return '<tr><td>' + c[0] + '<br><small style="color:#5d656b">' + c[1] + '</small></td><td>' + statusCell('tst' + i, S3) + '</td><td><input name="tst' + i + '_note"></td></tr>';
    }).join('');
    document.querySelector('#meas tbody').innerHTML = MEAS.map(function (m, i) {
      return '<tr><td>' + m[0] + '</td>' + [1, 2, 3].map(function (l) {
        return '<td class="num"><input name="m' + i + '_l' + l + '" type="number" step="0.1" inputmode="decimal"></td>';
      }).join('') + '<td>' + m[1] + '</td></tr>';
    }).join('');

    /* ---- battery table: one row per block, built from strings x blocks ---- */
    var batBody = document.querySelector('#bat tbody');
    function defaultRange() {
      var bv = +document.getElementById('block_v').value;
      return { min: +(bv * 1.1).toFixed(2), max: +(bv * 1.1667).toFixed(2) };   // 12 V block: 13.2 - 14.0 V
    }
    function buildBatRows(values) {
      var strings = Math.max(1, Math.min(8, +document.getElementById('strings').value || 1));
      var blocks = Math.max(1, Math.min(80, +document.getElementById('blocks').value || 1));
      var rows = '';
      for (var s = 1; s <= strings; s++) {
        for (var b = 1; b <= blocks; b++) {
          var k = 'b' + s + '_' + b;
          rows += '<tr><td>' + s + '</td><td>' + b + '</td>' +
            '<td class="num"><input name="' + k + '_v" data-bv type="number" step="0.01" inputmode="decimal"></td>' +
            '<td class="num"><input name="' + k + '_ir" data-bir type="number" step="0.01" inputmode="decimal"></td>' +
            '<td class="num"><input name="' + k + '_t" type="number" step="0.1" inputmode="decimal"></td>' +
            '<td><select name="' + k + '_c"><option></option><option>OK</option><option>Swollen</option><option>Leaking</option><option>Corroded terminal</option><option>Replace</option></select></td></tr>';
        }
      }
      batBody.innerHTML = rows;
      if (values) restore(values);
      evaluate();
    }

    function num(v) { return v === '' || v == null ? null : +v; }
    function evaluate() {
      var r = defaultRange();
      var vmin = num(document.getElementById('vmin').value), vmax = num(document.getElementById('vmax').value);
      if (vmin == null) vmin = r.min;
      if (vmax == null) vmax = r.max;
      document.getElementById('vrange').textContent = vmin + '–' + vmax + ' V';
      document.getElementById('vmin').placeholder = r.min; document.getElementById('vmax').placeholder = r.max;
      var irLimit = num(document.getElementById('ir_limit').value);
      var vs = [], out = 0, irOut = 0;
      batBody.querySelectorAll('[data-bv]').forEach(function (el) {
        el.classList.remove('flag-low', 'flag-high');
        var v = num(el.value);
        if (v == null) return;
        vs.push(v);
        if (v < vmin) { el.classList.add('flag-low'); out++; }
        else if (v > vmax) { el.classList.add('flag-high'); out++; }
      });
      batBody.querySelectorAll('[data-bir]').forEach(function (el) {
        el.classList.remove('flag-warn');
        var v = num(el.value);
        if (v != null && irLimit != null && v > irLimit) { el.classList.add('flag-warn'); irOut++; }
      });
      var avg = vs.length ? vs.reduce(function (a, b) { return a + b; }, 0) / vs.length : null;
      document.getElementById('s_avg').textContent = avg == null ? '–' : avg.toFixed(2) + ' V';
      document.getElementById('s_minmax').textContent = vs.length ? Math.min.apply(null, vs).toFixed(2) + ' / ' + Math.max.apply(null, vs).toFixed(2) : '–';
      document.getElementById('s_out').textContent = out;
      document.getElementById('s_ir').textContent = irOut;
      ['room_temp', 'load_pct', 'n_e'].forEach(function (id) { document.getElementById(id).classList.remove('flag-warn'); });
      var t = num(document.getElementById('room_temp').value), load = num(document.getElementById('load_pct').value), ne = num(document.getElementById('n_e').value);
      if (t != null && t > 25) document.getElementById('room_temp').classList.add('flag-warn');
      if (load != null && load > 80) document.getElementById('load_pct').classList.add('flag-warn');
      if (ne != null && ne > 2) document.getElementById('n_e').classList.add('flag-warn');
      suggest({ out: out, irOut: irOut, t: t, load: load, ne: ne });
    }

    /* ---- suggestions the engineer can tap to add ---- */
    function suggest(s) {
      var list = [];
      if (s.out) list.push(s.out + ' battery block(s) outside the float voltage range: re-test after a full charge and plan replacement if confirmed.');
      if (s.irOut) list.push(s.irOut + ' battery block(s) above the internal resistance level: plan replacement of the affected blocks.');
      if (s.t != null && s.t > 25) list.push('Room temperature ' + s.t + ' °C is above 25 °C: improve cooling to protect battery life.');
      if (s.load != null && s.load > 80) list.push('UPS load ' + s.load + ' % is above 80 %: review load growth and redundancy.');
      if (s.ne != null && s.ne > 2) list.push('Neutral–earth voltage ' + s.ne + ' V is high: check the neutral and earthing system.');
      var box = document.getElementById('suggest');
      box.innerHTML = list.length ? list.map(function (x, i) { return '<button type="button" data-s="' + i + '">+ ' + x + '</button>'; }).join('') : '<span class="note">No issues detected from the readings so far.</span>';
      box.querySelectorAll('[data-s]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var ta = form.elements.recommendations;
          var line = '• ' + list[+btn.getAttribute('data-s')];
          if (ta.value.indexOf(line) === -1) ta.value = (ta.value ? ta.value + '\n' : '') + line;
          saveNow();
        });
      });
    }

    /* ---- signatures (finger or mouse) ---- */
    var pads = {};
    function setupPad(id) {
      var c = document.getElementById(id), ctx = c.getContext('2d'), drawing = false;
      function size() {
        var data = c.width ? c.toDataURL() : null, r = c.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
        c.width = r.width * dpr; c.height = r.height * dpr; ctx.scale(dpr, dpr);
        ctx.lineWidth = 2; ctx.lineCap = 'round'; ctx.strokeStyle = '#16191c';
        if (data && pads[id] && pads[id].has) { var im = new Image(); im.onload = function () { ctx.drawImage(im, 0, 0, r.width, r.height); }; im.src = data; }
      }
      function pos(e) { var r = c.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
      c.addEventListener('pointerdown', function (e) { drawing = true; c.setPointerCapture(e.pointerId); var p = pos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); });
      c.addEventListener('pointermove', function (e) { if (!drawing) return; var p = pos(e); ctx.lineTo(p.x, p.y); ctx.stroke(); pads[id].has = true; });
      function mirror() { var img = document.getElementById(id + '_img'); if (pads[id].has) img.src = c.toDataURL('image/png'); else img.removeAttribute('src'); }
      ['pointerup', 'pointercancel'].forEach(function (ev) { c.addEventListener(ev, function () { if (drawing) { drawing = false; mirror(); save(); } }); });
      pads[id] = { canvas: c, has: false, load: function (url) { var im = new Image(); im.onload = function () { var r = c.getBoundingClientRect(); ctx.drawImage(im, 0, 0, r.width, r.height); pads[id].has = true; }; im.src = url; document.getElementById(id + '_img').src = url; },
                   clear: function () { ctx.clearRect(0, 0, c.width, c.height); pads[id].has = false; document.getElementById(id + '_img').removeAttribute('src'); } };
      size(); window.addEventListener('resize', size);
    }
    setupPad('sig_eng'); setupPad('sig_client');
    document.querySelectorAll('[data-clear]').forEach(function (b) { b.addEventListener('click', function () { pads[b.getAttribute('data-clear')].clear(); save(); }); });

    /* ---- draft: kept in this browser only ---- */
    function collect() {
      var data = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name) return;
        if ((el.type === 'radio' || el.type === 'checkbox')) { if (el.checked) data[el.name] = el.value; }
        else data[el.name] = el.value;
      });
      data._vmin = document.getElementById('vmin').value; data._vmax = document.getElementById('vmax').value;
      Object.keys(pads).forEach(function (id) { if (pads[id].has) data['_' + id] = pads[id].canvas.toDataURL('image/png'); });
      return data;
    }
    function restore(data) {
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || !(el.name in data)) return;
        if (el.type === 'radio' || el.type === 'checkbox') el.checked = (data[el.name] === el.value);
        else el.value = data[el.name];
      });
    }
    var savedEl = document.getElementById('saved'), timer = null;
    function saveNow() {
      clearTimeout(timer);
      try { localStorage.setItem(KEY, JSON.stringify(collect())); } catch (e) {}
    }
    window.addEventListener('pagehide', saveNow);
    document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') saveNow(); });
    function save() {
      clearTimeout(timer);
      timer = setTimeout(function () {
        try { localStorage.setItem(KEY, JSON.stringify(collect())); savedEl.textContent = 'Draft saved on this device ' + new Date().toLocaleTimeString(); }
        catch (e) { savedEl.textContent = 'Draft could not be saved on this device'; }
      }, 300);
    }
    function newReportNo() {
      var d = new Date(), p = function (n) { return String(n).padStart(2, '0'); };
      return 'BAV-UPS-' + d.getFullYear() + p(d.getMonth() + 1) + p(d.getDate()) + '-' + p(d.getHours()) + p(d.getMinutes());
    }
    function fresh() {
      form.reset();
      Object.keys(pads).forEach(function (id) { pads[id].clear(); });
      document.getElementById('report_no').value = newReportNo();
      document.getElementById('date').valueAsDate = new Date();
      document.getElementById('vmin').value = ''; document.getElementById('vmax').value = '';
      buildBatRows(null);
    }

    var draft = null;
    try { draft = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { draft = null; }
    if (draft) {
      restore(draft);
      document.getElementById('vmin').value = draft._vmin || ''; document.getElementById('vmax').value = draft._vmax || '';
      buildBatRows(draft);
      Object.keys(pads).forEach(function (id) { if (draft['_' + id]) pads[id].load(draft['_' + id]); });
    } else {
      fresh();
    }

    form.addEventListener('input', function (e) {
      if (e.target.id === 'strings' || e.target.id === 'blocks' || e.target.id === 'block_v') buildBatRows(collect());
      else evaluate();
      save();
    });
    form.addEventListener('change', save);
    document.getElementById('vmin').addEventListener('input', function () { evaluate(); save(); });
    document.getElementById('vmax').addEventListener('input', function () { evaluate(); save(); });
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    document.getElementById('print').addEventListener('click', function () {
      var no = document.getElementById('report_no').value || 'UPS-report';
      var prev = document.title; document.title = no + ' ' + (form.elements.client.value || '');
      window.print(); setTimeout(function () { document.title = prev; }, 500);
    });
    document.getElementById('new').addEventListener('click', function () {
      var btn = this;
      if (btn.dataset.confirm !== '1') { btn.dataset.confirm = '1'; btn.textContent = 'Tap again to clear'; setTimeout(function () { btn.dataset.confirm = ''; btn.textContent = 'New report'; }, 3000); return; }
      btn.dataset.confirm = ''; btn.textContent = 'New report';
      try { localStorage.removeItem(KEY); } catch (e) {}
      fresh(); save();
    });
  })();
