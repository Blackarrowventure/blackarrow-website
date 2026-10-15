-- Black Arrow 3D: server-sent confirmation emails + Arrowhead Rewards at checkout.
-- Run once in the WEBSITE Supabase project (zhqrluepxyejdyceyabu) -> SQL editor.
-- Safe to re-run.

-- Full order details for the server's "Order CONFIRMED" emails, and markers so
-- emails and rewards spending happen exactly once per order.
alter table public.card_orders
  add column if not exists details jsonb,
  add column if not exists emails_sent_at timestamptz,
  add column if not exists rewards_redeemed_at timestamptz;

alter table public.tabby_orders
  add column if not exists details jsonb,
  add column if not exists emails_sent_at timestamptz,
  add column if not exists rewards_redeemed_at timestamptz;

-- The phone a customer's rewards card was opened with. Set once by the server
-- at enrolment, so changing the profile phone later can't open a second card
-- (and a second welcome credit) for the same account.
alter table public.customers
  add column if not exists rewards_phone text;

-- Customers can still edit their own name/phone/address from the browser, but
-- rewards_phone is ignored unless the server (service role) sets it.
create or replace function public.customers_lock_rewards_phone()
returns trigger
language plpgsql
as $$
begin
  if current_user in ('anon', 'authenticated') then
    if tg_op = 'INSERT' then
      new.rewards_phone := null;
    else
      new.rewards_phone := old.rewards_phone;
    end if;
  end if;
  return new;
end;
$$;

drop trigger if exists customers_lock_rewards_phone on public.customers;
create trigger customers_lock_rewards_phone
  before insert or update on public.customers
  for each row execute function public.customers_lock_rewards_phone();
