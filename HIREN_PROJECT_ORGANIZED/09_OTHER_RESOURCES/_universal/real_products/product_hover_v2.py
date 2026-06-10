import xmlrpc.client, sys

sys.stdout.reconfigure(encoding='utf-8')
URL = 'https://country-cove-inc.odoo.com'
DB  = 'country-cove-inc'
UID = 2
PW  = 'M@nhattan1234'

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
print("Connected")

# ─────────────────────────────────────────────────────────────
# ACTUAL DOM STRUCTURE ON LIVE SITE (confirmed by fetch):
#
#   <a href="/shop/product-slug-310">           ← IMAGE ANCHOR
#     <img src="...image_1024..." alt="Name">
#   </a>
#   <h6><a href="/shop/product-slug-310">Name</a></h6>
#   <text node: description...>                 ← plain text / span
#   $ 89.99
#   <a>Add to Cart</a>
#   <a>Add to wishlist</a>
#
# STRATEGY:
#   1. Find every <a> that wraps an <img> with src containing
#      "image_1024" or "image_512" (Odoo product thumbnails)
#   2. Make that anchor position:relative, inject glow button inside
#   3. On hover → glow button pulses up
#   4. On click → full description slides up in bottom sheet modal
#   5. Description text = next sibling text after the h6
#   6. Also HIDE the description text in the card (truncate to 0 lines)
#      so cards look clean — full text only shows in the modal
# ─────────────────────────────────────────────────────────────

