"""
Builds celebration greeting HTML sections for all 7 Hiren Kumar stores.
Each store gets its own branded banner showing upcoming celebrations
with a countdown, discount badge, and CTA — ready to paste into Odoo
Website Builder as a Custom HTML block on the homepage.

Also writes one master HTML file per store under:
  ScrappedMaterial/<store_folder>/homepage_celebration_banner.html
"""

import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))
from build_master_celebration_sheet import build_all_days
from store_configs import STORES

TODAY = date.today()
YEAR  = 2026
BASE  = Path(r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\ScrappedMaterial")

STORE_FOLDERS = {
    "LongIslandConvenience": "01_LongIslandConvenience",
    "LongIslandBalloons":    "02_LongIslandBalloons",
    "LIGiftBasket":          "03_LIGiftBasket",
    "LongIslandPrintMail":   "04_LongIslandPrintMail",
    "LongIslandCards":       "05_LongIslandCards",
    "HirenKumar":            "06_HirenKumar",
    "ConsultCyber":          "07_ConsultCyber",
}


def get_upcoming(rows, days=90, limit=8):
    out = []
    for r in rows:
        du = r.get("Days Until")
        if isinstance(du, int) and 0 <= du <= days:
            out.append(r)
        if len(out) >= limit:
            break
    return out


def urgency_style(days_until, accent):
    if days_until == 0:
        return "#e74c3c", "TODAY!"
    if days_until <= 3:
        return "#e74c3c", f"{days_until}d left!"
    if days_until <= 7:
        return "#e67e22", f"{days_until} days"
    if days_until <= 21:
        return "#f39c12", f"{days_until} days"
    return accent, f"{days_until} days"


def build_store_html(store_key: str, store: dict, rows: list) -> str:
    upcoming = get_upcoming(rows)
    g1   = store["grad_color1"]
    g2   = store["grad_color2"]
    acc  = store["accent"]
    txt  = store["text_light"]
    domain  = store["domain"]
    name    = store["name"]
    emoji   = store["emoji"]
    tagline = store["tagline"]
    cta     = store["cta_text"]
    noun    = store["offer_noun"]
    phone   = store["phone"]
    address = store["address"]

    total_upcoming = len([r for r in rows if isinstance(r.get("Days Until"), int) and r["Days Until"] >= 0])

    # ── celebration cards ─────────────────────────────────────────────────────
    cards = ""
    for r in upcoming:
        du = r["Days Until"]
        bg_badge, label = urgency_style(du, acc)
        is_urgent = du <= 7
        card_border = f"3px solid {bg_badge}" if is_urgent else f"1px solid rgba(255,255,255,0.2)"
        cards += f"""
      <div onclick="window.location.href='/shop'" style="
          background:rgba(255,255,255,{'0.18' if not is_urgent else '0.25'});
          border:{card_border};
          border-radius:16px;
          padding:18px 12px;
          text-align:center;
          cursor:pointer;
          transition:transform .25s,box-shadow .25s;
          backdrop-filter:blur(8px);
          min-width:140px;
      "
      onmouseover="this.style.transform='translateY(-6px)';this.style.boxShadow='0 12px 30px rgba(0,0,0,.3)'"
      onmouseout="this.style.transform='none';this.style.boxShadow='none'">
        <div style="font-size:2.2rem;line-height:1">{r['Emoji']}</div>
        <div style="color:{bg_badge};font-size:.75rem;font-weight:700;margin:4px 0;
                    background:rgba(0,0,0,.25);border-radius:20px;padding:2px 8px;
                    display:inline-block;">{label}</div>
        <div style="color:{txt};font-weight:700;font-size:.82rem;margin:4px 0;line-height:1.3">{r['Event']}</div>
        <div style="background:{acc};color:#222;border-radius:12px;padding:3px 10px;
                    font-size:.78rem;font-weight:800;margin-top:6px;display:inline-block">
          {r['Discount %']}% OFF</div>
      </div>"""

    # ── ticker text ───────────────────────────────────────────────────────────
    ticker_items = " &#160;|&#160; ".join(
        f"{r['Emoji']} <b>{r['Event']}</b> — {r['Discount %']}% off (code: {r['Promo Code']})"
        for r in get_upcoming(rows, days=30, limit=6)
    )

    html = f"""<!-- =====================================================================
     {name} — Celebration Greeting Banner
     Generated: {TODAY} | Paste into Odoo Website Builder → Custom HTML
     ===================================================================== -->
<section id="celebration-banner-{store_key.lower()}" style="
    background:linear-gradient(135deg,{g1} 0%,{g2} 100%);
    font-family:'Segoe UI',Arial,sans-serif;
    overflow:hidden;
    position:relative;
">

  <!-- Ticker / scrolling alert bar -->
  <div style="background:rgba(0,0,0,.35);padding:8px 0;overflow:hidden;white-space:nowrap">
    <div style="display:inline-block;animation:ticker 40s linear infinite;color:{acc};font-size:.85rem;padding-left:100%">
      {ticker_items}
    </div>
  </div>

  <!-- Main content -->
  <div style="max-width:1200px;margin:0 auto;padding:50px 20px 40px">

    <!-- Header row -->
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:30px">
      <div>
        <div style="font-size:2rem">{emoji}</div>
        <h2 style="color:{txt};font-size:clamp(1.4rem,3vw,2.2rem);margin:6px 0;font-weight:800">
          Celebrate Every Moment
        </h2>
        <p style="color:rgba(255,255,255,.8);margin:0;font-size:.95rem">{tagline}</p>
      </div>
      <div style="background:rgba(255,255,255,.15);border-radius:16px;padding:16px 24px;text-align:center;backdrop-filter:blur(6px)">
        <div style="color:{acc};font-size:2.6rem;font-weight:800;line-height:1">{total_upcoming}</div>
        <div style="color:{txt};font-size:.85rem;margin-top:4px">celebrations this year</div>
      </div>
    </div>

    <!-- Cards row -->
    <div style="display:flex;flex-wrap:wrap;gap:14px;margin-bottom:32px;justify-content:flex-start">
      {cards}
    </div>

    <!-- CTA row -->
    <div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center">
      <a href="/shop" style="
          background:{acc};color:#111;padding:14px 32px;border-radius:50px;
          font-weight:800;font-size:1rem;text-decoration:none;
          box-shadow:0 6px 20px rgba(0,0,0,.25);transition:opacity .2s"
         onmouseover="this.style.opacity='.85'" onmouseout="this.style.opacity='1'">
        {cta} &gt;&gt;
      </a>
      <a href="/contact" style="
          color:{txt};border:2px solid rgba(255,255,255,.5);padding:12px 28px;
          border-radius:50px;font-weight:700;font-size:.95rem;text-decoration:none">
        Custom Order
      </a>
      <span style="color:rgba(255,255,255,.6);font-size:.88rem;margin-left:8px">
        📞 {phone} &nbsp;|&nbsp; 📍 {address}
      </span>
    </div>

    <p style="color:rgba(255,255,255,.5);font-size:.78rem;margin-top:18px">
      Showing next 90 days of celebrations.
      Use promo codes at checkout for instant discount.
      Free delivery on Long Island on qualifying orders.
    </p>
  </div><!-- /max-width -->

</section>

<style>
  @keyframes ticker {{
    0%   {{ transform:translateX(0) }}
    100% {{ transform:translateX(-100%) }}
  }}
  #celebration-banner-{store_key.lower()} * {{ box-sizing:border-box }}
</style>
"""
    return html


def build_all_store_htmls():
    rows = build_all_days()
    print(f"\n  Events loaded: {len(rows)}")
    upcoming = [r for r in rows if isinstance(r.get("Days Until"), int) and r["Days Until"] >= 0]
    print(f"  Upcoming events: {len(upcoming)}")

    for store_key, folder_name in STORE_FOLDERS.items():
        store = STORES[store_key]
        out_dir = BASE / folder_name
        out_dir.mkdir(parents=True, exist_ok=True)

        html = build_store_html(store_key, store, rows)
        out_file = out_dir / "homepage_celebration_banner.html"
        out_file.write_text(html, encoding="utf-8")
        print(f"  Saved: {folder_name}/homepage_celebration_banner.html  ({len(html):,} chars)")

    print(f"\n  All 7 store banners written to ScrappedMaterial/")


if __name__ == "__main__":
    build_all_store_htmls()
