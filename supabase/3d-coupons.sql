-- Black Arrow 3D: discount codes with real "use limits".
-- Run once in the Supabase dashboard -> SQL editor. Safe to re-run.
--
-- Codes live ONLY in this table. Row Level Security is on and there are no
-- policies, so the website (publishable key) can never read the list of codes;
-- it can only call check_coupon / redeem_coupon below, one code at a time.

create table if not exists public.coupons (
  code        text primary key,               -- stored UPPERCASE, e.g. 'BAV50-K7Q2'
  amount      integer not null check (amount > 0),  -- SAR off the order subtotal
  max_uses    integer not null default 1 check (max_uses > 0),
  used_count  integer not null default 0,
  min_order   integer not null default 0,     -- minimum subtotal in SAR
  expires_on  date,                           -- last valid day (null = never)
  active      boolean not null default true,
  note        text,                           -- private reminder, e.g. who it is for
  created_at  timestamptz not null default now()
);

create table if not exists public.coupon_redemptions (
  id           text primary key,
  code         text not null,
  amount       integer not null,
  redeemed_at  timestamptz not null default now()
);

alter table public.coupons enable row level security;
alter table public.coupon_redemptions enable row level security;

-- Cart page: "is this code valid for this subtotal?" (does NOT use it up)
create or replace function public.check_coupon(p_code text, p_subtotal numeric)
returns jsonb language plpgsql security definer set search_path = public as $$
declare c public.coupons;
begin
  select * into c from public.coupons where code = upper(btrim(p_code)) and active;
  if not found then return jsonb_build_object('ok', false, 'reason', 'invalid'); end if;
  if c.expires_on is not null and current_date > c.expires_on then
    return jsonb_build_object('ok', false, 'reason', 'expired'); end if;
  if c.used_count >= c.max_uses then
    return jsonb_build_object('ok', false, 'reason', 'used'); end if;
  if p_subtotal < c.min_order then
    return jsonb_build_object('ok', false, 'reason', 'min', 'min', c.min_order); end if;
  return jsonb_build_object('ok', true, 'amount', c.amount);
end $$;

-- Checkout: atomically uses one redemption. Two people racing for the last
-- use can't both win. Returns a redemption id that goes into the order email.
create or replace function public.redeem_coupon(p_code text, p_subtotal numeric)
returns jsonb language plpgsql security definer set search_path = public as $$
declare c public.coupons; rid text;
begin
  update public.coupons
     set used_count = used_count + 1
   where code = upper(btrim(p_code)) and active
     and (expires_on is null or current_date <= expires_on)
     and used_count < max_uses
     and p_subtotal >= min_order
  returning * into c;
  if not found then
    return public.check_coupon(p_code, p_subtotal);  -- explains why (never ok here)
  end if;
  rid := 'R' || upper(substr(md5(random()::text || clock_timestamp()::text), 1, 8));
  insert into public.coupon_redemptions(id, code, amount) values (rid, c.code, c.amount);
  return jsonb_build_object('ok', true, 'amount', c.amount, 'redemption', rid);
end $$;

grant execute on function public.check_coupon(text, numeric) to anon, authenticated;
grant execute on function public.redeem_coupon(text, numeric) to anon, authenticated;

-- ---- Making a code (repeat whenever you need one) -------------------------
-- insert into public.coupons (code, amount, max_uses, note)
--   values ('BAV50-K7Q2', 50, 1, 'for Ahmed');
-- Optional columns: min_order (SAR), expires_on ('2026-12-31'), max_uses (>1 = shared code)
-- Turn a code off:   update public.coupons set active = false where code = 'BAV50-K7Q2';
-- See who used what: select * from public.coupon_redemptions order by redeemed_at desc;
