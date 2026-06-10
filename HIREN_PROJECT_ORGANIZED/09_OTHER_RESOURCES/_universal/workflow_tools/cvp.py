import xmlrpc.client, sys

sys.stdout.reconfigure(encoding='utf-8')
URL = 'https://country-cove-inc.odoo.com'
DB  = 'country-cove-inc'
UID = 2
PW  = 'M@nhattan1234'

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
print("Connected\n")

# Homepage view 600 = Long Island Convenience (site 1)
HP_VIEW_ID = 600

# Read current arch
arch = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'read',
                         [[HP_VIEW_ID]], {'fields': ['arch_db']})[0]['arch_db']
print(f"Read view {HP_VIEW_ID}: {len(arch)} chars")

# ─────────────────────────────────────────────────────────────
# KEY FIXES vs previous attempts:
# 1. NO <!-- --> comment markers with -- inside them
# 2. NO &mdash; or special entities that expand to --
# 3. JS wrapped in CDATA so < > & are safe
# 4. Marker uses single dashes only: <!- CONV_POPUP_START ->
#    Actually: use a plain div id as marker, no XML comments at all
# ─────────────────────────────────────────────────────────────

CONV_EVENTS = [
    {"year":2026,"month":6, "day":15,"name":"Father's Day",    "emoji":"👔", "color":"#2d6a4f","msg":"Grab snacks and drinks for Dad!",      "cta":"Shop Now",       "url":"/shop"},
    {"year":2026,"month":6, "day":19,"name":"Juneteenth",      "emoji":"✊", "color":"#c1121f","msg":"Stock up for the celebration!",        "cta":"Shop Now",       "url":"/shop"},
    {"year":2026,"month":7, "day":4, "name":"Independence Day","emoji":"🇺🇸","color":"#e63946","msg":"BBQ snacks, drinks and party supplies!","cta":"Shop 4th July",  "url":"/shop"},
    {"year":2026,"month":8, "day":28,"name":"Back to School",  "emoji":"✏️","color":"#f4a261","msg":"Snacks and essentials for school!",     "cta":"Shop Now",       "url":"/shop"},
    {"year":2026,"month":9, "day":7, "name":"Labor Day",       "emoji":"⚒️","color":"#457b9d","msg":"Long weekend essentials stocked up!",   "cta":"Shop Now",       "url":"/shop"},
    {"year":2026,"month":10,"day":31,"name":"Halloween",       "emoji":"🎃","color":"#e76f51","msg":"Candy, drinks and spooky snacks!",      "cta":"Shop Halloween", "url":"/shop"},
    {"year":2026,"month":11,"day":26,"name":"Thanksgiving",    "emoji":"🦃","color":"#ca6702","msg":"Holiday snacks and party essentials!",  "cta":"Shop Now",       "url":"/shop"},
    {"year":2026,"month":12,"day":25,"name":"Christmas",       "emoji":"🎄","color":"#c1121f","msg":"Holiday treats, drinks and gifts!",     "cta":"Shop Now",       "url":"/shop"},
]

import json
events_json = json.dumps(CONV_EVENTS)

