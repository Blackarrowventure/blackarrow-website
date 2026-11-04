-- Black Arrow 3D security fixes, 4 Nov 2026.
-- Run once in the WEBSITE Supabase project (zhqrluepxyejdyceyabu) -> SQL editor. Safe to re-run.
--
-- 1. Rewards cards: one website account per phone. rewards_phone is stored normalized
--    (9665XXXXXXXX) and unique, so a second account can't claim a member's card by typing
--    their phone number. (The server, api/_lib/rewards.js, checks this too.)
-- 2. Flood limits on the public forms: reviews, back-in-stock requests, review photo uploads,
--    and (via rate_hit, called by the server) bank-transfer orders.

-- ---------------------------------------------------------------- 1. rewards phone
create or replace function public.normalize_phone_sa(p text) returns text
language sql immutable set search_path = public as $$
  -- Same rule as normalizePhone() in api/_lib/rewards.js and the CRM's bav3d_normalize_phone().
  select case
    when d = '' then null
    when d like '00%' then substr(d, 3)
    when d like '05%' and length(d) = 10 then '966' || substr(d, 2)
    when d like '5%' and length(d) = 9 then '966' || d
    else d end
  from (select regexp_replace(coalesce(p, ''), '[^0-9]', '', 'g') as d) x;
$$;

update public.customers
   set rewards_phone = public.normalize_phone_sa(rewards_phone)
 where rewards_phone is not null
   and rewards_phone is distinct from public.normalize_phone_sa(rewards_phone);

do $$
begin
  if exists (select 1 from public.customers where rewards_phone is not null
             group by rewards_phone having count(*) > 1) then
    raise notice 'Some phones are linked to more than one account - see the list below. Unique rule NOT added yet.';
  else
    create unique index if not exists customers_rewards_phone_unique
      on public.customers (rewards_phone) where rewards_phone is not null;
  end if;
end $$;

-- ---------------------------------------------------------------- 2. flood limits
create table if not exists public.rate_hits (
  key text not null,
  at  timestamptz not null default now()
);
create index if not exists rate_hits_key_at on public.rate_hits (key, at);
alter table public.rate_hits enable row level security;   -- no policies: server/functions only
revoke all on public.rate_hits from anon, authenticated;

-- True and counts one hit if p_key had fewer than p_max hits in p_window; false otherwise.
create or replace function public.rate_hit(p_key text, p_max integer, p_window interval)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if random() < 0.02 then delete from public.rate_hits where at < now() - interval '2 days'; end if;
  if (select count(*) from public.rate_hits where key = p_key and at > now() - p_window) >= p_max then
    return false;
  end if;
  insert into public.rate_hits (key) values (p_key);
  return true;
end $$;
revoke all on function public.rate_hit(text, integer, interval) from public, anon, authenticated;
grant execute on function public.rate_hit(text, integer, interval) to service_role;

-- The visitor's IP for calls made straight from the browser (Cloudflare's header first).
create or replace function public.request_ip() returns text
language sql stable set search_path = public as $$
  select coalesce(
    nullif(btrim(current_setting('request.headers', true)::json->>'cf-connecting-ip'), ''),
    nullif(btrim(split_part(current_setting('request.headers', true)::json->>'x-forwarded-for', ',', 1)), ''),
    'unknown');
$$;

-- Reviews: 3 per visitor per day, 50 per day in total (each one emails you).
create or replace function public.submit_review(
  p_name text, p_rating integer, p_comment text, p_lang text, p_photos text[] default '{}'
) returns jsonb language plpgsql security definer set search_path = public as $$
declare n text := btrim(coalesce(p_name, ''));
        c text := btrim(coalesce(p_comment, ''));
        ph text[] := coalesce(p_photos, '{}');
        f text;
