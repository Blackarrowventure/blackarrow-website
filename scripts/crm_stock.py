"""The catalog with the CRM's stock applied - what a visitor sees once the page has loaded.

3d-store.js overrides the catalog's in-stock / pre-order flags with the CRM's Website Inventory
(/api/availability/). Google reads the page source, so the static builds must use the same
stock or Google shows "In stock" for things we cannot sell. sync_crm_prices.py saves the CRM
rows to 3d/assets/data/3d-stock.json every night; this applies them with the same rules as
applyCrmStock() in 3d-store.js. Without that file the catalog is used as it is.
"""
import io
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CATALOG = os.path.join(ROOT, '3d', 'assets', 'data', '3d-products.json')
STOCK = os.path.join(ROOT, '3d', 'assets', 'data', '3d-stock.json')


def apply_stock(products, rows):
    by_product = {}
    for r in rows:
        by_product.setdefault(r['id'], {})[(r.get('variant') or '').strip().lower()] = r
    for p in products:
        crm = by_product.get(p['id'])
        if crm is None:
            # Missing from the CRM: out of stock (3D Artwork is printed to order; kits and
            # pick-bundles follow their parts).
            if p.get('category') == '3D Artwork' or p.get('kit') or p.get('bundlePick'):
                continue
            p['available'] = False
            p['preorder'] = False
            for v in p.get('variants') or []:
                v['available'] = False
            continue
        whole = crm.get('')
        vs = p.get('variants') or []
        if vs:
            for v in vs:
                row = crm.get(v['label'].strip().lower())
                v['available'] = (row['available'] is not False) if row else bool(whole and whole['available'] is not False)
                v['preorder'] = bool(row['preorder'] if row else whole and whole.get('preorder'))
            buyable = [v for v in vs if v['available']]
            p['available'] = not (whole and whole['available'] is False) and bool(buyable)
            p['preorder'] = bool(buyable) and all(v['preorder'] for v in buyable)
        else:
            p['available'] = bool(whole and whole['available'] is not False)
            p['preorder'] = bool(whole and whole.get('preorder'))
    return products


def load_rows():
    if not os.path.isfile(STOCK):
        return None
    with io.open(STOCK, encoding='utf-8') as f:
        return json.load(f).get('rows') or None


def load_products():
    with io.open(CATALOG, encoding='utf-8') as f:
        products = json.load(f)['products']
    rows = load_rows()
    return apply_stock(products, rows) if rows else products
