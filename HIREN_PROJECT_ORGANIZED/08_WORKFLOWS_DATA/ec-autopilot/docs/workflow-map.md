# Workflow Map — EC-Autopilot

## Master Flow Diagram

```
TELEGRAM BOT (@ecAutopilot_bot)
         │
         ├─── /addproduct ──────────► WF-01: Product Sync
         │                                    │
         │                                    ├── WF-16: AI Description
         │                                    ├── All 7 WooCommerce Stores
         │                                    └── WF-19: Launch Campaign
         │                                              ├── WF-17: Social Post
         │                                              └── WF-18: Email Blast
         │
         ├─── /writeblog ───────────► WF-02: SEO Blog Generator
         │                                    │
         │                                    └── WordPress (longislandconvenience.com)
         │
         ├─── /createad ────────────► WF-05: Ad Campaign Creator
         │                                    │
         │                                    ├── Meta Ads Draft
         │                                    └── Google Ads Draft
         │
         ├─── /videoscript ─────────► WF-15: Video Script Generator
         │                                    └── Claude → Script → Telegram reply
         │
         ├─── /report ──────────────► WF-20: KPI Report (on-demand)
         │
         └─── Customer message ─────► WF-09: Support Bot
                                              │
                                              ├── Claude answers
                                              ├── WF-10: Odoo ticket (if unresolved)
                                              └── WF-11: Order status lookup


CRON SCHEDULES (Automatic, No trigger needed)
         │
         ├── Daily 8 AM  ──────────► WF-14: Social Post Generator
         ├── Daily 9 AM  ──────────► WF-02: SEO Blog (geo-targeted)
         ├── Daily 10 AM ──────────► WF-17: Social Media Auto-Poster
         ├── Every 4 hrs ──────────► WF-03: Inventory Sync
         ├── Mon 8 AM    ──────────► WF-20: Weekly KPI Report
         ├── Mon 9 AM    ──────────► WF-18: Email Campaign
         └── 1st of Month ─────────► WF-21: Monthly Dashboard


ODOO CRM TRIGGERS (Event-based)
         │
         ├── Lead created ──────────► WF-07: Follow-up Email Sequence
         ├── Lead = Interested ─────► WF-08: Call Scheduling
         └── Ticket closed ─────────► WF-12: Resolution Follow-up Email


WOOCOMMERCE WEBHOOKS
         │
         ├── New order ─────────────► WF-11: Order Status Handling
         └── Low stock ─────────────► WF-03: Inventory Alert → Supplier email
```

---

## Data Flow — Product Add (WF-01)

```
Telegram /addproduct
    → n8n receives product name + image + price + category
    → Claude API generates:
        - Product title (SEO optimized)
        - Short description (local Long Island angle)
        - Long description (benefits, local delivery mention)
        - Meta title + meta description
        - Tags: "Long Island", "Plainview", "convenience store near me"
    → OpenAI DALL-E generates product lifestyle image (if no image given)
    → n8n loops through all 7 WooCommerce stores:
        - POST /wp-json/wc/v3/products on each store
        - Uploads image to each store media library
    → Triggers WF-19 (Launch Campaign):
        - Creates social post for IG + FB
        - Sends email blast to Mailchimp list
    → Sends success confirmation to Telegram
```

---

## Data Flow — SEO Blog (WF-02)

```
Daily cron 9 AM (or /writeblog command)
    → n8n picks blog topic from rotating list:
        - "Best convenience store snacks in Plainview NY"
        - "Late night delivery Long Island — what's open near you"
        - "Weekly grocery deals Hicksville and Bethpage"
        - "Same day delivery Long Island convenience items"
    → Claude API generates:
        - Blog title (geo-keyword rich)
        - 800-1200 word article body
        - Meta description
        - 5 internal links to product pages
        - Featured image prompt
    → OpenAI generates featured image
    → n8n publishes to WordPress via REST API:
        - POST /wp-json/wp/v2/posts
        - Sets category, tags, featured image, SEO fields (Yoast)
    → Auto-shares to Facebook Page
    → Sends Telegram confirmation with live URL
```

---

## Data Flow — Support Bot (WF-09)

```
Customer sends message to @ecAutopilot_bot
    → n8n Telegram webhook fires
    → Check if order status query:
        YES → pull WooCommerce order by email/order# → reply
        NO  → send to Claude with context:
              "You are support agent for Long Island Convenience Store.
               Answer helpfully. If you can't resolve, say so."
    → Claude replies
    → n8n saves conversation to Odoo helpdesk ticket
    → If flagged/unresolved → assigns to human agent in Odoo
    → Human closes ticket → WF-12 sends follow-up satisfaction email
```

---

## API Calls Reference

| Service | Endpoint Pattern | Used In |
|---------|-----------------|---------|
| Claude | POST api.anthropic.com/v1/messages | WF-01,02,05,09,13,14,15,16,20 |
| WooCommerce | POST {store}/wp-json/wc/v3/products | WF-01,03,04 |
| WordPress | POST {site}/wp-json/wp/v2/posts | WF-02,13 |
| Meta Graph | POST /me/feed, /me/photos | WF-17,19 |
| Odoo JSONRPC | POST /web/dataset/call_kw | WF-06,10,12 |
| Mailchimp | POST /3.0/campaigns, /actions/send | WF-18,19 |
| Telegram | POST /bot{token}/sendMessage | All WFs |
| OpenAI Images | POST api.openai.com/v1/images/generations | WF-01,02,13,14 |

---

*Updated: 2026-05-25*
