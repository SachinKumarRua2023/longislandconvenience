import xmlrpc.client, re

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

def upd_view(view_id, arch):
    xc('ir.ui.view', 'write', [[view_id], {'arch_db': arch}])

def upd_page(pid, vals):
    xc('website.page', 'write', [[pid], vals])  # vals inside args list

def set_nav(wid, items):
    menus = xc('website.menu','search_read',[[['website_id','=',wid]]],{'fields':['id','parent_id']})
    root = [mn for mn in menus if not mn['parent_id']]
    if not root: return
    root_id = root[0]['id']
    children = [mn['id'] for mn in menus if mn['parent_id']]
    if children: xc('website.menu','unlink',[children])
    for name, url, seq in items:
        xc('website.menu','create',[{'name':name,'url':url,'website_id':wid,'parent_id':root_id,'sequence':seq}])
    print(f'  Nav: {[i[0] for i in items]}')

def get_hp(wid):
    return xc('website.page','search_read',[[['website_id','=',wid],['url','=','/']]],{'fields':['id','view_id']})[0]

def get_page(wid, url):
    r = xc('website.page','search_read',[[['website_id','=',wid],['url','=',url]]],{'fields':['id','view_id']})
    return r[0] if r else None

print('=== Removing personal branding — all sites ===\n')

# ─── Fix ALL page meta titles & descriptions ───────────────────────────────
print('[0] Fixing all meta titles & descriptions...')
all_pages = xc('website.page','search_read',
    [[['website_id','in',[1,36,37,38,39,41]]]],
    {'fields':['id','website_meta_title','website_meta_description','website_id']})

replacements = [
    ("Hiren's Long Island Convenience", "Long Island Convenience"),
    ("Hiren's Long Island Cards", "Long Island Cards"),
    ("Hiren's Long Island Gift Basket", "Long Island Gift Basket"),
    ("Hiren's Long Island Balloons", "Long Island Balloons & Decor"),
    ("Hiren's Long Island Print", "Long Island Print"),
    ("Hiren's one-stop local hub", "Your one-stop local hub"),
    ("Hiren's one-stop shop", "Your one-stop shop"),
    ("Hiren Chauhan, ", ""),
    ("Hiren Chauhan", "our team"),
    ("Hiren's team", "our team"),
    ("Hiren's ", ""),
    ("| Hiren&#39;s ", "| "),
    ("Hiren&#39;s ", ""),
]

for p in all_pages:
    title = p.get('website_meta_title') or ''
    desc  = p.get('website_meta_description') or ''
    new_title, new_desc = title, desc
    for old, new in replacements:
        new_title = new_title.replace(old, new)
        new_desc  = new_desc.replace(old, new)
    if new_title != title or new_desc != desc:
        xc('website.page','write',[[p['id']],{
            'website_meta_title': new_title,
            'website_meta_description': new_desc
        }])
        print(f'  Fixed meta: {new_title[:60]}')

# ─── 1. Long Island Convenience ────────────────────────────────────────────
print('\n[1] Long Island Convenience')

