-- Black Arrow 3D: "Notify me when it's back in stock" requests.
-- Run in the Supabase dashboard -> SQL editor, AFTER supabase/3d-reviews-admin.sql
-- (it reuses the Resend key saved in Vault there). Safe to re-run.
--
-- The website can only ADD a request (through submit_restock_alert). The table
-- has Row Level Security on and no policies, so nobody can read it from the
-- site. Read the list in the dashboard: Table Editor -> restock_alerts.
-- When an item is back, message everyone on its list, then set notified = true.

create extension if not exists pg_net;

create table if not exists public.restock_alerts (
  id          bigint generated always as identity primary key,
  product_id  text        not null,
  variant     text        not null default '',
  contact     text        not null,          -- 9665XXXXXXXX or an email address
  lang        text        not null default 'en' check (lang in ('en', 'ar')),
  notified    boolean     not null default false,
  created_at  timestamptz not null default now(),
  unique (product_id, variant, contact)
);
alter table public.restock_alerts enable row level security;

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
  -- simple flood guard: at most 20 requests per contact per day
  if (select count(*) from public.restock_alerts
      where contact = c and created_at > now() - interval '1 day') >= 20 then
    return jsonb_build_object('ok', false, 'reason', 'limit'); end if;
  insert into public.restock_alerts (product_id, variant, contact, lang)
  values (pid, v, c, case when p_lang = 'ar' then 'ar' else 'en' end)
  on conflict (product_id, variant, contact) do update set notified = false, created_at = now();
  return jsonb_build_object('ok', true);
end $$;

revoke all on function public.submit_restock_alert(text, text, text, text) from public;
grant execute on function public.submit_restock_alert(text, text, text, text) to anon, authenticated;

-- Email sales@ for every new request (uses the same Resend key as reviews).
create or replace function public.notify_restock_alert() returns trigger
language plpgsql security definer set search_path = public, extensions, vault as $$
declare k text;
begin
  select decrypted_secret into k from vault.decrypted_secrets where name = 'resend_api_key' limit 1;
  if k is null then return new; end if;
  perform net.http_post(
    url     := 'https://api.resend.com/emails',
    headers := jsonb_build_object('Authorization', 'Bearer ' || k, 'Content-Type', 'application/json'),
    body    := jsonb_build_object(
      'from',    'Black Arrow 3D <onboarding@resend.dev>',
      'to',      jsonb_build_array('sales@blackarrowksa.com'),
      'subject', 'Back-in-stock request: ' || new.product_id || case when new.variant <> '' then ' (' || new.variant || ')' else '' end,
      'text',    'A customer wants to know when this is back in stock.' || E'\n\n' ||
                 'Product: https://www.blackarrowksa.com/3d/product/' || new.product_id || '/' || E'\n' ||
                 'Option: ' || coalesce(nullif(new.variant, ''), '-') || E'\n' ||
                 'Contact: ' || new.contact || E'\n' ||
                 'Language: ' || new.lang || E'\n\n' ||
                 'Full list: Supabase -> Table Editor -> restock_alerts')
  );
  return new;
exception when others then
  return new;
end $$;

drop trigger if exists restock_alerts_notify on public.restock_alerts;
create trigger restock_alerts_notify after insert on public.restock_alerts
  for each row execute function public.notify_restock_alert();
