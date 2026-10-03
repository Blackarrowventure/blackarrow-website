-- Black Arrow 3D: card orders created through Paymob.
-- Run once in the Supabase dashboard -> SQL editor. Safe to re-run.
--
-- RLS is enabled with no policies, so anon and logged-in browser users cannot
-- read or write this table. Only the server (service role key) can.

create table if not exists public.card_orders (
  order_ref            text primary key,
  status               text not null default 'pending' check (status in ('pending', 'paid', 'failed')),
  amount_cents         integer not null check (amount_cents > 0),
  currency             text not null default 'SAR',
  items                jsonb not null,
  billing              jsonb not null,
  paymob_intention_id  text,
  paymob_transaction_id bigint,
  created_at           timestamptz not null default now(),
  paid_at              timestamptz
);

alter table public.card_orders enable row level security;