# Build popup - NO XML comments with double-hyphens, NO &mdash;
# Use a wrapper div with id="conv-popup-block" as our marker
POPUP = f"""<div id="conv-popup-block">
<div id="cel-splash-overlay" style="display:none;position:fixed;inset:0;z-index:999999;background:rgba(0,0,0,.75);justify-content:center;align-items:center;padding:16px;box-sizing:border-box;opacity:0;transition:opacity .4s ease;">
  <div id="cel-splash-card" style="background:#fff;border-radius:24px;max-width:800px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 24px 80px rgba(0,0,0,.6);transform:scale(.2);opacity:0;transition:transform .65s cubic-bezier(.34,1.56,.64,1),opacity .4s ease;position:relative;">
    <div style="background:linear-gradient(135deg,#c1121f,#f4a261);padding:28px 28px 20px;text-align:center;border-radius:24px 24px 0 0;position:relative;">
      <button onclick="window._closeCelSplash()" style="position:absolute;top:14px;right:16px;background:rgba(255,255,255,.25);border:none;color:#fff;font-size:1.3rem;width:34px;height:34px;border-radius:50%;cursor:pointer;font-weight:900;">&#10005;</button>
      <div style="font-size:2.2rem;margin-bottom:6px;">&#127881;</div>
      <h2 style="font-size:clamp(1.3rem,4vw,1.9rem);font-weight:900;color:#fff;margin:0 0 6px;text-shadow:0 2px 8px rgba(0,0,0,.3);">Upcoming Celebrations!</h2>
      <p style="color:rgba(255,255,255,.9);font-size:.95rem;margin:0;">Stock up at Long Island Convenience for these special dates!</p>
    </div>
    <div id="cel-splash-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;padding:24px 22px 10px;"></div>
    <div style="margin:0 22px 20px;height:5px;background:#eee;border-radius:3px;overflow:hidden;">
      <div id="cel-splash-bar" style="height:100%;width:100%;background:linear-gradient(90deg,#c1121f,#f4a261);border-radius:3px;transition:none;"></div>
    </div>
  </div>
</div>
<style>
.csp-card{{border-radius:14px;padding:16px 12px;text-align:center;text-decoration:none;display:block;transition:transform .2s,box-shadow .2s;border:2px solid transparent;}}
.csp-card:hover{{transform:translateY(-4px);box-shadow:0 10px 28px rgba(0,0,0,.18);}}
@keyframes csp-fall{{0%{{transform:translateY(-30px) rotate(0deg);opacity:1;}}100%{{transform:translateY(110vh) rotate(760deg);opacity:0;}}}}
.csp-confetti{{position:fixed;pointer-events:none;z-index:1000000;animation:csp-fall linear forwards;}}
</style>
<script>
//<![CDATA[
(function() {{
  var EVENTS = {events_json};
  var COLORS = ['#c1121f','#f4a261','#e74c3c','#3498db','#2ecc71','#9b59b6','#e67e22','#1abc9c'];
  var _shown = false;
  var _autoClose;

  function isHomepage() {{
    var p = window.location.pathname.replace(/\/+$/, '') || '/';
    return p === '' || p === '/';
  }}

  function getUpcoming() {{
    var today = new Date(); today.setHours(0,0,0,0);
    return EVENTS.map(function(e) {{
      var d = new Date(e.year, e.month-1, e.day);
      var days = Math.ceil((d - today) / 86400000);
      return Object.assign({{}}, e, {{days: days}});
    }}).filter(function(e) {{ return e.days >= 0 && e.days <= 120; }})
      .sort(function(a,b) {{ return a.days - b.days; }})
      .slice(0, 4);
  }}

  function buildGrid(upcoming) {{
    var grid = document.getElementById('cel-splash-grid');
    if (!grid) return false;
    grid.innerHTML = '';
    upcoming.forEach(function(e) {{
      var urgency = e.days === 0 ? '&#128293; TODAY!'
                  : e.days <= 3  ? '&#128293; ' + e.days + ' day' + (e.days > 1 ? 's' : '') + '!'
                  : e.days <= 10 ? '&#9889; ' + e.days + ' days!'
                  : e.days + ' days away';
      var uc = e.days <= 10 ? '#e63946' : e.color;
      var a = document.createElement('a');
      a.className = 'csp-card';
      a.href = e.url;
      a.style.cssText = 'background:' + e.color + '15;border-color:' + e.color + '45;';
      a.innerHTML =
        '<div style="font-size:2.2rem;margin-bottom:7px">' + e.emoji + '</div>' +
        '<div style="font-weight:800;font-size:.88rem;color:#1a1a2e;margin-bottom:4px;line-height:1.3">' + e.name + '</div>' +
        '<div style="font-size:1.15rem;font-weight:900;color:' + uc + ';margin-bottom:5px">' + urgency + '</div>' +
        '<div style="font-size:.72rem;color:#666;line-height:1.4;margin-bottom:10px">' + e.msg + '</div>' +
        '<span style="display:inline-block;padding:7px 16px;border-radius:20px;font-size:.75rem;font-weight:800;color:#fff;background:' + e.color + ';letter-spacing:.03em">' + e.cta + '</span>';
      grid.appendChild(a);
    }});
    return true;
  }}

  function launchConfetti() {{
    for (var i = 0; i < 60; i++) {{
      (function(idx) {{
        var el = document.createElement('div');
        el.className = 'csp-confetti';
        var size = 6 + Math.round(Math.random() * 8);
        el.style.cssText = [
          'left:' + (Math.random() * 100) + 'vw',
          'top:-20px',
          'width:' + size + 'px',
          'height:' + size + 'px',
          'background:' + COLORS[idx % COLORS.length],
          'border-radius:' + (Math.random() > .5 ? '50%' : '2px'),
          'animation-duration:' + (2.2 + Math.random() * 3.5) + 's',
          'animation-delay:' + (Math.random() * 1.5) + 's',
        ].join(';');
        document.body.appendChild(el);
        setTimeout(function() {{ try {{ el.parentNode.removeChild(el); }} catch(x) {{}} }}, 6000);
      }})(i);
    }}
  }}

  window._closeCelSplash = function() {{
    clearTimeout(_autoClose);
    var o = document.getElementById('cel-splash-overlay');
    var c = document.getElementById('cel-splash-card');
    if (c) {{ c.style.transform = 'scale(.85)'; c.style.opacity = '0'; }}
    if (o) {{
      setTimeout(function() {{ o.style.opacity = '0'; }}, 180);
      setTimeout(function() {{ o.style.display = 'none'; }}, 550);
    }}
  }};

  function showPopup() {{
    if (_shown) return;
    if (!isHomepage()) return;
    var upcoming = getUpcoming();
    if (!upcoming.length) return;
    var overlay = document.getElementById('cel-splash-overlay');
    var card = document.getElementById('cel-splash-card');
    if (!overlay || !card) return;
    if (!buildGrid(upcoming)) return;
    _shown = true;
    overlay.style.display = 'flex';
    void overlay.offsetWidth;
    overlay.style.opacity = '1';
    setTimeout(function() {{ card.style.transform = 'scale(1)'; card.style.opacity = '1'; }}, 80);
    launchConfetti();
    var bar = document.getElementById('cel-splash-bar');
    if (bar) {{
      bar.style.transition = 'none';
      bar.style.width = '100%';
      setTimeout(function() {{
        bar.style.transition = 'width 11.5s linear';
        void bar.offsetWidth;
        bar.style.width = '0%';
      }}, 750);
    }}
    _autoClose = setTimeout(window._closeCelSplash, 12500);
  }}

  function pollUntilReady() {{
    if (_shown) return;
    if (!isHomepage()) return;
    if (document.getElementById('cel-splash-overlay') && document.getElementById('cel-splash-grid')) {{
      showPopup();
    }} else {{
      setTimeout(pollUntilReady, 250);
    }}
  }}

  function initTrigger() {{ setTimeout(pollUntilReady, 600); }}

  if (document.readyState === 'complete' || document.readyState === 'interactive') {{
    initTrigger();
  }} else {{
    document.addEventListener('DOMContentLoaded', initTrigger);
    window.addEventListener('load', initTrigger);
  }}

  (function() {{
    var lastPath = window.location.pathname;
    function onNav() {{
      var np = window.location.pathname;
      if (np !== lastPath) {{
        lastPath = np; _shown = false;
        clearTimeout(_autoClose);
        setTimeout(pollUntilReady, 600);
      }}
    }}
    window.addEventListener('popstate', onNav);
    var _push = history.pushState;
    history.pushState = function() {{ _push.apply(history, arguments); onNav(); }};
    var _rep = history.replaceState;
    history.replaceState = function() {{ _rep.apply(history, arguments); onNav(); }};
  }})();
}})();
//]]>
</script>
</div>"""

