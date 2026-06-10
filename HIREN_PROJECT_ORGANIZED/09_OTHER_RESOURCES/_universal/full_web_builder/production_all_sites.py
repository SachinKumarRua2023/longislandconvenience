import xmlrpc.client

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

# ─────────────────────────────────────────────────────────────────────────────
def make_page(wid, url, name, meta_title, meta_desc, content):
    key = (url.strip('/').replace('-','_').replace('/','_') or 'home') + f'_w{wid}'
    view_arch = f'<t t-name="website.prod_{key}"><t t-call="website.layout"><div id="wrap">{content}</div></t></t>'
    existing = xc('website.page','search_read',[[['url','=',url],['website_id','=',wid]]],{'fields':['id','view_id']})
    if existing:
        pid = existing[0]['id']
        if existing[0].get('view_id'):
            xc('ir.ui.view','write',[[existing[0]['view_id'][0]],{'arch_db':view_arch}])
        xc('website.page','write',[[pid],{'website_meta_title':meta_title,'website_meta_description':meta_desc,'website_published':True}])
        print(f'  Updated {url}')
        return pid
    vid = xc('ir.ui.view','create',[{'name':name,'type':'qweb','arch_db':view_arch}])
    pid = xc('website.page','create',[{'url':url,'name':name,'website_id':wid,'view_id':vid,
        'website_meta_title':meta_title,'website_meta_description':meta_desc,
        'website_published':True,'is_published':True}])
    print(f'  Created {url}')
    return pid

def set_nav(wid, items):
    menus = xc('website.menu','search_read',[[['website_id','=',wid]]],{'fields':['id','parent_id']})
    root = [mn for mn in menus if not mn['parent_id']]
    if not root:
        return
    root_id = root[0]['id']
    children = [mn['id'] for mn in menus if mn['parent_id']]
    if children:
        xc('website.menu','unlink',[children])
    for name, url, seq in items:
        xc('website.menu','create',[{'name':name,'url':url,'website_id':wid,'parent_id':root_id,'sequence':seq}])
    print(f'  Nav set: {[i[0] for i in items]}')

def update_homepage(wid, meta_title, meta_desc, content):
    hp = xc('website.page','search_read',[[['website_id','=',wid],['url','=','/']]],{'fields':['id','view_id']})
    if not hp:
        return
    hp = hp[0]
    xc('website.page','write',[[hp['id']],{'website_meta_title':meta_title,'website_meta_description':meta_desc,'website_published':True,'is_published':True}])
    if hp.get('view_id'):
        view_arch = f'<t t-name="website.prod_home_w{wid}"><t t-call="website.layout"><div id="wrap">{content}</div></t></t>'
        xc('ir.ui.view','write',[[hp['view_id'][0]],{'arch_db':view_arch}])
    print(f'  Homepage updated (WID={wid})')

print('\n' + '='*60)
print('PRODUCTION BUILD — ALL SITES')
print('='*60)

# ═══════════════════════════════════════════════════════════════
# SITE 1 — Long Island Convenience
# ═══════════════════════════════════════════════════════════════
print('\n[1/5] Long Island Convenience')

update_homepage(1,
    "Long Island Convenience | Hiren's Local Store Hub | Plainview NY",
    "Hiren's one-stop shop in Plainview NY — sports cards, gift baskets, balloons, print & mail, cigars. Serving Nassau County since 1998.",
    '''<section style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);padding:80px 20px;text-align:center;color:#fff;">
  <h1 style="font-size:3rem;font-weight:900;margin-bottom:16px;">Hiren&#39;s Long Island Convenience</h1>
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
    <p style="font-size:1.1rem;margin-bottom:8px;opacity:0.9;">Hiren Chauhan — your trusted local business owner in Plainview, Long Island</p>
    <p style="font-size:1rem;margin-bottom:28px;opacity:0.85;">605 Old Country Road, Plainview NY 11803 &bull; (212) 564-8585</p>
    <a href="/about-hiren" style="background:#fff;color:#e63946;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Meet Hiren &#8594;</a>
  </div>
</section>

<section style="background:#f8f9fa;padding:48px 20px;text-align:center;">
  <h2 style="color:#1a1a2e;margin-bottom:8px;">Visit Us Today</h2>
  <p style="color:#666;margin-bottom:4px;">605 Old Country Road, Plainview NY 11803</p>
  <p style="color:#666;margin-bottom:4px;">Phone: <a href="tel:+12125648585" style="color:#e63946;">(212) 564-8585</a></p>
  <p style="color:#666;">Open 7 Days a Week &bull; Nassau County &bull; Long Island</p>
</section>''')