HOVER_BLOCK = """
<!-- ===== PRODUCT CARD HOVER DESCRIPTION ===== -->
<style>
/* ── 1. Hide description text in shop cards — show only on hover panel ── */
.o_wsale_product_grid_cell .o_not_editable,
.oe_product .o_not_editable,
[data-pcd-desc] {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  opacity: .7;
  font-size: .8rem !important;
  line-height: 1.45 !important;
  margin-bottom: 6px !important;
}

/* ── 2. Image anchor — must be relative for button to sit inside ── */
a.pcd-img-wrap {
  position: relative !important;
  display: block;
  overflow: hidden;
  border-radius: 10px;
}

/* ── 3. Glow button — hidden by default ── */
.pcd-btn {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%) translateY(16px);
  z-index: 30;
  padding: 9px 20px;
  background: linear-gradient(135deg, #1a5c3a 0%, #52b788 100%);
  color: #fff !important;
  font-size: .78rem;
  font-weight: 800;
  border: 2px solid rgba(255,255,255,.35);
  border-radius: 30px;
  cursor: pointer;
  white-space: nowrap;
  letter-spacing: .05em;
  opacity: 0;
  pointer-events: none;
  transition:
    opacity .28s ease,
    transform .38s cubic-bezier(.34,1.56,.64,1),
    box-shadow .28s ease;
  text-decoration: none !important;
  box-shadow: 0 4px 20px rgba(45,106,79,.0);
}

/* ── 4. Pulse ring animation ── */
@keyframes pcd-pulse {
  0%   { box-shadow: 0 0 0 0 rgba(82,183,136,.8), 0 4px 20px rgba(45,106,79,.4); }
  60%  { box-shadow: 0 0 0 10px rgba(82,183,136,0), 0 4px 20px rgba(45,106,79,.4); }
  100% { box-shadow: 0 0 0 0 rgba(82,183,136,0), 0 4px 20px rgba(45,106,79,.4); }
}

/* ── 5. Show on hover ── */
a.pcd-img-wrap:hover .pcd-btn,
a.pcd-img-wrap.pcd-touched .pcd-btn {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
  pointer-events: auto;
  animation: pcd-pulse 1.6s ease infinite;
}

/* ── 6. Dim image on hover ── */
a.pcd-img-wrap img {
  transition: filter .3s ease, transform .4s ease;
  display: block;
  width: 100%;
}
a.pcd-img-wrap:hover img {
  filter: brightness(.72) saturate(1.15);
  transform: scale(1.03);
}

/* ════════════════════════════════════════════════
   BOTTOM SHEET MODAL
════════════════════════════════════════════════ */
#pcd-overlay {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 1000000;
  background: rgba(10,20,15,.6);
  backdrop-filter: blur(7px);
  -webkit-backdrop-filter: blur(7px);
  align-items: flex-end;
  justify-content: center;
  opacity: 0;
  transition: opacity .3s ease;
}
#pcd-overlay.pcd-show {
  display: flex;
  opacity: 0;
}
#pcd-overlay.pcd-visible { opacity: 1; }

#pcd-sheet {
  background: #fff;
  width: 100%;
  max-width: 700px;
  max-height: 85vh;
  border-radius: 22px 22px 0 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transform: translateY(110%);
  transition: transform .42s cubic-bezier(.32,1.25,.6,1);
  box-shadow: 0 -16px 70px rgba(0,0,0,.28);
}
#pcd-overlay.pcd-visible #pcd-sheet { transform: translateY(0); }

/* Drag handle */
#pcd-handle {
  width: 42px; height: 5px;
  background: rgba(255,255,255,.5);
  border-radius: 3px;
  margin: 10px auto 0;
  flex-shrink: 0;
}

/* Header */
#pcd-head {
  background: linear-gradient(135deg, #1a5c3a, #52b788);
  padding: 6px 20px 18px;
  flex-shrink: 0;
  position: relative;
}
#pcd-head h3 {
  color: #fff;
  font-size: clamp(1rem,3.5vw,1.2rem);
  font-weight: 900;
  margin: 12px 40px 4px 0;
  line-height: 1.3;
  text-shadow: 0 1px 5px rgba(0,0,0,.2);
}
#pcd-price-tag {
  display: inline-block;
  background: rgba(255,255,255,.22);
  color: #fff;
  font-size: .85rem;
  font-weight: 800;
  padding: 3px 12px;
  border-radius: 20px;
  margin-top: 4px;
}
#pcd-x {
  position: absolute;
  top: 12px; right: 14px;
  background: rgba(255,255,255,.25);
  border: none; color: #fff;
  width: 32px; height: 32px;
  border-radius: 50%;
  font-size: 1rem; font-weight: 900;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background .2s;
}
#pcd-x:hover { background: rgba(255,255,255,.45); }

/* Body */
#pcd-body {
  padding: 20px 22px 8px;
  overflow-y: auto;
  flex: 1;
}
#pcd-text {
  font-size: .96rem;
  line-height: 1.8;
  color: #222;
}

/* Footer CTA buttons */
#pcd-foot {
  padding: 14px 20px 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  border-top: 1px solid #f0f0f0;
  flex-shrink: 0;
}
.pcd-cta {
  flex: 1;
  min-width: 130px;
  padding: 12px 18px;
  border-radius: 30px;
  text-align: center;
  font-size: .82rem;
  font-weight: 800;
  letter-spacing: .04em;
  text-decoration: none !important;
  transition: opacity .2s, transform .2s;
  cursor: pointer;
  border: none;
}
.pcd-cta:hover { opacity: .88; transform: translateY(-2px); }
.pcd-cta.prim { background: linear-gradient(135deg,#1a5c3a,#52b788); color: #fff !important; }
.pcd-cta.sec  { background: #eef5f1; color: #1a5c3a !important; }
</style>

<!-- Bottom sheet modal -->
<div id="pcd-overlay">
  <div id="pcd-sheet">
    <div id="pcd-handle"></div>
    <div id="pcd-head">
      <button id="pcd-x" onclick="pcdClose()" aria-label="Close">&#10005;</button>
      <h3 id="pcd-title">Product Details</h3>
      <span id="pcd-price-tag"></span>
    </div>
    <div id="pcd-body">
      <p id="pcd-text"></p>
    </div>
    <div id="pcd-foot">
      <a id="pcd-cart"  href="#" class="pcd-cta prim">&#128722; Add to Cart</a>
      <a id="pcd-page"  href="#" class="pcd-cta sec">View Full Page &#8594;</a>
    </div>
  </div>
</div>

<script>
(function(){
  var ov = document.getElementById('pcd-overlay');

  // ── Open modal ────────────────────────────────────────────
  window.pcdOpen = function(title, desc, price, pageUrl) {
    document.getElementById('pcd-title').textContent    = title || '';
    document.getElementById('pcd-text').textContent     = desc  || '';
    document.getElementById('pcd-price-tag').textContent= price ? ('$' + price) : '';
    document.getElementById('pcd-cart').href  = pageUrl || '#';
    document.getElementById('pcd-page').href  = pageUrl || '#';
    ov.style.display = 'flex';
    requestAnimationFrame(function(){
      requestAnimationFrame(function(){
        ov.classList.add('pcd-show','pcd-visible');
      });
    });
    document.body.style.overflow = 'hidden';
  };

  // ── Close modal ───────────────────────────────────────────
  window.pcdClose = function() {
    ov.classList.remove('pcd-visible');
    setTimeout(function(){
      ov.classList.remove('pcd-show');
      ov.style.display = 'none';
      document.body.style.overflow = '';
    }, 420);
  };

  // Close on backdrop click
  ov.addEventListener('click', function(e){ if(e.target===ov) pcdClose(); });
  // Close on Escape
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') pcdClose(); });

  // ── Inject glow buttons into product image anchors ────────
  function injectCards() {
    // Select every <a> that directly wraps a product thumbnail
    var anchors = document.querySelectorAll('a[href*="/shop/"]');
    anchors.forEach(function(a) {
      // Must contain an img with product image URL
      var img = a.querySelector('img[src*="image_1024"], img[src*="image_512"], img[src*="product"]');
      if (!img) return;
      if (a.querySelector('.pcd-btn')) return; // already done

      a.classList.add('pcd-img-wrap');
      // Prevent the anchor navigating when button is clicked
      // (handled by stopPropagation on button)

      // ── Gather card data ────────────────────────────────
      // Walk UP to find the product cell container
      var cell = a.closest('[class*="product"], [class*="col"], article, li, div')
               || a.parentElement;

      // Title from alt attr (most reliable in Odoo) or h6
      var title = img.alt || '';
      if (!title) {
        var h = cell ? cell.querySelector('h6 a, h5 a, h4 a, h6, h5') : null;
        title = h ? h.textContent.trim() : 'Product Details';
      }

      // Page URL
      var pageUrl = a.href;

      // Price — find $ text in the cell
      var priceEl = cell ? cell.querySelector('[class*="price"], .oe_price, .o_price') : null;
      var price = '';
      if (!priceEl && cell) {
        // Fallback: look for text containing $
        Array.from(cell.querySelectorAll('*')).forEach(function(el){
          if (!price && el.childNodes.length === 1 && /\$\s*[\d.]+/.test(el.textContent)) {
            price = el.textContent.trim().replace('$','').trim();
          }
        });
      } else if (priceEl) {
        price = priceEl.textContent.trim().replace('$','').trim();
      }

      // Description — longest text block in the cell that isn't the title
      var desc = '';
      if (cell) {
        var candidates = cell.querySelectorAll('span, p, div');
        candidates.forEach(function(el){
          var t = el.textContent.trim();
          if (t.length > desc.length && t !== title && !t.match(/^\$/) && !t.match(/^Add/) && el.children.length === 0) {
            desc = t;
          }
        });
      }
      // Fallback to img title attribute
      if (!desc) desc = a.title || '';

      // ── Build glow button ───────────────────────────────
      var btn = document.createElement('button');
      btn.className = 'pcd-btn';
      btn.innerHTML = '&#128214;&nbsp;&nbsp;View Details';
      btn.setAttribute('type','button');
      btn.setAttribute('aria-label','View details for ' + title);

      btn.addEventListener('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        pcdOpen(title, desc, price, pageUrl);
      });

      a.appendChild(btn);

      // ── Touch: tap image = show button, tap button = open modal ──
      a.addEventListener('touchstart', function(e){
        if (e.target === btn) return; // let button handle it
        if (!a.classList.contains('pcd-touched')) {
          e.preventDefault();
          a.classList.add('pcd-touched');
        }
      }, {passive:false});
    });

    // Hide touch-highlight when tapping elsewhere
    document.addEventListener('touchstart', function(e){
      document.querySelectorAll('a.pcd-img-wrap.pcd-touched').forEach(function(el){
        if (!el.contains(e.target)) el.classList.remove('pcd-touched');
      });
    }, {passive:true});
  }

  // ── Run + poll for Odoo lazy-rendered cards ───────────────
  function boot() {
    injectCards();
    var n = 0, t = setInterval(function(){
      injectCards();
      if (++n >= 16) clearInterval(t);
    }, 500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(boot, 300); });
  } else {
    setTimeout(boot, 300);
  }

  // Odoo SPA navigation
  ['pushState','replaceState'].forEach(function(fn){
    var orig = history[fn];
    history[fn] = function(){
      orig.apply(history, arguments);
      setTimeout(boot, 700);
    };
  });
  window.addEventListener('popstate', function(){ setTimeout(boot, 700); });
})();
</script>
<!-- ===== END PRODUCT CARD HOVER DESCRIPTION ===== -->
"""

