#!/usr/bin/env python3
"""Builds the Saudi-wide SEO pages of the Black Arrow 3D blog (EN + AR):
city guides (scripts/seo_posts_cities.py), buying guides
(scripts/seo_posts_buying.py) and local/education guides
(scripts/seo_posts_local.py), and lists them on both blog index pages.

Uses the same page builders as the troubleshooting guides
(scripts/build_3d_troubleshooting_guides.py). Safe to re-run: pages are
rewritten and index cards are only added once.

Afterwards run: python scripts/generate_3d_static.py && python scripts/update_sitemap_3d.py

Usage: python scripts/build_3d_seo_posts.py [slug ...]   (slugs: build only those posts)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_3d_troubleshooting_guides as guides  # noqa: E402
import generate_3d_blog_ar as ar_blog  # noqa: E402

# (module, publish date). seo_posts_products: filament and product posts added 2026-10-22.
MODULES = [('seo_posts_cities', '2026-10-15'), ('seo_posts_buying', '2026-10-15'), ('seo_posts_local', '2026-10-15'),
           ('seo_posts_products', '2026-10-22'), ('seo_posts_bambu_filament', '2026-11-01'),
           ('seo_posts_kingroon', '2026-11-04'), ('seo_posts_bambu_h3c', '2026-11-04'),
           ('seo_posts_refresh_2026_11', '2026-11-09'), ('seo_posts_refresh_2026_11b', '2026-11-10')]


def load_posts():
    posts = []
    for name, date in MODULES:
        try:
            mod = __import__(name)
        except ImportError:
            print('skipped (not written yet):', name)
            continue
        for p in mod.POSTS:
            p.setdefault('date', date)
        posts += mod.POSTS
    return posts


def main():
    posts = load_posts()
    if sys.argv[1:]:
        posts = [p for p in posts if p['slug'] in sys.argv[1:]]
        assert posts, 'no post with that slug'
    for p in posts:
        for lang in ('en', 'ar'):
            for key in ('headline', 'title', 'desc', 'lead'):
                assert '"' not in p[lang][key], (p['slug'], lang, key)
    for p in posts:
        guides.DATE = p['date']
        guides.build_en(p)
        a = p['ar']
        ar_blog.SEO_TITLES[p['slug']] = a['title']
        ar_blog.build_post(p['slug'], {
            'meta_description': a['desc'], 'headline': a['headline'],
            'meta_line': a['meta_line'], 'lead': a['lead'], 'body': a['body'],
        })
    # Newest first on the index pages: cities last so buying guides lead.
    guides.GUIDES = list(reversed(posts))
    print('pages built:', len(posts), 'x EN + AR')
    print('index cards added: EN', guides.add_cards(os.path.join(guides.BLOG, 'index.html'), 'en'),
          '| AR', guides.add_cards(os.path.join(guides.AR_BLOG, 'index.html'), 'ar'))


if __name__ == '__main__':
    main()