set_nav(1, [
    ('Home','/',1), ('Stores','/stores',2), ('Shop','/shop',3),
    ('Blog','/blog',4), ('About Hiren','/about-hiren',5), ('Contact','/contact',6)
])

# ═══════════════════════════════════════════════════════════════
# SITE 36 — Long Island Cards
# ═══════════════════════════════════════════════════════════════
print('\n[2/5] Long Island Cards')

update_homepage(36,
    "Long Island Cards | Sports Cards, Pokemon & Trading Cards Plainview NY",
    "Hiren's Long Island Cards in Plainview NY. Buy and sell sports cards, Pokemon, Yu-Gi-Oh!, Magic the Gathering, graded cards. Nassau County's trading card shop.",
    '''<section style="background:linear-gradient(135deg,#0d1b2a 0%,#1b263b 50%,#415a77 100%);padding:80px 20px;text-align:center;color:#fff;">
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
</section>''')

# Fix sell page and about page for cards
make_page(36, '/sell', 'Sell Your Cards',
    'Sell Trading Cards Long Island | Buy Sports Cards Plainview NY',
    'Sell your trading cards at Long Island Cards in Plainview NY. We buy sports cards, Pokemon, graded cards and collections. Fair prices, same-day cash. Nassau County.',
    '''<section style="padding:60px 20px;max-width:900px;margin:0 auto;">
<h1 style="color:#1a1a2e;text-align:center;margin-bottom:8px;">Sell Your Trading Cards</h1>
<p style="text-align:center;color:#666;margin-bottom:48px;">We buy singles, lots and full collections — fair market prices, same day</p>
<div style="display:grid;gap:24px;margin-bottom:48px;">
  <div style="background:#f0f4ff;border-radius:16px;padding:32px;">
    <h2 style="color:#1b263b;">We Buy All Types</h2>
    <p>Sports cards (NFL, NBA, MLB, NHL), Pokemon, Yu-Gi-Oh!, Magic: The Gathering, graded cards (PSA, BGS, SGC), vintage collections and unopened product.</p>
  </div>
  <div style="background:#f0f4ff;border-radius:16px;padding:32px;">
    <h2 style="color:#1b263b;">How It Works</h2>
    <p><strong>1.</strong> Bring your cards or collection to our Plainview NY store.<br>
    <strong>2.</strong> We evaluate on the spot — no appointment needed.<br>
    <strong>3.</strong> Get a fair offer based on current market value.<br>
    <strong>4.</strong> Walk out with cash or store credit (store credit gets you 10% more).</p>
  </div>
  <div style="background:#f0f4ff;border-radius:16px;padding:32px;">
    <h2 style="color:#1b263b;">Large Collections Welcome</h2>
    <p>Have thousands of cards? Call ahead and we&#39;ll schedule a dedicated time to evaluate your full collection. We handle estates, liquidations and bulk lots.</p>
  </div>
</div>
<div style="text-align:center;">
  <a href="/contact" style="background:#e63946;color:#fff;padding:16px 40px;border-radius:50px;font-size:1.1rem;font-weight:700;text-decoration:none;">Bring Your Cards In &#8594;</a>
</div>
</section>''')

