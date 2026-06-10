"""
Builds the LI Gift Basket Odoo homepage celebration section.
- Creates a "Celebrations Calendar" section on the website
- Shows upcoming holidays with countdown timers and offer banners
- Generates 365-day Excel calendar with all celebration dates
- Sets up promotional records in Odoo for each celebration
"""

import sys
import os
import json
import time
import requests
import pandas as pd
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from celebrations_data import get_all_celebrations, get_message_for_celebration

# ── Odoo Config ──────────────────────────────────────────────────────────────
ODOO_URL = "https://country-cove-inc.odoo.com"
ODOO_DB = "country-cove-inc"
ODOO_EMAIL = "countrycoveinc@gmail.com"
ODOO_PASSWORD = "M@nhattan1234"

# LI Gift Basket website ID in Odoo
GIFTBASKET_WEBSITE_ID = 14

# Output
OUTPUT_DIR = Path(r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\ScrappedMaterial\03_LIGiftBasket")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class OdooClient:
    def __init__(self, url, db, email, password):
        self.url = url.rstrip("/")
        self.db = db
        self.uid = None
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._login(email, password)

    def _login(self, email, password):
        resp = self.session.post(f"{self.url}/web/session/authenticate", json={
            "jsonrpc": "2.0", "method": "call", "id": 1,
            "params": {"db": self.db, "login": email, "password": password}
        })
        result = resp.json().get("result", {})
        self.uid = result.get("uid")
        if self.uid:
            print(f"  Odoo login OK (uid={self.uid})")
        else:
            print("  Odoo login FAILED — check credentials")

    def call(self, model, method, args=None, kwargs=None):
        payload = {
            "jsonrpc": "2.0", "method": "call", "id": 2,
            "params": {
                "model": model,
                "method": method,
                "args": args or [],
                "kwargs": kwargs or {},
            }
        }
        resp = self.session.post(f"{self.url}/web/dataset/call_kw", json=payload)
        data = resp.json()
        if "error" in data:
            print(f"  Odoo error: {data['error']}")
            return None
        return data.get("result")


def generate_celebration_excel(year: int = 2026):
    """Generate a full 365-day celebration calendar Excel file."""
    print(f"\n[1] Generating {year} Celebration Calendar Excel...")
    celebrations = get_all_celebrations(year)

    today = date.today()
    rows = []
    for c in celebrations:
        d = c.get("date")
        days_left = (d - today).days if d else None
        rows.append({
            "Date": d.strftime("%B %d, %Y") if d else "",
            "Day of Week": d.strftime("%A") if d else "",
            "Celebration": c.get("name", ""),
            "Category": c.get("category", ""),
            "Emoji": c.get("emoji", ""),
            "Discount %": c.get("discount", 0),
            "Days Until (from today)": days_left if days_left is not None else "",
            "Status": "UPCOMING" if (days_left is not None and days_left >= 0) else "PAST",
            "Promo Code": (c.get("name", "").upper().replace(" ", "")[:8] + str(year)[-2:]),
            "Theme": c.get("theme", ""),
            "Alert 7-day?": "YES" if (days_left is not None and 0 <= days_left <= 7) else "",
            "Alert 14-day?": "YES" if (days_left is not None and 0 <= days_left <= 14) else "",
        })

    df = pd.DataFrame(rows)

    # Split into sheets by category
    excel_path = OUTPUT_DIR / f"celebration_calendar_{year}.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        # All celebrations
        df.to_excel(writer, sheet_name="All Celebrations", index=False)

        # Upcoming only
        upcoming = df[df["Status"] == "UPCOMING"]
        upcoming.to_excel(writer, sheet_name="Upcoming", index=False)

        # By category
        for cat in df["Category"].unique():
            cat_df = df[df["Category"] == cat]
            sheet_name = cat[:31]
            cat_df.to_excel(writer, sheet_name=sheet_name, index=False)

        # 7-day alerts
        alerts = df[df["Alert 7-day?"] == "YES"]
        if not alerts.empty:
            alerts.to_excel(writer, sheet_name="7-Day Alerts", index=False)

    print(f"  Excel saved: {excel_path}")
    print(f"  Total celebrations in {year}: {len(celebrations)}")
    upcoming_count = len([c for c in celebrations if c.get("date") and c["date"] >= today])
    print(f"  Upcoming this year: {upcoming_count}")
    return celebrations, excel_path


def generate_email_whatsapp_templates(celebrations: list, year: int = 2026):
    """Generate all email + WhatsApp templates for each celebration."""
    print(f"\n[2] Generating Email & WhatsApp templates...")
    today = date.today()
    templates = []

    for c in celebrations:
        d = c.get("date")
        if not d or d < today:
            continue
        days_until = (d - today).days
        msgs = get_message_for_celebration(c, customer_name="[Customer Name]", days_until=days_until, year=year)
        templates.append({
            "date": d.strftime("%Y-%m-%d"),
            "celebration": c["name"],
            "category": c["category"],
            "emoji": c.get("emoji", ""),
            "days_until": days_until,
            "discount": c.get("discount", 10),
            "email_subject": msgs["subject"],
            "email_body": msgs["email_body"],
            "whatsapp_message": msgs["whatsapp_message"],
            "promo_code": (c["name"].upper().replace(" ", "")[:8] + str(year)[-2:]),
            "send_7_days_before": (d - timedelta(days=7)).strftime("%Y-%m-%d"),
            "send_3_days_before": (d - timedelta(days=3)).strftime("%Y-%m-%d"),
            "send_1_day_before": (d - timedelta(days=1)).strftime("%Y-%m-%d"),
        })

    # Save as Excel
    df = pd.DataFrame(templates)
    tmpl_path = OUTPUT_DIR / "email_whatsapp_templates.xlsx"
    df.to_excel(tmpl_path, index=False, engine="openpyxl")
    print(f"  Templates saved: {tmpl_path} ({len(templates)} celebrations)")

    # Also save as JSON for n8n import
    json_path = OUTPUT_DIR / "celebration_templates.json"
    with open(json_path, "w") as f:
        json.dump(templates, f, indent=2, default=str)
    print(f"  JSON saved: {json_path}")

    return templates


def create_odoo_promotions(odoo: OdooClient, celebrations: list, year: int = 2026):
    """Create Odoo promotional pricelist entries for major celebrations."""
    print(f"\n[3] Creating Odoo promotions for major celebrations...")
    today = date.today()
    major_cats = ["Major Holiday", "Federal Holiday", "Shopping"]
    major = [c for c in celebrations if c.get("category") in major_cats and
             c.get("date") and c["date"] >= today][:15]

    created = 0
    for c in major:
        d = c["date"]
        discount = c.get("discount", 10)
        promo_name = f"{c['name']} {year} — {discount}% Off Gift Baskets"
        code = (c["name"].upper().replace(" ", "")[:8] + str(year)[-2:])

        # Create coupon program in Odoo
        try:
            promo_id = odoo.call(
                "loyalty.program", "create",
                args=[{
                    "name": promo_name,
                    "program_type": "promotion",
                    "applies_on": "current",
                    "trigger": "auto",
                    "reward_ids": [(0, 0, {
                        "reward_type": "discount",
                        "discount": discount,
                        "discount_mode": "percent",
                        "discount_applicability": "order",
                    })],
                }]
            )
            if promo_id:
                created += 1
                print(f"  Created promo: {promo_name} (ID={promo_id})")
        except Exception as e:
            print(f"  Skip promo for {c['name']}: {e}")
        time.sleep(0.5)

    print(f"  Created {created} Odoo promotions")
    return created


def build_homepage_celebration_html(celebrations: list, year: int = 2026) -> str:
    """
    Build HTML/CSS for the LI Gift Basket homepage celebration section.
    This gets pasted into the Odoo website builder as a custom HTML block.
    """
    today = date.today()
    upcoming = [c for c in celebrations if c.get("date") and 0 <= (c["date"] - today).days <= 90][:12]

    cards_html = ""
    for c in upcoming:
        d = c["date"]
        days_left = (d - today).days
        urgency_class = "urgent" if days_left <= 7 else "soon" if days_left <= 21 else "coming"
        urgency_label = "🔥 This Week!" if days_left <= 7 else f"{days_left} days away"

        cards_html += f"""
        <div class="celebration-card {urgency_class}">
            <div class="celebration-emoji">{c.get('emoji', '🎁')}</div>
            <div class="celebration-date">{d.strftime("%b %d")}</div>
            <div class="celebration-name">{c['name']}</div>
            <div class="celebration-urgency">{urgency_label}</div>
            <div class="celebration-discount">{c.get('discount', 10)}% OFF</div>
            <a href="/shop?celebration={c.get('theme', 'default')}" class="celebration-btn">Shop Now</a>
        </div>"""

    html = f"""
<!-- LI Gift Basket — Celebration Calendar Section -->
<!-- Generated: {datetime.now().strftime('%Y-%m-%d')} | Paste into Odoo Website Builder -->
<section id="celebration-calendar" style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 60px 20px;
    text-align: center;
    font-family: 'Poppins', sans-serif;
">
    <div style="max-width: 1200px; margin: 0 auto;">
        <h2 style="color: #fff; font-size: 2.5em; margin-bottom: 10px; font-weight: 700;">
            🎁 Celebrate Every Moment
        </h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2em; margin-bottom: 40px;">
            Long Island's favorite gift baskets — for every celebration, every day of the year
        </p>

        <!-- Celebration Counter -->
        <div style="background: rgba(255,255,255,0.15); border-radius: 20px; padding: 20px; margin-bottom: 40px; display: inline-block;">
            <span style="color: #FFD700; font-size: 3em; font-weight: 700;">{len(upcoming)}</span>
            <span style="color: #fff; font-size: 1.1em; margin-left: 10px;">Celebrations in the next 90 days!</span>
        </div>

        <!-- Celebration Cards Grid -->
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        ">
        {''.join([f"""
            <div style="
                background: {'rgba(255,69,58,0.9)' if (c['date']-today).days<=7 else 'rgba(255,255,255,0.15)'};
                border-radius: 16px;
                padding: 20px 15px;
                backdrop-filter: blur(10px);
                border: 2px solid {'#FFD700' if (c['date']-today).days<=7 else 'rgba(255,255,255,0.3)'};
                transition: transform 0.3s;
                cursor: pointer;
            " onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 2.5em;">{c.get('emoji','🎁')}</div>
                <div style="color: #FFD700; font-weight: 700; font-size: 0.85em; margin: 5px 0;">{c['date'].strftime('%b %d')}</div>
                <div style="color: #fff; font-weight: 600; font-size: 0.9em; line-height: 1.3;">{c['name']}</div>
                <div style="background: #FFD700; color: #333; border-radius: 20px; padding: 4px 12px; font-size: 0.8em; font-weight: 700; margin: 8px auto; display: inline-block;">{c.get('discount',10)}% OFF</div>
            </div>""" for c in upcoming])}
        </div>

        <!-- CTA -->
        <div>
            <a href="/shop" style="
                background: #FFD700;
                color: #333;
                padding: 16px 40px;
                border-radius: 50px;
                font-size: 1.2em;
                font-weight: 700;
                text-decoration: none;
                display: inline-block;
                margin: 10px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            ">🛍️ Shop Gift Baskets</a>
            <a href="/contact" style="
                background: transparent;
                color: #fff;
                padding: 16px 40px;
                border-radius: 50px;
                font-size: 1.2em;
                font-weight: 700;
                text-decoration: none;
                display: inline-block;
                margin: 10px;
                border: 2px solid #fff;
            ">📞 Custom Order</a>
        </div>

        <p style="color: rgba(255,255,255,0.7); margin-top: 20px; font-size: 0.9em;">
            🚚 Free delivery across Nassau & Suffolk County on orders $60+ | 📍 Plainview, Long Island, NY
        </p>
    </div>
</section>
"""
    return html


def inject_to_odoo_website(odoo: OdooClient, html_content: str):
    """Inject the celebration section into Odoo website as a snippet/page block."""
    print("\n[4] Injecting celebration section into Odoo LI Gift Basket website...")

    # Find the homepage of website 14
    pages = odoo.call("website.page", "search_read",
                      args=[[["website_id", "=", GIFTBASKET_WEBSITE_ID], ["url", "=", "/"]]],
                      kwargs={"fields": ["id", "name", "arch", "url"]})

    if not pages:
        print("  Homepage not found — searching for any page on website 14...")
        pages = odoo.call("website.page", "search_read",
                          args=[[["website_id", "=", GIFTBASKET_WEBSITE_ID]]],
                          kwargs={"fields": ["id", "name", "url"], "limit": 5})
        if pages:
            for p in pages:
                print(f"    Found page: ID={p['id']} | {p['url']}")
        return

    page = pages[0]
    print(f"  Found homepage: ID={page['id']}")

    # Save HTML block for manual insertion
    html_file = OUTPUT_DIR / "celebration_section_homepage.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  HTML block saved: {html_file}")
    print("  → In Odoo Website Builder: Add > HTML Block > paste this file's content")


