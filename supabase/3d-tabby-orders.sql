-- Black Arrow 3D: orders paid through Tabby (pay in 4).
-- Run once in the Supabase dashboard -> SQL editor. Safe to re-run.
--
-- RLS is enabled with no policies, so browsers cannot read or write this table.
-- Only the server (service role key) can.

create table if not exists public.tabby_orders (
  order_ref          text primary key,
  status             text not null default 'pending' check (status in ('pending', 'paid', 'failed')),
  amount_cents       integer not null check (amount_cents > 0),
  currency           text not null default 'SAR',
  items              jsonb not null,
  tabby_payment_id   text,
  created_at         timestamptz not null default now(),
  paid_at            timestamptz
);

alter table public.tabby_orders enable row level security;
