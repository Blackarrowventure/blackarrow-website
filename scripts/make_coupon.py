"""Create a discount code for the Black Arrow 3D cart.

Usage:
  py scripts/make_coupon.py BAV50 50
  py scripts/make_coupon.py RAMADAN100 100 --expires 2027-03-30 --min 300 --note "for Ahmed"

The code itself is NOT stored: only a SHA-256 hash goes into
3d/assets/data/3d-coupons.json, so the list of codes can't be read from the
site. Keep your own record of the codes you hand out (the --note field helps).
Commit and push the JSON file to make the code live.
"""
import argparse, hashlib, json, pathlib

FILE = pathlib.Path(__file__).resolve().parent.parent / '3d' / 'assets' / 'data' / '3d-coupons.json'

ap = argparse.ArgumentParser()
ap.add_argument('code')
ap.add_argument('amount', type=int, help='SAR taken off the order subtotal')
ap.add_argument('--expires', help='last valid day, YYYY-MM-DD')
ap.add_argument('--min', type=int, default=0, help='minimum subtotal in SAR')
ap.add_argument('--note', default='', help='private reminder, e.g. who it is for')
a = ap.parse_args()

h = hashlib.sha256(('b3d:' + a.code.strip().upper()).encode()).hexdigest()
data = json.loads(FILE.read_text(encoding='utf-8'))
data['coupons'] = [c for c in data['coupons'] if c['hash'] != h]
entry = {'hash': h, 'amount': a.amount}
if a.expires: entry['expires'] = a.expires
if a.min: entry['minOrder'] = a.min
if a.note: entry['note'] = a.note
data['coupons'].append(entry)
FILE.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
print('Added %s = %d SAR off%s%s' % (a.code.upper(), a.amount,
      (', expires ' + a.expires) if a.expires else '', (', min order %d SAR' % a.min) if a.min else ''))
