#!/usr/bin/env python3
"""
Rebuild SEO head views with CORRECT QWeb escaping.
Root cause of 500s: { } in JSON-LD inside QWeb <script> were parsed as t-expressions.
Fix: use string concatenation (NOT f-strings) to embed the QWeb-escaped JSON.
  f-string turns {{ back to {, so we must concatenate AFTER escaping.
"""
import xmlrpc.client, sys, json
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

layout_id = xc('ir.ui.view', 'search_read',
    [[['key', '=', 'website.layout']]], {'fields': ['id'], 'limit': 1})[0]['id']
print(f"layout_id: {layout_id}")

def build_seo_arch(wid, domain, og_title, meta_desc, schema_dict):
    """
    Build QWeb-safe SEO head view using STRING CONCATENATION — not f-strings —
    for the JSON-LD block so {{ }} escaping survives into the stored arch_db.
    """
    jsonld_raw    = json.dumps(schema_dict, indent=2)
    # Escape { and } for QWeb BEFORE any string ops
    jsonld_qweb   = jsonld_raw.replace('{', '{{').replace('}', '}}')

    meta_desc_xml = meta_desc.replace('&', '&amp;').replace('"', '&quot;')
    og_title_xml  = og_title.replace('&', '&amp;').replace('"', '&quot;')

    # Build arch via concatenation — f-string only for non-JSON parts
    head = (
        f'<t name="SEO Head {wid}" t-name="website.seo_head_{wid}" inherit_id="website.layout">\n'
        f'  <xpath expr="//head" position="inside">\n'
        f'    <meta name="description" content="{meta_desc_xml}"/>\n'
        f'    <meta name="robots" content="index, follow"/>\n'
        f'    <meta property="og:type" content="website"/>\n'
        f'    <meta property="og:title" content="{og_title_xml}"/>\n'
        f'    <meta property="og:description" content="{meta_desc_xml}"/>\n'
        f'    <meta property="og:url" content="{domain}"/>\n'
        f'    <meta name="twitter:card" content="summary_large_image"/>\n'
        f'    <meta name="twitter:title" content="{og_title_xml}"/>\n'
        f'    <meta name="twitter:description" content="{meta_desc_xml}"/>\n'
        f'    <script type="application/ld+json">'
    )
    tail = (
        '</script>\n'
        '  </xpath>\n'
        '</t>'
    )
    # Concatenate: head + escaped JSON (not processed by f-string) + tail
    return head + jsonld_qweb + tail

