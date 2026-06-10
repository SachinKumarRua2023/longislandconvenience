#!/usr/bin/env python3
"""
Fix header for Long Island Cards (website 36).
- Delete broken view 3507
- Create new view with unique key (not website.layout)
- Use correct QWeb variable: user (not env.user)
- Proper xpath: //header[@id='top']
"""
import xmlrpc.client, sys

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"
SITE_ID = 36

def connect():
    uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
    if not uid: sys.exit("Auth failed")
    m = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    print("Connected UID", uid)
    return m, uid

def xc(m, uid, model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

# ─────────────────────────────────────────────────
#  HEADER ARCH — unique key, correct QWeb variables
# ─────────────────────────────────────────────────
HEADER_ARCH = '''<data>
<xpath expr="//header[@id='top']" position="replace">

<header id="top" data-anchor="true" t-attf-class="o_cc o_cc1 #{('o_header_sidebar' if is_vertical_nav else '')}" style="position:sticky;top:0;z-index:1000;">

  <!-- STYLE BLOCK -->
  <style>
    #lic-header { background:#0a0a0a; border-bottom:1px solid rgba(212,175,55,0.18); box-shadow:0 2px 24px rgba(0,0,0,0.55); }
    #lic-announce { background:#D4AF37; padding:6px 0; text-align:center; }
    #lic-announce span { font-size:11px; font-weight:700; color:#000; letter-spacing:1.2px; }
    #lic-nav-inner { max-width:1280px; margin:0 auto; padding:0 28px; display:flex; align-items:center; justify-content:space-between; height:66px; }
    #lic-logo a { text-decoration:none; display:flex; align-items:center; gap:10px; }
    #lic-logo .badge { width:38px; height:38px; background:#D4AF37; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:17px; font-weight:900; color:#000; flex-shrink:0; }
    #lic-logo .name-top { color:#fff; font-size:15px; font-weight:900; letter-spacing:-0.4px; line-height:1.1; }
    #lic-logo .name-bot { color:#D4AF37; font-size:9px; font-weight:700; letter-spacing:3.5px; text-transform:uppercase; }
    .lic-nav-link { color:rgba(255,255,255,0.72); font-size:13.5px; font-weight:600; padding:7px 13px; border-radius:6px; text-decoration:none; transition:color .15s; }
    .lic-nav-link:hover { color:#D4AF37; }
    .lic-icon-btn { color:rgba(255,255,255,0.6); padding:8px; border-radius:6px; text-decoration:none; display:flex; align-items:center; background:transparent; border:none; cursor:pointer; }
    .lic-icon-btn:hover { color:#D4AF37; background:rgba(212,175,55,0.08); }
    /* Dropdown */
    .lic-dd { position:relative; }
    .lic-dd-btn { display:flex; align-items:center; gap:6px; font-size:13px; font-weight:700; padding:8px 14px; border-radius:6px; cursor:pointer; border:1px solid transparent; }
    .lic-dd-menu { display:none; position:absolute; right:0; top:calc(100% + 10px); border-radius:12px; min-width:210px; padding:8px; box-shadow:0 16px 48px rgba(0,0,0,0.7); z-index:9999; }
    .lic-dd:hover .lic-dd-menu, .lic-dd-btn:focus + .lic-dd-menu { display:block; }
    .lic-dd-menu a { display:flex; align-items:center; gap:10px; padding:9px 12px; font-size:13px; text-decoration:none; border-radius:6px; }
    .lic-dd-menu a:hover { background:rgba(255,255,255,0.05); }
    .lic-dd-sep { border-top:1px solid rgba(255,255,255,0.07); margin:6px 0; padding-top:6px; }
    .lic-dd-label { font-size:10px; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; padding:8px 12px 6px; }
    .lic-dd-user { font-size:12px; padding:2px 12px 10px; color:rgba(255,255,255,0.4); border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:6px; }
    /* Role: customer */
    .lic-btn-customer { background:rgba(212,175,55,0.1); color:#D4AF37; border-color:rgba(212,175,55,0.28); }
    .lic-menu-customer { background:#141408; border:1px solid rgba(212,175,55,0.18); }
    .lic-menu-customer a { color:rgba(255,255,255,0.72); }
    .lic-menu-customer .lic-dd-label { color:#D4AF37; }
    /* Role: seller */
    .lic-btn-seller { background:rgba(34,197,94,0.08); color:#22c55e; border-color:rgba(34,197,94,0.22); }
    .lic-menu-seller { background:#0b150d; border:1px solid rgba(34,197,94,0.18); }
    .lic-menu-seller a { color:rgba(255,255,255,0.72); }
    .lic-menu-seller .lic-dd-label { color:#22c55e; }
    /* Role: admin */
    .lic-btn-admin { background:rgba(99,102,241,0.1); color:#818cf8; border-color:rgba(99,102,241,0.25); }
    .lic-menu-admin { background:#0c0c18; border:1px solid rgba(99,102,241,0.2); }
    .lic-menu-admin a { color:rgba(255,255,255,0.72); }
    .lic-menu-admin .lic-dd-label { color:#818cf8; }
    /* auth btns */
    .lic-btn-login  { color:rgba(255,255,255,0.7); font-size:13px; font-weight:600; padding:8px 16px; border-radius:6px; text-decoration:none; border:1px solid rgba(255,255,255,0.14); }
    .lic-btn-signup { background:#D4AF37; color:#000; font-size:13px; font-weight:800; padding:8px 18px; border-radius:6px; text-decoration:none; }
    /* Mobile */
    #lic-mobile-toggle { display:none; background:transparent; border:1px solid rgba(255,255,255,0.15); border-radius:6px; padding:8px 10px; cursor:pointer; flex-direction:column; gap:4px; align-items:center; justify-content:center; }
    #lic-mobile-toggle span { display:block; width:20px; height:2px; background:rgba(255,255,255,0.7); border-radius:1px; }
    #lic-mobile-menu { display:none; background:#111; border-top:1px solid rgba(212,175,55,0.12); padding:0 24px 24px; }
    .lic-mob-link { display:block; padding:12px 0; font-size:14px; text-decoration:none; border-bottom:1px solid rgba(255,255,255,0.05); }
    @media (max-width:991px) {
      #lic-desktop-nav { display:none !important; }
      #lic-desktop-right { display:none !important; }
      #lic-mobile-toggle { display:flex !important; }
    }
    @media (min-width:992px) {
      #lic-mobile-toggle { display:none !important; }
      #lic-mobile-menu  { display:none !important; }
    }
  </style>

  <div id="lic-header">
    <!-- Announcement bar -->
    <div id="lic-announce">
      <span>Free shipping on orders over $75 &#8226; Same-day dispatch before 3 PM &#8226; Open 7 days &#8226; Plainview, NY</span>
    </div>

    <!-- Main nav row -->
    <div id="lic-nav-inner">

      <!-- LOGO -->
      <div id="lic-logo">
        <a href="/">
          <div class="badge">LI</div>
          <div>
            <div class="name-top">Long Island</div>
            <div class="name-bot">Cards</div>
          </div>
        </a>
      </div>

      <!-- DESKTOP LINKS -->
      <nav id="lic-desktop-nav" style="display:flex;align-items:center;gap:2px;">
        <a class="lic-nav-link" href="/shop">Shop</a>
        <a class="lic-nav-link" href="/shop?category=sports-cards">Sports</a>
        <a class="lic-nav-link" href="/shop?category=pokemon">Pokemon</a>
        <a class="lic-nav-link" href="/shop?category=magic-the-gathering">MTG</a>
        <a class="lic-nav-link" href="/shop?category=yu-gi-oh">Yu-Gi-Oh!</a>
        <a class="lic-nav-link" href="/shop?category=graded-cards">Graded</a>
        <a class="lic-nav-link" href="/contact">Contact</a>
      </nav>

      <!-- DESKTOP RIGHT ACTIONS -->
      <div id="lic-desktop-right" style="display:flex;align-items:center;gap:6px;">

        <!-- Search -->
        <a class="lic-icon-btn" href="/shop" title="Search">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        </a>

        <!-- ══ GUEST ══ -->
        <t t-if="user._is_public()">
          <a class="lic-btn-login" href="/web/login">Log In</a>
          <a class="lic-btn-signup" href="/web/signup">Sign Up</a>
        </t>

        <!-- ══ PORTAL CUSTOMER ══ -->
        <t t-if="not user._is_public() and user.share">
          <!-- Cart -->
          <a class="lic-icon-btn" href="/shop/cart" title="Cart" style="position:relative;">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
          </a>
          <!-- Account menu -->
          <div class="lic-dd" tabindex="0">
            <div class="lic-dd-btn lic-btn-customer">
              <svg width="13" height="13" fill="currentColor" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              My Account
              <svg width="9" height="9" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6,9 12,15 18,9"/></svg>
            </div>
            <div class="lic-dd-menu lic-menu-customer">
              <div class="lic-dd-label">Customer</div>
              <div class="lic-dd-user" t-out="user.name"/>
              <a href="/my/orders"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> My Orders</a>
              <a href="/my/account"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> My Profile</a>
              <a href="/shop/wishlist"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg> Wishlist</a>
              <a href="/shop/cart"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg> Cart</a>
              <div class="lic-dd-sep"><a href="/web/session/logout?redirect=/" style="color:rgba(220,80,80,0.75) !important;"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg> Log Out</a></div>
            </div>
          </div>
        </t>

        <!-- ══ SELLER (internal, not admin) ══ -->
        <t t-if="not user._is_public() and not user.share and not user.has_group('base.group_erp_manager')">
          <a class="lic-icon-btn" href="/shop/cart" title="Cart">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
          </a>
          <div class="lic-dd" tabindex="0">
            <div class="lic-dd-btn lic-btn-seller">
              <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
              Seller Panel
              <svg width="9" height="9" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6,9 12,15 18,9"/></svg>
            </div>
            <div class="lic-dd-menu lic-menu-seller">
              <div class="lic-dd-label">Seller</div>
              <div class="lic-dd-user" t-out="user.name"/>
              <a href="/odoo/sales"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg> My Sales</a>
              <a href="/odoo/inventory/products"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 7H4a2 2 0 00-2 2v10a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/></svg> My Products</a>
              <a href="/odoo/sales?status=to_invoice"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/></svg> Pending Orders</a>
              <a href="/my/account"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> My Profile</a>
              <div class="lic-dd-sep"><a href="/web/session/logout?redirect=/" style="color:rgba(220,80,80,0.75) !important;"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg> Log Out</a></div>
            </div>
          </div>
        </t>

        <!-- ══ ADMIN ══ -->
        <t t-if="not user._is_public() and not user.share and user.has_group('base.group_erp_manager')">
          <a class="lic-icon-btn" href="/shop/cart" title="Cart">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
          </a>
          <div class="lic-dd" tabindex="0">
            <div class="lic-dd-btn lic-btn-admin">
              <svg width="13" height="13" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
              Admin
              <svg width="9" height="9" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6,9 12,15 18,9"/></svg>
            </div>
            <div class="lic-dd-menu lic-menu-admin">
              <div class="lic-dd-label">Administrator</div>
              <div class="lic-dd-user" t-out="user.name"/>
              <a href="/odoo" style="font-weight:600;"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg> Odoo Backend</a>
              <a href="/odoo/ecommerce/products"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 7H4a2 2 0 00-2 2v10a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/></svg> Products</a>
              <a href="/odoo/ecommerce/orders"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/></svg> Orders</a>
              <a href="/odoo/website"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg> Website Editor</a>
              <a href="/odoo/users"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg> Users</a>
              <a href="/odoo/reporting/sales"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg> Reports</a>
              <div class="lic-dd-sep"><a href="/web/session/logout?redirect=/" style="color:rgba(220,80,80,0.75) !important;"><svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg> Log Out</a></div>
            </div>
          </div>
        </t>

        <!-- Hamburger (tablet/mobile) -->
        <button id="lic-mobile-toggle" onclick="var m=document.getElementById('lic-mobile-menu');m.style.display=m.style.display=='block'?'none':'block';">
          <span/><span/><span/>
        </button>

      </div><!-- /desktop right -->

    </div><!-- /nav inner -->

    <!-- MOBILE MENU -->
    <div id="lic-mobile-menu">
      <a class="lic-mob-link" href="/shop" style="color:rgba(255,255,255,0.8);font-weight:600;">Shop All</a>
      <a class="lic-mob-link" href="/shop?category=sports-cards" style="color:rgba(255,255,255,0.65);">Sports Cards</a>
      <a class="lic-mob-link" href="/shop?category=pokemon" style="color:rgba(255,255,255,0.65);">Pokemon</a>
      <a class="lic-mob-link" href="/shop?category=magic-the-gathering" style="color:rgba(255,255,255,0.65);">MTG</a>
      <a class="lic-mob-link" href="/shop?category=yu-gi-oh" style="color:rgba(255,255,255,0.65);">Yu-Gi-Oh!</a>
      <a class="lic-mob-link" href="/shop?category=graded-cards" style="color:rgba(255,255,255,0.65);">Graded Cards</a>
      <a class="lic-mob-link" href="/contact" style="color:rgba(255,255,255,0.65);">Contact</a>
      <t t-if="user._is_public()">
        <div style="display:flex;gap:12px;margin-top:16px;">
          <a href="/web/login" style="flex:1;text-align:center;color:#fff;font-size:14px;font-weight:600;padding:12px;border-radius:8px;text-decoration:none;border:1px solid rgba(255,255,255,0.18);">Log In</a>
          <a href="/web/signup" style="flex:1;text-align:center;background:#D4AF37;color:#000;font-size:14px;font-weight:800;padding:12px;border-radius:8px;text-decoration:none;">Sign Up</a>
        </div>
      </t>
      <t t-if="not user._is_public()">
        <div style="margin-top:14px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.07);">
          <a href="/my/orders" style="display:block;padding:10px 0;color:rgba(255,255,255,0.65);font-size:14px;text-decoration:none;">My Orders</a>
          <a href="/my/account" style="display:block;padding:10px 0;color:rgba(255,255,255,0.65);font-size:14px;text-decoration:none;">My Profile</a>
          <a href="/shop/cart" style="display:block;padding:10px 0;color:rgba(255,255,255,0.65);font-size:14px;text-decoration:none;">Cart</a>
          <a href="/web/session/logout?redirect=/" style="display:block;padding:10px 0;color:rgba(220,80,80,0.75);font-size:14px;text-decoration:none;">Log Out</a>
        </div>
      </t>
    </div>

  </div><!-- /#lic-header -->

</header>
</xpath>
</data>'''


def main():
    m, uid = connect()

    # Delete broken view 3507
    print("\n[1] Removing broken header view 3507...")
    try:
        xc(m, uid, 'ir.ui.view', 'unlink', [[3507]])
        print("  Deleted view 3507")
    except Exception as e:
        # Try archiving instead
        xc(m, uid, 'ir.ui.view', 'write', [[3507], {'active': False}])
        print("  Archived view 3507 (unlink failed)")

    # Also delete/archive any other website-36 website.layout views
    dupes = xc(m, uid, 'ir.ui.view', 'search_read',
        [[('key','=','website.layout'),('website_id','=',SITE_ID)]],
        {'fields':['id','name']})
    for d in dupes:
        try:
            xc(m, uid, 'ir.ui.view', 'unlink', [[d['id']]])
            print(f"  Deleted dupe [{d['id']}]")
        except:
            xc(m, uid, 'ir.ui.view', 'write', [[d['id']], {'active': False}])
            print(f"  Archived dupe [{d['id']}]")

    # Create new header view with UNIQUE key
    print("\n[2] Creating correct header view...")
    vid = xc(m, uid, 'ir.ui.view', 'create', [{
        'name':       'Long Island Cards — Custom Header',
        'key':        'website.lic_cards_header',   # unique key
        'type':       'qweb',
        'inherit_id': 603,                          # website.layout
        'website_id': SITE_ID,
        'arch_db':    HEADER_ARCH,
        'active':     True,
        'priority':   25,
    }])
    print(f"  CREATED header view [{vid}]  key=website.lic_cards_header")

    # Verify
    v = xc(m, uid, 'ir.ui.view', 'read', [[vid]], {'fields':['key','active','website_id','priority']})
    print("  Verified:", v[0])

    print("\nDone. Hard refresh longislandcards.com (Ctrl+Shift+R)")

if __name__ == '__main__':
    main()