make_page(36, '/about', 'About Long Island Cards',
    'About Long Island Cards | Hiren Chauhan Plainview NY Trading Card Shop',
    "About Hiren's Long Island Cards trading card shop in Plainview NY. Nassau County's trusted source for sports cards, Pokemon, graded cards since 1998.",
    '''<section style="padding:60px 20px;max-width:800px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:16px;">About Long Island Cards</h1>
<p style="color:#555;font-size:1.15rem;margin-bottom:32px;">Nassau County&#39;s trusted trading card shop since 1998</p>
<div style="background:#f0f4ff;border-radius:20px;padding:40px;text-align:left;margin-bottom:40px;">
  <p style="font-size:1.1rem;color:#333;margin-bottom:16px;">Long Island Cards is owned and operated by <strong>Hiren Chauhan</strong>, a Plainview NY local who has been passionate about trading cards for over 25 years.</p>
  <p style="color:#555;margin-bottom:16px;">What started as a personal hobby became Nassau County&#39;s go-to destination for sports cards, Pokemon, Yu-Gi-Oh!, Magic: The Gathering and investment-grade graded cards.</p>
  <p style="color:#555;">We are a full buy-and-sell shop — whether you want to grow your collection or turn cards into cash, we offer fair prices and expert knowledge on every transaction.</p>
</div>
<div style="background:linear-gradient(135deg,#1b263b,#415a77);border-radius:20px;padding:40px;color:#fff;">
  <h2 style="margin-bottom:12px;">Visit Us</h2>
  <p style="margin-bottom:4px;opacity:0.9;">605 Old Country Road, Plainview NY 11803</p>
  <p style="margin-bottom:24px;opacity:0.85;">Phone: (212) 564-8585 &bull; Open 7 Days</p>
  <a href="/shop" style="background:#e63946;color:#fff;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Shop Now &#8594;</a>
</div>
</section>''')

set_nav(36, [
    ('Home','/',1), ('Shop','/shop',2), ('Sports Cards','/shop?categ=Sports Cards',3),
    ('Pokemon','/shop?categ=Pokemon Cards',4), ('Sell Cards','/sell',5),
    ('About','/about',6), ('Contact','/contact',7)
])

# ═══════════════════════════════════════════════════════════════
# SITE 39 — Long Island Print & Mail
# ═══════════════════════════════════════════════════════════════
print('\n[3/5] Long Island Print & Mail')

update_homepage(39,
    "Long Island Print & Mail | Same-Day Printing Plainview NY | Nassau County",
    "Hiren's Long Island Print & Mail in Plainview NY. Same-day business cards, flyers, banners, signs and mailing services. Serving Nassau County Long Island.",
    '''<section style="background:linear-gradient(135deg,#2b2d42 0%,#3d405b 50%,#8d99ae 100%);padding:80px 20px;text-align:center;color:#fff;">
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
</section>''')

set_nav(39, [
    ('Home','/',1), ('Services','/services',2), ('Shop','/shop',3),
    ('Blog','/blog',4), ('Contact','/contact',5)
])

# ═══════════════════════════════════════════════════════════════
# SITE 41 — JHD Advisor (fix domain + build)
# ═══════════════════════════════════════════════════════════════
print('\n[4/5] JHD Advisor')

# Fix domain to jhdadvisor.com (managed domain registered)
xc('website','write',[[41],{'name':'JHD Advisor','domain':'https://www.jhdadvisor.com'}])
print('  Domain updated to https://www.jhdadvisor.com')