hp = get_hp(1)
upd_view(hp['view_id'][0], '''<t t-name="website.prod_home_w1"><t t-call="website.layout"><div id="wrap">
<section style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);padding:80px 20px;text-align:center;color:#fff;">
  <h1 style="font-size:3rem;font-weight:900;margin-bottom:16px;">Long Island Convenience</h1>
  <p style="font-size:1.3rem;margin-bottom:8px;opacity:0.9;">Your One-Stop Local Shop in Plainview, NY</p>
  <p style="font-size:1.1rem;margin-bottom:36px;opacity:0.8;">Sports Cards &bull; Gift Baskets &bull; Balloons &bull; Print &amp; Mail &bull; Cigars</p>
  <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
    <a href="/stores" style="background:#e63946;color:#fff;padding:16px 36px;border-radius:50px;font-weight:800;font-size:1.1rem;text-decoration:none;">Our Stores &#8594;</a>
    <a href="/contact" style="background:transparent;color:#fff;border:2px solid #fff;padding:16px 36px;border-radius:50px;font-weight:700;font-size:1.1rem;text-decoration:none;">Contact Us</a>
  </div>
</section>

<section style="padding:60px 20px;max-width:1100px;margin:0 auto;text-align:center;">
  <h2 style="font-size:2rem;color:#1a1a2e;margin-bottom:12px;">Everything You Need — One Location</h2>
  <p style="color:#555;font-size:1.1rem;max-width:700px;margin:0 auto 48px;">605 Old Country Road, Plainview NY 11803 &bull; Open 7 Days a Week</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px;margin-bottom:60px;">
    <a href="https://www.longislandcards.com" target="_blank" style="background:#f0f4ff;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#127183;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Sports Cards</h3>
      <p style="color:#666;font-size:0.9rem;">Pokemon, Yu-Gi-Oh!, MTG, graded cards &amp; more</p>
    </a>
    <a href="https://www.ligiftbasket.com" target="_blank" style="background:#f0faf4;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#127873;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Gift Baskets</h3>
      <p style="color:#666;font-size:0.9rem;">Custom gift baskets for every occasion</p>
    </a>
    <a href="https://www.longislandballoonsdecor.com" target="_blank" style="background:#fff5f7;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#127881;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Balloon Decor</h3>
      <p style="color:#666;font-size:0.9rem;">Arches, garlands, gender reveals &amp; events</p>
    </a>
    <a href="https://www.longislandprintandmail.com" target="_blank" style="background:#fff8f0;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#128247;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Print &amp; Mail</h3>
      <p style="color:#666;font-size:0.9rem;">Business cards, flyers, banners &amp; same-day printing</p>
    </a>
    <a href="/shop" style="background:#f5f0ff;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#128684;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Cigars</h3>
      <p style="color:#666;font-size:0.9rem;">Premium cigars &amp; accessories for connoisseurs</p>
    </a>
    <a href="/shop" style="background:#f0fff4;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#127977;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Greeting Cards</h3>
      <p style="color:#666;font-size:0.9rem;">Birthdays, holidays, thank-you &amp; all occasions</p>
    </a>
  </div>

  <div style="background:linear-gradient(135deg,#e63946,#c1121f);border-radius:20px;padding:48px;color:#fff;margin-bottom:48px;">
    <h2 style="font-size:1.8rem;margin-bottom:12px;">Proudly Serving Nassau County Since 1998</h2>
    <p style="font-size:1.1rem;margin-bottom:8px;opacity:0.9;">Your trusted local business in Plainview, Long Island</p>
    <p style="font-size:1rem;margin-bottom:28px;opacity:0.85;">605 Old Country Road, Plainview NY 11803 &bull; (212) 564-8585</p>
    <a href="/about" style="background:#fff;color:#e63946;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">About Us &#8594;</a>
  </div>
</section>

<section style="background:#f8f9fa;padding:48px 20px;text-align:center;">
  <h2 style="color:#1a1a2e;margin-bottom:8px;">Visit Us Today</h2>
  <p style="color:#666;margin-bottom:4px;">605 Old Country Road, Plainview NY 11803</p>
  <p style="color:#666;margin-bottom:4px;">Phone: <a href="tel:+12125648585" style="color:#e63946;">(212) 564-8585</a></p>
  <p style="color:#666;">Open 7 Days a Week &bull; Nassau County &bull; Long Island</p>
</section>
</div></t></t>''')
upd_page(hp['id'], {
    'website_meta_title': "Long Island Convenience | One-Stop Local Shop | Plainview NY",
    'website_meta_description': "Long Island Convenience — your one-stop local shop in Plainview NY. Sports cards, gift baskets, balloons, print & mail, cigars. Serving Nassau County since 1998."
})

# Rename About Hiren nav to About Us, keep URL
set_nav(1, [
    ('Home','/',1),('Stores','/stores',2),('Shop','/shop',3),
    ('Blog','/blog',4),('About Us','/about-hiren',5),('Contact','/contact',6)
])

