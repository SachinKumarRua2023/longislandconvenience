#!/usr/bin/env python3
"""
Inject SEO meta tags + JSON-LD structured data into all 3 live Odoo websites.
  - longislandconvenience.com  (website 36, homepage view 600)
  - longislandcards.com        (website 35, homepage view ~599 or find it)
  - longislandprintandmail.com (website 39, homepage view 2958)
"""
import xmlrpc.client, sys, re, json
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

# ── SEO data per website ──────────────────────────────────────────────────────
SITES = {
    36: {  # longislandconvenience.com
        "domain": "https://www.longislandconvenience.com",
        "meta_title": "Long Island Convenience Store | Plainview NY | Hiren Shop",
        "meta_desc": "Your local convenience store in Plainview, NY. Shop cigars, tobacco, vape, lottery tickets, gift baskets & more. Long Island's one-stop convenience shop — open daily.",
        "meta_keywords": "long island convenience store, convenience store plainview ny, hiren shop, cigars tobacco long island, lottery tickets nassau county, gift baskets long island",
        "og_title": "Long Island Convenience — Plainview NY",
        "schema_type": "ConvenienceStore",
        "schema_name": "Long Island Convenience",
        "schema_desc": "Local convenience store in Plainview, NY offering cigars, tobacco, vape products, lottery tickets, gift baskets, greeting cards, and more. Family-owned and operated.",
        "price_range": "$",
        "phone": "+1-516-000-0000",
        "address_street": "Plainview",
        "address_city": "Plainview",
        "address_state": "NY",
        "address_zip": "11803",
        "area_served": ["Plainview NY", "Nassau County", "Long Island NY"],
        "homepage_view_id": 600,
    },
    35: {  # longislandcards.com
        "domain": "https://www.longislandcards.com",
        "meta_title": "Long Island Cards | Sports & Trading Cards Plainview NY | Hiren Cards",
        "meta_desc": "Buy PSA & BGS graded sports cards, Pokemon, MTG, Yu-Gi-Oh!, One Piece cards in Plainview, NY. Authenticated trading cards — rookies to legends. Long Island's top card shop.",
        "meta_keywords": "sports cards long island, trading cards plainview ny, graded cards long island, PSA cards near me, pokemon cards long island, hiren cards shop",
        "og_title": "Long Island Cards — Sports & Trading Cards Plainview NY",
        "schema_type": "Store",
        "schema_name": "Long Island Cards",
        "schema_desc": "Sports and trading card shop in Plainview, NY. Specializing in PSA and BGS graded cards, sports singles, Pokemon TCG, Magic: The Gathering, Yu-Gi-Oh!, and One Piece cards.",
        "price_range": "$$",
        "phone": "+1-516-000-0001",
        "address_street": "Plainview",
        "address_city": "Plainview",
        "address_state": "NY",
        "address_zip": "11803",
        "area_served": ["Plainview NY", "Nassau County", "Long Island NY"],
        "homepage_view_id": None,  # will be found dynamically
    },
    39: {  # longislandprintandmail.com
        "domain": "https://www.longislandprintandmail.com",
        "meta_title": "Long Island Print & Mail | Same-Day Printing Plainview NY | Hiren Print Shop",
        "meta_desc": "Same-day business card, banner & flyer printing in Plainview, NY. Notary services, shipping & more. Long Island's trusted print and mail shop. Open daily.",
        "meta_keywords": "print and mail long island, printing services plainview ny, same day printing long island, business card printing nassau county, banner printing long island, hiren print shop",
        "og_title": "Long Island Print & Mail — Same-Day Printing in Plainview NY",
        "schema_type": "PrintShop",
        "schema_name": "Long Island Print & Mail",
        "schema_desc": "Professional print and mail shop in Plainview, NY. Same-day business cards, banners, flyers, shipping, notary services, and more. Serving all of Long Island.",
        "price_range": "$$",
        "phone": "+1-516-000-0002",
        "address_street": "Plainview",
        "address_city": "Plainview",
        "address_state": "NY",
        "address_zip": "11803",
        "area_served": ["Plainview NY", "Nassau County", "Long Island NY"],
        "homepage_view_id": 2958,
    },
}

# ── Build JSON-LD block ───────────────────────────────────────────────────────
def make_jsonld(s):
    schema = {
        "@context": "https://schema.org",
        "@type": s["schema_type"],
        "name": s["schema_name"],
        "description": s["schema_desc"],
        "url": s["domain"],
        "telephone": s["phone"],
        "priceRange": s["price_range"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": s["address_street"],
            "addressLocality": s["address_city"],
            "addressRegion": s["address_state"],
            "postalCode": s["address_zip"],
            "addressCountry": "US"
        },
        "areaServed": s["area_served"],
        "openingHours": ["Mo-Su 09:00-21:00"],
        "image": s["domain"] + "/web/image/website/" + str(list(SITES.keys())[list(SITES.values()).index(s)]) + "/logo" if s in SITES.values() else "",
        "sameAs": [
            "https://www.yelp.com/biz/" + s["schema_name"].lower().replace(" ", "-"),
        ]
    }
    return json.dumps(schema, indent=2)

