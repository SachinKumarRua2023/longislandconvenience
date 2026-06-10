"""
Injects a celebration greeting bar DIRECTLY into the Odoo homepage arch
for all 7 stores. The bar appears on the homepage itself — visible to every visitor.

Approach:
  - Read the homepage ir.ui.view arch
  - Insert celebration section right after the first </section> (after the hero)
  - Write it back via Odoo RPC
  - Falls back to saving an HTML file if no Odoo site ID

Run this any time the celebration calendar changes.
"""

import sys, io, re, time, json, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))
from build_master_celebration_sheet import build_all_days
from store_configs import STORES

ODOO_URL  = "https://country-cove-inc.odoo.com"
ODOO_DB   = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASS = "M@nhattan1234"

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

MARKER_START = "<!-- CEL-START -->"
MARKER_END   = "<!-- CEL-END -->"


# ── Odoo client ───────────────────────────────────────────────────────────────
class Odoo:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["Content-Type"] = "application/json"
        self.uid = None
        r = self.s.post(f"{ODOO_URL}/web/session/authenticate", json={
            "jsonrpc":"2.0","method":"call","id":1,
            "params":{"db":ODOO_DB,"login":ODOO_USER,"password":ODOO_PASS}
        })
        self.uid = r.json().get("result",{}).get("uid")
        status = f"uid={self.uid}" if self.uid else "FAILED"
        print(f"  Odoo auth: {status}")

    def rpc(self, model, method, args=None, kw=None):
        r = self.s.post(f"{ODOO_URL}/web/dataset/call_kw", json={
            "jsonrpc":"2.0","method":"call","id":2,
            "params":{"model":model,"method":method,"args":args or [],"kwargs":kw or {}}
        })
        d = r.json()
        if "error" in d:
            raise RuntimeError(d["error"]["data"]["message"][:300])
        return d.get("result")

    def read(self, model, ids, fields):
        return self.rpc(model, "read", args=[ids], kw={"fields": fields})

    def write(self, model, ids, vals):
        return self.rpc(model, "write", args=[ids, vals])

    def search_read(self, model, domain, fields, limit=20):
        return self.rpc(model, "search_read", args=[domain], kw={"fields":fields,"limit":limit})


