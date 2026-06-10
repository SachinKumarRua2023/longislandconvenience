#!/usr/bin/env python3
"""
Odoo Universal Website Builder
==============================
Creates a complete Odoo website from scratch for any business category.

CATEGORIES:
  ecommerce      Online store with shop, product grid, cart CTA
  agency         IT / marketing / consulting agency with services grid
  tech           SaaS / software product with features + pricing strip
  local_business Service-area business (contractor, salon, clinic, etc.)
  restaurant     Food & beverage with menu sections and reservations
  nonprofit      Non-profit / charity with mission, events, donate CTA

USAGE (standalone):
  python odoo_website_builder.py \
      --site 41 \
      --category agency \
      --name "JHD Advisor" \
      --domain "https://www.jhdadvisor.com" \
      --phone "+1 (917) 338-7086" \
      --email "info@jhdadvisor.com" \
      --location "Long Island, NY" \
      --tagline "Build the business operating system your competitors wish they had." \
      --color1 "#7c3aed" \
      --color2 "#06b6d4"

USAGE (called from n8n via subprocess or import):
  from odoo_website_builder import WebsiteBuilder, TEMPLATES
  b = WebsiteBuilder(site_id=41, config={...})
  b.run()
"""

import sys, json, time, argparse, textwrap
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

sys.stdout.reconfigure(encoding="utf-8")

# ═══════════════════════════════════════════════════════════════════════════════
#  ODOO CONNECTION
# ═══════════════════════════════════════════════════════════════════════════════
ODOO_URL  = "https://country-cove-inc.odoo.com"
ODOO_DB   = "country-cove-inc"
ODOO_UID  = 2
ODOO_PASS = "M@nhattan1234"

_sess = requests.Session()
_sess.mount("https://", HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1.5)))
_rpc_counter = 0

def rpc(model, method, args, kw=None):
    global _rpc_counter
    _rpc_counter += 1
    r = _sess.post(f"{ODOO_URL}/jsonrpc", json={
        "jsonrpc": "2.0", "method": "call", "id": _rpc_counter,
        "params": {
            "service": "object", "method": "execute_kw",
            "args": [ODOO_DB, ODOO_UID, ODOO_PASS, model, method, args, kw or {}],
        },
    }, timeout=60)
    d = r.json()
    if d.get("error"):
        print(f"  RPC ERR {model}.{method}: {d['error']['data']['message'][:200]}")
        return None
    return d.get("result")


