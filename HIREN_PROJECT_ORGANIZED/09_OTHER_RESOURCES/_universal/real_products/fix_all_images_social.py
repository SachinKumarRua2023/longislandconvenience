import xmlrpc.client, urllib.request, base64, sys, re
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://country-cove-inc.odoo.com'
db  = 'country-cove-inc'
username = 'countrycoveinc@gmail.com'
password = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid    = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

def dl_b64(img_url):
    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return base64.b64encode(r.read()).decode()

# ─────────────────────────────────────────────────────────────────────────
# FIX 1: Product VARIANT images (product.product) — the ones actually shown
# ─────────────────────────────────────────────────────────────────────────
print('FIX 1: Updating product.product (variant) images...')
card_images = {
    259: ('Happy Fathers Day Card — Classic',
          'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=600&fit=crop&auto=format&q=85'),
    260: ('Fathers Day Card — Funny Dad Jokes',
          'https://images.unsplash.com/photo-1513151233558-d860c5398176?w=600&h=600&fit=crop&auto=format&q=85'),
    261: ('Best Dad Ever — Premium Foil Card',
          'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=600&h=600&fit=crop&auto=format&q=85'),
    262: ('Congrats Graduate! — Class of 2026 Card',
          'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=600&h=600&fit=crop&auto=format&q=85'),
    263: ('Funny Graduation Card — Finally Done!',
          'https://images.unsplash.com/photo-1467810563316-b5476525c0f9?w=600&h=600&fit=crop&auto=format&q=85'),
    264: ('Dr./MBA/Masters Graduation — Premium',
          'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=600&h=600&fit=crop&auto=format&q=85'),
}

for prod_id, (name, img_url) in card_images.items():
    try:
        img_b64 = dl_b64(img_url)
        # Update BOTH product.product (variant) AND product.template
        models.execute_kw(db, uid, password, 'product.product', 'write',
            [[prod_id], {'image_1920': img_b64}])
        models.execute_kw(db, uid, password, 'product.template', 'write',
            [[prod_id], {'image_1920': img_b64}])
        print(f'  OK  ID {prod_id}: {name}')
    except Exception as e:
        print(f'  ERR ID {prod_id}: {e}')

# ─────────────────────────────────────────────────────────────────────────
# FIX 2: Add Twitter/X to Cards footer (3506) and Gift Basket footer (3629)
# Using same X account: https://x.com/MRuaji85542
# ─────────────────────────────────────────────────────────────────────────
TWITTER_BTN = (
    '<a href="https://x.com/MRuaji85542" target="_blank" rel="noopener" '
    'aria-label="X / Twitter" style="display:inline-flex;align-items:center;'
    'justify-content:center;width:36px;height:36px;border-radius:50%;'
    'background:#000;color:#fff;text-decoration:none;font-weight:900;font-size:0.8rem;">X</a>'
)

for view_id, site_name in [(3506, 'Cards'), (3629, 'Gift Basket')]:
    print(f'\nFIX 2: Adding Twitter/X to {site_name} footer ({view_id})...')
    arch = models.execute_kw(db, uid, password, 'ir.ui.view', 'read',
        [[view_id]], {'fields': ['arch_db']})[0]['arch_db']

    if 'x.com/MRuaji85542' in arch:
        print(f'  Already has X link — skipping')
        continue

    # Find the Instagram button and append X after it
    if 'instagram' in arch.lower():
        # After IG button closing </a>, add X
        new_arch = re.sub(
            r'(aria-label=["\']Instagram["\'][^>]*>IG</a>)',
            r'\1' + TWITTER_BTN,
            arch, count=1
        )
        if new_arch == arch:
            # Try alternative: after the last </a> in social div area
            new_arch = re.sub(
                r'(instagram\.com[^"]*"[^>]*>IG</a>)',
                r'\1' + TWITTER_BTN,
                arch, count=1
            )
        if new_arch != arch:
            models.execute_kw(db, uid, password, 'ir.ui.view', 'write',
                [[view_id], {'arch_db': new_arch}])
            print(f'  OK  X added after Instagram button')
        else:
            print(f'  Could not inject X button — IG pattern not found, showing arch snippet:')
            idx = arch.lower().find('instagram')
            print(f'  {arch[max(0,idx-50):idx+200]}')
    else:
        print(f'  No Instagram button found yet in {site_name} footer')

print('\nAll done.')
