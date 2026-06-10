import xmlrpc.client, urllib.request, base64

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

# ── Logo download URLs from Canva export ──────────────────────────────────
LOGOS = {
    1:  'https://export-download.canva.com/L2SqA/DAHKf4L2SqA/-1/0/0001-7909950970396435842.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260523%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260523T141940Z&X-Amz-Expires=10529&X-Amz-Signature=803532fc20e94fa719c68797f610000f26c5b3e7fbaaa2ff769eba8cbb6dadb0&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2023%20May%202026%2017%3A15%3A09%20GMT',
    36: 'https://export-download.canva.com/Lua5g/DAHKf9Lua5g/-1/0/0001-4916183118566314258.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260523%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260523T031228Z&X-Amz-Expires=49927&X-Amz-Signature=46ddb9ffd54acf988bbdb60531e7808c2a4e8b71009f06b5c09599230462b947&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2023%20May%202026%2017%3A04%3A35%20GMT',
    37: 'https://export-download.canva.com/70KhA/DAHKf770KhA/-1/0/0001-8672185204617540082.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260522%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260522T152526Z&X-Amz-Expires=92256&X-Amz-Signature=f2fb5fc70383fba763f814f4559f776b5c345067152bf9dc60681b3825667581&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2023%20May%202026%2017%3A03%3A02%20GMT',
    38: 'https://export-download.canva.com/OuLFs/DAHKf7OuLFs/-1/0/0001-2870422986418456450.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260522%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260522T231629Z&X-Amz-Expires=62586&X-Amz-Signature=094dad730f46f9c60634a77d5a0d2834bb06cb43d4641ddb3c8b681b87ddefe7&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2023%20May%202026%2016%3A39%3A35%20GMT',
    39: 'https://export-download.canva.com/imZaY/DAHKf-imZaY/-1/0/0001-4263161171554307119.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260523%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260523T005233Z&X-Amz-Expires=57636&X-Amz-Signature=937368de0373f001936f03b1d1f2fa94942c068841b99e4fa47da897824aad56&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2023%20May%202026%2016%3A53%3A09%20GMT',
    41: 'https://export-download.canva.com/6-JB8/DAHKfy6-JB8/-1/0/0001-2528149414962394264.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260523%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260523T094615Z&X-Amz-Expires=25195&X-Amz-Signature=f2a8bbcd6a8b62f437e32c64823def009c5af2bfe495d99224d6d81e317d9b18&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2023%20May%202026%2016%3A46%3A10%20GMT',
}

NAMES = {1:'Long Island Convenience',36:'Long Island Cards',37:'Long Island Gift Basket',
         38:'Long Island Balloons',39:'Long Island Print & Mail',41:'JHD Advisor'}

# ── 1. Download and upload logos ──────────────────────────────────────────
print('=== Uploading Logos to Odoo ===')
req = urllib.request.Request
for wid, logo_url in LOGOS.items():
    try:
        r = urllib.request.urlopen(req(logo_url, headers={'User-Agent':'Mozilla/5.0'}), timeout=30)
        img_data = base64.b64encode(r.read()).decode('utf-8')
        xc('website', 'write', [[wid], {'logo': img_data}])
        print(f'  Uploaded logo -> {NAMES[wid]} (WID={wid})')
    except Exception as e:
        print(f'  FAILED {NAMES[wid]}: {e}')

# ── 2. Fix JHD Advisor footer ─────────────────────────────────────────────
print('\n=== Fixing JHD Advisor Footer ===')

JHD_FOOTER = '''<t t-name="website.footer_custom" t-inherit="website.footer_custom" t-inherit-mode="primary">
  <div class="o_footer_copyright_name">JHD Advisor LLC</div>
</t>'''

# Create a website-specific footer_custom override for WID=41
# First check if one already exists
existing = xc('ir.ui.view','search_read',
    [[['key','=','website.footer_custom'],['website_id','=',41]]],
    {'fields':['id']})

