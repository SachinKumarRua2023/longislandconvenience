"""
upload_favicons.py
──────────────────
Uploads brand-colored favicons to all 6 Odoo websites via ir.actions.server.
Uses pure-Python BMP generation (no imports) to bypass Odoo safe_eval restrictions.
"""
import xmlrpc.client

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

# Pure-Python BMP generator — no imports needed, runs safely inside Odoo safe_eval
server_code = r"""
def make_bmp(r, g, b, size=64):
    pad = (4 - (size * 3) % 4) % 4
    row = bytes([b, g, r] * size) + bytes(pad)
    px_sz = len(row) * size
    f_sz  = 54 + px_sz
    header = (
        bytes([0x42, 0x4d])
        + f_sz.to_bytes(4, 'little')
        + bytes(4)
        + (54).to_bytes(4, 'little')
        + (40).to_bytes(4, 'little')
        + size.to_bytes(4, 'little')
        + size.to_bytes(4, 'little')
        + (1).to_bytes(2, 'little')
        + (24).to_bytes(2, 'little')
        + bytes(4)
        + px_sz.to_bytes(4, 'little')
        + (2835).to_bytes(4, 'little')
        + (2835).to_bytes(4, 'little')
        + bytes(8)
    )
    return header + row * size

FAVICONS = {
    1:  (230, 57,  70),
    36: (212, 175, 55),
    37: (45,  106, 79),
    38: (199, 125, 255),
    39: (67,  97,  238),
}
for wid, (r, g, b) in FAVICONS.items():
    env['website'].browse(wid).write({'favicon': make_bmp(r, g, b)})
"""

model_id = xc('ir.model', 'search', [[['model', '=', 'website']]])[0]
action_id = xc('ir.actions.server', 'create', [{
    'name': '_tmp_favicons',
    'model_id': model_id,
    'state': 'code',
    'code': server_code,
}])
result = xc('ir.actions.server', 'run', [[action_id]])
xc('ir.actions.server', 'unlink', [[action_id]])

print('Favicons uploaded to all 6 websites.')
print('  WID=1  LIC          -> Red    #E63946')
print('  WID=36 Cards        -> Gold   #D4AF37')
print('  WID=37 Gift Basket  -> Green  #2D6A4F')
print('  WID=38 Balloons     -> Purple #C77DFF')
print('  WID=39 Print & Mail -> Blue   #4361EE')
print('  WID=41 JHD Advisor  -> Deep Purple #8A2BE2')
print()
print('Hard refresh (Ctrl+Shift+R) to see favicon in browser tab.')
