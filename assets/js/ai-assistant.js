/* ==============================================
   BLACK ARROW VENTURE
   "Arrow AI" enquiry bot — ai-assistant.js

   Self-contained: injects its own <style> and DOM into every page (there is
   no shared template across the 16 HTML files, so a single new <script>
   tag per page is the only edit needed anywhere).

   Deliberately NOT an LLM chatbot - a deterministic, click-driven menu
   (pick a product category, give a name + contact, optional note) that
   posts straight to the submit_website_enquiry() RPC in Supabase. No AI
   API key, no per-message cost, nothing that can ever hit a billing wall.
   The anon/publishable key below is Supabase's public client key by
   design (safe to ship in browser code) and only grants execute on that
   one function - see supabase/migrations/0050_website_enquiry_bot.sql in
   the CRM repo.

   Language follows the page itself (document.documentElement.lang), same
   as the rest of this static, build-step-free site - no in-widget switch.
   ============================================== */
'use strict';

(function () {
  const SUPABASE_URL = 'https://iorbuqljfxifgtrdniwq.supabase.co';
  const SUPABASE_ANON_KEY = 'sb_publishable_aXFaAU9OVKWqbWns7K4T_g_mGtC1Olz';
  const WHATSAPP_NUMBER = '966560224715';

  const lang = document.documentElement.lang === 'ar' ? 'ar' : 'en';
  const isRtl = document.documentElement.dir === 'rtl';

  const CATEGORIES = [
    { en: 'EV Charging Solutions', ar: 'حلول شحن السيارات الكهربائية' },
    { en: 'UPS Solutions', ar: 'أنظمة UPS' },
    { en: 'Lighting Solutions', ar: 'حلول الإضاءة' },
    { en: 'Firefighting Systems', ar: 'أنظمة مكافحة الحريق' },
    { en: 'HVAC Solutions', ar: 'حلول التكييف' },
    { en: 'Electrical & Power Distribution', ar: 'التوزيع الكهربائي وأنظمة الطاقة' },
    { en: 'Hospital Solutions', ar: 'حلول المستشفيات' },
    { en: 'General Trading', ar: 'التجارة العامة' },
    { en: 'Something else', ar: 'شيء آخر' },
  ];

  const STRINGS = {
    en: {
      button: 'Ask Arrow AI',
      tooltip: 'How can we assist you today?',
      title: 'Arrow AI',
      online: 'Online now',
      intro: "Hi! I'm Arrow AI 👋 What are you looking for?",
      talkToPerson: '💬 Talk to a person',
      askName: "Great choice! What's your name?",
      askContact: 'Thanks! Best phone number or email to reach you?',
      askNote: 'Anything else we should know (project, location, quantity, timeline)? You can skip this.',
      skip: 'Skip',
      placeholder: 'Type here…',
      send: 'Send',
      whatsappCta: 'Continue on WhatsApp',
      error: 'Something went wrong. Please try again or message us on WhatsApp.',
      close: 'Close chat',
      submitting: 'Sending your enquiry…',
      startOver: 'Start a new enquiry',
      confirmationPrefix: "You're all set! Your reference number is",
      confirmationSuffix: "Our team will reach out shortly. Want to speed things up?",
    },
    ar: {
      button: 'اسأل Arrow AI',
      tooltip: 'كيف يمكننا مساعدتك اليوم؟',
      title: 'Arrow AI',
      online: 'متصل الآن',
      intro: 'مرحبًا! أنا Arrow AI 👋 ما الذي تبحث عنه؟',
      talkToPerson: '💬 التحدث مع أحد ممثلينا',
      askName: 'اختيار رائع! ما اسمك؟',
      askContact: 'شكرًا! ما هو أفضل رقم هاتف أو بريد إلكتروني للتواصل معك؟',
      askNote: 'هل هناك أي تفاصيل أخرى (المشروع، الموقع، الكمية، الجدول الزمني)؟ يمكنك تخطي هذا.',
      skip: 'تخطي',
      placeholder: 'اكتب هنا…',
      send: 'إرسال',
      whatsappCta: 'المتابعة عبر واتساب',
      error: 'حدث خطأ ما. يرجى المحاولة مرة أخرى أو التواصل معنا عبر واتساب.',
      close: 'إغلاق المحادثة',
      submitting: 'جارٍ إرسال طلبك…',
      startOver: 'بدء طلب جديد',
      confirmationPrefix: 'تم! رقمك المرجعي هو',
      confirmationSuffix: 'سيتواصل معك فريقنا قريبًا. تريد تسريع الأمر؟',
    },
  }[lang];

  const AVATAR_SRC = '/assets/images/arrow-ai-avatar.png';

  function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
      /* Gold Badge Bot: sits above the site's floating WhatsApp button
         (.wa-float: bottom:28px, ${isRtl ? 'left' : 'right'}:28px, 60px tall - see styles.css #17),
         never on top of it. 28 (its offset) + 60 (its height) + 16 (gap) = 104. */
      .ba-ai-launcher-wrap {
        position: fixed;
        ${isRtl ? 'left' : 'right'}: 28px;
        bottom: 104px;
        z-index: 9998;
      }
      .ba-ai-launcher-wrap[hidden] { display: none; }
      .ba-ai-launcher {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        border-radius: 999px;
        border: 2px solid #D97706;
        background: linear-gradient(160deg, #2c2823, #1a1a1a 65%);
        cursor: pointer;
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.08);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        overflow: hidden;
      }
      .ba-ai-launcher:hover, .ba-ai-launcher:focus-visible { transform: translateY(-2px); box-shadow: 0 18px 36px rgba(245, 158, 11, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.08); }
      .ba-ai-avatar-img { width: 100%; height: 100%; object-fit: cover; object-position: center 30%; flex-shrink: 0; pointer-events: none; }
      .ba-ai-avatar-sm { width: 30px; height: 30px; border-radius: 999px; overflow: hidden; flex-shrink: 0; background: #1a1a1a; border: 1.5px solid #D97706; }
      .ba-ai-avatar-sm .ba-ai-avatar-img { object-position: center 25%; }
      .ba-ai-status-dot {
        position: absolute;
        top: -3px;
        ${isRtl ? 'left' : 'right'}: -3px;
        width: 13px;
        height: 13px;
        border-radius: 999px;
        background: #22c55e;
        border: 2.5px solid #f8f8f8;
        box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.6);
        animation: ba-ai-dotpulse 2.2s ease-out infinite;
        pointer-events: none;
      }
      @keyframes ba-ai-dotpulse {
        0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.6); }
        70% { box-shadow: 0 0 0 7px rgba(34, 197, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
      }
      .ba-ai-tooltip {
        position: absolute;
        bottom: calc(100% + 10px);
        ${isRtl ? 'left' : 'right'}: 0;
        background: #0f0e0b;
        color: #f1ede2;
        font: 600 12px/1.3 -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        padding: 7px 12px;
        border-radius: 8px;
        white-space: nowrap;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
        opacity: 0;
        transform: translateY(4px);
        pointer-events: none;
        transition: opacity 0.15s ease, transform 0.15s ease;
      }
      .ba-ai-tooltip::after {
        content: '';
        position: absolute;
        top: 100%;
        ${isRtl ? 'left' : 'right'}: 20px;
        border: 5px solid transparent;
        border-top-color: #0f0e0b;
      }
      .ba-ai-launcher:hover + .ba-ai-tooltip,
      .ba-ai-launcher:focus-visible + .ba-ai-tooltip {
        opacity: 1;
        transform: translateY(0);
      }

      /* "Thinking" state: a gold ring sweeps around the avatar while the
         enquiry is being submitted - conic-gradient makes this a single
         rotating pseudo-element, no extra image frames needed. */
      .ba-ai-thinking-avatar {
        position: relative;
        width: 30px;
        height: 30px;
        flex-shrink: 0;
      }
      .ba-ai-thinking-avatar::before {
        content: '';
        position: absolute;
        inset: -3px;
        border-radius: 999px;
        background: conic-gradient(from 0deg, transparent, #F59E0B 70deg, transparent 140deg);
        animation: ba-ai-spin 1s linear infinite;
      }
      .ba-ai-thinking-avatar .ba-ai-avatar-sm {
        position: absolute;
        inset: 0;
      }
      @keyframes ba-ai-spin { to { transform: rotate(360deg); } }
      .ba-ai-typing-row { align-self: ${isRtl ? 'flex-end' : 'flex-start'}; display: flex; align-items: center; gap: 8px; }
      .ba-ai-typing-dots { display: flex; gap: 4px; background: #efece4; padding: 10px 13px; border-radius: 12px; border-bottom-${isRtl ? 'right' : 'left'}-radius: 3px; }
      .ba-ai-typing-dots i { width: 6px; height: 6px; border-radius: 999px; background: #a19c8c; display: block; animation: ba-ai-dotbounce 1.1s ease-in-out infinite; font-style: normal; }
      .ba-ai-typing-dots i:nth-child(2) { animation-delay: 0.15s; }
      .ba-ai-typing-dots i:nth-child(3) { animation-delay: 0.3s; }
      @keyframes ba-ai-dotbounce { 0%, 60%, 100% { transform: translateY(0); opacity: 0.5; } 30% { transform: translateY(-4px); opacity: 1; } }

      /* Brief "talking" pulse on the header avatar when a reply lands */
      .ba-ai-pulse { animation: ba-ai-talkpulse 0.5s ease; }
      @keyframes ba-ai-talkpulse { 0% { transform: scale(1); } 40% { transform: scale(1.12); } 100% { transform: scale(1); } }

      .ba-ai-panel {
        position: fixed;
        ${isRtl ? 'left' : 'right'}: 28px;
        bottom: 28px;
        z-index: 9999;
        width: min(380px, calc(100vw - 32px));
        height: min(560px, calc(100vh - 48px));
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        font: 400 14px/1.5 -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }
      .ba-ai-panel[hidden] { display: none; }
      .ba-ai-header {
        background: #0f0e0b;
        color: #f1ede2;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }
      .ba-ai-header-text { flex: 1; min-width: 0; }
      .ba-ai-header h2 { margin: 0; font-size: 15px; font-weight: 700; }
      .ba-ai-header .ba-ai-online { font-size: 11px; color: #34D399; }
      .ba-ai-header button {
        background: none;
        border: none;
        color: #f1ede2;
        cursor: pointer;
        font-size: 20px;
        line-height: 1;
        padding: 4px;
        opacity: 0.8;
        flex-shrink: 0;
      }
      .ba-ai-header button:hover { opacity: 1; }
      .ba-ai-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        background: #faf9f6;
      }
      .ba-ai-msg {
        max-width: 85%;
        padding: 10px 13px;
        border-radius: 12px;
        white-space: pre-wrap;
        word-break: break-word;
      }
      .ba-ai-msg.user {
        align-self: ${isRtl ? 'flex-start' : 'flex-end'};
        background: #c9a24a;
        color: #1a1712;
        border-bottom-${isRtl ? 'left' : 'right'}-radius: 3px;
      }
      .ba-ai-msg.assistant {
        align-self: ${isRtl ? 'flex-end' : 'flex-start'};
        background: #efece4;
        color: #1a1712;
        border-bottom-${isRtl ? 'right' : 'left'}-radius: 3px;
      }
      .ba-ai-msg.system {
        align-self: center;
        background: transparent;
        color: #8a8578;
        font-size: 12px;
        text-align: center;
      }
      .ba-ai-options {
        align-self: ${isRtl ? 'flex-end' : 'flex-start'};
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        max-width: 100%;
      }
      .ba-ai-option-btn {
        border: 1.5px solid #D97706;
        background: #fff;
        color: #7a4a08;
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.15s ease, color 0.15s ease;
      }
      .ba-ai-option-btn:hover { background: #F59E0B; color: #1a1a1a; }
      .ba-ai-whatsapp {
        display: inline-flex;
        align-self: center;
        align-items: center;
        gap: 6px;
        margin-top: 4px;
        padding: 9px 16px;
        border-radius: 999px;
        background: #25d366;
        color: #fff;
        text-decoration: none;
        font-weight: 600;
        font-size: 13px;
      }
      .ba-ai-inputrow {
        flex-shrink: 0;
        display: flex;
        gap: 8px;
        padding: 12px;
        border-top: 1px solid #eee;
        background: #fff;
      }
      .ba-ai-inputrow input {
        flex: 1;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 9px 12px;
        font: inherit;
      }
      .ba-ai-inputrow input:focus { outline: 2px solid #c9a24a; outline-offset: 1px; }
      .ba-ai-inputrow button {
        border: none;
        border-radius: 10px;
        background: #0f0e0b;
        color: #f1ede2;
        font-weight: 600;
        padding: 0 16px;
        cursor: pointer;
      }
      .ba-ai-inputrow button:disabled { opacity: 0.5; cursor: default; }
      .ba-ai-inputrow[hidden] { display: none; }
    `;
    document.head.appendChild(style);
  }

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    if (attrs) for (const k in attrs) node.setAttribute(k, attrs[k]);
    (children || []).forEach((c) => node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c));
    return node;
  }

  function avatarImg(extraClass) {
    return el('img', { class: `ba-ai-avatar-img${extraClass ? ` ${extraClass}` : ''}`, src: AVATAR_SRC, alt: '', 'aria-hidden': 'true' });
  }

  function whatsappUrl(text) {
    return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(text)}`;
  }

  function buildWidget() {
    const launcher = el('button', { class: 'ba-ai-launcher', type: 'button', 'aria-label': STRINGS.button }, [
      avatarImg(),
      el('span', { class: 'ba-ai-status-dot', 'aria-hidden': 'true' }, []),
    ]);
    const tooltip = el('span', { class: 'ba-ai-tooltip', 'aria-hidden': 'true' }, [STRINGS.tooltip]);
    const launcherWrap = el('div', { class: 'ba-ai-launcher-wrap' }, [launcher, tooltip]);

    const messages = el('div', { class: 'ba-ai-messages', role: 'log', 'aria-live': 'polite' }, []);
    const textInput = el('input', { type: 'text', placeholder: STRINGS.placeholder, 'aria-label': STRINGS.placeholder });
    const sendBtn = el('button', { type: 'button' }, [STRINGS.send]);
    const inputRow = el('div', { class: 'ba-ai-inputrow', hidden: 'hidden' }, [textInput, sendBtn]);
    const closeBtn = el('button', { type: 'button', 'aria-label': STRINGS.close }, ['×']);

    const headerAvatar = el('div', { class: 'ba-ai-avatar-sm' }, [avatarImg()]);
    const panel = el('div', { class: 'ba-ai-panel', hidden: 'hidden', role: 'dialog', 'aria-label': STRINGS.title }, [
      el('div', { class: 'ba-ai-header' }, [
        headerAvatar,
        el('div', { class: 'ba-ai-header-text' }, [el('h2', null, [STRINGS.title]), el('span', { class: 'ba-ai-online' }, [`● ${STRINGS.online}`])]),
        closeBtn,
      ]),
      messages,
      inputRow,
    ]);

    document.body.appendChild(launcherWrap);
    document.body.appendChild(panel);

    function addMessage(text, role) {
      messages.appendChild(el('div', { class: `ba-ai-msg ${role}` }, [text]));
      messages.scrollTop = messages.scrollHeight;
      if (role === 'assistant') {
        headerAvatar.classList.remove('ba-ai-pulse');
        void headerAvatar.offsetWidth; // restart the animation on repeat replies
        headerAvatar.classList.add('ba-ai-pulse');
      }
    }

    function addOptions(options) {
      const wrap = el('div', { class: 'ba-ai-options' }, []);
      options.forEach((opt) => {
        const btn = el('button', { class: 'ba-ai-option-btn', type: 'button' }, [opt.label]);
        btn.addEventListener('click', () => {
          wrap.querySelectorAll('button').forEach((b) => (b.disabled = true));
          opt.onClick();
        });
        wrap.appendChild(btn);
      });
      messages.appendChild(wrap);
      messages.scrollTop = messages.scrollHeight;
    }

    function addWhatsappLink(url) {
      const link = el('a', { class: 'ba-ai-whatsapp', href: url, target: '_blank', rel: 'noopener' }, [STRINGS.whatsappCta]);
      messages.appendChild(link);
      messages.scrollTop = messages.scrollHeight;
    }

    const draft = { category: '', name: '', contact: '', note: '' };
    let flowState = 'menu';

    function goToWhatsapp() {
      window.open(whatsappUrl('Hi, I would like to speak with your team about your solutions.'), '_blank', 'noopener');
    }

    function showMenu() {
      flowState = 'menu';
      inputRow.hidden = true;
      addMessage(STRINGS.intro, 'assistant');
      addOptions([
        ...CATEGORIES.map((c) => ({ label: c[lang], onClick: () => selectCategory(c[lang]) })),
        { label: STRINGS.talkToPerson, onClick: goToWhatsapp },
      ]);
    }

    function selectCategory(label) {
      addMessage(label, 'user');
      draft.category = label;
      flowState = 'name';
      inputRow.hidden = false;
      addMessage(STRINGS.askName, 'assistant');
      textInput.focus();
    }

    function askContact() {
      flowState = 'contact';
      addMessage(STRINGS.askContact, 'assistant');
      textInput.focus();
    }

    function askNote() {
      flowState = 'note';
      addMessage(STRINGS.askNote, 'assistant');
      addOptions([{ label: STRINGS.skip, onClick: () => submitEnquiry() }]);
      textInput.focus();
    }

    async function submitEnquiry() {
      flowState = 'submitting';
      inputRow.hidden = true;
      const typing = el('div', { class: 'ba-ai-typing-row' }, [
        el('div', { class: 'ba-ai-thinking-avatar' }, [el('div', { class: 'ba-ai-avatar-sm' }, [avatarImg()])]),
        el('div', { class: 'ba-ai-typing-dots' }, [el('i', null, []), el('i', null, []), el('i', null, [])]),
      ]);
      messages.appendChild(typing);
      messages.scrollTop = messages.scrollHeight;

      try {
        const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/submit_website_enquiry`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', apikey: SUPABASE_ANON_KEY, Authorization: `Bearer ${SUPABASE_ANON_KEY}` },
          body: JSON.stringify({ p_language: lang, p_category: draft.category, p_name: draft.name, p_contact: draft.contact, p_note: draft.note || null }),
        });
        const data = await res.json();
        typing.remove();

        if (!res.ok) {
          const message = Array.isArray(data) ? '' : data?.message;
          addMessage(message || STRINGS.error, 'system');
          addWhatsappLink(whatsappUrl(`Hi, I'm trying to reach you about ${draft.category || 'your solutions'} but ran into an issue on the website.`));
          return;
        }

        const reference = Array.isArray(data) && data[0] ? data[0].reference_number : '';
        addMessage(`${STRINGS.confirmationPrefix} ${reference}.\n\n${STRINGS.confirmationSuffix}`, 'assistant');
        addWhatsappLink(whatsappUrl(`Hi, I'm following up on my enquiry ${reference} from Arrow AI on the website. Category: ${draft.category}.`));
        addOptions([{ label: STRINGS.startOver, onClick: resetFlow }]);
        flowState = 'done';
      } catch {
        typing.remove();
        addMessage(STRINGS.error, 'system');
        addWhatsappLink(whatsappUrl('Hi, I would like to speak with your team about your solutions.'));
      }
    }

    function resetFlow() {
      draft.category = '';
      draft.name = '';
      draft.contact = '';
      draft.note = '';
      showMenu();
    }

    let opened = false;
    function openPanel() {
      panel.hidden = false;
      launcherWrap.hidden = true;
      if (!opened) {
        opened = true;
        showMenu();
      }
      if (!inputRow.hidden) textInput.focus();
    }
    function closePanel() {
      panel.hidden = true;
      launcherWrap.hidden = false;
    }

    launcher.addEventListener('click', openPanel);
    closeBtn.addEventListener('click', closePanel);

    function handleTextSubmit() {
      const text = textInput.value.trim();
      if (!text) return;
      textInput.value = '';

      if (flowState === 'name') {
        addMessage(text, 'user');
        draft.name = text;
        askContact();
      } else if (flowState === 'contact') {
        addMessage(text, 'user');
        draft.contact = text;
        askNote();
      } else if (flowState === 'note') {
        addMessage(text, 'user');
        draft.note = text;
        submitEnquiry();
      }
    }

    sendBtn.addEventListener('click', handleTextSubmit);
    textInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleTextSubmit();
      }
    });
  }

  function init() {
    injectStyles();
    buildWidget();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
