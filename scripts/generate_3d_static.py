#!/usr/bin/env python3
"""Generates pre-rendered, crawlable static pages for the Black Arrow 3D
store: one page per product at /3d/product/<id>/ (+ /3d/ar/product/<id>/),
one landing page per category at /3d/shop/<slug>/ (+ AR), and the AR
mirrors of the homepage and shop index.

Run this after ANY change to 3d/assets/data/3d-products.json (new product,
price change, new category) — it is the only thing that keeps the
pre-rendered pages in sync with the catalog. The interactive site (cart,
compare, live shop filtering) is untouched; 3d-store.js still hydrates
every one of these pages on load exactly as before, this script only
bakes in the same content server-side so search engines see it without
running JavaScript.

Usage: python scripts/generate_3d_static.py
"""
import json
import sys
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_JSON = os.path.join(ROOT, '3d', 'assets', 'data', '3d-products.json')
I18N_JSON = os.path.join(ROOT, 'scripts', '_3d-i18n-dump.json')
PRODUCT_TEMPLATE = os.path.join(ROOT, '3d', 'product', 'index.html')
SHOP_TEMPLATE = os.path.join(ROOT, '3d', 'shop', 'index.html')
HOME_TEMPLATE = os.path.join(ROOT, '3d', 'index.html')

SITE = 'https://www.blackarrowksa.com'

CATEGORY_SLUGS = {
    '3D Printers': '3d-printers',
    'Filament': 'filament',
    'Accessories': 'accessories',
    '3D Artwork': '3d-artwork',
}
CATEGORY_NAV_KEY = {
    '3D Printers': 'nav_3d_printers',
    'Filament': 'nav_filaments',
    'Accessories': 'nav_accessories',
    '3D Artwork': 'nav_gaming_accessories',
}

with open(I18N_JSON, encoding='utf-8') as f:
    I18N = json.load(f)

with open(PRODUCTS_JSON, encoding='utf-8') as f:
    PRODUCTS = json.load(f)['products']


def T(key, lang):
    entry = I18N.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get('en') or key


def L(p, field, lang):
    if lang == 'ar' and p.get(field + '_ar'):
        return p[field + '_ar']
    return p.get(field)


def L_specs(p, lang):
    if lang == 'ar' and p.get('specs_ar'):
        return p['specs_ar']
    return p.get('specs') or []


def L_compat(p, lang):
    if lang == 'ar' and p.get('compatibility_ar'):
        return p['compatibility_ar']
    return p.get('compatibility') or []


def L_variant(v, lang):
    if lang == 'ar' and v.get('label_ar'):
        return v['label_ar']
    return v.get('label')


def category_label(cat, lang):
    key = CATEGORY_NAV_KEY.get(cat)
    return T(key, lang) if key else cat


def money(n, currency):
    return '{:,}'.format(n) + ' ' + (currency or 'SAR')


def primary_image(p):
    if p.get('cardImage'):
        return p['cardImage']
    if p.get('images'):
        return p['images'][0]
    if p.get('image'):
        return p['image']
    return None


def product_url(p, lang):
    return ('/3d/ar' if lang == 'ar' else '/3d') + '/product/' + p['id'] + '/'


def category_url(cat, lang):
    slug = CATEGORY_SLUGS.get(cat, cat.lower().replace(' ', '-'))
    return ('/3d/ar' if lang == 'ar' else '/3d') + '/shop/' + slug + '/'


def shop_url(lang):
    return ('/3d/ar' if lang == 'ar' else '/3d') + '/shop/'


def home_url(lang):
    return '/3d/ar/' if lang == 'ar' else '/3d/'


def abs_url(path):
    if not path:
        return ''
    return SITE + path if path.startswith('/') else SITE + '/' + path


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def corner_badges(p, lang):
    out = ''
    if p.get('featured'):
        out += '<span class="b3d-corner-badge b3d-corner-badge--featured">' + T('shop_featured', lang) + '</span>'
    if p.get('onSale'):
        out += '<span class="b3d-corner-badge b3d-corner-badge--sale">' + T('js_sale_badge', lang) + '</span>'
    return out


def status_badge(p, lang):
    if p.get('preorder'):
        return '<span class="b3d-stock-badge b3d-stock-badge--pre">' + T('js_pre_order', lang) + '</span>'
    if p.get('available') is False:
        return '<span class="b3d-stock-badge b3d-stock-badge--out">' + T('js_out_of_stock', lang) + '</span>'
    return ''


def variant_price_html(v, p):
    """A variant with `oldPrice` renders as an offer (old price struck through)."""
    if v.get('oldPrice') and v['oldPrice'] > v['price']:
        return ('<span class="b3d-price b3d-price--sale">' + money(v['price'], p.get('currency')) + '</span>'
                + '<span class="b3d-price-was">' + money(v['oldPrice'], p.get('currency')) + '</span>')
    return '<span class="b3d-price">' + money(v['price'], p.get('currency')) + '</span>'


def current_price(p):
    """The price a customer actually pays for the base listing."""
    if p.get('variants'):
        return min(v['price'] for v in p['variants'])
    if p.get('onSale') and p.get('salePrice') is not None:
        return p['salePrice']
    return p.get('price')


def price_block(p, lang):
    variants = p.get('variants')
    if variants:
        prices = [v['price'] for v in variants]
        lo = min(prices)
        if all(pr == lo for pr in prices):
            return variant_price_html(variants[0], p)
        return ('<span class="b3d-price-was" style="text-decoration:none;display:block;cursor:help;" title="'
                + T('js_from_tooltip', lang) + '">' + T('js_from', lang) + '</span><span class="b3d-price">'
                + money(lo, p.get('currency')) + '</span>')
    if p.get('onSale') and p.get('salePrice') is not None:
        return ('<span class="b3d-price b3d-price--sale">' + money(p['salePrice'], p.get('currency')) + '</span>'
                + '<span class="b3d-price-was">' + money(p['price'], p.get('currency')) + '</span>')
    return '<span class="b3d-price">' + money(p['price'], p.get('currency')) + '</span>'


def product_detail_html(p, lang):
    name = L(p, 'name', lang)
    desc = L(p, 'description', lang) or ''
    images = p.get('images') or ([p['image']] if p.get('image') else [])
    hero_img = p.get('cardImage') or (images[0] if images else None)
    main_visual = ('<img src="' + hero_img + '" alt="' + esc(name) + '" data-pd-main-img>') if hero_img else \
        '<div class="b3d-card__visual-placeholder">' + T('js_product_image', lang) + '</div>'

    thumbs_html = ''
    if len(images) > 1:
        thumbs = []
        for i, src in enumerate(images):
            label = T('js_view_image', lang) + ' ' + str(i + 1) + ' — ' + name
            active = ' is-active' if src == hero_img else ''
            thumbs.append('<button class="b3d-pd__thumb' + active + '" data-thumb-src="' + src
                           + '" aria-label="' + esc(label) + '"><img src="' + src + '" alt="' + esc(label) + '"></button>')
        thumbs_html = '<div class="b3d-pd__thumbs">' + ''.join(thumbs) + '</div>'

    specs_html = ''.join(
        '<tr><td>' + esc(row[0]) + '</td><td>' + esc(row[1]) + '</td></tr>' for row in L_specs(p, lang)
    )
    compat_list = L_compat(p, lang)
    compat_html = ''
    if compat_list:
        compat_html = ('<div class="b3d-pd__compat"><h2>' + T('js_compatibility_heading', lang) + '</h2><ul>'
                        + ''.join('<li>' + esc(c) + '</li>' for c in compat_list) + '</ul></div>')

    variants = p.get('variants')
    variant_selector_html = ''
    if variants:
        has_swatches = any(v.get('swatch') for v in variants)
        pills = []
        for i, v in enumerate(variants):
            if v.get('swatch'):
                pills.append('<button type="button" class="b3d-swatch" data-variant-idx="' + str(i)
                              + '" aria-pressed="' + ('true' if i == 0 else 'false') + '" title="'
                              + esc(L_variant(v, lang)) + '" style="background:' + v['swatch'] + ';"></button>')
            else:
                pills.append('<button type="button" class="b3d-quick-pill" data-variant-idx="' + str(i)
                              + '" aria-pressed="' + ('true' if i == 0 else 'false') + '">'
                              + esc(L_variant(v, lang)) + '</button>')
        variant_selector_html = ('<div class="b3d-pd__variants' + (' b3d-pd__swatches' if has_swatches else '')
                                  + '" data-pd-variants style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px;align-items:center;">'
                                  + ''.join(pills) + '</div>')
        initial_price_html = variant_price_html(variants[0], p)
    else:
        initial_price_html = price_block(p, lang)

    pd_available = p.get('available') is not False
    is_art = p.get('category') == '3D Artwork'
    compare_btn = '' if is_art else ('<button class="btn btn-outline" data-pd-compare="' + p['id'] + '">'
                                      + T('js_compare_btn', lang) + '</button>')
    add_label = T('js_pre_order', lang) if p.get('preorder') else (T('js_add_to_cart', lang) if pd_available else T('js_out_of_stock', lang))
    add_disabled = '' if (pd_available or p.get('preorder')) else 'disabled'
    status = status_badge(p, lang)
    wa_msg = 'Hello! I have a question about ' + name + '.'

    html = (
        '<div>'
        + '<div class="b3d-pd__visual' + (' b3d-pd__visual--art' if is_art else '') + '">'
        + corner_badges(p, lang) + main_visual + '</div>'
        + thumbs_html + '</div>'
        + '<div>'
        + '<div class="b3d-pd__cat">' + (esc(p['brand']) + ' &middot; ' if p.get('brand') else '') + category_label(p.get('category'), lang) + '</div>'
        + '<h1 class="b3d-pd__title">' + esc(name) + '</h1>'
        + '<div class="b3d-pd__price" data-pd-price>' + initial_price_html + '</div>'
        + variant_selector_html
        + ('<div style="margin-bottom:16px;">' + status + '</div>' if status else '')
        + '<p class="b3d-pd__desc">' + esc(desc) + '</p>'
        + '<div class="b3d-pd__actions">'
        + '<div class="b3d-qty">'
        + '<button type="button" data-pd-qty="minus" aria-label="' + T('js_qty_decrease', lang) + '">−</button>'
        + '<input type="text" readonly value="1" data-pd-qty-val aria-label="' + T('js_qty_label', lang) + '">'
        + '<button type="button" data-pd-qty="plus" aria-label="' + T('js_qty_increase', lang) + '">+</button>'
        + '</div>'
        + '<button class="btn btn-primary" data-pd-add ' + add_disabled + '>' + add_label + '</button>'
        + compare_btn
        + '<a href="/3d/cart/" class="btn btn-outline">' + T('js_view_cart', lang) + '</a>'
        + '</div>'
        + '<div class="b3d-pd__contact-actions">'
        + '<a href="https://wa.me/966560224715?text=' + wa_msg.replace(' ', '%20') + '" target="_blank" rel="noopener noreferrer" class="btn btn-outline">' + T('js_ask_whatsapp', lang) + '</a>'
        + '</div>'
        + ('<table class="b3d-spec-table"><tbody>' + specs_html + '</tbody></table>' if specs_html else '')
        + compat_html
        + ('<div class="b3d-pd__warranty"><h2>' + T('js_warranty_heading', lang) + '</h2><p>' + esc(L(p, 'warranty', lang)) + '</p></div>' if L(p, 'warranty', lang) else '')
        + '<div class="b3d-pd__shipreturn">'
        + '<div><strong>' + T('js_shipping_heading', lang) + '</strong><p>' + T('js_shipping_desc', lang) + '</p></div>'
        + '<div><strong>' + T('js_returns_heading', lang) + '</strong><p>' + T('js_returns_desc_prefix', lang)
        + ' <a href="/3d/returns/">' + T('footer_returns', lang) + '</a> ' + T('js_returns_desc_suffix', lang) + '</p></div>'
        + '</div>'
        + '</div>'
    )
    return html


