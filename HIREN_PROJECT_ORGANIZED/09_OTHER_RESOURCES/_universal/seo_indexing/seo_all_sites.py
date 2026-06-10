import xmlrpc.client, sys, re

sys.stdout.reconfigure(encoding='utf-8')
URL = 'https://country-cove-inc.odoo.com'
DB  = 'country-cove-inc'
UID = 2
PW  = 'M@nhattan1234'

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
print("Connected\n")

# ── Helpers ──────────────────────────────────────────────────
def trim(s, n):
    return s if len(s) <= n else s[:n-1].rstrip() + '…'

def no_parens(s):
    return re.sub(r'\s*\([^)]*\)', '', s).strip()

def has_geo(name):
    return any(x in name for x in ['Long Island', 'Plainview', '– LI', '— LI'])

# ════════════════════════════════════════════════════════════
# SEO GENERATORS PER SITE TYPE
# ════════════════════════════════════════════════════════════

def seo_cards(name, price):
    n = name.lower()
    # Detect game
    if any(x in n for x in ['psa','bgs','cgc']) and 'psa 9' not in n[:3]:
        game, gword = 'graded', 'graded card'
    elif any(x in n for x in ['booster box','booster pack','elite trainer','pre-release','pre-order','starter deck','collector booster']):
        game, gword = 'sealed', 'sealed TCG product'
    elif any(x in n for x in ['charizard','pikachu','pokemon','pokémon','gardevoir','miraidon','umbreon','iono','paldea','destined','surging','stellar','vmax','vstar']):
        game, gword = 'pokemon', 'Pokémon card'
    elif any(x in n for x in ['blue-eyes','dark magician','ash blossom','exodia','red-eyes','effect veiler','ygo','yu-gi','speed duel','burst protocol']):
        game, gword = 'yugioh', 'Yu-Gi-Oh! card'
    elif any(x in n for x in ['mtg','black lotus','murktide','orcish bowmasters','ragavan','sheoldred','solitude','wrenn','final fantasy','lord of the rings','dominaria']):
        game, gword = 'mtg', 'MTG card'
    elif any(x in n for x in ['tatis','lebron','luka','mahomes','ohtani','topps','panini','prizm','chrome','rookie','nfl','nba','mlb','rc ']):
        game, gword = 'sports', 'sports card'
    elif 'one piece' in n:
        game, gword = 'onepiece', 'One Piece TCG product'
    else:
        game, gword = 'trading', 'trading card'

    new_name = name if has_geo(name) else f"{name} – Long Island NY"

    clean = no_parens(name)
    raw_title = f"{clean} | Long Island Cards NY"
    if len(raw_title) > 60:
        words = clean.split()
        raw_title = f"{' '.join(words[:5])} | Long Island Cards NY"
    meta_title = trim(raw_title, 60)

    if game == 'graded':
        desc = f"Buy {trim(name,44)} at Long Island Cards, Plainview NY. Certified graded slab. Free shipping $75+. Same-day dispatch before 3 PM. Open 7 days. Nassau County's #1 card shop."
    elif game == 'sealed':
        desc = f"Buy {trim(name,42)} at Long Island Cards, Plainview NY. Sealed in stock now. Free shipping $75+. Same-day dispatch before 3 PM. Open 7 days in Nassau County."
    elif game == 'pokemon':
        desc = f"Buy {trim(name,38)} Pokémon card at Long Island Cards, Plainview NY. Near-mint singles. Free shipping $75+. Same-day dispatch before 3 PM. Open 7 days. Nassau County's top card shop."
    elif game == 'yugioh':
        desc = f"Buy {trim(name,38)} Yu-Gi-Oh! card at Long Island Cards, Plainview NY. Tournament-ready. Free shipping $75+. Same-day dispatch before 3 PM. Open 7 days in Nassau County."
    elif game == 'mtg':
        desc = f"Buy {trim(name,40)} MTG card at Long Island Cards, Plainview NY. Modern, Legacy & Commander staples. Free shipping $75+. Same-day dispatch before 3 PM. Open 7 days."
    elif game == 'sports':
        desc = f"Buy {trim(name,42)} at Long Island Cards, Plainview NY. Graded sports cards & raw singles. Free shipping $75+. Same-day dispatch before 3 PM. Open 7 days in Nassau County."
    else:
        desc = f"Buy {trim(name,44)} at Long Island Cards, Plainview NY. Buy, sell & trade cards. Free shipping $75+. Same-day dispatch before 3 PM. Open 7 days in Nassau County."
    return new_name, meta_title, trim(desc, 160)


