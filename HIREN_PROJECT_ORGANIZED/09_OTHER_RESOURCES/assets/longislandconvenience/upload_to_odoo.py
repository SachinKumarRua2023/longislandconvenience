"""
upload_to_odoo.py
─────────────────
Uploads logos (PNG) and favicons (ICO) to all 6 Odoo websites.
Logos: via XMLRPC write to website.logo field.
Favicons: via ir.actions.server (bypasses _handle_favicon XMLRPC bug).
"""
import xmlrpc.client, base64, os

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

HERE = os.path.dirname(os.path.abspath(__file__))

SITES = [
    {'wid': 1,  'logo': 'lic_logo.png',          'favicon': 'lic_favicon.ico',          'name': 'Long Island Convenience'},
    {'wid': 36, 'logo': 'lic_cards_logo.png',     'favicon': 'lic_cards_favicon.ico',     'name': 'Long Island Cards'},
    {'wid': 37, 'logo': 'lic_giftbasket_logo.png','favicon': 'lic_giftbasket_favicon.ico','name': 'Long Island Gift Basket'},
    {'wid': 38, 'logo': 'lic_balloons_logo.png',  'favicon': 'lic_balloons_favicon.ico',  'name': 'Long Island Balloons'},
    {'wid': 39, 'logo': 'lic_printmail_logo.png', 'favicon': 'lic_printmail_favicon.ico', 'name': 'Long Island Print & Mail'},
    {'wid': 41, 'logo': 'jhd_advisor_logo.png',   'favicon': 'jhd_advisor_favicon.ico',   'name': 'JHD Advisor'},
]

# ── 1. Upload logos via XMLRPC ────────────────────────────────────────────────
print('=== Uploading Logos ===')
for s in SITES:
    path = os.path.join(HERE, s['logo'])
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    xc('website', 'write', [[s['wid']], {'logo': b64}])
    print(f'  WID={s["wid"]} logo uploaded -> {s["name"]}')

# ── 2. Upload favicons via ir.actions.server (bypasses _handle_favicon bug) ──
print('\n=== Uploading Favicons via Server Action ===')

# Build a dict of wid -> base64 ICO data
favicon_data = {}
for s in SITES:
    path = os.path.join(HERE, s['favicon'])
    with open(path, 'rb') as f:
        favicon_data[s['wid']] = base64.b64encode(f.read()).decode('utf-8')

# Build the server action code — decodes base64 inside Odoo and writes real bytes
favicon_lines = '\n'.join(
    f'    {wid}: b64decode("{b64}"),'
    for wid, b64 in favicon_data.items()
)

server_code = f'''import base64
from base64 import b64decode
FAVICONS = {{
{favicon_lines}
}}
for wid, img_bytes in FAVICONS.items():
    env['website'].browse(wid).write({{'favicon': base64.b64encode(img_bytes).decode()}})
'''

model_id = xc('ir.model', 'search', [[['model', '=', 'website']]])[0]
action_id = xc('ir.actions.server', 'create', [{
    'name': '_tmp_upload_favicons',
    'model_id': model_id,
    'state': 'code',
    'code': server_code,
}])
xc('ir.actions.server', 'run', [[action_id]])
xc('ir.actions.server', 'unlink', [[action_id]])
print('  All 6 favicons uploaded via server action')

print('\n=== ALL DONE ===')
print('Logos and favicons uploaded to all 6 websites.')
print('Do a hard refresh (Ctrl+Shift+R) in browser to see changes.')
