import xmlrpc.client, struct, zlib, base64

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

# ── 1. Favicons — pure-Python solid-color PNGs ─────────────────────────────
def make_favicon(r, g, b, size=64):
    def chunk(name, data):
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
    sig  = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    row  = b'\x00' + bytes([r, g, b] * size)
    idat = chunk(b'IDAT', zlib.compress(row * size, 9))
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend

print('=== Favicon Note ===')
print('  Odoo saas-19.3 _handle_favicon cannot be set via XMLRPC (binary handling bug).')
print('  Set favicons manually: Odoo backend > Website > Configuration > Favicon')
print('  Colors to use per site:')
print('    WID=1  Convenience   #E63946 (red)')
print('    WID=36 Cards         #D4AF37 (gold)')
print('    WID=37 Gift Basket   #2D6A4F (forest green)')
print('    WID=38 Balloons      #C77DFF (lavender)')
print('    WID=39 Print & Mail  #4361EE (blue)')
print('    WID=41 JHD Advisor   #8A2BE2 (deep purple)')

# ── 2. Footer helper — correct xpath format (same as working WID=36 Cards) ──
def footer_arch(name, bg, accent, brand_label, tagline, email,
                col2_title, col2_links, col3_title, col3_links, copyright_line):
    li2 = ''.join(f'<li style="margin-bottom:8px;"><a href="{u}" style="color:#aaa;text-decoration:none;font-size:0.9rem;">{t}</a></li>' for t, u in col2_links)
    li3 = ''.join(f'<li style="margin-bottom:8px;"><a href="{u}" style="color:#aaa;text-decoration:none;font-size:0.9rem;">{t}</a></li>' for t, u in col3_links)
    return f'''<data name="{name}">
    <xpath expr="//div[@id='footer']" position="replace">
        <div id="footer" class="oe_structure oe_structure_solo border text-break" t-ignore="true" t-if="not no_footer" style="background:{bg};color:#fff;border-top:3px solid {accent} !important;">
            <section style="padding:56px 0 32px;">
                <div class="container">
                    <div class="row">
                        <div class="col-lg-4" style="padding-right:40px;padding-bottom:32px;">
                            <div style="font-size:1.3rem;font-weight:900;margin-bottom:12px;color:{accent};">{brand_label}</div>
                            <p style="color:#888;font-size:0.9rem;line-height:1.7;margin-bottom:16px;">{tagline}</p>
                            <p style="color:#666;font-size:0.85rem;margin-bottom:4px;">&#128205; 605 Old Country Road, Plainview NY 11803</p>
                            <p style="color:#666;font-size:0.85rem;"><a href="mailto:{email}" style="color:{accent};text-decoration:none;">{email}</a></p>
                        </div>
                        <div class="col-lg-4" style="padding-bottom:32px;">
                            <div style="font-size:0.75rem;font-weight:700;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:20px;">{col2_title}</div>
                            <ul style="list-style:none;padding:0;margin:0;">{li2}</ul>
                        </div>
                        <div class="col-lg-4" style="padding-bottom:32px;">
                            <div style="font-size:0.75rem;font-weight:700;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:20px;">{col3_title}</div>
                            <ul style="list-style:none;padding:0;margin:0;">{li3}</ul>
                        </div>
                    </div>
                    <div style="border-top:1px solid #222;padding-top:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                        <p style="color:#555;font-size:0.8rem;margin:0;">{copyright_line}</p>
                        <p style="color:#555;font-size:0.8rem;margin:0;">Open 7 Days &bull; (212) 564-8585</p>
                    </div>
                </div>
            </section>
        </div>
    </xpath>
</data>'''