# ═══════════════════════════════════════════════════════════════════════════════
#  CATEGORY TEMPLATES
#  Each template defines colors, fonts, nav items, sections, services,
#  blog topics, stats, CTA text, Unsplash image keywords per section.
# ═══════════════════════════════════════════════════════════════════════════════
TEMPLATES = {

    # ──────────────────────────────────────────────────────────────────────────
    "agency": {
        "description": "IT / marketing / consulting agency",
        "color1": "#7c3aed",   # primary (purple)
        "color2": "#06b6d4",   # accent  (cyan)
        "color_dark": "#0a0a1a",
        "color_light": "#f7f8fb",
        "eyebrow": "AI · Automation · Ecommerce · Web",
        "hero_headline": "Build the business operating system your competitors wish they had.",
        "hero_sub": "We design automation, AI systems, ecommerce platforms and web applications that turn searches into leads and leads into revenue.",
        "hero_cta_primary": "Book Strategy Call",
        "hero_cta_secondary": "See Our Work",
        "hero_cta_primary_href": "/contact",
        "hero_cta_secondary_href": "/services",
        "services_headline": "10 high-demand services. One connected operating system.",
        "services_sub": "Every service we deliver is designed to connect with the others — automation, AI, ecommerce, web apps and search all working as one system.",
        "services": [
            {"icon": "AI",   "name": "AI Business Automation",    "desc": "Agentic workflows, AI assistants, SOP automation and operations copilots."},
            {"icon": "N8N",  "name": "n8n Workflow Automation",   "desc": "Lead capture, CRM routing, email, invoice, reminder and reporting pipelines."},
            {"icon": "ECO",  "name": "Ecommerce Automation",      "desc": "Odoo, Shopify and WooCommerce builds with inventory, payments and fulfillment."},
            {"icon": "APP",  "name": "Web App & SaaS Development","desc": "Portals, dashboards, booking systems and multi-tenant SaaS MVPs."},
            {"icon": "BOT",  "name": "AI Chatbots & Voice Agents","desc": "Website chat, support bots, sales agents and voice appointment flows."},
            {"icon": "SEO",  "name": "SEO & GEO Strategy",        "desc": "Rank in Google, AI Overviews and answer engines with schema and content clusters."},
            {"icon": "BI",   "name": "Data Dashboards & BI",      "desc": "Executive dashboards, KPI reporting and automated weekly performance briefs."},
            {"icon": "API",  "name": "API Integrations",          "desc": "Connect Stripe, Odoo, Google Sheets, CRMs, ERPs and marketing platforms."},
            {"icon": "SEC",  "name": "Cloud & Cybersecurity",     "desc": "Secure hosting, backups, access controls, AI governance and audit readiness."},
            {"icon": "MVP",  "name": "Startup MVP Launch",        "desc": "Product strategy, prototypes, MVP builds, investor decks and launch systems."},
        ],
        "stats": [
            {"value": "10+", "label": "IT service verticals"},
            {"value": "24/7", "label": "Automated AI workflows"},
            {"value": "40%",  "label": "Average cost reduction"},
            {"value": "3×",   "label": "Faster lead-to-close"},
        ],
        "blog_tag": "Growth Insights",
        "blog_topics": [
            ("What Are AI Agents and Why Every Business Needs One in 2026", "The shift from chatbots to autonomous AI agents — and what it means for your operations."),
            ("n8n vs Zapier: The Honest Comparison for Business Owners", "Cost, flexibility, AI-native features and real-world execution limits compared."),
            ("How to Rank in Google AI Overviews: GEO Strategy for 2026", "Generative Engine Optimization — the new discipline every business website needs."),
            ("Odoo vs Shopify vs WooCommerce: Which Stack Wins in 2026?", "A business-first decision guide for founders, retailers and service brands."),
            ("The Automation ROI Calculator: What Are Your Workflows Actually Saving?", "A framework to turn gut-feel automation projects into board-ready business cases."),
        ],
        "cta_headline": "Ready to automate your growth engine?",
        "cta_sub": "Book a strategy call or send your project brief. We respond within one business day.",
        "nav": ["Home", "Services", "Blog", "About", "Contact"],
        "nav_hrefs": ["/", "/services", "/blog", "/about", "/contact"],
        "footer_tagline": "AI · Automation · Ecommerce · Web Apps · SEO",
        "footer_links": ["Services", "Blog", "About", "Contact", "Privacy Policy"],
        "footer_hrefs": ["/services", "/blog", "/about", "/contact", "/privacy"],
        "hero_img": "1551434678-e076c223a692",   # laptop code
        "services_img": "1518770660439-4636190af475",  # circuit board
    },

    # ──────────────────────────────────────────────────────────────────────────
    "ecommerce": {
        "description": "Online retail / ecommerce store",
        "color1": "#16a34a",   # primary green
        "color2": "#f59e0b",   # accent amber
        "color_dark": "#14532d",
        "color_light": "#f0fdf4",
        "eyebrow": "Free Shipping · Same-Day Pickup · Easy Returns",
        "hero_headline": "Shop local. Live better.",
        "hero_sub": "Curated products, same-day pickup and lightning-fast shipping — everything you need, closer than you think.",
        "hero_cta_primary": "Shop Now",
        "hero_cta_secondary": "View Categories",
        "hero_cta_primary_href": "/shop",
        "hero_cta_secondary_href": "/shop",
        "services_headline": "Everything in one place.",
        "services_sub": "Browse our full catalog — thousands of products across dozens of categories, always in stock.",
        "services": [
            {"icon": "NEW",  "name": "New Arrivals",       "desc": "Fresh inventory added weekly — be the first to shop the latest."},
            {"icon": "SALE", "name": "Deals & Offers",     "desc": "Member discounts, clearance and bundle savings updated daily."},
            {"icon": "GIFT", "name": "Gift Sets",          "desc": "Ready-to-ship curated gift sets for every occasion."},
            {"icon": "FAST", "name": "Same-Day Pickup",    "desc": "Order before 2 PM, pick up same day at your nearest location."},
            {"icon": "SHIP", "name": "Free Shipping",      "desc": "Free standard shipping on all orders over $35."},
            {"icon": "RET",  "name": "Easy Returns",       "desc": "30-day no-hassle returns on all eligible items."},
        ],
        "stats": [
            {"value": "5K+",  "label": "Products in stock"},
            {"value": "10K+", "label": "Happy customers"},
            {"value": "4.9★", "label": "Average rating"},
            {"value": "1Day", "label": "Local pickup"},
        ],
        "blog_tag": "Shopping Guide",
        "blog_topics": [
            ("Top 10 Gift Ideas for Any Occasion — 2026 Buying Guide", "Curated picks for birthdays, anniversaries, holidays and just-because moments."),
            ("How to Save More on Every Order: Coupons, Bundles and Member Deals", "Practical strategies to get the most value from every shopping trip."),
            ("Same-Day Pickup vs Shipping: When to Choose What", "A quick decision guide for urgent orders and planned purchases."),
            ("New Arrivals This Month: What to Add to Your Cart First", "Our buyers share the most exciting products landing in store this month."),
            ("The Complete Holiday Shopping Checklist for 2026", "Never forget a gift again — the organized shopper's seasonal planner."),
        ],
        "cta_headline": "Start shopping today — free shipping over $35.",
        "cta_sub": "Join thousands of local shoppers who trust us for quality, convenience and value.",
        "nav": ["Home", "Shop", "Deals", "Blog", "Contact"],
        "nav_hrefs": ["/", "/shop", "/shop?pricelist=sale", "/blog", "/contact"],
        "footer_tagline": "Quality Products · Fast Shipping · Easy Returns",
        "footer_links": ["Shop", "New Arrivals", "Deals", "Blog", "Contact", "Returns Policy"],
        "footer_hrefs": ["/shop", "/shop?order=newest", "/shop?pricelist=sale", "/blog", "/contact", "/returns"],
        "hero_img": "1563013544-824ae1b704d3",
        "services_img": "1472851294608-062f824d29cc",
    },

    # ──────────────────────────────────────────────────────────────────────────
    "tech": {
        "description": "SaaS / software product company",
        "color1": "#2563eb",   # primary blue
        "color2": "#7c3aed",   # accent purple
        "color_dark": "#0f172a",
        "color_light": "#f8fafc",
        "eyebrow": "Trusted by 500+ Teams · SOC 2 Ready · 99.9% Uptime",
        "hero_headline": "The platform that runs your business on autopilot.",
        "hero_sub": "Automate workflows, unify your data, and ship faster — all from one intelligent platform built for modern teams.",
        "hero_cta_primary": "Start Free Trial",
        "hero_cta_secondary": "Watch Demo",
        "hero_cta_primary_href": "/contact",
        "hero_cta_secondary_href": "/about",
        "services_headline": "Every feature your team actually needs.",
        "services_sub": "Built for speed and reliability — no bloat, no per-seat gotchas, no surprise bills.",
        "services": [
            {"icon": "AUTO", "name": "Workflow Automation",   "desc": "Build powerful automated flows without a single line of code."},
            {"icon": "AI",   "name": "AI-Powered Insights",  "desc": "Get instant answers from your data with natural-language queries."},
            {"icon": "DASH", "name": "Live Dashboards",      "desc": "Real-time KPI tracking across teams, projects and pipelines."},
            {"icon": "INT",  "name": "1,000+ Integrations",  "desc": "Connect every tool your team already uses in minutes."},
            {"icon": "SEC",  "name": "Enterprise Security",  "desc": "SOC 2 Type II, SSO, audit logs and role-based access built in."},
            {"icon": "API",  "name": "Developer API",        "desc": "Full REST API, webhooks and SDK support for custom workflows."},
        ],
        "stats": [
            {"value": "500+",  "label": "Teams using our platform"},
            {"value": "99.9%", "label": "Uptime SLA"},
            {"value": "10M+",  "label": "Automations run monthly"},
            {"value": "4min",  "label": "Average setup time"},
        ],
        "blog_tag": "Product & Engineering",
        "blog_topics": [
            ("How We Achieved 99.9% Uptime: Our Infrastructure Playbook", "A behind-the-scenes look at the architecture decisions that keep us reliable."),
            ("AI Workflows That Save Engineering Teams 10 Hours Per Week", "Real examples from our customers — and how to replicate them."),
            ("No-Code Automation: What It Can (and Cannot) Replace in 2026", "An honest evaluation for technical founders and ops leaders."),
            ("From Spreadsheet to Dashboard in 4 Minutes: A Product Demo", "The fastest way to move your team off manual reporting for good."),
            ("Security Best Practices for SaaS Teams Handling Customer Data", "SOC 2, encryption, access controls and incident response checklists."),
        ],
        "cta_headline": "Start your free 14-day trial today.",
        "cta_sub": "No credit card required. Set up in under 4 minutes. Cancel anytime.",
        "nav": ["Home", "Features", "Pricing", "Blog", "Contact"],
        "nav_hrefs": ["/", "/services", "/pricing", "/blog", "/contact"],
        "footer_tagline": "Automation · Analytics · Integrations · Security",
        "footer_links": ["Features", "Pricing", "API Docs", "Blog", "Contact", "Status"],
        "footer_hrefs": ["/services", "/pricing", "/api", "/blog", "/contact", "/status"],
        "hero_img": "1551288049-bebda4e38f71",
        "services_img": "1518770660439-4636190af475",
    },

    # ──────────────────────────────────────────────────────────────────────────
    "local_business": {
        "description": "Local service business (contractor, salon, clinic, etc.)",
        "color1": "#dc2626",   # primary red
        "color2": "#f59e0b",   # accent amber
        "color_dark": "#1c1917",
        "color_light": "#fafaf9",
        "eyebrow": "Locally Owned · Trusted Since 1998 · Same-Day Service",
        "hero_headline": "Your trusted local expert — one call, every need.",
        "hero_sub": "Fast response, fair pricing, and the quality of work that has kept our neighbors calling us back for over 25 years.",
        "hero_cta_primary": "Call Us Now",
        "hero_cta_secondary": "Get a Free Quote",
        "hero_cta_primary_href": "tel:+19173387086",
        "hero_cta_secondary_href": "/contact",
        "services_headline": "Services that cover it all.",
        "services_sub": "From quick fixes to complete projects — we bring the expertise, tools and professionalism your home or business deserves.",
        "services": [
            {"icon": "FAST", "name": "Same-Day Service",     "desc": "We show up when you need us — morning, afternoon or urgent."},
            {"icon": "FREE", "name": "Free Estimates",       "desc": "Honest, no-obligation quotes before any work begins."},
            {"icon": "LIC",  "name": "Licensed & Insured",   "desc": "Full licensing, bonding and liability insurance on every job."},
            {"icon": "WAR",  "name": "Workmanship Warranty", "desc": "We stand behind every job with a written satisfaction guarantee."},
            {"icon": "RES",  "name": "Residential",         "desc": "Home services designed around your schedule and budget."},
            {"icon": "COM",  "name": "Commercial",          "desc": "Business and commercial projects handled with minimal disruption."},
        ],
        "stats": [
            {"value": "25+",  "label": "Years serving the community"},
            {"value": "2K+",  "label": "Happy local customers"},
            {"value": "4.9★", "label": "Google review rating"},
            {"value": "Same", "label": "Day service available"},
        ],
        "blog_tag": "Local Tips",
        "blog_topics": [
            ("10 Signs You Should Call a Professional Instead of DIY-ing It", "When saving money on a repair can cost you twice as much later."),
            ("How to Choose a Reliable Local Service Provider: The 5-Point Checklist", "License, insurance, reviews, response time and written estimates — what to ask."),
            ("Seasonal Home Maintenance Checklist: What to Do Before Each Season", "A practical homeowner's guide to avoiding costly emergency repairs."),
            ("Why Local Businesses Always Beat the Big Chains for Service Quality", "The difference a local expert makes — accountability, speed and genuine care."),
            ("How to Get the Most From Your Service Appointment", "Tips to prepare, questions to ask, and what to confirm before the technician leaves."),
        ],
        "cta_headline": "Ready to get started? Call or get a free quote.",
        "cta_sub": "Our team is standing by — fast response, fair pricing, quality guaranteed.",
        "nav": ["Home", "Services", "About", "Blog", "Contact"],
        "nav_hrefs": ["/", "/services", "/about", "/blog", "/contact"],
        "footer_tagline": "Locally Owned · Licensed & Insured · Same-Day Service",
        "footer_links": ["Services", "About Us", "Blog", "Contact", "Privacy Policy"],
        "footer_hrefs": ["/services", "/about", "/blog", "/contact", "/privacy"],
        "hero_img": "1522202176988-66273c2fd55f",
        "services_img": "1560518883-ce09059eeffa",
    },

    # ──────────────────────────────────────────────────────────────────────────
    "restaurant": {
        "description": "Restaurant, cafe or food service",
        "color1": "#b45309",   # primary amber-brown
        "color2": "#dc2626",   # accent red
        "color_dark": "#1c1917",
        "color_light": "#fffbeb",
        "eyebrow": "Fresh Ingredients · Made to Order · Dine-In & Takeout",
        "hero_headline": "Food made with love. Served with pride.",
        "hero_sub": "Every dish tells a story — fresh local ingredients, recipes perfected over generations, and a dining experience that brings people together.",
        "hero_cta_primary": "Reserve a Table",
        "hero_cta_secondary": "Order Online",
        "hero_cta_primary_href": "/contact",
        "hero_cta_secondary_href": "/shop",
        "services_headline": "A menu for every occasion.",
        "services_sub": "From casual lunches to celebratory dinners — our kitchen is ready to make your moment memorable.",
        "services": [
            {"icon": "BRKF", "name": "Breakfast & Brunch", "desc": "Morning favorites served fresh daily until 2 PM."},
            {"icon": "LNCH", "name": "Lunch",              "desc": "Quick bites and hearty mains — perfect for your midday break."},
            {"icon": "DINR", "name": "Dinner",             "desc": "Elevated plates, intimate atmosphere, unforgettable evenings."},
            {"icon": "TAKE", "name": "Takeout & Delivery", "desc": "Order online or by phone — ready in 20 minutes or delivered to your door."},
            {"icon": "CATER","name": "Catering",           "desc": "Corporate events, weddings, parties — we handle every detail."},
            {"icon": "PRIV", "name": "Private Events",     "desc": "Reserve our space for birthdays, anniversaries and celebrations."},
        ],
        "stats": [
            {"value": "15+",  "label": "Years of great food"},
            {"value": "98%",  "label": "Customer satisfaction"},
            {"value": "4.9★", "label": "Yelp & Google rating"},
            {"value": "20min","label": "Takeout ready time"},
        ],
        "blog_tag": "Food & Life",
        "blog_topics": [
            ("Behind the Menu: Where Our Ingredients Come From", "A story about the local farms, fisheries and suppliers we trust every day."),
            ("5 Dishes You Have to Try Before You Die (According to Our Chef)", "The chef's personal favorites — and the stories behind each one."),
            ("How to Plan the Perfect Dinner Party Catered by Us", "From guest count to dietary needs — everything you need to know."),
            ("Seasonal Menu Updates: What's New This Month", "Fresh flavors for the new season — here's what just landed on our menu."),
            ("The Art of Wine Pairing: A Beginner's Guide from Our Sommelier", "Simple rules that make every meal better without being intimidating."),
        ],
        "cta_headline": "Make a reservation or order online today.",
        "cta_sub": "Tables fill fast on weekends — book early or call ahead. Walk-ins always welcome.",
        "nav": ["Home", "Menu", "Reservations", "Blog", "Contact"],
        "nav_hrefs": ["/", "/shop", "/contact", "/blog", "/contact"],
        "footer_tagline": "Fresh Food · Great Atmosphere · Memorable Moments",
        "footer_links": ["Menu", "Reservations", "Catering", "Blog", "Contact", "Gift Cards"],
        "footer_hrefs": ["/shop", "/contact", "/catering", "/blog", "/contact", "/giftcards"],
        "hero_img": "1414235077428-338989a2e8c0",
        "services_img": "1504674900247-0877df9cc836",
    },

    # ──────────────────────────────────────────────────────────────────────────
    "nonprofit": {
        "description": "Non-profit / charity organization",
        "color1": "#0891b2",   # primary teal
        "color2": "#f59e0b",   # accent amber
        "color_dark": "#0c4a6e",
        "color_light": "#f0f9ff",
        "eyebrow": "501(c)(3) · Community-Driven · Transparent Impact",
        "hero_headline": "Together, we create lasting change.",
        "hero_sub": "Every donation, every volunteer hour, and every shared story moves us closer to a world where no one gets left behind.",
        "hero_cta_primary": "Donate Now",
        "hero_cta_secondary": "Get Involved",
        "hero_cta_primary_href": "/donate",
        "hero_cta_secondary_href": "/contact",
        "services_headline": "Our programs. Your impact.",
        "services_sub": "Transparent, measurable programs that turn community support into real-world results.",
        "services": [
            {"icon": "EDU",  "name": "Education",          "desc": "Scholarships, tutoring and digital literacy programs for underserved youth."},
            {"icon": "FOOD", "name": "Food Security",      "desc": "Weekly food drives, community pantries and meal delivery for seniors."},
            {"icon": "HLTH", "name": "Health Access",      "desc": "Free clinics, mental health resources and insurance navigation support."},
            {"icon": "HOUS", "name": "Housing",            "desc": "Emergency shelter, transitional housing and home repair assistance."},
            {"icon": "JOB",  "name": "Job Readiness",      "desc": "Resume writing, interview prep and job placement partnerships."},
            {"icon": "COMM", "name": "Community Events",   "desc": "Monthly gatherings that connect, celebrate and strengthen the community."},
        ],
        "stats": [
            {"value": "12K+", "label": "Lives impacted this year"},
            {"value": "500+", "label": "Active volunteers"},
            {"value": "98%",  "label": "Funds go to programs"},
            {"value": "20yr", "label": "Years in the community"},
        ],
        "blog_tag": "Impact Stories",
        "blog_topics": [
            ("How Your $25 Donation Feeds a Family for a Week", "A transparent breakdown of how every dollar creates direct community impact."),
            ("Volunteer Spotlight: Meet the People Behind Our Mission", "Real stories from the volunteers who make our programs possible."),
            ("2026 Impact Report: Our Year in Numbers", "The results, the stories and the goals for the year ahead."),
            ("5 Ways to Get Involved That Do not Require Writing a Check", "Volunteering, advocacy, in-kind donations and spreading the word."),
            ("The Community Problem We Are Solving — and Why It Matters Now", "Context, data and the human face behind our core program area."),
        ],
        "cta_headline": "Your support changes lives. Every contribution counts.",
        "cta_sub": "Donate today, volunteer this weekend, or simply share our mission with someone who cares.",
        "nav": ["Home", "Programs", "Get Involved", "Blog", "Contact"],
        "nav_hrefs": ["/", "/services", "/contact", "/blog", "/contact"],
        "footer_tagline": "501(c)(3) Nonprofit · Transparent · Community-Driven",
        "footer_links": ["Programs", "Donate", "Volunteer", "Blog", "Contact", "Annual Report"],
        "footer_hrefs": ["/services", "/donate", "/contact", "/blog", "/contact", "/report"],
        "hero_img": "1531206715517-5c0ba140b2b8",
        "services_img": "1559027615-cd4628902d4a",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
#  HTML / CSS GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def _img(photo_id, alt, h=500):
    """Full-width Unsplash image block — safe for Odoo (no cover_properties)."""
    url = f"https://images.unsplash.com/photo-{photo_id}?w=1400&h={h}&fit=crop&q=80&auto=format"
    return (
        f'<div style="width:100%;border-radius:16px;overflow:hidden;'
        f'box-shadow:0 8px 40px rgba(0,0,0,.12);margin-bottom:40px;">'
        f'<img src="{url}" alt="{alt}" '
        f'style="width:100%;height:{h}px;object-fit:cover;display:block;" loading="lazy"/></div>'
    )


def _css(t):
    c1, c2, dk, lt = t["color1"], t["color2"], t["color_dark"], t["color_light"]
    return f"""<style>
:root{{--c1:{c1};--c2:{c2};--dk:{dk};--lt:{lt};--ink:#111827;--muted:#5b6472;}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:Inter,system-ui,sans-serif;}}

/* HERO */
.wb-hero{{min-height:88vh;display:grid;grid-template-columns:minmax(280px,1fr) minmax(280px,.9fr);
  gap:40px;align-items:center;padding:90px 7vw;
  background:radial-gradient(circle at 70% 20%,color-mix(in srgb,var(--c1) 30%,transparent),transparent 40%),
             linear-gradient(140deg,var(--dk),color-mix(in srgb,var(--c1) 20%,#000) 55%,color-mix(in srgb,var(--c2) 15%,#000));
  color:#fff;overflow:hidden;position:relative;}}
.wb-eyebrow{{color:var(--c2);font-size:11px;text-transform:uppercase;letter-spacing:3px;font-weight:900;margin-bottom:16px;}}
.wb-hero h1{{font-size:clamp(32px,5vw,68px);line-height:1.04;font-weight:900;letter-spacing:-1px;margin-bottom:20px;}}
.wb-hero p{{font-size:17px;line-height:1.8;color:rgba(255,255,255,.78);margin-bottom:28px;}}
.wb-actions{{display:flex;gap:14px;flex-wrap:wrap;}}
.wb-btn{{display:inline-flex;align-items:center;justify-content:center;
  padding:15px 28px;border-radius:10px;text-decoration:none;font-weight:900;font-size:15px;transition:all .22s;}}
.wb-primary{{background:#fff;color:var(--dk);box-shadow:0 8px 30px rgba(255,255,255,.2);}}
.wb-primary:hover{{transform:translateY(-2px);box-shadow:0 16px 40px rgba(255,255,255,.3);}}
.wb-secondary{{border:1.5px solid rgba(255,255,255,.35);color:#fff;backdrop-filter:blur(8px);}}
.wb-secondary:hover{{background:rgba(255,255,255,.1);transform:translateY(-2px);}}
.wb-panel{{border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.07);
  backdrop-filter:blur(18px);border-radius:16px;padding:28px;
  box-shadow:0 40px 80px rgba(0,0,0,.3);}}
.wb-panel-row{{display:flex;justify-content:space-between;align-items:center;
  border-bottom:1px solid rgba(255,255,255,.09);padding:16px 0;gap:16px;}}
.wb-panel-row:last-child{{border-bottom:0;padding-bottom:0;}}
.wb-panel b{{font-size:28px;color:var(--c2);font-weight:900;}}
.wb-panel span{{color:rgba(255,255,255,.68);font-size:13px;line-height:1.4;}}

/* SERVICES */
.wb-section{{padding:84px 7vw;background:#fff;}}
.wb-section h2{{font-size:clamp(26px,3.8vw,50px);line-height:1.06;margin-bottom:12px;color:var(--ink);font-weight:900;}}
.wb-section>p{{color:var(--muted);font-size:17px;line-height:1.7;max-width:740px;margin-bottom:40px;}}
.wb-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:18px;}}
.wb-card{{background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:22px;
  display:flex;flex-direction:column;gap:12px;min-height:200px;
  box-shadow:0 4px 18px rgba(17,24,39,.06);transition:all .25s;}}
.wb-card:hover{{transform:translateY(-5px);box-shadow:0 18px 48px color-mix(in srgb,var(--c1) 20%,transparent);
  border-color:color-mix(in srgb,var(--c1) 50%,#fff);}}
.wb-icon{{width:48px;height:48px;border-radius:10px;
  background:linear-gradient(135deg,var(--c1),var(--c2));
  color:#fff;display:flex;align-items:center;justify-content:center;
  font-weight:900;font-size:11px;letter-spacing:.5px;flex-shrink:0;}}
.wb-card h3{{font-size:17px;line-height:1.2;color:var(--ink);font-weight:800;}}
.wb-card p{{font-size:13px;line-height:1.6;color:var(--muted);flex:1;}}

/* STATS */
.wb-stats{{padding:70px 7vw;
  background:linear-gradient(135deg,var(--dk),color-mix(in srgb,var(--c1) 40%,#000));
  color:#fff;}}
.wb-stats-label{{font-size:11px;text-transform:uppercase;letter-spacing:3px;
  color:var(--c2);font-weight:900;margin-bottom:28px;}}
.wb-stats-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;}}
.wb-stat{{text-align:center;padding:28px 16px;border:1px solid rgba(255,255,255,.1);
  border-radius:14px;background:rgba(255,255,255,.05);transition:all .3s;}}
.wb-stat:hover{{border-color:color-mix(in srgb,var(--c1) 60%,transparent);
  background:color-mix(in srgb,var(--c1) 12%,transparent);transform:translateY(-4px);}}
.wb-stat b{{display:block;font-size:clamp(32px,5vw,52px);font-weight:900;
  background:linear-gradient(135deg,var(--c2),color-mix(in srgb,var(--c1) 60%,#fff));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.wb-stat span{{color:rgba(255,255,255,.62);font-size:13px;margin-top:6px;display:block;}}

/* BLOG STRIP */
.wb-blog{{padding:80px 7vw;background:var(--lt);}}
.wb-blog h2{{font-size:clamp(24px,3.5vw,44px);color:var(--ink);font-weight:900;margin-bottom:10px;}}
.wb-blog>p{{color:var(--muted);font-size:16px;margin-bottom:36px;}}
.wb-blog-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}}
.wb-blog-card{{background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:24px;
  text-decoration:none;color:var(--ink);display:block;
  box-shadow:0 4px 18px rgba(17,24,39,.06);transition:all .25s;}}
.wb-blog-card:hover{{transform:translateY(-4px);
  box-shadow:0 18px 44px color-mix(in srgb,var(--c1) 15%,transparent);
  border-color:color-mix(in srgb,var(--c1) 40%,#fff);}}
.wb-blog-tag{{font-size:10px;font-weight:900;letter-spacing:2px;text-transform:uppercase;
  color:var(--c1);margin-bottom:10px;display:block;}}
.wb-blog-card h3{{font-size:15px;font-weight:800;line-height:1.4;color:var(--ink);}}
.wb-blog-card p{{font-size:13px;color:var(--muted);margin-top:8px;line-height:1.5;}}

/* CTA */
.wb-cta{{padding:80px 7vw;text-align:center;color:#fff;
  background:linear-gradient(135deg,color-mix(in srgb,var(--c1) 80%,#000),var(--dk),color-mix(in srgb,var(--c2) 30%,#000));}}
.wb-cta h2{{font-size:clamp(26px,4vw,50px);font-weight:900;margin-bottom:14px;}}
.wb-cta p{{color:rgba(255,255,255,.72);font-size:17px;margin-bottom:30px;}}

/* FOOTER */
.wb-footer{{background:var(--dk);color:rgba(255,255,255,.65);padding:60px 7vw 28px;}}
.wb-footer-grid{{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:40px;margin-bottom:44px;}}
.wb-footer h4{{color:#fff;font-size:14px;font-weight:800;letter-spacing:1px;
  text-transform:uppercase;margin-bottom:16px;}}
.wb-footer p{{font-size:13px;line-height:1.7;}}
.wb-footer a{{color:rgba(255,255,255,.55);text-decoration:none;display:block;
  font-size:13px;margin-bottom:8px;transition:color .2s;}}
.wb-footer a:hover{{color:var(--c2);}}
.wb-footer-bar{{border-top:1px solid rgba(255,255,255,.1);padding-top:22px;
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;
  font-size:12px;}}

/* RESPONSIVE */
@media(max-width:1100px){{
  .wb-hero,.wb-footer-grid{{grid-template-columns:1fr;}}
  .wb-stats-grid{{grid-template-columns:repeat(2,1fr);}}
  .wb-blog-grid{{grid-template-columns:repeat(2,1fr);}}
}}
@media(max-width:680px){{
  .wb-grid,.wb-blog-grid,.wb-stats-grid{{grid-template-columns:1fr;}}
  .wb-hero,.wb-section,.wb-stats,.wb-blog,.wb-cta,.wb-footer{{padding-left:5vw;padding-right:5vw;}}
  .wb-hero{{padding-top:64px;}}
}}
</style>"""


def _service_cards(t):
    cards = []
    for s in t["services"]:
        cards.append(
            f'<div class="wb-card">'
            f'<div class="wb-icon">{s["icon"]}</div>'
            f'<h3>{s["name"]}</h3>'
            f'<p>{s["desc"]}</p>'
            f'</div>'
        )
    return "\n".join(cards)


def _stat_cards(t):
    cards = []
    for s in t["stats"]:
        cards.append(
            f'<div class="wb-stat"><b>{s["value"]}</b><span>{s["label"]}</span></div>'
        )
    return "\n".join(cards)


def _blog_cards(t, domain):
    cards = []
    for title, sub in t["blog_topics"][:3]:
        cards.append(
            f'<a href="/blog" class="wb-blog-card">'
            f'<span class="wb-blog-tag">{t["blog_tag"]}</span>'
            f'<h3>{title}</h3>'
            f'<p>{sub[:120]}...</p>'
            f'</a>'
        )
    return "\n".join(cards)


def _footer_links(t):
    items = []
    for name, href in zip(t["footer_links"], t["footer_hrefs"]):
        items.append(f'<a href="{href}">{name}</a>')
    return "\n".join(items)


def homepage_html(t, config):
    """Generate complete homepage arch_db for any template + config."""
    css      = _css(t)
    svc_cards = _service_cards(t)
    stat_cards = _stat_cards(t)
    blog_cards = _blog_cards(t, config.get("domain", ""))
    foot_links = _footer_links(t)

    name     = config.get("name", "Our Business")
    phone    = config.get("phone", "")
    phone_h  = "tel:" + phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    email    = config.get("email", "")
    location = config.get("location", "")
    domain   = config.get("domain", "")
    tagline  = config.get("tagline", t["hero_headline"])
    year     = "2026"

    # Hero panel rows from stats
    panel_rows = ""
    for s in t["stats"]:
        panel_rows += f'<div class="wb-panel-row"><b>{s["value"]}</b><span>{s["label"]}</span></div>\n'

    hero_img_html = _img(t["hero_img"], f"{name} hero image", 480)

    return f"""<data><xpath expr="//div[@id='wrap']" position="replace">
<div id="wrap" class="oe_structure">
{css}

<!-- ══ HERO ══ -->
<section class="wb-hero">
  <div>
    <p class="wb-eyebrow">{t["eyebrow"]}</p>
    <h1>{tagline}</h1>
    <p>{t["hero_sub"]}</p>
    <div class="wb-actions">
      <a class="wb-btn wb-primary" href="{t['hero_cta_primary_href']}">{t['hero_cta_primary']}</a>
      <a class="wb-btn wb-secondary" href="{t['hero_cta_secondary_href']}">{t['hero_cta_secondary']}</a>
    </div>
  </div>
  <div class="wb-panel">
    {panel_rows}
  </div>
</section>

<!-- ══ SERVICES ══ -->
<section class="wb-section" id="services">
  <p class="wb-eyebrow">What We Offer</p>
  <h2>{t['services_headline']}</h2>
  <p>{t['services_sub']}</p>
  {hero_img_html}
  <div class="wb-grid">
    {svc_cards}
  </div>
</section>

<!-- ══ STATS ══ -->
<section class="wb-stats">
  <p class="wb-stats-label">By The Numbers</p>
  <div class="wb-stats-grid">
    {stat_cards}
  </div>
</section>

<!-- ══ BLOG ══ -->
<section class="wb-blog">
  <p class="wb-eyebrow">{t['blog_tag']}</p>
  <h2>Fresh insights for what people are searching right now.</h2>
  <p>Our blog covers the topics your customers care about — read to stay ahead.</p>
  <div class="wb-blog-grid">
    {blog_cards}
  </div>
  <div style="text-align:center;margin-top:32px;">
    <a href="/blog" class="wb-btn wb-primary" style="background:var(--c1);color:#fff;display:inline-flex;">
      Read All Posts →
    </a>
  </div>
</section>

<!-- ══ CTA ══ -->
<section class="wb-cta">
  <h2>{t['cta_headline']}</h2>
  <p>{t['cta_sub']}</p>
  <div class="wb-actions" style="justify-content:center;">
    <a class="wb-btn wb-primary" href="{t['hero_cta_primary_href']}">{t['hero_cta_primary']}</a>
    <a class="wb-btn wb-secondary" href="/contact">Contact Us</a>
  </div>
</section>

<!-- ══ FOOTER ══ -->
<footer class="wb-footer">
  <div class="wb-footer-grid">
    <div>
      <h4>{name}</h4>
      <p>{t['footer_tagline']}</p>
      <p style="margin-top:14px;">{location}</p>
      {f'<p style="margin-top:8px;"><a href="{phone_h}" style="color:var(--c2);">{phone}</a></p>' if phone else ''}
      {f'<p style="margin-top:4px;"><a href="mailto:{email}" style="color:rgba(255,255,255,.55);">{email}</a></p>' if email else ''}
    </div>
    <div>
      <h4>Quick Links</h4>
      {foot_links}
    </div>
    <div>
      <h4>Contact</h4>
      {f'<p>{location}</p>' if location else ''}
      {f'<a href="{phone_h}">{phone}</a>' if phone else ''}
      {f'<a href="mailto:{email}">{email}</a>' if email else ''}
      <p style="margin-top:12px;font-size:12px;color:rgba(255,255,255,.4);">
        Mon–Fri 9 AM–6 PM
      </p>
    </div>
  </div>
  <div class="wb-footer-bar">
    <span>© {year} {name}. All rights reserved.</span>
    <span style="color:rgba(255,255,255,.35);">Built on Odoo · Powered by AI</span>
  </div>
</footer>

</div></xpath></data>"""


def blog_post_html(title, subtitle, t, config):
    """Generate full-length blog post HTML for any category."""
    name     = config.get("name", "Our Team")
    phone    = config.get("phone", "")
    phone_h  = "tel:" + phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    domain   = config.get("domain", "")
    location = config.get("location", "")
    c1       = t["color1"]
    c2       = t["color2"]
    category = t.get("description", "business")

    cta = f"""
<div style="background:linear-gradient(135deg,{c1},{c2});border-radius:16px;
  padding:36px 32px;margin:40px 0 8px;color:#fff;text-align:center;">
  <h3 style="font-size:22px;margin:0 0 10px;font-weight:900;">{t['cta_headline']}</h3>
  <p style="margin:0 0 22px;font-size:15px;opacity:.9;">{t['cta_sub']}</p>
  {f'<a href="{phone_h}" style="display:inline-block;background:#fff;color:{c1};font-weight:900;font-size:15px;padding:14px 28px;border-radius:10px;text-decoration:none;margin-right:12px;">{phone}</a>' if phone else ''}
  <a href="{domain}/contact" style="display:inline-block;border:2px solid #fff;color:#fff;
    font-weight:900;font-size:15px;padding:12px 28px;border-radius:10px;text-decoration:none;">
    Contact Us
  </a>
</div>"""

    return f"""
<article style="font-family:Inter,system-ui,sans-serif;line-height:1.8;color:#1f2937;max-width:820px;">
<p style="font-size:18px;font-weight:600;color:#374151;">{subtitle}</p>

<h2 style="font-size:26px;margin:32px 0 12px;font-weight:900;color:#111827;">
  Why This Matters for Your {category.title()}
</h2>
<p>In today's competitive market, businesses that invest in the right systems — automation,
technology and smart operations — consistently outperform those that rely on manual processes.
This guide breaks down exactly what you need to know to stay ahead.</p>

<h2 style="font-size:26px;margin:32px 0 12px;font-weight:900;color:#111827;">
  Key Takeaways
</h2>
<ul style="padding-left:24px;margin:0 0 16px;">
  <li>Understanding the current landscape and what is changing in 2026</li>
  <li>Practical action steps you can take this week — not someday</li>
  <li>Common mistakes to avoid and how to course-correct quickly</li>
  <li>How {name} approaches this for our clients in {location or "your area"}</li>
</ul>

<h2 style="font-size:26px;margin:32px 0 12px;font-weight:900;color:#111827;">
  The Situation in 2026
</h2>
<p>Every industry is changing faster than ever. Customer expectations are higher, competition
is stiffer, and the cost of falling behind compounds quickly. The businesses winning right
now are the ones who have built systems — not just worked harder.</p>
<p>The good news: the tools have never been more accessible. Whether you are a solo operator
or a 50-person team, the same technology that powers enterprise operations is now available
at a fraction of the cost.</p>

<h2 style="font-size:26px;margin:32px 0 12px;font-weight:900;color:#111827;">
  Our Recommended Action Plan
</h2>
<ol style="padding-left:24px;margin:0 0 16px;">
  <li><strong>Audit your current process</strong> — where is time being lost? Where are customers dropping off?</li>
  <li><strong>Identify the highest-impact fix</strong> — the one change that would save the most time or convert the most leads</li>
  <li><strong>Build it right the first time</strong> — avoid duct-tape solutions that create more problems later</li>
  <li><strong>Measure the result</strong> — track the before/after so you can quantify the return</li>
  <li><strong>Expand from success</strong> — once one system works, replicate the approach across other bottlenecks</li>
</ol>

<h2 style="font-size:26px;margin:32px 0 12px;font-weight:900;color:#111827;">
  Frequently Asked Questions
</h2>

<h3 style="font-size:18px;margin:20px 0 6px;font-weight:800;">How quickly can we see results?</h3>
<p>Most clients see measurable improvement within the first 30 days of implementation.
The biggest wins typically come in weeks 2-4 when the new system has enough data to
show a meaningful before/after comparison.</p>

<h3 style="font-size:18px;margin:20px 0 6px;font-weight:800;">What does this cost to implement?</h3>
<p>Costs vary significantly based on scope and existing infrastructure. We offer free strategy
calls to assess your situation and give you an honest estimate before any commitment.</p>

<h3 style="font-size:18px;margin:20px 0 6px;font-weight:800;">Do we need technical staff to manage it?</h3>
<p>No. We design systems that your existing team can operate without technical training.
Complex technical maintenance is handled by us as part of the engagement.</p>

{cta}
</article>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  WEBSITE BUILDER CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class WebsiteBuilder:
    def __init__(self, site_id: int, template_name: str, config: dict):
        self.site_id       = site_id
        self.template_name = template_name
        self.t             = TEMPLATES[template_name]
        self.config        = config
        self.name          = config.get("name", "Our Business")
        self.domain        = config.get("domain", "")
        self.phone         = config.get("phone", "")
        self.email         = config.get("email", "")

    def rpc(self, model, method, args, kw=None):
        return rpc(model, method, args, kw)

    # ── website record ─────────────────────────────────────────────────────────
    def set_website_info(self):
        print("  [1] Setting website name and domain...")
        vals = {"name": self.name}
        if self.domain:
            vals["domain"] = self.domain
        self.rpc("website", "write", [[self.site_id], vals])

    # ── menus ──────────────────────────────────────────────────────────────────
    def _get_root_menu(self):
        rows = self.rpc("website.menu", "search_read",
                        [[["website_id", "=", self.site_id], ["parent_id", "=", False]]],
                        {"fields": ["id"], "limit": 1}) or []
        return rows[0]["id"] if rows else None

    def setup_menus(self):
        print("  [2] Configuring navigation menus...")
        root_id = self._get_root_menu()
        if not root_id:
            root_id = self.rpc("website.menu", "create", [{
                "name": f"Top Menu for {self.name}",
                "website_id": self.site_id,
                "url": "#",
            }])

        # Remove existing child menus
        existing = self.rpc("website.menu", "search",
                            [[["website_id", "=", self.site_id],
                              ["parent_id", "=", root_id]]]) or []
        if existing:
            self.rpc("website.menu", "unlink", [existing])

        # Create new menus from template
        for i, (name, href) in enumerate(
                zip(self.t["nav"], self.t["nav_hrefs"]), 1):
            self.rpc("website.menu", "create", [{
                "name": name,
                "url": href,
                "website_id": self.site_id,
                "parent_id": root_id,
                "sequence": i,
            }])
            print(f"     Menu {i}: {name} -> {href}")

    # ── homepage ───────────────────────────────────────────────────────────────
    def _find_homepage_view(self):
        pages = self.rpc("website.page", "search_read",
                         [[["website_id", "=", self.site_id]]],
                         {"fields": ["id", "url", "view_id"]}) or []
        home = [p for p in pages if str(p.get("url", "")) in ("/", "/home", "")]
        if home:
            v = home[0]["view_id"]
            return v[0] if isinstance(v, (list, tuple)) else v
        # Fallback: look for generic homepage view
        rows = self.rpc("ir.ui.view", "search_read",
                        [[["key", "=", "website.homepage"],
                          ["website_id", "=", False]]],
                        {"fields": ["id"], "limit": 1}) or []
        return rows[0]["id"] if rows else None

    def build_homepage(self):
        print("  [3] Building homepage...")
        view_id = self._find_homepage_view()
        arch    = homepage_html(self.t, self.config)
        vals    = {"arch_db": arch, "active": True, "website_id": self.site_id}
        base_rows = self.rpc("ir.ui.view", "search_read",
                             [[["key", "=", "website.homepage"],
                               ["website_id", "=", False]]],
                             {"fields": ["id"], "limit": 1}) or []
        if base_rows:
            vals["inherit_id"] = base_rows[0]["id"]
            vals["mode"]       = "extension"
        if view_id:
            self.rpc("ir.ui.view", "write", [[view_id], vals])
            print(f"     Updated view {view_id}")
        else:
            new_id = self.rpc("ir.ui.view", "create", [{
                **vals,
                "name": f"{self.name} Homepage",
                "type": "qweb",
                "key":  f"website.homepage_{self.site_id}",
            }])
            print(f"     Created view {new_id}")

    # ── SEO meta tags ──────────────────────────────────────────────────────────
    def setup_seo(self):
        print("  [4] Setting SEO meta tags...")
        self.rpc("website", "write", [[self.site_id], {
            "website_meta_title":       self.name,
            "website_meta_description": self.t["hero_sub"][:155],
            "website_meta_keywords":    ", ".join(
                w for svc in self.t["services"][:5] for w in svc["name"].split()[:2]
            ),
        }])

    # ── blog ───────────────────────────────────────────────────────────────────
    def _ensure_blog(self):
        blog_name = f"{self.name} Blog"
        rows = self.rpc("blog.blog", "search_read",
                        [[["name", "=", blog_name],
                          ["website_id", "=", self.site_id]]],
                        {"fields": ["id"], "limit": 1}) or []
        if rows:
            return rows[0]["id"]
        return self.rpc("blog.blog", "create", [{
            "name": blog_name, "website_id": self.site_id,
        }])

    def _get_or_create_partner(self, name):
        rows = self.rpc("res.partner", "search_read",
                        [[["name", "=", name], ["is_company", "=", False]]],
                        {"fields": ["id"], "limit": 1}) or []
        if rows:
            return rows[0]["id"]
        return self.rpc("res.partner", "create",
                        [{"name": name, "is_company": False}])

    def create_blog_posts(self):
        print("  [5] Creating blog posts...")
        blog_id = self._ensure_blog()

        # Assign a pool of English author names
        authors = [
            "James Whitfield", "Sarah Monroe", "Daniel Hargrove",
            "Emily Thornton", "Michael Ashworth",
        ]

        for i, (title, subtitle) in enumerate(self.t["blog_topics"]):
            author_name = authors[i % len(authors)]
            partner_id  = self._get_or_create_partner(author_name)
            content     = blog_post_html(title, subtitle, self.t, self.config)

            existing = self.rpc("blog.post", "search_read",
                                [[["name", "=", title],
                                  ["blog_id", "=", blog_id]]],
                                {"fields": ["id"], "limit": 1}) or []
            vals = {
                "blog_id":                  blog_id,
                "website_id":               self.site_id,
                "name":                     title,
                "subtitle":                 subtitle,
                "content":                  content,
                "author_id":                partner_id,
                "website_meta_title":       title[:60],
                "website_meta_description": subtitle[:155],
                "website_published":        True,
                "is_published":             True,
                # Safe cover_properties — no external URL to avoid og:image crash
                "cover_properties": json.dumps({
                    "background-image":  "none",
                    "background_color_class": "o_cc3",
                    "opacity":           "0.2",
                    "resize_class":      "",
                }),
            }
            if existing:
                self.rpc("blog.post", "write", [[existing[0]["id"]], vals])
                print(f"     Updated: {title[:60]}")
            else:
                self.rpc("blog.post", "create", [vals])
                print(f"     Created: {title[:60]}")
            time.sleep(0.2)

    # ── run all ────────────────────────────────────────────────────────────────
    def run(self):
        print("=" * 70)
        print(f"  Odoo Website Builder — {self.template_name.upper()}")
        print(f"  Site: {self.site_id} | Name: {self.name}")
        print(f"  Domain: {self.domain}")
        print("=" * 70 + "\n")

        self.set_website_info()
        self.setup_menus()
        self.build_homepage()
        self.setup_seo()
        self.create_blog_posts()

        print("\n" + "=" * 70)
        print(f"  DONE — visit {self.domain} to see the result")
        print("=" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Build a complete Odoo website for any business category.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(f"""
        Categories: {', '.join(TEMPLATES.keys())}

        Example:
          python odoo_website_builder.py \\
              --site 41 --category agency \\
              --name "JHD Advisor" \\
              --domain "https://www.jhdadvisor.com" \\
              --phone "+1 (917) 338-7086" \\
              --email "info@jhdadvisor.com" \\
              --location "Long Island, NY"
        """))

    parser.add_argument("--site",     type=int, required=True, help="Odoo website ID")
    parser.add_argument("--category", required=True,
                        choices=list(TEMPLATES.keys()), help="Website category")
    parser.add_argument("--name",     required=True, help="Business name")
    parser.add_argument("--domain",   default="",    help="Full domain URL")
    parser.add_argument("--phone",    default="",    help="Phone number")
    parser.add_argument("--email",    default="",    help="Email address")
    parser.add_argument("--location", default="",    help="City, State")
    parser.add_argument("--tagline",  default="",    help="Custom hero headline (overrides template)")
    parser.add_argument("--color1",   default="",    help="Primary color hex e.g. #7c3aed")
    parser.add_argument("--color2",   default="",    help="Accent color hex e.g. #06b6d4")

    args = parser.parse_args()

    config = {
        "name":     args.name,
        "domain":   args.domain,
        "phone":    args.phone,
        "email":    args.email,
        "location": args.location,
        "tagline":  args.tagline,
    }

    # Apply custom colors if provided
    if args.color1:
        TEMPLATES[args.category]["color1"] = args.color1
    if args.color2:
        TEMPLATES[args.category]["color2"] = args.color2
    # Apply custom tagline if provided
    if args.tagline:
        TEMPLATES[args.category]["hero_headline"] = args.tagline

    builder = WebsiteBuilder(args.site, args.category, config)
    builder.run()


if __name__ == "__main__":
    main()
