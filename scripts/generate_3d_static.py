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
        seo_title = _fit(name + ' — ' + price_txt + ' ريال | Black Arrow 3D', name + ' | Black Arrow 3D', name)
        seo_desc = (desc.rstrip('.') + '. السعر ' + price_txt + ' ريال. توصيل لكل مناطق السعودية.')
    else:
        seo_title = _fit(name + ' — ' + price_txt + ' SAR | Black Arrow 3D', name + ' | Black Arrow 3D', name)
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
        'availability': 'https://schema.org/OutOfStock' if p.get('available') is False else 'https://schema.org/InStock',
        'itemCondition': 'https://schema.org/NewCondition',
        'url': url,
        'hasMerchantReturnPolicy': {
            '@type': 'MerchantReturnPolicy',
            'applicableCountry': 'SA',
            'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow',
            'merchantReturnDays': 3,
            'merchantReturnLink': SITE + '/3d/returns/',
            'returnMethod': 'https://schema.org/ReturnByMail',
            'returnFees': 'https://schema.org/FreeReturn',
        },
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
        lambda m: '<div class="b3d-pd" data-b3d-product>' + detail_html + '</div>\n\n        ' + m.group(1),
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
            items.append('<li><a href="' + product_url(p, lang) + '">' + esc(L(p, 'name', lang)) + '</a>'
                         + (' \u2014 ' + g['vol'] + ' <bdi dir="ltr">' + esc(vol.replace(' mm', '')) + '</bdi> ' + ('\u0645\u0645' if lang == 'ar' else 'mm') if vol else '')
                         + ' \u00b7 <bdi dir="ltr">' + price + '</bdi></li>')
        out.append('<section><h2>' + esc(heading) + '</h2><p>' + esc(para) + '</p><ul>' + ''.join(items) + '</ul></section>')
    out.append('<p><a class="btn btn-outline" href="' + shop_url(lang) + '">' + esc(g['shop_link']) + '</a></p>')
    out.append('</div>')
    return ''.join(out)



def build_category_page(cat, lang, products_in_cat, brand=None):
    """Static landing page for a category, or (brand=...) for a brand."""
    def _url(l):
        return brand_url(brand, l) if brand else category_url(cat, l)

    with open(SHOP_TEMPLATE, encoding='utf-8') as f:
        html = f.read()

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

    cards = []
    for p in products_in_cat:
        name = L(p, 'name', lang)
        img = primary_image(p)
        cards.append(
            '<a class="b3d-cat-landing__card" href="' + product_url(p, lang) + '">'
            + (('<span class="b3d-corner-badge b3d-corner-badge--sale">' + T('js_sale_badge', lang) + '</span>') if p.get('onSale') else '')
            + ('<img src="' + img + '" alt="' + esc(name) + '" loading="lazy" width="300" height="300">' if img else '')
            + '<span class="b3d-cat-landing__name">' + esc(name) + '</span>'
            + '<span class="b3d-cat-landing__price">' + price_block(p, lang) + '</span>'
            + '</a>'
        )

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


def build_ar_home():
    with open(HOME_TEMPLATE, encoding='utf-8') as f:
        html = f.read()
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
    html = translate_static_chrome(html, 'ar')
    html = localize_ar_hrefs(html, 'ar')
    html = lang_toggle_link(html, 'ar', '/3d/')
    write(os.path.join(ROOT, '3d', 'ar', 'index.html'), html)


def build_ar_shop_index():
    with open(SHOP_TEMPLATE, encoding='utf-8') as f:
        html = f.read()
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
    html = translate_static_chrome(html, 'ar')
    html = localize_ar_hrefs(html, 'ar')
    html = lang_toggle_link(html, 'ar', '/3d/shop/')
    write(os.path.join(ROOT, '3d', 'ar', 'shop', 'index.html'), html)


def main():
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

    build_ar_home()
    build_ar_shop_index()
    print('generated AR home + shop index')


if __name__ == '__main__':
    main()
