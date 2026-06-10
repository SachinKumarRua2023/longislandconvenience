# n8n Automation Workflow Plan
## Hiren Kumar Digital Ecosystem | SeekHowItHRua

---

## Why n8n Over Make.com

| Factor | n8n (Self-Hosted) | Make.com |
|--------|------------------|---------|
| Cost | ~$20/mo (VPS only) | $29-$299/mo based on executions |
| Executions | Unlimited | Limited by plan |
| Data privacy | Your server | Their cloud |
| Customization | Full Node.js code | Visual only |
| Long-term cost | Low | Scales with usage |
| **Verdict** | **WINNER for volume** | Backup for complex integrations |

**Decision: n8n self-hosted on Hostinger VPS as primary. Make.com for specific integrations that require it.**

---

## Workflow Inventory

### WF-001 — New Customer Welcome Sequence
**Trigger:** New Odoo contact created (email signup or first purchase)
**Flow:**
1. Wait 5 minutes (prevent duplicate triggers)
2. Send Welcome Email (Odoo Mail template)
3. Send WhatsApp welcome message (Twilio)
4. Add to "New Customers" email segment
5. Schedule Day 3 follow-up check

**n8n Nodes:** Odoo Trigger → Wait → HTTP (Odoo Email) → HTTP (Twilio WA) → Odoo (update tag)

---

### WF-002 — Order Confirmation
**Trigger:** New order created in Odoo (any of 7 stores)
**Flow:**
1. Extract order details (customer name, items, total, estimated delivery)
2. Send order confirmation email (HTML template with order summary)
3. Send WhatsApp confirmation (text + emoji summary)
4. Update CRM: mark as "active buyer"

---

### WF-003 — Cart Abandonment Recovery
**Trigger:** Odoo cart inactive for 1 hour (webhook)
**Flow:**
- Hour 1: "You left something behind" email + WhatsApp
- Hour 24: "Still interested?" email with 5% discount code
- Hour 72: "Last chance" email with 10% discount
- If purchase made: Cancel remaining messages, send thank you

---

### WF-004 — Social Media Auto-Posting
**Trigger:** Content approved in content management spreadsheet/Odoo note
**Flow:**
1. Fetch approved content (image/video URL, caption, hashtags)
2. Post to Instagram (Meta Graph API)
3. Post to Facebook Page (Meta Graph API)
4. Post to TikTok (TikTok API)
5. Post to Pinterest (Pinterest API)
6. Post to Twitter/X (Twitter API v2)
7. Upload to YouTube (YouTube Data API — for long videos)
8. Log result (success/fail) to Odoo activity
9. Alert team on Telegram/WhatsApp if any post fails

---

### WF-005 — Blog Content Automation
**Trigger:** Weekly schedule (Monday 9 AM)
**Flow:**
1. Pull top 5 trending keywords for Long Island from Google Trends API
2. Check existing blog for gaps (n8n HTTP call to Odoo CMS)
3. Send keyword list to Claude API: generate full blog article (1,500 words)
4. Generate featured image via DALL-E 3
5. Create draft in Odoo Website CMS
6. Notify content manager via WhatsApp for review
7. Publish on approval (or auto-publish if enabled)

---

### WF-006 — Short Video Creation Pipeline
**Trigger:** Product/trend alert OR manual trigger from content team
**Flow:**
1. Research hook: scrape TikTok trending sounds + hashtags
2. Write video script (Claude API, 30-60 seconds)
3. Generate voiceover (ElevenLabs API)
4. Generate B-roll clips (Runway ML API)
5. Assemble video (n8n HTTP call to video assembly service)
6. Add captions + branding watermark
7. Send to content manager for review (WhatsApp preview link)
8. On approval → WF-004 auto-posting

---

### WF-007 — Lead Management
**Trigger:** New form submission (any of 7 websites) OR social media DM keyword detection
**Flow:**
1. Create Odoo CRM lead (name, email, phone, source, message)
2. Assign to available sales rep (round-robin)
3. Send internal notification (WhatsApp to rep + email)
4. Send external acknowledgment email to lead
5. Start follow-up sequence: Day 1, Day 3, Day 7
6. If no response Day 7 → add to long-term nurture list

---

### WF-008 — Review Request Automation
**Trigger:** Order status changed to "Delivered" in Odoo
**Flow:**
1. Wait 3 days post-delivery
2. Send review request email: "How did we do?" + Google review link
3. Send WhatsApp follow-up 24h later if email not opened
4. If review posted (monitored via Google Places API): send thank you + loyalty points
5. If 1-2 star review: alert management immediately via WhatsApp

---

### WF-009 — Birthday Campaign
**Trigger:** Daily check — customer birthday = today (Odoo scheduled action)
**Flow:**
1. Query Odoo for customers with today's birthday
2. Generate personalized birthday discount code (15% off, 7-day validity)
3. Send birthday email with code + animated GIF greeting
4. Send WhatsApp birthday message with code
5. Send push notification (mobile app)

---

### WF-010 — VOIP Call Summary
**Trigger:** Twilio call ends (webhook)
**Flow:**
1. Fetch call recording from Twilio
2. Transcribe with OpenAI Whisper
3. Summarize key points (Claude API)
4. Create Odoo CRM note with summary
5. If new contact mentioned: create Odoo lead
6. Send summary to manager via WhatsApp

---

### WF-011 — Inventory Alert
**Trigger:** Odoo inventory item below reorder point
**Flow:**
1. Identify low-stock product and supplier
2. Draft purchase order in Odoo
3. Alert inventory manager via WhatsApp
4. If auto-reorder enabled: submit PO automatically
5. Update product page "Low Stock" badge

---

### WF-012 — Performance Report
**Trigger:** Every Monday 8 AM
**Flow:**
1. Pull last 7 days data from Odoo (orders, revenue, new customers)
2. Pull social media analytics (Instagram Insights, TikTok, YouTube)
3. Pull email campaign stats from Odoo Email Marketing
4. Compile into formatted PDF report (n8n PDF generation)
5. Email report to Hiren + Sachin
6. Post summary to internal Telegram channel

---

## n8n Server Setup

```bash
# Hostinger VPS — Ubuntu 22.04
# Minimum: 2 CPU, 4GB RAM, 50GB SSD

# Install n8n via Docker
docker-compose.yml:
  n8n:
    image: n8nio/n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=[SECURE]
      - WEBHOOK_URL=https://n8n.yourdomain.com
      - N8N_ENCRYPTION_KEY=[32-char-key]
    volumes:
      - n8n_data:/home/node/.n8n
    ports:
      - "5678:5678"
```

**Access URL:** https://n8n.hirenautomation.com (or subdomain of choice)

---
