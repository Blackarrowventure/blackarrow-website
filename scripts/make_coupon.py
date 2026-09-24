"""Create one-time discount codes for the Black Arrow 3D cart.

  py scripts/make_coupon.py 50
  py scripts/make_coupon.py 50 --note "for Ahmed"
  py scripts/make_coupon.py 100 --note Ramadan --min 300 --expires 2027-03-30
  py scripts/make_coupon.py 50 --count 10

Needs .env.local in the project root (gitignored - the repo is public):
  SUPABASE_SERVICE_KEY=<service_role key from Supabase > Project Settings > API>
The key can mint codes, so it must never be committed or pasted anywhere else.
"""
import argparse, json, pathlib, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
cfg = (ROOT / '3d/assets/js/3d-supabase-config.js').read_text(encoding='utf-8')
url = cfg.split("url: '")[1].split("'")[0]

env = {}
f = ROOT / '.env.local'
if f.exists():
    for line in f.read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"\'')
key = env.get('SUPABASE_SERVICE_KEY')
if not key:
    sys.exit('Missing SUPABASE_SERVICE_KEY in .env.local (see the docstring at the top of this file).')

ap = argparse.ArgumentParser()
ap.add_argument('amount', type=int, help='SAR off the order subtotal')
ap.add_argument('--note', default=None)
ap.add_argument('--min', type=int, default=0, help='minimum subtotal in SAR')
ap.add_argument('--expires', default=None, help='last valid day, YYYY-MM-DD')
ap.add_argument('--count', type=int, default=1)
a = ap.parse_args()

for _ in range(a.count):
    req = urllib.request.Request(
        url + '/rest/v1/rpc/generate_coupon',
        data=json.dumps({'p_amount': a.amount, 'p_note': a.note, 'p_min_order': a.min, 'p_expires': a.expires}).encode(),
        headers={'Content-Type': 'application/json', 'apikey': key, 'Authorization': 'Bearer ' + key},
        method='POST')
    try:
        code = json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        sys.exit('Failed (%s): %s' % (e.code, e.read().decode()[:300]))
    print(code)
