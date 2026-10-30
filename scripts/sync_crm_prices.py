#!/usr/bin/env python3
"""Brings every price on the site in line with the CRM's Website Inventory prices.

The live store already shows CRM prices (3d-store.js reads /api/availability/), but the page
source - product pages, the shop grid, blog posts, Google's price data - is built from
3d/assets/data/3d-products.json. This script:

  1. reads the CRM prices from the public /api/availability/ endpoint (no key needed),
  2. writes them into 3d-products.json (keeping the file's own formatting),
  3. updates every price marked <span data-b3d-price="id|option">...</span> in the HTML and
     in the blog source scripts (scripts/seo_posts_*.py),
  4. saves the CRM's stock to 3d/assets/data/3d-stock.json (read by scripts/crm_stock.py), so
     Google's in-stock data and the Google Shopping feed match the live store,
  5. rebuilds the product/shop pages, the Shopping feed and the blog FAQ data when anything changed.

Run nightly by .github/workflows/sync-prices.yml; safe to run by hand any time.
Prints 'changed' or 'unchanged' on the last line.

Usage: python scripts/sync_crm_prices.py [--api URL] [--no-build]
"""
import glob
import io
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CATALOG = os.path.join(ROOT, '3d', 'assets', 'data', '3d-products.json')
STOCK = os.path.join(ROOT, '3d', 'assets', 'data', '3d-stock.json')
API = 'https://www.blackarrowksa.com/api/availability/'
SPAN = re.compile(r'(<span data-b3d-price="([^"]+)">)([^<]*)(</span>)')


def read(path):
    with io.open(path, encoding='utf-8', newline='') as f:
        return f.read()


def write(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def fetch_rows(url):
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        rows = json.load(r).get('rows') or []
    if not rows:
        # An empty answer means the CRM could not be reached: change nothing.
        raise SystemExit('No rows from the CRM - nothing changed.')
    return rows


def num_text(n):
    n = float(n)
    return ('%d' % n) if n == int(n) else ('%.2f' % n)


def block_span(raw, pid):
    i = raw.index('"id": "%s"' % pid)
    return raw.rindex('    {\n', 0, i), raw.index('\n    }', i) + len('\n    }')


def apply_crm_prices(raw, products, rows):
    """Returns the catalog text with the CRM prices written in, and how many prices changed."""
    by_id = {p['id']: p for p in products}
    changed = 0
    for r in rows:
        if r.get('price') is None or r['id'] not in by_id:
            continue
        p, label = by_id[r['id']], (r.get('variant') or '').strip()
        a, b = block_span(raw, p['id'])
        blk = raw[a:b]
        new = blk
        if label:
            v = next((v for v in p.get('variants') or [] if v['label'].strip().lower() == label.lower()), None)
            if not v or v['price'] == r['price']:
                continue
            lines = blk.split('\n')
            for k, line in enumerate(lines):
                if line.lstrip().startswith('{ ') and ('"label": %s' % json.dumps(v['label'], ensure_ascii=False)) in line:
                    lines[k] = re.sub(r'"price": [0-9.]+', '"price": ' + num_text(r['price']), line, count=1)
                    break
            new = '\n'.join(lines)
        elif not p.get('variants'):
            price, old = r['price'], r.get('oldPrice')
            on_sale = old is not None and old > price
            want = (old, price) if on_sale else (price, None)
            have = (p['price'], p.get('salePrice') if p.get('onSale') else None)
            if have == want:
                continue
            new = re.sub(r'\n      "price": [0-9.]+,', '\n      "price": %s,' % num_text(want[0]), new, count=1)
            new = re.sub(r'\n      "salePrice": [0-9.]+,', '', new)
            new = re.sub(r'\n      "onSale": (true|false),', '', new)
            if on_sale:
                new = new.replace('\n      "currency":', '\n      "salePrice": %s,\n      "onSale": true,\n      "currency":' % num_text(price), 1)
        if new != blk:
            raw = raw[:a] + new + raw[b:]
            changed += 1
    json.loads(raw)  # still valid JSON
    return raw, changed


def live_price(products_by_id, key):
    """Same rule as livePriceOf() in 3d-store.js."""
    pid, _, label = key.partition('|')
    p = products_by_id.get(pid)
    if not p:
        return None
    vs = p.get('variants') or []
    if label.strip():
        v = next((v for v in vs if v['label'].strip().lower() == label.strip().lower()), None)
        return v['price'] if v else None
    if vs:
        return min(v['price'] for v in vs)
    return p['salePrice'] if p.get('onSale') and p.get('salePrice') is not None else p['price']


def fmt(n):
    return '{:,.2f}'.format(n) if n % 1 else '{:,}'.format(int(n))


def update_spans(products):
    by_id = {p['id']: p for p in products}
    files = [f for f in glob.glob(os.path.join(ROOT, '3d', '**', '*.html'), recursive=True)]
    files += glob.glob(os.path.join(ROOT, 'scripts', 'seo_posts_*.py'))
    changed = 0
    for path in files:
        text = read(path)
        if 'data-b3d-price' not in text:
            continue

        def repl(m):
            n = live_price(by_id, m.group(2).replace('&quot;', '"'))
            return m.group(0) if n is None else m.group(1) + fmt(n) + m.group(4)

        new = SPAN.sub(repl, text)
        if new != text:
            write(path, new)
            changed += 1
    return changed


def save_stock(rows):
    """Writes the CRM stock (no prices - those go into the catalog); True when it changed."""
    keep = ('id', 'variant', 'available', 'preorder')
    slim = sorted(({k: r.get(k) for k in keep} for r in rows), key=lambda r: (r['id'], r['variant'] or ''))
    text = json.dumps({'_note': 'CRM stock, written by scripts/sync_crm_prices.py. Do not edit.', 'rows': slim},
                      ensure_ascii=False, indent=1) + '\n'
    if os.path.isfile(STOCK) and read(STOCK) == text:
        return False
    write(STOCK, text)
    return True


def main():
    api = sys.argv[sys.argv.index('--api') + 1] if '--api' in sys.argv else API
    rows = fetch_rows(api)
    raw = read(CATALOG)
    products = json.loads(raw)['products']
    raw, prices_changed = apply_crm_prices(raw, products, rows)
    if prices_changed:
        write(CATALOG, raw)
        products = json.loads(raw)['products']
    files_changed = update_spans(products)
    stock_changed = save_stock(rows)
    print('catalog prices changed:', prices_changed, '| files with marked prices updated:', files_changed,
          '| stock changed:', stock_changed)
    if not (prices_changed or files_changed or stock_changed):
        print('unchanged')
        return
    if '--no-build' not in sys.argv:
        for script in ('generate_3d_static.py', 'build_merchant_feed.py', 'add_blog_faq_schema.py', 'seo_meta_overrides.py'):
            subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', script)], check=True, cwd=ROOT)
    print('changed')


if __name__ == '__main__':
    main()