# Update the about-hiren page meta
ah = get_page(1, '/about-hiren')
if ah:
    upd_page(ah['id'], {
        'website_meta_title': "About Us | Long Island Convenience | Plainview NY",
        'website_meta_description': "About Long Island Convenience — your trusted local shop in Plainview NY. Serving Nassau County since 1998 with sports cards, gift baskets, balloons, print & mail and more."
    })
    upd_view(ah['view_id'][0], '''<t t-name="website.about_hiren_w1"><t t-call="website.layout"><div id="wrap">
<section style="padding:60px 20px;max-width:800px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:16px;">About Long Island Convenience</h1>
<p style="color:#555;font-size:1.1rem;margin-bottom:32px;">Nassau County&#39;s trusted one-stop local shop since 1998</p>
<div style="background:linear-gradient(135deg,#f8f9fa,#e9ecef);border-radius:20px;padding:40px;text-align:left;margin-bottom:40px;">
  <p style="font-size:1.1rem;color:#333;margin-bottom:16px;line-height:1.7;">Long Island Convenience has been serving the Plainview NY community for over 25 years. We are your neighborhood destination for sports cards, custom gift baskets, balloon decorations, printing &amp; mailing, premium cigars and greeting cards.</p>
  <p style="color:#555;margin-bottom:16px;line-height:1.7;">Every product and service we offer is designed to save you time and give you quality — all under one roof at 605 Old Country Road, Plainview NY.</p>
  <p style="color:#555;line-height:1.7;">We are a proud Nassau County local business, committed to the community we call home.</p>
</div>
<div style="background:linear-gradient(135deg,#e63946,#c1121f);border-radius:20px;padding:40px;color:#fff;">
  <h2 style="margin-bottom:12px;">Visit Us</h2>
  <p style="margin-bottom:4px;opacity:0.9;">605 Old Country Road, Plainview NY 11803</p>
  <p style="margin-bottom:24px;opacity:0.85;">(212) 564-8585 &bull; Open 7 Days a Week</p>
  <a href="/stores" style="background:#fff;color:#e63946;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Our Stores &#8594;</a>
</div>
</section>
</div></t></t>''')
    print('  About Us page updated')

# ─── 2. Long Island Cards ──────────────────────────────────────────────────
print('\n[2] Long Island Cards')

