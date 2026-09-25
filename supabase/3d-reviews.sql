-- Black Arrow 3D: customer reviews with moderation.
-- Run once in the Supabase dashboard -> SQL editor. Safe to re-run.
--
-- Reviews live ONLY in this table. Row Level Security is on and there are no
-- policies, so the website (publishable key) can never read or edit rows
-- directly. It can only call submit_review (adds a PENDING review) and
-- get_reviews (returns APPROVED reviews of one product), below.
--
-- A review is invisible on the site until you approve it (see the bottom).

create table if not exists public.reviews (
  id          bigint generated always as identity primary key,
  product_id  text        not null,              -- product slug, e.g. 'bambu-lab-a1'
  name        text        not null,              -- shown publicly
  rating      integer     not null check (rating between 1 and 5),
  comment     text        not null,              -- as the customer wrote it
  lang        text        not null check (lang in ('en', 'ar')),  -- language it was written in
  comment_en  text,                              -- optional English version (you add it)
  comment_ar  text,                              -- optional Arabic version (you add it)
  status      text        not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  created_at  timestamptz not null default now()
);

create index if not exists reviews_product_status_idx on public.reviews (product_id, status);

alter table public.reviews enable row level security;

-- Website: add a review. It always starts as 'pending'.
create or replace function public.submit_review(
  p_product text, p_name text, p_rating integer, p_comment text, p_lang text
) returns jsonb language plpgsql security definer set search_path = public as $$
declare n text := btrim(coalesce(p_name, ''));
        c text := btrim(coalesce(p_comment, ''));
begin
  if char_length(btrim(coalesce(p_product, ''))) not between 1 and 120 then
    return jsonb_build_object('ok', false, 'reason', 'invalid'); end if;
  if char_length(n) not between 2 and 40 then
    return jsonb_build_object('ok', false, 'reason', 'name'); end if;
  if p_rating is null or p_rating not between 1 and 5 then
    return jsonb_build_object('ok', false, 'reason', 'rating'); end if;
  if char_length(c) not between 10 and 600 then
    return jsonb_build_object('ok', false, 'reason', 'comment'); end if;
  if p_lang not in ('en', 'ar') then
    return jsonb_build_object('ok', false, 'reason', 'invalid'); end if;
  -- ignore an exact duplicate of a review already sent
  if exists (select 1 from public.reviews where product_id = p_product and name = n and comment = c) then
    return jsonb_build_object('ok', true); end if;
  insert into public.reviews (product_id, name, rating, comment, lang)
  values (p_product, n, p_rating, c, p_lang);
  return jsonb_build_object('ok', true);
end $$;

-- Website: approved reviews of one product, newest first.
create or replace function public.get_reviews(p_product text)
returns jsonb language sql stable security definer set search_path = public as $$
  select coalesce(jsonb_agg(r order by r.created_at desc), '[]'::jsonb)
  from (
    select name, rating, comment, lang, comment_en, comment_ar, created_at
    from public.reviews
    where product_id = p_product and status = 'approved'
    order by created_at desc
    limit 50
  ) r;
$$;

grant execute on function public.submit_review(text, text, integer, text, text) to anon, authenticated;
grant execute on function public.get_reviews(text) to anon, authenticated;

-- ---------------------------------------------------------------------------
-- HOW YOU MANAGE REVIEWS (run these in the SQL editor when needed)
--
--   See what is waiting for approval:
--     select id, product_id, name, rating, lang, comment, created_at
--     from public.reviews where status = 'pending' order by created_at;
--
--   Approve one:
--     update public.reviews set status = 'approved' where id = 1;
--
--   Reject (hide) one:
--     update public.reviews set status = 'rejected' where id = 1;
--
--   Add a translation so the review reads in both languages (optional):
--     update public.reviews set comment_en = 'Great printer, fast delivery.' where id = 1;
--     update public.reviews set comment_ar = 'طابعة ممتازة وتوصيل سريع.' where id = 2;
--   Without a translation, the review shows on both language versions of the
--   site in the language it was written in, with a small "Written in ..." tag.
-- ---------------------------------------------------------------------------