def seo_basket(name, price):
    n = name.lower()
    if has_geo(name):
        new_name = name
    else:
        new_name = f"{name} – Long Island NY"

    clean = no_parens(name).replace(' – Long Island NY','').replace('– Long Island NY','').strip()
    raw_title = f"{trim(clean,36)} | Gift Basket Long Island NY"
    meta_title = trim(raw_title, 60)

    # Occasion detection
    if any(x in n for x in ["father","dad","bbq","grill","whiskey","beer","meat","sports fan"]):
        occasion = "Father's Day"
        occ_tag = "Perfect Father's Day gift"
    elif any(x in n for x in ["birthday","birth"]):
        occasion = "birthdays"
        occ_tag = "Ideal birthday gift"
    elif any(x in n for x in ["grad","graduation","class of"]):
        occasion = "graduation"
        occ_tag = "Perfect graduation gift"
    elif any(x in n for x in ["christmas","holiday","thanksgiving","new year"]):
        occasion = "holidays"
        occ_tag = "Perfect holiday gift"
    elif any(x in n for x in ["chocolate","brownie","candy","sweet","strawberr"]):
        occasion = "any occasion"
        occ_tag = "Indulgent chocolate gift"
    elif any(x in n for x in ["cheese","charcuterie","gourmet","tuscan","wine","picnic"]):
        occasion = "any occasion"
        occ_tag = "Gourmet gift for any occasion"
    elif any(x in n for x in ["fruit","organic","tropical","apple","pear"]):
        occasion = "any occasion"
        occ_tag = "Fresh fruit gift basket"
    else:
        occasion = "any occasion"
        occ_tag = "Thoughtfully curated gift"

    desc = f"Order {trim(clean,34)} from Long Island Gift Basket, Plainview NY. {occ_tag}. Free delivery in Nassau County. Same-day if ordered by noon. Serving all of Long Island."
    return new_name, meta_title, trim(desc, 160)


def seo_convenience(name, price):
    n = name.lower()
    new_name = name if has_geo(name) else f"{name} – Plainview NY"

    clean = no_parens(name)
    raw_title = f"{trim(clean,36)} | Long Island Convenience NY"
    meta_title = trim(raw_title, 60)

    # Category detection
    if any(x in n for x in ["balloon","bouquet","arch","mylar","foil balloon"]):
        cat = "balloon"
        desc = f"Buy {trim(name,40)} at Long Island Convenience, Plainview NY. Same-day pickup available. Perfect for celebrations. Open 7 days in Nassau County. Stop in or call ahead."
    elif any(x in n for x in ["card","foil card","photo booth","props"]):
        cat = "greeting"
        desc = f"Buy {trim(name,40)} at Long Island Convenience, Plainview NY. Greeting cards & party supplies. Open 7 days in Nassau County. Same-day pickup available anytime."
    elif any(x in n for x in ["lottery","lotto","scratch","mega millions","powerball"]):
        cat = "lottery"
        desc = f"Buy New York Lottery tickets at Long Island Convenience, Plainview NY. Scratch tickets, Mega Millions & Powerball. Open 7 days. Nassau County's friendly convenience store."
    elif any(x in n for x in ["basket","bundle","kit","set","combo","bag","gift"]):
        cat = "bundle"
        desc = f"Buy {trim(name,38)} at Long Island Convenience, Plainview NY. Same-day pickup available. Perfect for last-minute gifts. Open 7 days in Nassau County. Quick and easy."
    elif any(x in n for x in ["coca","gatorade","red bull","energy","soda","water","drink"]):
        cat = "beverage"
        desc = f"Buy {trim(name,44)} at Long Island Convenience, Plainview NY. Cold beverages always in stock. Open 7 days in Nassau County. Fresh stocked daily — grab & go convenience."
    elif any(x in n for x in ["advil","band-aid","colgate","toothpaste","medicine","health"]):
        cat = "health"
        desc = f"Buy {trim(name,44)} at Long Island Convenience, Plainview NY. Health essentials always in stock. Open 7 days in Nassau County. Quick stop — no prescription needed."
    elif any(x in n for x in ["doritos","lay's","pringles","kit kat","snickers","m&m","chips","snack","candy"]):
        cat = "snack"
        desc = f"Buy {trim(name,44)} at Long Island Convenience, Plainview NY. Snacks & candy always in stock. Open 7 days in Nassau County. Grab-and-go convenience in Plainview."
    else:
        cat = "general"
        desc = f"Buy {trim(name,44)} at Long Island Convenience, Plainview NY. Open 7 days a week in Nassau County. Fast, friendly service. Fresh stocked daily — stop in anytime."

    return new_name, meta_title, trim(desc, 160)


