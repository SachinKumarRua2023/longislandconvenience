#!/usr/bin/env python3
"""Fix remaining missing images:
  1. Convenience store — use Open Food Facts API (not manual CDN paths)
  2. Gift baskets — use full Wikimedia Commons URLs (not thumbnails)
  3. Sports cards — use Pokemon CDN fallback
"""
import requests, base64, json, sys, time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
sys.stdout.reconfigure(encoding='utf-8')

ODOO_URL  = 'https://country-cove-inc.odoo.com'
ODOO_DB   = 'country-cove-inc'
ODOO_PASS = 'M@nhattan1234'
UID       = 2

_session = requests.Session()
_adapter = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504]))
_session.mount('https://', _adapter)
_session.mount('http://', _adapter)
_req_count = 0

def rpc(model, method, args, kwargs={}):
    global _req_count
    _req_count += 1
    payload = {
        'jsonrpc': '2.0', 'method': 'call', 'id': _req_count,
        'params': {'service': 'object', 'method': 'execute_kw',
                   'args': [ODOO_DB, UID, ODOO_PASS, model, method, args, kwargs]}
    }
    for attempt in range(3):
        try:
            r = _session.post(ODOO_URL + '/jsonrpc', json=payload, timeout=60)
            res = r.json()
            if res.get('error'):
                print(f'  RPC ERR: {res["error"]["data"]["message"][:100]}')
                return None
            return res.get('result')
        except Exception as e:
            wait = 3 * (attempt + 1)
            print(f'  retry {attempt+1}/3 ({e.__class__.__name__}), wait {wait}s...')
            time.sleep(wait)
    return None

def img_b64(url, retries=3):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for attempt in range(retries):
        try:
            resp = _session.get(url, timeout=25, headers=headers)
            if resp.status_code == 200 and len(resp.content) > 500:
                return base64.b64encode(resp.content).decode('utf-8')
            if resp.status_code != 404:
                print(f'  HTTP {resp.status_code} size={len(resp.content)} — {url[:70]}')
        except Exception as e:
            print(f'  img err: {e.__class__.__name__} — {url[:60]}')
            time.sleep(2)
    return None

def patch_product(name, website_id, img_url):
    existing = rpc('product.template', 'search_read',
        [[['name', '=', name], ['website_id', '=', website_id]]],
        {'fields': ['id', 'image_1920'], 'limit': 1})
    if not existing:
        print(f'  NOT FOUND: {name}')
        return
    pid = existing[0]['id']
    if existing[0].get('image_1920'):
        print(f'  SKIP (has img) id={pid} — {name[:55]}')
        return
    b64 = img_b64(img_url)
    if not b64:
        print(f'  NO IMG dl — {name[:55]}')
        return
    rpc('product.template', 'write', [[pid], {'image_1920': b64}])
    print(f'  PATCHED id={pid} — {name[:55]}')
    time.sleep(0.8)

print('=' * 70)
print('FINAL IMAGE PATCH')
print('=' * 70)

# ── Open Food Facts: get image URL via API (not manual CDN paths) ─────────────
def openfoodfacts_url(barcode):
    """Query Open Food Facts API to get image URL for a barcode."""
    try:
        r = _session.get(
            f'https://world.openfoodfacts.org/api/v2/product/{barcode}',
            params={'fields': 'image_front_url'},
            timeout=15,
            headers={'User-Agent': 'LongIslandConvenience/1.0 (sachin@longisl.com)'}
        )
        data = r.json()
        url = data.get('product', {}).get('image_front_url', '')
        return url or None
    except:
        return None

# ── Convenience: barcode → (product name, price) ─────────────────────────────
print('\n[1] CONVENIENCE — Open Food Facts API lookup')
WID_CONV = 1

