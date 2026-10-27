#!/usr/bin/env python3
"""Builds the Google Merchant Center product feed: /3d/feed/google-merchant.xml

Free Google Shopping listings (the Shopping tab, product panels in search, Google Images)
come from this feed. Every product option is its own item, grouped by product; prices and
stock are the CRM's (catalog prices from sync_crm_prices.py, stock via crm_stock.py), so the
feed always matches the product pages. Rebuilt nightly by sync_crm_prices.py.

In Merchant Center: Products > Add products > Add from a file > Enter a link to your file,
then paste https://www.blackarrowksa.com/3d/feed/google-merchant.xml and fetch daily.

Usage: python scripts/build_merchant_feed.py
"""
import io
import os
import re
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crm_stock import ROOT, load_products  # noqa: E402

SITE = 'https://www.blackarrowksa.com'
OUT = os.path.join(ROOT, '3d', 'feed', 'google-merchant.xml')

# Same free-delivery rules as the cart (3d-store.js): orders from 3,000 SAR, artwork from 100 SAR.
FREE_SHIP_PRINTER_MIN = 3000
FREE_SHIP_ARTWORK_MIN = 100
SHIPPING_FEE = 30

PRODUCT_TYPE = {
    '3D Printers': '3D Printing > 3D Printers',
    'Filament': '3D Printing > Filament',
    'Accessories': '3D Printing > Printer Parts & Accessories',
    '3D Artwork': 'Gifts > 3D Printed Gifts',
}


def abs_url(path):
    # A JPEG twin is preferred where one exists: every Shopping surface takes JPEG.
    if path.endswith('.webp') and os.path.isfile(os.path.join(ROOT, path.lstrip('/')[:-5] + '.jpg')):
        path = path[:-5] + '.jpg'
    return path if path.startswith('http') else SITE + '/' + path.lstrip('/')


def plain(text, limit=4900):
    text = re.sub(r'<[^>]+>', ' ', text or '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:limit]


def money(n):
    return '%.2f SAR' % float(n)


def availability(available, preorder):
    if not available:
        return 'out_of_stock'
    return 'preorder' if preorder else 'in_stock'


def ship_fee(p, price):
    if price >= FREE_SHIP_PRINTER_MIN or (p.get('category') == '3D Artwork' and price >= FREE_SHIP_ARTWORK_MIN):
        return 0
    return SHIPPING_FEE


def item(p, item_id, title, price, old_price, available, preorder, images, group=None):
    link = SITE + '/3d/product/' + p['id'] + '/'
    on_sale = old_price is not None and old_price > price
    tags = [
        ('g:id', item_id),
        ('g:title', title[:150]),
        ('g:description', plain(p.get('description') or p.get('shortDesc')) or title),
        ('g:link', link),
        ('g:image_link', abs_url(images[0])),
    ]
    tags += [('g:additional_image_link', abs_url(i)) for i in images[1:11]]
    tags += [
        ('g:availability', availability(available, preorder)),
        ('g:price', money(old_price if on_sale else price)),
    ]
    if on_sale:
        tags.append(('g:sale_price', money(price)))
    tags += [
        ('g:condition', 'new'),
        ('g:brand', p.get('brand') or 'Black Arrow 3D'),
        ('g:identifier_exists', 'no'),
        ('g:product_type', PRODUCT_TYPE.get(p.get('category'), '3D Printing')),
    ]
    if group:
        tags.append(('g:item_group_id', group))
    out = ['    <item>']
    out += ['      <%s>%s</%s>' % (k, escape(str(v)), k) for k, v in tags]
    out += ['      <g:shipping>', '        <g:country>SA</g:country>',
            '        <g:service>Standard</g:service>',
            '        <g:price>%s</g:price>' % money(ship_fee(p, price)), '      </g:shipping>']
    out.append('    </item>')
    return '\n'.join(out)


def build(products):
    items = []
    for p in products:
        images = p.get('images') or []
        if not images:
            continue
        vs = p.get('variants') or []
        if len(vs) > 1:
            for v in vs:
                imgs = ([v['image']] if v.get('image') else []) + [i for i in images if i != v.get('image')]
                items.append(item(p, v.get('sku') or p['id'] + '-' + re.sub(r'[^a-z0-9]+', '-', v['label'].lower()).strip('-'),
                                  p['name'] + ' - ' + v['label'], v['price'], v.get('oldPrice'),
                                  v.get('available') is not False and p.get('available') is not False,
                                  bool(v.get('preorder') or p.get('preorder')), imgs, group=p['id']))
        else:
            v = vs[0] if vs else {}
            price = v.get('price', p['salePrice'] if p.get('onSale') and p.get('salePrice') is not None else p['price'])
            old = v.get('oldPrice') if vs else (p['price'] if p.get('onSale') and p.get('salePrice') is not None else None)
            items.append(item(p, p['id'], p['name'], price, old,
                              p.get('available') is not False and v.get('available') is not False,
                              bool(p.get('preorder')), images))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n'
            '  <channel>\n'
            '    <title>Black Arrow 3D</title>\n'
            '    <link>%s/3d/</link>\n'
            '    <description>3D printers, filament, parts and 3D printed gifts - delivered across Saudi Arabia.</description>\n'
            '%s\n'
            '  </channel>\n'
            '</rss>\n') % (SITE, '\n'.join(items)), len(items)


def main():
    xml, n = build(load_products())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(xml)
    print('google-merchant.xml:', n, 'items')


if __name__ == '__main__':
    main()