I18N_ATTR_RE = re.compile(r'(<([a-zA-Z0-9]+)([^>]*?)\bdata-i18n="([a-zA-Z0-9_]+)"([^>]*)>)(.*?)(</\2>)', re.DOTALL)
I18N_PLACEHOLDER_RE = re.compile(r'data-i18n-placeholder="([a-zA-Z0-9_]+)"')


def translate_static_chrome(html, lang):
    """Bakes data-i18n text (and data-i18n-placeholder attrs) into the given
    language, exactly like 3d-i18n.js's translateStaticPage() does at
    runtime (both just set textContent from the same dictionary) — so the
    pre-rendered HTML matches what JS would produce, with nothing invented."""

    def repl(m):
        open_tag, tag, pre_attrs, key, post_attrs, _inner, close_tag = m.groups()
        val = T(key, lang)
        return open_tag + esc(val) + close_tag

    html = I18N_ATTR_RE.sub(repl, html)
    html = I18N_PLACEHOLDER_RE.sub(lambda m: 'data-i18n-placeholder="' + m.group(1) + '" placeholder="' + esc(T(m.group(1), lang)) + '"', html)
    return html


def localize_ar_hrefs(html, lang):
    """The shared nav/footer chrome (copied as-is from the EN templates)
    only has its text translated by translate_static_chrome(); its hrefs
    still point at the English home/shop/blog URLs. On AR pages, redirect
    the handful of links that DO have a real Arabic twin (home, shop
    index, shop's own ?cat= filters, blog index) to their /3d/ar/...
    equivalent. Everything without an Arabic twin yet (cart, account,
    compare, terms, returns, individual blog posts linked from outside
    their own page) is deliberately left pointing at the English-only
    page."""
    if lang != 'ar':
        return html
    html = html.replace('href="/3d/shop/?cat=', 'href="/3d/ar/shop/?cat=')
    for slug in CATEGORY_SLUGS.values():
        html = html.replace('href="/3d/shop/' + slug + '/"', 'href="/3d/ar/shop/' + slug + '/"')
    html = html.replace('href="/3d/brands/', 'href="/3d/ar/brands/')
    for _slug in ('3d-printing-service-saudi-arabia', 'shipping'):
        html = html.replace('href="/3d/' + _slug + '/"', 'href="/3d/ar/' + _slug + '/"')
    html = re.sub(r'href="/3d/product/([a-z0-9-]+)/"', r'href="/3d/ar/product/\1/"', html)
    html = html.replace('href="/3d/shop/"', 'href="/3d/ar/shop/"')
    html = html.replace('href="/3d/blog/"', 'href="/3d/ar/blog/"')
    html = html.replace('href="/3d/"', 'href="/3d/ar/"')
    return html


def set_lang_attrs(html, lang):
    html = html.replace('<html lang="en" dir="ltr">', '<html lang="ar" dir="rtl">' if lang == 'ar' else '<html lang="en" dir="ltr">')
    return html


def lang_toggle_link(html, lang, counterpart_url):
    """Replaces the JS localStorage-toggle button with a real link to the
    counterpart page — these pages have a genuine separate URL per
    language now, so the toggle should navigate there directly instead of
    reloading in place."""
    label = 'EN' if lang == 'ar' else 'AR'
    old = '<button class="navbar__pill" data-lang-toggle type="button">AR</button>'
    new = '<a class="navbar__pill" href="' + counterpart_url + '">' + label + '</a>'
    return html.replace(old, new)


def write(path, content):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def _ship(label, price, lo, hi):
    return {
        '@type': 'OfferShippingDetails',
        'shippingLabel': label,
        'shippingRate': {'@type': 'MonetaryAmount', 'value': price, 'currency': 'SAR'},
        'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'SA'},
        'deliveryTime': {'@type': 'ShippingDeliveryTime',
                         'transitTime': {'@type': 'QuantitativeValue', 'minValue': lo, 'maxValue': hi, 'unitCode': 'DAY'}},
    }


SHIPPING_DETAILS = [_ship('Standard shipping', 30, 4, 5), _ship('Fast shipping', 50, 2, 3)]


# Unused printers and filament can be returned within 7 days (see /3d/returns/);
# everything else: defects, wrong product or shipping damage within 3 days.
RETURN_7_DAY_CATEGORIES = ('3D Printers', 'Filament')


def merchant_return_policy(p):
    seven = p.get('category') in RETURN_7_DAY_CATEGORIES
    return {
        '@type': 'MerchantReturnPolicy',
        'applicableCountry': 'SA',
        'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow',
        'merchantReturnDays': 7 if seven else 3,
        'merchantReturnLink': SITE + '/3d/returns/',
        'returnMethod': 'https://schema.org/ReturnByMail',
        'returnFees': 'https://schema.org/ReturnShippingFees' if seven else 'https://schema.org/FreeReturn',
    }