# Remove existing popup block if present
MARKER = 'id="conv-popup-block"'
if MARKER in arch:
    # Find the wrapping <div id="conv-popup-block"> ... </div>
    start = arch.index('<div id="conv-popup-block">')
    # Find matching closing </div> by counting depth
    pos = start + len('<div id="conv-popup-block">')
    depth = 1
    while depth > 0 and pos < len(arch):
        next_open  = arch.find('<div', pos)
        next_close = arch.find('</div>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    arch = arch[:start] + arch[pos:]
    print("  Removed existing popup block.")

# Inject before closing </t>
if arch.rstrip().endswith('</t>'):
    arch_new = arch.rstrip()[:-4] + '\n' + POPUP + '\n</t>'
elif arch.rstrip().endswith('</template>'):
    arch_new = arch.rstrip()[:-11] + '\n' + POPUP + '\n</template>'
else:
    arch_new = arch.rstrip() + '\n' + POPUP

print("Injecting popup into view 600...")
res = models.execute_kw(DB, UID, PW, 'ir.ui.view', 'write',
                        [[HP_VIEW_ID], {'arch_db': arch_new}])
print(f"View {HP_VIEW_ID} updated: {res}")

print("""
==============================================
  CONVENIENCE POPUP LIVE

  Test:
    1. Visit https://www.longislandconvenience.com
    2. Hard refresh: Ctrl+Shift+R
    3. Popup fires within 1 second with confetti
==============================================
""")