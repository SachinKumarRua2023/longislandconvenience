"""
Generates the AI greeting widget JavaScript block for all 7 stores.
The widget:
  - Shows a floating chat bubble (bottom-right)
  - Auto-detects today's celebration from the built-in calendar
  - Greets visitor with a toast notification on page load
  - Opens a chat window that calls the VPS AI proxy
  - Suggests products based on store type + celebration

Output: one JS/HTML snippet per store, saved as:
  ScrappedMaterial/<store>/ai_widget.html

Run inject_ai_widget.py after this to push to Odoo.
"""

import sys, io, json
if hasattr(sys.stdout, "buffer") and not isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))
from build_master_celebration_sheet import build_all_days
from store_configs import STORES

# ── IMPORTANT: Update this to your VPS IP or domain after deploying ai_proxy_server.py
AI_PROXY_URL = "https://your-vps-domain.com:8765"  # e.g. https://142.93.12.34:8765

BASE = Path(r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\ScrappedMaterial")
STORE_FOLDERS = {
    "LongIslandConvenience": "01_LongIslandConvenience",
    "LongIslandBalloons":    "02_LongIslandBalloons",
    "LIGiftBasket":          "03_LIGiftBasket",
    "LongIslandPrintMail":   "04_LongIslandPrintMail",
    "LongIslandCards":       "05_LongIslandCards",
    "HirenKumar":            "06_HirenKumar",
    "ConsultCyber":          "07_ConsultCyber",
}

STORE_COLORS = {
    "LongIslandConvenience": {"bg": "#e63946", "fg": "#fff"},
    "LongIslandBalloons":    {"bg": "#ff6b6b", "fg": "#fff"},
    "LIGiftBasket":          {"bg": "#764ba2", "fg": "#fff"},
    "LongIslandPrintMail":   {"bg": "#3498db", "fg": "#fff"},
    "LongIslandCards":       {"bg": "#134e5e", "fg": "#FFD700"},
    "HirenKumar":            {"bg": "#302b63", "fg": "#c0a060"},
    "ConsultCyber":          {"bg": "#0a3d62", "fg": "#00d2d3"},
}


def get_today_celebration(rows: list) -> dict:
    """Return today's celebration row, or the next upcoming one."""
    today_rows = [r for r in rows if r.get("Days Until") == 0]
    if today_rows:
        return today_rows[0]
    upcoming = [r for r in rows if isinstance(r.get("Days Until"), int) and r["Days Until"] > 0]
    return upcoming[0] if upcoming else {}


def build_celebration_js_array(rows: list) -> str:
    """Build a compact JS array of next 30 celebrations for offline calendar lookup."""
    upcoming = [
        r for r in rows
        if isinstance(r.get("Days Until"), int) and 0 <= r["Days Until"] <= 365
    ][:30]
    items = []
    for r in upcoming:
        items.append({
            "d": r["Days Until"],
            "name": r["Event"][:40],
            "emoji": r["Emoji"],
            "disc": r["Discount %"],
            "code": r["Promo Code"],
        })
    return json.dumps(items)


def build_widget_html(store_key: str, store: dict, rows: list, proxy_url: str) -> str:
    col = STORE_COLORS.get(store_key, {"bg": "#e63946", "fg": "#fff"})
    bg  = col["bg"]
    fg  = col["fg"]
    name = store["name"]
    cta  = store["cta_text"]

    today_row  = get_today_celebration(rows)
    cel_name   = today_row.get("Event", "")
    cel_emoji  = today_row.get("Emoji", "🎉")
    cel_disc   = today_row.get("Discount %", 10)
    cel_code   = today_row.get("Promo Code", "")
    cel_days   = today_row.get("Days Until", -1)
    cel_array  = build_celebration_js_array(rows)

    greeting_intro = (
        f"Happy {cel_name}!" if cel_days == 0
        else f"{cel_name} is coming up in {cel_days} day{'s' if cel_days != 1 else ''}!"
        if cel_days > 0 else "Welcome!"
    )

    return f"""<!-- ============================================================
     {name} — AI Greeting Widget
     Calls: {proxy_url}
     Paste into Odoo Website Builder -> Custom HTML block
     ============================================================ -->

<div id="cel-ai-widget">

  <!-- Floating chat button -->
  <div id="cel-bubble" onclick="celToggleChat()" style="
      position:fixed;bottom:24px;right:24px;z-index:99999;
      width:56px;height:56px;border-radius:50%;
      background:{bg};color:{fg};
      display:flex;align-items:center;justify-content:center;
      font-size:1.6rem;cursor:pointer;
      box-shadow:0 4px 18px rgba(0,0,0,.35);
      transition:transform .2s;
  " onmouseover="this.style.transform='scale(1.12)'" onmouseout="this.style.transform='scale(1)'"
     title="Ask our AI assistant">
    {cel_emoji}
    <span id="cel-badge" style="
        position:absolute;top:-4px;right:-4px;
        background:#e63946;color:#fff;border-radius:50%;
        width:18px;height:18px;font-size:.65rem;font-weight:700;
        display:flex;align-items:center;justify-content:center;
    ">1</span>
  </div>

  <!-- Toast notification (auto-shows on load) -->
  <div id="cel-toast" style="
      position:fixed;bottom:92px;right:24px;z-index:99998;
      background:#fff;border-left:4px solid {bg};
      border-radius:12px;padding:14px 16px;
      box-shadow:0 6px 24px rgba(0,0,0,.18);
      max-width:270px;font-family:'Segoe UI',Arial,sans-serif;
      opacity:0;transform:translateY(20px);
      transition:opacity .4s,transform .4s;pointer-events:none;
  ">
    <div style="font-size:.7rem;color:#888;margin-bottom:4px">{name}</div>
    <div style="font-weight:700;color:#222;font-size:.9rem;margin-bottom:4px">
      {cel_emoji} {greeting_intro}
    </div>
    <div style="font-size:.82rem;color:#555">
      {'Use code <b>' + cel_code + '</b> for ' + str(cel_disc) + '% off!' if cel_code else 'Ask me for personalized suggestions!'}
    </div>
    <div onclick="document.getElementById('cel-toast').style.opacity='0'"
         style="position:absolute;top:8px;right:10px;cursor:pointer;color:#bbb;font-size:.9rem">&#10005;</div>
  </div>

  <!-- Chat window -->
  <div id="cel-chat" style="
      position:fixed;bottom:92px;right:24px;z-index:99998;
      width:330px;max-height:520px;
      background:#fff;border-radius:18px;
      box-shadow:0 8px 32px rgba(0,0,0,.22);
      font-family:'Segoe UI',Arial,sans-serif;
      display:none;flex-direction:column;overflow:hidden;
  ">
    <!-- Header -->
    <div style="background:{bg};color:{fg};padding:14px 16px;display:flex;align-items:center;justify-content:space-between;">
      <div>
        <div style="font-weight:700;font-size:.95rem">{cel_emoji} {name}</div>
        <div style="font-size:.72rem;opacity:.85">AI Shopping Assistant</div>
      </div>
      <div onclick="celToggleChat()" style="cursor:pointer;font-size:1.1rem;opacity:.8">&#10005;</div>
    </div>

    <!-- Messages area -->
    <div id="cel-messages" style="
        flex:1;overflow-y:auto;padding:12px;
        display:flex;flex-direction:column;gap:8px;
        max-height:330px;
    "></div>

    <!-- Input row -->
    <div style="padding:10px 12px;border-top:1px solid #f0f0f0;display:flex;gap:8px;">
      <input id="cel-input" type="text" placeholder="Ask about products..."
             onkeydown="if(event.key==='Enter')celSend()"
             style="flex:1;border:1px solid #ddd;border-radius:20px;padding:8px 14px;
                    font-size:.85rem;outline:none;font-family:inherit;">
      <button onclick="celSend()" style="
          background:{bg};color:{fg};border:none;border-radius:50%;
          width:36px;height:36px;cursor:pointer;font-size:1rem;
          display:flex;align-items:center;justify-content:center;
      ">&#9658;</button>
    </div>
    <div style="text-align:center;font-size:.65rem;color:#ccc;padding:4px 0 8px">
      Powered by AI &#183; {name}
    </div>
  </div>

</div>

<script>
(function() {{
  var PROXY = "{proxy_url}";
  var STORE = "{store_key}";
  var CEL_DATA = {cel_array};

  // Find today's celebration from data
  function todayCel() {{
    for (var i = 0; i < CEL_DATA.length; i++) {{
      if (CEL_DATA[i].d === 0) return CEL_DATA[i];
    }}
    return CEL_DATA[0] || {{name:"", emoji:"🎉", disc:10, code:""}};
  }}

  var cel = todayCel();
  var chatHistory = [];
  var chatOpen = false;
  var greeted = false;

  // Show toast after 2.5s
  setTimeout(function() {{
    var t = document.getElementById("cel-toast");
    if (t) {{ t.style.opacity="1"; t.style.transform="translateY(0)"; t.style.pointerEvents="auto"; }}
    setTimeout(function() {{
      if (t) t.style.opacity="0";
    }}, 7000);
  }}, 2500);

  window.celToggleChat = function() {{
    chatOpen = !chatOpen;
    var chat  = document.getElementById("cel-chat");
    var toast = document.getElementById("cel-toast");
    var badge = document.getElementById("cel-badge");
    if (chat)  chat.style.display  = chatOpen ? "flex" : "none";
    if (toast) toast.style.opacity = "0";
    if (badge) badge.style.display = "none";
    if (chatOpen && !greeted) {{ celAutoGreet(); greeted = true; }}
    if (chatOpen) {{ setTimeout(function(){{var inp=document.getElementById("cel-input");if(inp)inp.focus();}},100); }}
  }};

  function celAutoGreet() {{
    var msg = cel.name
      ? "Hello! " + cel.emoji + " " + (cel.d===0 ? "Happy " + cel.name + "!" : cel.name + " is in " + cel.d + " days!") + " What would you like to find today?"
      : "Hello! Welcome to {name}. How can I help you today?";
    celAppendMessage("assistant", msg);
    chatHistory.push({{role:"assistant", content:msg}});
  }}

  window.celSend = function() {{
    var inp = document.getElementById("cel-input");
    if (!inp || !inp.value.trim()) return;
    var txt = inp.value.trim();
    inp.value = "";
    celAppendMessage("user", txt);
    chatHistory.push({{role:"user", content:txt}});
    celFetch(txt);
  }};

  function celFetch(userMsg) {{
    var typing = celAppendMessage("assistant", "...", true);
    fetch(PROXY + "/ai-chat", {{
      method: "POST",
      headers: {{"Content-Type":"application/json"}},
      body: JSON.stringify({{
        store: STORE,
        celebration: cel.name || "",
        emoji: cel.emoji || "🎉",
        message: userMsg,
        history: chatHistory.slice(-8)
      }})
    }})
    .then(function(r){{ return r.json(); }})
    .then(function(d){{
      if (typing) typing.remove();
      var reply = d.reply || d.error || "Sorry, I couldn't connect right now.";
      celAppendMessage("assistant", reply);
      chatHistory.push({{role:"assistant", content:reply}});
    }})
    .catch(function(){{
      if (typing) typing.remove();
      celAppendMessage("assistant", "Sorry, the assistant is temporarily unavailable. Please call us or browse the shop!");
    }});
  }}

  function celAppendMessage(role, text, isTyping) {{
    var msgs = document.getElementById("cel-messages");
    if (!msgs) return null;
    var div = document.createElement("div");
    div.style.cssText = "max-width:85%;padding:9px 13px;border-radius:14px;font-size:.84rem;line-height:1.4;" +
      (role==="user"
        ? "background:{bg};color:{fg};align-self:flex-end;border-bottom-right-radius:4px;"
        : "background:#f4f4f4;color:#222;align-self:flex-start;border-bottom-left-radius:4px;");
    div.textContent = text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }}
}})();
</script>"""


def build_all_widgets():
    rows = build_all_days()
    today = date.today()
    print(f"\nBuilding AI widgets for {today} ...")
    print(f"Events loaded: {len(rows)}\n")

    saved = []
    for store_key, folder_name in STORE_FOLDERS.items():
        store   = STORES[store_key]
        html    = build_widget_html(store_key, store, rows, AI_PROXY_URL)
        out_dir = BASE / folder_name
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "ai_widget.html"
        out_file.write_text(html, encoding="utf-8")
        print(f"  Saved: {folder_name}/ai_widget.html  ({len(html):,} chars)")
        saved.append(str(out_file))

    print(f"\nAll 7 AI widget files written to ScrappedMaterial/")
    print(f"\nNEXT STEPS:")
    print(f"  1. Deploy ai_proxy_server.py on your VPS")
    print(f"  2. Update AI_PROXY_URL in this file to your VPS domain/IP")
    print(f"  3. Run inject_ai_widget.py to push widgets to all Odoo homepages")
    return saved


if __name__ == "__main__":
    build_all_widgets()
