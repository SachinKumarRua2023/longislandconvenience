import xmlrpc.client, sys

sys.stdout.reconfigure(encoding='utf-8')
URL = 'https://country-cove-inc.odoo.com'
DB  = 'country-cove-inc'
UID = 2
PW  = 'M@nhattan1234'

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
print("Connected\n")

# ─────────────────────────────────────────────────────────────
# FIX: The 500 error was caused by FinalFathersDay.py injecting
# a <div id="pcd-modal"> and <script> INSIDE <head> via XPath.
# Odoo QWeb rejects block HTML elements inside <head>.
#
# CORRECT approach:
#   • CSS only  → goes inside <head>
#   • Modal HTML + JS → goes AFTER <body> opens (inside <body>)
#
# We split into two separate xpath positions:
#   1. //head  position="inside"  → CSS only
#   2. //body  position="inside"  → modal div + script
# ─────────────────────────────────────────────────────────────

# ── Step 1: Delete the broken global view ─────────────────────
print("Step 1: Removing broken global hover view(s)...")
bad_ids = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'search', [[
    ['name', 'in', [
        'LI GiftBasket - Global Hover CSS JS',
        'LI GiftBasket - Product Hover Button',
        'LI GiftBasket - Shop Hover CSS',
        'LI GiftBasket Hover CSS JS',
    ]],
    ['website_id', '=', 37]
]])
if bad_ids:
    models.execute_kw(DB, UID, PW, 'ir.ui.view', 'unlink', [bad_ids])
    print(f"  Deleted {len(bad_ids)} broken view(s): {bad_ids}")
else:
    print("  None found.")

# ── Step 2: Also clean homepage view 2956 of any pcd blocks ───
print("\nStep 2: Cleaning homepage view 2956...")
arch_home = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'read',
                               [[2956]], {'fields': ['arch_db']})[0]['arch_db']

changed = False
for marker_s, marker_e in [
    ('<!-- ===== PRODUCT CARD HOVER DESCRIPTION =====',
     '<!-- ===== END PRODUCT CARD HOVER DESCRIPTION ====='),
]:
    if marker_s in arch_home and marker_e in arch_home:
        s = arch_home.index(marker_s)
        e = arch_home.index(marker_e) + len(marker_e)
        arch_home = arch_home[:s] + arch_home[e:]
        changed = True

if changed:
    models.execute_kw(DB, UID, PW, 'ir.ui.view', 'write',
                      [[2956], {'arch_db': arch_home}])
    print("  Cleaned old pcd block from homepage.")
else:
    print("  Homepage already clean.")

# ── Step 3: Get website.layout view ID ────────────────────────
layout_id = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'search',
                               [[['key', '=', 'website.layout']]])[0]
print(f"\nStep 3: website.layout view ID = {layout_id}")

# ── Step 4: Create FIXED inherit view ─────────────────────────
# Split correctly:
#   xpath 1 → //head  (CSS only, no HTML block elements)
#   xpath 2 → //body  (modal div + script)