SITES = [
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
            "description": "Hiren Chauhan's convenience hub in Plainview NY. Sports cards, gift baskets, balloon decor, print and mail, cigars, tobacco, lottery tickets.",
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
            "areaServed": ["Plainview NY", "Nassau County NY", "Long Island NY"],
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
            "description": "Hiren Chauhan's sports and trading card shop in Plainview NY. PSA and BGS graded cards, Pokemon TCG, Magic The Gathering, Yu-Gi-Oh, One Piece. Nassau County Long Island.",
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
            "openingHours": ["Mo-Su 10:00-20:00"]
        }
    },
    {
        'view_id': 3521, 'website_id': 39,
        'domain': 'https://www.longislandprintandmail.com',
        'og_title': 'Long Island Print and Mail — Hiren Chauhan | Same-Day Printing Plainview NY',
        'meta_desc': "Hiren's print shop in Plainview NY. Same-day business cards, banners, flyers. Notary and shipping. Nassau County Long Island.",
        'schema': {
            "@context": "https://schema.org",
            "@type": "PrintShop",
            "name": "Long Island Print and Mail",
            "alternateName": ["Hiren Print Shop", "Hiren Chauhan Printing Long Island"],
            "description": "Hiren Chauhan's print and mail shop in Plainview NY. Same-day business cards, banners, flyers, shipping, notary. Nassau County Long Island.",
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

print("\nRebuilding SEO views with correct QWeb escaping...")
for s in SITES:
    arch = build_seo_arch(
        s['website_id'], s['domain'], s['og_title'], s['meta_desc'], s['schema']
    )

    # Verify the arch actually has {{ }} (not bare { })
    json_section = arch[arch.find('<script'):]
    if '{{' in json_section:
        print(f"  View {s['view_id']}: QWeb escaping confirmed ({{ found in JSON)")
    else:
        print(f"  View {s['view_id']}: WARNING — no {{ found, may still fail!")

    result = xc('ir.ui.view', 'write', [[s['view_id']], {
        'arch_db': arch,
        'active': True,
        'inherit_id': layout_id,
        'mode': 'extension',
        'website_id': s['website_id'],
    }])
    print(f"  View {s['view_id']} (website {s['website_id']}) saved: {result}")

# Fix About Hiren page — remove JSON-LD from page content (it had bare { })
# Rebuild it without inline JSON-LD (clean HTML only)
print("\nRebuilding About Hiren page without inline JSON-LD...")
about_arch = '''<t name="About Hiren Chauhan" t-name="website.about_hiren">
  <t t-call="website.layout">
    <div id="wrap">
      <section style="max-width:900px;margin:60px auto;padding:0 24px;font-family:system-ui,sans-serif;">

        <div style="text-align:center;margin-bottom:48px;">
          <h1 style="font-size:2.6em;font-weight:800;color:#1a1a2e;margin-bottom:12px;">
            Hiren Chauhan &#8212; Long Island Local Business Owner
          </h1>
          <p style="font-size:1.15em;color:#555;max-width:680px;margin:0 auto;">
            Building Long Island&#39;s premier family of local specialty stores in Plainview, Nassau County, NY.
          </p>
        </div>

        <div style="background:#f8f9ff;border-radius:16px;padding:36px;margin-bottom:36px;border-left:5px solid #1a3c6e;">
          <h2 style="color:#1a3c6e;font-size:1.5em;margin-top:0;">About Hiren</h2>
          <p style="font-size:1.05em;line-height:1.8;color:#333;">
            Hiren Chauhan is a Plainview, New York-based entrepreneur and proud Long Island business owner.
            Starting with a passion for collectibles and community service, Hiren built a growing family of
            specialty retail stores serving Nassau County and the wider Long Island area.
          </p>
          <p style="font-size:1.05em;line-height:1.8;color:#333;">
            Known locally as <strong>Hiren Shop</strong> or <strong>Hiren Store on Long Island</strong>,
            the collection spans sports trading cards, gift baskets, professional printing,
            balloon decor, and convenience retail &#8212; all from Plainview, NY 11803.
          </p>
        </div>

        <h2 style="color:#1a1a2e;font-size:1.7em;">Hiren&#39;s Long Island Stores</h2>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:36px;">

          <a href="https://www.longislandcards.com" target="_blank"
             style="background:#fff;border:2px solid #1a3c6e;border-radius:12px;padding:22px;text-decoration:none;display:block;">
            <div style="font-size:1.8em;margin-bottom:8px;">&#127183;</div>
            <h3 style="color:#1a3c6e;margin:0 0 6px 0;">Hiren&#39;s Card Shop</h3>
            <p style="color:#555;margin:0;font-size:0.9em;">Long Island Cards &#8212; PSA graded cards, Pokemon, MTG, Yu-Gi-Oh, One Piece. Plainview NY.</p>
          </a>

          <a href="https://www.longislandprintandmail.com" target="_blank"
             style="background:#fff;border:2px solid #2563eb;border-radius:12px;padding:22px;text-decoration:none;display:block;">
            <div style="font-size:1.8em;margin-bottom:8px;">&#128424;</div>
            <h3 style="color:#2563eb;margin:0 0 6px 0;">Hiren&#39;s Print Shop</h3>
            <p style="color:#555;margin:0;font-size:0.9em;">Long Island Print &#38; Mail &#8212; Same-day business cards, banners, flyers, notary. Plainview NY.</p>
          </a>

          <a href="https://www.ligiftbasket.com" target="_blank"
             style="background:#fff;border:2px solid #d97706;border-radius:12px;padding:22px;text-decoration:none;display:block;">
            <div style="font-size:1.8em;margin-bottom:8px;">&#127873;</div>
            <h3 style="color:#d97706;margin:0 0 6px 0;">Hiren&#39;s Gift Baskets</h3>
            <p style="color:#555;margin:0;font-size:0.9em;">Long Island Gift Basket &#8212; Curated baskets with same-day delivery Nassau &#38; Suffolk County.</p>
          </a>

          <a href="https://www.longislandballoonsdecor.com" target="_blank"
             style="background:#fff;border:2px solid #7c3aed;border-radius:12px;padding:22px;text-decoration:none;display:block;">
            <div style="font-size:1.8em;margin-bottom:8px;">&#127880;</div>
            <h3 style="color:#7c3aed;margin:0 0 6px 0;">Hiren&#39;s Balloon Shop</h3>
            <p style="color:#555;margin:0;font-size:0.9em;">Long Island Balloons &#38; Decor &#8212; Custom balloon arrangements for Long Island events.</p>
          </a>

        </div>

        <div style="background:#1a1a2e;color:#fff;border-radius:16px;padding:36px;margin-bottom:36px;">
          <h2 style="color:#fff;margin-top:0;">Serving All of Long Island</h2>
          <p style="color:#ccc;line-height:1.8;">
            Hiren Chauhan&#39;s stores serve customers across Nassau County and Suffolk County:
            Plainview, Hicksville, Syosset, Jericho, Bethpage, Levittown, Westbury, Farmingdale,
            Old Bethpage, Woodbury, Oyster Bay, Melville and greater Long Island, New York.
          </p>
        </div>

        <div style="background:#f0f9ff;border-radius:16px;padding:28px;">
          <h2 style="color:#1a3c6e;margin-top:0;">Find Hiren&#39;s Stores</h2>
          <ul style="font-size:1em;line-height:2.2;color:#333;margin:0;padding-left:20px;">
            <li><strong>Location:</strong> Plainview, NY 11803 (Nassau County)</li>
            <li><strong>Phone:</strong> (917) 338-7086</li>
            <li><strong>Hours:</strong> Monday &#8211; Sunday, 9:00 AM &#8211; 9:00 PM</li>
            <li><strong>Hub site:</strong> <a href="https://www.longislandconvenience.com">longislandconvenience.com</a></li>
          </ul>
        </div>

      </section>
    </div>
  </t>
</t>'''

result = xc('ir.ui.view', 'write', [[3611], {'arch_db': about_arch, 'active': True}])
print(f"About Hiren view 3611 rebuilt: {result}")

# Final verification
print("\nFinal site checks...")
import urllib.request, ssl, re
ctx = ssl.create_default_context()
all_good = True
for domain, wid in [
    ('https://www.longislandconvenience.com', 1),
    ('https://www.longislandcards.com', 36),
    ('https://www.longislandprintandmail.com', 39),
]:
    try:
        req = urllib.request.Request(domain, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            body = r.read().decode('utf-8', 'ignore')
            has_jsonld = 'application/ld+json' in body
            has_desc   = 'name="description"' in body
            title_m    = re.search(r'<title>([^<]+)</title>', body)
            title      = title_m.group(1)[:60] if title_m else 'NO TITLE'
            status_sym = "OK" if r.status == 200 else "FAIL"
            print(f"  [{status_sym}] {domain}")
            print(f"       HTTP={r.status} | JSON-LD={has_jsonld} | meta-desc={has_desc}")
            print(f"       Title: {title}")
            if r.status != 200: all_good = False
    except Exception as e:
        print(f"  [FAIL] {domain}: {e}")
        all_good = False

print(f"\n{'All 3 sites ONLINE and SEO-ready!' if all_good else 'Some sites still have issues — check above'}")
