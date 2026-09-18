/* Black Arrow 3D — EmailJS config, used only to send the CUSTOMER their own
   order-confirmation email at checkout (the site-owner notification already
   works today via Web3Forms and needs no change).

   EmailJS is a free service (200 emails/month on the free plan) that can send
   templated email straight from browser JS with no backend server — the same
   constraint this static site already has for Web3Forms/Supabase. Until the
   three values below are filled in, checkout keeps working exactly as before
   (order still reaches Black Arrow by email) — it just skips sending the
   customer's confirmation copy instead of erroring.

   One-time setup (free, ~5 minutes, do this yourself since it needs your own
   inbox to connect):
   1. Create a free account at https://www.emailjs.com/ and verify it.
   2. Email Services -> Add New Service -> connect the inbox that should send
      these emails (e.g. info@blackarrowksa.com via Gmail or SMTP). Copy the
      "Service ID" it gives you.
   3. Email Templates -> Create New Template. Use these variables in the
      template body (EmailJS inserts them automatically):
        {{to_email}}       - customer's email (recipient)
        {{to_name}}        - customer's full name
        {{order_summary}}  - itemized list of what they ordered
        {{shipping_method}}
        {{payment_method}}
        {{order_total}}    - grand total incl. shipping, in SAR
      Set the template's "To email" field to {{to_email}}.
      Copy the "Template ID".
   4. Account -> General -> copy your "Public Key".
   5. Paste all three below and it starts working immediately, no deploy step
      beyond saving this file. */
window.BLACK_ARROW_EMAILJS_CONFIG = {
  publicKey: 'DN3sB2Ge_A6IXCu_f',
  serviceId: 'service_2rpw1y5',
  templateId: 'template_hopo6zf'
};
