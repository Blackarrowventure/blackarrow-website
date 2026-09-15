-- Black Arrow 3D — adds saved-address support to the customers table.
-- Run this once in the Supabase SQL Editor (Project → SQL Editor → New query)
-- AFTER 3d-customers-schema.sql has already been run.
--
-- Lets a signed-in customer check "Save this information for next time" at
-- checkout so their delivery details prefill next visit. Existing RLS
-- policies from 3d-customers-schema.sql already cover this new column —
-- a customer can only ever read/write their own row.

alter table public.customers add column if not exists last_address jsonb;
