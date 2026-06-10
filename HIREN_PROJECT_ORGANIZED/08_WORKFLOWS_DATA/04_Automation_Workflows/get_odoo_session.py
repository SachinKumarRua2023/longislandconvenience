"""
get_odoo_session.py
───────────────────
Gets Odoo session cookie for use in n8n WF-B HTTP nodes.
Run this once and paste the session_id into the n8n 'Odoo — Create Blog Post' node.

Usage:  python get_odoo_session.py
"""
import urllib.request, urllib.parse, json

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

payload = json.dumps({
    "jsonrpc": "2.0",
    "method": "call",
    "id": 1,
    "params": {
        "db": DB,
        "login": USER,
        "password": PASS,
    }
}).encode('utf-8')

req = urllib.request.Request(
    f'{URL}/web/session/authenticate',
    data=payload,
    headers={'Content-Type': 'application/json'},
)

with urllib.request.urlopen(req) as resp:
    headers = dict(resp.headers)
    body = json.loads(resp.read())

# Extract session_id from Set-Cookie header
raw_cookie = headers.get('Set-Cookie', '')
session_id = None
for part in raw_cookie.split(';'):
    part = part.strip()
    if part.startswith('session_id='):
        session_id = part.split('=', 1)[1]
        break

if session_id:
    print(f'\nOdoo session cookie:')
    print(f'   session_id={session_id}')
    print(f'\nCopy this value into n8n -> HTTP: Odoo - Create Blog Post -> Headers -> Cookie field:')
    print(f'   session_id={session_id}')
    print(f'\nNOTE: Session cookies expire. Re-run this script every ~7 days or when you get 401 errors.\n')
else:
    print('FAILED: Could not extract session_id from response headers.')
    print(f'Response body uid: {body.get("result", {}).get("uid")}')
    print('Headers received:', headers)

# Also get blog_id for WID=1
import xmlrpc.client
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

blogs = xc('blog.blog', 'search_read',
    [[['website_id', '=', 1]]],
    {'fields': ['id', 'name', 'website_id']})
print('\n=== Blog IDs for WID=1 (LongIslandConvenience.com) ===')
for b in blogs:
    print(f'  Blog ID={b["id"]}  Name={b["name"]}  -> Use this in WF-B node')
print('\nSet "blog_id": <ID> in the HTTP node body.\n')
