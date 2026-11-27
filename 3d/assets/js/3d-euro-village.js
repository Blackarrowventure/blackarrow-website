/* Euro Village stall page (/3d/euro-village/): the customer types the amount the stall tells them
   for a "3D item" and pays with Apple Pay or card through Paymob (api/paymob/create-intention.js,
   event "euro-village"). Paymob sends them back here with ?paid=<ref>; the page then shows the
   result in large type (amount + order number) for the stall team to check before handing over. */
(function () {
  var form = document.querySelector('[data-ev-form]');
  var result = document.querySelector('[data-ev-result]');
  if (!form || !result) return;
  var errorEl = form.querySelector('[data-ev-error]');
  var amountEl = form.querySelector('#ev-amount');
  var ar = function () { return document.documentElement.lang === 'ar'; };
  var T = function (en, a) { return ar() ? a : en; };
  var sar = function (n) { return Number(n).toLocaleString('en-US', { maximumFractionDigits: 2 }) + ' SAR'; };

  // Apple Pay only where the device can pay with it.
  var apple = form.querySelector('[data-ev-pay="applepay"]');
  // Shown where the browser says it can pay with Apple Pay, and on every iPhone / iPad: some iPhone
  // browsers (in-app ones, older Chrome) don't say so, and the Paymob page decides there anyway.
  var appleDevice = /iPhone|iPad|iPod/.test(navigator.userAgent) || (/Macintosh/.test(navigator.userAgent) && navigator.maxTouchPoints > 1);
  var canApple = false;
  try { canApple = !!(window.ApplePaySession && window.ApplePaySession.canMakePayments()); } catch (e) {}
  apple.hidden = !(canApple || appleDevice);

  form.querySelectorAll('[data-amt]').forEach(function (b) {
    b.addEventListener('click', function () { amountEl.value = b.getAttribute('data-amt'); markChip(); amountEl.focus(); });
  });
  // The quick-amount button matching the typed amount lights up.
  function markChip() {
    form.querySelectorAll('[data-amt]').forEach(function (c) { c.classList.toggle('is-on', Number(c.getAttribute('data-amt')) === Number(amountEl.value)); });
  }
  amountEl.addEventListener('input', markChip);

  // The problem is said right above the pay buttons and the field is outlined red, so the
  // customer always knows why nothing happened.
  function showError(msg, field) {
    errorEl.textContent = msg; errorEl.hidden = !msg;
    form.querySelectorAll('.is-bad').forEach(function (el) { el.classList.remove('is-bad'); });
    if (!msg) return;
    if (field) {
      (field.id === 'ev-amount' ? field.parentNode : field).classList.add('is-bad');
      field.scrollIntoView({ behavior: 'smooth', block: 'center' });
      try { field.focus({ preventScroll: true }); } catch (e) { field.focus(); }
    } else errorEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
  form.addEventListener('input', function () { if (!errorEl.hidden) showError(''); });
  var PROBLEMS = {
    invalid_billing: ['Please check your name and mobile number, then try again.', 'يرجى التحقق من الاسم ورقم الجوال ثم المحاولة مرة أخرى.'],
    invalid_amount: ['Enter the amount in SAR (1 to 20,000).', 'أدخل المبلغ بالريال (من 1 إلى 20,000).'],
    payment_not_configured: ['This payment option is not available right now. Please use another option, or pay cash at the stall.', 'وسيلة الدفع هذه غير متاحة حاليًا. استخدم وسيلة أخرى أو ادفع نقدًا في الركن.'],
    method_unavailable: ['This payment option is not available right now. Please use another option, or pay cash at the stall.', 'وسيلة الدفع هذه غير متاحة حاليًا. استخدم وسيلة أخرى أو ادفع نقدًا في الركن.'],
    gateway_rejected: ['The payment page could not be opened. Please try again, or pay cash at the stall.', 'تعذّر فتح صفحة الدفع. حاول مرة أخرى أو ادفع نقدًا في الركن.'],
    gateway_unreachable: ['The payment service is not responding. Please try again in a moment, or pay cash at the stall.', 'خدمة الدفع لا تستجيب. حاول بعد قليل أو ادفع نقدًا في الركن.'],
    order_store_unavailable: ['We could not start the payment just now. Please try again in a moment.', 'تعذّر بدء الدفع الآن. حاول مرة أخرى بعد قليل.'],
    crm_unavailable: ['We could not record the order just now. Please try again, or tell our team.', 'تعذّر تسجيل الطلب الآن. حاول مرة أخرى أو أخبر فريقنا.'],
    too_many_orders: ['Too many attempts. Please wait a minute and try again, or tell our team.', 'محاولات كثيرة. انتظر دقيقة ثم حاول مرة أخرى أو أخبر فريقنا.'],
    network: ['No internet connection. Please check your connection and try again.', 'لا يوجد اتصال بالإنترنت. تحقق من الاتصال وحاول مرة أخرى.']
  };
  function problem(err, fallbackEn, fallbackAr) {
    var code = err && err.name === 'TypeError' ? 'network' : err && err.message;
    var m = PROBLEMS[code];
    return m ? T(m[0], m[1]) : T(fallbackEn, fallbackAr);
  }

  function pay(channel, btn) {
    showError('');
    var amount = Math.round(Number(String(amountEl.value).replace(',', '.')) * 100) / 100;
    var name = form.querySelector('#ev-name').value.trim().replace(/\s+/g, ' ');
    var phone = form.querySelector('#ev-phone').value.replace(/[^\d+]/g, '');
    var email = form.querySelector('#ev-email').value.trim();
    if (!(amount >= 1 && amount <= 20000)) return showError(T('Enter the amount in SAR (1 to 20,000).', 'أدخل المبلغ بالريال (من 1 إلى 20,000).'), amountEl);
    if (name.length < 2) return showError(T('Enter your name.', 'أدخل اسمك.'), form.querySelector('#ev-name'));
    if (phone.replace(/\D/g, '').length < 9) return showError(T('Enter your mobile number (at least 9 digits), e.g. 0551234567.', 'أدخل رقم جوالك (9 أرقام على الأقل)، مثل 0551234567.'), form.querySelector('#ev-phone'));
    if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return showError(T('Check the email address, or leave it empty.', 'تحقق من البريد الإلكتروني أو اتركه فارغًا.'), form.querySelector('#ev-email'));
    var parts = name.split(' ');
    var buttons = form.querySelectorAll('[data-ev-pay]');
    buttons.forEach(function (b) { b.disabled = true; });
    var label = btn.innerHTML;
    btn.textContent = channel === 'cash' ? T('Recording your order…', 'جارٍ تسجيل الطلب…') : T('Opening secure payment…', 'جارٍ فتح الدفع الآمن…');
    if (channel === 'cash') return cash(amount, parts, phone, email, buttons, btn, label);
    fetch('/api/paymob/create-intention', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event: 'euro-village',
        amount: amount,
        channel: channel,
        lang: ar() ? 'ar' : 'en',
        // No email: a placeholder Paymob accepts; our emails skip it (isPlaceholderEmail).
        billing: { firstName: parts[0], lastName: parts.slice(1).join(' ') || '-', phone: phone, email: email || 'stall@example.com', city: 'Euro Village' },
      }),
    }).then(function (r) { return r.json().catch(function () { return {}; }); }).then(function (d) {
      if (d && d.checkoutUrl) { window.location.href = d.checkoutUrl; return; }
      throw new Error((d && d.error) || 'failed');
    }).catch(function (err) {
      buttons.forEach(function (b) { b.disabled = false; });
      btn.innerHTML = label;
      showError(problem(err, 'The payment could not be opened. Please try again, or pay cash at the stall.', 'تعذّر فتح الدفع. حاول مرة أخرى أو ادفع نقدًا في الركن.'));
    });
  }

  // Cash: the order goes to the CRM as unpaid cash; the screen tells the customer what to hand over.
  function cash(amount, parts, phone, email, buttons, btn, label) {
    fetch('/api/bank-order/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event: 'euro-village', payment: 'cash', amount: amount,
        billing: { firstName: parts[0], lastName: parts.slice(1).join(' ') || '-', phone: phone, email: email } }),
    }).then(function (r) { return r.json().catch(function () { return {}; }); }).then(function (d) {
      if (!d || !d.ok) throw new Error((d && d.error) || 'failed');
      form.hidden = true;
      result.hidden = false;
      result.setAttribute('data-state', 'cash');
      result.querySelector('[data-ev-badge]').textContent = 'SAR';
      result.querySelector('[data-ev-title]').textContent = T('Please pay in cash to our team', 'يرجى الدفع نقدًا لفريقنا');
      result.querySelector('[data-ev-amt]').textContent = sar(d.amount);
      result.querySelector('[data-ev-order]').textContent = T('Order ', 'الطلب ') + d.orderId + ' · ' + new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
      result.querySelector('[data-ev-text]').textContent = T('Show this screen to our team when you pay. Thank you!', 'أظهر هذه الشاشة لفريقنا عند الدفع. شكرًا لك!');
      window.scrollTo(0, 0);
    }).catch(function (err) {
      buttons.forEach(function (b) { b.disabled = false; });
      btn.innerHTML = label;
      showError(problem(err, 'Could not record the order. Please try again, or tell our team.', 'تعذّر تسجيل الطلب. حاول مرة أخرى أو أخبر فريقنا.'));
    });
  }

  form.querySelectorAll('[data-ev-pay]').forEach(function (b) {
    b.addEventListener('click', function () { pay(b.getAttribute('data-ev-pay'), b); });
  });
  form.addEventListener('submit', function (e) { e.preventDefault(); pay('card', form.querySelector('[data-ev-pay="card"]')); });

  // Back from Paymob: ask the server (it only trusts Paymob's signed result) and show the outcome.
  var params = new URLSearchParams(window.location.search);
  var ref = params.get('paid');
  if (!ref || !/^[a-f0-9]{24}$/.test(ref)) return;
  form.hidden = true;
  result.hidden = false;
  var badge = result.querySelector('[data-ev-badge]');
  var title = result.querySelector('[data-ev-title]');
  var amt = result.querySelector('[data-ev-amt]');
  var order = result.querySelector('[data-ev-order]');
  var text = result.querySelector('[data-ev-text]');
  function state(kind, t, x) {
    result.setAttribute('data-state', kind);
    badge.textContent = kind === 'paid' ? '✓' : kind === 'failed' ? '✕' : '…';
    title.textContent = t;
    text.textContent = x || '';
  }
  state('wait', T('Checking your payment…', 'جارٍ التحقق من الدفع…'));
  var qs = new URLSearchParams(window.location.search);
  qs.delete('paid'); qs.delete('pm'); qs.set('ref', ref);
  var tries = 0;
  (function check() {
    tries++;
    fetch('/api/paymob/status/?' + qs.toString()).then(function (r) { return r.json(); }).catch(function () { return {}; }).then(function (d) {
      if (d.amount) amt.textContent = sar(d.amount);
      if (d.orderNumber) order.textContent = T('Order ', 'الطلب ') + d.orderNumber + ' · ' + new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
      if (d.status === 'paid') {
        state('paid', T('Payment received. Thank you!', 'تم استلام الدفع. شكرًا لك!'), T('Please show this screen to our team.', 'يرجى إظهار هذه الشاشة لفريقنا.'));
        // Clean address: a refresh re-checks the same order, never pays again.
        try { history.replaceState(null, '', '/3d/euro-village/?paid=' + ref); } catch (e) {}
      } else if (d.status === 'failed') {
        state('failed', T('Payment not completed', 'لم يكتمل الدفع'), T('No money was taken. Tap "New payment" to try again.', 'لم يتم خصم أي مبلغ. اضغط "دفعة جديدة" للمحاولة مرة أخرى.'));
      } else if (tries < 40) {
        if (tries === 8) state('wait', T('Still confirming your payment…', 'ما زلنا نؤكد الدفع…'), T('This can take a minute. Keep this page open.', 'قد يستغرق ذلك دقيقة. أبقِ هذه الصفحة مفتوحة.'));
        setTimeout(check, tries < 8 ? 2500 : 8000);
      } else {
        state('wait', T('Payment not confirmed yet', 'لم يتم تأكيد الدفع بعد'), T('Please ask our team to check it.', 'يرجى الطلب من فريقنا التحقق منه.'));
      }
    });
  })();
})();