def main():
    year = 2026
    print(f"\n{'='*65}")
    print(f"  LI GIFT BASKET — CELEBRATION CALENDAR & AUTO-GREETING SYSTEM")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*65}")

    # Step 1: Generate full year calendar
    celebrations, excel_path = generate_celebration_excel(year)
    print(f"\n  RESULT: {len(celebrations)} total celebration days found for {year}!")

    # Step 2: Generate all email + WhatsApp templates
    templates = generate_email_whatsapp_templates(celebrations, year)

    # Step 3: Build homepage HTML
    print(f"\n[3] Building homepage celebration section HTML...")
    html = build_homepage_celebration_html(celebrations, year)
    print("  HTML block generated")

    # Step 4: Connect to Odoo and inject
    try:
        odoo = OdooClient(ODOO_URL, ODOO_DB, ODOO_EMAIL, ODOO_PASSWORD)
        if odoo.uid:
            inject_to_odoo_website(odoo, html)
            create_odoo_promotions(odoo, celebrations, year)
        else:
            print("  Odoo not available — saving files locally only")
            html_file = OUTPUT_DIR / "celebration_section_homepage.html"
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  HTML saved: {html_file}")
    except Exception as e:
        print(f"  Odoo step skipped: {e}")
        html_file = OUTPUT_DIR / "celebration_section_homepage.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)

    # Summary
    today = date.today()
    upcoming_7 = [c for c in celebrations if c.get("date") and 0 <= (c["date"] - today).days <= 7]
    upcoming_30 = [c for c in celebrations if c.get("date") and 0 <= (c["date"] - today).days <= 30]

    print(f"\n{'='*65}")
    print(f"  SUMMARY")
    print(f"{'='*65}")
    print(f"  Total 2026 celebrations mapped:  {len(celebrations)}")
    print(f"  Upcoming in next 7 days:         {len(upcoming_7)}")
    print(f"  Upcoming in next 30 days:        {len(upcoming_30)}")
    print(f"  Email templates generated:       {len(templates)}")
    print(f"\n  FILES CREATED:")
    print(f"  📊 {OUTPUT_DIR / f'celebration_calendar_{year}.xlsx'}")
    print(f"  📧 {OUTPUT_DIR / 'email_whatsapp_templates.xlsx'}")
    print(f"  📱 {OUTPUT_DIR / 'celebration_templates.json'}")
    print(f"  🌐 {OUTPUT_DIR / 'celebration_section_homepage.html'}")
    print(f"\n  NEXT STEPS:")
    print(f"  1. Open celebration_section_homepage.html → paste into Odoo Website Builder")
    print(f"  2. Import celebration_templates.json into n8n workflow (see n8n_workflow.json)")
    print(f"  3. Configure Gmail/Twilio in n8n for automated sends")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