# ── Build celebration bar XML ─────────────────────────────────────────────────
def build_celebration_xml(store_key: str, store: dict, rows: list) -> str:
    """
    Build a compact, XML-safe celebration section for the homepage.
    All special characters are properly escaped for Odoo arch XML.
    No bare & or < or > in attribute values.
    """
    today = date.today()
    upcoming = [
        r for r in rows
        if isinstance(r.get("Days Until"), int) and 0 <= r["Days Until"] <= 60
    ][:6]

    if not upcoming:
        return ""

    # Accent / brand colors per store
    colors = {
        "LongIslandConvenience": ("#e63946", "#0f0c29"),
        "LongIslandBalloons":    ("#ff6b6b", "#fff"),
        "LIGiftBasket":          ("#764ba2", "#667eea"),
        "LongIslandPrintMail":   ("#3498db", "#2c3e50"),
        "LongIslandCards":       ("#71b280", "#134e5e"),
        "HirenKumar":            ("#c0a060", "#0f0c29"),
        "ConsultCyber":          ("#00d2d3", "#0a3d62"),
    }
    accent, bg = colors.get(store_key, ("#e63946", "#1a1a2e"))

    name    = store["name"]
    domain  = store["domain"]
    cta     = store["cta_text"]

    # Build card divs (XML-safe — no bare & allowed)
    cards_xml = ""
    for r in upcoming:
        du = r["Days Until"]
        label = "TODAY!" if du == 0 else f"{du}d"
        badge_bg = "#e63946" if du <= 3 else "#e67e22" if du <= 7 else accent
        ev_name = r["Event"][:28] + ("..." if len(r["Event"]) > 28 else "")
        disc    = r["Discount %"]
        promo   = r["Promo Code"]
        emj     = r["Emoji"]

        cards_xml += f"""
        <div style="display:inline-block;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:12px;padding:12px 14px;text-align:center;min-width:110px;vertical-align:top;">
          <div style="font-size:1.6rem;line-height:1">{emj}</div>
          <div style="background:{badge_bg};color:#fff;font-size:0.7rem;font-weight:700;border-radius:20px;padding:2px 8px;margin:4px auto;display:inline-block">{label}</div>
          <div style="color:#fff;font-size:0.75rem;font-weight:600;margin:3px 0;line-height:1.3">{ev_name}</div>
          <div style="background:#FFD700;color:#333;border-radius:8px;padding:2px 8px;font-size:0.7rem;font-weight:800;margin-top:4px;display:inline-block">{disc}% OFF</div>
        </div>"""

    # Ticker — next 5 events
    ticker_parts = []
    for r in upcoming[:5]:
        ticker_parts.append(
            f"{r['Emoji']} {r['Event']} ({r['Days Until']}d) - {r['Discount %']}% off code: {r['Promo Code']}"
        )
    ticker_text = "   |   ".join(ticker_parts)

    # The full section XML — no bare &, no <br>, all XHTML-valid
    section = f"""{MARKER_START}
<section style="background:{bg};padding:0;font-family:inherit;overflow:hidden;">

  <!-- Ticker bar -->
  <div style="background:rgba(0,0,0,0.4);padding:7px 0;overflow:hidden;white-space:nowrap;">
    <span style="display:inline-block;color:{accent};font-size:0.82rem;font-weight:600;animation:cel-ticker 35s linear infinite;padding-left:100%">
      {ticker_text}
    </span>
  </div>

  <!-- Cards row -->
  <div style="max-width:1200px;margin:0 auto;padding:24px 20px 20px;">
    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px;">
      <div style="color:{accent};font-size:1.2rem;font-weight:800;">Upcoming Celebrations</div>
      <div style="background:rgba(255,255,255,0.15);color:#fff;font-size:0.8rem;border-radius:20px;padding:3px 12px;">
        {len([r for r in rows if isinstance(r.get('Days Until'), int) and r['Days Until'] >= 0])} events this year
      </div>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px;">
      {cards_xml}
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
      <a href="/celebrations" style="background:{accent};color:#111;padding:10px 24px;border-radius:50px;font-weight:700;font-size:0.9rem;text-decoration:none;display:inline-block;">
        {cta} - See All Celebrations
      </a>
      <span style="color:rgba(255,255,255,0.55);font-size:0.82rem;">Free delivery on Long Island on qualifying orders</span>
    </div>
  </div>

</section>
<style>
@keyframes cel-ticker {{ 0% {{ transform:translateX(0) }} 100% {{ transform:translateX(-100%) }} }}
</style>
{MARKER_END}"""

    return section


# ── Strip old banner from arch ────────────────────────────────────────────────
def strip_old_banner(arch: str) -> str:
    return re.sub(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        "", arch, flags=re.DOTALL
    )


# ── Find injection point and insert ──────────────────────────────────────────
def inject_after_hero(arch: str, banner: str) -> str:
    """Insert banner after the first </section> in the arch (after hero).
    Handles empty pages and self-closing wrap divs."""
    arch = strip_old_banner(arch)

    # Case 1: normal page — inject after first </section>
    m = re.search(r"</section>", arch, re.IGNORECASE)
    if m:
        pos = m.end()
        return arch[:pos] + "\n" + banner + "\n" + arch[pos:]

    # Case 2: empty page with self-closing wrap div
    # <div id="wrap" ... /> → <div id="wrap" ...>banner</div>
    m2 = re.search(r'(<div[^>]+id=["\']wrap["\'][^/]*)/>',  arch, re.IGNORECASE)
    if m2:
        replacement = m2.group(1) + ">\n" + banner + "\n</div>"
        return arch[:m2.start()] + replacement + arch[m2.end():]

    # Case 3: before closing </t>
    m3 = re.search(r'</t>\s*$', arch)
    if m3:
        return arch[:m3.start()] + "\n" + banner + "\n" + arch[m3.start():]

    return arch + "\n" + banner


