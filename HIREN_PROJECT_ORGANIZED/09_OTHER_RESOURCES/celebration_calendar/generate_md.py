"""
Generates CELEBRATIONS.md — complete list of all 156+ celebration days
organized by month, with auto-greeting text for email and WhatsApp.
One file covers all 7 Hiren Kumar stores.
"""

import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))
from build_master_celebration_sheet import build_all_days

TODAY = date.today()
YEAR = 2026

# Per-store offer mapping: category → what each store offers
STORE_OFFERS = {
    "LongIslandConvenience": {
        "name": "Long Island Convenience",
        "domain": "longislandconvenience.com",
        "emoji": "🏪",
        "tagline": "Your neighborhood store — open every day",
        "offer_suffix": "snacks, drinks & everyday essentials on sale",
    },
    "LongIslandBalloons": {
        "name": "Long Island Balloons Decor",
        "domain": "longislandballoonsdecor.com",
        "emoji": "🎈",
        "tagline": "Balloon decorations & party setups — Long Island",
        "offer_suffix": "balloon arrangements & party decoration packages",
    },
    "LIGiftBasket": {
        "name": "LI Gift Basket",
        "domain": "ligiftbasket.com",
        "emoji": "🎁",
        "tagline": "Curated gift baskets — Plainview, Long Island NY",
        "offer_suffix": "curated gift baskets & custom orders",
    },
    "LongIslandPrintMail": {
        "name": "Long Island Print & Mail",
        "domain": "longislandprintandmail.org",
        "emoji": "🖨️",
        "tagline": "Printing, banners & mailing — Long Island",
        "offer_suffix": "custom cards, banners & printed invitations",
    },
    "LongIslandCards": {
        "name": "Long Island Card",
        "domain": "longislandcard.com",
        "emoji": "🃏",
        "tagline": "Sports cards, collectibles & greeting cards",
        "offer_suffix": "sports cards, collectibles & greeting cards",
    },
    "HirenKumar": {
        "name": "Hiren Kumar Advisory",
        "domain": "hirenkumar.us",
        "emoji": "💼",
        "tagline": "Financial & business advisory — Plainview NY",
        "offer_suffix": "free consultation for your financial goals",
    },
    "ConsultCyber": {
        "name": "Consult Cyber",
        "domain": "consultcyber.net",
        "emoji": "🔐",
        "tagline": "Cybersecurity & IT consulting — Long Island NY",
        "offer_suffix": "IT security assessment & managed services",
    },
}

CATEGORY_ICON = {
    "Graduation & Ceremony":    "🎓",
    "Major US Holiday":         "🇺🇸",
    "Personal Milestone":       "🎂",
    "Religious":                "🙏",
    "Corporate & Professional": "💼",
    "Seasonal":                 "🌿",
    "Long Island Special":      "🗽",
    "Health & Awareness":       "💙",
    "Love & Romance":           "❤️",
    "Food & Fun":               "🍕",
    "Shopping & Sale":          "🛍️",
}