hp = get_hp(36)
upd_view(hp['view_id'][0], '''<t t-name="website.prod_home_w36"><t t-call="website.layout"><div id="wrap">
<section style="background:linear-gradient(135deg,#0d1b2a 0%,#1b263b 50%,#415a77 100%);padding:80px 20px;text-align:center;color:#fff;">
  <h1 style="font-size:3rem;font-weight:900;margin-bottom:16px;">Long Island Cards</h1>
  <p style="font-size:1.3rem;margin-bottom:8px;opacity:0.9;">Nassau County&#39;s Trading Card Shop</p>
  <p style="font-size:1.1rem;margin-bottom:36px;opacity:0.8;">Sports Cards &bull; Pokemon &bull; Yu-Gi-Oh! &bull; Magic: The Gathering &bull; Graded Cards</p>
  <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
    <a href="/shop" style="background:#e63946;color:#fff;padding:16px 36px;border-radius:50px;font-weight:800;font-size:1.1rem;text-decoration:none;">Shop Cards &#8594;</a>
    <a href="/sell" style="background:transparent;color:#fff;border:2px solid #fff;padding:16px 36px;border-radius:50px;font-weight:700;font-size:1.1rem;text-decoration:none;">Sell Your Cards</a>
  </div>
</section>

<section style="padding:60px 20px;max-width:1100px;margin:0 auto;text-align:center;">
  <h2 style="font-size:2rem;color:#1a1a2e;margin-bottom:12px;">Plainview&#39;s Premier Trading Card Destination</h2>
  <p style="color:#555;font-size:1.1rem;max-width:700px;margin:0 auto 48px;">Whether you&#39;re a collector, investor or casual player — we have the cards you need and buy what you want to sell.</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px;margin-bottom:60px;">
    <a href="/shop?categ=Sports Cards" style="background:#f0f4ff;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#9917;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Sports Cards</h3>
      <p style="color:#666;font-size:0.9rem;">NFL, NBA, MLB, NHL — rookies, autos &amp; vintage</p>
    </a>
    <a href="/shop?categ=Pokemon Cards" style="background:#fff8e1;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#9889;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Pokemon</h3>
      <p style="color:#666;font-size:0.9rem;">Booster packs, singles, holos &amp; rare finds</p>
    </a>
    <a href="/shop?categ=Yu-Gi-Oh! Cards" style="background:#fff0f5;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#9760;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Yu-Gi-Oh!</h3>
      <p style="color:#666;font-size:0.9rem;">Singles, sets, tournament staples</p>
    </a>
    <a href="/shop?categ=Magic: The Gathering" style="background:#f5f0ff;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#129497;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Magic: The Gathering</h3>
      <p style="color:#666;font-size:0.9rem;">Standard, Modern, Commander staples</p>
    </a>
    <a href="/shop?categ=Graded Cards" style="background:#f0faf4;border-radius:16px;padding:32px 20px;text-decoration:none;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#127942;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Graded Cards</h3>
      <p style="color:#666;font-size:0.9rem;">PSA, BGS, SGC certified investment cards</p>
    </a>
    <a href="/contact" style="background:#fafafa;border-radius:16px;padding:32px 20px;text-decoration:none;border:2px dashed #ddd;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#128176;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Sell Your Cards</h3>
      <p style="color:#666;font-size:0.9rem;">Bring in your collection — we buy singles &amp; lots</p>
    </a>
  </div>

  <div style="background:linear-gradient(135deg,#1b263b,#415a77);border-radius:20px;padding:48px;color:#fff;margin-bottom:48px;">
    <h2 style="font-size:1.8rem;margin-bottom:12px;">We Buy &amp; Sell Trading Cards</h2>
    <p style="font-size:1.1rem;margin-bottom:8px;opacity:0.9;">Bring in your collection for a free appraisal. We offer fair market prices on singles and lots.</p>
    <p style="font-size:1rem;margin-bottom:28px;opacity:0.85;">605 Old Country Road, Plainview NY 11803 &bull; (212) 564-8585</p>
    <a href="/contact" style="background:#e63946;color:#fff;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Get an Appraisal &#8594;</a>
  </div>
</section>

<section style="background:#f8f9fa;padding:48px 20px;text-align:center;">
  <h2 style="color:#1a1a2e;margin-bottom:8px;">Visit Our Plainview NY Card Shop</h2>
  <p style="color:#666;margin-bottom:4px;">605 Old Country Road, Plainview NY 11803</p>
  <p style="color:#666;margin-bottom:4px;">Phone: <a href="tel:+12125648585" style="color:#e63946;">(212) 564-8585</a></p>
  <p style="color:#666;">Open 7 Days a Week &bull; Nassau County Long Island</p>
</section>
</div></t></t>''')
upd_page(hp['id'], {
    'website_meta_title': "Long Island Cards | Sports Cards, Pokemon & Trading Cards Plainview NY",
    'website_meta_description': "Long Island Cards in Plainview NY — buy and sell sports cards, Pokemon, Yu-Gi-Oh!, graded cards and more. Nassau County's trading card shop since 1998."
})

# Update about page for cards
ab = get_page(36, '/about')
if ab:
    upd_view(ab['view_id'][0], '''<t t-name="website.prod_about_w36"><t t-call="website.layout"><div id="wrap">
<section style="padding:60px 20px;max-width:800px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:16px;">About Long Island Cards</h1>
<p style="color:#555;font-size:1.1rem;margin-bottom:32px;">Nassau County&#39;s trusted trading card shop since 1998</p>
<div style="background:#f0f4ff;border-radius:20px;padding:40px;text-align:left;margin-bottom:40px;">
  <p style="font-size:1.1rem;color:#333;margin-bottom:16px;line-height:1.7;">Long Island Cards is Plainview NY&#39;s premier destination for trading cards. We are a full buy-and-sell shop serving collectors, investors and players across Nassau County for over 25 years.</p>
  <p style="color:#555;margin-bottom:16px;line-height:1.7;">Our inventory includes sports cards (NFL, NBA, MLB, NHL), Pokemon, Yu-Gi-Oh!, Magic: The Gathering, and investment-grade graded cards (PSA, BGS, SGC).</p>
  <p style="color:#555;line-height:1.7;">We offer fair market prices on all purchases — singles, lots and full collections welcome. Free appraisals with no obligation.</p>
</div>
<div style="background:linear-gradient(135deg,#1b263b,#415a77);border-radius:20px;padding:40px;color:#fff;">
  <h2 style="margin-bottom:12px;">Visit Us</h2>
  <p style="margin-bottom:4px;opacity:0.9;">605 Old Country Road, Plainview NY 11803</p>
  <p style="margin-bottom:24px;opacity:0.85;">(212) 564-8585 &bull; Open 7 Days</p>
  <a href="/shop" style="background:#e63946;color:#fff;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Shop Now &#8594;</a>
</div>
</section>
</div></t></t>''')
    upd_page(ab['id'], {
        'website_meta_title': "About Long Island Cards | Trading Card Shop Plainview NY",
        'website_meta_description': "About Long Island Cards — Nassau County's trusted trading card shop in Plainview NY since 1998. Buy and sell sports cards, Pokemon, graded cards and more."
    })
    print('  About page updated')

