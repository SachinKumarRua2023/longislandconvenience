# Daily SEO Blog Workflow — Setup Guide

## File to Import
`WF-BLOG-DAILY-FINAL.json`

---

## What This Does

**Every day at 10:00 AM ET** (Eastern Time, auto-handles DST):
1. Picks today's SEO topic from 30 rotating topics (graduation, balloons, gift baskets, greeting cards)
2. Calls Claude API to write a 750–900 word geo-targeted blog post
3. Authenticates to Odoo via JSON-RPC
4. Creates + publishes the post on **longislandconvenience.com**
5. Logs the live URL and Google Search Console inspection link

---

## Step 1 — Import the Workflow

1. n8n → **Workflows → Import from File**
2. Select: `WF-BLOG-DAILY-FINAL.json`
3. Click **Import**

---

## Step 2 — Activate

1. Toggle **Inactive → Active** at the top right
2. First run: **10:00 AM ET** tomorrow

> **No credentials to set up.** Claude API key (`sk-ant-api03-cSj82...`) and Odoo credentials are already embedded — just import and activate.

---

## Manual Test (Optional)

Click **Test Workflow** to run it immediately and verify:
- Claude generates a blog post
- Odoo auth succeeds
- Blog post appears on https://www.longislandconvenience.com/blog

---

## Topic Rotation (30 Topics)

| # | Category | Blog Section | Focus Keyword |
|---|----------|-------------|---------------|
| 1 | Balloons | Balloons & Party | Graduation Balloon Decorations Long Island |
| 2 | Gift Baskets | Gift Baskets | Graduation Gift Baskets Long Island NY |
| 3 | Greeting Cards | Convenience | Graduation Greeting Cards Near Plainview NY |
| 4 | Balloons | Balloons & Party | Balloon Arch Setup Graduation Nassau County |
| 5 | Gift Baskets | Gift Baskets | Personalized Graduation Gifts Plainview NY |
| 6 | Balloons | Balloons & Party | Birthday Balloon Delivery Long Island Same Day |
| 7 | Balloons | Balloons & Party | Baby Shower Balloon Garland Nassau County |
| 8 | Balloons | Balloons & Party | Helium Balloons Plainview NY Same Day Pickup |
| 9 | Balloons | Balloons & Party | Corporate Event Balloons Long Island NY |
| 10 | Balloons | Balloons & Party | Wedding Balloon Decorations Nassau County |
| 11 | Gift Baskets | Gift Baskets | Father's Day Gift Baskets Long Island NY |
| 12 | Gift Baskets | Gift Baskets | Birthday Gift Baskets Nassau County |
| 13 | Gift Baskets | Gift Baskets | Corporate Gift Baskets Long Island |
| 14 | Gift Baskets | Gift Baskets | Thank You Gift Baskets Nassau County |
| 15 | Gift Baskets | Gift Baskets | Baby Shower Gift Baskets Long Island |
| 16 | Greeting Cards | Convenience | Greeting Cards for Every Occasion Plainview |
| 17 | Greeting Cards | Convenience | Father's Day Cards Long Island 2026 |
| 18 | Greeting Cards | Convenience | Birthday Cards and Gifts Long Island |
| 19 | Greeting Cards | Convenience | Sympathy Cards Nassau County |
| 20 | Greeting Cards | Convenience | Holiday Cards and Gift Wrap Long Island |
| 21 | Balloons | Balloons & Party | July 4th Patriotic Balloons Long Island |
| 22 | Balloons | Balloons & Party | Halloween Balloon Decorations Nassau County |
| 23 | Balloons | Balloons & Party | Valentine's Day Balloon Bouquet Long Island |
| 24 | Gift Baskets | Gift Baskets | Holiday Gift Baskets Christmas Hanukkah |
| 25 | Gift Baskets | Gift Baskets | Mother's Day Gift Basket Long Island |
| 26 | Gift Baskets | Gift Baskets | Same Day Gift Ideas Plainview NY |
| 27 | Balloons | Balloons & Party | Best Party Supplies Store Long Island |
| 28 | General | Convenience | Long Island Convenience Store Plainview NY |
| 29 | Balloons | Balloons & Party | Balloon and Gift Bundle Nassau County |
| 30 | Balloons | Balloons & Party | Graduation 2026 Party Planning Long Island |

Topics cycle by day of year — each runs once every 30 days.

---

## SEO / GEO Keywords Targeted

**Primary Geo:** Long Island, Plainview NY, Nassau County, Suffolk County  
**Service Keywords:**
- graduation balloons Long Island NY
- balloon arch Nassau County
- gift basket Long Island same day
- graduation gift basket Plainview NY
- greeting cards near me Long Island
- same day balloon delivery Nassau County
- balloon bouquet delivery Long Island
- balloon decoration Plainview NY
- gift basket graduation Nassau County
- party supplies Long Island

---

## Blog Sections Used

| Odoo Blog ID | Section Name | Posts Published To |
|---|---|---|
| 3 | Balloons & Party Decor | Balloon/graduation/party posts |
| 5 | Gift Baskets & Gifts | Gift basket posts |
| 7 | Convenience & Grocery | Greeting cards / general |

---

## Live Blog URLs

| Blog Section | URL |
|---|---|
| All posts | https://www.longislandconvenience.com/blog |
| Balloons & Party | https://www.longislandconvenience.com/blog/balloons-party-decor-3 |
| Gift Baskets | https://www.longislandconvenience.com/blog/gift-baskets-gifts-5 |
| Convenience/Cards | https://www.longislandconvenience.com/blog/convenience-grocery-7 |

**Example URL pattern Odoo generates:**
```
https://www.longislandconvenience.com/blog/balloons-party-decor-3/graduation-balloon-decorations-long-island-ny-2026-38
```

---

## Google Search Console — Indexing Inspection

After each post, the workflow logs a GSC URL. To request indexing:

1. Go to: https://search.google.com/search-console/
2. Property: `https://www.longislandconvenience.com/`
3. URL Inspection → paste the blog post URL → **Request Indexing**

> Google typically indexes new pages within 24-72 hours. With daily fresh content, the site will build strong crawl frequency over time.

---

## Odoo Credentials Used (Hardcoded in Workflow)

These are baked into the workflow Code nodes — no separate credential needed for Odoo:

| Field | Value |
|---|---|
| Instance | https://country-cove-inc.odoo.com |
| DB | country-cove-inc |
| Login | countrycoveinc@gmail.com |
| UID | 2 |

---

## Schedule: Why 10 AM ET?

Research shows blog posts published at **9–11 AM ET on weekdays** receive:
- 30% more organic traffic in first 24 hours
- Higher Google crawl priority (Googlebot US-East crawls heavily in morning)
- More social shares (people browse at work morning break)

Eastern Time = UTC-5 (EST, Nov–Mar) / UTC-4 (EDT, Mar–Nov)  
n8n cron `0 10 * * *` with timezone `America/New_York` handles DST automatically.
