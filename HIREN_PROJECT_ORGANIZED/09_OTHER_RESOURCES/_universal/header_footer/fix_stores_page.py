import xmlrpc.client

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

arch = '''<t t-name="website.stores_w1"><t t-call="website.layout"><div id="wrap">

<section style="background:linear-gradient(135deg,#0f0c29,#302b63);padding:60px 20px;text-align:center;color:#fff;">
  <h1 style="font-size:2.5rem;font-weight:900;margin-bottom:12px;">Our 7 Brands</h1>
  <p style="font-size:1.1rem;opacity:0.8;">All at 605 Old Country Road, Plainview NY 11803 &bull; Open 7 Days</p>
</section>

<section style="padding:60px 20px;max-width:1200px;margin:0 auto;">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;">

    <a href="https://www.longislandcards.com" target="_blank" style="text-decoration:none;">
      <div style="background:#fff;border:2px solid #e8eaf6;border-radius:20px;padding:36px 28px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
          <div style="font-size:3rem;">&#127183;</div>
          <span style="background:#22c55e;color:#fff;font-size:0.75rem;font-weight:700;padding:4px 12px;border-radius:50px;">LIVE</span>
        </div>
        <h3 style="color:#1a1a2e;font-size:1.2rem;margin-bottom:8px;">Long Island Cards</h3>
        <p style="color:#666;font-size:0.9rem;margin-bottom:16px;">Sports cards, Pokemon, Yu-Gi-Oh!, Magic: The Gathering, graded cards. Buy &amp; sell.</p>
        <div style="color:#e63946;font-weight:700;font-size:0.9rem;">longislandcards.com &#8594;</div>
      </div>
    </a>

    <a href="https://www.ligiftbasket.com" target="_blank" style="text-decoration:none;">
      <div style="background:#fff;border:2px solid #e8f5e9;border-radius:20px;padding:36px 28px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
          <div style="font-size:3rem;">&#127873;</div>
          <span style="background:#22c55e;color:#fff;font-size:0.75rem;font-weight:700;padding:4px 12px;border-radius:50px;">LIVE</span>
        </div>
        <h3 style="color:#1a1a2e;font-size:1.2rem;margin-bottom:8px;">Long Island Gift Basket</h3>
        <p style="color:#666;font-size:0.9rem;margin-bottom:16px;">Custom hand-packed gift baskets for every occasion. Same-day pickup available.</p>
        <div style="color:#2d6a4f;font-weight:700;font-size:0.9rem;">ligiftbasket.com &#8594;</div>
      </div>
    </a>

    <a href="https://www.longislandballoonsdecor.com" target="_blank" style="text-decoration:none;">
      <div style="background:#fff;border:2px solid #fce4ec;border-radius:20px;padding:36px 28px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
          <div style="font-size:3rem;">&#127881;</div>
          <span style="background:#22c55e;color:#fff;font-size:0.75rem;font-weight:700;padding:4px 12px;border-radius:50px;">LIVE</span>
        </div>
        <h3 style="color:#1a1a2e;font-size:1.2rem;margin-bottom:8px;">Long Island Balloons &amp; Decor</h3>
        <p style="color:#666;font-size:0.9rem;margin-bottom:16px;">Custom balloon arches, garlands, gender reveals, weddings and corporate events.</p>
        <div style="color:#c77dff;font-weight:700;font-size:0.9rem;">longislandballoonsdecor.com &#8594;</div>
      </div>
    </a>

    <a href="https://www.longislandprintandmail.com" target="_blank" style="text-decoration:none;">
      <div style="background:#fff;border:2px solid #e3f2fd;border-radius:20px;padding:36px 28px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
          <div style="font-size:3rem;">&#128247;</div>
          <span style="background:#22c55e;color:#fff;font-size:0.75rem;font-weight:700;padding:4px 12px;border-radius:50px;">LIVE</span>
        </div>
        <h3 style="color:#1a1a2e;font-size:1.2rem;margin-bottom:8px;">Long Island Print &amp; Mail</h3>
        <p style="color:#666;font-size:0.9rem;margin-bottom:16px;">Same-day business cards, flyers, banners, signs and USPS/UPS/FedEx mailing.</p>
        <div style="color:#3d405b;font-weight:700;font-size:0.9rem;">longislandprintandmail.com &#8594;</div>
      </div>
    </a>

    <a href="https://www.jhdadvisor.com" target="_blank" style="text-decoration:none;">
      <div style="background:#fff;border:2px solid #ede7f6;border-radius:20px;padding:36px 28px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
          <div style="font-size:3rem;">&#128640;</div>
          <span style="background:#22c55e;color:#fff;font-size:0.75rem;font-weight:700;padding:4px 12px;border-radius:50px;">LIVE</span>
        </div>
        <h3 style="color:#1a1a2e;font-size:1.2rem;margin-bottom:8px;">JHD Advisor</h3>
        <p style="color:#666;font-size:0.9rem;margin-bottom:16px;">Digital agency — e-commerce, AI automation, SEO and startup-to-unicorn growth consulting.</p>
        <div style="color:#8a2be2;font-weight:700;font-size:0.9rem;">jhdadvisor.com &#8594;</div>
      </div>
    </a>

    <div style="opacity:0.55;cursor:not-allowed;">
      <div style="background:#fafafa;border:2px dashed #ddd;border-radius:20px;padding:36px 28px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
          <div style="font-size:3rem;">&#128684;</div>
          <span style="background:#f59e0b;color:#fff;font-size:0.75rem;font-weight:700;padding:4px 12px;border-radius:50px;">COMING SOON</span>
        </div>
        <h3 style="color:#999;font-size:1.2rem;margin-bottom:8px;">Long Island Cigars</h3>
        <p style="color:#aaa;font-size:0.9rem;margin-bottom:16px;">Premium cigars and accessories for connoisseurs. Online store launching soon.</p>
        <div style="color:#bbb;font-weight:700;font-size:0.9rem;">Opening Soon</div>
      </div>
    </div>

    <div style="opacity:0.55;cursor:not-allowed;">
      <div style="background:#fafafa;border:2px dashed #ddd;border-radius:20px;padding:36px 28px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
          <div style="font-size:3rem;">&#127922;</div>
          <span style="background:#f59e0b;color:#fff;font-size:0.75rem;font-weight:700;padding:4px 12px;border-radius:50px;">COMING SOON</span>
        </div>
        <h3 style="color:#999;font-size:1.2rem;margin-bottom:8px;">Long Island Lotto</h3>
        <p style="color:#aaa;font-size:0.9rem;margin-bottom:16px;">Lottery tickets, scratch cards and gaming products. Store launching soon.</p>
        <div style="color:#bbb;font-weight:700;font-size:0.9rem;">Opening Soon</div>
      </div>
    </div>

  </div>
</section>

<section style="background:#f8f9fa;padding:40px 20px;text-align:center;">
  <p style="color:#666;margin-bottom:4px;">605 Old Country Road, Plainview NY 11803</p>
  <p style="color:#666;">Phone: <a href="tel:+12125648585" style="color:#e63946;">(212) 564-8585</a> &bull; Open 7 Days a Week</p>
</section>

</div></t></t>'''

# Get page and view IDs
stores = xc('website.page','search_read',[[['website_id','=',1],['url','=','/stores']]],{'fields':['id','view_id']})[0]
xc('ir.ui.view', 'write', [[stores['view_id'][0]], {'arch_db': arch}])
xc('website.page', 'write', [[stores['id']], {
    'website_meta_title': 'Our Brands | Long Island Convenience | Plainview NY',
    'website_meta_description': '7 brands at Long Island Convenience in Plainview NY: Trading Cards, Gift Baskets, Balloons, Print & Mail, JHD Advisor — plus Cigars and Lotto coming soon.'
}])
print('Stores page updated — all 7 brands, cigars + lotto = COMING SOON')