def build_product_page(p, lang):
    with open(PRODUCT_TEMPLATE, encoding='utf-8') as f:
        html = f.read()

    name = L(p, 'name', lang)
    desc = L(p, 'shortDesc', lang) or L(p, 'description', lang) or ''
    url = SITE + product_url(p, lang)
    img = abs_url(primary_image(p))
    price_now = p['variants'][0]['price'] if p.get('variants') else current_price(p)
    price_txt = ('{:g}'.format(price_now) if isinstance(price_now, (int, float)) else str(price_now))
    def _fit(*cands):
        for c in cands:
            if len(c) <= 60:
                return c
        return cands[-1]
    if lang == 'ar':
        # Stable keyword-led title; the live SAR price comes from the Product markup and the page itself.
        lead = ('طابعة ' + name if p.get('category') == '3D Printers' and not name.startswith('طابعة') else name)
        seo_title = _fit(*([lead + ' في السعودية | Black Arrow 3D'] if 'السعود' not in name else []), lead + ' | Black Arrow 3D', name)
        seo_desc = (desc.rstrip('.') + '. السعر ' + price_txt + ' ريال. توصيل لكل مناطق السعودية.')
    else:
        lead = (name + ' 3D Printer' if p.get('category') == '3D Printers' else name)
        seo_title = _fit(*([lead + ' in Saudi Arabia | Black Arrow 3D'] if 'Saudi' not in name else []), lead + ' | Black Arrow 3D', name + ' | Black Arrow 3D', name)
        seo_desc = (desc.rstrip('.') + '. Price: ' + price_txt + ' SAR. Delivery across Saudi Arabia.')

    html = set_lang_attrs(html, lang)
    html = html.replace(
        '<meta name="description" content="Full specs, SAR pricing and warranty details for 3D printers, filament and accessories at Black Arrow 3D — order online with delivery across Saudi Arabia.">',
        '<meta name="description" content="' + esc(seo_desc) + '">'
    )
    html = html.replace('<meta property="og:title" content="Product — Black Arrow 3D">',
                         '<meta property="og:title" content="' + esc(seo_title) + '">')
    html = html.replace('<meta property="og:description" content="Full specs, SAR pricing and warranty details — order online with delivery across Saudi Arabia.">',
                         '<meta property="og:description" content="' + esc(seo_desc) + '">')
    html = html.replace('<meta property="og:url" content="https://www.blackarrowksa.com/3d/product/">',
                         '<meta property="og:url" content="' + url + '">')
    if img:
        html = html.replace('<meta property="og:image" content="https://www.blackarrowksa.com/assets/images/black-arrow-og.png">',
                             '<meta property="og:image" content="' + img + '">')
    html = html.replace('<link rel="canonical" href="https://www.blackarrowksa.com/3d/product/" data-pd-canonical>',
                         '<link rel="canonical" href="' + url + '">'
                         + '\n  <link rel="alternate" hreflang="en" href="' + SITE + product_url(p, "en") + '">'
                         + '\n  <link rel="alternate" hreflang="ar" href="' + SITE + product_url(p, "ar") + '">'
                         + '\n  <link rel="alternate" hreflang="x-default" href="' + SITE + product_url(p, "en") + '">')
    html = html.replace('<title>Product — Black Arrow 3D</title>', '<title>' + esc(seo_title) + '</title>')

    price_value = p['variants'][0]['price'] if p.get('variants') else current_price(p)
    offer = {
        '@type': 'Offer',
        'price': price_value,
        'priceCurrency': p.get('currency', 'SAR'),
        'availability': ('https://schema.org/OutOfStock' if p.get('available') is False
                         else 'https://schema.org/PreOrder' if p.get('preorder')
                         else 'https://schema.org/InStock'),
        'itemCondition': 'https://schema.org/NewCondition',
        'url': url,
        'hasMerchantReturnPolicy': merchant_return_policy(p),
        'shippingDetails': SHIPPING_DETAILS,
    }
    json_ld = {
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': name,
        'description': desc,
        'url': url,
        'sku': p.get('sku', p['id']),
        'brand': {'@type': 'Brand', 'name': p.get('brand', 'Black Arrow 3D')},
        'image': [abs_url(i) for i in (p.get('images') or [])],
        'offers': offer,
    }
    breadcrumb_ld = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Black Arrow Venture', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Black Arrow 3D', 'item': SITE + home_url(lang)},
            {'@type': 'ListItem', 'position': 3, 'name': T('nav_shop', lang), 'item': SITE + shop_url(lang)},
            {'@type': 'ListItem', 'position': 4, 'name': name, 'item': url},
        ],
    }
    html = html.replace('</head>',
                         '  <script type="application/ld+json">' + json.dumps(json_ld, ensure_ascii=False) + '</script>\n'
                         + '  <script type="application/ld+json">' + json.dumps(breadcrumb_ld, ensure_ascii=False) + '</script>\n'
                         + '</head>')

    html = translate_static_chrome(html, lang)
    html = localize_ar_hrefs(html, lang)
    html = lang_toggle_link(html, lang, product_url(p, 'ar' if lang == 'en' else 'en'))

    html = html.replace('<span data-b3d-crumb data-i18n="pd_crumb_default">' + T('pd_crumb_default', 'en') + '</span>',
                         '<span data-b3d-crumb>' + esc(name) + '</span>')
    html = html.replace('<span data-b3d-crumb>' + esc(T('pd_crumb_default', lang)) + '</span>',
                         '<span data-b3d-crumb>' + esc(name) + '</span>')

    detail_html = product_detail_html(p, lang)
    html = html.replace(
        '<div class="b3d-pd" data-b3d-product">',
        '<div class="b3d-pd" data-b3d-product>'
    )
    html = re.sub(
        r'<div class="b3d-pd" data-b3d-product>.*?</div>\s*\n\s*(<div data-b3d-related></div>)',
        lambda m: '<div class="b3d-pd" data-b3d-product>' + detail_html + '</div>\n\n        ' + related_products_html(p, lang),
        html, count=1, flags=re.DOTALL
    )

    out_path = os.path.join(ROOT, '3d', 'ar' if lang == 'ar' else '', 'product', p['id'], 'index.html')
    write(out_path, html)


CATEGORY_SEO = {
    '3D Printers': {
        'en': ('3D Printers in Saudi Arabia | Bambu Lab, Creality & More',
               'Buy 3D printers online in Saudi Arabia: Bambu Lab, Creality, Elegoo, Anycubic, Snapmaker and Flashforge. Prices in SAR with delivery across the Kingdom.',
               'Browse 3D printers for beginners, hobbyists, students and professionals. Every price is in Saudi riyals and orders are delivered across Saudi Arabia. Compare models by price and build volume in the shop, or read our buying guides before you choose.'),
        'ar': ('طابعات ثلاثية الأبعاد في السعودية | Black Arrow 3D',
               'اشترِ طابعات ثلاثية الأبعاد أونلاين في السعودية: Bambu Lab وCreality وElegoo وAnycubic وSnapmaker وFlashforge. الأسعار بالريال مع التوصيل لكل مناطق المملكة.',
               'تصفّح الطابعات ثلاثية الأبعاد للمبتدئين والهواة والطلاب والمحترفين. جميع الأسعار بالريال السعودي والتوصيل لكل مناطق المملكة. قارن الطرازات حسب السعر وحجم الطباعة في المتجر، أو اقرأ أدلة الشراء قبل الاختيار.'),
    },
    'Filament': {
        'en': ('3D Printer Filament in Saudi Arabia | Black Arrow 3D',
               'Buy 3D printer filament in Saudi Arabia, including PLA. Prices in SAR with delivery across the Kingdom.',
               'Filament for your 3D printer, priced in Saudi riyals and delivered across Saudi Arabia. Not sure which material to pick? Read our PLA vs PETG vs ABS filament guide.'),
        'ar': ('خيوط الطباعة ثلاثية الأبعاد في السعودية | Black Arrow 3D',
               'اشترِ خيوط الطباعة ثلاثية الأبعاد في السعودية، بما فيها PLA. الأسعار بالريال مع التوصيل لكل مناطق المملكة.',
               'خيوط لطابعتك ثلاثية الأبعاد بالريال السعودي مع التوصيل لكل مناطق المملكة. لست متأكدًا من الخامة؟ اقرأ دليلنا للمقارنة بين PLA وPETG وABS.'),
    },
    'Accessories': {
        'en': ('3D Printer Accessories in Saudi Arabia | Black Arrow 3D',
               'Buy 3D printer accessories and spare parts in Saudi Arabia: hotends, extruders and more for Bambu Lab A1 series printers. Prices in SAR.',
               'Spare parts and upgrades for your 3D printer, priced in Saudi riyals and delivered across Saudi Arabia. See our maintenance guide for when to replace a hotend or extruder.'),
        'ar': ('إكسسوارات الطابعات ثلاثية الأبعاد في السعودية | Black Arrow',
               'اشترِ إكسسوارات وقطع غيار الطابعات ثلاثية الأبعاد في السعودية: هوت إند ووحدات بثق وغيرها لطابعات Bambu Lab سلسلة A1. الأسعار بالريال.',
               'قطع غيار وترقيات لطابعتك ثلاثية الأبعاد بالريال السعودي مع التوصيل لكل مناطق المملكة. اطّلع على دليل الصيانة لمعرفة متى تستبدل الهوت إند أو وحدة البثق.'),
    },
    '3D Artwork': {
        'en': ('3D Printed Gifts & Keychains in Saudi Arabia | Black Arrow',
               'Shop 3D printed artwork, keychains and gifts made by Black Arrow in Saudi Arabia, including Saudi National Day designs. Prices in SAR.',
               'Unique 3D printed artwork, keychains, decor and gifts, printed by Black Arrow, including Saudi National Day designs. Priced in Saudi riyals and delivered across Saudi Arabia.'),
        'ar': ('هدايا ومفاتيح ثلاثية الأبعاد في السعودية | Black Arrow',
               'تسوّق أعمالًا فنية وميدالِيات مفاتيح وهدايا مطبوعة بالطباعة ثلاثية الأبعاد من Black Arrow في السعودية، بما فيها تصاميم اليوم الوطني السعودي. الأسعار بالريال.',
               'أعمال فنية وميدالِيات مفاتيح وديكور وهدايا مطبوعة بالطباعة ثلاثية الأبعاد من Black Arrow، بما فيها تصاميم اليوم الوطني السعودي. الأسعار بالريال السعودي والتوصيل لكل مناطق المملكة.'),
    },
}