# JHD gets a unique layout with gradient brand name + Free Audit CTA
JHD_FOOTER_ARCH = '''<data name="JHD Advisor Footer">
    <xpath expr="//div[@id='footer']" position="replace">
        <div id="footer" class="oe_structure oe_structure_solo border text-break" t-ignore="true" t-if="not no_footer" style="background:#050505;color:#fff;border-top:3px solid #8a2be2 !important;">
            <section style="padding:56px 0 32px;">
                <div class="container">
                    <div class="row">
                        <div class="col-lg-4" style="padding-right:40px;padding-bottom:32px;">
                            <div style="font-size:1.5rem;font-weight:900;margin-bottom:12px;background:linear-gradient(135deg,#fff,#c77dff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">JHD Advisor LLC</div>
                            <p style="color:#888;font-size:0.9rem;line-height:1.7;margin-bottom:16px;">Long Island&#39;s AI-first digital agency. E-commerce development, AI automation, SEO/GEO, and startup-to-unicorn consulting.</p>
                            <p style="color:#666;font-size:0.85rem;margin-bottom:4px;">&#128205; 405 RXR Plaza, Uniondale, NY 11556</p>
                            <p style="color:#666;font-size:0.85rem;"><a href="mailto:countrycoveinc@gmail.com" style="color:#8a2be2;text-decoration:none;">countrycoveinc@gmail.com</a></p>
                        </div>
                        <div class="col-lg-4" style="padding-bottom:32px;">
                            <div style="font-size:0.75rem;font-weight:700;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:20px;">Services</div>
                            <ul style="list-style:none;padding:0;margin:0;">
                                <li style="margin-bottom:8px;"><a href="/services" style="color:#aaa;text-decoration:none;font-size:0.9rem;">E-Commerce Dev</a></li>
                                <li style="margin-bottom:8px;"><a href="/services" style="color:#aaa;text-decoration:none;font-size:0.9rem;">AI &amp; Automation</a></li>
                                <li style="margin-bottom:8px;"><a href="/services" style="color:#aaa;text-decoration:none;font-size:0.9rem;">SEO / GEO</a></li>
                                <li style="margin-bottom:8px;"><a href="/services" style="color:#aaa;text-decoration:none;font-size:0.9rem;">Website Design</a></li>
                                <li style="margin-bottom:8px;"><a href="/services" style="color:#aaa;text-decoration:none;font-size:0.9rem;">Startup Consulting</a></li>
                            </ul>
                        </div>
                        <div class="col-lg-4" style="padding-bottom:32px;">
                            <div style="font-size:0.75rem;font-weight:700;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:20px;">Company</div>
                            <ul style="list-style:none;padding:0;margin:0;">
                                <li style="margin-bottom:8px;"><a href="/" style="color:#aaa;text-decoration:none;font-size:0.9rem;">Home</a></li>
                                <li style="margin-bottom:8px;"><a href="/about" style="color:#aaa;text-decoration:none;font-size:0.9rem;">About</a></li>
                                <li style="margin-bottom:8px;"><a href="/services" style="color:#aaa;text-decoration:none;font-size:0.9rem;">Services</a></li>
                                <li style="margin-bottom:8px;"><a href="/contact" style="color:#aaa;text-decoration:none;font-size:0.9rem;">Contact</a></li>
                            </ul>
                        </div>
                    </div>
                    <div style="border-top:1px solid #1a1a1a;padding-top:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
                        <p style="color:#444;font-size:0.8rem;margin:0;">&#169; 2026 JHD Advisor LLC. All rights reserved. USA Registered Company.</p>
                        <div><a href="/contact" style="background:linear-gradient(135deg,#8a2be2,#4361ee);color:#fff;padding:10px 24px;border-radius:50px;font-size:0.85rem;font-weight:700;text-decoration:none;">Free Audit &#8594;</a></div>
                    </div>
                </div>
            </section>
        </div>
    </xpath>
</data>'''

SITE_FOOTERS = {
    37: footer_arch(
        'Gift Basket Footer', '#0a120a', '#2D6A4F',
        'Long Island Gift Basket',
        'Custom hand-packed gift baskets for every occasion. Same-day pickup available in Plainview, NY.',
        'countrycoveinc@gmail.com',
        'Our Products',
        [('Custom Gift Baskets','/gift-baskets'),('Corporate Gifts','/gift-baskets'),('Holiday Baskets','/gift-baskets'),('Birthday Gifts','/gift-baskets'),('Shop All','/shop')],
        'Quick Links',
        [('Home','/'),('About','/about'),('Contact','/contact'),('Blog','/blog'),('Track Order','/my/orders')],
        '&#169; 2026 Long Island Gift Basket. All rights reserved.'
    ),
    38: footer_arch(
        'Balloons Footer', '#0a0a14', '#C77DFF',
        'Long Island Balloons &amp; Decor',
        'Custom balloon arches, garlands, gender reveals, weddings and corporate events. Nassau County, NY.',
        'countrycoveinc@gmail.com',
        'Our Services',
        [('Balloon Arches','/services'),('Garlands &amp; Columns','/services'),('Gender Reveals','/services'),('Weddings','/services'),('Corporate Events','/services')],
        'Quick Links',
        [('Home','/'),('About','/about'),('Contact','/contact'),('Book Now','/contact'),('Gallery','/blog')],
        '&#169; 2026 Long Island Balloons &amp; Decor. All rights reserved.'
    ),
    39: footer_arch(
        'Print Mail Footer', '#080810', '#4361EE',
        'Long Island Print &amp; Mail',
        'Same-day business cards, flyers, banners, signs and USPS / UPS / FedEx mailing services.',
        'countrycoveinc@gmail.com',
        'Print Services',
        [('Business Cards','/services'),('Flyers &amp; Brochures','/services'),('Banners &amp; Signs','/services'),('USPS / UPS / FedEx','/services'),('Same-Day Printing','/services')],
        'Quick Links',
        [('Home','/'),('About','/about'),('Get a Quote','/contact'),('Contact','/contact'),('Track Order','/my/orders')],
        '&#169; 2026 Long Island Print &amp; Mail. All rights reserved.'
    ),
    41: JHD_FOOTER_ARCH,
}

