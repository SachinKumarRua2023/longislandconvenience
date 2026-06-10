# EC-Autopilot — Full AI E-Commerce Automation System

> AI-powered, department-by-department automation for Long Island Convenience and all 7 stores.
> Brain: Claude AI | Gateway: Telegram Bot (@ecAutopilot_bot) | CRM: Odoo | Automation: n8n

---

## Project Overview

This system automates every operational department of a full e-commerce business —
from adding a product to all 7 stores, generating geo-targeted SEO blogs, running
ad campaigns, handling customer support, and delivering weekly reports — all on autopilot.

**Primary Store:** longislandconvenience.com
**Target Market:** Long Island, Plainview, Hicksville, Syosset, NY area
**Total Workflows:** 21 n8n automations across 6 departments

---

## Folder Structure

```
ec-autopilot/
├── .env                        ← All API credentials (never share/commit)
├── README.md                   ← This file
├── workflows/
│   ├── 01-ecommerce/           ← Product sync, blog, inventory
│   ├── 02-sales/               ← Ads, leads, call automation
│   ├── 03-support/             ← Telegram bot, CRM, tickets
│   ├── 04-content/             ← Posts, blogs, video scripts
│   ├── 05-marketing/           ← Email, social posting, SEO
│   └── 06-reporting/           ← Weekly/monthly dashboards
└── docs/
    └── workflow-map.md         ← Full workflow diagram and logic
```

---

## Department Workflows

### 01 — E-Commerce (4 Workflows)

| # | Workflow | Trigger | What it Does |
|---|----------|---------|--------------|
| WF-01 | Product Add & Sync | Telegram command or form | Add product once → auto-syncs to all 7 stores with Claude-written description |
| WF-02 | SEO Geo Blog Generator | Daily cron (9 AM) | Claude writes Long Island/Plainview targeted blog → auto-publishes to WP |
| WF-03 | Inventory Sync | Every 4 hours | Syncs stock levels across all stores |
| WF-04 | Price Update Broadcast | Manual trigger | Change price in master → updates all 7 stores |

---

### 02 — Sales Department (4 Workflows)

| # | Workflow | Trigger | What it Does |
|---|----------|---------|--------------|
| WF-05 | Ad Campaign Creator | Telegram command | Claude writes ad copy → creates Meta/Google campaign draft |
| WF-06 | Lead Capture → Odoo | Form submission / FB Lead Ad | New lead → auto-creates contact in Odoo CRM + assigns salesperson |
| WF-07 | Lead Follow-up Sequence | Lead created in Odoo | Sends 3-email nurture sequence over 7 days via SMTP |
| WF-08 | Call Scheduling | Lead status = "Interested" | Books call slot → sends calendar invite to lead + salesperson |

---

### 03 — Support Department (4 Workflows)

| # | Workflow | Trigger | What it Does |
|---|----------|---------|--------------|
| WF-09 | Telegram Customer Bot | Customer message | Claude answers query; escalates if needed; logs to Odoo |
| WF-10 | Support Ticket → Odoo | Any unresolved query | Creates helpdesk ticket in Odoo with full conversation |
| WF-11 | Order Status Bot | Customer asks "where is my order" | Pulls WooCommerce order status → replies instantly |
| WF-12 | Query Resolution Email | Ticket closed in Odoo | Sends satisfaction follow-up email to customer |

---

### 04 — Content Creation (4 Workflows)

| # | Workflow | Trigger | What it Does |
|---|----------|---------|--------------|
| WF-13 | Blog Post Generator | Daily cron / Telegram | Claude generates SEO blog → publishes to WP with featured image |
| WF-14 | Social Post Generator | Daily cron (8 AM) | Creates 3 posts per day (product, tip, promo) with image captions |
| WF-15 | Video Script Generator | Telegram command | Claude writes 60-sec product video script + hook + CTA |
| WF-16 | Product Description AI | WF-01 sub-workflow | Claude writes compelling product copy + SEO meta for each new product |

---

### 05 — Marketing Department (3 Workflows)

| # | Workflow | Trigger | What it Does |
|---|----------|---------|--------------|
| WF-17 | Social Media Auto-Poster | Daily 10 AM | Posts generated content to FB + Instagram automatically |
| WF-18 | Email Campaign Sender | Weekly Monday 9 AM | Sends promo email to Mailchimp list — AI-written subject + body |
| WF-19 | New Product Launch Campaign | WF-01 trigger | When product added → auto-posts to social + sends email blast |

---

### 06 — Reporting (2 Workflows)

| # | Workflow | Trigger | What it Does |
|---|----------|---------|--------------|
| WF-20 | Weekly KPI Report | Every Monday 8 AM | GA4 + WooCommerce data → Claude summarizes → emails client |
| WF-21 | Monthly Performance Dashboard | 1st of month | Full revenue, traffic, leads, ad spend report → Google Sheets + email |

---

## Telegram Bot Commands

| Command | Action |
|---------|--------|
| `/addproduct` | Trigger product add to all 7 stores |
| `/writeblog` | Generate and publish a geo-targeted SEO blog |
| `/createad` | Generate ad copy and create campaign draft |
| `/report` | Get latest KPI summary |
| `/videoscript [product name]` | Generate 60-sec video script |
| `/status` | Show all workflow statuses |
| `/support` | Open customer support mode |

---

## AI Brain — Claude Integration

All workflows that generate content call Claude API with:
- **Geo context:** Long Island, Plainview, Hicksville, NY
- **Brand voice:** Friendly, local, trustworthy convenience store
- **SEO focus:** Local keywords — "near me", "Long Island delivery", "Plainview grocery"
- **Model:** claude-sonnet-4-6

---

## Setup Checklist

- [ ] Revoke old Telegram token → get new one from @BotFather → add to `.env`
- [ ] Add Claude API key to `.env`
- [ ] Add WooCommerce API keys for all 7 stores to `.env`
- [ ] Add Odoo API credentials to `.env`
- [ ] Add Meta API credentials to `.env`
- [ ] Configure n8n webhook base URL in `.env`
- [ ] Import workflow JSONs from `workflows/` folders into n8n
- [ ] Test WF-01 (product sync) end-to-end first
- [ ] Activate all cron workflows

---

## Build Order (Today)
0. Clone of real e-commerce and other website first
******************Layout Design Auotomation*******************

a.Taking the inspiration of atleast 3-10 websites
feature counting like menu and category and other features understanding and implementing
b.And ai brain to redesign

1. WF-01 — Product Add & Sync (core, everything depends on it)

2. WF-09 — Telegram Support Bot (Telegram is live, build first)

3. WF-02 — SEO Blog Generator (high value for longislandconvenience.com)

4. WF-14 — Social Post Generator

5. WF-17 — Social Media Auto-Poster

6. WF-06 — Lead Capture → Odoo

7. WF-20 — Weekly KPI Report

---

## Security Rules

- Never share `.env` file
- Never paste API tokens in Telegram or chat
- Rotate all tokens immediately if accidentally exposed
- `.env` is gitignored — do not commit it

---

*Last updated: 2026-05-25 | PM: Sachin | Client: Hiren Kumar / Long Island Convenience*
