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
  try { apple.hidden = !(window.ApplePaySession && window.ApplePaySession.canMakePayments()); } catch (e) { apple.hidden = true; }

  form.querySelectorAll('[data-amt]').forEach(function (b) {
    b.addEventListener('click', function () { amountEl.value = b.getAttribute('data-amt'); amountEl.focus(); });
  });

  function showError(msg) { errorEl.textContent = msg; errorEl.hidden = !msg; }
  form.addEventListener('input', function () { if (!errorEl.hidden) showError(''); });

  function pay(channel, btn) {
    showError('');
    var amount = Math.round(Number(String(amountEl.value).replace(',', '.')) * 100) / 100;
    var name = form.querySelector('#ev-name').value.trim().replace(/\s+/g, ' ');
    var phone = form.querySelector('#ev-phone').value.replace(/[^\d+]/g, '');
    var email = form.querySelector('#ev-email').value.trim();
    if (!(amount >= 1 && amount <= 20000)) { amountEl.focus(); return showError(T('Enter the amount in SAR (1 to 20,000).', 'أدخل المبلغ بالريال (من 1 إلى 20,000).')); }
    if (name.length < 2) { form.querySelector('#ev-name').focus(); return showError(T('Enter your name.', 'أدخل اسمك.')); }
    if (phone.replace(/\D/g, '').length < 9) { form.querySelector('#ev-phone').focus(); return showError(T('Enter your mobile number.', 'أدخل رقم جوالك.')); }
    if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { form.querySelector('#ev-email').focus(); return showError(T('Check the email address, or leave it empty.', 'تحقق من البريد الإلكتروني أو اتركه فارغًا.')); }
    var parts = name.split(' ');
    var buttons = form.querySelectorAll('[data-ev-pay]');
    buttons.forEach(function (b) { b.disabled = true; });
    var label = btn.innerHTML;
    btn.textContent = T('Opening secure payment…', 'جارٍ فتح الدفع الآمن…');
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
    }).catch(function () {
      buttons.forEach(function (b) { b.disabled = false; });
      btn.innerHTML = label;
      showError(T('The payment could not be opened. Please try again, or pay our team directly.', 'تعذر فتح الدفع. حاول مرة أخرى أو ادفع لفريقنا مباشرة.'));
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
