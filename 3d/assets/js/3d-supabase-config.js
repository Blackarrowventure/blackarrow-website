/* Black Arrow 3D — Supabase project config, dedicated to the website's own
   customer accounts (separate from the BAV CRM's project). The key below is
   a publishable key — safe to ship in client-side code by design (same
   idea as a Firebase web config or a Stripe publishable key); real access
   control lives in the database's Row Level Security policies, not in
   keeping this key secret. */
window.BLACK_ARROW_SUPABASE_CONFIG = {
  url: 'https://zhqrluepxyejdyceyabu.supabase.co',
  anonKey: 'sb_publishable_YwJkqnHZlq_VIMSIxpJCZg_X2Qq6mhY'
};
