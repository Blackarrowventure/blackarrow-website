#!/usr/bin/env python3
"""Builds the Saudi-wide SEO pages of the Black Arrow 3D blog (EN + AR):
city guides (scripts/seo_posts_cities.py), buying guides
(scripts/seo_posts_buying.py) and local/education guides
(scripts/seo_posts_local.py), and lists them on both blog index pages.

Uses the same page builders as the troubleshooting guides
(scripts/build_3d_troubleshooting_guides.py). Safe to re-run: pages are
rewritten and index cards are only added once.

Afterwards run: python scripts/generate_3d_static.py && python scripts/update_sitemap_3d.py

Usage: python scripts/build_3d_seo_posts.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_3d_troubleshooting_guides as guides  # noqa: E402
import generate_3d_blog_ar as ar_blog  # noqa: E402

MODULES = ['seo_posts_cities', 'seo_posts_buying', 'seo_posts_local']


def load_posts():
    posts = []
    for name in MODULES:
        try:
            mod = __import__(name)
        except ImportError:
            print('skipped (not written yet):', name)
            continue
        posts += mod.POSTS
    return posts


def main():
    posts = load_posts()
    for p in posts:
        for lang in ('en', 'ar'):
            for key in ('headline', 'title', 'desc', 'lead'):
                assert '"' not in p[lang][key], (p['slug'], lang, key)
    guides.DATE = '2026-10-15'
    for p in posts:
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
