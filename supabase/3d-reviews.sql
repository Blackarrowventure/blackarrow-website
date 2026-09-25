-- Black Arrow 3D: customer reviews of the service (with photos) and moderation.
-- Run in the Supabase dashboard -> SQL editor. Safe to re-run, and it also
-- upgrades the earlier per-product version of this file.
--
-- Reviews live ONLY in this table. Row Level Security is on and there are no
-- policies, so the website (publishable key) can never read or edit rows
-- directly. It can only call submit_review (adds a PENDING review) and
-- get_reviews (returns APPROVED reviews), below.
-- Photos go into a storage bucket; a review only shows the photos you approve
-- together with it.

create table if not exists public.reviews (
  id          bigint generated always as identity primary key,
  product_id  text        not null default 'service',   -- kept for older rows
  name        text        not null,
  rating      integer     not null check (rating between 1 and 5),
  comment     text        not null,
  lang        text        not null check (lang in ('en', 'ar')),
  comment_en  text,
  comment_ar  text,
  status      text        not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  created_at  timestamptz not null default now()
);
alter table public.reviews add column if not exists photos text[] not null default '{}';
alter table public.reviews alter column product_id set default 'service';
alter table public.reviews enable row level security;

-- Older per-product functions are replaced by the general ones below.
drop function if exists public.submit_review(text, text, integer, text, text);
drop function if exists public.get_reviews(text);

-- Website: add a review. It always starts as 'pending'.
create or replace function public.submit_review(
  p_name text, p_rating integer, p_comment text, p_lang text, p_photos text[] default '{}'
) returns jsonb language plpgsql security definer set search_path = public as $$
declare n text := btrim(coalesce(p_name, ''));
        c text := btrim(coalesce(p_comment, ''));
        ph text[] := coalesce(p_photos, '{}');
        f text;
begin
  if char_length(n) not between 2 and 40 then
    return jsonb_build_object('ok', false, 'reason', 'name'); end if;
  if p_rating is null or p_rating not between 1 and 5 then
    return jsonb_build_object('ok', false, 'reason', 'rating'); end if;
  if char_length(c) not between 10 and 600 then
    return jsonb_build_object('ok', false, 'reason', 'comment'); end if;
  if p_lang not in ('en', 'ar') then
    return jsonb_build_object('ok', false, 'reason', 'invalid'); end if;
  if coalesce(array_length(ph, 1), 0) > 3 then
    return jsonb_build_object('ok', false, 'reason', 'photos'); end if;
  foreach f in array ph loop
    if f !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.jpg$' then
      return jsonb_build_object('ok', false, 'reason', 'photos'); end if;
  end loop;
  if exists (select 1 from public.reviews where name = n and comment = c) then
    return jsonb_build_object('ok', true); end if;
  insert into public.reviews (product_id, name, rating, comment, lang, photos)
  values ('service', n, p_rating, c, p_lang, ph);
  return jsonb_build_object('ok', true);
end $$;

-- Website: approved reviews, newest first.
create or replace function public.get_reviews()
returns jsonb language sql stable security definer set search_path = public as $$
  select coalesce(jsonb_agg(r order by r.created_at desc), '[]'::jsonb)
  from (
    select name, rating, comment, lang, comment_en, comment_ar, photos, created_at
    from public.reviews
    where status = 'approved'
    order by created_at desc
    limit 50
  ) r;
$$;

grant execute on function public.submit_review(text, integer, text, text, text[]) to anon, authenticated;
grant execute on function public.get_reviews() to anon, authenticated;

-- Photo storage: JPEG only (the site converts every photo to JPEG), max 2 MB each.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('review-photos', 'review-photos', true, 2097152, array['image/jpeg'])
on conflict (id) do update
  set public = true, file_size_limit = 2097152, allowed_mime_types = array['image/jpeg'];

drop policy if exists "review photos upload" on storage.objects;
create policy "review photos upload" on storage.objects
  for insert to anon, authenticated with check (bucket_id = 'review-photos');

-- ---------------------------------------------------------------------------
-- HOW YOU MANAGE REVIEWS (run these in the SQL editor when needed)
--
--   See what is waiting for approval (photos = file names in the bucket):
--     select id, name, rating, lang, comment, photos, created_at
--     from public.reviews where status = 'pending' order by created_at;
--
--   Approve one:
--     update public.reviews set status = 'approved' where id = 1;
--
--   Reject (hide) one:
--     update public.reviews set status = 'rejected' where id = 1;
--
--   Remove a photo from a review (keep the review):
--     update public.reviews set photos = '{}' where id = 1;
--
--   Add a translation so the review reads in both languages (optional):
--     update public.reviews set comment_en = 'Great print quality, fast delivery.' where id = 1;
--     update public.reviews set comment_ar = 'جودة طباعة ممتازة وتوصيل سريع.' where id = 2;
--   Without a translation, the review shows on both language versions of the
--   site in the language it was written in, with a small "Written in ..." tag.
--
--   To look at a pending photo before approving: Supabase -> Storage ->
--   review-photos, or open  <project-url>/storage/v1/object/public/review-photos/<file-name>
-- ---------------------------------------------------------------------------