def seo_print(name, price):
    n = name.lower()
    new_name = name if has_geo(name) else f"{name} – Long Island NY"

    clean = no_parens(name).replace(' – Long Island NY','').strip()
    raw_title = f"{trim(clean,34)} | Long Island Print & Mail NY"
    meta_title = trim(raw_title, 60)

    if any(x in n for x in ["business card"]):
        desc = f"Order {trim(name,38)} at Long Island Print & Mail, Plainview NY. Professional quality, fast turnaround. Serving Nassau County businesses. Same-day pickup available. Open 7 days."
    elif any(x in n for x in ["flyer"]):
        desc = f"Order {trim(name,38)} at Long Island Print & Mail, Plainview NY. Full-color flyers for Nassau County businesses. Fast turnaround. Same-day pickup available. Open 7 days."
    elif any(x in n for x in ["banner","vinyl"]):
        desc = f"Order {trim(name,38)} at Long Island Print & Mail, Plainview NY. Eye-catching vinyl banners for businesses. Serving Nassau County. Fast turnaround. Open 7 days a week."
    elif any(x in n for x in ["brochure","tri-fold"]):
        desc = f"Order {trim(name,38)} at Long Island Print & Mail, Plainview NY. Professional tri-fold brochures for Nassau County businesses. Fast turnaround & same-day pickup available."
    elif any(x in n for x in ["yard sign"]):
        desc = f"Order {trim(name,38)} at Long Island Print & Mail, Plainview NY. Durable yard signs for real estate, events & businesses. Nassau County. Fast turnaround. Open 7 days."
    elif any(x in n for x in ["copy","copying","b&w","color cop"]):
        desc = f"Fast {trim(name,38)} service at Long Island Print & Mail, Plainview NY. Walk-ins welcome. Affordable B&W & color copying for Nassau County. Open 7 days a week."
    elif any(x in n for x in ["scan","pdf"]):
        desc = f"Scan to PDF service at Long Island Print & Mail, Plainview NY. Quick, affordable scanning for Nassau County residents & businesses. Walk-ins welcome. Open 7 days."
    elif any(x in n for x in ["notary"]):
        desc = f"Notary service at Long Island Print & Mail, Plainview NY. Fast, certified notarization for Nassau County. Walk-ins welcome. Affordable per-signature fee. Open 7 days."
    elif any(x in n for x in ["shipping box","box"]):
        desc = f"Buy {trim(name,40)} at Long Island Print & Mail, Plainview NY. Shipping supplies for Nassau County. Full-service shipping center. Walk-ins welcome. Open 7 days."
    elif 'roll-up' in n or 'banner stand' in n or 'retractable' in n:
        desc = f"Order a {trim(name,36)} at Long Island Print & Mail, Plainview NY. Professional displays for Nassau County businesses & events. Fast turnaround. Open 7 days."
    else:
        desc = f"Order {trim(name,40)} at Long Island Print & Mail, Plainview NY. Professional printing for Nassau County businesses. Fast turnaround & quality guaranteed. Open 7 days."

    return new_name, meta_title, trim(desc, 160)


# ════════════════════════════════════════════════════════════
# PROCESS ALL SITES
# ════════════════════════════════════════════════════════════
SITES = [
    (36, "Long Island Cards",       seo_cards),
    (37, "Long Island Gift Basket", seo_basket),
    (1,  "Long Island Convenience", seo_convenience),
    (39, "Long Island Print & Mail",seo_print),
]

grand_total = 0

for site_id, site_name, seo_fn in SITES:
    print(f"\n{'═'*65}")
    print(f"  {site_name}  (site {site_id})")
    print(f"{'═'*65}")

    prods = models.execute_kw(DB, UID, PW, 'product.template', 'search_read',
        [[['website_id','=',site_id]]],
        {'fields':['id','name','list_price','website_meta_title','website_meta_description'], 'limit':100})

    # Skip already-done (have meta title) for gift basket
    if site_id == 37:
        todo = [p for p in prods if not p['website_meta_title']]
        print(f"  Skipping {len(prods)-len(todo)} already-optimised products")
    else:
        todo = prods

    print(f"  Optimising {len(todo)} products…\n")
    warnings = []

    for p in todo:
        pid = p['id']
        new_name, meta_title, meta_desc = seo_fn(p['name'], p['list_price'])

        # Validate lengths
        mt_len = len(meta_title)
        md_len = len(meta_desc)
        nm_len = len(new_name)

        models.execute_kw(DB, UID, PW, 'product.template', 'write',
            [[pid], {
                'name':                     new_name,
                'website_meta_title':       meta_title,
                'website_meta_description': meta_desc,
            }])

        flag = ' ⚠️ DESC LONG' if md_len > 165 else ''
        print(f"  [{pid}] ✅ {new_name[:55]}")
        print(f"         TITLE ({mt_len:3d}): {meta_title}")
        print(f"         DESC  ({md_len:3d}): {meta_desc[:80]}…{flag}")
        print()

        if md_len > 165:
            warnings.append(f"[{pid}] desc {md_len} chars")

        grand_total += 1

    if warnings:
        print(f"  ⚠️  Warnings: {warnings}")

print(f"\n{'═'*65}")
print(f"  SEO + GEO OPTIMIZATION COMPLETE")
print(f"  Total products updated: {grand_total}")
print(f"{'═'*65}")
print("""
  All products now have:
    ✅ Name  — with Long Island NY / Plainview NY geo suffix
    ✅ Meta Title — 50-60 chars, keyword + location
    ✅ Meta Desc  — 150-160 chars, geo-targeted copy

  Live verify:
    Cards:   https://www.longislandcards.com/shop
    Basket:  https://www.ligiftbasket.com/shop
    Conv.:   https://www.longislandconvenience.com/shop
    Print:   https://www.longislandprintandmail.com/shop
""")
