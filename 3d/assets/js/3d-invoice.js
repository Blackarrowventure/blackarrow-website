// Customer invoice page (/3d/invoice/?t=<signed token>). Loads the invoice from
// /api/invoice/ (api/_lib/invoice-link.js) and fills the page. "Download PDF / Print"
// opens the browser's print dialog, where "Save as PDF" makes the PDF.
(function () {
  var state = document.getElementById('state');
  var doc = document.getElementById('doc');
  var token = new URLSearchParams(location.search).get('t') || '';

  function fail(en, ar) { state.textContent = en + ' · ' + ar; }
  function set(id, text) { document.getElementById(id).textContent = text == null ? '' : String(text); }
  function money(n) { return Number(n || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function date(iso) {
    if (!iso) return '';
    var d = new Date(String(iso).length === 10 ? iso + 'T00:00:00' : iso);
    return isNaN(d) ? String(iso) : d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  }

  if (!/^[0-9a-f-]{36}\.[A-Za-z0-9_-]{32}$/.test(token)) {
    fail('This invoice link is not valid. Please use the link from your email.', 'رابط الفاتورة غير صحيح. يرجى استخدام الرابط من بريدك الإلكتروني.');
    return;
  }

  fetch('/api/invoice/?t=' + encodeURIComponent(token), { cache: 'no-store' })
    .then(function (r) { return r.json().then(function (b) { return { ok: r.ok, status: r.status, body: b }; }); })
    .then(function (res) {
      if (!res.ok) {
        if (res.status === 404) fail('We could not find this invoice. Please use the link from your email, or contact us on WhatsApp.', 'لم نعثر على هذه الفاتورة. يرجى استخدام الرابط من بريدك الإلكتروني أو التواصل معنا عبر واتساب.');
        else fail('Your invoice could not be loaded right now. Please try again in a few minutes.', 'تعذر تحميل الفاتورة الآن. يرجى المحاولة بعد دقائق.');
        return;
      }
      var inv = res.body;
      document.title = 'Invoice ' + inv.invoiceNumber + ' | Black Arrow 3D';
      set('f-number', inv.invoiceNumber);
      set('f-date', date(inv.invoiceDate));
      set('f-status', inv.status === 'Paid' ? 'Paid · مدفوعة' : inv.status);
      set('f-name', inv.customer && inv.customer.name);
      set('f-email', inv.customer && inv.customer.email);
      set('f-order', inv.orderRef);
      set('f-method', inv.paymentMethod);
      set('f-paid', inv.status === 'Paid' ? date(inv.paidDate || inv.invoiceDate) : '—');
      set('f-foot', 'Invoice ' + inv.invoiceNumber);

      var body = document.getElementById('f-items');
      (inv.items || []).forEach(function (it, i) {
        var tr = document.createElement('tr');
        [String(i + 1), it.description, String(it.quantity), money(it.unitPrice), money(it.quantity * it.unitPrice)].forEach(function (v, j) {
          var td = document.createElement('td');
          td.textContent = v;
          if (j >= 2) td.className = 'r';
          tr.appendChild(td);
        });
        body.appendChild(tr);
      });

      var sum = document.getElementById('f-sum');
      function line(label, value, total) {
        var d = document.createElement('div');
        if (total) d.className = 'total';
        var l = document.createElement('span'); l.className = 'lbl'; l.textContent = label;
        var v = document.createElement('strong'); v.textContent = value;
        d.appendChild(l); d.appendChild(v); sum.appendChild(d);
      }
      line('Subtotal (incl. VAT) · المجموع', 'SAR ' + money(inv.subtotal));
      if (inv.discount > 0) line('Discount · الخصم', '- SAR ' + money(inv.discount));
      if (inv.deliveryFee > 0) line('Delivery · التوصيل', 'SAR ' + money(inv.deliveryFee));
      if (inv.payLaterFee > 0) line('Pay-later service fee · رسوم الدفع لاحقًا', 'SAR ' + money(inv.payLaterFee));
      line('Amount before VAT · المبلغ قبل الضريبة', 'SAR ' + money(inv.taxableAmount));
      line('VAT (' + inv.vatRate + '%) · الضريبة', 'SAR ' + money(inv.vatAmount));
      line('Total · الإجمالي', 'SAR ' + money(inv.total), true);

      state.hidden = true;
      doc.hidden = false;
    })
    .catch(function () {
      fail('Your invoice could not be loaded right now. Please check your connection and try again.', 'تعذر تحميل الفاتورة الآن. تحقق من اتصالك وحاول مرة أخرى.');
    });

  document.getElementById('print').addEventListener('click', function () { window.print(); });
})();
