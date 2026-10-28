/* Homepage welcome band: "Welcome to Black Arrow 3D" printed layer by layer inside a drawn
   printer chamber (frame posts, Z screws, LED strip, textured PEI plate, gantry rail).
   Plays once per visit (sessionStorage); after that, and with reduced motion, the finished
   print is drawn straight away. Pointing at the band prints it again. Text and font follow <html lang>. */
(function () {
  var band = document.querySelector('[data-b3d-welcome]');
  if (!band) return;
  var canvas = band.querySelector('.b3d-welcome__print'), chamber = band.querySelector('.b3d-welcome__chamber');
  if (!canvas || !chamber || !canvas.getContext) return;
  var ctx = canvas.getContext('2d'), bctx = chamber.getContext('2d');

  var AR = (document.documentElement.lang || '').slice(0, 2) === 'ar';
  var TEXT = AR ? 'أهلاً بك في Black Arrow 3D' : 'Welcome to Black Arrow 3D';
  var FONT = AR ? '700 {s}px "Noto Kufi Arabic", Tahoma, sans-serif' : '800 {s}px "Playfair Display", Georgia, serif';
  var DESCEND_MS = 350, DURATION = 2400, LAYER_CSS_PX = 3, SEEN_KEY = 'b3dWelcomePrinted';
  var raf = 0, played = false, printing = false;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function seen() { try { return sessionStorage.getItem(SEEN_KEY) === '1'; } catch (e) { return false; } }
  function markSeen() { try { sessionStorage.setItem(SEEN_KEY, '1'); } catch (e) {} }

  function hexToRgb(h) { var n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  var HOT = hexToRgb('#FFF4C9'), WARM = hexToRgb('#FFB547'), AMBER = hexToRgb('#F59E0B');
  function mix(a, b, t) { return 'rgb(' + a.map(function (v, i) { return Math.round(v + (b[i] - v) * t); }).join(',') + ')'; }
  function cool(age) { // ms since laid -> plastic colour
    if (age < 160) return mix(HOT, WARM, Math.max(0, age) / 160);
    if (age < 650) return mix(WARM, AMBER, (age - 160) / 490);
    return 'rgb(' + AMBER.join(',') + ')';
  }

  // Slice the text into layers, bottom to top, like a slicer.
  function plan() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = Math.round(canvas.clientWidth * dpr), H = Math.round(canvas.clientHeight * dpr);
    canvas.width = W; canvas.height = H;
    var mask = document.createElement('canvas'); mask.width = W; mask.height = H;
    var m = mask.getContext('2d');
    m.direction = AR ? 'rtl' : 'ltr'; m.textAlign = 'center'; m.textBaseline = 'middle';
    var size = H * 0.42;
    m.font = FONT.replace('{s}', size);
    var w = m.measureText(TEXT).width;
    if (w > W * 0.82) { size *= (W * 0.82) / w; m.font = FONT.replace('{s}', size); }
    m.fillStyle = '#000';
    m.fillText(TEXT, W / 2, H * 0.6);
    var data = m.getImageData(0, 0, W, H).data;
    var layerH = Math.max(2, Math.round(LAYER_CSS_PX * dpr));
    var layers = [];
    for (var top = H - layerH; top > -layerH; top -= layerH) {
      var y0 = Math.max(0, top), y1 = Math.min(H, top + layerH), lo = W, hi = -1;
      for (var y = y0; y < y1; y++) for (var x = 0; x < W; x++) {
        if (data[(y * W + x) * 4 + 3] > 90) { if (x < lo) lo = x; if (x > hi) hi = x; }
      }
      if (hi >= 0) layers.push({ top: y0, h: y1 - y0, lo: lo, hi: hi + 1 });
    }
    var total = layers.reduce(function (s, L) { return s + (L.hi - L.lo); }, 0) || 1, t = DESCEND_MS;
    layers.forEach(function (L, i) {
      L.start = t; L.dur = DURATION * (L.hi - L.lo) / total; t += L.dur; L.end = t;
      L.rev = (i % 2 === 1); // serpentine, like a real toolpath
    });
    var scale = Math.max(0.7, Math.min(1.25, size / (52 * dpr))) * dpr;
    var P = { W: W, H: H, dpr: dpr, s: scale, mask: mask, layers: layers,
              plateY: layers.length ? layers[0].top + layers[0].h : H };
    drawChamber(P);
    return P;
  }

  // The printer around the print: chamber walls, LED strip, frame posts with Z screws, build plate.
  function drawChamber(P) {
    var d = P.dpr, r = chamber.getBoundingClientRect(), pr = canvas.getBoundingClientRect();
    var W = Math.round(r.width * d), H = Math.round(r.height * d);
    chamber.width = W; chamber.height = H;
    var oy = (pr.top - r.top) * d, plate = oy + P.plateY, c = bctx;
    var wall = c.createLinearGradient(0, 0, 0, H);
    wall.addColorStop(0, '#0d0f12'); wall.addColorStop(.55, '#1a1d22'); wall.addColorStop(1, '#121418');
    c.fillStyle = wall; c.fillRect(0, 0, W, H);
    c.fillStyle = 'rgba(255,255,255,.028)'; // back panel seams
    for (var x = W / 2 % (140 * d); x < W; x += 140 * d) c.fillRect(Math.round(x), 0, Math.max(1, d), plate);
    var led = c.createRadialGradient(W / 2, -10 * d, 0, W / 2, -10 * d, W * .6); // chamber light
    led.addColorStop(0, 'rgba(255,240,214,.22)'); led.addColorStop(.5, 'rgba(255,240,214,.06)'); led.addColorStop(1, 'rgba(255,240,214,0)');
    c.fillStyle = led; c.fillRect(0, 0, W, H);
    var strip = c.createLinearGradient(W * .2, 0, W * .8, 0); // LED strip, fading at the ends
    strip.addColorStop(0, 'rgba(255,244,224,0)'); strip.addColorStop(.5, 'rgba(255,244,224,.45)'); strip.addColorStop(1, 'rgba(255,244,224,0)');
    c.fillStyle = strip; c.fillRect(W * .2, 0, W * .6, 1.5 * d);
    // Build plate in perspective: textured PEI, gold on black.
    var inset = Math.max(30 * d, W * .05), x0 = inset, x1 = W - inset;
    c.save();
    c.beginPath(); c.moveTo(x0, plate); c.lineTo(x1, plate); c.lineTo(W + 4 * d, H); c.lineTo(-4 * d, H); c.closePath(); c.clip();
    var pg = c.createLinearGradient(0, plate, 0, H);
    pg.addColorStop(0, '#2e2617'); pg.addColorStop(1, '#16120b');
    c.fillStyle = pg; c.fillRect(0, plate, W, H - plate);
    for (var i = 0, n = Math.round(W * (H - plate) / (14 * d * d)); i < n; i++) {
      c.fillStyle = Math.random() < .6 ? 'rgba(222,178,96,.30)' : 'rgba(0,0,0,.35)';
      c.fillRect(Math.random() * W, plate + Math.random() * (H - plate), d, d);
    }
    var pool = c.createRadialGradient(W / 2, plate, 0, W / 2, plate, W * .45); // warm light on the plate
    pool.addColorStop(0, 'rgba(245,158,11,.22)'); pool.addColorStop(1, 'rgba(245,158,11,0)');
    c.fillStyle = pool; c.fillRect(0, plate, W, H - plate);
    c.restore();
    c.fillStyle = 'rgba(255,214,150,.45)'; c.fillRect(x0, plate, x1 - x0, Math.max(1, d)); // plate edge
    // Frame posts (aluminium extrusion) and Z lead screws, both sides.
    var pw = Math.max(10 * d, W * .014);
    [[0, 1], [W - pw, -1]].forEach(function (p) {
      var px = p[0], g = c.createLinearGradient(px, 0, px + pw, 0);
      g.addColorStop(0, '#2b2e34'); g.addColorStop(.45, '#5a5f68'); g.addColorStop(1, '#25282d');
      c.fillStyle = g; c.fillRect(px, 0, pw, H);
      c.fillStyle = 'rgba(0,0,0,.45)'; c.fillRect(px + pw / 2 - .75 * d, 0, 1.5 * d, H); // T-slot
      var sx = p[1] > 0 ? px + pw + 8 * d : px - 12 * d; // lead screw
      c.fillStyle = '#6e6a60'; c.fillRect(sx, 0, 4 * d, plate);
      c.strokeStyle = 'rgba(30,28,24,.8)'; c.lineWidth = d;
      for (var y = 0; y < plate; y += 3 * d) { c.beginPath(); c.moveTo(sx, y + 2 * d); c.lineTo(sx + 4 * d, y); c.stroke(); }
    });
  }

  // X gantry rail the head rides on; it climbs with every layer.
  function drawRail(P, y, alpha) {
    var s = P.s, ry = Math.max(5 * s, y - 40 * s);
    ctx.save(); ctx.globalAlpha = alpha;
    var g = ctx.createLinearGradient(0, ry - 4 * s, 0, ry + 4 * s);
    g.addColorStop(0, '#4a4d54'); g.addColorStop(.5, '#22252a'); g.addColorStop(1, '#101114');
    ctx.fillStyle = g; ctx.fillRect(-20, ry - 4 * s, P.W + 40, 8 * s);
    ctx.fillStyle = 'rgba(255,255,255,.18)'; ctx.fillRect(-20, ry - 4 * s, P.W + 40, Math.max(1, .6 * s));
    ctx.restore();
  }

  function roundRect(x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }

  // Print head with its nozzle tip at (x, y): nozzle, heater block, heatsink, fan shroud, filament.
  function drawHead(P, x, y, alpha, extruding, now) {
    var s = P.s;
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = 'rgba(245,158,11,.75)'; ctx.lineWidth = 1.6 * s; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(x + 2 * s, -2); ctx.quadraticCurveTo(x + 9 * s, (y - 46 * s) / 2, x + 2 * s, y - 46 * s); ctx.stroke();
    var g = ctx.createLinearGradient(x - 15 * s, 0, x + 15 * s, 0);
    g.addColorStop(0, '#26241f'); g.addColorStop(.5, '#3a3832'); g.addColorStop(1, '#1c1b17');
    ctx.fillStyle = g;
    roundRect(x - 15 * s, y - 48 * s, 30 * s, 22 * s, 3 * s); ctx.fill();
    ctx.strokeStyle = '#55524a'; ctx.lineWidth = 1 * s;
    ctx.beginPath(); ctx.arc(x, y - 37 * s, 6.5 * s, 0, Math.PI * 2); ctx.stroke(); // fan
    ctx.beginPath(); ctx.arc(x, y - 37 * s, 2 * s, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = '#F59E0B'; ctx.fillRect(x - 15 * s, y - 27.5 * s, 30 * s, 1.8 * s); // brand stripe
    ctx.fillStyle = '#9a968c'; // heatsink fins
    for (var i = 0; i < 4; i++) ctx.fillRect(x - 5 * s, y - 25 * s + i * 2.4 * s, 10 * s, 1.3 * s);
    ctx.fillStyle = '#6f6c64'; ctx.fillRect(x - 1.5 * s, y - 25 * s, 3 * s, 10 * s);
    var hb = ctx.createLinearGradient(0, y - 15 * s, 0, y - 8 * s); // heater block
    hb.addColorStop(0, '#d2cec4'); hb.addColorStop(1, '#8e8a80');
    ctx.fillStyle = hb; roundRect(x - 7 * s, y - 15 * s, 14 * s, 7 * s, 1.2 * s); ctx.fill();
    ctx.fillStyle = '#d4a64a'; // brass nozzle
    ctx.beginPath(); ctx.moveTo(x - 3.5 * s, y - 8 * s); ctx.lineTo(x + 3.5 * s, y - 8 * s); ctx.lineTo(x + 1 * s, y - .8 * s); ctx.lineTo(x - 1 * s, y - .8 * s); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fillRect(x - 2.4 * s, y - 7.5 * s, 1 * s, 5 * s);
    if (extruding) { // molten tip glow
      var f = .8 + .2 * Math.sin(now / 22);
      var rg = ctx.createRadialGradient(x, y, 0, x, y, 9 * s);
      rg.addColorStop(0, 'rgba(255,214,130,' + (.75 * f) + ')'); rg.addColorStop(1, 'rgba(255,160,40,0)');
      ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(x, y, 9 * s, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }

  function render(P, now) {
    ctx.globalCompositeOperation = 'source-over';
    ctx.clearRect(0, 0, P.W, P.H);
    var head = null;
    P.layers.forEach(function (L) {
      if (now <= L.start) return;
      var f = Math.min(1, (now - L.start) / L.dur);
      var x = L.rev ? L.hi - (L.hi - L.lo) * f : L.lo + (L.hi - L.lo) * f;
      var a = L.rev ? x : L.lo, b = L.rev ? L.hi : x;
      ctx.fillStyle = f >= 1 ? cool(now - L.end + 120) : cool(now - (L.start + L.dur * f * 0.5));
      ctx.fillRect(a, L.top, b - a, L.h);
      ctx.fillStyle = 'rgba(0,0,0,.18)'; // faint seam between layers
      ctx.fillRect(a, L.top, b - a, Math.max(1, P.dpr * 0.6));
      if (f < 1) head = { x: x, y: L.top };
    });
    ctx.globalCompositeOperation = 'destination-in';
    ctx.drawImage(P.mask, 0, 0);
    ctx.globalCompositeOperation = 'source-over';
    return head;
  }

  function drawFinished(P) {
    if (!P.layers.length) return;
    var lastL = P.layers[P.layers.length - 1];
    render(P, lastL.end + 2000);
    drawRail(P, lastL.top - 50 * P.dpr, 1);
  }

  function play(again) {
    cancelAnimationFrame(raf);
    var P = plan();
    if (!P.layers.length) return;
    if (reduce || (!again && (played || seen()))) { drawFinished(P); printing = false; return; }
    played = true; printing = true; markSeen();
    var first = P.layers[0], end = P.layers[P.layers.length - 1].end;
    var t0 = performance.now(), last = { x: first.rev ? first.hi : first.lo, y: first.top };
    (function frame(ts) {
      var now = ts - t0;
      var head = render(P, now);
      if (now < DESCEND_MS) { // head comes down to the first layer
        var k = Math.max(0, now) / DESCEND_MS, e = 1 - Math.pow(1 - k, 3), hy = first.top - (1 - e) * 40 * P.dpr;
        drawRail(P, hy, Math.min(1, k * 2)); drawHead(P, last.x, hy, Math.min(1, k * 2), false, now);
      } else if (head) {
        last = head; drawRail(P, head.y, 1); drawHead(P, head.x, head.y, 1, true, now);
      } else if (now < end + 650) { // done: the head lifts off and fades out
        var q = Math.min(1, (now - end) / 650), ly = last.y - q * q * 50 * P.dpr;
        drawRail(P, ly, 1); drawHead(P, last.x, ly, 1 - q, false, now);
      } else drawRail(P, last.y - 50 * P.dpr, 1);
      if (now < end + 1000) raf = requestAnimationFrame(frame);
      else printing = false;
    })(t0);
  }

  function start(again) {
    var go = function () { play(again === true); };
    var ready = document.fonts && document.fonts.load ? document.fonts.load(FONT.replace('{s}', 40), TEXT) : Promise.resolve();
    ready.then(go, go);
  }

  // Hover replays the print (mouse/trackpad only), once the current one has finished.
  band.addEventListener('mouseenter', function () {
    if (!printing && !reduce) start(true);
  });

  var lastW = 0, rt;
  window.addEventListener('resize', function () {
    if (canvas.clientWidth === lastW) return; // ignore phone address-bar height changes
    clearTimeout(rt); rt = setTimeout(function () { lastW = canvas.clientWidth; start(); }, 200);
  });
  lastW = canvas.clientWidth;
  start();
})();
