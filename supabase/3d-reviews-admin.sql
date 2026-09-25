-- Black Arrow 3D: review notifications + sign-in-protected approval.
-- Run AFTER supabase/3d-reviews.sql. Safe to re-run.
--
-- 1) Emails sales@blackarrowksa.com the moment a review is submitted (sent by the
--    database itself through Resend, so it does not depend on the customer's browser).
-- 2) Lets only the accounts listed in review_admins (signed in with a confirmed
--    email) see and approve reviews on /3d/review-admin/.
--
-- BEFORE running: replace the two placeholders marked  <<< ... >>> below.

create extension if not exists pg_net;

-- --- who may approve reviews --------------------------------------------------
create table if not exists public.review_admins (email text primary key);
alter table public.review_admins enable row level security;   -- no policies: not readable by the site

insert into public.review_admins (email) values ('sales@blackarrowksa.com')
on conflict do nothing;
-- To allow another person later:
--   insert into public.review_admins (email) values ('name@example.com');

-- Only a signed-in user whose email is CONFIRMED and listed above.
create or replace function public.is_review_admin() returns boolean
language sql stable security definer set search_path = public, auth as $$
  select exists (
    select 1
    from auth.users u
    join public.review_admins a on lower(a.email) = lower(u.email)
    where u.id = auth.uid() and u.email_confirmed_at is not null
  );
$$;

create or replace function public.admin_list_reviews(p_status text default 'pending')
returns jsonb language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_review_admin() then raise exception 'not allowed'; end if;
  return (select coalesce(jsonb_agg(r order by r.created_at desc), '[]'::jsonb)
          from (select id, name, rating, comment, lang, comment_en, comment_ar, photos, status, created_at
                from public.reviews where status = p_status
                order by created_at desc limit 100) r);
end $$;

create or replace function public.admin_set_review(
  p_id bigint, p_status text default null, p_comment_en text default null,
  p_comment_ar text default null, p_clear_photos boolean default false
) returns jsonb language plpgsql security definer set search_path = public as $$
begin
  if not public.is_review_admin() then raise exception 'not allowed'; end if;
  if p_status is not null and p_status not in ('pending', 'approved', 'rejected') then
    raise exception 'bad status'; end if;
  update public.reviews set
    status     = coalesce(p_status, status),
    comment_en = case when p_comment_en is null then comment_en else nullif(btrim(p_comment_en), '') end,
    comment_ar = case when p_comment_ar is null then comment_ar else nullif(btrim(p_comment_ar), '') end,
    photos     = case when p_clear_photos then '{}' else photos end
  where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

revoke all on function public.admin_list_reviews(text) from public;
revoke all on function public.admin_set_review(bigint, text, text, text, boolean) from public;
grant execute on function public.admin_list_reviews(text) to authenticated;
grant execute on function public.admin_set_review(bigint, text, text, text, boolean) to authenticated;

-- --- email notification -------------------------------------------------------
-- The Resend API key is kept in Supabase Vault (private), never in the website.
-- Run this ONE line once, with your real key, then delete the key from the editor:
--
--   select vault.create_secret('<<< PASTE YOUR RESEND API KEY HERE >>>', 'resend_api_key');
--
-- (If you ever need to replace it:  select vault.update_secret(id, 'new key') ... or
--  delete the old row in Vault first and create it again.)

create or replace function public.notify_new_review() returns trigger
language plpgsql security definer set search_path = public, extensions, vault as $$
declare k text;
begin
  select decrypted_secret into k from vault.decrypted_secrets where name = 'resend_api_key' limit 1;
  if k is null then return new; end if;          -- no key saved yet: just skip the email
  perform net.http_post(
    url     := 'https://api.resend.com/emails',
    headers := jsonb_build_object('Authorization', 'Bearer ' || k, 'Content-Type', 'application/json'),
    body    := jsonb_build_object(
      'from',    'Black Arrow 3D <onboarding@resend.dev>',
      'to',      jsonb_build_array('sales@blackarrowksa.com'),
      'subject', 'New review waiting: ' || new.rating || ' stars from ' || left(new.name, 40),
      'text',    'A customer left a review on Black Arrow 3D.' || E'\n\n' ||
                 'Name: ' || new.name || E'\n' ||
                 'Rating: ' || new.rating || ' / 5' || E'\n' ||
                 'Language: ' || new.lang || E'\n' ||
                 'Photos: ' || coalesce(array_length(new.photos, 1), 0) || E'\n\n' ||
                 left(new.comment, 600) || E'\n\n' ||
                 'Approve or reject it here: https://www.blackarrowksa.com/3d/review-admin/')
  );
  return new;
exception when others then
  return new;                                    -- an email problem must never block a review
end $$;

drop trigger if exists reviews_notify on public.reviews;
create trigger reviews_notify after insert on public.reviews
  for each row execute function public.notify_new_review();