FIXED_VIEW = """<t t-name="ligiftbasket.global_hover_css" t-inherit="website.layout" t-inherit-mode="extension">

  <!-- ① CSS into <head> (safe — no block elements) -->
  <xpath expr="//head" position="inside">
    <style>
      .pcd-wrap{position:relative!important;display:block;overflow:hidden;}
      .pcd-glow-btn{position:absolute;bottom:12px;left:50%;transform:translateX(-50%) translateY(20px);z-index:50;padding:9px 22px;background:linear-gradient(135deg,#1a5c3a,#52b788);color:#fff!important;font-size:.78rem;font-weight:800;border:2px solid rgba(255,255,255,.4);border-radius:30px;cursor:pointer;white-space:nowrap;letter-spacing:.05em;opacity:0;pointer-events:none;transition:opacity .28s ease,transform .38s cubic-bezier(.34,1.56,.64,1);text-decoration:none!important;}
      @keyframes pcd-pulse{0%{box-shadow:0 0 0 0 rgba(82,183,136,.8);}70%{box-shadow:0 0 0 12px rgba(82,183,136,0);}100%{box-shadow:0 0 0 0 rgba(82,183,136,0);}}
      .pcd-wrap:hover .pcd-glow-btn,.pcd-wrap.pcd-touch .pcd-glow-btn{opacity:1;transform:translateX(-50%) translateY(0);pointer-events:auto;animation:pcd-pulse 1.5s ease infinite;}
      .pcd-wrap img{transition:filter .3s ease,transform .4s ease;display:block;width:100%;}
      .pcd-wrap:hover img{filter:brightness(.75) saturate(1.1);transform:scale(1.03);}
      #pcd-modal{display:none;position:fixed;inset:0;z-index:1000000;background:rgba(5,15,10,.65);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);align-items:flex-end;justify-content:center;opacity:0;transition:opacity .3s ease;}
      #pcd-modal.on{display:flex;}
      #pcd-modal.vis{opacity:1;}
      #pcd-sheet{background:#fff;width:100%;max-width:680px;max-height:88vh;border-radius:22px 22px 0 0;overflow:hidden;display:flex;flex-direction:column;transform:translateY(110%);transition:transform .42s cubic-bezier(.32,1.25,.6,1);box-shadow:0 -16px 70px rgba(0,0,0,.3);}
      #pcd-modal.vis #pcd-sheet{transform:translateY(0);}
      #pcd-handle{width:42px;height:5px;background:#ddd;border-radius:3px;margin:10px auto 4px;}
      #pcd-head{background:linear-gradient(135deg,#1a5c3a,#52b788);padding:6px 20px 18px;position:relative;flex-shrink:0;}
      #pcd-head h3{color:#fff;font-size:clamp(1rem,3.5vw,1.18rem);font-weight:900;margin:10px 40px 4px 0;line-height:1.3;}
      #pcd-price-tag{display:inline-block;background:rgba(255,255,255,.22);color:#fff;font-size:.85rem;font-weight:800;padding:3px 12px;border-radius:20px;margin-top:2px;}
      #pcd-x{position:absolute;top:12px;right:14px;background:rgba(255,255,255,.25);border:none;color:#fff;width:32px;height:32px;border-radius:50%;font-size:1rem;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;}
      #pcd-body{padding:20px 22px 8px;overflow-y:auto;flex:1;}
      #pcd-desc{font-size:.97rem;line-height:1.8;color:#222;}
      #pcd-foot{padding:14px 20px 22px;display:flex;gap:10px;flex-wrap:wrap;border-top:1px solid #f0f0f0;flex-shrink:0;}
      .pcd-cta{flex:1;min-width:130px;padding:12px 18px;border-radius:30px;text-align:center;font-size:.82rem;font-weight:800;letter-spacing:.04em;text-decoration:none!important;transition:opacity .2s,transform .2s;border:none;cursor:pointer;}
      .pcd-cta.p{background:linear-gradient(135deg,#1a5c3a,#52b788);color:#fff!important;}
      .pcd-cta.s{background:#eef5f1;color:#1a5c3a!important;}
    </style>
  </xpath>

  <!-- ② Modal HTML + JS into <body> (block elements are fine here) -->
  <xpath expr="//body" position="inside">
    <div id="pcd-modal">
      <div id="pcd-sheet">
        <div id="pcd-handle"></div>
        <div id="pcd-head">
          <button id="pcd-x" onclick="pcdClose()" type="button">&#10005;</button>
          <h3 id="pcd-title">Product Details</h3>
          <span id="pcd-price-tag"></span>
        </div>
        <div id="pcd-body"><p id="pcd-desc"></p></div>
        <div id="pcd-foot">
          <a id="pcd-cart" href="#" class="pcd-cta p">&#128722; Add to Cart</a>
          <a id="pcd-page" href="#" class="pcd-cta s">View Full Page &#8594;</a>
        </div>
      </div>
    </div>

    <script>
    (function(){
      var modal=document.getElementById('pcd-modal');
      if(!modal)return;

      window.pcdOpen=function(title,desc,price,url){
        document.getElementById('pcd-title').textContent=title||'';
        document.getElementById('pcd-desc').textContent=desc||'';
        var ptag=document.getElementById('pcd-price-tag');
        ptag.textContent=price?'$'+price:''; ptag.style.display=price?'':'none';
        document.getElementById('pcd-cart').href=url||'#';
        document.getElementById('pcd-page').href=url||'#';
        modal.classList.add('on');
        requestAnimationFrame(function(){requestAnimationFrame(function(){modal.classList.add('vis');});});
        document.body.style.overflow='hidden';
      };
      window.pcdClose=function(){
        modal.classList.remove('vis');
        setTimeout(function(){modal.classList.remove('on');document.body.style.overflow='';},420);
      };
      modal.addEventListener('click',function(e){if(e.target===modal)pcdClose();});
      document.addEventListener('keydown',function(e){if(e.key==='Escape')pcdClose();});

      function inject(){
        var links=document.querySelectorAll('a[href*="/shop/"]');
        links.forEach(function(a){
          if(a.querySelector('.pcd-glow-btn'))return;
          var img=a.querySelector('img');
          if(!img)return;
          if(!/product|image_1024|image_512|image_256/.test(img.src||''))return;
          a.classList.add('pcd-wrap');
          var card=a.parentElement;
          for(var i=0;i<5;i++){if(!card)break;if(card.querySelectorAll('h6,h5').length)break;card=card.parentElement;}
          var title=img.alt||(card&amp;&amp;card.querySelector('h6,h5')?card.querySelector('h6,h5').textContent.trim():'');
          var url=a.href;
          var price='';
          if(card){var all=card.querySelectorAll('*');for(var j=0;j&lt;all.length;j++){var t=all[j];if(t.children.length===0){var txt=t.textContent.trim();var m=txt.match(/\$?\s*([\d,]+\.?\d*)/);if(m&amp;&amp;parseFloat(m[1])&gt;0&amp;&amp;parseFloat(m[1])&lt;10000){price=m[1];break;}}}}
          var desc='';
          if(card){var nodes=card.querySelectorAll('span,p,div');nodes.forEach(function(el){if(el.children.length&gt;0)return;var t2=el.textContent.trim();if(t2.length&gt;desc.length&amp;&amp;t2!==title&amp;&amp;!/add to/i.test(t2)&amp;&amp;!/wishlist/i.test(t2)&amp;&amp;!/^\$/.test(t2)){desc=t2;}});}
          var btn=document.createElement('button');
          btn.className='pcd-glow-btn';btn.type='button';
          btn.innerHTML='&#128214;&nbsp;View Details';
          btn.setAttribute('aria-label','View details for '+title);
          btn.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();pcdOpen(title,desc,price,url);});
          a.appendChild(btn);
          a.addEventListener('touchstart',function(e){if(e.target===btn||btn.contains(e.target))return;if(!a.classList.contains('pcd-touch')){e.preventDefault();a.classList.add('pcd-touch');}},{passive:false});
        });
        document.addEventListener('touchstart',function(e){document.querySelectorAll('.pcd-wrap.pcd-touch').forEach(function(el){if(!el.contains(e.target))el.classList.remove('pcd-touch');});},{passive:true});
      }

      function boot(){inject();var n=0,timer=setInterval(function(){inject();if(++n&gt;=20)clearInterval(timer);},400);}
      if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',function(){setTimeout(boot,300);});}
      else{setTimeout(boot,300);}
      ['pushState','replaceState'].forEach(function(fn){var o=history[fn];history[fn]=function(){o.apply(history,arguments);setTimeout(boot,700);};});
      window.addEventListener('popstate',function(){setTimeout(boot,700);});
    })();
    </script>
  </xpath>

</t>"""

print("\nStep 4: Creating fixed inherit view...")
new_id = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'create', [{
    'name':       'LI GiftBasket - Global Hover CSS JS',
    'key':        'ligiftbasket.global_hover_css',
    'type':       'qweb',
    'mode':       'extension',
    'inherit_id': layout_id,
    'website_id': 37,
    'active':     True,
    'priority':   20,
    'arch_db':    FIXED_VIEW,
}])
print(f"  Created view ID: {new_id}")

print("""
══════════════════════════════════════════════════
  FIX COMPLETE

  The 500 error was caused by block HTML (<div>, <script>)
  being injected inside <head>. Now fixed:
    • CSS only  → <head>
    • Modal + JS → <body>

  Test:
    1. Open https://www.ligiftbasket.com
    2. Should load without 500 error
    3. Go to /shop?search=father
    4. Hover any product image → green glow button
    5. Click → description slides up
══════════════════════════════════════════════════
""")