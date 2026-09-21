"""Set each sitemap <lastmod> to the date of the last git commit that touched that page.

    py scripts/sitemap_lastmod.py
Run after build_sitemap.py --apply and update_sitemap_3d.py.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
SM = ROOT / 'sitemap.xml'
SITE = 'https://www.blackarrowksa.com'


def page_file(path):
    p = path.lstrip('/')
    if p == '' or p.endswith('/'):
        p += 'index.html'
    return p


def last_date(rel):
    if not (ROOT / rel).exists():
        return None
    out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', rel], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    return out or None


s = SM.read_text('utf-8')
n = 0


def fix(m):
    global n
    loc = m.group(1)
    d = last_date(page_file(loc.replace(SITE, '')))
    if not d:
        return m.group(0)
    n += 1
    return re.sub(r'<lastmod>[^<]*</lastmod>', '<lastmod>%s</lastmod>' % d, m.group(0))


s = re.sub(r'<url>\s*<loc>([^<]+)</loc>.*?</url>', fix, s, flags=re.S)
SM.write_text(s, 'utf-8', newline='')
print('updated', n)
