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
      button: 'Ask Black Arrow AI',
      title: 'Black Arrow AI Assistant',
      intro: "Hi! I'm the Black Arrow AI Assistant. Ask me about our EV charging, UPS, lighting, firefighting, HVAC, electrical, hospital, or aviation lighting solutions — or tell me what you need and I'll help get you a quote.",
      placeholder: 'Type your message…',
      send: 'Send',
      whatsappCta: 'Continue on WhatsApp',
      error: 'Something went wrong. Please try again or message us on WhatsApp.',
      referencePrefix: 'Reference',
      close: 'Close chat',
    },
    ar: {
      button: 'اسأل بلاك أرو AI',
      title: 'مساعد بلاك أرو الذكي',
      intro: 'مرحبًا! أنا مساعد بلاك أرو الذكي. اسألني عن حلول شحن السيارات الكهربائية، أنظمة UPS، الإضاءة، مكافحة الحريق، التكييف، الكهرباء، حلول المستشفيات، أو إضاءة المطارات — أو أخبرني بما تحتاجه وسأساعدك في الحصول على عرض سعر.',
      placeholder: 'اكتب رسالتك…',
      send: 'إرسال',
      whatsappCta: 'المتابعة عبر واتساب',
      error: 'حدث خطأ ما. يرجى المحاولة مرة أخرى أو التواصل معنا عبر واتساب.',
      referencePrefix: 'الرقم المرجعي',
      close: 'إغلاق المحادثة',
    },
  }[lang];

  function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .ba-ai-launcher {
        position: fixed;
        ${isRtl ? 'left' : 'right'}: 20px;
        bottom: 20px;
        z-index: 9998;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 18px 12px 14px;
        border-radius: 999px;
        border: none;
        background: #0f0e0b;
        color: #f1ede2;
        font: 600 14px/1 -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
      }
      .ba-ai-launcher:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(0,0,0,0.3); }
      .ba-ai-launcher svg { width: 20px; height: 20px; flex-shrink: 0; }
      .ba-ai-launcher[hidden] { display: none; }

      .ba-ai-panel {
        position: fixed;
        ${isRtl ? 'left' : 'right'}: 20px;
        bottom: 20px;
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
        padding: 16px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
      }
      .ba-ai-header h2 { margin: 0; font-size: 15px; font-weight: 700; }
      .ba-ai-header button {
        background: none;
        border: none;
        color: #f1ede2;
        cursor: pointer;
        font-size: 20px;
        line-height: 1;
        padding: 4px;
        opacity: 0.8;
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
      .ba-ai-typing { align-self: ${isRtl ? 'flex-end' : 'flex-start'}; color: #8a8578; font-size: 12px; padding: 0 4px; }
    `;
    document.head.appendChild(style);
  }

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    if (attrs) for (const k in attrs) node.setAttribute(k, attrs[k]);
    (children || []).forEach((c) => node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c));
    return node;
  }

  function buildWidget() {
    const launcher = el('button', { class: 'ba-ai-launcher', type: 'button', 'aria-label': STRINGS.button }, [
      (function () {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('viewBox', '0 0 24 24');
        svg.setAttribute('fill', 'none');
        svg.setAttribute('stroke', 'currentColor');
        svg.setAttribute('stroke-width', '2');
        svg.setAttribute('stroke-linecap', 'round');
        svg.setAttribute('stroke-linejoin', 'round');
        svg.setAttribute('aria-hidden', 'true');
        svg.innerHTML = '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>';
        return svg;
      })(),
      el('span', null, [STRINGS.button]),
    ]);

    const messages = el('div', { class: 'ba-ai-messages', role: 'log', 'aria-live': 'polite' }, []);
    const textarea = el('textarea', { rows: '1', placeholder: STRINGS.placeholder, 'aria-label': STRINGS.placeholder });
    const sendBtn = el('button', { type: 'button' }, [STRINGS.send]);
    const closeBtn = el('button', { type: 'button', 'aria-label': STRINGS.close }, ['×']);

    const panel = el('div', { class: 'ba-ai-panel', hidden: 'hidden', role: 'dialog', 'aria-label': STRINGS.title }, [
      el('div', { class: 'ba-ai-header' }, [el('h2', null, [STRINGS.title]), closeBtn]),
      messages,
      el('div', { class: 'ba-ai-inputrow' }, [textarea, sendBtn]),
    ]);

    document.body.appendChild(launcher);
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
    }

    function addWhatsappLink(url) {
      const link = el('a', { class: 'ba-ai-whatsapp', href: url, target: '_blank', rel: 'noopener' }, [STRINGS.whatsappCta]);
      messages.appendChild(link);
      messages.scrollTop = messages.scrollHeight;
    }

    let opened = false;
    function openPanel() {
      panel.hidden = false;
      launcher.hidden = true;
      if (!opened) {
        opened = true;
        addMessage(STRINGS.intro, 'assistant');
      }
      textarea.focus();
    }
    function closePanel() {
      panel.hidden = true;
      launcher.hidden = false;
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

      const typing = el('div', { class: 'ba-ai-typing' }, ['…']);
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
