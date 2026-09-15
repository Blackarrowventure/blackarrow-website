/* Black Arrow 3D — Supabase project config (this doubles as the CRM: it
   holds both account sign-in and the "customers" table). The key below is
   a publishable key — safe to ship in client-side code by design (same
   idea as a Firebase web config or a Stripe publishable key); real access
   control lives in the database's Row Level Security policies, not in
   keeping this key secret. */
window.BLACK_ARROW_SUPABASE_CONFIG = {
  url: 'https://iorbuqljfxifgtrdniwq.supabase.co',
  anonKey: 'sb_publishable_aXFaAU9OVKWqbWns7K4T_g_mGtC1Olz'
};
