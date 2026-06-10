#!/usr/bin/env python3
"""
Long Island Cards — Complete Setup:
1. Responsive header with role-based nav (Guest / Customer / Seller / Admin)
2. Professional footer (already view 3506, update it)
3. Create 3 user accounts: customer, seller, admin
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
    print(f"Connected UID {uid}")
    return m, uid

def xc(m, uid, model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

# ─────────────────────────────────────────────────────────────────
#  HEADER TEMPLATE  (website.layout inherit, website_id=36)
#  Three-tier nav: Guest | Customer (portal) | Seller | Admin
# ─────────────────────────────────────────────────────────────────
HEADER_ARCH = '''<data>
<xpath expr="//header" position="replace">
<header t-attf-class="o_cc o_cc1 o_header_affix #{('o_header_sidebar' if is_vertical_nav else '')}" id="top" data-anchor="true" style="position:sticky;top:0;z-index:1000;background:#0a0a0a;border-bottom:1px solid rgba(212,175,55,0.18);box-shadow:0 2px 20px rgba(0,0,0,0.6);">

  <!-- ── ANNOUNCEMENT BAR ────────────────────────── -->
  <div style="background:#D4AF37;padding:6px 0;text-align:center;">
    <span style="font-size:12px;font-weight:700;color:#000;letter-spacing:1px;">
      Free shipping on orders over $75 &#8226; Same-day dispatch before 3 PM &#8226; Serving Long Island since 2010
    </span>
  </div>

  <!-- ── MAIN NAV ────────────────────────────────── -->
  <div style="max-width:1280px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:68px;">

    <!-- LOGO -->
    <a href="/" style="text-decoration:none;flex-shrink:0;display:flex;align-items:center;gap:10px;">
      <div style="width:38px;height:38px;background:#D4AF37;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;color:#000;line-height:1;">LI</div>
      <div>
        <div style="color:#ffffff;font-size:16px;font-weight:900;letter-spacing:-0.5px;line-height:1;">Long Island</div>
        <div style="color:#D4AF37;font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;line-height:1.2;">Cards</div>
      </div>
    </a>

    <!-- DESKTOP NAV LINKS -->
    <nav style="display:flex;align-items:center;gap:4px;" class="d-none d-lg-flex">
      <a href="/shop" style="color:rgba(255,255,255,0.75);font-size:14px;font-weight:600;padding:8px 14px;border-radius:6px;text-decoration:none;">Shop</a>
      <a href="/shop?category=sports-cards" style="color:rgba(255,255,255,0.75);font-size:14px;font-weight:600;padding:8px 14px;border-radius:6px;text-decoration:none;">Sports Cards</a>
      <a href="/shop?category=pokemon" style="color:rgba(255,255,255,0.75);font-size:14px;font-weight:600;padding:8px 14px;border-radius:6px;text-decoration:none;">Pokemon</a>
      <a href="/shop?category=magic-the-gathering" style="color:rgba(255,255,255,0.75);font-size:14px;font-weight:600;padding:8px 14px;border-radius:6px;text-decoration:none;">MTG</a>
      <a href="/shop?category=yu-gi-oh" style="color:rgba(255,255,255,0.75);font-size:14px;font-weight:600;padding:8px 14px;border-radius:6px;text-decoration:none;">Yu-Gi-Oh!</a>
      <a href="/shop?category=graded-cards" style="color:rgba(255,255,255,0.75);font-size:14px;font-weight:600;padding:8px 14px;border-radius:6px;text-decoration:none;">Graded</a>
    </nav>

    <!-- RIGHT SIDE ACTIONS -->
    <div style="display:flex;align-items:center;gap:8px;">

      <!-- SEARCH -->
      <a href="/shop" style="color:rgba(255,255,255,0.55);padding:8px;border-radius:6px;text-decoration:none;font-size:16px;display:flex;align-items:center;" title="Search">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </a>

      <!-- ═══ GUEST (not logged in) ═══ -->
      <t t-if="env.user._is_public()">
        <a href="/web/login" style="color:rgba(255,255,255,0.7);font-size:13px;font-weight:600;padding:8px 16px;border-radius:6px;text-decoration:none;border:1px solid rgba(255,255,255,0.15);">Log In</a>
        <a href="/web/login?redirect=%2Fshop" style="background:#D4AF37;color:#000;font-size:13px;font-weight:700;padding:8px 18px;border-radius:6px;text-decoration:none;">Sign Up</a>
      </t>

      <!-- ═══ PORTAL CUSTOMER ═══ -->
      <t t-if="not env.user._is_public() and env.user.share">
        <!-- Cart -->
        <a href="/shop/cart" style="position:relative;color:rgba(255,255,255,0.7);padding:8px;border-radius:6px;text-decoration:none;display:flex;align-items:center;" title="Cart">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
          <t t-set="cart_qty" t-value="website_sale_cart_quantity or 0"/>
          <span t-if="cart_qty" style="position:absolute;top:2px;right:2px;background:#D4AF37;color:#000;font-size:9px;font-weight:800;min-width:16px;height:16px;border-radius:8px;display:flex;align-items:center;justify-content:center;padding:0 3px;" t-out="cart_qty"/>
        </a>
        <!-- Account dropdown -->
        <div style="position:relative;" class="o_header_customer_dropdown">
          <button onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display=='block'?'none':'block'" style="background:rgba(212,175,55,0.12);color:#D4AF37;font-size:13px;font-weight:700;padding:8px 14px;border-radius:6px;border:1px solid rgba(212,175,55,0.3);cursor:pointer;display:flex;align-items:center;gap:6px;">
            <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            My Account
            <svg width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6,9 12,15 18,9"/></svg>
          </button>
          <div style="display:none;position:absolute;right:0;top:calc(100% + 8px);background:#1a1a1a;border:1px solid rgba(212,175,55,0.2);border-radius:10px;min-width:200px;padding:8px;box-shadow:0 12px 40px rgba(0,0,0,0.6);z-index:999;">
            <div style="padding:10px 12px 8px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:6px;">
              <div style="color:#D4AF37;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Customer</div>
              <div style="color:rgba(255,255,255,0.5);font-size:12px;margin-top:2px;" t-out="env.user.name"/>
            </div>
            <a href="/my/orders" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.7);font-size:13px;text-decoration:none;border-radius:6px;">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>My Orders
            </a>
            <a href="/my/account" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.7);font-size:13px;text-decoration:none;border-radius:6px;">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>My Profile
            </a>
            <a href="/shop/wishlist" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.7);font-size:13px;text-decoration:none;border-radius:6px;">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>Wishlist
            </a>
            <div style="border-top:1px solid rgba(255,255,255,0.06);margin:6px 0;padding-top:6px;">
              <a href="/web/session/logout?redirect=/" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,100,100,0.7);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>Log Out
              </a>
            </div>
          </div>
        </div>
      </t>

      <!-- ═══ INTERNAL USER (Seller / Admin) ═══ -->
      <t t-if="not env.user._is_public() and not env.user.share">

        <!-- Cart (internal staff can browse shop too) -->
        <a href="/shop/cart" style="color:rgba(255,255,255,0.7);padding:8px;border-radius:6px;text-decoration:none;display:flex;align-items:center;" title="Cart">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
        </a>

        <!-- SELLER PANEL (non-admin internal) -->
        <t t-if="not env.user.has_group('base.group_erp_manager') and not env.user.has_group('base.group_system')">
          <div style="position:relative;">
            <button onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display=='block'?'none':'block'" style="background:rgba(34,197,94,0.1);color:#22c55e;font-size:13px;font-weight:700;padding:8px 14px;border-radius:6px;border:1px solid rgba(34,197,94,0.25);cursor:pointer;display:flex;align-items:center;gap:6px;">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
              Seller Panel
              <svg width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6,9 12,15 18,9"/></svg>
            </button>
            <div style="display:none;position:absolute;right:0;top:calc(100% + 8px);background:#0f1a0f;border:1px solid rgba(34,197,94,0.2);border-radius:10px;min-width:210px;padding:8px;box-shadow:0 12px 40px rgba(0,0,0,0.7);z-index:999;">
              <div style="padding:10px 12px 8px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:6px;">
                <div style="color:#22c55e;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Seller Account</div>
                <div style="color:rgba(255,255,255,0.45);font-size:12px;margin-top:2px;" t-out="env.user.name"/>
              </div>
              <a href="/odoo/sales" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>My Sales
              </a>
              <a href="/odoo/inventory/products" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 7H4a2 2 0 00-2 2v10a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/></svg>My Products
              </a>
              <a href="/odoo/sales?status=to_invoice" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>Pending Orders
              </a>
              <a href="/my/account" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>My Profile
              </a>
              <div style="border-top:1px solid rgba(255,255,255,0.06);margin:6px 0;padding-top:6px;">
                <a href="/web/session/logout?redirect=/" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,100,100,0.6);font-size:13px;text-decoration:none;border-radius:6px;">
                  <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>Log Out
                </a>
              </div>
            </div>
          </div>
        </t>

        <!-- ADMIN PANEL -->
        <t t-if="env.user.has_group('base.group_erp_manager') or env.user.has_group('base.group_system')">
          <div style="position:relative;">
            <button onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display=='block'?'none':'block'" style="background:rgba(99,102,241,0.12);color:#818cf8;font-size:13px;font-weight:700;padding:8px 14px;border-radius:6px;border:1px solid rgba(99,102,241,0.3);cursor:pointer;display:flex;align-items:center;gap:6px;">
              <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
              Admin
              <svg width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6,9 12,15 18,9"/></svg>
            </button>
            <div style="display:none;position:absolute;right:0;top:calc(100% + 8px);background:#0d0d1a;border:1px solid rgba(99,102,241,0.25);border-radius:10px;min-width:220px;padding:8px;box-shadow:0 12px 40px rgba(0,0,0,0.75);z-index:999;">
              <div style="padding:10px 12px 8px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:6px;">
                <div style="color:#818cf8;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Administrator</div>
                <div style="color:rgba(255,255,255,0.45);font-size:12px;margin-top:2px;" t-out="env.user.name"/>
              </div>
              <a href="/odoo" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.8);font-size:13px;font-weight:600;text-decoration:none;border-radius:6px;background:rgba(99,102,241,0.08);">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>Odoo Backend
              </a>
              <a href="/odoo/ecommerce/products" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 7H4a2 2 0 00-2 2v10a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/></svg>Products
              </a>
              <a href="/odoo/ecommerce/orders" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Orders
              </a>
              <a href="/odoo/website" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>Website Editor
              </a>
              <a href="/odoo/users" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>Users
              </a>
              <a href="/odoo/reporting/sales" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,255,255,0.75);font-size:13px;text-decoration:none;border-radius:6px;">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>Sales Report
              </a>
              <div style="border-top:1px solid rgba(255,255,255,0.06);margin:6px 0;padding-top:6px;">
                <a href="/web/session/logout?redirect=/" style="display:flex;align-items:center;gap:10px;padding:9px 12px;color:rgba(255,100,100,0.6);font-size:13px;text-decoration:none;border-radius:6px;">
                  <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>Log Out
                </a>
              </div>
            </div>
          </div>
        </t>

      </t><!-- /internal user -->

      <!-- MOBILE HAMBURGER -->
      <button class="d-lg-none" onclick="document.getElementById('lic_mobile_menu').classList.toggle('lic_open')"
              style="background:transparent;border:1px solid rgba(255,255,255,0.15);border-radius:6px;padding:8px 10px;cursor:pointer;display:flex;flex-direction:column;gap:4px;align-items:center;justify-content:center;">
        <span style="display:block;width:20px;height:2px;background:rgba(255,255,255,0.7);border-radius:1px;"></span>
        <span style="display:block;width:20px;height:2px;background:rgba(255,255,255,0.7);border-radius:1px;"></span>
        <span style="display:block;width:20px;height:2px;background:rgba(255,255,255,0.7);border-radius:1px;"></span>
      </button>

    </div><!-- /right actions -->
  </div><!-- /main nav -->

  <!-- ── MOBILE MENU ─────────────────────────────── -->
  <div id="lic_mobile_menu" style="display:none;background:#111;border-top:1px solid rgba(212,175,55,0.15);padding:16px 24px 24px;" class="d-lg-none">
    <style>.lic_open #lic_mobile_menu { display:block !important; }</style>
    <a href="/shop" style="display:block;padding:12px 0;color:rgba(255,255,255,0.8);font-size:15px;font-weight:600;text-decoration:none;border-bottom:1px solid rgba(255,255,255,0.05);">Shop All</a>
    <a href="/shop?category=sports-cards" style="display:block;padding:12px 0;color:rgba(255,255,255,0.7);font-size:14px;text-decoration:none;border-bottom:1px solid rgba(255,255,255,0.05);">Sports Cards</a>
    <a href="/shop?category=pokemon" style="display:block;padding:12px 0;color:rgba(255,255,255,0.7);font-size:14px;text-decoration:none;border-bottom:1px solid rgba(255,255,255,0.05);">Pokemon</a>
    <a href="/shop?category=magic-the-gathering" style="display:block;padding:12px 0;color:rgba(255,255,255,0.7);font-size:14px;text-decoration:none;border-bottom:1px solid rgba(255,255,255,0.05);">MTG</a>
    <a href="/shop?category=yu-gi-oh" style="display:block;padding:12px 0;color:rgba(255,255,255,0.7);font-size:14px;text-decoration:none;border-bottom:1px solid rgba(255,255,255,0.05);">Yu-Gi-Oh!</a>
    <a href="/shop?category=graded-cards" style="display:block;padding:12px 0;color:rgba(255,255,255,0.7);font-size:14px;text-decoration:none;border-bottom:1px solid rgba(255,255,255,0.05);">Graded Cards</a>
    <t t-if="env.user._is_public()">
      <div style="display:flex;gap:12px;margin-top:16px;">
        <a href="/web/login" style="flex:1;text-align:center;color:#fff;font-size:14px;font-weight:600;padding:12px;border-radius:8px;text-decoration:none;border:1px solid rgba(255,255,255,0.2);">Log In</a>
        <a href="/web/login" style="flex:1;text-align:center;background:#D4AF37;color:#000;font-size:14px;font-weight:700;padding:12px;border-radius:8px;text-decoration:none;">Sign Up</a>
      </div>
    </t>
    <t t-if="not env.user._is_public()">
      <div style="margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.08);">
        <div style="color:rgba(255,255,255,0.35);font-size:11px;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">Account</div>
        <a href="/my/orders" style="display:block;padding:10px 0;color:rgba(255,255,255,0.7);font-size:14px;text-decoration:none;">My Orders</a>
        <a href="/my/account" style="display:block;padding:10px 0;color:rgba(255,255,255,0.7);font-size:14px;text-decoration:none;">My Profile</a>
        <a href="/shop/cart" style="display:block;padding:10px 0;color:rgba(255,255,255,0.7);font-size:14px;text-decoration:none;">Cart</a>
        <a href="/web/session/logout?redirect=/" style="display:block;padding:10px 0;color:rgba(255,100,100,0.7);font-size:14px;text-decoration:none;">Log Out</a>
      </div>
    </t>
  </div>

</header>
</xpath>
</data>'''


def main():
    m, uid = connect()

    # ── 1. Get group IDs ──────────────────────────────────────
    print("\n[1] Getting group IDs...")
    all_groups = xc(m, uid, 'res.groups', 'search_read', [[]], {'fields': ['id','full_name'], 'limit': 100})
    group_map = {g['full_name']: g['id'] for g in all_groups}

    portal_gid    = group_map.get('Role / Portal') or group_map.get('Extra Rights / Portal') or 10
    internal_gid  = next((g['id'] for g in all_groups if 'Internal User' in g['full_name']), None)
    sales_gid     = group_map.get('Sales / User: All Documents') or 23
    admin_gid     = next((g['id'] for g in all_groups if 'Settings' in g['full_name'] and 'Configuration' not in g['full_name']), None)

    print(f"  Portal={portal_gid} Internal={internal_gid} Sales={sales_gid} Admin={admin_gid}")

    # ── 2. Create / ensure CUSTOMER account ──────────────────
    print("\n[2] Customer account...")
    existing = xc(m, uid, 'res.users', 'search_read',
        [[('login','=','customer@longislandcards.com')]], {'fields':['id','name']})
    if existing:
        print(f"  EXISTS: {existing[0]}")
    else:
        try:
            cust_vals = {
                'name': 'Card Collector',
                'login': 'customer@longislandcards.com',
                'email': 'customer@longislandcards.com',
                'password': 'Customer@2026',
                'groups_id': [(6, 0, [portal_gid])],
                'website_id': SITE_ID,
            }
            cid = xc(m, uid, 'res.users', 'create', [cust_vals])
            print(f"  CREATED customer user [{cid}]")
        except Exception as e:
            print(f"  Customer create: {str(e)[:120]}")

    # ── 3. Create / ensure SELLER account ────────────────────
    print("\n[3] Seller account...")
    existing = xc(m, uid, 'res.users', 'search_read',
        [[('login','=','seller@longislandcards.com')]], {'fields':['id','name']})
    if existing:
        print(f"  EXISTS: {existing[0]}")
    else:
        try:
            seller_groups = [internal_gid, sales_gid] if internal_gid else [sales_gid]
            seller_vals = {
                'name': 'LI Cards Seller',
                'login': 'seller@longislandcards.com',
                'email': 'seller@longislandcards.com',
                'password': 'Seller@2026',
                'groups_id': [(6, 0, [g for g in seller_groups if g])],
                'website_id': SITE_ID,
            }
            sid = xc(m, uid, 'res.users', 'create', [seller_vals])
            print(f"  CREATED seller user [{sid}]")
        except Exception as e:
            print(f"  Seller create: {str(e)[:120]}")

    # ── 4. Create / ensure ADMIN account ─────────────────────
    print("\n[4] Admin account...")
    existing = xc(m, uid, 'res.users', 'search_read',
        [[('login','=','admin@longislandcards.com')]], {'fields':['id','name']})
    if existing:
        print(f"  EXISTS: {existing[0]}")
    else:
        try:
            admin_groups = [g for g in [internal_gid, admin_gid] if g]
            admin_vals = {
                'name': 'LI Cards Admin',
                'login': 'admin@longislandcards.com',
                'email': 'admin@longislandcards.com',
                'password': 'Admin@2026!',
                'groups_id': [(6, 0, admin_groups)],
                'website_id': SITE_ID,
            }
            aid = xc(m, uid, 'res.users', 'create', [admin_vals])
            print(f"  CREATED admin user [{aid}]")
        except Exception as e:
            print(f"  Admin create: {str(e)[:120]}")

    # ── 5. Create website-36 header override ─────────────────
    print("\n[5] Setting up responsive header for website 36...")

    existing = xc(m, uid, 'ir.ui.view', 'search_read',
        [[('key','=','website.layout'),('website_id','=',SITE_ID)]],
        {'fields': ['id','name']})

    if existing:
        xc(m, uid, 'ir.ui.view', 'write', [[existing[0]['id']], {
            'arch_db': HEADER_ARCH,
            'active': True,
        }])
        print(f"  UPDATED header view [{existing[0]['id']}]")
    else:
        vid = xc(m, uid, 'ir.ui.view', 'create', [{
            'name': 'Long Island Cards — Header',
            'key': 'website.layout',
            'type': 'qweb',
            'inherit_id': 603,
            'website_id': SITE_ID,
            'arch_db': HEADER_ARCH,
            'active': True,
            'priority': 20,
        }])
        print(f"  CREATED header view [{vid}]")

    print("\n" + "="*55)
    print("  DONE — Hard refresh longislandcards.com")
    print("="*55)
    print("\n  LOGIN CREDENTIALS:")
    print("  Customer  : customer@longislandcards.com / Customer@2026")
    print("  Seller    : seller@longislandcards.com   / Seller@2026")
    print("  Admin     : admin@longislandcards.com    / Admin@2026!")
    print("  Master    : countrycoveinc@gmail.com     / M@nhattan1234")
    print("="*55)

if __name__ == '__main__':
    main()
