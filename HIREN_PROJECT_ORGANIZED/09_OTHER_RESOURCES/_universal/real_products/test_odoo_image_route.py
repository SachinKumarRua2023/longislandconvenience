#!/usr/bin/env python3
"""
POC: Fetch 3 real card images per category from free APIs → insert into Odoo (website_id=36).
Tests the complete route: API download → base64 → product.template create → verify on site.

Categories used (already exist):
  Pokemon TCG   → Trading Card Games / Pokemon Cards     (categ_id=100)
  MTG           → Trading Card Games / Magic: The Gath.  (categ_id=101)
  Yu-Gi-Oh!     → Trading Card Games / Yu-Gi-Oh! Cards   (categ_id=102)
  Sports        → Country Cove Sports & Cards / Baseball  (categ_id=42)
"""
import xmlrpc.client, base64, requests, sys, time, json
sys.stdout.reconfigure(encoding='utf-8')

# ── Odoo connection ──────────────────────────────────────────────────────────
URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"
SITE = 36  # Long Island Cards

uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
m   = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc  = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)
print(f"✓ Odoo connected  UID={uid}  site={SITE}\n")

HDRS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}

def dl_b64(url, label=""):
    """Download image URL → base64 string.  Returns (b64_str, kb) or (None, 0)."""
    if not url:
        return None, 0
    try:
        r = requests.get(url, headers=HDRS, timeout=15, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 500:
            b64 = base64.b64encode(r.content).decode()
            kb  = len(r.content) // 1024
            print(f"    ↓ {label} {kb}KB  ({url[:70]})")
            return b64, kb
        print(f"    ✗ {label} HTTP {r.status_code} ({url[:60]})")
    except Exception as e:
        print(f"    ✗ {label} error: {e}")
    return None, 0

def create_product(name, price, categ_id, b64_img, description, badge="New"):
    """Create product.template on site 36.  Returns new product ID or None."""
    vals = {
        'name':             name,
        'type':             'consu',
        'sale_ok':          True,
        'list_price':       price,
        'standard_price':   round(price * 0.5, 2),
        'categ_id':         categ_id,
        'description_sale': description,
        'website_id':       SITE,
        'is_published':     True,
    }
    if b64_img:
        vals['image_1920'] = b64_img
    try:
        pid = xc('product.template', 'create', [vals])
        return pid
    except Exception as e:
        print(f"    ✗ create failed: {str(e)[:200]}")
        return None

# ── SECTION 1: Pokemon TCG (pokemontcg.io) ─────────────────────────────────
print("=" * 60)
print("1. POKEMON TCG  →  categ_id=100  (pokemontcg.io)")
print("=" * 60)

poke_url = ("https://api.pokemontcg.io/v2/cards"
            "?q=supertype:Pokémon+rarity:Rare+set.series:Scarlet+%26+Violet"
            "&page=1&pageSize=3"
            "&select=name,images,set,rarity,tcgplayer")
try:
    poke_resp = requests.get(poke_url, timeout=20).json()
    poke_cards = poke_resp.get('data', [])
    print(f"  API returned {len(poke_cards)} cards")
except Exception as e:
    poke_cards = []
    print(f"  API error: {e}")

poke_created = []
for card in poke_cards[:3]:
    name     = card.get('name', 'Pokemon Card')
    set_name = card.get('set', {}).get('name', 'Scarlet & Violet')
    rarity   = card.get('rarity', 'Rare')
    price    = (card.get('tcgplayer', {}).get('prices', {})
                .get('holoRare', {}).get('market')
                or card.get('tcgplayer', {}).get('prices', {})
                .get('normal', {}).get('market') or 9.99)
    price    = float(price) if price else 9.99
    img_url  = card.get('images', {}).get('large') or card.get('images', {}).get('small')

    print(f"\n  Card: {name}  |  Set: {set_name}  |  ${price:.2f}")
    b64, kb = dl_b64(img_url, name[:30])

    desc  = f"<p><strong>{name}</strong> — {rarity} from <em>{set_name}</em>.</p>"
    desc += f"<p>Authentic Pokémon Trading Card Game single. Market price ${price:.2f}.</p>"
    desc += f"<p>Condition: Near Mint. Ships in protective sleeve and toploader.</p>"

    pid = create_product(f"[POC] {name} ({set_name})", price, 100, b64, desc)
    if pid:
        poke_created.append({'id': pid, 'name': name, 'has_img': bool(b64)})
        print(f"    ✓ Created product ID {pid}  image={'yes' if b64 else 'NO'}")
    time.sleep(0.3)

print(f"\n  Pokemon: {len(poke_created)}/3 created")

# ── SECTION 2: Magic: The Gathering (Scryfall) ──────────────────────────────
print("\n" + "=" * 60)
print("2. MAGIC: THE GATHERING  →  categ_id=101  (scryfall.com)")
print("=" * 60)

mtg_url = ("https://api.scryfall.com/cards/search"
           "?q=f:modern+type:creature+r:rare+lang:en"
           "&unique=cards&order=edhrec&dir=desc&page=1")
try:
    mtg_resp  = requests.get(mtg_url, timeout=20).json()
    mtg_cards = mtg_resp.get('data', [])
    print(f"  API returned {len(mtg_cards)} cards")
except Exception as e:
    mtg_cards = []
    print(f"  API error: {e}")

mtg_created = []
for card in mtg_cards[:3]:
    name     = card.get('name', 'MTG Card')
    set_name = card.get('set_name', 'Modern')
    rarity   = card.get('rarity', 'rare').title()
    price    = float(card.get('prices', {}).get('usd') or 4.99)
    oracle   = (card.get('oracle_text') or '')[:140]
    img_url  = (card.get('image_uris', {}).get('normal')
                or card.get('image_uris', {}).get('large'))

    print(f"\n  Card: {name}  |  Set: {set_name}  |  ${price:.2f}")
    b64, kb = dl_b64(img_url, name[:30])

    desc  = f"<p><strong>{name}</strong> — {rarity} from <em>{set_name}</em>.</p>"
    if oracle:
        desc += f"<p><em>{oracle}</em></p>"
    desc += f"<p>Format: Modern Legal. Condition: Near Mint. Market price ${price:.2f}.</p>"

    pid = create_product(f"[POC] {name} ({set_name})", price, 101, b64, desc)
    if pid:
        mtg_created.append({'id': pid, 'name': name, 'has_img': bool(b64)})
        print(f"    ✓ Created product ID {pid}  image={'yes' if b64 else 'NO'}")
    time.sleep(0.3)

print(f"\n  MTG: {len(mtg_created)}/3 created")

# ── SECTION 3: Yu-Gi-Oh! (YGOPRODECK) ──────────────────────────────────────
print("\n" + "=" * 60)
print("3. YU-GI-OH!  →  categ_id=102  (ygoprodeck.com)")
print("=" * 60)

ygo_url = ("https://db.ygoprodeck.com/api/v7/cardinfo.php"
           "?type=Effect%20Monster&level=8&num=3&offset=0&sort=name")
try:
    ygo_resp  = requests.get(ygo_url, timeout=20).json()
    ygo_cards = ygo_resp.get('data', [])
    print(f"  API returned {len(ygo_cards)} cards")
except Exception as e:
    ygo_cards = []
    print(f"  API error: {e}")

ygo_created = []
for card in ygo_cards[:3]:
    name     = card.get('name', 'Yu-Gi-Oh! Card')
    card_desc= (card.get('desc') or '')[:140]
    set_info = card.get('card_sets', [{}])
    set_name = set_info[0].get('set_name', 'Effect Monster') if set_info else 'Effect Monster'
    price    = 7.99
    img_url  = ((card.get('card_images') or [{}])[0]).get('image_url')

    print(f"\n  Card: {name}  |  Set: {set_name}")
    b64, kb = dl_b64(img_url, name[:30])

    desc  = f"<p><strong>{name}</strong> — Level 8 Effect Monster.</p>"
    if card_desc:
        desc += f"<p><em>{card_desc}</em></p>"
    desc += f"<p>Authentic Yu-Gi-Oh! single. Ships in sleeve and toploader.</p>"

    pid = create_product(f"[POC] {name}", price, 102, b64, desc)
    if pid:
        ygo_created.append({'id': pid, 'name': name, 'has_img': bool(b64)})
        print(f"    ✓ Created product ID {pid}  image={'yes' if b64 else 'NO'}")
    time.sleep(0.3)

print(f"\n  YGO: {len(ygo_created)}/3 created")

# ── SECTION 4: Sports Cards (Baseball via Firecrawl placeholder) ────────────
print("\n" + "=" * 60)
print("4. SPORTS CARDS  →  categ_id=42  (hardcoded PoC cards)")
print("=" * 60)

SPORTS_CARDS = [
    {'name': '[POC] 2023 Topps Chrome Julio Rodriguez RC PSA 10',
     'set': '2023 Topps Chrome', 'price': 89.99,
     'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/240px-PNG_transparency_demonstration_1.png'},
    {'name': '[POC] 2024 Bowman Chrome Prospects Lot (x10)',
     'set': '2024 Bowman Chrome', 'price': 29.99, 'img': None},
    {'name': '[POC] 2022 Panini Prizm Shohei Ohtani Silver Prizm',
     'set': '2022 Panini Prizm', 'price': 49.99,
     'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Culinary_fruits_front_view.jpg/320px-Culinary_fruits_front_view.jpg'},
]

sports_created = []
for card in SPORTS_CARDS:
    print(f"\n  Card: {card['name']}")
    b64, kb = dl_b64(card.get('img'), card['name'][:30]) if card.get('img') else (None, 0)

    desc  = f"<p><strong>{card['name']}</strong> from <em>{card['set']}</em>.</p>"
    desc += f"<p>Authenticated trading card. Ships securely in toploader.</p>"

    pid = create_product(card['name'], card['price'], 42, b64, desc)
    if pid:
        sports_created.append({'id': pid, 'name': card['name'], 'has_img': bool(b64)})
        print(f"    ✓ Created product ID {pid}  image={'yes' if b64 else 'NO'}")
    time.sleep(0.3)

print(f"\n  Sports: {len(sports_created)}/3 created")

# ── FINAL REPORT ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FINAL REPORT")
print("=" * 60)
all_created = poke_created + mtg_created + ygo_created + sports_created
total = len(all_created)
with_img = sum(1 for p in all_created if p.get('has_img'))
print(f"  Products created : {total}/12")
print(f"  With real images : {with_img}/{total}")
print(f"  Missing images   : {total - with_img}/{total}")
print()
for p in all_created:
    img_tag = "🖼 IMG" if p.get('has_img') else "  ---"
    print(f"  [{img_tag}] ID {p['id']:5} | {p['name'][:55]}")

print(f"\n  Odoo Shop URL : {URL}/shop")
print(f"  Admin Products: {URL}/odoo/website  (filter by site 36)")
print()
print("Next step: visit the shop URL above and confirm images display correctly.")
print("If images show — route is confirmed. Then update n8n workflows to use xmlrpc.")
