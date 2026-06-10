import xmlrpc.client, sys, re
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://country-cove-inc.odoo.com'
db  = 'country-cove-inc'
username = 'countrycoveinc@gmail.com'
password = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid    = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# ─────────────────────────────────────────────────────────────────────────
# FIX 1: Balloon footer (3630) — correct social links
# Balloon accounts:
#   FB: https://www.facebook.com/profile.php?id=61589529507651
#   IG: https://www.instagram.com/longislandcoveballoons/
#   X:  https://x.com/MRuaji85542
# ─────────────────────────────────────────────────────────────────────────
print('FIX 1: Balloon footer correct social links...')
arch = models.execute_kw(db, uid, password, 'ir.ui.view', 'read',
    [[3630]], {'fields': ['arch_db']})[0]['arch_db']

# Replace wrong cards FB link with correct balloon FB
arch = arch.replace(
    'https://www.facebook.com/profile.php?id=61560730345126',
    'https://www.facebook.com/profile.php?id=61589529507651'
)
# Replace wrong cards IG link with correct balloon IG
arch = arch.replace(
    'https://www.instagram.com/longislandsportscard?igsh=bWY0dm93dDVxaWQz',
    'https://www.instagram.com/longislandcoveballoons/'
)

# Add X/Twitter button — inject after last </a> in the social div row
# The social div ends with IG </a> then </div>
TWITTER_BTN = (
    '<a href="https://x.com/MRuaji85542" target="_blank" rel="noopener" '
    'aria-label="X / Twitter" style="display:inline-flex;align-items:center;'
    'justify-content:center;width:38px;height:38px;border-radius:50%;'
    'background:#000;color:#fff;text-decoration:none;font-weight:900;font-size:0.8rem;">X</a>'
)

# Find the social div and append X button before its closing </div>
# Pattern: ...IG button </a> </div> <p ...Open 7 Days
arch = re.sub(
    r'(aria-label="Instagram"[^>]*>IG</a>\s*)(</div>)',
    r'\1' + TWITTER_BTN + r'\2',
    arch, count=1
)

models.execute_kw(db, uid, password, 'ir.ui.view', 'write', [[3630], {'arch_db': arch}])
print('  OK  FB : https://www.facebook.com/profile.php?id=61589529507651')
print('  OK  IG : https://www.instagram.com/longislandcoveballoons/')
print('  OK  X  : https://x.com/MRuaji85542')

# ─────────────────────────────────────────────────────────────────────────
# FIX 2: Cards footer (3506) — add social icons for Long Island Sports Cards
# Cards accounts:
#   FB: https://www.facebook.com/profile.php?id=61560730345126
#   IG: https://www.instagram.com/longislandsportscard?igsh=bWY0dm93dDVxaWQz
# ─────────────────────────────────────────────────────────────────────────
print()
print('FIX 2: Cards footer social icons...')
cards = models.execute_kw(db, uid, password, 'ir.ui.view', 'read',
    [[3506]], {'fields': ['arch_db']})[0]['arch_db']

FB_CARDS = 'https://www.facebook.com/profile.php?id=61560730345126'
IG_CARDS = 'https://www.instagram.com/longislandsportscard?igsh=bWY0dm93dDVxaWQz'

if 'instagram' in cards.lower():
    # Already exists — just update URLs
    cards = re.sub(r'https://www\.instagram\.com/[^\s"\'<>]+', IG_CARDS, cards)
    cards = re.sub(r'https://www\.facebook\.com/[^\s"\'<>]+', FB_CARDS, cards)
    models.execute_kw(db, uid, password, 'ir.ui.view', 'write', [[3506], {'arch_db': cards}])
    print('  OK  Updated existing social links in cards footer')
else:
    SOCIAL_ICONS = (
        '<div style="margin-top:24px;padding-top:20px;border-top:1px solid #222;">'
        '<div style="display:flex;gap:12px;align-items:center;margin-bottom:12px;">'
        '<a href="' + FB_CARDS + '" target="_blank" rel="noopener" '
        'style="display:inline-flex;align-items:center;justify-content:center;'
        'width:36px;height:36px;border-radius:50%;background:#1877F2;color:#fff;'
        'text-decoration:none;font-weight:900;font-size:1rem;">f</a>'
        '<a href="' + IG_CARDS + '" target="_blank" rel="noopener" '
        'style="display:inline-flex;align-items:center;justify-content:center;'
        'width:36px;height:36px;border-radius:50%;'
        'background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);'
        'color:#fff;text-decoration:none;font-weight:900;font-size:0.8rem;">IG</a>'
        '</div></div>'
    )
    # Insert before the final </div></xpath> or </data>
    if '</xpath>' in cards:
        cards = cards.replace('</xpath>', SOCIAL_ICONS + '</xpath>', 1)
    else:
        cards = cards.replace('</data>', SOCIAL_ICONS + '</data>', 1)
    models.execute_kw(db, uid, password, 'ir.ui.view', 'write', [[3506], {'arch_db': cards}])
    print('  OK  FB : ' + FB_CARDS)
    print('  OK  IG : ' + IG_CARDS)

print()
print('All social links done.')