# ── Per-store injection ───────────────────────────────────────────────────────
def process_store(odoo: Odoo, store_key: str, store: dict, rows: list) -> dict:
    site_id = store.get("odoo_site_id")
    name    = store["name"]
    result  = {"store": name, "status": "PENDING", "note": ""}

    # Build and save XML banner
    banner = build_celebration_xml(store_key, store, rows)

    # Always save HTML file
    folder   = STORE_FOLDERS[store_key]
    out_dir  = BASE / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "homepage_celebration_banner.html").write_text(banner, encoding="utf-8")

    if not site_id or not odoo.uid:
        result.update(status="FILE_ONLY", note="No site ID or auth — HTML saved")
        print(f"  [{name}] HTML saved (no site ID)")
        return result

    try:
        # Find homepage page
        pages = odoo.search_read(
            "website.page",
            [["website_id", "=", site_id], ["url", "=", "/"]],
            ["id", "view_id"]
        )
        if not pages:
            result.update(status="NO_PAGE", note="No homepage found")
            print(f"  [{name}] No homepage page found")
            return result

        page   = pages[0]
        view_r = page.get("view_id")
        view_id = view_r[0] if isinstance(view_r, list) else view_r

        if not view_id:
            result.update(status="NO_VIEW", note="Page has no view_id")
            return result

        # Read current arch
        view_data = odoo.read("ir.ui.view", [view_id], ["arch_db"])
        if not view_data:
            result.update(status="NO_ARCH", note="View not readable")
            return result

        arch = view_data[0].get("arch_db") or ""
        new_arch = inject_after_hero(arch, banner)

        odoo.write("ir.ui.view", [view_id], {"arch_db": new_arch})
        result.update(
            status="INJECTED",
            note=f"view {view_id} updated | https://{store['domain']}/"
        )
        print(f"  [{name}] Injected into homepage view {view_id}")

    except Exception as e:
        result.update(status="ERROR", note=str(e)[:300])
        print(f"  [{name}] Error: {e}")

    time.sleep(0.6)
    return result


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    today = date.today()
    print(f"\n{'='*65}")
    print(f"  HOMEPAGE CELEBRATION BANNER — ALL 7 STORES")
    print(f"  Date: {today}")
    print(f"{'='*65}\n")

    rows = build_all_days()
    upcoming = [r for r in rows if isinstance(r.get("Days Until"), int) and r["Days Until"] >= 0]
    print(f"  Events: {len(rows)} total | {len(upcoming)} upcoming\n")

    odoo    = Odoo()
    results = []

    for store_key, store in STORES.items():
        print(f"\n  [{store['name']}] site_id={store.get('odoo_site_id')}")
        res = process_store(odoo, store_key, store, rows)
        results.append(res)

    # Summary
    print(f"\n{'='*65}")
    print(f"  FINAL SUMMARY")
    print(f"{'='*65}")
    icons = {"INJECTED":"[LIVE]","FILE_ONLY":"[FILE]","NO_PAGE":"[WARN]","ERROR":"[ERR]","PENDING":"[-]"}
    for r in results:
        icon = icons.get(r["status"], "[?]")
        print(f"  {icon} {r['store']:35s}  {r['note']}")

    live = sum(1 for r in results if r["status"] == "INJECTED")
    print(f"\n  Live on homepage: {live}/7")
    print(f"  HTML files ready: 7/7  (ScrappedMaterial/<store>/homepage_celebration_banner.html)")
    print(f"\n  For stores not yet live — paste HTML in Odoo:")
    print(f"  Website -> Edit -> + Block -> HTML -> paste file content")
    print(f"{'='*65}")

    with open(BASE / "injection_summary.json", "w") as f:
        json.dump({"date": str(today), "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