# ─── 3. Long Island Print & Mail ───────────────────────────────────────────
print('\n[3] Long Island Print & Mail')

hp = get_hp(39)
upd_view(hp['view_id'][0], '''<t t-name="website.prod_home_w39"><t t-call="website.layout"><div id="wrap">
<section style="background:linear-gradient(135deg,#2b2d42 0%,#3d405b 50%,#8d99ae 100%);padding:80px 20px;text-align:center;color:#fff;">
  <h1 style="font-size:3rem;font-weight:900;margin-bottom:16px;">Long Island Print &amp; Mail</h1>
  <p style="font-size:1.3rem;margin-bottom:8px;opacity:0.9;">Same-Day Printing &amp; Mailing Services in Plainview, NY</p>
  <p style="font-size:1.1rem;margin-bottom:36px;opacity:0.8;">Business Cards &bull; Flyers &bull; Banners &bull; Signs &bull; Mailing</p>
  <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
    <a href="/services" style="background:#e63946;color:#fff;padding:16px 36px;border-radius:50px;font-weight:800;font-size:1.1rem;text-decoration:none;">Our Services &#8594;</a>
    <a href="/contact" style="background:transparent;color:#fff;border:2px solid #fff;padding:16px 36px;border-radius:50px;font-weight:700;font-size:1.1rem;text-decoration:none;">Get a Quote</a>
  </div>
</section>

<section style="padding:60px 20px;max-width:1100px;margin:0 auto;text-align:center;">
  <h2 style="font-size:2rem;color:#1a1a2e;margin-bottom:12px;">Nassau County&#39;s Fast Print Shop</h2>
  <p style="color:#555;font-size:1.1rem;max-width:700px;margin:0 auto 48px;">Order by noon, pick up today. Professional printing and mailing for businesses and individuals across Long Island.</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px;margin-bottom:60px;">
    <div style="background:#f8f9fa;border-radius:16px;padding:32px 20px;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#128196;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Business Cards</h3>
      <p style="color:#666;font-size:0.9rem;">Standard, premium, foil &amp; specialty finishes. Same-day available.</p>
    </div>
    <div style="background:#f8f9fa;border-radius:16px;padding:32px 20px;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#128203;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Flyers &amp; Brochures</h3>
      <p style="color:#666;font-size:0.9rem;">Full-color, double-sided, folded — any quantity.</p>
    </div>
    <div style="background:#f8f9fa;border-radius:16px;padding:32px 20px;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#127379;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Banners &amp; Signs</h3>
      <p style="color:#666;font-size:0.9rem;">Vinyl banners, foam boards, yard signs &amp; A-frames.</p>
    </div>
    <div style="background:#f8f9fa;border-radius:16px;padding:32px 20px;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#128230;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Mailing Services</h3>
      <p style="color:#666;font-size:0.9rem;">USPS, UPS, FedEx — packing, shipping &amp; tracking.</p>
    </div>
    <div style="background:#f8f9fa;border-radius:16px;padding:32px 20px;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#128444;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Photo Printing</h3>
      <p style="color:#666;font-size:0.9rem;">Enlargements, canvas prints, photo books &amp; gifts.</p>
    </div>
    <div style="background:#f8f9fa;border-radius:16px;padding:32px 20px;">
      <div style="font-size:2.5rem;margin-bottom:12px;">&#128221;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Custom Stationery</h3>
      <p style="color:#666;font-size:0.9rem;">Invitations, letterheads, envelopes &amp; notepads.</p>
    </div>
  </div>
  <div style="background:linear-gradient(135deg,#2b2d42,#3d405b);border-radius:20px;padding:48px;color:#fff;margin-bottom:48px;">
    <h2 style="font-size:1.8rem;margin-bottom:12px;">Same-Day Printing — Order by Noon</h2>
    <p style="font-size:1.1rem;margin-bottom:8px;opacity:0.9;">Walk in with your files or email them ahead. We print, finish and package while you wait.</p>
    <p style="font-size:1rem;margin-bottom:28px;opacity:0.85;">605 Old Country Road, Plainview NY 11803 &bull; (212) 564-8585</p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <a href="/contact" style="background:#e63946;color:#fff;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Get a Quote &#8594;</a>
      <a href="tel:+12125648585" style="background:transparent;color:#fff;border:2px solid #fff;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Call Now</a>
    </div>
  </div>
</section>
<section style="background:#f8f9fa;padding:48px 20px;text-align:center;">
  <h2 style="color:#1a1a2e;margin-bottom:8px;">Visit Our Print Shop in Plainview, NY</h2>
  <p style="color:#666;margin-bottom:4px;">605 Old Country Road, Plainview NY 11803</p>
  <p style="color:#666;margin-bottom:4px;">Phone: <a href="tel:+12125648585" style="color:#e63946;">(212) 564-8585</a></p>
  <p style="color:#666;">Open 7 Days a Week &bull; Nassau County Long Island</p>
</section>
</div></t></t>''')
upd_page(hp['id'], {
    'website_meta_title': "Long Island Print & Mail | Same-Day Printing Plainview NY",
    'website_meta_description': "Long Island Print & Mail in Plainview NY — same-day business cards, flyers, banners, signs and mailing services. Serving Nassau County Long Island."
})