# ─────────────────────────────────────────────────────────────
# REPLACE OLD BLOCK + INJECT FIXED VERSION INTO VIEW 2956
# ─────────────────────────────────────────────────────────────
MARKER_S = '<!-- ===== PRODUCT CARD HOVER DESCRIPTION ====='
MARKER_E = '<!-- ===== END PRODUCT CARD HOVER DESCRIPTION ====='

print('\nReading view 2956...')
arch = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'read',
                         [[2956]], {'fields': ['arch_db']})[0]['arch_db']

# Remove old version
if MARKER_S in arch and MARKER_E in arch:
    s = arch.index(MARKER_S)
    e = arch.index(MARKER_E) + len(MARKER_E)
    arch = arch[:s] + arch[e:]
    print('  Removed old hover block.')
else:
    print('  No existing hover block found — fresh inject.')

# Append before closing root tag
for closing in ['</t>', '</template>']:
    if arch.rstrip().endswith(closing):
        arch = arch.rstrip()[:-len(closing)] + '\n' + HOVER_BLOCK.strip() + '\n' + closing
        break
else:
    arch = arch.rstrip() + '\n' + HOVER_BLOCK.strip()

res = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'write',
                        [[2956], {'arch_db': arch}])
print(f'  View 2956 updated: {res}')

print("""
Done! Test steps:
  1. Open https://www.ligiftbasket.com/shop?search=father
  2. Hard refresh: Ctrl+Shift+R
  3. Hover over any product IMAGE
  4. Green glowing "📖 View Details" button should pulse up
  5. Click it → full description slides up from bottom
""")