begin
  if char_length(n) not between 2 and 40 then
    return jsonb_build_object('ok', false, 'reason', 'name'); end if;
  if p_rating is null or p_rating not between 1 and 5 then
    return jsonb_build_object('ok', false, 'reason', 'rating'); end if;
  if char_length(c) not between 10 and 600 then
    return jsonb_build_object('ok', false, 'reason', 'comment'); end if;
  if p_lang not in ('en', 'ar') then
    return jsonb_build_object('ok', false, 'reason', 'invalid'); end if;
  if coalesce(array_length(ph, 1), 0) > 3 then
    return jsonb_build_object('ok', false, 'reason', 'photos'); end if;
  foreach f in array ph loop
    if f !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.jpg$' then
      return jsonb_build_object('ok', false, 'reason', 'photos'); end if;
  end loop;
  if exists (select 1 from public.reviews where name = n and comment = c) then
    return jsonb_build_object('ok', true); end if;
  if not public.rate_hit('review:all', 50, interval '1 day')
     or not public.rate_hit('review:' || public.request_ip(), 3, interval '1 day') then
    return jsonb_build_object('ok', false, 'reason', 'limit'); end if;
  insert into public.reviews (product_id, name, rating, comment, lang, photos)
  values ('service', n, p_rating, c, p_lang, ph);
  return jsonb_build_object('ok', true);
end $$;
grant execute on function public.submit_review(text, integer, text, text, text[]) to anon, authenticated;

-- Back-in-stock requests: 10 per visitor per hour, 200 per day in total (each one emails sales@).
create or replace function public.submit_restock_alert(
  p_product_id text, p_variant text, p_contact text, p_lang text default 'en'
) returns jsonb language plpgsql security definer set search_path = public as $$
declare pid text := btrim(coalesce(p_product_id, ''));
        v   text := left(btrim(coalesce(p_variant, '')), 80);
        c   text := lower(btrim(coalesce(p_contact, '')));
begin
  if pid !~ '^[a-z0-9-]{2,80}$' then
    return jsonb_build_object('ok', false, 'reason', 'product'); end if;
  if c !~ '^9665[0-9]{8}$' and c !~ '^[^\s@]+@[^\s@]+\.[^\s@]{2,}$' then
    return jsonb_build_object('ok', false, 'reason', 'contact'); end if;
  if char_length(c) > 80 then
    return jsonb_build_object('ok', false, 'reason', 'contact'); end if;
  -- at most 20 requests per contact per day
  if (select count(*) from public.restock_alerts
      where contact = c and created_at > now() - interval '1 day') >= 20 then
    return jsonb_build_object('ok', false, 'reason', 'limit'); end if;
  if not public.rate_hit('restock:all', 200, interval '1 day')
     or not public.rate_hit('restock:' || public.request_ip(), 10, interval '1 hour') then
    return jsonb_build_object('ok', false, 'reason', 'limit'); end if;
  insert into public.restock_alerts (product_id, variant, contact, lang)
  values (pid, v, c, case when p_lang = 'ar' then 'ar' else 'en' end)
  on conflict (product_id, variant, contact) do update set notified = false, created_at = now();
  return jsonb_build_object('ok', true);
end $$;
revoke all on function public.submit_restock_alert(text, text, text, text) from public;
grant execute on function public.submit_restock_alert(text, text, text, text) to anon, authenticated;

-- Review photos: only the site's own file names (<uuid>.jpg), and at most 60 uploads an hour
-- in total. (The count runs as the function owner: the bucket has no read policy for visitors.)
create or replace function public.review_photo_uploads_last_hour() returns integer
language sql stable security definer set search_path = public, storage as $$
  select count(*)::int from storage.objects
   where bucket_id = 'review-photos' and created_at > now() - interval '1 hour';
$$;
revoke all on function public.review_photo_uploads_last_hour() from public;
grant execute on function public.review_photo_uploads_last_hour() to anon, authenticated;

drop policy if exists "review photos upload" on storage.objects;
create policy "review photos upload" on storage.objects
  for insert to anon, authenticated with check (
    bucket_id = 'review-photos'
    and name ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.jpg$'
    and public.review_photo_uploads_last_hour() < 60
  );

-- ---------------------------------------------------------------- check
-- Phones linked to more than one account (should be empty; if not, tell Claude which account keeps it):
select rewards_phone, count(*) as accounts, array_agg(id) as account_ids
  from public.customers where rewards_phone is not null
 group by rewards_phone having count(*) > 1;
