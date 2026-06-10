#!/usr/bin/env python3
"""
Full local SEO domination for Hiren's Long Island stores.
1. Update all meta titles/desc to include "Hiren" brand
2. Create local keyword landing pages (Pokemon Cards Plainview NY, etc.)
3. Create competitor-beating blog posts
4. Create "About Hiren Chauhan" page
5. Add location-specific JSON-LD with exact Hiren branding
"""
import xmlrpc.client, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
m   = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
def xc(model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)
print(f"Connected UID {uid}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Update ALL meta tags to include "Hiren" brand signal
# ─────────────────────────────────────────────────────────────────────────────
print("\n== STEP 1: Updating meta tags with Hiren brand ==")

META_UPDATES = [
    # (page_id, website_id, meta_title, meta_desc, meta_kw)
    (5,  1,
     "Long Island Convenience | Hiren's Local Store Hub | Plainview NY",
     "Hiren's one-stop local hub in Plainview NY. Sports cards, gift baskets, print & mail, balloons, cigars, lotto. Long Island convenience store by Hiren Chauhan.",
     "hiren shop, hiren chauhan, hiren store long island, long island convenience plainview ny, hiren convenience store nassau county"),

    (44, 36,
     "Long Island Cards | Hiren's Card Shop | Pokemon Trading Cards Plainview NY",
     "Hiren's sports and trading card shop in Plainview NY. PSA graded cards, Pokemon, MTG, Yu-Gi-Oh!, One Piece. Hiren Chauhan's Long Island card store — Nassau County's top.",
     "hiren cards, hiren card shop, hiren chauhan cards, pokemon cards long island new york, trading cards plainview ny, PSA cards nassau county, sports cards near me plainview"),

    (47, 39,
     "Long Island Print & Mail | Hiren's Print Shop | Same-Day Printing Plainview NY",
     "Hiren's print and mail shop in Plainview NY. Same-day business cards, banners, flyers. Notary and shipping services. Hiren Chauhan's Long Island print shop.",
     "hiren print shop, hiren chauhan printing, print and mail long island, same day printing plainview ny, banner printing nassau county, business cards long island"),
]

for page_id, wid, title, desc, kw in META_UPDATES:
    result = xc('website.page', 'write', [[page_id], {
        'website_meta_title': title,
        'website_meta_description': desc,
        'website_meta_keywords': kw,
    }])
    print(f"  Page {page_id} (website {wid}): {result} — {title[:55]}...")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Update JSON-LD SEO views to include Hiren's name
# ─────────────────────────────────────────────────────────────────────────────
print("\n== STEP 2: Updating JSON-LD with Hiren branding ==")

layout_id = xc('ir.ui.view', 'search_read',
    [[['key', '=', 'website.layout']]], {'fields': ['id'], 'limit': 1})[0]['id']

SCHEMAS = [
    {
        'view_id': 3519, 'website_id': 1,
        'domain': 'https://www.longislandconvenience.com',
        'og_title': 'Long Island Convenience — Hiren Chauhan, Plainview NY',
        'meta_desc': "Hiren's one-stop local hub in Plainview NY. Sports cards, gift baskets, print & mail, balloons, cigars, lotto.",
        'schema': {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Long Island Convenience",
            "alternateName": ["Hiren Shop", "Hiren Store Long Island", "Hiren Chauhan Store"],
            "description": "Hiren Chauhan's one-stop convenience hub in Plainview, NY. Sports trading cards, PSA graded collectibles, gift baskets, balloon decor, print & mail services, cigars, tobacco, and lottery tickets.",
            "url": "https://www.longislandconvenience.com",
            "telephone": "+1-516-555-0100",
            "priceRange": "$",
            "founder": {"@type": "Person", "name": "Hiren Chauhan"},
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Plainview",
                "addressLocality": "Plainview",
                "addressRegion": "NY",
                "postalCode": "11803",
                "addressCountry": "US"
            },
            "geo": {"@type": "GeoCoordinates", "latitude": "40.7769", "longitude": "-73.4671"},
            "areaServed": [
                {"@type": "City", "name": "Plainview"},
                {"@type": "City", "name": "Hicksville"},
                {"@type": "City", "name": "Syosset"},
                {"@type": "City", "name": "Jericho"},
                {"@type": "City", "name": "Bethpage"},
                {"@type": "City", "name": "Levittown"},
                {"@type": "County", "name": "Nassau County"},
                {"@type": "State", "name": "Long Island NY"}
            ],
            "openingHours": ["Mo-Su 09:00-21:00"],
            "sameAs": [
                "https://www.longislandcards.com",
                "https://www.longislandprintandmail.com",
                "https://www.ligiftbasket.com",
                "https://www.longislandballoonsdecor.com"
            ]
        }
    },
    {
        'view_id': 3520, 'website_id': 36,
        'domain': 'https://www.longislandcards.com',
        'og_title': 'Long Island Cards — Hiren Chauhan | Pokemon Cards Plainview NY',
        'meta_desc': "Hiren's sports and trading card shop in Plainview NY. PSA graded cards, Pokemon, MTG, Yu-Gi-Oh!, One Piece.",
        'schema': {
            "@context": "https://schema.org",
            "@type": "Store",
            "name": "Long Island Cards",
            "alternateName": ["Hiren Cards", "Hiren Card Shop", "Hiren Chauhan Cards Long Island"],
            "description": "Hiren Chauhan's sports and trading card shop in Plainview, NY. Specializing in PSA and BGS graded cards, sports singles, Pokemon TCG, Magic: The Gathering, Yu-Gi-Oh!, and One Piece. Serving Nassau County and all of Long Island.",
            "url": "https://www.longislandcards.com",
            "telephone": "+1-516-555-0101",
            "priceRange": "$$",
            "founder": {"@type": "Person", "name": "Hiren Chauhan"},
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Plainview",
                "addressLocality": "Plainview",
                "addressRegion": "NY",
                "postalCode": "11803",
                "addressCountry": "US"
            },
            "geo": {"@type": "GeoCoordinates", "latitude": "40.7769", "longitude": "-73.4671"},
            "areaServed": [
                {"@type": "City", "name": "Plainview"},
                {"@type": "County", "name": "Nassau County"},
                {"@type": "State", "name": "Long Island NY"},
                {"@type": "City", "name": "New York"}
            ],
            "openingHours": ["Mo-Su 10:00-20:00"],
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Trading Cards Catalog",
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Product", "name": "PSA Graded Sports Cards"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Product", "name": "Pokemon TCG Cards Long Island"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Product", "name": "Magic The Gathering Cards"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Product", "name": "Yu-Gi-Oh Cards Plainview NY"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Product", "name": "One Piece TCG Cards"}}
                ]
            }
        }
    },
    {
        'view_id': 3521, 'website_id': 39,
        'domain': 'https://www.longislandprintandmail.com',
        'og_title': 'Long Island Print & Mail — Hiren Chauhan | Same-Day Printing Plainview NY',
        'meta_desc': "Hiren's print shop in Plainview NY. Same-day business cards, banners, flyers. Notary and shipping services.",
        'schema': {
            "@context": "https://schema.org",
            "@type": "PrintShop",
            "name": "Long Island Print & Mail",
            "alternateName": ["Hiren Print Shop", "Hiren Chauhan Printing Long Island"],
            "description": "Hiren Chauhan's professional print and mail shop in Plainview, NY. Same-day business cards, banners, flyers, shipping, notary services. Serving Nassau County and Long Island.",
            "url": "https://www.longislandprintandmail.com",
            "telephone": "+1-516-555-0102",
            "priceRange": "$$",
            "founder": {"@type": "Person", "name": "Hiren Chauhan"},
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Plainview",
                "addressLocality": "Plainview",
                "addressRegion": "NY",
                "postalCode": "11803",
                "addressCountry": "US"
            },
            "areaServed": [
                {"@type": "City", "name": "Plainview"},
                {"@type": "County", "name": "Nassau County"},
                {"@type": "State", "name": "Long Island NY"}
            ],
            "openingHours": ["Mo-Su 09:00-20:00"]
        }
    },
]