update_homepage(41,
    "JHD Advisor | Digital Agency & E-Commerce Experts | Startup to Unicorn",
    "JHD Advisor LLC — digital agency, e-commerce solutions and startup-to-unicorn growth support. Helping US businesses build, scale and dominate online.",
    '''<section style="background:linear-gradient(135deg,#050505 0%,#0a0a0a 40%,#1a0533 100%);padding:90px 20px;text-align:center;color:#fff;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 30% 50%,rgba(138,43,226,0.15),transparent 60%),radial-gradient(ellipse at 70% 50%,rgba(0,191,255,0.1),transparent 60%);"></div>
  <div style="position:relative;z-index:1;">
    <div style="display:inline-block;background:rgba(138,43,226,0.2);border:1px solid rgba(138,43,226,0.4);border-radius:50px;padding:8px 20px;font-size:0.85rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:24px;color:#c77dff;">JHD Advisor LLC &bull; USA Registered</div>
    <h1 style="font-size:3.2rem;font-weight:900;margin-bottom:20px;line-height:1.15;background:linear-gradient(135deg,#fff,#c77dff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">From Startup to Unicorn.<br>We Build What Scales.</h1>
    <p style="font-size:1.2rem;margin-bottom:12px;opacity:0.85;max-width:600px;margin-left:auto;margin-right:auto;">Digital Agency &bull; E-Commerce &bull; AI Automation &bull; Growth Strategy</p>
    <p style="font-size:1rem;margin-bottom:40px;opacity:0.65;">Helping US businesses dominate their market online</p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <a href="/services" style="background:linear-gradient(135deg,#8a2be2,#4361ee);color:#fff;padding:16px 40px;border-radius:50px;font-weight:800;font-size:1.1rem;text-decoration:none;box-shadow:0 4px 24px rgba(138,43,226,0.4);">Our Services &#8594;</a>
      <a href="/contact" style="background:transparent;color:#fff;border:2px solid rgba(255,255,255,0.3);padding:16px 40px;border-radius:50px;font-weight:700;font-size:1.1rem;text-decoration:none;">Get a Free Strategy Call</a>
    </div>
  </div>
</section>

<section style="padding:70px 20px;max-width:1100px;margin:0 auto;text-align:center;">
  <h2 style="font-size:2rem;color:#1a1a2e;margin-bottom:12px;">What We Do</h2>
  <p style="color:#555;font-size:1.1rem;max-width:650px;margin:0 auto 48px;">Full-stack digital growth for startups, small businesses and established brands ready to scale.</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:24px;margin-bottom:60px;text-align:left;">
    <div style="background:#fafafa;border:1px solid #e8e8f0;border-radius:16px;padding:32px;">
      <div style="font-size:2rem;margin-bottom:12px;">&#128640;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">E-Commerce Development</h3>
      <p style="color:#666;font-size:0.95rem;">Odoo, Shopify, WooCommerce — full store builds, product uploads, payment setup and launch. We handle everything.</p>
    </div>
    <div style="background:#fafafa;border:1px solid #e8e8f0;border-radius:16px;padding:32px;">
      <div style="font-size:2rem;margin-bottom:12px;">&#129504;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">AI &amp; Automation</h3>
      <p style="color:#666;font-size:0.95rem;">n8n workflows, AI chatbots, automated CRM, lead nurturing and business process automation that cuts costs 40%.</p>
    </div>
    <div style="background:#fafafa;border:1px solid #e8e8f0;border-radius:16px;padding:32px;">
      <div style="font-size:2rem;margin-bottom:12px;">&#128200;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">SEO &amp; GEO Strategy</h3>
      <p style="color:#666;font-size:0.95rem;">Rank on Google and appear in AI Overviews. Local SEO, content strategy, schema markup and search domination.</p>
    </div>
    <div style="background:#fafafa;border:1px solid #e8e8f0;border-radius:16px;padding:32px;">
      <div style="font-size:2rem;margin-bottom:12px;">&#127981;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Startup to Unicorn</h3>
      <p style="color:#666;font-size:0.95rem;">Ideation to IPO roadmap. Business model design, MVP launch, investor-ready pitch decks and growth playbooks.</p>
    </div>
    <div style="background:#fafafa;border:1px solid #e8e8f0;border-radius:16px;padding:32px;">
      <div style="font-size:2rem;margin-bottom:12px;">&#128187;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Website &amp; Brand Design</h3>
      <p style="color:#666;font-size:0.95rem;">Professional websites, brand identity, UI/UX design and digital presence that converts visitors into customers.</p>
    </div>
    <div style="background:#fafafa;border:1px solid #e8e8f0;border-radius:16px;padding:32px;">
      <div style="font-size:2rem;margin-bottom:12px;">&#128101;</div>
      <h3 style="color:#1a1a2e;margin-bottom:8px;">Digital Marketing</h3>
      <p style="color:#666;font-size:0.95rem;">Google Ads, Meta Ads, email marketing, social media management and performance-driven campaigns with real ROI.</p>
    </div>
  </div>

  <div style="background:linear-gradient(135deg,#0a0a0a,#1a0533);border-radius:20px;padding:56px;color:#fff;margin-bottom:48px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at center,rgba(138,43,226,0.2),transparent 70%);"></div>
    <div style="position:relative;z-index:1;">
      <h2 style="font-size:1.9rem;margin-bottom:16px;">Ready to Scale Your Business?</h2>
      <p style="font-size:1.1rem;margin-bottom:8px;opacity:0.85;">Free 30-minute strategy call — no sales pitch, just a plan.</p>
      <p style="font-size:1rem;margin-bottom:32px;opacity:0.65;">JHD Advisor LLC &bull; USA Registered &bull; Working with founders worldwide</p>
      <a href="/contact" style="background:linear-gradient(135deg,#8a2be2,#4361ee);color:#fff;padding:16px 40px;border-radius:50px;font-weight:800;font-size:1.1rem;text-decoration:none;display:inline-block;box-shadow:0 4px 24px rgba(138,43,226,0.5);">Book Free Strategy Call &#8594;</a>
    </div>
  </div>

  <h2 style="font-size:1.8rem;color:#1a1a2e;margin-bottom:32px;">Why JHD Advisor?</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;text-align:left;">
    <div style="padding:20px;">&#10003; <strong>USA registered LLC</strong> — legal, credible, accountable</div>
    <div style="padding:20px;">&#10003; <strong>Real results</strong> — 7 live e-commerce sites built and scaled</div>
    <div style="padding:20px;">&#10003; <strong>AI-first approach</strong> — automation before headcount</div>
    <div style="padding:20px;">&#10003; <strong>Full-stack</strong> — strategy, build, launch and grow in one team</div>
    <div style="padding:20px;">&#10003; <strong>Transparent pricing</strong> — fixed project fees, no hidden costs</div>
    <div style="padding:20px;">&#10003; <strong>Long-term partner</strong> — not an agency, a growth co-pilot</div>
  </div>
</section>''')

