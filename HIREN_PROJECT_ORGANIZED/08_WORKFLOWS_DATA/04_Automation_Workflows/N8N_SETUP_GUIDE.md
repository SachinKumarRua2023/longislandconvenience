# n8n Setup Guide — Long Island Brand Network
## Country Cove Inc | Sachin PM | May 2026

---

## STEP 1 — Install n8n on Hostinger VPS

### 1.1 Connect to VPS
```bash
ssh root@YOUR_VPS_IP
# Password: M@nhattan1083
```

### 1.2 Install n8n (recommended: Docker)
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker && systemctl start docker

# Install n8n with docker-compose
mkdir -p /opt/n8n && cd /opt/n8n

cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=0.0.0.0
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://YOUR_DOMAIN_OR_IP:5678
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=M@nhattan1234
      - EXECUTIONS_DATA_SAVE_ON_SUCCESS=all
      - EXECUTIONS_DATA_SAVE_ON_ERROR=all
      - N8N_ENCRYPTION_KEY=longislandccnc2026secretkey32chr
      - GENERIC_TIMEZONE=America/New_York
      - TZ=America/New_York
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
EOF

docker-compose up -d
```

### 1.3 Access n8n
- URL: `http://YOUR_VPS_IP:5678`
- Username: `admin`
- Password: `M@nhattan1234`

---

## STEP 2 — Import Workflows

1. In n8n, go to **Workflows** → **Import from File**
2. Import in this order:
   - `WF-A-SOCIAL-BLAST.json` (import first — WF-B depends on it)
   - `WF-B-DAILY-BLOG.json`
3. After import, WF-A will give you a webhook URL like:
   `https://YOUR_VPS_IP:5678/webhook/social-blast`
4. Copy that URL into WF-B node `HTTP: Trigger WF-A Social Blast`

---

## STEP 3 — Set Up Credentials in n8n

Go to **n8n** → **Settings** → **Credentials** → **New Credential**

### 3.1 Anthropic Claude API
- Type: **HTTP Header Auth**
- Name: `Anthropic Claude API`
- Header: `x-api-key`
- Value: `YOUR_ANTHROPIC_API_KEY`
- Also add: Header `anthropic-version` = `2023-06-01`

Get key at: https://console.anthropic.com/settings/keys

### 3.2 OpenAI API (for DALL-E 3)
- Type: **HTTP Header Auth**
- Name: `OpenAI API`
- Header: `Authorization`
- Value: `Bearer YOUR_OPENAI_API_KEY`

Get key at: https://platform.openai.com/api-keys

### 3.3 Meta Graph API (Facebook + Instagram)
- Type: **HTTP Header Auth**
- Name: `Meta Graph API`
- Header: `Authorization`
- Value: `Bearer YOUR_META_PAGE_ACCESS_TOKEN`

**How to get Meta Page Access Token:**
1. Go to https://developers.facebook.com/
2. Create App → Business → Get App ID + Secret
3. Add Facebook Login + Instagram Graph API products
4. In Graph API Explorer → select your page → generate long-lived token
5. Exchange for 60-day long-lived token (or permanent with System User):
   ```
   GET https://graph.facebook.com/v19.0/oauth/access_token
     ?grant_type=fb_exchange_token
     &client_id=APP_ID
     &client_secret=APP_SECRET
     &fb_exchange_token=SHORT_LIVED_TOKEN
   ```

**Get Instagram Business Account ID:**
```
GET https://graph.facebook.com/v19.0/me/accounts?access_token=PAGE_TOKEN
# Find your page → get its id
GET https://graph.facebook.com/v19.0/PAGE_ID?fields=instagram_business_account&access_token=PAGE_TOKEN
# Returns instagram_business_account.id
```

### 3.4 Pinterest API
- Type: **HTTP Header Auth**
- Name: `Pinterest API`
- Header: `Authorization`
- Value: `Bearer YOUR_PINTEREST_ACCESS_TOKEN`

Get token at: https://developers.pinterest.com/apps/

### 3.5 Twitter/X API
- Type: **HTTP Header Auth**
- Name: `Twitter OAuth2`
- Header: `Authorization`
- Value: `Bearer YOUR_TWITTER_BEARER_TOKEN`

Or use OAuth2 User Context:
1. Go to https://developer.twitter.com/
2. Create app → Enable OAuth 2.0
3. Scopes: `tweet.write`, `users.read`, `offline.access`

### 3.6 LinkedIn API
- Type: **HTTP Header Auth**
- Name: `LinkedIn API`
- Header: `Authorization`
- Value: `Bearer YOUR_LINKEDIN_ACCESS_TOKEN`

Get at: https://www.linkedin.com/developers/apps

---

## STEP 4 — Fill in Brand IDs in WF-A

Open WF-A → `Code: Prepare Platform Content` node → fill in:

```javascript
const BRAND_CONFIGS = {
  longislandconvenience: {
    fb_page_id:    'YOUR_FACEBOOK_PAGE_ID',       // from Graph API Explorer
    ig_account_id: 'YOUR_IG_BUSINESS_ACCOUNT_ID', // from /me/accounts
    pinterest_board_id: 'YOUR_PINTEREST_BOARD_ID', // from Pinterest API
    linkedin_org_id: null,                          // optional for LIC
    ...
  },
  ...
};
```

**To get Facebook Page ID:**
```
GET https://graph.facebook.com/v19.0/me/accounts?access_token=TOKEN
```
Returns list of pages with their IDs.

**To get Pinterest Board ID:**
```
GET https://api.pinterest.com/v5/boards
Authorization: Bearer YOUR_TOKEN
```

---

## STEP 5 — Odoo Session for WF-B

The `HTTP: Odoo — Create Blog Post` node needs a session cookie.

**Option A (Quick):** Run `get_odoo_session.py` and paste the cookie.
```bash
cd "04_Automation_Workflows"
python get_odoo_session.py
```
Copy the `session_id=...` value into the Cookie header in WF-B.

**Option B (Better, long-term):** Add an Odoo authenticate node BEFORE the blog post node:
1. Add HTTP Request node at start of WF-B
2. POST to `https://country-cove-inc.odoo.com/web/session/authenticate`
3. Body: `{"jsonrpc":"2.0","method":"call","params":{"db":"country-cove-inc","login":"countrycoveinc@gmail.com","password":"M@nhattan1234"}}`
4. Set it to send cookies and store them for subsequent calls

---

## STEP 6 — API Keys to Obtain (Priority Order)

| Priority | Service | Purpose | Cost/Month | Get At |
|----------|---------|---------|-----------|--------|
| 1 | Meta Developer | FB + IG posting | FREE | developers.facebook.com |
| 2 | Anthropic Claude | Blog writing | ~$20-40 | console.anthropic.com |
| 3 | OpenAI | DALL-E 3 images | ~$20-40 | platform.openai.com |
| 4 | SerpAPI | Google Trends | ~$50 (100 calls/mo free) | serpapi.com |
| 5 | Pinterest API | Pinterest posts | FREE | developers.pinterest.com |
| 6 | Twitter/X API | Twitter posts | $100/mo Basic | developer.twitter.com |
| 7 | LinkedIn API | LinkedIn posts | FREE (limited) | linkedin.com/developers |
| 8 | ElevenLabs | Video voiceover (WF-C) | ~$22 | elevenlabs.io |
| 9 | Shotstack | Video assembly (WF-C) | ~$49 | shotstack.io |

**Start with:** Meta + Claude + OpenAI (3 keys = FB, IG, blog writing, images working)

---

## STEP 7 — Test Workflows

### Test WF-A (Social Blast)
Send this to the webhook URL using curl or Postman:
```json
POST https://YOUR_N8N_URL:5678/webhook/social-blast
Content-Type: application/json

{
  "brand": "longislandconvenience",
  "content_type": "promotion",
  "text": "Stop by Long Island Convenience today! Gift baskets, balloons, sports cards and more. Plainview NY.",
  "text_long": "Looking for the perfect gift in Plainview, Long Island? We have it all! Custom gift baskets starting at $35, balloon arrangements for any occasion, graded sports cards, and same-day print & mail services. Come see us at 605 Old Country Road, Plainview NY 11803.",
  "image_url": "https://via.placeholder.com/1080x1080.png?text=Long+Island+Convenience",
  "link_url": "https://www.longislandconvenience.com",
  "hashtags": ["LongIsland", "PlainviewNY", "NassauCounty", "ShopLocal"],
  "platforms": ["facebook", "instagram"]
}
```

### Test WF-B (Daily Blog)
- Open WF-B → Click **Test Workflow** (runs once manually)
- Check Odoo → Website → Blog → Long Island News for new post
- Check WF-A webhook was triggered

---

## STEP 8 — Go Live

1. Activate WF-A: Toggle **Active** switch in n8n
2. Activate WF-B: Toggle **Active** switch in n8n
3. Monitor: n8n → Executions tab (check for errors daily)

---

## Blog ID Reference (LongIslandConvenience.com)

| Blog ID | Blog Name | Use For |
|---------|-----------|---------|
| 6 | Long Island News | **Daily auto-blog** (WF-B uses this) |
| 7 | Convenience & Grocery | Grocery/convenience posts |
| 3 | Balloons & Party Decor | Balloon event posts |
| 5 | Gift Baskets & Gifts | Gift basket posts |
| 2 | Sports & Trading Cards | Cards posts |
| 4 | Print & Mail Services | Printing posts |

---

## Quick Reference — Odoo Credentials

```
URL:   https://country-cove-inc.odoo.com
DB:    country-cove-inc
User:  countrycoveinc@gmail.com
Pass:  M@nhattan1234
```

**Websites:**
- WID=1  → longislandconvenience.com
- WID=36 → longislandcards.com
- WID=37 → ligiftbasket.com
- WID=38 → longislandballoonsdecor.com
- WID=39 → longislandprintandmail.com
- WID=41 → jhdadvisor.com
