-- Black Arrow 3D: sequential order IDs (BAV-3D-5001, BAV-3D-5002, ...).
-- Run once in the Supabase dashboard -> SQL editor. Safe to re-run.
--
-- The counter itself is never exposed to the website; the site can only call
-- next_order_id(), which atomically bumps the sequence and hands back the
-- next formatted id. Two checkouts racing can't both get the same number.

create sequence if not exists public.order_id_seq start with 5001;

create or replace function public.next_order_id()
returns text language sql security definer set search_path = public as $$
  select 'BAV-3D-' || nextval('public.order_id_seq')::text;
$$;

grant execute on function public.next_order_id() to anon, authenticated;

-- Check the next number that will be handed out (does NOT consume it):
--   select last_value + 1 from public.order_id_seq;
