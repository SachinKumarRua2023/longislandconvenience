#!/usr/bin/env python3
"""
Create product.public.category records for the shop,
link all products to the correct public category,
then update homepage + header views with correct category IDs.
"""
import xmlrpc.client, sys

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"
SITE_ID = 36

def connect():
    uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
    if not uid: sys.exit("Auth failed")
    m = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    print("Connected UID", uid)
    return m, uid

def xc(m, uid, model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

def get_or_create_pub_cat(m, uid, name, parent_id=None):
    domain = [('name','=',name)]
    if parent_id:
        domain.append(('parent_id','=',parent_id))
    existing = xc(m, uid, 'product.public.category','search_read',[domain],{'fields':['id'],'limit':1})
    if existing:
        return existing[0]['id']
    vals = {'name': name}
    if parent_id:
        vals['parent_id'] = parent_id
    return xc(m, uid, 'product.public.category','create',[vals])

def main():
    m, uid = connect()

    # ── 1. Create public categories ───────────────────────────
    print("\n[1] Creating website (public) categories...")
    cats = {}

    # Top level
    cats['Sports Cards']         = get_or_create_pub_cat(m, uid, 'Sports Cards')
    cats['Trading Card Games']   = get_or_create_pub_cat(m, uid, 'Trading Card Games')
    cats['Graded Cards']         = get_or_create_pub_cat(m, uid, 'Graded Cards')
    cats['Sealed Products']      = get_or_create_pub_cat(m, uid, 'Sealed Products')
    cats['Card Accessories']     = get_or_create_pub_cat(m, uid, 'Card Accessories')

    # Children of Sports Cards
    cats['Baseball Cards']       = get_or_create_pub_cat(m, uid, 'Baseball Cards',      cats['Sports Cards'])
    cats['Basketball Cards']     = get_or_create_pub_cat(m, uid, 'Basketball Cards',    cats['Sports Cards'])
    cats['Football Cards']       = get_or_create_pub_cat(m, uid, 'Football Cards',      cats['Sports Cards'])
    cats['Hockey Cards']         = get_or_create_pub_cat(m, uid, 'Hockey Cards',        cats['Sports Cards'])

    # Children of Trading Card Games
    cats['Pokemon Cards']        = get_or_create_pub_cat(m, uid, 'Pokemon Cards',       cats['Trading Card Games'])
    cats['Magic: The Gathering'] = get_or_create_pub_cat(m, uid, 'Magic: The Gathering',cats['Trading Card Games'])
    cats['Yu-Gi-Oh! Cards']      = get_or_create_pub_cat(m, uid, 'Yu-Gi-Oh! Cards',    cats['Trading Card Games'])

    # Children of Graded Cards
    cats['PSA Graded']           = get_or_create_pub_cat(m, uid, 'PSA Graded',          cats['Graded Cards'])
    cats['BGS Graded']           = get_or_create_pub_cat(m, uid, 'BGS Graded',          cats['Graded Cards'])

    # Children of Sealed Products
    cats['Booster Boxes']        = get_or_create_pub_cat(m, uid, 'Booster Boxes',       cats['Sealed Products'])
    cats['Elite Trainer Boxes']  = get_or_create_pub_cat(m, uid, 'Elite Trainer Boxes', cats['Sealed Products'])

    # Accessories children
    cats['Sleeves & Top Loaders']= get_or_create_pub_cat(m, uid, 'Sleeves & Top Loaders',cats['Card Accessories'])
    cats['Binders & Albums']     = get_or_create_pub_cat(m, uid, 'Binders & Albums',    cats['Card Accessories'])

    for name, cid in cats.items():
        print(f"  [{cid:4}] {name}")

    # ── 2. Map product names → public category ────────────────
    PRODUCT_CAT_MAP = {
        "2024-25 Panini Prizm Basketball Hobby Box":         "Basketball Cards",
        "2024 Topps Baseball Series 1 Hobby Box":            "Baseball Cards",
        "2024-25 Panini Donruss Football Hobby Box":         "Football Cards",
        "2024-25 Upper Deck Hockey Series 1 Hobby Box":      "Hockey Cards",
        "Pokemon Scarlet & Violet Prismatic Evolutions Booster Box": "Booster Boxes",
        "Pokemon Elite Trainer Box — Scarlet & Violet":      "Elite Trainer Boxes",
        "Pokemon Booster Pack — Assorted Sets":              "Pokemon Cards",
        "Pokemon Charizard ex (PSA 10) — Obsidian Flames":   "PSA Graded",
        "Magic: The Gathering — Duskmourn Booster Box (Draft)": "Magic: The Gathering",
        "MTG Commander Precon Deck — Assorted":              "Magic: The Gathering",
        "Yu-Gi-Oh! Burst Protocol Booster Box":              "Yu-Gi-Oh! Cards",
        "Yu-Gi-Oh! Blue-Eyes White Dragon (PSA 9) — Starter Deck": "PSA Graded",
        "One Piece Card Game — Two Legends Booster Box":     "Trading Card Games",
        "Mike Trout 2011 Topps Update Rookie (PSA 10)":      "PSA Graded",
        "Luka Doncic 2018-19 Panini Prizm Rookie (BGS 9.5)": "BGS Graded",
        "Ultra Pro 9-Pocket Card Binder (360 Cards)":        "Binders & Albums",
        "Top Loader Pack — 3x4 inch (25 pack)":              "Sleeves & Top Loaders",
        "Perfect Fit Card Sleeves — 100 pack":               "Sleeves & Top Loaders",
        "Bicycle Standard Playing Cards — 2 Deck Set":       "Card Accessories",
        "Long Island Cards Starter Bundle — Sports":         "Sports Cards",
        "Long Island Cards Starter Bundle — TCG":            "Trading Card Games",
    }

    print("\n[2] Linking products to public categories...")
    updated = 0
    for prod_name, cat_name in PRODUCT_CAT_MAP.items():
        prods = xc(m, uid, 'product.template','search_read',
            [[('name','=',prod_name)]],{'fields':['id','name'],'limit':1})
        if not prods:
            print(f"  NOT FOUND: {prod_name[:50]}")
            continue
        pid = prods[0]['id']
        pub_cat_id = cats.get(cat_name)
        if pub_cat_id:
            xc(m, uid, 'product.template','write',[[pid],{
                'public_categ_ids': [(6, 0, [pub_cat_id])],
                'website_id': SITE_ID,
                'is_published': True,
            }])
            print(f"  [{pid}] {prod_name[:40]:40} -> {cat_name}")
            updated += 1
    print(f"  Total updated: {updated}")

    # ── 3. Print category ID map for URLs ─────────────────────
    print("\n[3] Category URL mapping:")
    key_cats = {
        'Sports Cards':          cats['Sports Cards'],
        'Pokemon Cards':         cats['Pokemon Cards'],
        'Magic: The Gathering':  cats['Magic: The Gathering'],
        'Yu-Gi-Oh! Cards':       cats['Yu-Gi-Oh! Cards'],
        'Graded Cards':          cats['Graded Cards'],
        'Card Accessories':      cats['Card Accessories'],
        'Trading Card Games':    cats['Trading Card Games'],
        'Sealed Products':       cats['Sealed Products'],
    }
    for name, cid in key_cats.items():
        print(f"  /shop?category={cid}  =>  {name}")

    return cats

if __name__ == '__main__':
    m, uid = connect()
    main()