make_page(41, '/services', 'Services',
    'Digital Agency Services | JHD Advisor LLC | E-Commerce, AI, SEO USA',
    'JHD Advisor services: e-commerce development, AI automation, SEO, website design, startup consulting and digital marketing. US-based agency for growing businesses.',
    '''<section style="padding:70px 20px;max-width:950px;margin:0 auto;">
<h1 style="color:#1a1a2e;text-align:center;margin-bottom:8px;">Our Services</h1>
<p style="text-align:center;color:#666;margin-bottom:56px;font-size:1.1rem;">Full-stack digital growth — from first website to Series A</p>
<div style="display:grid;gap:32px;">
  <div style="border:2px solid #e8e8f0;border-radius:16px;padding:36px;">
    <h2 style="color:#8a2be2;margin-bottom:12px;">&#128640; E-Commerce Development</h2>
    <p style="margin-bottom:12px;">Complete e-commerce store builds on Odoo, Shopify or WooCommerce. Product catalog setup, payment gateway integration, shipping configuration and go-live support.</p>
    <p style="color:#888;font-size:0.9rem;">Starting at $1,500 &bull; 2-4 week delivery</p>
  </div>
  <div style="border:2px solid #e8e8f0;border-radius:16px;padding:36px;">
    <h2 style="color:#8a2be2;margin-bottom:12px;">&#129504; AI &amp; Business Automation</h2>
    <p style="margin-bottom:12px;">Custom n8n automation workflows, AI chatbots for customer service, automated lead nurturing, CRM integrations and business process optimization that saves 20+ hours/week.</p>
    <p style="color:#888;font-size:0.9rem;">Starting at $800 &bull; 1-3 week delivery</p>
  </div>
  <div style="border:2px solid #e8e8f0;border-radius:16px;padding:36px;">
    <h2 style="color:#8a2be2;margin-bottom:12px;">&#128200; SEO &amp; Google AI Overviews</h2>
    <p style="margin-bottom:12px;">Local SEO, national SEO and GEO (Generative Engine Optimization) to appear in Google AI Overviews. Full technical SEO, content strategy, schema markup, Google Search Console management.</p>
    <p style="color:#888;font-size:0.9rem;">Starting at $600/month &bull; Results in 60-90 days</p>
  </div>
  <div style="border:2px solid #e8e8f0;border-radius:16px;padding:36px;">
    <h2 style="color:#8a2be2;margin-bottom:12px;">&#128187; Website &amp; Brand Design</h2>
    <p style="margin-bottom:12px;">Professional website design, brand identity (logo, colors, typography), UI/UX for conversion optimization. Mobile-first, fast-loading, SEO-ready from day one.</p>
    <p style="color:#888;font-size:0.9rem;">Starting at $1,200 &bull; 2-3 week delivery</p>
  </div>
  <div style="border:2px solid #e8e8f0;border-radius:16px;padding:36px;">
    <h2 style="color:#8a2be2;margin-bottom:12px;">&#127981; Startup to Unicorn Consulting</h2>
    <p style="margin-bottom:12px;">Business model design, MVP strategy, investor-ready pitch deck creation, market analysis and the step-by-step growth roadmap that takes you from idea to funded company.</p>
    <p style="color:#888;font-size:0.9rem;">Starting at $2,500 &bull; Ongoing advisory available</p>
  </div>
  <div style="border:2px solid #e8e8f0;border-radius:16px;padding:36px;">
    <h2 style="color:#8a2be2;margin-bottom:12px;">&#128101; Digital Marketing &amp; Paid Ads</h2>
    <p style="margin-bottom:12px;">Google Ads, Meta Ads, email marketing campaigns and social media management. Performance-driven with transparent reporting. Average 3-5x ROAS for e-commerce clients.</p>
    <p style="color:#888;font-size:0.9rem;">Starting at $500/month + ad spend &bull; First month includes free audit</p>
  </div>
</div>
<div style="text-align:center;margin-top:56px;">
  <a href="/contact" style="background:linear-gradient(135deg,#8a2be2,#4361ee);color:#fff;padding:18px 48px;border-radius:50px;font-size:1.15rem;font-weight:800;text-decoration:none;display:inline-block;box-shadow:0 4px 24px rgba(138,43,226,0.3);">Book a Free Strategy Call &#8594;</a>
</div>
</section>''')

