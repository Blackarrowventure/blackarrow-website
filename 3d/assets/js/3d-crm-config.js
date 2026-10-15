/* Black Arrow 3D — Supabase project config for Arrowhead Rewards, dedicated
   to the BAV CRM's project (separate from the website's own customer
   accounts in 3d-supabase-config.js). The key below is a publishable key —
   safe to ship in client-side code by design, same as the website's own
   config; real access control lives in the database's Row Level Security
   and the narrow security-definer RPCs it exposes (bav3d_loyalty_*), not in
   keeping this key secret. */
window.BLACK_ARROW_CRM_CONFIG = {
  url: 'https://iorbuqljfxifgtrdniwq.supabase.co',
  anonKey: 'sb_publishable_aXFaAU9OVKWqbWns7K4T_g_mGtC1Olz'
};