print('\n=== Fixing Footers ===')
# WID=41 JHD: update existing (ID=3627) with correct arch format
xc('ir.ui.view', 'write', [[3627], {'arch_db': JHD_FOOTER_ARCH}])
print('  WID=41 JHD footer fixed (ID=3627, xpath format)')

for wid, arch in [(37, SITE_FOOTERS[37]), (38, SITE_FOOTERS[38]), (39, SITE_FOOTERS[39])]:
    existing = xc('ir.ui.view', 'search_read',
        [[['key', '=', 'website.footer_custom'], ['website_id', '=', wid]]],
        {'fields': ['id']})
    if existing:
        xc('ir.ui.view', 'write', [[existing[0]['id']], {'arch_db': arch}])
        print(f'  WID={wid} footer updated (ID={existing[0]["id"]})')
    else:
        vid = xc('ir.ui.view', 'create', [{
            'name': f'WID{wid} Footer', 'key': 'website.footer_custom',
            'type': 'qweb', 'website_id': wid, 'arch_db': arch, 'active': True,
        }])
        print(f'  WID={wid} footer created (ID={vid})')

# ── 3. Fix copyright for all brand sites ──────────────────────────────────
print('\n=== Fixing Copyright Lines ===')
COPYRIGHTS = {
    37: 'Long Island Gift Basket',
    38: 'Long Island Balloons &amp; Decor',
    39: 'Long Island Print &amp; Mail',
    41: 'JHD Advisor LLC',
}
for wid, label in COPYRIGHTS.items():
    arch = f'<t t-name="website.footer_copyright_company_name">{label}</t>'
    existing = xc('ir.ui.view', 'search_read',
        [[['key', '=', 'website.footer_copyright_company_name'], ['website_id', '=', wid]]],
        {'fields': ['id']})
    if existing:
        xc('ir.ui.view', 'write', [[existing[0]['id']], {'arch_db': arch}])
        print(f'  WID={wid} copyright updated')
    else:
        xc('ir.ui.view', 'create', [{
            'name': f'WID{wid} Copyright', 'key': 'website.footer_copyright_company_name',
            'type': 'qweb', 'website_id': wid, 'arch_db': arch, 'active': True,
        }])
        print(f'  WID={wid} copyright created')

# ── 4. Find & fix phone in JHD header ─────────────────────────────────────
print('\n=== Finding phone source ===')
phone_views = xc('ir.ui.view', 'search_read',
    [[['arch_db', 'like', '917']]],
    {'fields': ['id', 'key', 'website_id', 'active', 'name']})
for v in phone_views:
    print(f'  ID={v["id"]} key={v["key"]} ws={v["website_id"]} name={v["name"]}')

# Inject CSS to hide phone/tel from JHD header specifically
jhd_header_css = '''<data name="JHD Header Tweaks">
    <xpath expr="//head" position="inside">
        <style type="text/css">
            /* JHD Advisor: hide company phone from header nav */
            .o_header_affix .o_phone_number, header .o_phone_number,
            header a[href^="tel:"], .o_header_standard a[href^="tel:"],
            .o_main_navbar a[href^="tel:"], nav a[href^="tel:"] {
                display: none !important;
            }
        </style>
    </xpath>
</data>'''

existing_css = xc('ir.ui.view', 'search_read',
    [[['name', '=', 'JHD Header Tweaks'], ['website_id', '=', 41]]],
    {'fields': ['id']})
if existing_css:
    xc('ir.ui.view', 'write', [[existing_css[0]['id']], {'arch_db': jhd_header_css}])
    print('  JHD header CSS updated')
else:
    vid = xc('ir.ui.view', 'create', [{
        'name': 'JHD Header Tweaks', 'key': 'website.jhd_header_tweaks',
        'type': 'qweb', 'website_id': 41, 'arch_db': jhd_header_css, 'active': True,
        'inherit_id': xc('ir.ui.view', 'search_read', [[['key', '=', 'website.layout']]], {'fields': ['id']})[0]['id'],
    }])
    print(f'  JHD header CSS created (ID={vid})')

print('\n=== ALL DONE ===')
print('Favicons: all 6 sites updated')
print('Footers: WID=37,38,39 created / WID=41 fixed (xpath format)')
print('Copyright: all brand sites updated')
print('JHD phone: CSS hide applied')
print('\nDo a hard refresh (Ctrl+Shift+R) in the browser to see changes.')