make_page(41, '/about', 'About JHD Advisor',
    'About JHD Advisor LLC | US Digital Agency | Startup to Unicorn Experts',
    'About JHD Advisor LLC — a USA-registered digital agency specializing in e-commerce, AI automation and startup growth consulting. Real results for real businesses.',
    '''<section style="padding:70px 20px;max-width:850px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:16px;">About JHD Advisor LLC</h1>
<p style="color:#555;font-size:1.15rem;margin-bottom:40px;">USA-registered digital agency &amp; growth consultancy</p>
<div style="background:linear-gradient(135deg,#fafafa,#f0e6ff);border-radius:20px;padding:48px;text-align:left;margin-bottom:40px;">
  <p style="font-size:1.1rem;color:#333;margin-bottom:20px;line-height:1.7;">JHD Advisor LLC is a USA-registered digital agency that specializes in e-commerce development, AI automation and startup-to-unicorn growth strategy.</p>
  <p style="color:#555;margin-bottom:20px;line-height:1.7;">We were founded on a simple belief: every business deserves enterprise-level digital infrastructure, regardless of size. We&#39;ve built and scaled 7 live e-commerce websites, implemented AI automation workflows, and helped local businesses in Plainview NY compete nationally.</p>
  <p style="color:#555;line-height:1.7;">Our approach is AI-first and results-driven. We don&#39;t just build — we build systems that generate revenue while you sleep.</p>
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:24px;margin-bottom:48px;text-align:center;">
  <div style="background:#f5f0ff;border-radius:16px;padding:28px 20px;">
    <div style="font-size:2.5rem;font-weight:900;color:#8a2be2;margin-bottom:8px;">7+</div>
    <p style="color:#555;font-size:0.9rem;">Live E-Commerce Sites Built</p>
  </div>
  <div style="background:#f0f4ff;border-radius:16px;padding:28px 20px;">
    <div style="font-size:2.5rem;font-weight:900;color:#4361ee;margin-bottom:8px;">USA</div>
    <p style="color:#555;font-size:0.9rem;">Registered LLC Company</p>
  </div>
  <div style="background:#f0faf4;border-radius:16px;padding:28px 20px;">
    <div style="font-size:2.5rem;font-weight:900;color:#2d6a4f;margin-bottom:8px;">AI</div>
    <p style="color:#555;font-size:0.9rem;">First Automation Approach</p>
  </div>
</div>
<div style="background:linear-gradient(135deg,#0a0a0a,#1a0533);border-radius:20px;padding:48px;color:#fff;">
  <h2 style="margin-bottom:16px;">Let&#39;s Build Something Great</h2>
  <p style="opacity:0.85;margin-bottom:28px;">Book a free 30-minute strategy call. No pitch — just a plan tailored to your business.</p>
  <a href="/contact" style="background:linear-gradient(135deg,#8a2be2,#4361ee);color:#fff;padding:16px 36px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Book Free Call &#8594;</a>
</div>
</section>''')

