/* ==============================================
   BLACK ARROW VENTURE
   "Ask Black Arrow AI" chat widget — ai-assistant.js

   Self-contained: injects its own <style> and DOM into every page (there is
   no shared template across the 16 HTML files, so a single new <script>
   tag per page is the only edit needed anywhere). Talks only to the
   ai-assistant Supabase Edge Function - never to Postgrest directly, so no
   database credential of any kind lives in this file. The anon/publishable
   key below is Supabase's public client key by design (safe to ship in
   browser code, the same way every Supabase web app ships it) and grants
   nothing on its own; the Edge Function is the real trust boundary.

   Language follows the page itself (document.documentElement.lang), same
   as the rest of this static, build-step-free site - no in-widget switch.
   ============================================== */
'use strict';

(function () {
  const SUPABASE_FUNCTION_URL = 'https://iorbuqljfxifgtrdniwq.supabase.co/functions/v1/ai-assistant';
  const SUPABASE_ANON_KEY = 'sb_publishable_aXFaAU9OVKWqbWns7K4T_g_mGtC1Olz';
  const WHATSAPP_NUMBER = '966560224715';
  const SESSION_KEY = 'ba_ai_session_id';

  const lang = document.documentElement.lang === 'ar' ? 'ar' : 'en';
  const isRtl = document.documentElement.dir === 'rtl';

  const STRINGS = {
    en: {
      button: 'Ask Arrow AI',
      tooltip: 'How can we assist you today?',
      title: 'Arrow AI',
      subtitle: 'Black Arrow Project Assistant',
      online: 'Online now',
      intro: "Hi! I'm Arrow AI 👋 Ask me about our EV charging, UPS, lighting, firefighting, HVAC, electrical, or hospital solutions — or tell me what you need and I'll help get you a quote.",
      placeholder: 'Type your message…',
      send: 'Send',
      whatsappCta: 'Continue on WhatsApp',
      error: 'Something went wrong. Please try again or message us on WhatsApp.',
      referencePrefix: 'Reference',
      close: 'Close chat',
    },
    ar: {
      button: 'اسأل Arrow AI',
      tooltip: 'كيف يمكننا مساعدتك اليوم؟',
      title: 'Arrow AI',
      subtitle: 'مساعد مشاريع بلاك أرو',
      online: 'متصل الآن',
      intro: 'مرحبًا! أنا Arrow AI 👋 اسألني عن حلول شحن السيارات الكهربائية، أنظمة UPS، الإضاءة، مكافحة الحريق، التكييف، الكهرباء، أو حلول المستشفيات — أو أخبرني بما تحتاجه وسأساعدك في الحصول على عرض سعر.',
      placeholder: 'اكتب رسالتك…',
      send: 'إرسال',
      whatsappCta: 'المتابعة عبر واتساب',
      error: 'حدث خطأ ما. يرجى المحاولة مرة أخرى أو التواصل معنا عبر واتساب.',
      referencePrefix: 'الرقم المرجعي',
      close: 'إغلاق المحادثة',
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

      /* "Thinking" state: a gold ring sweeps around the avatar while a reply
         is being generated - conic-gradient makes this a single rotating
         pseudo-element, no extra image frames needed. */
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
      .ba-ai-inputrow textarea {
        flex: 1;
        resize: none;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 9px 12px;
        font: inherit;
        max-height: 80px;
      }
      .ba-ai-inputrow textarea:focus { outline: 2px solid #c9a24a; outline-offset: 1px; }
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

  function buildWidget() {
    const launcher = el('button', { class: 'ba-ai-launcher', type: 'button', 'aria-label': STRINGS.button }, [
      avatarImg(),
      el('span', { class: 'ba-ai-status-dot', 'aria-hidden': 'true' }, []),
    ]);
    const tooltip = el('span', { class: 'ba-ai-tooltip', 'aria-hidden': 'true' }, [STRINGS.tooltip]);
    const launcherWrap = el('div', { class: 'ba-ai-launcher-wrap' }, [launcher, tooltip]);

    const messages = el('div', { class: 'ba-ai-messages', role: 'log', 'aria-live': 'polite' }, []);
    const textarea = el('textarea', { rows: '1', placeholder: STRINGS.placeholder, 'aria-label': STRINGS.placeholder });
    const sendBtn = el('button', { type: 'button' }, [STRINGS.send]);
    const closeBtn = el('button', { type: 'button', 'aria-label': STRINGS.close }, ['×']);

    const headerAvatar = el('div', { class: 'ba-ai-avatar-sm' }, [avatarImg()]);
    const panel = el('div', { class: 'ba-ai-panel', hidden: 'hidden', role: 'dialog', 'aria-label': STRINGS.title }, [
      el('div', { class: 'ba-ai-header' }, [
        headerAvatar,
        el('div', { class: 'ba-ai-header-text' }, [el('h2', null, [STRINGS.title]), el('span', { class: 'ba-ai-online' }, [`● ${STRINGS.online}`])]),
        closeBtn,
      ]),
      messages,
      el('div', { class: 'ba-ai-inputrow' }, [textarea, sendBtn]),
    ]);

    document.body.appendChild(launcherWrap);
    document.body.appendChild(panel);

    let sessionId = null;
    try {
      sessionId = sessionStorage.getItem(SESSION_KEY);
    } catch {
      /* sessionStorage unavailable (private mode etc.) - conversation just won't persist across a reload */
    }

    function addMessage(text, role) {
      messages.appendChild(el('div', { class: `ba-ai-msg ${role}` }, [text]));
      messages.scrollTop = messages.scrollHeight;
      if (role === 'assistant') {
        headerAvatar.classList.remove('ba-ai-pulse');
        void headerAvatar.offsetWidth; // restart the animation on repeat replies
        headerAvatar.classList.add('ba-ai-pulse');
      }
    }

    function addWhatsappLink(url) {
      const link = el('a', { class: 'ba-ai-whatsapp', href: url, target: '_blank', rel: 'noopener' }, [STRINGS.whatsappCta]);
      messages.appendChild(link);
      messages.scrollTop = messages.scrollHeight;
    }

    let opened = false;
    function openPanel() {
      panel.hidden = false;
      launcherWrap.hidden = true;
      if (!opened) {
        opened = true;
        addMessage(STRINGS.intro, 'assistant');
      }
      textarea.focus();
    }
    function closePanel() {
      panel.hidden = true;
      launcherWrap.hidden = false;
    }

    launcher.addEventListener('click', openPanel);
    closeBtn.addEventListener('click', closePanel);

    let sending = false;
    async function sendMessage() {
      const text = textarea.value.trim();
      if (!text || sending) return;
      sending = true;
      sendBtn.disabled = true;
      textarea.value = '';
      addMessage(text, 'user');

      const typing = el('div', { class: 'ba-ai-typing-row' }, [
        el('div', { class: 'ba-ai-thinking-avatar' }, [el('div', { class: 'ba-ai-avatar-sm' }, [avatarImg()])]),
        el('div', { class: 'ba-ai-typing-dots' }, [el('i', null, []), el('i', null, []), el('i', null, [])]),
      ]);
      messages.appendChild(typing);
      messages.scrollTop = messages.scrollHeight;

      try {
        const res = await fetch(SUPABASE_FUNCTION_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', apikey: SUPABASE_ANON_KEY, Authorization: `Bearer ${SUPABASE_ANON_KEY}` },
          body: JSON.stringify({ sessionId, language: lang, message: text }),
        });
        const data = await res.json();
        typing.remove();

        if (!res.ok) {
          addMessage(data.error || STRINGS.error, 'system');
          if (data.whatsappUrl) addWhatsappLink(data.whatsappUrl);
          return;
        }

        if (data.sessionId) {
          sessionId = data.sessionId;
          try {
            sessionStorage.setItem(SESSION_KEY, sessionId);
          } catch {
            /* ignore */
          }
        }
        addMessage(data.reply, 'assistant');
        if (data.handoff && data.whatsappUrl) addWhatsappLink(data.whatsappUrl);
      } catch {
        typing.remove();
        addMessage(STRINGS.error, 'system');
      } finally {
        sending = false;
        sendBtn.disabled = false;
      }
    }

    sendBtn.addEventListener('click', sendMessage);
    textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
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