jhd_footer_arch = '''<t t-name="website.footer_custom">
  <footer style="background:#050505;color:#fff;padding:56px 20px 24px;">
    <div style="max-width:1100px;margin:0 auto;">
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:48px;margin-bottom:48px;">

        <div>
          <div style="font-size:1.4rem;font-weight:900;margin-bottom:12px;background:linear-gradient(135deg,#fff,#c77dff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">JHD Advisor LLC</div>
          <p style="color:#888;font-size:0.9rem;line-height:1.7;margin-bottom:16px;">Long Island&#39;s AI-first digital agency. E-commerce development, AI automation, SEO/GEO, and startup-to-unicorn consulting.</p>
          <p style="color:#666;font-size:0.85rem;margin-bottom:4px;">&#128205; 405 RXR Plaza, Uniondale, NY 11556</p>
          <p style="color:#666;font-size:0.85rem;"><a href="mailto:countrycoveinc@gmail.com" style="color:#8a2be2;text-decoration:none;">countrycoveinc@gmail.com</a></p>
        </div>

        <div>
          <div style="font-size:0.75rem;font-weight:700;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:20px;">Services</div>
          <ul style="list-style:none;padding:0;margin:0;">
            <li style="margin-bottom:10px;"><a href="/services" style="color:#999;text-decoration:none;font-size:0.9rem;">E-Commerce Dev</a></li>
            <li style="margin-bottom:10px;"><a href="/services" style="color:#999;text-decoration:none;font-size:0.9rem;">AI &amp; Automation</a></li>
            <li style="margin-bottom:10px;"><a href="/services" style="color:#999;text-decoration:none;font-size:0.9rem;">SEO / GEO</a></li>
            <li style="margin-bottom:10px;"><a href="/services" style="color:#999;text-decoration:none;font-size:0.9rem;">Website Design</a></li>
            <li style="margin-bottom:10px;"><a href="/services" style="color:#999;text-decoration:none;font-size:0.9rem;">Startup Consulting</a></li>
          </ul>
        </div>

        <div>
          <div style="font-size:0.75rem;font-weight:700;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:20px;">Company</div>
          <ul style="list-style:none;padding:0;margin:0;">
            <li style="margin-bottom:10px;"><a href="/" style="color:#999;text-decoration:none;font-size:0.9rem;">Home</a></li>
            <li style="margin-bottom:10px;"><a href="/about" style="color:#999;text-decoration:none;font-size:0.9rem;">About</a></li>
            <li style="margin-bottom:10px;"><a href="/contact" style="color:#999;text-decoration:none;font-size:0.9rem;">Contact</a></li>
            <li style="margin-bottom:10px;"><a href="/blog" style="color:#999;text-decoration:none;font-size:0.9rem;">Blog</a></li>
          </ul>
        </div>

      </div>

      <div style="border-top:1px solid #1a1a1a;padding-top:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
        <p style="color:#444;font-size:0.8rem;margin:0;">&#169; 2026 JHD Advisor LLC. All rights reserved. USA Registered Company.</p>
        <div style="display:flex;gap:16px;">
          <a href="/contact" style="background:linear-gradient(135deg,#8a2be2,#4361ee);color:#fff;padding:10px 24px;border-radius:50px;font-size:0.85rem;font-weight:700;text-decoration:none;">Free Audit &#8594;</a>
        </div>
      </div>
    </div>
  </footer>
</t>'''

if existing:
    xc('ir.ui.view','write',[[existing[0]['id']],{'arch_db':jhd_footer_arch}])
    print('  Footer updated (existing override)')
else:
    # Create website-specific footer override
    vid = xc('ir.ui.view','create',[{
        'name': 'JHD Advisor Footer',
        'key': 'website.footer_custom',
        'type': 'qweb',
        'website_id': 41,
        'arch_db': jhd_footer_arch,
        'active': True,
    }])
    print(f'  Footer created (new view ID={vid})')

# ── 3. Fix JHD copyright line ─────────────────────────────────────────────
existing_copy = xc('ir.ui.view','search_read',
    [[['key','=','website.footer_copyright_company_name'],['website_id','=',41]]],
    {'fields':['id']})
copy_arch = '<t t-name="website.footer_copyright_company_name">JHD Advisor LLC</t>'
if existing_copy:
    xc('ir.ui.view','write',[[existing_copy[0]['id']],{'arch_db':copy_arch}])
else:
    xc('ir.ui.view','create',[{
        'name':'JHD Advisor Copyright',
        'key':'website.footer_copyright_company_name',
        'type':'qweb','website_id':41,'arch_db':copy_arch,'active':True
    }])
print('  Copyright updated -> JHD Advisor LLC')

# ── 4. Update JHD meta with research findings ─────────────────────────────
print('\n=== Updating JHD Advisor SEO & Content ===')

hp = xc('website.page','search_read',[[['website_id','=',41],['url','=','/']]],{'fields':['id','view_id']})[0]
xc('website.page','write',[[hp['id']],{
    'website_meta_title': "JHD Advisor | AI Agency & Digital Marketing | Long Island NY",
    'website_meta_description': "JHD Advisor LLC — AI automation, e-commerce development, SEO/GEO, n8n workflows and startup consulting for Long Island NY businesses. Get a free audit today.",
    'website_meta_keywords': "AI automation agency Long Island NY, digital marketing agency Nassau County, n8n automation consultant, GEO optimization agency, e-commerce development Long Island, startup consulting NY, AI agency New York"
}])
print('  JHD homepage meta updated with research keywords')

# Update website name
xc('website','write',[[41],{'name':'JHD Advisor'}])

# Update other JHD pages meta
pages_meta = [
    ('/services', 'JHD Advisor Services | AI Automation, E-Commerce, SEO/GEO | Long Island NY',
     'AI automation, e-commerce development, SEO/GEO, n8n workflows, website design and startup consulting. Long Island AI agency serving businesses nationwide.'),
    ('/about', 'About JHD Advisor | AI-First Digital Agency | Long Island NY USA',
     'About JHD Advisor LLC — Long Island\'s AI-first digital agency. E-commerce, n8n automation, GEO optimization and startup-to-unicorn consulting. USA registered company.'),
    ('/contact', 'Get a Free Audit | JHD Advisor | AI Agency Long Island NY',
     'Book a free 30-minute strategy call or AI audit with JHD Advisor LLC. Long Island NY digital agency specializing in AI automation, SEO/GEO and e-commerce.'),
]
for url, title, desc in pages_meta:
    page = xc('website.page','search_read',[[['website_id','=',41],['url','=',url]]],{'fields':['id']})
    if page:
        xc('website.page','write',[[page[0]['id']],{
            'website_meta_title':title,'website_meta_description':desc
        }])
        print(f'  Updated meta: {url}')

print('\n=== ALL DONE ===')
print('Logos uploaded to all 6 websites')
print('JHD Advisor footer fixed — no more Long Island Convenience branding')
print('JHD meta keywords updated based on competitor research')
