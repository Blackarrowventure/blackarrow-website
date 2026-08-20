/* ==============================================
   BLACK ARROW VENTURE
   save-contact.js — vCard download for /contacts/* cards
   ==============================================

   This used to be an inline <script> plus an onclick="" attribute on each
   of the five contact pages. Both forms are blocked by the Content-Security
   -Policy, and an inline handler cannot be allowed back without
   'unsafe-inline', which would re-open the exact hole the policy exists to
   close. So the behaviour moved here and the per-person details moved onto
   data-* attributes of the button.

   One file now serves all five people. Previously the same 40 lines were
   copy-pasted five times with only the name and number changed, which is
   how Zayn's card ended up carrying Adnan's phone number once already.
   ============================================== */

'use strict';

(function () {
  /* vCard 3.0 wants CRLF line endings. Most parsers tolerate bare \n, but
     Outlook is the notable one that does not, and it is exactly what a
     Saudi contractor's client is likely to be using. */
  function buildVCard(d) {
    return [
      'BEGIN:VCARD',
      'VERSION:3.0',
      'FN:' + d.fn,
      'N:' + d.n,
      'TITLE:' + d.title,
      'ORG:' + (d.org || 'Black Arrow Venture'),
      'TEL;TYPE=WORK;TYPE=VOICE:' + d.tel,
      'EMAIL;TYPE=WORK:' + d.email,
      'URL;TYPE=WORK:' + (d.url || 'https://www.blackarrowksa.com'),
      'END:VCARD'
    ].join('\r\n');
  }

  function download(btn) {
    const d = btn.dataset;
    if (!d.fn || !d.tel) return;          // nothing useful to save

    const blob = new Blob([buildVCard(d)], { type: 'text/vcard;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = d.file || (d.fn.replace(/\s+/g, '-') + '.vcf');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    /* Revoking immediately can cancel the download in some browsers before
       it has read the blob, so give it a beat. */
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);

    /* The card has a hidden confirmation strip. Without this the button
       looks like it did nothing, because a .vcf download is silent on
       desktop. */
    const msg = document.getElementById('successMsg');
    if (msg) {
      msg.classList.add('show');
      setTimeout(function () { msg.classList.remove('show'); }, 3000);
    }
  }

  document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-vcard]');
    if (btn) {
      e.preventDefault();
      download(btn);
    }
  });
})();