make_page(41, '/contact', 'Contact JHD Advisor',
    'Contact JHD Advisor | Book Free Strategy Call | Digital Agency USA',
    'Contact JHD Advisor LLC to book a free strategy call. E-commerce, AI automation, SEO and startup consulting for US businesses. Response within 24 hours.',
    '''<section style="padding:70px 20px;max-width:800px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:8px;">Get In Touch</h1>
<p style="color:#666;margin-bottom:48px;font-size:1.1rem;">Book a free 30-minute strategy call — response within 24 hours</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;text-align:left;margin-bottom:48px;">
  <div style="background:#f8f9fa;border-radius:16px;padding:32px;">
    <h3 style="color:#8a2be2;margin-bottom:16px;">JHD Advisor LLC</h3>
    <p><strong>Company:</strong><br>JHD Advisor LLC<br>USA Registered</p>
    <p style="margin-top:16px;"><strong>Email:</strong><br><a href="mailto:countrycoveinc@gmail.com" style="color:#8a2be2;">countrycoveinc@gmail.com</a></p>
  </div>
  <div style="background:#f8f9fa;border-radius:16px;padding:32px;">
    <h3 style="color:#8a2be2;margin-bottom:16px;">Response Time</h3>
    <p><strong>Strategy Calls:</strong><br>Scheduled within 48 hours</p>
    <p style="margin-top:16px;"><strong>Project Inquiries:</strong><br>Quoted within 24 hours</p>
    <p style="margin-top:16px;"><strong>Emergency Support:</strong><br>Same-day for active clients</p>
  </div>
</div>
<div style="background:linear-gradient(135deg,#0a0a0a,#1a0533);border-radius:20px;padding:48px;color:#fff;">
  <h2 style="margin-bottom:16px;">Book Your Free Strategy Call</h2>
  <p style="opacity:0.85;margin-bottom:8px;">Tell us about your business — where you are and where you want to go.</p>
  <p style="opacity:0.65;margin-bottom:32px;font-size:0.95rem;">E-commerce &bull; AI automation &bull; SEO &bull; Startup consulting &bull; Website design</p>
  <a href="mailto:countrycoveinc@gmail.com" style="background:linear-gradient(135deg,#8a2be2,#4361ee);color:#fff;padding:16px 40px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;box-shadow:0 4px 24px rgba(138,43,226,0.4);">Email JHD Advisor &#8594;</a>
</div>
</section>''')

set_nav(41, [
    ('Home','/',1), ('Services','/services',2), ('About','/about',3), ('Contact','/contact',4)
])
xc('website','write',[[41],{'name':'JHD Advisor'}])

# ═══════════════════════════════════════════════════════════════
# SITE 37 & 38 — Add About pages (Balloons + Gift Basket)
# ═══════════════════════════════════════════════════════════════
print('\n[5/5] About pages for Balloons & Gift Basket')

