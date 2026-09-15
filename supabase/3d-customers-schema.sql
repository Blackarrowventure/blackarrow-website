-- Black Arrow 3D — customers table (the CRM record backing account sign-up).
-- Run this once in the Supabase SQL Editor (Project → SQL Editor → New query)
-- for project https://iorbuqljfxifgtrdniwq.supabase.co, then Run.
--
-- This does NOT touch anything else in the project — it only creates this
-- one table and its access rules. Safe to re-run: the IF NOT EXISTS guards
-- mean running it twice won't error or duplicate anything.

create table if not exists public.customers (
  id uuid primary key references auth.users(id) on delete cascade,
  name text,
  email text,
  phone text,
  source text default '3d-site',
  created_at timestamptz not null default now()
);

alter table public.customers enable row level security;

-- Each signed-in customer can see, create, and update only their own row —
-- never anyone else's. (You, as the project owner, can still see every row
-- from the Supabase dashboard's Table Editor, which bypasses RLS.)
drop policy if exists "customers_select_own" on public.customers;
create policy "customers_select_own"
  on public.customers for select
  using (auth.uid() = id);

drop policy if exists "customers_insert_own" on public.customers;
create policy "customers_insert_own"
  on public.customers for insert
  with check (auth.uid() = id);

drop policy if exists "customers_update_own" on public.customers;
create policy "customers_update_own"
  on public.customers for update
  using (auth.uid() = id);