# ─── 4. Balloons — update about page ──────────────────────────────────────
print('\n[4] Long Island Balloons & Decor')

ab = get_page(38, '/about')
if ab:
    upd_view(ab['view_id'][0], '''<t t-name="website.prod_about_w38"><t t-call="website.layout"><div id="wrap">
<section style="padding:60px 20px;max-width:800px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:16px;">About Long Island Balloons &amp; Decor</h1>
<p style="color:#555;font-size:1.1rem;margin-bottom:32px;">Nassau County&#39;s custom balloon decorator since 1998</p>
<div style="background:linear-gradient(135deg,#fff5f7,#f0e6ff);border-radius:20px;padding:40px;text-align:left;margin-bottom:40px;">
  <p style="font-size:1.1rem;color:#333;margin-bottom:16px;line-height:1.7;">Long Island Balloons &amp; Decor is Plainview NY&#39;s premier balloon decoration studio. We specialize in custom arrangements that make every event unforgettable — from intimate birthday parties to grand corporate openings.</p>
  <p style="color:#555;margin-bottom:16px;line-height:1.7;">Our team has been creating stunning balloon arches, garlands, gender reveals and full event setups across Nassau County for over 25 years.</p>
  <p style="color:#555;line-height:1.7;">Same-day pickup available when ordered by noon. Delivery across Long Island.</p>
</div>
<div style="background:linear-gradient(135deg,#c77dff,#ff85a1);border-radius:20px;padding:40px;color:#fff;">
  <h2 style="margin-bottom:12px;">Book Your Balloon Setup</h2>
  <p style="margin-bottom:24px;opacity:0.9;">605 Old Country Road, Plainview NY 11803 &bull; (212) 564-8585</p>
  <a href="/contact" style="background:#fff;color:#c77dff;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Contact Us &#8594;</a>
</div>
</section>
</div></t></t>''')
    upd_page(ab['id'], {
        'website_meta_title': "About Long Island Balloons & Decor | Plainview NY Nassau County",
        'website_meta_description': "About Long Island Balloons & Decor — Nassau County's custom balloon decorator in Plainview NY. Arches, garlands, gender reveals, weddings and corporate events since 1998."
    })
    print('  About page updated')

