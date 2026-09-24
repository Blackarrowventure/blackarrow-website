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

-- ---- Making a code: always unique, always single-use ----------------------
-- Run this in the SQL editor whenever you need a code. It invents a random,
-- unguessable code, saves it with ONE use, and shows it to you to hand over:
--
--   select public.generate_coupon(50);                       -- 50 SAR off
--   select public.generate_coupon(50, 'for Ahmed');          -- with a private note
--   select public.generate_coupon(100, 'Ramadan', 300, '2027-03-30');
--                                   -- amount, note, min order SAR, last valid day
--   select public.generate_coupon(50) from generate_series(1, 10);   -- 10 codes at once
--
-- Turn a code off:   update public.coupons set active = false where code = 'BAV-XXXXXXXX';
-- See who used what: select * from public.coupon_redemptions order by redeemed_at desc;
-- See unused codes:  select code, amount, note from public.coupons where used_count = 0 and active;

create or replace function public.generate_coupon(
  p_amount integer, p_note text default null, p_min_order integer default 0, p_expires date default null)
returns text language plpgsql security definer set search_path = public as $$
declare
  alphabet constant text := 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';  -- no 0/O/1/I/L
  new_code text; i integer;
begin
  loop
    new_code := 'BAV-';
    for i in 1..8 loop
      new_code := new_code || substr(alphabet, 1 + floor(random() * length(alphabet))::int, 1);
    end loop;
    begin
      insert into public.coupons(code, amount, max_uses, min_order, expires_on, note)
      values (new_code, p_amount, 1, coalesce(p_min_order, 0), p_expires, p_note);
      return new_code;
    exception when unique_violation then
      null;  -- extremely unlikely clash: try another code
    end;
  end loop;
end $$;

-- Only you (dashboard / service role) can mint codes - never the website.
revoke execute on function public.generate_coupon(integer, text, integer, date) from public, anon, authenticated;
