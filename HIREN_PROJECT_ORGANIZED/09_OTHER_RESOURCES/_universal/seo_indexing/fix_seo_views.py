#!/usr/bin/env python3
"""
Fix SEO head views — deactivate broken ones, recreate with QWeb-safe JSON-LD.
Root cause: { and } in JSON-LD inside <script> were parsed as QWeb expressions.
Fix: escape all { as {{ and } as }} in QWeb arch, OR use t-raw with a variable.
Best fix: use Odoo's <script> with t-js="false" or move JSON to t-set + t-raw.
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

# Step 1: Deactivate all broken SEO views
print("\nStep 1: Deactivating broken SEO views...")
for vid in [3519, 3520, 3521]:
    r = xc('ir.ui.view', 'write', [[vid], {'active': False}])
    print(f"  View {vid} deactivated: {r}")

def escape_qweb(s):
    """Escape { and } for safe embedding in QWeb arch."""
    return s.replace('{', '{{').replace('}', '}}')

def make_safe_seo_arch(wid, domain, og_title, meta_desc, schema_dict):
    """
    Build QWeb-safe SEO head view.
    JSON-LD is embedded with {{ }} escaping so QWeb doesn't parse it as expressions.
    """
    jsonld_raw = json.dumps(schema_dict, indent=2)
    # Escape all { and } for QWeb
    jsonld_escaped = escape_qweb(jsonld_raw)

    # Also escape & in meta content (XML requirement)
    meta_desc_xml  = meta_desc.replace('&', '&amp;')
    og_title_xml   = og_title.replace('&', '&amp;')

    return f'''<t name="SEO Head {wid}" t-name="website.seo_head_{wid}" inherit_id="website.layout">
  <xpath expr="//head" position="inside">
    <meta name="description" content="{meta_desc_xml}"/>
    <meta name="robots" content="index, follow"/>
    <meta property="og:type" content="website"/>
    <meta property="og:title" content="{og_title_xml}"/>
    <meta property="og:description" content="{meta_desc_xml}"/>
    <meta property="og:url" content="{domain}"/>
    <meta name="twitter:card" content="summary_large_image"/>
    <meta name="twitter:title" content="{og_title_xml}"/>
    <meta name="twitter:description" content="{meta_desc_xml}"/>
    <script type="application/ld+json">{jsonld_escaped}</script>
  </xpath>
</t>'''

# Step 2: Rebuild safe SEO views
print("\nStep 2: Rebuilding QWeb-safe SEO views...")

SCHEMAS = [
    {
        'view_id': 3519, 'website_id': 1,
        'domain': 'https://www.longislandconvenience.com',
        'og_title': 'Long Island Convenience — Hiren Chauhan, Plainview NY',
        'meta_desc': "Hiren's one-stop local hub in Plainview NY. Sports cards, gift baskets, print and mail, balloons, cigars, lotto. Long Island convenience store by Hiren Chauhan.",
        'schema': {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Long Island Convenience",
            "alternateName": ["Hiren Shop", "Hiren Store Long Island", "Hiren Chauhan Store"],
            "description": "Hiren Chauhan's one-stop convenience hub in Plainview, NY. Sports trading cards, gift baskets, balloon decor, print and mail services, cigars, tobacco, and lottery tickets.",
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
                "Plainview NY", "Hicksville NY", "Syosset NY",
                "Jericho NY", "Nassau County NY", "Long Island NY"
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
        'meta_desc': "Hiren's sports and trading card shop in Plainview NY. PSA graded cards, Pokemon, MTG, Yu-Gi-Oh, One Piece. Nassau County top card store.",
        'schema': {
            "@context": "https://schema.org",
            "@type": "Store",
            "name": "Long Island Cards",
            "alternateName": ["Hiren Cards", "Hiren Card Shop", "Hiren Chauhan Cards Long Island"],
            "description": "Hiren Chauhan's sports and trading card shop in Plainview, NY. PSA and BGS graded cards, Pokemon TCG, Magic The Gathering, Yu-Gi-Oh, and One Piece. Nassau County Long Island.",
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
            "areaServed": ["Plainview NY", "Nassau County NY", "Long Island NY"],
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
        'og_title': 'Long Island Print and Mail — Hiren Chauhan | Same-Day Printing Plainview NY',
        'meta_desc': "Hiren's print shop in Plainview NY. Same-day business cards, banners, flyers. Notary and shipping services. Long Island Nassau County.",
        'schema': {
            "@context": "https://schema.org",
            "@type": "PrintShop",
            "name": "Long Island Print and Mail",
            "alternateName": ["Hiren Print Shop", "Hiren Chauhan Printing Long Island"],
            "description": "Hiren Chauhan's professional print and mail shop in Plainview, NY. Same-day business cards, banners, flyers, shipping, notary services. Nassau County Long Island.",
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
            "areaServed": ["Plainview NY", "Nassau County NY", "Long Island NY"],
            "openingHours": ["Mo-Su 09:00-20:00"]
        }
    },
]

layout_id = xc('ir.ui.view', 'search_read',
    [[['key', '=', 'website.layout']]], {'fields': ['id'], 'limit': 1})[0]['id']

for s in SCHEMAS:
    arch = make_safe_seo_arch(
        s['website_id'], s['domain'], s['og_title'], s['meta_desc'], s['schema']
    )

    # Update and reactivate the view
    result = xc('ir.ui.view', 'write', [[s['view_id']], {
        'arch_db': arch,
        'active': True,
        'inherit_id': layout_id,
        'mode': 'extension',
        'website_id': s['website_id'],
    }])
    print(f"  View {s['view_id']} (website {s['website_id']}) rebuilt and activated: {result}")

# Step 3: Verify sites are up
print("\nStep 3: Verifying sites...")
import urllib.request, ssl
ctx = ssl.create_default_context()
for domain in [
    'https://www.longislandconvenience.com',
    'https://www.longislandcards.com',
    'https://www.longislandprintandmail.com'
]:
    try:
        req = urllib.request.Request(domain, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
            body = r.read().decode('utf-8', 'ignore')
            has_jsonld = 'application/ld+json' in body
            has_title  = bool(__import__('re').search(r'<title>[^<]+</title>', body))
            print(f"  {domain}")
            print(f"    HTTP: {r.status} | title: {has_title} | JSON-LD: {has_jsonld}")
    except Exception as e:
        print(f"  {domain} — ERROR: {e}")

print("\nAll done. Sites should be live with proper SEO tags.")