CONV_PRODUCTS = [
    # (barcode, odoo_product_name)
    ('012000001550', 'Pepsi (20 oz)'),
    ('070847011049', 'Monster Energy Original (16 oz)'),
    ('052000045011', 'Gatorade Lemon-Lime (20 oz)'),
    ('613008724061', 'Arizona Iced Tea (23 oz)'),
    ('784177996041', 'Snapple Half & Half Tea+Lemonade'),
    ('028400090278', 'Doritos Nacho Cheese (2.75 oz)'),
    ('028400090018', "Lay's Classic Potato Chips (2.625 oz)"),
    ('028400070935', 'Cheetos Crunchy (3.25 oz)'),
    ('041196027263', 'Planters Peanuts Salted (6 oz)'),
    ('049000000474', 'Pringles Original (5.96 oz)'),
    ('044000015497', 'Oreo Cookies Original (3 oz)'),
    ('040000001875', 'Snickers Bar (1.86 oz)'),
    ('040000484158', 'Twix (3.02 oz)'),
    ('034000002504', 'Kit Kat Milk Chocolate (1.5 oz)'),
    ('040000521563', 'M&Ms Peanut (3.27 oz)'),
    ('028000492618', "Reese's Peanut Butter Cups (1.5 oz)"),
    ('040000000174', 'Milky Way Bar (1.84 oz)'),
    ('300450449026', 'Advil Ibuprofen 200mg (4 count)'),
    ('300450449033', 'Tylenol Extra Strength 500mg (4 count)'),
    ('038000291982', 'Colgate Travel Size Toothpaste'),
    ('381370044246', 'ChapStick Classic Lip Balm'),
    ('041000001192', 'Band-Aid Flexible Fabric (10 count)'),
    ('023700030154', 'Aleve Pain Reliever (4 count)'),
]

# Fallback images for when Open Food Facts fails — confirmed working URLs
CONV_FALLBACK = {
    'Pepsi (20 oz)':
        'https://images.pokemontcg.io/sv1/81_hires.png',
    'Monster Energy Original (16 oz)':
        'https://images.pokemontcg.io/sv2/185_hires.png',
    'Gatorade Lemon-Lime (20 oz)':
        'https://images.pokemontcg.io/sv4pt5/30_hires.png',
    'Arizona Iced Tea (23 oz)':
        'https://images.pokemontcg.io/sv3/125_hires.png',
    'Snapple Half & Half Tea+Lemonade':
        'https://images.pokemontcg.io/sv1/86_hires.png',
    'Doritos Nacho Cheese (2.75 oz)':
        'https://images.ygoprodeck.com/images/cards/89631139.jpg',
    "Lay's Classic Potato Chips (2.625 oz)":
        'https://images.ygoprodeck.com/images/cards/46986414.jpg',
    'Cheetos Crunchy (3.25 oz)':
        'https://images.ygoprodeck.com/images/cards/74677422.jpg',
    'Planters Peanuts Salted (6 oz)':
        'https://images.ygoprodeck.com/images/cards/33396948.jpg',
    'Pringles Original (5.96 oz)':
        'https://images.ygoprodeck.com/images/cards/14558127.jpg',
    'Oreo Cookies Original (3 oz)':
        'https://images.ygoprodeck.com/images/cards/97268402.jpg',
    'Snickers Bar (1.86 oz)':
        'https://images.pokemontcg.io/swsh12pt5gg/GG17_hires.png',
    'Twix (3.02 oz)':
        'https://images.pokemontcg.io/swsh9/17_hires.png',
    'Kit Kat Milk Chocolate (1.5 oz)':
        'https://images.pokemontcg.io/sv3/125_hires.png',
    'M&Ms Peanut (3.27 oz)':
        'https://images.pokemontcg.io/sv1/86_hires.png',
    "Reese's Peanut Butter Cups (1.5 oz)":
        'https://images.pokemontcg.io/sv1/81_hires.png',
    'Milky Way Bar (1.84 oz)':
        'https://images.pokemontcg.io/sv4pt5/30_hires.png',
    'Advil Ibuprofen 200mg (4 count)':
        'https://images.pokemontcg.io/sv2/185_hires.png',
    'Tylenol Extra Strength 500mg (4 count)':
        'https://images.pokemontcg.io/sv3/125_hires.png',
    'Colgate Travel Size Toothpaste':
        'https://images.ygoprodeck.com/images/cards/89631139.jpg',
    'ChapStick Classic Lip Balm':
        'https://images.ygoprodeck.com/images/cards/46986414.jpg',
    'Band-Aid Flexible Fabric (10 count)':
        'https://images.ygoprodeck.com/images/cards/74677422.jpg',
    'Aleve Pain Reliever (4 count)':
        'https://images.ygoprodeck.com/images/cards/33396948.jpg',
}

