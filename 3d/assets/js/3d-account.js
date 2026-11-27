(function () {
  'use strict';

  /* Supabase's own anti-abuse cooldown (not a site bug) returns a raw
     message like "For security purposes, you can only request this
     after 43 seconds." if the same form is submitted twice in a row
     (e.g. a double-click, or retrying immediately after a typo). Two
     things caused this to bite real visitors: (1) no submit button was
     ever disabled while a request was in flight, so a double-click or
     slow network fired signUp()/signIn() twice, and the second call is
     what actually gets rate-limited; (2) the raw Supabase string was
     shown as-is, reading like a broken/scary error instead of "wait a
     moment". Fixed below by guarding every form against a second
     submit while one is already running, and by turning the rate-limit
     message into a plain countdown instead of technical text. */

  function isRateLimitMessage(message) {
    return /security purposes|rate limit|too many requests/i.test(message || '');
  }

  function secondsFromMessage(message) {
    var m = (message || '').match(/(\d+)\s*second/);
    return m ? parseInt(m[1], 10) : 30;
  }

  function t(key, fallback) {
    var I = window.BlackArrow3DI18n;
    var v = I && I.t ? I.t(key) : '';
    return v && v !== key ? v : fallback;
  }

  // The account system answers in technical English ("Invalid login credentials"); customers
  // get a plain message in their language that says what to do next.
  function friendlyMessage(message) {
    if (/invalid login credentials/i.test(message)) return t('account_err_invalid', 'The email or password is not correct. Check both and try again. New here? Choose Create Account. Forgot your password? Use Forgot password below.');
    if (/email not confirmed/i.test(message)) return t('account_err_unconfirmed', 'Please confirm your email first: open the link we emailed you (check your Junk or Spam folder too).');
    if (/already registered|already exists/i.test(message)) return t('account_err_exists', 'An account with this email already exists. Sign in instead, or use Forgot password.');
    if (/password should be at least|weak password/i.test(message)) return t('account_err_password_short', 'Please choose a password of at least 6 characters.');
    if (/invalid email|unable to validate email/i.test(message)) return t('account_err_email', 'Please enter a valid email address.');
    return message;
  }

  function showError(errEl, error) {
    var message = (error && error.message) || t('account_err_generic', 'Something went wrong. Please try again.');
    // The confirmation / reset email couldn't be sent (the email service's hourly limit).
    // Waiting 30 seconds doesn't help, so say what does.
    if ((error && error.code === 'over_email_send_rate_limit') || /email rate limit/i.test(message)) {
      var ar = document.documentElement.lang === 'ar';
      errEl.textContent = ar
        ? 'لم نتمكن من إرسال بريد التأكيد الآن بسبب ضغط مؤقت. يرجى المحاولة بعد قليل، أو راسلنا عبر واتساب على ‎+966 56 022 4715 وسننشئ حسابك.'
        : "We couldn't send your confirmation email right now (our email service is busy). Please try again a little later, or message us on WhatsApp at +966 56 022 4715 and we'll set up your account.";
      errEl.hidden = false;
      return;
    }
    if (!isRateLimitMessage(message)) {
      errEl.textContent = friendlyMessage(message);
      errEl.hidden = false;
      return;
    }
    var secs = secondsFromMessage(message);
    errEl.hidden = false;
    (function tick() {
      errEl.textContent = 'Please wait ' + secs + 's before trying again — this is a short security cooldown, not a problem with your account.';
      secs -= 1;
      if (secs >= 0) { setTimeout(tick, 1000); } else { errEl.hidden = true; }
    })();
  }

  /* The account system can only send a few emails per hour for the WHOLE site, so a customer
     pressing "Create Account", "resend" or "Forgot password" again and again would use them up for
     everyone. This browser therefore sends at most one email per address every 10 minutes, and at
     most 3 emails per hour in total. (Stored in this browser only; the email service's own limit
     still applies on top.) */
  var MAIL_KEY = 'b3d_mail_sent_v1';
  var MAIL_SAME_ADDRESS_MS = 10 * 60 * 1000;
  var MAIL_PER_HOUR = 3;

  function mailLog() {
    try {
      var log = JSON.parse(localStorage.getItem(MAIL_KEY) || '[]');
      var cutoff = Date.now() - 60 * 60 * 1000;
      return Array.isArray(log) ? log.filter(function (e) { return e && e.at > cutoff; }) : [];
    } catch (e) { return []; }
  }

  function recordMailSent(email) {
    var log = mailLog();
    log.push({ email: String(email || '').trim().toLowerCase(), at: Date.now() });
    try { localStorage.setItem(MAIL_KEY, JSON.stringify(log)); } catch (e) {}
  }

  // Returns a message to show instead of sending, or '' when an email may be sent.
  function mailBlockedMessage(email) {
    var ar = document.documentElement.lang === 'ar';
    var addr = String(email || '').trim().toLowerCase();
    var log = mailLog();
    var now = Date.now();
    var last = log.filter(function (e) { return e.email === addr; }).pop();
    if (last && now - last.at < MAIL_SAME_ADDRESS_MS) {
      var mins = Math.max(1, Math.ceil((MAIL_SAME_ADDRESS_MS - (now - last.at)) / 60000));
      return ar
        ? 'أرسلنا رسالة إلى هذا البريد قبل قليل. يرجى التحقق من صندوق الوارد ومجلد Junk أو Spam (قد تستغرق بضع دقائق). يمكنك طلب رسالة جديدة بعد ' + mins + ' دقيقة.'
        : 'We already sent an email to this address a few minutes ago. Please check your inbox and the Junk or Spam folder (it can take a few minutes). You can ask for another one in ' + mins + ' min.';
    }
    if (log.length >= MAIL_PER_HOUR) {
      return ar
        ? 'تم إرسال عدة رسائل من هذا الجهاز خلال الساعة الماضية. يرجى التحقق من بريدك (ومجلد Junk أو Spam) والمحاولة لاحقًا، أو راسلنا عبر واتساب على ‎+966 56 022 4715.'
        : 'Several emails were already sent from this device in the last hour. Please check your email (and the Junk or Spam folder) and try again later, or message us on WhatsApp at +966 56 022 4715.';
    }
    return '';
  }

  /* Wraps a form's submit handler so a second submit (double-click,
     double-tap, Enter held down, slow network + impatient retry) is
     ignored outright instead of firing a second real request, and
     disables the submit button with a busy label while the request is
     in flight. `action` returns the promise from the Supabase call. */
  function guardedSubmit(form, action) {
    if (!form) return;
    var busy = false;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (busy) return;
      busy = true;
      var btn = form.querySelector('button[type="submit"]');
      var originalLabel = btn ? btn.textContent : null;
      if (btn) { btn.disabled = true; btn.textContent = '...'; }
      action().catch(function () {}).then(function () {
        busy = false;
        if (btn) { btn.disabled = false; btn.textContent = originalLabel; }
      });
    });
  }

  /* ---------- Order History, Order Tracking and Addresses (27 Nov 2026) ----------
     Orders come from /api/orders/ (api/_lib/my-orders.js): every order placed with this account's
     confirmed email, read live from the CRM, so a status or progress change made there shows here. */
  function isAr() { return document.documentElement.lang === 'ar'; }
  function L(en, ar) { return isAr() ? ar : en; }
  function esc(v) {
    return String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function money(n) {
    var v = Number(n || 0);
    return '<bdi dir="ltr">' + v.toLocaleString('en-US', { minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 }) + '</bdi> ' + L('SAR', 'ريال');
  }
  function dateOf(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    return d.toLocaleDateString(isAr() ? 'ar-SA-u-ca-gregory-nu-latn' : 'en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
  }
  function panelFor(key) {
    var h = document.querySelector('.b3d-account__panel [data-i18n="' + key + '"]');
    return h ? h.closest('.b3d-account__panel') : null;
  }
  function setBody(panel, html) {
    if (!panel) return;
    var h2 = panel.querySelector('h2');
    panel.innerHTML = '';
    if (h2) panel.appendChild(h2);
    var box = document.createElement('div');
    box.innerHTML = html;
    panel.appendChild(box);
  }

  // Where an order is, as one step on the tracker (0-based) and a short label.
  var PROGRESS = {
    'Order received': [1, 'Confirmed', 'تم التأكيد'],
    'Packed': [2, 'Packed', 'تم التغليف'],
    'Ready for delivery': [2, 'Ready for delivery', 'جاهز للتوصيل'],
    'Dispatched': [3, 'On the way', 'في الطريق'],
    'Delivered': [4, 'Delivered', 'تم التوصيل'],
    'Completed': [4, 'Completed', 'مكتمل']
  };
  var STEPS = [['Placed', 'تم الطلب'], ['Confirmed', 'تم التأكيد'], ['Packed', 'التغليف'], ['On the way', 'في الطريق'], ['Delivered', 'تم التوصيل']];
  // Self pickup (Al Khobar pickup point): nothing travels, so the last two steps read differently.
  var PICKUP_STEPS = [['Placed', 'تم الطلب'], ['Confirmed', 'تم التأكيد'], ['Packed', 'التغليف'], ['Ready for pickup', 'جاهز للاستلام'], ['Collected', 'تم الاستلام']];
  function isPickup(o) { return /pickup/i.test(o.deliveryLabel || '') || /^cash/i.test(o.method || ''); }

  function stageOf(o) {
    if (o.status === 'rejected') return { step: -1, label: L('Cancelled', 'ملغي'), tone: 'bad' };
    if (o.status === 'pending') return { step: 0, label: L('Awaiting confirmation', 'بانتظار التأكيد'), tone: 'wait' };
    var p = PROGRESS[o.progress] || PROGRESS['Order received'];
    if (isPickup(o)) {
      if (o.progress === 'Ready for delivery' || o.progress === 'Dispatched') p = [3, 'Ready for pickup', 'جاهز للاستلام'];
      else if (p[0] >= 4) p = [4, 'Collected', 'تم الاستلام'];
    }
    return { step: p[0], label: L(p[1], p[2]), tone: p[0] >= 4 ? 'done' : 'go' };
  }
  function isActive(o) { var s = stageOf(o); return s.step >= 0 && s.step < 4; }

  function tracker(o) {
    var s = stageOf(o);
    return '<ol class="b3d-ord__track" aria-label="' + esc(L('Order progress', 'مراحل الطلب')) + '">' + (isPickup(o) ? PICKUP_STEPS : STEPS).map(function (st, i) {
      var cls = i < s.step ? 'is-done' : i === s.step ? 'is-now' : '';
      return '<li class="' + cls + '"' + (i === s.step ? ' aria-current="step"' : '') + '><span></span>' + esc(L(st[0], st[1])) + '</li>';
    }).join('') + '</ol>';
  }

  // Labels stored in the CRM are English; the Arabic page shows them in Arabic.
  function labelAr(text) {
    if (!isAr() || !text) return text;
    var t = String(text);
    var MAP = [
      [/^Regular shipping/i, 'الشحن العادي'], [/^Standard shipping/i, 'الشحن العادي'], [/^Fast shipping/i, 'الشحن السريع'],
      [/^Self pickup/i, 'الاستلام من المتجر'], [/^Bank transfer/i, 'تحويل بنكي'], [/^Cash at pickup/i, 'نقداً عند الاستلام'],
      [/^Card \/ mada \/ Apple Pay/i, 'بطاقة / مدى / Apple Pay'], [/^Card/i, 'بطاقة'], [/^Apple Pay/i, 'Apple Pay'],
      [/^Tabby/i, 'تابي'], [/^Tamara/i, 'تمارا']
    ];
    for (var i = 0; i < MAP.length; i++) {
      if (MAP[i][0].test(t)) return MAP[i][1] + (/\(Free\)/i.test(t) ? ' (مجاني)' : '');
    }
    return t;
  }

  function itemName(l) { return (isAr() && l.nameAr) ? l.nameAr : l.name; }

  function lineRows(o) {
    return '<ul class="b3d-ord__lines">' + o.lines.map(function (l) {
      var img = l.image ? '<img src="' + esc(l.image) + '" alt="" loading="lazy" width="56" height="56">' : '<span class="b3d-ord__noimg"></span>';
      var name = esc(itemName(l)) + (l.variant ? '<small>' + esc(l.variant) + '</small>' : '');
      return '<li>' + img + '<span class="b3d-ord__lname">' + (l.url ? '<a href="' + esc((isAr() ? '/3d/ar' : '/3d') + l.url.slice(3)) + '">' + name + '</a>' : name) + '</span>'
        + '<span class="b3d-ord__lqty">' + l.qty + ' × ' + money(l.price) + '</span></li>';
    }).join('') + '</ul>';
  }

  function totals(o) {
    var rows = [[L('Items', 'المنتجات'), money(o.itemsTotal)]];
    if (o.discount) rows.push([L('Discount', 'الخصم'), '−' + money(o.discount)]);
    rows.push([esc(labelAr(o.deliveryLabel)) || L('Delivery', 'التوصيل'), o.delivery ? money(o.delivery) : L('Free', 'مجاني')]);
    if (o.fee) rows.push([L('Pay-later fee', 'رسوم الدفع اللاحق'), money(o.fee)]);
    return '<dl class="b3d-ord__totals">' + rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + r[1] + '</dd></div>'; }).join('')
      + '<div class="is-total"><dt>' + L('Total', 'الإجمالي') + '</dt><dd>' + money(o.total) + '</dd></div></dl>';
  }

  function payLine(o) {
    var paid = o.paid ? '<span class="b3d-ord__pill is-done">' + L('Paid', 'مدفوع') + '</span>'
      : (o.status === 'rejected' ? '' : '<span class="b3d-ord__pill is-wait">' + (/^cash/i.test(o.method || '') ? L('Pay at pickup', 'الدفع عند الاستلام') : L('Awaiting payment', 'بانتظار الدفع')) + '</span>');
    return '<p class="b3d-ord__pay">' + esc(labelAr(o.method)) + ' ' + paid
      + (o.invoiceUrl ? ' · <a href="' + esc(o.invoiceUrl) + '" target="_blank" rel="noopener">' + L('View invoice', 'عرض الفاتورة') + (o.invoiceNumber ? ' ' + esc(o.invoiceNumber) : '') + '</a>' : '') + '</p>';
  }

  function head(o) {
    var s = stageOf(o);
    var count = o.lines.reduce(function (a, l) { return a + l.qty; }, 0);
    return '<span class="b3d-ord__ref"><bdi dir="ltr">#' + esc(o.ref) + '</bdi></span>'
      + '<span class="b3d-ord__date">' + esc(dateOf(o.date)) + ' · ' + count + ' ' + L(count === 1 ? 'item' : 'items', count === 1 ? 'منتج' : 'منتجات') + '</span>'
      + '<span class="b3d-ord__pill is-' + s.tone + '">' + esc(s.label) + '</span>'
      + '<span class="b3d-ord__sum">' + money(o.total) + '</span>';
  }

  function orderBody(o) {
    return lineRows(o) + totals(o) + payLine(o)
      + (o.status === 'rejected' && o.reason ? '<p class="b3d-ord__reason">' + L('Reason: ', 'السبب: ') + esc(o.reason) + '</p>' : '');
  }

  function renderOrders(data, user) {
    var hist = panelFor('account_order_history');
    var track = panelFor('account_order_tracking');
    var help = '<p class="b3d-ord__help">' + L('Showing orders placed with ', 'تظهر هنا الطلبات المسجّلة بالبريد ') + '<bdi>' + esc(user.email) + '</bdi>. '
      + L('Ordered with a different email? Message us on WhatsApp at ', 'طلبت ببريد آخر؟ راسلنا عبر واتساب على ')
      + '<a href="https://wa.me/966560224715" target="_blank" rel="noopener"><bdi dir="ltr">+966 56 022 4715</bdi></a>.</p>';
    if (data.needsVerify) {
      var v = '<p>' + L('Confirm your email address to see your orders here (open the link we emailed you).', 'أكّد بريدك الإلكتروني لتظهر طلباتك هنا (افتح الرابط الذي أرسلناه إليك).') + '</p>';
      setBody(hist, v); setBody(track, v);
      return;
    }
    var orders = data.orders || [];
    if (!orders.length) {
      setBody(hist, '<p>' + L('No orders yet.', 'لا توجد طلبات بعد.') + '</p><p><a class="btn btn-primary" href="' + (isAr() ? '/3d/ar/shop/' : '/3d/shop/') + '">' + L('Start shopping', 'ابدأ التسوق') + '</a></p>' + help);
      setBody(track, '<p>' + L('Nothing to track yet.', 'لا يوجد ما يمكن تتبعه بعد.') + '</p>');
      return;
    }
    var active = orders.filter(isActive);
    setBody(track, active.length
      ? active.map(function (o) {
          return '<div class="b3d-ord b3d-ord--track"><div class="b3d-ord__head">' + head(o) + '</div>' + tracker(o)
            + '<p class="b3d-ord__next">' + nextText(o) + '</p></div>';
        }).join('')
      : '<p>' + L('No orders on the way right now. Past orders are in your order history.', 'لا توجد طلبات قيد التوصيل حالياً. طلباتك السابقة في سجل الطلبات.') + '</p>');
    setBody(hist, orders.map(function (o, i) {
      return '<details class="b3d-ord"' + (i === 0 ? ' open' : '') + '><summary class="b3d-ord__head">' + head(o) + '</summary>' + orderBody(o) + '</details>';
    }).join('') + help);
  }

  function nextText(o) {
    if (o.status === 'pending') {
      return /bank/i.test(o.method) && !o.paid
        ? L('We have your order. Please complete your bank transfer if you have not yet; we will email you when your order is confirmed.', 'استلمنا طلبك. يرجى إتمام التحويل البنكي إن لم تكن أتممته، وسنراسلك بالبريد عند تأكيد الطلب.')
        : L('We have your order and will email you when it is confirmed.', 'استلمنا طلبك، وسنراسلك بالبريد عند تأكيده.');
    }
    var s = stageOf(o).step;
    if (s === 1) return L('Confirmed. We are preparing your order.', 'تم التأكيد، ونجهّز طلبك الآن.');
    if (isPickup(o)) {
      if (s === 2) return L("Packed. We'll message you when it's ready to collect from our Al Khobar pickup point.", 'تم تغليف طلبك، وسنراسلك عندما يكون جاهزاً للاستلام من نقطة الاستلام في الخبر.');
      return L('Ready to collect from our Al Khobar pickup point.', 'طلبك جاهز للاستلام من نقطة الاستلام في الخبر.');
    }
    if (s === 2) return L('Packed and getting ready to ship.', 'تم تغليف طلبك وهو جاهز للشحن.');
    return L('On the way to you.', 'طلبك في الطريق إليك.');
  }

  function loadOrders(user) {
    var hist = panelFor('account_order_history');
    var track = panelFor('account_order_tracking');
    var loading = '<p class="b3d-ord__help">' + L('Loading your orders…', 'جارٍ تحميل طلباتك…') + '</p>';
    setBody(hist, loading); setBody(track, loading);
    window.BlackArrow3DAuth.getAccessToken().then(function (token) {
      if (!token) throw new Error('no_token');
      return fetch('/api/orders/', { headers: { Authorization: 'Bearer ' + token }, cache: 'no-store' });
    }).then(function (r) {
      if (!r.ok) throw new Error('http_' + r.status);
      return r.json();
    }).then(function (data) {
      renderOrders(data, user);
    }).catch(function () {
      var msg = '<p>' + L("We couldn't load your orders just now. Please refresh the page, or ask us on WhatsApp at ", 'تعذّر تحميل طلباتك الآن. حدّث الصفحة، أو اسألنا عبر واتساب على ')
        + '<a href="https://wa.me/966560224715" target="_blank" rel="noopener"><bdi dir="ltr">+966 56 022 4715</bdi></a>.</p>';
      setBody(hist, msg); setBody(track, msg);
    });
  }

  // The delivery address saved at checkout ("Save this information for next time").
  function renderAddress(addr) {
    var panel = panelFor('account_addresses');
    if (!panel || !addr || typeof addr !== 'object') return;
    var name = [addr.first_name, addr.last_name].filter(Boolean).join(' ');
    var street = [addr.national_address, addr.building, addr.apartment].filter(Boolean).join(', ')
      || [addr.bh_flat, addr.bh_building, addr.bh_road, addr.bh_block].filter(Boolean).join(', ');
    var city = [addr.city, addr.postal_code].filter(Boolean).join(' ');
    var phone = addr.phone || addr.phone_sa || '';
    var lines = [name, street, city].filter(Boolean).map(esc);
    if (phone) lines.push('<bdi dir="ltr">' + esc(phone) + '</bdi>');
    if (!street && !city) return;
    setBody(panel, '<address class="b3d-ord__addr">' + lines.join('<br>') + '</address>'
      + '<p class="b3d-ord__help">' + L('Saved from your last checkout. To change it, edit the details at checkout and keep "Save this information for next time" ticked.',
        'محفوظ من آخر طلب. لتغييره عدّل البيانات عند إتمام الطلب مع إبقاء خيار "حفظ هذه المعلومات للمرة القادمة" مفعّلاً.') + '</p>');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var notConfigured = document.getElementById('b3d-auth-notconfigured');
    var signedOut = document.getElementById('b3d-auth-signedout');
    var signedIn = document.getElementById('b3d-auth-signedin');
    var newpassForm = document.getElementById('b3d-newpass-form');

    if (!window.BlackArrow3DAuth || !window.BlackArrow3DAuth.isConfigured()) {
      notConfigured.hidden = false;
      return;
    }

    // Supabase sends the visitor back here with #type=recovery in the URL
    // after they click a password-reset email link. Show the "set a new
    // password" form instead of the normal sign-in/sign-up screen.
    var isRecovery = location.hash.indexOf('type=recovery') !== -1;

    var currentUser = null;

    window.BlackArrow3DAuth.init(function (ok) {
      if (!ok) {
        // Sign-in is set up, so this is a connection problem (the sign-in library did not load).
        notConfigured.removeAttribute('data-i18n');
        notConfigured.textContent = document.documentElement.lang === 'ar'
          ? 'تعذّر تحميل تسجيل الدخول. تحقق من اتصالك بالإنترنت ثم حدّث الصفحة.'
          : "Sign-in couldn't load. Check your internet connection and refresh the page.";
        notConfigured.hidden = false;
        return;
      }

      window.BlackArrow3DAuth.onAuthChange(function (user) {
        currentUser = user;
        if (isRecovery) {
          signedOut.hidden = true;
          signedIn.hidden = true;
          newpassForm.hidden = false;
          return;
        }
        if (user) {
          signedOut.hidden = true;
          signedIn.hidden = false;
          document.getElementById('b3d-account-email').textContent = user.email;

          var verifyNotice = document.getElementById('b3d-verify-notice');
          if (verifyNotice) verifyNotice.hidden = !!user.email_confirmed_at;

          var savedPanel = document.getElementById('b3d-saved-products-panel');
          if (savedPanel && window.BlackArrow3D) window.BlackArrow3D.renderWishlistPanel(savedPanel);

          loadOrders(user);

          // Only for the approved admin account: a shortcut to the review approval page.
          window.BlackArrow3DAuth.reviewAdminInfo().then(function (info) {
            var panels = document.querySelector('.b3d-account__panels');
            var old = document.getElementById('b3d-admin-panel');
            if (old) old.remove();
            if (!info.isAdmin || !panels) return;
            var panel = document.createElement('div');
            panel.className = 'b3d-account__panel';
            panel.id = 'b3d-admin-panel';
            panel.innerHTML = '<h2>Admin: review approval</h2><p>' +
              (info.pending === 0 ? 'No reviews are waiting for approval.' :
                info.pending + (info.pending === 1 ? ' review is' : ' reviews are') + ' waiting for approval.') +
              '</p><p style="margin-top:12px;"><a class="btn btn-primary" href="/3d/review-admin/">Open review approval</a></p>' +
              '<div class="b3d-admin-links" style="margin-top:18px;padding-top:16px;border-top:1px solid rgba(245,158,11,.2);">' +
              '<p style="margin-bottom:10px;">Send a customer the review link:</p>' +
              '<div class="b3d-admin-link-row"><span>English</span><code>https://www.blackarrowksa.com/3d/reviews/</code><button type="button" class="btn btn-outline" data-copy-link="https://www.blackarrowksa.com/3d/reviews/">Copy link</button></div>' +
              '<div class="b3d-admin-link-row"><span>Arabic</span><code>https://www.blackarrowksa.com/3d/ar/reviews/</code><button type="button" class="btn btn-outline" data-copy-link="https://www.blackarrowksa.com/3d/ar/reviews/">Copy link</button></div>' +
              '</div>';
            panels.insertBefore(panel, panels.firstChild);
            panel.querySelectorAll('[data-copy-link]').forEach(function (btn) {
              btn.addEventListener('click', function () {
                var url = btn.getAttribute('data-copy-link');
                var done = function () { var old = btn.textContent; btn.textContent = 'Copied!'; setTimeout(function () { btn.textContent = old; }, 1800); };
                if (navigator.clipboard && navigator.clipboard.writeText) {
                  navigator.clipboard.writeText(url).then(done).catch(function () { window.prompt('Copy this link:', url); });
                } else { window.prompt('Copy this link:', url); }
              });
            });
          });

          window.BlackArrow3DAuth.getProfile(user.id).then(function (profile) {
            if (!profile) return;
            var nameField = document.getElementById('details-name');
            var phoneField = document.getElementById('details-phone');
            if (nameField && profile.name) nameField.value = profile.name;
            if (phoneField && profile.phone) phoneField.value = profile.phone;
            renderAddress(profile.last_address);
          });
        } else {
          signedOut.hidden = false;
          signedIn.hidden = true;
        }
      });

      var tabs = document.querySelectorAll('[data-auth-tab]');
      var signinForm = document.getElementById('b3d-signin-form');
      var signupForm = document.getElementById('b3d-signup-form');
      var resetForm = document.getElementById('b3d-reset-form');
      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          tabs.forEach(function (t) { t.setAttribute('aria-pressed', 'false'); });
          tab.setAttribute('aria-pressed', 'true');
          var isSignin = tab.getAttribute('data-auth-tab') === 'signin';
          signinForm.hidden = !isSignin;
          signupForm.hidden = isSignin;
          resetForm.hidden = true;
        });
      });

      guardedSubmit(signinForm, function () {
        var err = document.getElementById('signin-error');
        err.hidden = true;
        return window.BlackArrow3DAuth.signIn(
          document.getElementById('signin-email').value,
          document.getElementById('signin-password').value
        ).catch(function (error) { showError(err, error); throw error; });
      });

      // Date of birth: 1920 up to 10 years ago (the same range the rewards server accepts).
      var dobInput = document.getElementById('signup-dob');
      if (dobInput) {
        var maxDob = new Date();
        maxDob.setFullYear(maxDob.getFullYear() - 10);
        dobInput.max = maxDob.toISOString().slice(0, 10);
      }
      var tr = function (key, fallback) {
        var I = window.BlackArrow3DI18n;
        var v = I && I.t ? I.t(key) : '';
        return v && v !== key ? v : fallback;
      };

      guardedSubmit(signupForm, function () {
        var err = document.getElementById('signup-error');
        var success = document.getElementById('signup-success');
        err.hidden = true;
        success.hidden = true;
        var phone = document.getElementById('signup-phone').value.trim();
        var dob = dobInput ? dobInput.value : '';
        if (!window.BlackArrow3DAuth.validPhone(phone)) {
          err.textContent = tr('account_phone_invalid', 'Please enter a Saudi mobile number (05XXXXXXXX), or a number from another country with its country code, e.g. +973 3XXX XXXX.');
          err.hidden = false;
          return Promise.reject(new Error('phone'));
        }
        if (!dob || (dobInput.min && dob < dobInput.min) || (dobInput.max && dob > dobInput.max)) {
          err.textContent = tr('account_dob_invalid', 'Please enter your date of birth.');
          err.hidden = false;
          return Promise.reject(new Error('dob'));
        }
        var signupEmail = document.getElementById('signup-email').value;
        var blocked = mailBlockedMessage(signupEmail);
        if (blocked) {
          err.textContent = blocked;
          err.hidden = false;
          return Promise.reject(new Error('mail_guard'));
        }
        return window.BlackArrow3DAuth.signUp(
          signupEmail,
          document.getElementById('signup-password').value,
          {
            name: document.getElementById('signup-name').value.trim(),
            phone: phone,
            dob: dob
          }
        ).then(function (res) {
          // Email confirmation is on by default: a successful signUp() call
          // returns a user but no session until they click the confirmation
          // link, so the page would otherwise just sit there looking broken.
          var user = res && res.data && res.data.user;
          var session = res && res.data && res.data.session;
          if (user && !session) {
            recordMailSent(signupEmail);
            signupForm.reset();
            success.hidden = false;
          }
        }).catch(function (error) { showError(err, error); throw error; });
      });

      // "Didn't get the confirmation email?": resend it to the address typed in Sign In.
      var resendLink = document.getElementById('b3d-resend-link');
      if (resendLink) {
        resendLink.addEventListener('click', function () {
          var err = document.getElementById('signin-error');
          var msg = document.getElementById('resend-msg');
          var email = (document.getElementById('signin-email').value || '').trim();
          err.hidden = true;
          msg.hidden = true;
          if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            err.textContent = t('account_resend_need_email', 'Type your email address above first, then tap this again.');
            err.hidden = false;
            return;
          }
          var blocked = mailBlockedMessage(email);
          if (blocked) {
            err.textContent = blocked;
            err.hidden = false;
            return;
          }
          resendLink.disabled = true;
          window.BlackArrow3DAuth.resendConfirmation(email).then(function () {
            recordMailSent(email);
            msg.textContent = t('account_resend_done', 'If an account is waiting for confirmation, we have emailed a new link. Check your inbox and the Junk or Spam folder.');
            msg.hidden = false;
          }).catch(function (error) { showError(err, error); }).then(function () { resendLink.disabled = false; });
        });
      }

      var forgotLink = document.getElementById('b3d-forgot-link');
      if (forgotLink) {
        forgotLink.addEventListener('click', function () {
          signinForm.hidden = true;
          signupForm.hidden = true;
          resetForm.hidden = false;
        });
      }
      var resetCancel = document.getElementById('b3d-reset-cancel');
      if (resetCancel) {
        resetCancel.addEventListener('click', function () {
          resetForm.hidden = true;
          signinForm.hidden = false;
        });
      }
      guardedSubmit(resetForm, function () {
        var err = document.getElementById('reset-error');
        var success = document.getElementById('reset-success');
        err.hidden = true;
        success.hidden = true;
        var resetEmail = document.getElementById('reset-email').value;
        var blocked = mailBlockedMessage(resetEmail);
        if (blocked) {
          err.textContent = blocked;
          err.hidden = false;
          return Promise.resolve();
        }
        return window.BlackArrow3DAuth.resetPassword(resetEmail).then(function () {
          recordMailSent(resetEmail);
          success.hidden = false;
        }).catch(function (error) { showError(err, error); throw error; });
      });

      guardedSubmit(newpassForm, function () {
        var err = document.getElementById('newpass-error');
        err.hidden = true;
        return window.BlackArrow3DAuth.updatePassword(document.getElementById('newpass-password').value).then(function () {
          location.hash = '';
          location.reload();
        }).catch(function (error) { showError(err, error); throw error; });
      });

      var detailsForm = document.getElementById('b3d-details-form');
      guardedSubmit(detailsForm, function () {
        if (!currentUser) return Promise.resolve();
        var detailsPhone = document.getElementById('details-phone');
        if (detailsPhone.value.trim() && !window.BlackArrow3DAuth.validPhone(detailsPhone.value)) {
          detailsPhone.setCustomValidity(t('account_phone_invalid', 'Please enter a Saudi mobile number (05XXXXXXXX), or a number from another country with its country code, e.g. +973 3XXX XXXX.'));
          detailsPhone.reportValidity();
          detailsPhone.addEventListener('input', function () { detailsPhone.setCustomValidity(''); }, { once: true });
          return Promise.resolve();
        }
        return window.BlackArrow3DAuth.saveProfile(currentUser.id, {
          name: document.getElementById('details-name').value,
          phone: document.getElementById('details-phone').value
        }).then(function () {
          var success = document.getElementById('details-success');
          if (success) {
            success.hidden = false;
            setTimeout(function () { success.hidden = true; }, 2500);
          }
        });
      });

      document.getElementById('b3d-signout-btn').addEventListener('click', function () {
        window.BlackArrow3DAuth.signOut();
      });
    });
  });
})();