def build_md():
    rows = build_all_days()

    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    lines = []
    a = lines.append

    # ── Header ────────────────────────────────────────────────────────────────
    a("# 🎉 Hiren Kumar Stores — Complete 2026 Celebration & Special Days Calendar")
    a("")
    a("> **All 7 Long Island stores | Plainview, NY | Auto-greetings via Email & WhatsApp**")
    a("")
    a(f"Generated: **{TODAY}** | Total events: **{len(rows)}** | Upcoming: **{len([r for r in rows if r['Status'] in ('UPCOMING','TODAY')])}**")
    a("")
    a("---")
    a("")

    # ── Store Directory ───────────────────────────────────────────────────────
    a("## 🏬 Our 7 Stores")
    a("")
    for sk, sv in STORE_OFFERS.items():
        a(f"| {sv['emoji']} | **[{sv['name']}](https://{sv['domain']})** | {sv['tagline']} |")
    a("")
    a("---")
    a("")

    # ── Quick Stats ───────────────────────────────────────────────────────────
    a("## 📊 Quick Stats")
    a("")
    a("| Category | Count | Top Discount |")
    a("|---|---|---|")
    for cat, icon in CATEGORY_ICON.items():
        cat_rows = [r for r in rows if r["_cat"] == cat]
        max_disc = max((r["Discount %"] for r in cat_rows), default=0)
        a(f"| {icon} {cat} | {len(cat_rows)} | {max_disc}% |")
    a("")
    a("---")
    a("")

    # ── 7-Day Urgent Alerts ───────────────────────────────────────────────────
    urgent = [r for r in rows if isinstance(r["Days Until"], int) and 0 <= r["Days Until"] <= 7]
    if urgent:
        a("## 🚨 THIS WEEK — Send Greetings NOW")
        a("")
        for r in sorted(urgent, key=lambda x: x["Days Until"]):
            badge = "**TODAY**" if r["Days Until"] == 0 else f"in **{r['Days Until']} day(s)**"
            a(f"### {r['Emoji']} {r['Event']} — {badge}")
            a(f"- 📅 Date: `{r['Date']}`")
            a(f"- 🏷️ Promo: `{r['Promo Code']}` | Discount: **{r['Discount %']}% OFF**")
            a(f"- 📧 Subject: *{r['Email Subject']}*")
            a(f"- 📱 WhatsApp: `{r['WhatsApp Message']}`")
            a("")
        a("---")
        a("")

    # ── Month-by-Month listing ────────────────────────────────────────────────
    a("## 📅 Complete Calendar by Month")
    a("")

    for month in months:
        month_rows = [r for r in rows if r["Month"] == month]
        if not month_rows:
            continue
        upcoming_count = len([r for r in month_rows if r["Status"] in ("UPCOMING","TODAY")])
        status_note = f"✅ {upcoming_count} upcoming" if upcoming_count else "⬛ all past"

        a(f"---")
        a("")
        a(f"## 📆 {month.upper()} — {len(month_rows)} events ({status_note})")
        a("")

        for r in month_rows:
            # Status badge
            if r["Status"] == "TODAY":
                badge = "🔴 **TODAY**"
            elif r["Alert"] == "URGENT (≤7d)":
                badge = f"🟠 URGENT — {r['Days Until']} days"
            elif r["Alert"] == "SOON (≤30d)":
                badge = f"🟡 Soon — {r['Days Until']} days"
            elif r["Status"] == "UPCOMING":
                badge = f"🟢 {r['Days Until']} days away"
            else:
                badge = "⬛ Past"

            cat_icon = CATEGORY_ICON.get(r["_cat"], "📌")

            a(f"### {r['Emoji']} {r['Event']}")
            a(f"| Field | Value |")
            a(f"|---|---|")
            a(f"| 📅 Date | **{r['Date']}** ({r['Day']}) |")
            a(f"| 🏷️ Category | {cat_icon} {r['Category']} |")
            a(f"| ⏳ Status | {badge} |")
            a(f"| 💰 Discount | **{r['Discount %']}% OFF** |")
            a(f"| 🎟️ Promo Code | `{r['Promo Code']}` |")
            a(f"| 🎁 Best Gift | {r['Best Basket Idea']} |")
            a("")

            # Auto-greeting block
            a(f"<details>")
            a(f"<summary>📧 Auto Email Greeting — click to expand</summary>")
            a("")
            a(f"**Subject:** {r['Email Subject']}")
            a("")
            a("```")
            a(r["Email Body"])
            a("```")
            a("")
            a(f"</details>")
            a("")
            a(f"<details>")
            a(f"<summary>📱 WhatsApp Message — click to expand</summary>")
            a("")
            a("```")
            a(r["WhatsApp Message"])
            a("```")
            a("")
            a(f"</details>")
            a("")

            # Per-store offers
            a(f"<details>")
            a(f"<summary>🏬 Per-Store Offers — all 7 stores</summary>")
            a("")
            a("| Store | Offer | Link |")
            a("|---|---|---|")
            for sk, sv in STORE_OFFERS.items():
                code = r["Promo Code"]
                disc = r["Discount %"]
                a(f"| {sv['emoji']} {sv['name']} | {disc}% off {sv['offer_suffix']} — use `{code}` | [Shop](https://{sv['domain']}) |")
            a("")
            a(f"</details>")
            a("")

    # ── n8n Setup Guide ───────────────────────────────────────────────────────
    a("---")
    a("")
    a("## ⚙️ Auto-Greeting Setup Guide")
    a("")
    a("### Step 1 — Import n8n Workflow")
    a("1. Open your n8n instance (Hostinger VPS)")
    a("2. Click **Import Workflow**")
    a("3. Upload `n8n_all_stores_workflow.json`")
    a("4. Activate the workflow")
    a("")
    a("### Step 2 — Connect Credentials")
    a("| Service | Credential | Used For |")
    a("|---|---|---|")
    a("| Gmail | countrycoveinc@gmail.com | Send emails for all stores |")
    a("| Twilio | Long Island 631/516 number | WhatsApp messages |")
    a("| Odoo | country-cove-inc.odoo.com | Log activity to CRM |")
    a("")
    a("### Step 3 — Schedule")
    a("- Workflow runs **daily at 9:00 AM EST**")
    a("- Fires at **7 days before**, **3 days before**, **1 day before**, and **day-of**")
    a("- Each store gets its own branded message")
    a("")
    a("### Step 4 — Odoo Homepage Greetings")
    a("- Run `inject_all_store_greetings.py` to push celebration banners to all 7 Odoo websites")
    a("- Banners auto-update based on the current date")
    a("")
    a("---")
    a("")
    a("## 📁 Files Reference")
    a("")
    a("| File | Description |")
    a("|---|---|")
    a("| `CELEBRATIONS.md` | This file — full calendar |")
    a("| `MASTER_Celebration_SpecialDays_2026.xlsx` | Excel workbook — 14 sheets |")
    a("| `email_whatsapp_templates.xlsx` | Ready-to-send templates |")
    a("| `celebration_templates.json` | n8n-compatible JSON |")
    a("| `n8n_all_stores_workflow.json` | Import into n8n |")
    a("| `inject_all_store_greetings.py` | Push greetings to all 7 Odoo homepages |")
    a("| `celebration_section_homepage.html` | LI Gift Basket HTML block |")
    a("")
    a("---")
    a("")
    a(f"*Generated by Claude Code for Hiren Kumar / Country Cove Inc | Plainview, Long Island, NY | {TODAY}*")

    return "\n".join(lines)


if __name__ == "__main__":
    content = build_md()
    out = Path(r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\celebration_calendar\CELEBRATIONS.md")
    out.write_text(content, encoding="utf-8")
    print(f"CELEBRATIONS.md written — {len(content):,} chars, {content.count(chr(10))} lines")
    print(f"Path: {out}")