# ── Build SEO head snippet (injected via Odoo view) ──────────────────────────
def make_seo_view_arch(site_id, s):
    jsonld = make_jsonld(s)
    return f"""<t name="SEO Head - {s['schema_name']}" t-name="website.seo_head_{site_id}" inherit_id="website.layout" website_id="{site_id}">
  <xpath expr="//head" position="inside">
    <!-- SEO Meta Tags -->
    <meta name="description" t-att-content="''" content="{s['meta_desc']}"/>
    <meta name="keywords" content="{s['meta_keywords']}"/>
    <meta name="robots" content="index, follow"/>
    <meta name="author" content="{s['schema_name']}"/>
    <!-- Open Graph -->
    <meta property="og:type" content="website"/>
    <meta property="og:title" content="{s['og_title']}"/>
    <meta property="og:description" content="{s['meta_desc']}"/>
    <meta property="og:url" content="{s['domain']}"/>
    <meta property="og:site_name" content="{s['schema_name']}"/>
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image"/>
    <meta name="twitter:title" content="{s['og_title']}"/>
    <meta name="twitter:description" content="{s['meta_desc']}"/>
    <!-- Canonical -->
    <link rel="canonical" t-attf-href="{s['domain']}{{{{ request.httprequest.path }}}}"/>
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
{jsonld}
    </script>
  </xpath>
</t>"""

# ── Find website.layout view ID ───────────────────────────────────────────────
layout_views = xc('ir.ui.view', 'search_read',
                  [[['key', '=', 'website.layout'], ['type', '=', 'qweb']]],
                  {'fields': ['id', 'name'], 'limit': 1})
if not layout_views:
    print("ERROR: website.layout view not found")
    sys.exit(1)
layout_id = layout_views[0]['id']
print(f"website.layout view ID: {layout_id}")

# ── Find homepage view for longislandcards.com (website 35) ──────────────────
cards_hp = xc('ir.ui.view', 'search_read',
              [[['website_id', '=', 35], ['key', '=', 'website.homepage']]],
              {'fields': ['id', 'name', 'mode'], 'limit': 5})
print(f"\nLong Island Cards homepage views: {cards_hp}")
if cards_hp:
    SITES[35]['homepage_view_id'] = cards_hp[0]['id']

# ── Process each website ──────────────────────────────────────────────────────
for site_id, s in SITES.items():
    print(f"\n{'='*60}")
    print(f"Processing website {site_id}: {s['schema_name']}")
    print(f"Domain: {s['domain']}")

    # 1. Update website-level meta title ─────────────────────────────────────
    website_record = xc('website', 'read', [[site_id]], {'fields': ['id', 'name', 'domain']})[0]
    print(f"  Website name: {website_record['name']}, domain: {website_record['domain']}")

    # 2. Update homepage page meta tags ────────────────────────────────────────
    # Find the website.page record for homepage
    pages = xc('website.page', 'search_read',
               [[['website_id', '=', site_id], ['url', 'in', ['/', '/home']]]],
               {'fields': ['id', 'url', 'website_meta_title', 'website_meta_description'], 'limit': 5})
    print(f"  Homepage pages found: {len(pages)}")
    for page in pages:
        print(f"    Page {page['id']}: {page['url']}")
        result = xc('website.page', 'write', [[page['id']], {
            'website_meta_title': s['meta_title'],
            'website_meta_description': s['meta_desc'],
            'website_meta_keywords': s['meta_keywords'],
        }])
        print(f"    Updated page meta: {result}")

    # 3. Check if SEO head view already exists for this site ─────────────────
    existing_seo = xc('ir.ui.view', 'search_read',
                      [[['key', '=', f'website.seo_head_{site_id}']]],
                      {'fields': ['id', 'name'], 'limit': 1})

    seo_arch = make_seo_view_arch(site_id, s)

    if existing_seo:
        view_id = existing_seo[0]['id']
        print(f"  Updating existing SEO view {view_id}...")
        result = xc('ir.ui.view', 'write', [[view_id], {
            'arch_db': seo_arch,
            'active': True,
        }])
        print(f"  SEO view updated: {result}")
    else:
        print(f"  Creating new SEO head view for website {site_id}...")
        view_id = xc('ir.ui.view', 'create', [{
            'name': f'SEO Head - {s["schema_name"]}',
            'type': 'qweb',
            'key': f'website.seo_head_{site_id}',
            'inherit_id': layout_id,
            'mode': 'extension',
            'website_id': site_id,
            'active': True,
            'priority': 10,
            'arch_db': seo_arch,
        }])
        print(f"  SEO view created: ID {view_id}")

    # 4. Update homepage view title tag ────────────────────────────────────────
    hp_view_id = s.get('homepage_view_id')
    if hp_view_id:
        hp = xc('ir.ui.view', 'read', [[hp_view_id]], {'fields': ['arch_db']})[0]
        arch = hp['arch_db']
        # Check if there's already a <title> tag in the arch
        if '<title>' in arch:
            # Replace existing title
            arch_new = re.sub(r'<title>[^<]*</title>', f'<title>{s["meta_title"]}</title>', arch)
            if arch_new != arch:
                result = xc('ir.ui.view', 'write', [[hp_view_id], {'arch_db': arch_new}])
                print(f"  Updated <title> in homepage view: {result}")
            else:
                print(f"  Title tag unchanged in homepage view")
        else:
            print(f"  No <title> in homepage view (title managed by website.layout — OK)")

print(f"\n{'='*60}")
print("SEO implementation complete!")
print("\nNEXT STEPS (manual):")
print("1. Go to business.google.com — create Google Business Profile for each store")
print("2. Submit sitemap to Google Search Console:")
print("   - https://www.longislandconvenience.com/sitemap.xml")
print("   - https://www.longislandcards.com/sitemap.xml")
print("   - https://www.longislandprintandmail.com/sitemap.xml")
print("3. Add Google Analytics tracking code in Odoo Settings > Website > Tracking")
print("4. Submit all 3 stores to Yelp, Bing Places, YellowPages, Apple Maps")
print("5. Verify JSON-LD at: https://validator.schema.org")
print("   and: https://search.google.com/test/rich-results")