BRAND_SLUGS = {'Bambu Lab': 'bambu-lab'}
# A brand only gets an indexable page when it has enough stock and its own
# copy here (thin one-product brand pages are just duplicate filter pages).
BRAND_MIN_PRODUCTS = 3
BRAND_SEO = {
    'Bambu Lab': {
        'en': ('Bambu Lab 3D Printers & Parts in Saudi Arabia | Black Arrow 3D',
               'Buy Bambu Lab 3D printers and spare parts in Saudi Arabia from Black Arrow 3D. Prices in SAR with delivery across the Kingdom.',
               'Bambu Lab 3D printers and spare parts, priced in Saudi riyals and delivered across Saudi Arabia. Compare models by price and build volume in the shop.'),
        'ar': ('طابعات Bambu Lab ثلاثية الأبعاد وقطع الغيار في السعودية | Black Arrow 3D',
               'اشترِ طابعات Bambu Lab ثلاثية الأبعاد وقطع الغيار في السعودية من Black Arrow 3D. الأسعار بالريال مع التوصيل لكل مناطق المملكة.',
               'طابعات Bambu Lab ثلاثية الأبعاد وقطع الغيار بالريال السعودي مع التوصيل لكل مناطق المملكة. قارن الموديلات بالسعر وحجم الطباعة في المتجر.'),
    },
}


def brand_url(brand, lang):
    return ('/3d/ar' if lang == 'ar' else '/3d') + '/brands/' + BRAND_SLUGS[brand] + '/'




HREFLANG_RX = re.compile(r'\n?[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">')


def strip_hreflang(html):
    """Templates (home, shop) now carry their own English hreflang set; every page
    built from them writes its own, so drop the inherited lines first."""
    return HREFLANG_RX.sub('', html)


def ensure_english_hreflang(html, en_path, ar_path):
    html = strip_hreflang(html)
    block = ('\n  <link rel="alternate" hreflang="en" href="' + SITE + en_path + '">'
             '\n  <link rel="alternate" hreflang="ar" href="' + SITE + ar_path + '">'
             '\n  <link rel="alternate" hreflang="x-default" href="' + SITE + en_path + '">')
    return re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + block, html, count=1)


def landing_card(p, lang):
    """Plain crawlable product card: an ordinary <a href> with image, name and price."""
    name = L(p, 'name', lang)
    img = primary_image(p)
    return ('<a class="b3d-cat-landing__card" href="' + product_url(p, lang) + '">'
            + (('<span class="b3d-corner-badge b3d-corner-badge--sale">' + T('js_sale_badge', lang) + '</span>') if p.get('onSale') else '')
            + ('<img src="' + img + '" alt="' + esc(name) + '" loading="lazy" width="300" height="300">' if img else '')
            + '<span class="b3d-cat-landing__name">' + esc(name) + '</span>'
            + '<span class="b3d-cat-landing__price">' + price_block(p, lang) + '</span>'
            + '</a>')



def related_products_html(current, lang):
    """Same picks as the product-page script (same category or brand, first four),
    as plain links; the script replaces this on load."""
    related = [x for x in PRODUCTS if x['id'] != current['id']
               and (x['category'] == current['category'] or x.get('brand') == current.get('brand'))][:4]
    if not related:
        return '<div data-b3d-related></div>'
    return ('<div data-b3d-related><h2 class="b3d-related__title">' + esc(T('js_related_products', lang)) + '</h2>'
            '<div class="b3d-grid">' + ''.join(landing_card(x, lang) for x in related) + '</div></div>')


# Keep in sync with PRINTER_PICKER in 3d/assets/js/3d-store.js
PRINTER_PICKER = [
    ('bambu-lab-a1-mini', 'picker_tag_1', 'picker_why_1'),
    ('creality-sparkx-i7', 'picker_tag_2', 'picker_why_2'),
    ('bambu-lab-a2l', 'picker_tag_4', 'picker_why_4'),
    ('bambu-lab-h2c-combo', 'picker_tag_7', 'picker_why_7'),
]
PICKER_RX = re.compile(r'(<div class="b3d-picker-grid" data-b3d-picker-grid>)(?:<!--b3d-prerender-->.*?<!--/b3d-prerender-->)?(</div>)', re.S)


def picker_cards_html(lang):
    by_id = {x['id']: x for x in PRODUCTS}
    out = []
    for pid, tag_key, why_key in PRINTER_PICKER:
        x = by_id.get(pid)
        if not x:
            continue
        img = primary_image(x)
        out.append('<div class="b3d-picker-card">'
                   + ('<div class="b3d-picker-card__visual"><img src="' + img + '" alt="' + esc(L(x, 'name', lang)) + '" loading="lazy" width="300" height="300"></div>' if img else '')
                   + '<div class="b3d-picker-card__body">'
                   + '<span class="b3d-picker-card__tag">' + esc(T(tag_key, lang)) + '</span>'
                   + '<h3>' + esc(L(x, 'name', lang)) + '</h3>'
                   + '<p>' + esc(T(why_key, lang)) + '</p>'
                   + '<div class="b3d-picker-card__meta">' + price_block(x, lang) + '</div>'
                   + '<a href="' + product_url(x, lang) + '" class="btn btn-outline">' + esc(T('js_view_product', lang)) + '</a>'
                   + '</div></div>')
    return ''.join(out)


PRERENDER_RX = re.compile(r'(<div class="b3d-grid" data-b3d-(?:grid|featured-grid)>)(?:<!--b3d-prerender-->.*?<!--/b3d-prerender-->)?(</div>)', re.S)


def featured_products():
    """Same pick as the homepage script: pinned, then new arrivals, then the rest (max 8)."""
    avail = [p for p in PRODUCTS if p.get('available') is not False]
    pinned = [p for p in avail if p.get('featured')]
    fresh = [p for p in avail if not p.get('featured') and p.get('newArrival')][::-1]
    rest = [p for p in avail if not p.get('featured') and not p.get('newArrival')]
    return (pinned + fresh + rest)[:8]


BLOG_EN_INDEX = os.path.join(ROOT, '3d', 'blog', 'index.html')
HOME_BLOG_RX = re.compile(r'(<div class="b3d-blog-grid">\n)(.*?)(\n      </div>\n      <div style="text-align:center;margin-top:24px;">)', re.S)