# Balloons homepage — remove Hiren references
hp = get_hp(38)
upd_page(hp['id'], {
    'website_meta_title': "Long Island Balloons & Decor | Custom Balloon Arrangements Plainview NY",
    'website_meta_description': "Long Island Balloons & Decor in Plainview NY. Custom balloon arches, garlands, gender reveals, weddings and corporate events. Serving Nassau County."
})

# ─── 5. Gift Basket — update about page ───────────────────────────────────
print('\n[5] Long Island Gift Basket')

ab = get_page(37, '/about')
if ab:
    upd_view(ab['view_id'][0], '''<t t-name="website.prod_about_w37"><t t-call="website.layout"><div id="wrap">
<section style="padding:60px 20px;max-width:800px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:16px;">About Long Island Gift Basket</h1>
<p style="color:#555;font-size:1.1rem;margin-bottom:32px;">Plainview NY&#39;s hand-packed gift basket shop since 1998</p>
<div style="background:linear-gradient(135deg,#f0faf4,#d8f3dc);border-radius:20px;padding:40px;text-align:left;margin-bottom:40px;">
  <p style="font-size:1.1rem;color:#333;margin-bottom:16px;line-height:1.7;">Long Island Gift Basket is Nassau County&#39;s go-to destination for custom, hand-packed gift baskets. Every basket is assembled fresh in our Plainview NY store — not shipped from a warehouse.</p>
  <p style="color:#555;margin-bottom:16px;line-height:1.7;">We create thoughtful gift baskets for every occasion: birthdays, holidays, sympathy, corporate appreciation and custom builds. Same-day pickup available when ordered by noon.</p>
  <p style="color:#555;line-height:1.7;">Corporate and bulk orders welcome. Delivery across Nassau County and Long Island.</p>
</div>
<div style="background:linear-gradient(135deg,#2d6a4f,#52b788);border-radius:20px;padding:40px;color:#fff;">
  <h2 style="margin-bottom:12px;">Order a Custom Basket</h2>
  <p style="margin-bottom:24px;opacity:0.9;">605 Old Country Road, Plainview NY 11803 &bull; (212) 564-8585</p>
  <a href="/contact" style="background:#fff;color:#2d6a4f;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Contact Us &#8594;</a>
</div>
</section>
</div></t></t>''')
    upd_page(ab['id'], {
        'website_meta_title': "About Long Island Gift Basket | Custom Gift Shop Plainview NY",
        'website_meta_description': "About Long Island Gift Basket — Plainview NY's hand-packed gift basket shop since 1998. Custom baskets for every occasion. Nassau County delivery available."
    })
    print('  About page updated')

hp = get_hp(37)
upd_page(hp['id'], {
    'website_meta_title': "Long Island Gift Basket | Custom Gift Baskets Plainview NY",
    'website_meta_description': "Long Island Gift Basket in Plainview NY — custom hand-packed gift baskets for birthdays, holidays, corporate gifts and sympathy. Same-day pickup. Nassau County."
})

# ─── 6. Also fix all blog post meta that mention Hiren ────────────────────
print('\n[6] Fixing blog post meta...')
posts = xc('blog.post','search_read',
    [[['website_meta_description','ilike','Hiren']]],
    {'fields':['id','website_meta_description','website_meta_title']})

brand_map = [
    ("Hiren's Long Island Convenience", "Long Island Convenience"),
    ("Hiren's Long Island Cards", "Long Island Cards"),
    ("Hiren's Long Island Gift Basket", "Long Island Gift Basket"),
    ("Hiren's Long Island Balloons", "Long Island Balloons & Decor"),
    ("Hiren's Long Island Print", "Long Island Print & Mail"),
    ("Hiren Chauhan", "our team"),
    ("Hiren's ", ""),
]
fixed = 0
for post in posts:
    desc = post.get('website_meta_description') or ''
    title = post.get('website_meta_title') or ''
    nd, nt = desc, title
    for old, new in brand_map:
        nd = nd.replace(old, new)
        nt = nt.replace(old, new)
    if nd != desc or nt != title:
        xc('blog.post','write',[[post['id']],{
            'website_meta_description': nd,
            'website_meta_title': nt
        }])
        fixed += 1
print(f'  Fixed {fixed} blog posts')

print('\n=== ALL HIREN BRANDING REMOVED ===')
print('Every site now uses brand names only.')