for s in SCHEMAS:
    jsonld = json.dumps(s['schema'], indent=2)
    arch = f'''<t name="SEO Head {s['website_id']}" t-name="website.seo_head_{s['website_id']}" inherit_id="website.layout">
  <xpath expr="//head" position="inside">
    <meta name="description" content="{s['meta_desc']}"/>
    <meta name="robots" content="index, follow"/>
    <meta property="og:type" content="website"/>
    <meta property="og:title" content="{s['og_title']}"/>
    <meta property="og:description" content="{s['meta_desc']}"/>
    <meta property="og:url" content="{s['domain']}"/>
    <meta name="twitter:card" content="summary_large_image"/>
    <meta name="twitter:title" content="{s['og_title']}"/>
    <meta name="twitter:description" content="{s['meta_desc']}"/>
    <script type="application/ld+json">
{jsonld}
    </script>
  </xpath>
</t>'''
    result = xc('ir.ui.view', 'write', [[s['view_id']], {'arch_db': arch}])
    print(f"  View {s['view_id']} (website {s['website_id']}) updated: {result}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Create "About Hiren Chauhan" page on convenience.com
# ─────────────────────────────────────────────────────────────────────────────
print("\n== STEP 3: Creating About Hiren Chauhan page ==")

about_hiren_content = '''
<div id="wrap">
  <section style="max-width:900px;margin:60px auto;padding:0 24px;font-family:system-ui,sans-serif;">

    <div style="text-align:center;margin-bottom:48px;">
      <h1 style="font-size:2.8em;font-weight:800;color:#1a1a2e;margin-bottom:12px;">
        Hiren Chauhan — Long Island Local Business Owner
      </h1>
      <p style="font-size:1.2em;color:#555;max-width:680px;margin:0 auto;">
        Building Long Island's premier family of local specialty stores — one store at a time.
      </p>
    </div>

    <div style="background:#f8f9ff;border-radius:16px;padding:40px;margin-bottom:40px;border-left:5px solid #1a3c6e;">
      <h2 style="color:#1a3c6e;font-size:1.6em;margin-top:0;">About Hiren</h2>
      <p style="font-size:1.1em;line-height:1.8;color:#333;">
        Hiren Chauhan is a Plainview, New York-based entrepreneur and proud Long Island business owner.
        Starting with a passion for collectibles and community service, Hiren built a growing family of
        specialty retail stores serving Nassau County and the wider Long Island area.
      </p>
      <p style="font-size:1.1em;line-height:1.8;color:#333;">
        Known locally as <strong>"Hiren's Shop"</strong> or <strong>"Hiren's Store on Long Island"</strong>,
        the collection of businesses spans sports trading cards, gift baskets, professional printing,
        balloon decor, and convenience retail — all operated from Plainview, NY 11803.
      </p>
    </div>

    <h2 style="color:#1a1a2e;font-size:1.8em;">Hiren's Long Island Stores</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:40px;">

      <a href="https://www.longislandcards.com" target="_blank"
         style="background:#fff;border:2px solid #1a3c6e;border-radius:12px;padding:24px;text-decoration:none;display:block;">
        <div style="font-size:2em;margin-bottom:8px;">&#127183;</div>
        <h3 style="color:#1a3c6e;margin:0 0 8px 0;">Hiren's Card Shop</h3>
        <p style="color:#555;margin:0;font-size:0.95em;">Long Island Cards — Sports &amp; Trading Cards, PSA Graded, Pokemon, MTG, Yu-Gi-Oh!, One Piece. Plainview, NY.</p>
      </a>

      <a href="https://www.longislandprintandmail.com" target="_blank"
         style="background:#fff;border:2px solid #2563eb;border-radius:12px;padding:24px;text-decoration:none;display:block;">
        <div style="font-size:2em;margin-bottom:8px;">&#128424;</div>
        <h3 style="color:#2563eb;margin:0 0 8px 0;">Hiren's Print Shop</h3>
        <p style="color:#555;margin:0;font-size:0.95em;">Long Island Print &amp; Mail — Same-day business cards, banners, flyers, notary &amp; shipping. Plainview, NY.</p>
      </a>

      <a href="https://www.ligiftbasket.com" target="_blank"
         style="background:#fff;border:2px solid #d97706;border-radius:12px;padding:24px;text-decoration:none;display:block;">
        <div style="font-size:2em;margin-bottom:8px;">&#127873;</div>
        <h3 style="color:#d97706;margin:0 0 8px 0;">Hiren's Gift Baskets</h3>
        <p style="color:#555;margin:0;font-size:0.95em;">Long Island Gift Basket — Curated gift baskets with same-day delivery across Nassau &amp; Suffolk County.</p>
      </a>

      <a href="https://www.longislandballoonsdecor.com" target="_blank"
         style="background:#fff;border:2px solid #7c3aed;border-radius:12px;padding:24px;text-decoration:none;display:block;">
        <div style="font-size:2em;margin-bottom:8px;">&#127880;</div>
        <h3 style="color:#7c3aed;margin:0 0 8px 0;">Hiren's Balloon Shop</h3>
        <p style="color:#555;margin:0;font-size:0.95em;">Long Island Balloons &amp; Decor — Custom balloon arrangements for events across Long Island.</p>
      </a>

    </div>

    <div style="background:#1a1a2e;color:#fff;border-radius:16px;padding:40px;margin-bottom:40px;">
      <h2 style="color:#fff;margin-top:0;">Serving All of Long Island</h2>
      <p style="color:#ccc;line-height:1.8;">
        Hiren Chauhan's stores serve customers from across Nassau County and Suffolk County, including:
        <strong>Plainview, Hicksville, Syosset, Jericho, Bethpage, Levittown, Westbury, Farmingdale,
        Old Bethpage, Woodbury, Oyster Bay, Melville</strong> and the greater Long Island, New York area.
      </p>
    </div>

    <div style="background:#f0f9ff;border-radius:16px;padding:32px;">
      <h2 style="color:#1a3c6e;margin-top:0;">Find Hiren's Stores</h2>
      <ul style="font-size:1.05em;line-height:2;color:#333;">
        <li><strong>Location:</strong> Plainview, NY 11803</li>
        <li><strong>Phone:</strong> +1 (516) 555-0100</li>
        <li><strong>Email:</strong> contact@longislandconvenience.com</li>
        <li><strong>Hours:</strong> Monday – Sunday, 9:00 AM – 9:00 PM</li>
      </ul>
    </div>

    <div style="text-align:center;margin-top:48px;">
      <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Hiren Chauhan",
        "jobTitle": "Business Owner",
        "worksFor": [
          {"@type": "LocalBusiness", "name": "Long Island Cards", "url": "https://www.longislandcards.com"},
          {"@type": "LocalBusiness", "name": "Long Island Print and Mail", "url": "https://www.longislandprintandmail.com"},
          {"@type": "LocalBusiness", "name": "Long Island Gift Basket", "url": "https://www.ligiftbasket.com"},
          {"@type": "LocalBusiness", "name": "Long Island Balloons and Decor", "url": "https://www.longislandballoonsdecor.com"},
          {"@type": "LocalBusiness", "name": "Long Island Convenience", "url": "https://www.longislandconvenience.com"}
        ],
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Plainview",
          "addressRegion": "NY",
          "postalCode": "11803",
          "addressCountry": "US"
        },
        "url": "https://www.longislandconvenience.com/about-hiren"
      }
      </script>
    </div>

  </section>
</div>
'''

# Check if about-hiren page already exists
existing_about = xc('website.page', 'search_read',
    [[['url', '=', '/about-hiren'], ['website_id', '=', 1]]],
    {'fields': ['id'], 'limit': 1})

# Get home view for website 1 to find the right structure
home_view = xc('ir.ui.view', 'read', [[600]], {'fields': ['key', 'arch_db']})[0]

# Create view for the about-hiren page
about_arch = f'''<t name="About Hiren Chauhan" t-name="website.about_hiren">
  <t t-call="website.layout">
    {about_hiren_content}
  </t>
</t>'''

if existing_about:
    print(f"  About Hiren page already exists: ID {existing_about[0]['id']}")
    # Update content via the view
    existing_view = xc('ir.ui.view', 'search_read',
        [[['key', '=', 'website.about_hiren'], ['website_id', '=', 1]]],
        {'fields': ['id'], 'limit': 1})
    if existing_view:
        xc('ir.ui.view', 'write', [[existing_view[0]['id']], {'arch_db': about_arch}])
        print("  Updated About Hiren view")
else:
    # Create the view
    view_id = xc('ir.ui.view', 'create', [{
        'name': 'About Hiren Chauhan',
        'type': 'qweb',
        'key': 'website.about_hiren',
        'mode': 'primary',
        'website_id': 1,
        'active': True,
        'arch_db': about_arch,
    }])
    print(f"  Created About Hiren view: ID {view_id}")

    # Create the website.page record
    page_id = xc('website.page', 'create', [{
        'name': 'About Hiren Chauhan',
        'url': '/about-hiren',
        'website_id': 1,
        'website_published': True,
        'website_meta_title': 'About Hiren Chauhan | Long Island Local Business Owner | Plainview NY',
        'website_meta_description': 'Hiren Chauhan is a Plainview NY entrepreneur and owner of Long Island Cards, Print & Mail, Gift Baskets, and Balloons. Hiren shop — serving Nassau County since day one.',
        'website_meta_keywords': 'hiren chauhan, hiren shop, hiren store long island, hiren cards plainview ny, hiren print shop, hiren gift baskets, long island local business owner',
        'view_id': view_id,
    }])
    print(f"  Created About Hiren page: ID {page_id} at /about-hiren")

    # Add to navigation
    menus = xc('website.menu', 'search_read', [[['website_id', '=', 1]]], {'fields': ['id', 'name', 'parent_id', 'sequence']})
    root = [mn for mn in menus if not mn['parent_id']][0]
    about_exists = any(mn['name'] == 'About' for mn in menus)
    if not about_exists:
        xc('website.menu', 'create', [{
            'name': 'About Hiren',
            'url': '/about-hiren',
            'website_id': 1,
            'parent_id': root['id'],
            'sequence': 45,
        }])
        print("  Added 'About Hiren' to navigation")
    else:
        # Update existing About link
        about_menu = [mn for mn in menus if mn['name'] == 'About'][0]
        xc('website.menu', 'write', [[about_menu['id']], {'url': '/about-hiren', 'name': 'About Hiren'}])
        print("  Updated existing 'About' menu to 'About Hiren' -> /about-hiren")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Create more targeted blog posts (beating competitors)
# ─────────────────────────────────────────────────────────────────────────────
print("\n== STEP 4: Creating competitor-targeting blog posts ==")

def cta(label, url, color="#e63946"):
    return f'''
<div style="text-align:center;margin:40px 0 20px 0;">
  <a href="{url}" target="_blank"
     style="background:{color};color:#fff;padding:16px 40px;border-radius:8px;
            font-size:18px;font-weight:700;text-decoration:none;display:inline-block;">
    {label} &rarr;
  </a>
  <p style="color:#888;font-size:13px;margin-top:12px;">
    Hiren's Long Island store — Plainview, Nassau County, NY
  </p>
</div>'''

EXTRA_POSTS = [
    {
        "blog_name": "Sports & Trading Cards",
        "blog_id": 2,
        "title": "Pokemon Cards Long Island New York — Where to Buy in Plainview",
        "subtitle": "Hiren's local Long Island card shop stocks the latest sets and singles",
        "meta_title": "Pokemon Cards Long Island New York | Buy Pokemon TCG Plainview NY | Hiren Cards",
        "meta_desc": "Buy Pokemon cards on Long Island, NY at Hiren's card shop in Plainview. Latest Scarlet & Violet sets, ETBs, booster boxes, and rare singles. Nassau County's top card store.",
        "store_url": "https://www.longislandcards.com",
        "cta_label": "Shop Pokemon Cards at Hiren's Long Island Cards",
        "cta_color": "#e63030",
        "content": """
<h2>Pokemon Cards Long Island — Why Shop Local at Hiren's Store?</h2>
<p>When you search "pokemon cards long island new york" you'll find online marketplaces and big retailers — but nothing beats walking into <strong>Hiren's card shop in Plainview, NY</strong>. You can see the cards, get expert advice, and walk out the same day with exactly what you want.</p>

<h2>What Makes Hiren's Long Island Card Shop Different</h2>
<ul>
  <li><strong>Same-day availability</strong> — no waiting for shipping. Buy Pokemon cards today in Plainview, NY.</li>
  <li><strong>Expert advice</strong> — Hiren and the team know which sets have the best pull rates right now</li>
  <li><strong>Buy, sell, trade</strong> — bring your duplicates and trade up at fair Long Island market prices</li>
  <li><strong>Competitive pricing</strong> — local Nassau County prices, not inflated online marketplace prices</li>
  <li><strong>PSA grading submissions</strong> — grade your rare pulls right at the store</li>
</ul>

<h2>Current Pokemon Stock at Hiren's Plainview Store</h2>
<ul>
  <li>Scarlet &amp; Violet — Prismatic Evolutions booster boxes and ETBs</li>
  <li>Scarlet &amp; Violet — Stellar Crown, Surging Sparks, Obsidian Flames</li>
  <li>Single booster packs — assorted sets available</li>
  <li>Pokemon singles — rare cards, alt-arts, illustration rares</li>
  <li>Graded Pokemon cards — PSA 10 Charizard ex, PSA 9 vintage cards</li>
</ul>

<h2>Pokemon TCG Events on Long Island</h2>
<p>Hiren's Long Island Cards is your home base for Pokemon TCG on Nassau County. We host casual play sessions and can help you prep for regional tournaments. Follow our store for event announcements.</p>

<h2>Compared to Other Long Island Card Shops</h2>
<p>While other shops like Omega Level Gaming serve different parts of Long Island, Hiren's Long Island Cards focuses exclusively on <strong>Plainview, Hicksville, Syosset, Jericho, and central Nassau County</strong>. We're your neighborhood card shop — we know our regulars by name.</p>
"""
    },
    {
        "blog_name": "Sports & Trading Cards",
        "blog_id": 2,
        "title": "Trading Cards Nassau County NY — Complete Buyer's Guide",
        "subtitle": "From Pokemon to sports cards — what to buy, where to buy, and what to avoid",
        "meta_title": "Trading Cards Nassau County NY | Card Shop Plainview | Hiren Chauhan Cards",
        "meta_desc": "Looking for trading cards in Nassau County NY? Hiren Chauhan's card shop in Plainview stocks Pokemon, MTG, sports cards, graded slabs. Nassau County's local card store.",
        "store_url": "https://www.longislandcards.com",
        "cta_label": "Shop Trading Cards in Nassau County — Hiren Cards",
        "cta_color": "#1a3c6e",
        "content": """
<h2>Trading Cards in Nassau County, NY — Your Complete Guide</h2>
<p><strong>Hiren Chauhan</strong> opened Long Island Cards in Plainview to give Nassau County collectors a dedicated local card shop. This guide covers everything you need to know about buying trading cards in Nassau County, NY.</p>

<h2>Types of Trading Cards Available in Nassau County</h2>
<h3>Sports Cards</h3>
<p>Panini Prizm basketball, Topps Series 1 baseball, Panini Donruss football — the biggest sports card brands are in stock at Hiren's Plainview store. We carry both hobby boxes (better hit rates) and retail boxes.</p>
<h3>Pokemon TCG</h3>
<p>Nassau County's most popular trading card game. Hiren's Long Island Cards carries current-set booster boxes, ETBs, and a singles collection updated weekly.</p>
<h3>Magic: The Gathering</h3>
<p>Draft booster boxes, Commander precon decks, and individual MTG singles. Ask about our Duskmourn and Bloomburrow stock.</p>
<h3>Yu-Gi-Oh! and One Piece</h3>
<p>We carry the latest Yu-Gi-Oh! booster sets (Burst Protocol, Amazing Defenders) and One Piece card game product for both competitive players and collectors.</p>

<h2>Graded Cards — PSA and BGS in Nassau County</h2>
<p>Hiren's Long Island Cards is Nassau County's go-to for PSA and BGS graded cards. Buy authenticated slabs already graded, or submit your own cards through us for grading. Our graded inventory includes rare rookie cards, vintage sports cards, and PSA 10 Pokemon cards.</p>

<h2>Why Hiren Chauhan's Store Stands Out</h2>
<p>Hiren built Long Island Cards with one goal: give Nassau County collectors a place where expert knowledge, fair pricing, and community come first. No bots. No scalper prices. Just a local Plainview card shop run by people who love the hobby.</p>
"""
    },
    {
        "blog_name": "Long Island News",
        "blog_id": 6,
        "title": "Hiren Chauhan — Long Island's Local Convenience Store Entrepreneur",
        "subtitle": "The story of how Hiren built 5 stores in Plainview, Nassau County NY",
        "meta_title": "Hiren Chauhan Long Island | Hiren Shop Plainview NY | Local Business Owner Nassau County",
        "meta_desc": "Hiren Chauhan is the founder of Long Island's growing family of local stores in Plainview NY — cards, gift baskets, printing, balloons and convenience. Hiren's shop on Long Island.",
        "store_url": "https://www.longislandconvenience.com/about-hiren",
        "cta_label": "Meet Hiren — Long Island Convenience",
        "cta_color": "#059669",
        "content": """
<h2>Who is Hiren Chauhan?</h2>
<p><strong>Hiren Chauhan</strong> is a Plainview, New York entrepreneur and founder of the Long Island Convenience family of stores. Known locally as the owner of <strong>"Hiren's Shop"</strong> or simply <strong>"Hiren's Store"</strong> in Plainview, Hiren has built five specialty retail businesses serving Nassau County and the broader Long Island community.</p>

<h2>Hiren's Long Island Stores</h2>
<ul>
  <li><strong>Long Island Cards (Hiren's Card Shop)</strong> — Sports trading cards, Pokemon TCG, MTG, Yu-Gi-Oh!, PSA/BGS graded cards. Plainview, NY. Visit at <a href="https://www.longislandcards.com">longislandcards.com</a></li>
  <li><strong>Long Island Print &amp; Mail (Hiren's Print Shop)</strong> — Same-day business cards, banners, flyers, notary services. Plainview, NY. Visit at <a href="https://www.longislandprintandmail.com">longislandprintandmail.com</a></li>
  <li><strong>Long Island Gift Basket (Hiren's Gift Shop)</strong> — Curated gift baskets with same-day delivery across Nassau County. Visit at <a href="https://www.ligiftbasket.com">ligiftbasket.com</a></li>
  <li><strong>Long Island Balloons &amp; Decor (Hiren's Balloon Shop)</strong> — Custom balloon arrangements for Long Island events. Visit at <a href="https://www.longislandballoonsdecor.com">longislandballoonsdecor.com</a></li>
  <li><strong>Long Island Convenience (Hiren's Hub)</strong> — The central hub connecting all of Hiren's stores. Visit at <a href="https://www.longislandconvenience.com">longislandconvenience.com</a></li>
</ul>

<h2>Hiren's Mission for Long Island</h2>
<p>Hiren Chauhan's mission is simple: give the people of Plainview, Nassau County, and Long Island access to quality local specialty stores without having to drive to the city or wait for online shipping. Every store in the Long Island Convenience family is built on the same values — local expertise, fair prices, and genuine community service.</p>

<h2>Search for "Hiren Shop" or "Hiren Chauhan" on Long Island</h2>
<p>When Long Island residents search for <strong>"hiren shop"</strong>, <strong>"hiren chauhan store"</strong>, <strong>"hiren cards long island"</strong>, or <strong>"hiren print shop plainview"</strong> — they're looking for these stores. Bookmark <a href="https://www.longislandconvenience.com">longislandconvenience.com</a> as your starting point.</p>

<h2>Contact Hiren's Stores</h2>
<ul>
  <li>Location: Plainview, NY 11803 (Nassau County)</li>
  <li>Service area: Plainview, Hicksville, Syosset, Jericho, Bethpage, Levittown, Westbury, and all of Long Island</li>
</ul>
"""
    },
    {
        "blog_name": "Print & Mail Services",
        "blog_id": 4,
        "title": "Print Shop Plainview NY — Hiren's Same-Day Printing vs. Online Services",
        "subtitle": "Why local is faster, cheaper, and better for Nassau County businesses",
        "meta_title": "Print Shop Plainview NY | Hiren Print Shop | Same Day Printing Nassau County",
        "meta_desc": "Hiren's print shop in Plainview NY beats online printing every time for Nassau County businesses. Same-day turnaround, local support, fair prices. Long Island Print & Mail.",
        "store_url": "https://www.longislandprintandmail.com",
        "cta_label": "Order at Hiren's Print Shop — Long Island Print & Mail",
        "cta_color": "#2563eb",
        "content": """
<h2>Hiren's Print Shop in Plainview, NY — Faster Than Online</h2>
<p>For Nassau County businesses and residents, <strong>Hiren's Long Island Print &amp; Mail in Plainview</strong> consistently beats online printing services on speed, price, and support. Here's why local wins every time.</p>

<h2>Same-Day vs. Online Printing — Speed Comparison</h2>
<table style="width:100%;border-collapse:collapse;margin:20px 0;">
  <tr style="background:#1a3c6e;color:#fff;">
    <th style="padding:12px;text-align:left;">Service</th>
    <th style="padding:12px;text-align:left;">Turnaround</th>
    <th style="padding:12px;text-align:left;">Cost (250 cards)</th>
  </tr>
  <tr style="background:#f8f9ff;">
    <td style="padding:12px;font-weight:700;color:#1a3c6e;">Hiren's Print Shop, Plainview NY</td>
    <td style="padding:12px;color:#059669;font-weight:700;">Same day (2–4 hours)</td>
    <td style="padding:12px;">From $35</td>
  </tr>
  <tr>
    <td style="padding:12px;">VistaPrint (online)</td>
    <td style="padding:12px;">5–10 business days standard</td>
    <td style="padding:12px;">$25–$45 + shipping</td>
  </tr>
  <tr style="background:#f8f9ff;">
    <td style="padding:12px;">Staples (retail)</td>
    <td style="padding:12px;">1–3 business days</td>
    <td style="padding:12px;">$40–$60</td>
  </tr>
</table>

<h2>What Hiren's Print Shop Offers That Online Can't</h2>
<ul>
  <li><strong>Real human review</strong> — we check your file for errors before printing, no surprises</li>
  <li><strong>In-person proofing</strong> — see a printed sample before the full run</li>
  <li><strong>Design help on-site</strong> — don't have a file? We can design for you</li>
  <li><strong>Same-day emergency service</strong> — meeting in 3 hours? We can have cards ready</li>
  <li><strong>Notary &amp; shipping bundled</strong> — one stop for all your business needs</li>
</ul>

<h2>Serving Nassau County Businesses</h2>
<p>Hiren's Long Island Print &amp; Mail serves businesses across Nassau County: real estate agents in Syosset, restaurants in Hicksville, contractors in Bethpage, medical offices in Jericho, and small businesses throughout Plainview and the surrounding area.</p>
"""
    },
]

created_extra = 0
for post in EXTRA_POSTS:
    existing = xc('blog.post', 'search_read',
        [[['name', '=', post['title']]]], {'fields': ['id'], 'limit': 1})
    full_content = post['content'] + cta(post['cta_label'], post['store_url'], post['cta_color'])
    if existing:
        xc('blog.post', 'write', [[existing[0]['id']], {
            'subtitle': post['subtitle'], 'content': full_content,
            'website_meta_title': post['meta_title'],
            'website_meta_description': post['meta_desc'],
            'website_published': True,
        }])
        print(f"  Updated: {post['title'][:60]}")
    else:
        pid = xc('blog.post', 'create', [{
            'name': post['title'], 'subtitle': post['subtitle'],
            'blog_id': post['blog_id'], 'content': full_content,
            'website_meta_title': post['meta_title'],
            'website_meta_description': post['meta_desc'],
            'website_published': True,
        }])
        print(f"  Created post ID {pid}: {post['title'][:60]}")
        created_extra += 1

print(f"\n{created_extra} additional blog posts created")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — Summary
# ─────────────────────────────────────────────────────────────────────────────
total_posts = xc('blog.post', 'search_count', [[['website_published', '=', True]]])
print(f"\n{'='*60}")
print("ALL DONE — Hiren Local SEO Domination Complete")
print(f"{'='*60}")
print(f"Total published blog posts: {total_posts}")
print("\nKeywords now targeted across all assets:")
print("  - hiren shop")
print("  - hiren chauhan")
print("  - hiren store long island")
print("  - hiren cards plainview ny")
print("  - hiren print shop")
print("  - pokemon cards long island new york")
print("  - trading cards nassau county ny")
print("  - print shop plainview ny")
print("  - long island convenience plainview")
print("\nURLs to check:")
print("  https://www.longislandconvenience.com/blog")
print("  https://www.longislandconvenience.com/about-hiren")
print("  https://www.longislandcards.com")
print("  https://www.longislandprintandmail.com")