def refresh_home_blog(html, lang):
    """All guides on the homepage (was three), with excerpts; Arabic cards use the Arabic copy."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from generate_3d_blog_ar import BLOG_INDEX_CARDS
    with open(BLOG_EN_INDEX, encoding='utf-8') as f:
        idx = f.read()
    en = {}
    for m in re.finditer(r'<article class="b3d-blog-card">(.*?)</article>', idx, re.S):
        blk = m.group(1)
        slug = re.search(r'href="/3d/blog/([^/"]+)/"', blk).group(1)
        meta = re.search(r'b3d-blog-card__meta">(.*?)</span>', blk, re.S).group(1).strip()
        title = re.search(r'b3d-blog-card__title">(.*?)</h2>', blk, re.S).group(1).strip()
        exc = re.search(r'b3d-blog-card__excerpt">(.*?)</span>', blk, re.S).group(1).strip()
        en[slug] = (meta, title, exc)
    cards = []
    for slug, meta_ar, read_ar, title_ar, exc_ar in BLOG_INDEX_CARDS:
        if lang == 'ar':
            meta, title, exc, read, base = meta_ar + ' &middot; ' + read_ar, title_ar, exc_ar, '\u0627\u0642\u0631\u0623 \u0627\u0644\u0645\u0642\u0627\u0644 &rarr;', '/3d/ar/blog/'
        else:
            meta, title, exc = en[slug]
            read, base = 'Read article &rarr;', '/3d/blog/'
        cards.append('        <article class="b3d-blog-card">\n'
                     '          <a href="' + base + slug + '/" class="b3d-card__stretched-link" aria-label="' + title + '"></a>\n'
                     '          <span class="b3d-blog-card__meta">' + meta + '</span>\n'
                     '          <h3 class="b3d-blog-card__title">' + title + '</h3>\n'
                     '          <span class="b3d-blog-card__excerpt">' + exc + '</span>\n'
                     '          <span class="b3d-blog-card__read">' + read + '</span>\n'
                     '        </article>')
    return HOME_BLOG_RX.sub(lambda m: m.group(1) + '\n'.join(cards) + m.group(3), html, count=1)


def prerender_grids(html, lang, kind):
    """Put real product links into the JS-filled grid so the first HTML already has them.
    kind: 'shop' (all products) or 'home' (featured picks). The script replaces these on load."""
    items = PRODUCTS if kind == 'shop' else featured_products()
    cards = ''.join(landing_card(p, lang) for p in items)
    html = PRERENDER_RX.sub(lambda m: m.group(1) + '<!--b3d-prerender-->' + cards + '<!--/b3d-prerender-->' + m.group(2), html, count=1)
    if kind == 'home':
        html = refresh_home_blog(html, lang)
        html = PICKER_RX.sub(lambda m: m.group(1) + '<!--b3d-prerender-->' + picker_cards_html(lang) + '<!--/b3d-prerender-->' + m.group(2), html, count=1)
    if kind == 'shop':
        html = re.sub(r'(data-b3d-count>)[^<]*(<)', lambda m: m.group(1) + str(len(PRODUCTS)) + m.group(2), html, count=1)
    return html


def prerender_english_pages():
    """3d/shop/index.html and 3d/index.html are hand-authored templates that are
    also the live English pages; refresh their pre-rendered grids in place."""
    for path, kind in ((SHOP_TEMPLATE, 'shop'), (HOME_TEMPLATE, 'home')):
        with open(path, encoding='utf-8', newline='') as f:
            html = f.read()
        nl = '\r\n' if '\r\n' in html else '\n'
        new = prerender_grids(html.replace('\r\n', '\n'), 'en', kind)
        en_path, ar_path = ('/3d/shop/', '/3d/ar/shop/') if kind == 'shop' else ('/3d/', '/3d/ar/')
        new = ensure_english_hreflang(new, en_path, ar_path).replace('\n', nl)
        if new != html:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(new)


# Longer, genuinely useful copy for the 3D Printers landing page. Every claim
# below is taken from the product data (build volume, multicolor system,
# enclosure, listed materials) - nothing here is a new business claim.
# Arabic is DRAFT machine-assisted copy, flagged for review like the rest.
CATEGORY_H1 = {
    '3D Printers': {'en': '3D Printers in Saudi Arabia'},
}

CATEGORY_GUIDE = {
    '3D Printers': {
        'en': {
            'intro': [
                "Shop desktop 3D printers online in Saudi Arabia from Black Arrow 3D. We offer printers from Bambu Lab, Creality, Elegoo, Anycubic and Snapmaker, from compact, beginner-friendly models to enclosed printers for professional use and large-format machines with far more build room.",
                "Many models can print in several colors: Bambu Lab's AMS Lite, Creality's CFS Lite and Elegoo's CANVAS system each handle up to four filaments, and the Snapmaker U1 uses four independent toolheads. Every price is in Saudi riyals (SAR) and orders are delivered across Saudi Arabia.",
                "Not sure which one to pick? Use the guides below, compare build volume and price in the shop, or ask us on WhatsApp and we will help you choose.",
            ],
            'sections': [
                ('3D Printers for Beginners',
                 "Printers suited to first-time users, with automatic bed leveling and simple setup on the models that include them.",
                 ['bambu-lab-a1-mini', 'bambu-lab-a1', 'creality-sparkx-i7']),
                ('Professional & Engineering Printers',
                 "Enclosed printers built for everyday production. The H2C Combo and Centauri Carbon 2 also list engineering materials such as ABS and ASA.",
                 ['bambu-lab-h2c-combo', 'bambu-lab-p2s', 'elegoo-centauri-carbon-2']),
                ('Large-Format Printers',
                 "More build room for bigger models, prototypes, decor and oversized parts.",
                 ['bambu-lab-a2l', 'anycubic-kobra-3-max']),
                ('Multicolor 3D Printers',
                 "Print in several colors in one job: filament systems that handle up to four colors, or independent toolheads.",
                 ['bambu-lab-a1', 'creality-sparkx-i7', 'elegoo-centauri-carbon-2', 'snapmaker-u1', 'anycubic-kobra-3-max']),
            ],
            'vol': 'build volume',
            'shop_link': 'Compare all printers in the shop',
        },
        'ar': {
            'intro': [
                "تسوّق الطابعات ثلاثية الأبعاد المكتبية أونلاين في السعودية من Black Arrow 3D. نوفّر طابعات Bambu Lab وCreality وElegoo وAnycubic وSnapmaker، من الموديلات الصغيرة المناسبة للمبتدئين إلى الطابعات المغلقة للاستخدام المهني والطابعات كبيرة الحجم ذات مساحة الطباعة الأوسع.",
                "كثير من الموديلات تطبع بعدة ألوان: نظام AMS Lite من Bambu Lab ونظام CFS Lite من Creality ونظام CANVAS من Elegoo يتعامل كلٌّ منها مع ما يصل إلى أربعة خيوط، وتستخدم Snapmaker U1 أربعة رؤوس طباعة مستقلة. جميع الأسعار بالريال السعودي والتوصيل لكل مناطق المملكة.",
                "لست متأكدًا من الطابعة المناسبة؟ استعن بالأدلة أدناه، وقارن حجم الطباعة والسعر في المتجر، أو راسلنا عبر واتساب لنساعدك في الاختيار.",
            ],
            'sections': [
                ('طابعات ثلاثية الأبعاد للمبتدئين',
                 "طابعات مناسبة لمن يبدأ لأول مرة، مع معايرة تلقائية للسرير وإعداد بسيط في الموديلات التي توفّر ذلك.",
                 None),
                ('طابعات احترافية وهندسية',
                 "طابعات مغلقة مصمّمة للإنتاج اليومي. كما تذكر H2C Combo وCentauri Carbon 2 خامات هندسية مثل ABS وASA.",
                 None),
                ('طابعات كبيرة الحجم',
                 "مساحة طباعة أكبر للنماذج الكبيرة والنماذج الأولية والديكور والقطع كبيرة الحجم.",
                 None),
                ('طابعات ثلاثية الأبعاد متعددة الألوان',
                 "اطبع بعدة ألوان في مهمة واحدة: أنظمة خيوط تدعم حتى أربعة ألوان، أو رؤوس طباعة مستقلة.",
                 None),
            ],
            'vol': 'حجم الطباعة',
            'shop_link': 'قارن كل الطابعات في المتجر',
        },
    },
}


def category_guide_html(cat, lang, by_id):
    """H2 sections with linked products under the category grid."""
    g = CATEGORY_GUIDE.get(cat, {}).get(lang)
    if not g:
        return ''
    en_sections = CATEGORY_GUIDE[cat]['en']['sections']
    out = ['<div class="b3d-cat-guide">']
    for i, (heading, para, ids) in enumerate(g['sections']):
        ids = ids or en_sections[i][2]
        items = []
        for pid in ids:
            p = by_id.get(pid)
            if not p or p.get('available') is False:
                continue
            vol = ''
            for row in p.get('specs') or []:
                if row[0] == 'Build Volume':
                    vol = row[1].replace(' x ', ' \u00d7 ')
                    break
            price = money(current_price(p), p.get('currency'))
            img = primary_image(p)
            name = L(p, 'name', lang)
            items.append('<li><a class="b3d-guide-card" href="' + product_url(p, lang) + '">'
                         + '<span class="b3d-guide-card__img">' + ('<img src="' + img + '" alt="' + esc(name) + '" loading="lazy" width="240" height="240">' if img else '') + '</span>'
                         + '<span class="b3d-guide-card__name">' + esc(name) + '</span>'
                         + ('<span class="b3d-guide-card__spec">' + g['vol'] + ' <bdi dir="ltr">' + esc(vol.replace(' mm', '')) + '</bdi> ' + ('مم' if lang == 'ar' else 'mm') + '</span>' if vol else '')
                         + '<span class="b3d-guide-card__price"><bdi dir="ltr">' + price + '</bdi></span></a></li>')
        out.append('<section class="b3d-guide-sec"><h2>' + esc(heading) + '</h2><p>' + esc(para) + '</p><ul class="b3d-guide-grid">' + ''.join(items) + '</ul></section>')
    out.append('<p><a class="btn btn-outline" href="' + shop_url(lang) + '">' + esc(g['shop_link']) + '</a></p>')
    out.append('</div>')
    return ''.join(out)



def build_category_page(cat, lang, products_in_cat, brand=None):
    """Static landing page for a category, or (brand=...) for a brand."""
    def _url(l):
        return brand_url(brand, l) if brand else category_url(cat, l)

    with open(SHOP_TEMPLATE, encoding='utf-8') as f:
        html = strip_hreflang(f.read())

    label = brand if brand else category_label(cat, lang)
    url = SITE + _url(lang)
    seo = (BRAND_SEO[brand] if brand else CATEGORY_SEO.get(cat, {})).get(lang)
    if seo:
        title, desc, intro = seo
    else:
        intro = T('b3d_shop_p', lang)
        title = label + ' — Black Arrow 3D'
        desc = label + ': ' + intro

    html = set_lang_attrs(html, lang)
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="' + esc(desc) + '">', html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">',
                  '<meta property="og:title" content="' + esc(title) + '">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">',
                  '<meta property="og:description" content="' + esc(desc) + '">', html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*">',
                  '<meta property="og:url" content="' + url + '">', html, count=1)
    html = re.sub(r'<link rel="canonical" href="[^"]*">',
                  '<link rel="canonical" href="' + url + '">'
                  + '\n  <link rel="alternate" hreflang="en" href="' + SITE + _url("en") + '">'
                  + '\n  <link rel="alternate" hreflang="ar" href="' + SITE + _url("ar") + '">'
                  + '\n  <link rel="alternate" hreflang="x-default" href="' + SITE + _url("en") + '">',
                  html, count=1)
    html = re.sub(r'<title>[^<]*</title>', '<title>' + esc(title) + '</title>', html, count=1)

    cards = [landing_card(p, lang) for p in products_in_cat]

    breadcrumb_ld = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Black Arrow Venture', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Black Arrow 3D', 'item': SITE + home_url(lang)},
            {'@type': 'ListItem', 'position': 3, 'name': T('nav_shop', lang), 'item': SITE + shop_url(lang)},
            {'@type': 'ListItem', 'position': 4, 'name': label, 'item': url},
        ],
    }
    item_list_ld = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': L(p, 'name', lang), 'url': SITE + product_url(p, lang)}
            for i, p in enumerate(products_in_cat)
        ],
    }
    html = html.replace('</head>',
                         '  <script type="application/ld+json">' + json.dumps(breadcrumb_ld, ensure_ascii=False) + '</script>\n'
                         + '  <script type="application/ld+json">' + json.dumps(item_list_ld, ensure_ascii=False) + '</script>\n'
                         + '</head>')

    html = translate_static_chrome(html, lang)
    html = localize_ar_hrefs(html, lang)
    # category pages have no H2 before the footer columns: footer headings are H2 so the outline does not jump H1 -> H3
    _a, _b, _c = html.partition('<footer')
    html = _a + _b + _c.replace('<h3', '<h2').replace('</h3>', '</h2>')
    html = lang_toggle_link(html, lang, _url('ar' if lang == 'en' else 'en'))

    guide_copy = None if brand else CATEGORY_GUIDE.get(cat, {}).get(lang)
    live_shop_href = ('/3d/ar' if lang == 'ar' else '/3d') + ('/shop/?brand=' + brand.replace(' ', '+') if brand else '/shop/?cat=' + cat.replace(' ', '+'))
    landing_block = (
        '<section class="section" style="padding-top:20px;">'
        + '<div class="container">'
        + '<nav class="breadcrumb" aria-label="Breadcrumb">'
        + '<a href="' + home_url(lang) + '">' + esc(T('nav_black_arrow_3d_full', lang)) + '</a><span>›</span>'
        + '<a href="' + shop_url(lang) + '">' + esc(T('nav_shop', lang)) + '</a><span>›</span>'
        + '<span>' + esc(label) + '</span>'
        + '</nav>'
        + '<h1>' + esc(CATEGORY_H1.get(cat, {}).get(lang, label) if not brand else label) + '</h1>'
        + (''.join('<p class="b3d-shop-head__intro">' + esc(x) + '</p>' for x in guide_copy['intro']) if guide_copy else '<p class="b3d-shop-head__intro">' + esc(intro) + '</p>')
        + '<p><a class="btn btn-primary" href="' + live_shop_href + '">' + esc(T('shop_filters_btn', lang)) + ' →</a></p>'
        + '<div class="b3d-cat-landing__grid">' + ''.join(cards) + '</div>'
        + category_guide_html(cat, lang, {x['id']: x for x in PRODUCTS})
        + '</div></section>'
    )
    html = re.sub(r'<main id="main">.*?</main>', '<main id="main">' + landing_block + '</main>', html, count=1, flags=re.DOTALL)

    if brand:
        out_path = os.path.join(ROOT, '3d', 'ar' if lang == 'ar' else '', 'brands', BRAND_SLUGS[brand], 'index.html')
    else:
        out_path = os.path.join(ROOT, '3d', 'ar' if lang == 'ar' else '', 'shop', CATEGORY_SLUGS[cat], 'index.html')
    write(out_path, html)


"""DRAFT machine-assisted Arabic SEO copy — literal, not creative,
translations of the existing English marketing metadata. Flagged for
Afzal's review/approval like every other AR copy block in this project;
nothing here is a new business claim, just an Arabic rendering of
strings that already exist in English on the same pages."""
AR_HOME_META = {
    'description': 'اشترِ طابعات ثلاثية الأبعاد وخيوطاً وإكسسوارات وهدايا مطبوعة في السعودية من Bambu Lab وCreality وElegoo وغيرها. الأسعار بالريال والتوصيل لكل المملكة.',
    'og_title': 'شراء طابعات ثلاثية الأبعاد وخيوط وإكسسوارات أونلاين — Black Arrow 3D',
    'og_description': 'Bambu Lab وCreality وElegoo وSnapmaker وAnycubic وFlashforge — طابعات ثلاثية الأبعاد وخيوط وإكسسوارات لصناع المحتوى والطلاب والاستخدام المنزلي. ضمان شامل وتوصيل سريع لكل مناطق السعودية.',
    'title': 'طابعات وخيوط وهدايا ثلاثية الأبعاد | Black Arrow 3D',
}
AR_SHOP_META = {
    'description': 'تسوّق طابعات ثلاثية الأبعاد وخيوطاً وإكسسوارات في السعودية من Bambu Lab وCreality وElegoo وغيرها. قارن الأسعار بالريال مع التوصيل لكل المملكة.',
    'og_title': 'تسوق طابعات ثلاثية الأبعاد وخيوط وإكسسوارات أونلاين — Black Arrow 3D',
    'og_description': 'Bambu Lab وCreality وElegoo وSnapmaker وAnycubic وFlashforge — قارن الطابعات ثلاثية الأبعاد والخيوط والإكسسوارات بالسعر والعلامة التجارية وحجم الطباعة. ضمان شامل، توصيل لكل مناطق السعودية.',
    'title': 'تسوق طابعات وخيوط ثلاثية الأبعاد في السعودية | Black Arrow',
}


def apply_ar_meta(html, meta):
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="' + esc(meta['description']) + '">', html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">',
                  '<meta property="og:title" content="' + esc(meta['og_title']) + '">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">',
                  '<meta property="og:description" content="' + esc(meta['og_description']) + '">', html, count=1)
    html = re.sub(r'<title>[^<]*</title>', '<title>' + esc(meta['title']) + '</title>', html, count=1)
    return html



# ---------------------------------------------------------------------------
# Standalone content pages built from the shop template (own URL per language):
# the 3D printing service landing page and the shipping policy. Only facts the
# site already states are used (see /3d/returns/, FAQ, product pages).
# Arabic is DRAFT copy, flagged for review like every other AR block.
# ---------------------------------------------------------------------------
WA_QUOTE = 'https://wa.me/966560224715?text=Hello%21%20I%27d%20like%20to%20get%20something%203D%20printed.'

STATIC_PAGES = {
    '3d-printing-service-saudi-arabia': {
        'en': {
            'title': '3D Printing Service in Saudi Arabia | Black Arrow 3D',
            'desc': 'Custom 3D printing in Saudi Arabia: send your design file or a MakerWorld link, or tell us your idea. Get a quote on WhatsApp, with delivery across the Kingdom.',
            'h1': '3D Printing Service in Saudi Arabia',
            'crumb': '3D Printing Service',
            'body': [
                ('p', "Have a design you want printed? Send it to Black Arrow 3D and we will print it for you. We handle custom gifts, prototypes, decor and artwork, personalized products, customized parts and small batches, and we deliver across Saudi Arabia."),
                ('cta', 'Get Your Design Printed'),
                ('h2', 'What you can send us'),
                ('ul', ["Your own design file", "A MakerWorld link", "A sketch or an idea, and we will discuss it with you", "A photo or reference of what you want"]),
                ('h2', 'What we print'),
                ('ul', ["Custom gifts and personalized products", "Prototypes and rapid prototyping", "Decor and artwork", "Customized parts", "Small-batch production"]),
                ('h2', 'How it works'),
                ('ol', [
                    "Send us your design, MakerWorld link or idea on WhatsApp and ask for a quote.",
                    "We confirm all the details with you before production begins, including the file, material, colour, size and timing for your order.",
                    "We print your order. 3D printed items are typically prepared within 3 to 5 business days, as most are made to order.",
                    "We deliver across Saudi Arabia: standard shipping 30 SAR (4-5 business days) or fast shipping 50 SAR (2-3 business days). You receive a tracking number once your order has shipped.",
                ]),
                ('h2', 'Good to know'),
                ('ul', [
                    "Cancellation is possible only before production begins.",
                    "Custom and personalized orders are not returnable for change of mind. Defects, a wrong product or shipping damage are covered by our Return & Exchange Policy.",
                    "Payment: Cash on Delivery or Bank Transfer.",
                ]),
                ('h2', 'Ready-made 3D printed items'),
                ('p', "Prefer something ready to order? Browse our in-house designs in 3D Artwork: keychains, decor and gifts."),
                ('links', [('/3d/shop/3d-artwork/', 'Browse 3D Artwork'), ('/3d/product/custom-3d-artwork/', 'Custom 3D Artwork'), ('/3d/returns/', 'Return & Exchange Policy'), ('/3d/shipping/', 'Shipping Policy')]),
            ],
            'faq': [
                ("How do I get a price for a custom print?", "Send your design, MakerWorld link or idea on WhatsApp and ask for a 3D printing quote. We confirm the details with you before production."),
                ("How long does a custom order take?", "3D printed items are typically prepared within 3 to 5 business days, then shipped: standard shipping takes 4-5 business days and fast shipping 2-3 business days."),
                ("Do you deliver outside Saudi Arabia?", "No. We deliver across Saudi Arabia only."),
                ("Can I cancel a custom order?", "Only before production begins. Once production has started, cancellation is not available."),
            ],
            'service_name': '3D Printing Service',
        },
        'ar': {
            'title': 'خدمة الطباعة ثلاثية الأبعاد في السعودية | Black Arrow 3D',
            'desc': 'طباعة ثلاثية الأبعاد حسب الطلب في السعودية: أرسل ملف تصميمك أو رابط MakerWorld أو أخبرنا بفكرتك. احصل على عرض سعر عبر واتساب مع توصيل لكل مناطق المملكة.',
            'h1': 'خدمة الطباعة ثلاثية الأبعاد في السعودية',
            'crumb': 'خدمة الطباعة ثلاثية الأبعاد',
            'body': [
                ('p', "لديك تصميم تريد طباعته؟ أرسله إلى Black Arrow 3D ونطبعه لك. نتولى الهدايا المخصصة والنماذج الأولية والديكور والأعمال الفنية والمنتجات الشخصية والقطع المخصصة والدفعات الصغيرة، ونوصّل لجميع مناطق المملكة."),
                ('cta', 'اطبع تصميمك'),
                ('h2', 'ما الذي يمكنك إرساله'),
                ('ul', ["ملف تصميمك الخاص", "رابط من MakerWorld", "رسمة أو فكرة، ونناقشها معك", "صورة أو مرجع لما تريده"]),
                ('h2', 'ما الذي نطبعه'),
                ('ul', ["الهدايا المخصصة والمنتجات الشخصية", "النماذج الأولية والنماذج الأولية السريعة", "الديكور والأعمال الفنية", "القطع المخصصة", "الإنتاج بدفعات صغيرة"]),
                ('h2', 'كيف تتم الخدمة'),
                ('ol', [
                    "أرسل لنا تصميمك أو رابط MakerWorld أو فكرتك عبر واتساب واطلب عرض سعر.",
                    "نؤكد معك جميع التفاصيل قبل بدء الإنتاج، بما فيها الملف والخامة واللون والحجم والمدة لطلبك.",
                    "نطبع طلبك. تُجهَّز المنتجات المطبوعة ثلاثية الأبعاد عادةً خلال 3 إلى 5 أيام عمل، لأن معظمها يُصنع حسب الطلب.",
                    "نوصّل لجميع مناطق المملكة: شحن عادي 30 ريال (4-5 أيام عمل) أو شحن سريع 50 ريال (2-3 أيام عمل). ويصلك رقم تتبع بعد شحن الطلب.",
                ]),
                ('h2', 'من المفيد أن تعرف'),
                ('ul', [
                    "يمكن الإلغاء فقط قبل بدء الإنتاج.",
                    "لا يُقبل إرجاع الطلبات المخصصة والشخصية لمجرد تغيير الرأي. أما العيوب أو المنتج الخاطئ أو التلف أثناء الشحن فتشملها سياسة الاسترجاع والاستبدال.",
                    "الدفع: عند الاستلام أو بالتحويل البنكي.",
                ]),
                ('h2', 'منتجات مطبوعة جاهزة'),
                ('p', "تفضّل شيئًا جاهزًا للطلب؟ تصفح تصاميمنا الخاصة في قسم الأعمال الفنية: ميدالِيات المفاتيح والديكور والهدايا."),
                ('links', [('/3d/shop/3d-artwork/', 'تصفح الأعمال الفنية'), ('/3d/product/custom-3d-artwork/', 'أعمال فنية مخصصة'), ('/3d/returns/', 'سياسة الاسترجاع والاستبدال'), ('/3d/shipping/', 'سياسة الشحن')]),
            ],
            'faq': [
                ("كيف أحصل على سعر للطباعة المخصصة؟", "أرسل تصميمك أو رابط MakerWorld أو فكرتك عبر واتساب واطلب عرض سعر للطباعة ثلاثية الأبعاد. نؤكد معك التفاصيل قبل بدء الإنتاج."),
                ("كم يستغرق الطلب المخصص؟", "تُجهَّز المنتجات المطبوعة ثلاثية الأبعاد عادةً خلال 3 إلى 5 أيام عمل ثم تُشحن: الشحن العادي 4-5 أيام عمل والسريع 2-3 أيام عمل."),
                ("هل تشحنون خارج السعودية؟", "لا. نوصّل داخل المملكة العربية السعودية فقط."),
                ("هل يمكنني إلغاء طلب مخصص؟", "فقط قبل بدء الإنتاج. وبعد بدئه لا يتوفر الإلغاء."),
            ],
            'service_name': 'خدمة الطباعة ثلاثية الأبعاد',
        },
    },
    'shipping': {
        'en': {
            'title': 'Shipping Policy | Black Arrow 3D',
            'desc': 'Black Arrow 3D shipping policy: delivery across Saudi Arabia, standard and fast shipping options with costs and delivery times, preparation time and tracking.',
            'h1': 'Shipping Policy',
            'crumb': 'Shipping Policy',
            'body': [
                ('meta', 'Effective date: 24 September 2026'),
                ('h2', '1. Where we deliver'),
                ('p', "We deliver across Saudi Arabia. We do not ship internationally."),
                ('h2', '2. Shipping options and costs'),
                ('ul', ["Standard shipping: 30 SAR, delivered in 4-5 business days.", "Fast shipping: 50 SAR, delivered in 2-3 business days."]),
                ('p', "You choose the shipping option at checkout. Delivery times count from the day your order ships."),
                ('h2', '3. Order preparation'),
                ('p', "3D printed items (artwork, keychains, gifts and custom prints) are typically prepared within 3 to 5 business days, as most are made to order. For printers, filament and accessories, availability, including pre-order status, is shown on each product page."),
                ('h2', '4. Tracking'),
                ('p', "A tracking number is provided once your order has shipped, so you can follow its status."),
                ('h2', '5. Damage during shipping'),
                ('p', "If your order arrives damaged, contact us within 3 days of receiving it with clear photos. See the Return & Exchange Policy for details."),
                ('h2', '6. Payment'),
                ('p', "Cash on Delivery and Bank Transfer are available."),
                ('h2', '7. Contact'),
                ('contact', ''),
                ('links', [('/3d/returns/', 'Return & Exchange Policy'), ('/3d/terms/', 'Terms and Conditions')]),
            ],
            'faq': [],
            'service_name': None,
        },
        'ar': {
            'title': 'سياسة الشحن | Black Arrow 3D',
            'desc': 'سياسة الشحن في Black Arrow 3D: التوصيل لكل مناطق السعودية، وخيارات الشحن العادي والسريع بتكلفتها ومدد التوصيل، ومدة تجهيز الطلب والتتبع.',
            'h1': 'سياسة الشحن',
            'crumb': 'سياسة الشحن',
            'body': [
                ('meta', 'تاريخ السريان: 24 سبتمبر 2026'),
                ('h2', '1. أين نوصّل'),
                ('p', "نوصّل لجميع مناطق المملكة العربية السعودية. ولا نشحن خارج المملكة."),
                ('h2', '2. خيارات الشحن وتكلفتها'),
                ('ul', ["الشحن العادي: 30 ريال، يصل خلال 4-5 أيام عمل.", "الشحن السريع: 50 ريال، يصل خلال 2-3 أيام عمل."]),
                ('p', "تختار خيار الشحن عند إتمام الطلب. وتُحتسب مدة التوصيل من يوم شحن طلبك."),
                ('h2', '3. تجهيز الطلب'),
                ('p', "تُجهَّز المنتجات المطبوعة ثلاثية الأبعاد (الأعمال الفنية وميدالِيات المفاتيح والهدايا والطباعة المخصصة) عادةً خلال 3 إلى 5 أيام عمل، لأن معظمها يُصنع حسب الطلب. أما الطابعات وخيوط الطباعة والإكسسوارات فتظهر حالة التوفر، بما فيها الحجز المسبق، في صفحة كل منتج."),
                ('h2', '4. التتبع'),
                ('p', "يصلك رقم تتبع بعد شحن طلبك لتتمكن من متابعة حالته."),
                ('h2', '5. التلف أثناء الشحن'),
                ('p', "إذا وصل طلبك تالفًا، تواصل معنا خلال 3 أيام من استلامه مع صور واضحة. راجع سياسة الاسترجاع والاستبدال لمزيد من التفاصيل."),
                ('h2', '6. الدفع'),
                ('p', "الدفع عند الاستلام والتحويل البنكي متاحة."),
                ('h2', '7. التواصل'),
                ('contact', ''),
                ('links', [('/3d/returns/', 'سياسة الاسترجاع والاستبدال'), ('/3d/terms/', 'الشروط والأحكام')]),
            ],
            'faq': [],
            'service_name': None,
        },
    },
    'reviews': {
        'en': {
            'title': 'Customer Reviews | Black Arrow 3D',
            'desc': 'Read what customers say about Black Arrow 3D, and share your own review and photos of your order.',
            'h1': 'Customer Reviews',
            'crumb': 'Customer Reviews',
            'body': [
                ('p', "Ordered from Black Arrow 3D? Tell us how it went and add photos of your order. Reviews appear on the site after we approve them."),
                ('reviews', ''),
            ],
        },
        'ar': {
            'title': 'آراء العملاء | Black Arrow 3D',
            'desc': 'اقرأ ما يقوله عملاء Black Arrow 3D، وشاركنا تقييمك وصور طلبك.',
            'h1': 'آراء العملاء',
            'crumb': 'آراء العملاء',
            'body': [
                ('p', "طلبت من Black Arrow 3D؟ شاركنا تجربتك وأضف صور طلبك. تظهر التقييمات في الموقع بعد موافقتنا عليها."),
                ('reviews', ''),
            ],
        },
    },
}


def static_page_url(slug, lang):
    return ('/3d/ar' if lang == 'ar' else '/3d') + '/' + slug + '/'


def build_static_page(slug, lang):
    cfg = STATIC_PAGES[slug][lang]
    with open(SHOP_TEMPLATE, encoding='utf-8') as f:
        html = strip_hreflang(f.read())
    url = SITE + static_page_url(slug, lang)
    html = set_lang_attrs(html, lang)
    html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + esc(cfg['desc']) + '">', html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="' + esc(cfg['title']) + '">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + esc(cfg['desc']) + '">', html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="' + url + '">', html, count=1)
    html = re.sub(r'<link rel="canonical" href="[^"]*">',
                  '<link rel="canonical" href="' + url + '">'
                  + '\n  <link rel="alternate" hreflang="en" href="' + SITE + static_page_url(slug, 'en') + '">'
                  + '\n  <link rel="alternate" hreflang="ar" href="' + SITE + static_page_url(slug, 'ar') + '">'
                  + '\n  <link rel="alternate" hreflang="x-default" href="' + SITE + static_page_url(slug, 'en') + '">',
                  html, count=1)
    html = re.sub(r'<title>[^<]*</title>', '<title>' + esc(cfg['title']) + '</title>', html, count=1)

    ld = [{
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Black Arrow Venture', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Black Arrow 3D', 'item': SITE + home_url(lang)},
            {'@type': 'ListItem', 'position': 3, 'name': cfg['crumb'], 'item': url},
        ],
    }]
    if cfg.get('service_name'):
        ld.append({
            '@context': 'https://schema.org', '@type': 'Service',
            'name': cfg['service_name'], 'serviceType': '3D printing', 'url': url,
            'areaServed': {'@type': 'Country', 'name': 'Saudi Arabia'},
            'provider': {'@type': 'Organization', 'name': 'Black Arrow 3D', 'url': SITE + '/3d/'},
        })
    if cfg.get('faq'):
        ld.append({
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in cfg['faq']],
        })
    html = html.replace('</head>', ''.join('  <script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>\n' for x in ld) + '</head>')

    html = translate_static_chrome(html, lang)
    html = localize_ar_hrefs(html, lang)
    _a, _b, _c = html.partition('<footer')
    html = _a + _b + _c.replace('<h3', '<h2').replace('</h3>', '</h2>')
    html = lang_toggle_link(html, lang, static_page_url(slug, 'ar' if lang == 'en' else 'en'))

    out = []
    for kind, val in cfg['body']:
        if kind == 'p':
            out.append('<p>' + esc(val) + '</p>')
        elif kind == 'meta':
            out.append('<p class="b3d-legal__updated">' + esc(val) + '</p>')
        elif kind == 'h2':
            out.append('<h2>' + esc(val) + '</h2>')
        elif kind == 'ul':
            out.append('<ul>' + ''.join('<li>' + esc(x) + '</li>' for x in val) + '</ul>')
        elif kind == 'ol':
            out.append('<ol>' + ''.join('<li>' + esc(x) + '</li>' for x in val) + '</ol>')
        elif kind == 'cta':
            out.append('<p><a class="btn btn-primary" href="' + WA_QUOTE + '" target="_blank" rel="noopener noreferrer">' + esc(val) + '</a></p>')
        elif kind == 'contact':
            if lang == 'ar':
                out.append('<p>Black Arrow 3D &mdash; تُدار بواسطة Black Arrow Venture<br>الدمام، المنطقة الشرقية، المملكة العربية السعودية<br>البريد الإلكتروني: <a href="mailto:info@blackarrowksa.com">info@blackarrowksa.com</a><br>الهاتف/واتساب: <a href="tel:+966560224715">+966 56 022 4715</a></p>')
            else:
                out.append('<p>Black Arrow 3D &mdash; operated by Black Arrow Venture<br>Dammam, Eastern Province, Kingdom of Saudi Arabia<br>Email: <a href="mailto:info@blackarrowksa.com">info@blackarrowksa.com</a><br>Telephone/WhatsApp: <a href="tel:+966560224715">+966 56 022 4715</a></p>')
        elif kind == 'reviews':
            out.append('<div data-b3d-reviews="page"></div>')
        elif kind == 'links':
            base = '/3d/ar' if lang == 'ar' else '/3d'
            out.append('<p class="b3d-page__links">' + ' &middot; '.join(
                '<a href="' + (base + h[3:] if lang == 'ar' and not h.startswith(('/3d/returns', '/3d/terms')) else h) + '">' + esc(t) + '</a>' for h, t in val) + '</p>')
    if cfg.get('faq'):
        faq_title = 'الأسئلة الشائعة' if lang == 'ar' else 'Frequently asked questions'
        out.append('<h2>' + faq_title + '</h2><div class="b3d-faq">' + ''.join(
            '<details class="b3d-faq__item"><summary>' + esc(q) + '</summary><p>' + esc(a) + '</p></details>' for q, a in cfg['faq']) + '</div>')

    main = (
        '<section class="section" style="padding-top:20px;"><div class="container">'
        '<nav class="breadcrumb" aria-label="Breadcrumb">'
        '<a href="' + home_url(lang) + '">' + esc(T('nav_black_arrow_3d_full', lang)) + '</a><span>›</span><span>' + esc(cfg['crumb']) + '</span></nav>'
        '<article class="b3d-article b3d-page"><h1>' + esc(cfg['h1']) + '</h1>' + ''.join(out) + '</article>'
        '</div></section>'
    )
    html = re.sub(r'<main id="main">.*?</main>', lambda m: '<main id="main">' + main + '</main>', html, count=1, flags=re.DOTALL)
    if any(k == 'reviews' for k, _v in cfg['body']):
        html = html.replace('</body>', '  <script src="/3d/assets/js/3d-supabase-config.js" defer></script>' + chr(10) + '  <script src="/3d/assets/js/3d-reviews.js?v=20260963" defer></script>' + chr(10) + '</body>', 1)
    write(os.path.join(ROOT, '3d', 'ar' if lang == 'ar' else '', slug, 'index.html'), html)


def build_ar_home():
    with open(HOME_TEMPLATE, encoding='utf-8') as f:
        html = strip_hreflang(f.read())
    html = set_lang_attrs(html, 'ar')
    html = re.sub(r'<link rel="canonical" href="[^"]*">',
                  '<link rel="canonical" href="' + SITE + '/3d/ar/">'
                  + '\n  <link rel="alternate" hreflang="en" href="' + SITE + '/3d/">'
                  + '\n  <link rel="alternate" hreflang="ar" href="' + SITE + '/3d/ar/">'
                  + '\n  <link rel="alternate" hreflang="x-default" href="' + SITE + '/3d/">',
                  html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*">',
                  '<meta property="og:url" content="' + SITE + '/3d/ar/">', html, count=1)
    html = apply_ar_meta(html, AR_HOME_META)
    html = prerender_grids(html, 'ar', 'home')
    html = translate_static_chrome(html, 'ar')
    html = localize_ar_hrefs(html, 'ar')
    html = lang_toggle_link(html, 'ar', '/3d/')
    write(os.path.join(ROOT, '3d', 'ar', 'index.html'), html)


def build_ar_shop_index():
    with open(SHOP_TEMPLATE, encoding='utf-8') as f:
        html = strip_hreflang(f.read())
    html = set_lang_attrs(html, 'ar')
    html = re.sub(r'<link rel="canonical" href="[^"]*">',
                  '<link rel="canonical" href="' + SITE + '/3d/ar/shop/">'
                  + '\n  <link rel="alternate" hreflang="en" href="' + SITE + '/3d/shop/">'
                  + '\n  <link rel="alternate" hreflang="ar" href="' + SITE + '/3d/ar/shop/">'
                  + '\n  <link rel="alternate" hreflang="x-default" href="' + SITE + '/3d/shop/">',
                  html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*">',
                  '<meta property="og:url" content="' + SITE + '/3d/ar/shop/">', html, count=1)
    html = apply_ar_meta(html, AR_SHOP_META)
    html = prerender_grids(html, 'ar', 'shop')
    html = translate_static_chrome(html, 'ar')
    html = localize_ar_hrefs(html, 'ar')
    html = lang_toggle_link(html, 'ar', '/3d/shop/')
    write(os.path.join(ROOT, '3d', 'ar', 'shop', 'index.html'), html)


def main():
    prerender_english_pages()
    by_cat = {}
    for p in PRODUCTS:
        by_cat.setdefault(p['category'], []).append(p)

    for p in PRODUCTS:
        build_product_page(p, 'en')
        build_product_page(p, 'ar')
    print('generated', len(PRODUCTS) * 2, 'product pages')

    for cat, products_in_cat in by_cat.items():
        if cat not in CATEGORY_SLUGS:
            continue
        build_category_page(cat, 'en', products_in_cat)
        build_category_page(cat, 'ar', products_in_cat)
    print('generated', len(by_cat) * 2, 'category pages')

    by_brand = {}
    for p in PRODUCTS:
        by_brand.setdefault(p.get('brand'), []).append(p)
    n_brands = 0
    for brand in BRAND_SLUGS:
        prods = by_brand.get(brand, [])
        if sum(1 for p in prods if p.get('available') is not False) >= BRAND_MIN_PRODUCTS and brand in BRAND_SEO:
            build_category_page(None, 'en', prods, brand=brand)
            build_category_page(None, 'ar', prods, brand=brand)
            n_brands += 2
    print('generated', n_brands, 'brand pages')

    for _slug in STATIC_PAGES:
        for _lang in ('en', 'ar'):
            build_static_page(_slug, _lang)
    print('generated', len(STATIC_PAGES) * 2, 'content pages')

    build_ar_home()
    build_ar_shop_index()
    print('generated AR home + shop index')


if __name__ == '__main__':
    main()