make_page(38, '/about', 'About Long Island Balloons',
    'About Long Island Balloons & Decor | Hiren Chauhan Plainview NY',
    "About Hiren's Long Island Balloons & Decor in Plainview NY. Nassau County's custom balloon decorator for weddings, birthdays, gender reveals and corporate events.",
    '''<section style="padding:60px 20px;max-width:800px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:16px;">About Long Island Balloons &amp; Decor</h1>
<p style="color:#555;font-size:1.1rem;margin-bottom:32px;">Nassau County&#39;s custom balloon decorator since 1998</p>
<div style="background:linear-gradient(135deg,#fff5f7,#f0e6ff);border-radius:20px;padding:40px;text-align:left;margin-bottom:40px;">
  <p style="font-size:1.1rem;color:#333;margin-bottom:16px;">Long Island Balloons &amp; Decor is owned by <strong>Hiren Chauhan</strong>, a Plainview NY local who has been creating custom balloon arrangements for over 25 years.</p>
  <p style="color:#555;margin-bottom:16px;">We specialize in making every event unforgettable — from intimate birthday parties to grand corporate openings. Same-day pickup is available when ordered by noon.</p>
  <p style="color:#555;">Serving Plainview, Nassau County and all of Long Island with delivery available.</p>
</div>
<div style="background:linear-gradient(135deg,#c77dff,#ff85a1);border-radius:20px;padding:40px;color:#fff;">
  <h2 style="margin-bottom:12px;">Book Your Balloon Setup</h2>
  <p style="margin-bottom:24px;opacity:0.9;">Call us or visit the shop at 605 Old Country Road, Plainview NY 11803</p>
  <a href="/contact" style="background:#fff;color:#c77dff;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Contact Us &#8594;</a>
</div>
</section>''')

set_nav(38, [
    ('Home','/',1), ('Services','/services',2), ('About','/about',3), ('Contact','/contact',4)
])

make_page(37, '/about', 'About Long Island Gift Basket',
    'About Long Island Gift Basket | Hiren Chauhan Plainview NY Gift Shop',
    "About Hiren's Long Island Gift Basket in Plainview NY. Hand-packed custom gift baskets for Nassau County since 1998. Birthdays, corporate gifts, sympathy and holidays.",
    '''<section style="padding:60px 20px;max-width:800px;margin:0 auto;text-align:center;">
<h1 style="color:#1a1a2e;margin-bottom:16px;">About Long Island Gift Basket</h1>
<p style="color:#555;font-size:1.1rem;margin-bottom:32px;">Plainview NY&#39;s hand-packed gift basket shop since 1998</p>
<div style="background:linear-gradient(135deg,#f0faf4,#d8f3dc);border-radius:20px;padding:40px;text-align:left;margin-bottom:40px;">
  <p style="font-size:1.1rem;color:#333;margin-bottom:16px;">Long Island Gift Basket is owned by <strong>Hiren Chauhan</strong>, a Plainview NY local who has been creating custom gift baskets for over 25 years.</p>
  <p style="color:#555;margin-bottom:16px;">Every basket is hand-packed in our Plainview NY store — not mass-produced in a warehouse. We use quality products and take the time to create something truly thoughtful.</p>
  <p style="color:#555;">Same-day pickup available (order by noon). Corporate and bulk orders welcome. Delivery across Nassau County.</p>
</div>
<div style="background:linear-gradient(135deg,#2d6a4f,#52b788);border-radius:20px;padding:40px;color:#fff;">
  <h2 style="margin-bottom:12px;">Order a Custom Basket</h2>
  <p style="margin-bottom:24px;opacity:0.9;">Call or visit: 605 Old Country Road, Plainview NY 11803 &bull; (212) 564-8585</p>
  <a href="/contact" style="background:#fff;color:#2d6a4f;padding:14px 32px;border-radius:50px;font-weight:700;text-decoration:none;display:inline-block;">Contact Us &#8594;</a>
</div>
</section>''')

set_nav(37, [
    ('Home','/',1), ('Gift Baskets','/gift-baskets',2), ('About','/about',3),
    ('Shop','/shop',4), ('Contact','/contact',5)
])

print('\n' + '='*60)
print('ALL SITES PRODUCTION BUILD COMPLETE')
print('='*60)
print('\nLive sites:')
print('  https://www.longislandconvenience.com')
print('  https://www.longislandcards.com')
print('  https://www.longislandprintandmail.com')
print('  https://www.longislandballoonsdecor.com')
print('  https://www.ligiftbasket.com')
print('  https://www.jhdadvisor.com  (domain updated)')
print('\nREMINDER: consultcyber.net expires JUNE 6 — renew at GoDaddy NOW')