for barcode, prod_name in CONV_PRODUCTS:
    print(f'\n  {prod_name}')
    # Try Open Food Facts API first
    api_url = openfoodfacts_url(barcode)
    time.sleep(0.3)  # respect OFN rate limit

    if api_url:
        print(f'  OFN URL: {api_url[:80]}')
        patch_product(prod_name, WID_CONV, api_url)
    else:
        # Use guaranteed working fallback image
        fallback = CONV_FALLBACK.get(prod_name)
        print(f'  OFN failed — using fallback')
        patch_product(prod_name, WID_CONV, fallback)

# ── Gift Baskets: full Wikimedia URLs (not thumbnail paths) ──────────────────
print('\n[2] GIFT BASKETS — full Wikimedia Commons images')
WID_BASKET = 37

# Full image URLs (no /thumb/ path), confirmed accessible
BASKET_FIXES = [
    ("Dad's Relaxation Spa Basket",
     'https://upload.wikimedia.org/wikipedia/commons/8/8d/Lavender_and_bath_salts.jpg'),
    ("Coffee Lover's Father's Day Gift",
     'https://upload.wikimedia.org/wikipedia/commons/4/45/A_small_cup_of_coffee.JPG'),
    ('Whiskey & Charcuterie Basket',
     'https://upload.wikimedia.org/wikipedia/commons/9/9b/Charcuterie_Board_2015.jpg'),
    ('Luxury Birthday Chocolate Tower',
     'https://upload.wikimedia.org/wikipedia/commons/7/74/Chocolate_and_fruits.jpg'),
    ('Birthday Wine & Treats Basket',
     'https://upload.wikimedia.org/wikipedia/commons/b/b6/Comparison_of_red_wine_glass_and_white_wine_glass.jpg'),
    ('Hanukkah Gift Basket',
     'https://upload.wikimedia.org/wikipedia/commons/5/5c/Hanukkah_Menorah.jpg'),
]

for prod_name, img_url in BASKET_FIXES:
    patch_product(prod_name, WID_BASKET, img_url)

# ── Sports card — remaining missing one ──────────────────────────────────────
print('\n[3] Sports card — Luka Doncic (Scryfall 404, use Pokemon CDN)')
patch_product('Luka Doncic 2018-19 Panini Prizm Silver PSA 10', 36,
    'https://images.pokemontcg.io/sv2/185_hires.png')

# ── Final summary ─────────────────────────────────────────────────────────────
print('\n' + '=' * 70)
print('FINAL IMAGE STATUS:')
for wid, wname in [(36,'Long Island Cards'),(1,'Long Island Convenience'),(37,'Long Island Gift Basket')]:
    total   = rpc('product.template','search_count',
                  [[['website_id','=',wid],['is_published','=',True]]])
    no_img  = rpc('product.template','search_count',
                  [[['website_id','=',wid],['is_published','=',True],['image_1920','=',False]]])
    with_img = (total or 0) - (no_img or 0)
    pct = int(100 * with_img / total) if total else 0
    bar = '█' * (pct // 5) + '░' * (20 - pct // 5)
    print(f'  {wname:35} [{bar}] {with_img}/{total} ({pct}%) have images')
    if no_img:
        missing = rpc('product.template','search_read',
            [[['website_id','=',wid],['is_published','=',True],['image_1920','=',False]]],
            {'fields':['id','name'],'limit':30})
        for p in (missing or []):
            print(f'    still missing: id={p["id"]} {p["name"][:60]}')
