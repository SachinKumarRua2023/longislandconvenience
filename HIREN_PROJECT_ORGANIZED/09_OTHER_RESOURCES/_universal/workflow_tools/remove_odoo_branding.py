"""
Remove "Powered by Odoo" footer branding from ALL websites
on country-cove-inc.odoo.com

Method 1: Override web.brand_promotion_message view → renders nothing (permanent)
Method 2: Inject CSS into each website's custom_code_head (instant, belt-and-suspenders)

Run: python remove_odoo_branding.py
"""

import xmlrpc.client
import sys
sys.stdout.reconfigure(encoding='utf-8')

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

WEBSITE_IDS = [1, 18, 27, 29, 33, 36, 37, 38, 39, 40, 41]

CSS_HIDE = "<style>\n.o_footer_copyright_powered { display: none !important; }\n</style>"

# ── Authenticate ──────────────────────────────────────────────
print("Connecting to Odoo...")
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASS, {})
if not uid:
    raise SystemExit("Authentication failed — check credentials.")
print(f"Authenticated. UID: {uid}\n")

m = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

def read(model, domain, fields):
    return m.execute_kw(DB, uid, PASS, model, 'search_read', [domain], {'fields': fields})

def write(model, ids, vals):
    # CORRECT syntax: values dict goes in args[1], kwargs is empty {}
    return m.execute_kw(DB, uid, PASS, model, 'write', [ids, vals], {})

def create(model, vals):
    return m.execute_kw(DB, uid, PASS, model, 'create', [vals], {})


# ═══════════════════════════════════════════════════════════════
# METHOD 1 — Override web.brand_promotion_message
# This is the actual view that outputs "Powered by Odoo" text.
# We override it to render nothing. Permanent — survives caching.
# ═══════════════════════════════════════════════════════════════
print("=" * 60)
print("METHOD 1: Template override — web.brand_promotion_message")
print("=" * 60)

BRAND_VIEW_ID = 186   # confirmed by introspection
OVERRIDE_KEY  = 'custom.hide_brand_promotion_message'

# Check if override already exists
existing = read('ir.ui.view', [['key', '=', OVERRIDE_KEY]], ['id', 'name'])

if existing:
    print(f"Override already exists (ID: {existing[0]['id']}) — refreshing...")
    write('ir.ui.view', [existing[0]['id']], {
        'arch_db': (
            '<data inherit_id="web.brand_promotion_message" name="Hide Powered by Odoo">'
            '<xpath expr="//t[@t-out]" position="replace"/>'
            '</data>'
        ),
        'active': True,
    })
    print(f"Override updated OK.")
else:
    try:
        new_id = create('ir.ui.view', {
            'name':       'Hide Powered by Odoo Branding',
            'key':        OVERRIDE_KEY,
            'type':       'qweb',
            'inherit_id': BRAND_VIEW_ID,
            'arch_db': (
                '<data inherit_id="web.brand_promotion_message" name="Hide Powered by Odoo">'
                '<xpath expr="//t[@t-out]" position="replace"/>'
                '</data>'
            ),
            'active': True,
            'priority': 99,
        })
        print(f"View override CREATED — ID: {new_id}")
    except Exception as e:
        print(f"View override failed ({e})")
        print("Method 2 (CSS) will still cover it visually.")


# ═══════════════════════════════════════════════════════════════
# METHOD 2 — CSS injected into every website's <head>
# Belt-and-suspenders: hides the wrapper div even if Method 1
# is cached or delayed. Works immediately on page load.
# ═══════════════════════════════════════════════════════════════
print()
print("=" * 60)
print("METHOD 2: CSS injection into all website heads")
print("=" * 60)

websites = read('website', [['id', 'in', WEBSITE_IDS]], ['id', 'name', 'custom_code_head', 'domain'])
print(f"Updating {len(websites)} websites...\n")

for site in websites:
    wid  = site['id']
    name = site['name']
    head = site.get('custom_code_head') or ''

    if CSS_HIDE in head:
        print(f"  SKIP [{wid:>2}] {name} — CSS already present.")
        continue

    new_head = (head.strip() + '\n\n' + CSS_HIDE).strip() if head.strip() else CSS_HIDE

    try:
        # CORRECT: write([ids], {values}) — values in args, not kwargs
        write('website', [wid], {'custom_code_head': new_head})
        print(f"  OK   [{wid:>2}] {name}")
    except Exception as e:
        print(f"  ERR  [{wid:>2}] {name} — {e}")


# ═══════════════════════════════════════════════════════════════
# VERIFY
# ═══════════════════════════════════════════════════════════════
print()
print("=" * 60)
print("VERIFICATION")
print("=" * 60)

check = read('website', [['id', 'in', WEBSITE_IDS]], ['id', 'name', 'custom_code_head', 'domain'])
all_ok = True
for site in sorted(check, key=lambda s: s['id']):
    head   = site.get('custom_code_head') or ''
    ok     = CSS_HIDE in head
    domain = site.get('domain') or '(no domain)'
    status = "DONE" if ok else "MISSING"
    print(f"  [{status}] [{site['id']:>2}] {site['name']:<40} {domain}")
    if not ok:
        all_ok = False

print()
if all_ok:
    print("ALL DONE — Powered by Odoo removed from all 11 websites.")
    print("Clear browser cache and refresh to confirm.")
else:
    print("WARNING: Some sites still need attention (see MISSING above).")
