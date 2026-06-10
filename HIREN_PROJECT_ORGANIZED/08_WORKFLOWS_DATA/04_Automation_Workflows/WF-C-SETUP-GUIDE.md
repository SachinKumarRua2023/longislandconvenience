# WF-C — AI Tech YouTube Daily Digest
## Setup Guide — 100% FREE Stack

**File to import:** `WF-C-YOUTUBE-AI-DIGEST.json`

> **$0/month. No credit card. No paid APIs.**

---

## What It Does

Every day at **8 AM ET**, this workflow:
1. Picks a rotating AI topic theme (LLMs, tools, agents, etc.)
2. Searches YouTube for the **top 10 fresh AI tech videos** (last 48h)
3. Gets full stats: views, likes, duration, channel, description
4. Sends all data to **Claude AI** for expert summarization
5. Delivers a **beautiful HTML email digest** + **Telegram notification**

---

## Daily Theme Rotation

| Day | Theme | Focus |
|-----|-------|-------|
| Sunday | Weekly AI Roundup | Best of the week recap |
| Monday | LLMs & Models | GPT, Claude, Gemini releases |
| Tuesday | AI Tools & Productivity | Tools, automation, workflows |
| Wednesday | AI Generation | Image/video gen: Sora, Midjourney |
| Thursday | AI Agents & Code | Agents, Cursor, Copilot, coding |
| Friday | AI Business | Startups, launches, strategy |
| Saturday | ML Tutorials | Deep learning, technical deep dives |

---

## Setup — 5 Steps

### Step 1 — Get YouTube Data API Key (FREE)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create project → **APIs & Services → Library**
3. Search **"YouTube Data API v3"** → Enable
4. **APIs & Services → Credentials → Create Credentials → API Key**
5. Copy the key

**Free quota:** 10,000 units/day. This workflow uses ~120 units/run. That's 80+ runs/day for free.

### Step 2 — Get Groq API Key (FREE — No Credit Card)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google or email — completely free
3. Click **API Keys → Create API Key**
4. Copy the key (format: `gsk_...`)

**Free tier:** 14,400 requests/day with Llama 3.3 70B. This workflow uses 1 request/day.

In the workflow node **"HTTP: Groq AI — Generate Digest"**, replace:
```
FILL_YOUR_GROQ_API_KEY
```
with your Groq key (`gsk_...`)

### Step 3 — Set Up Telegram Bot (Primary Notification)

1. Message **@BotFather** on Telegram → `/newbot`
2. Follow prompts → get your **Bot Token** (format: `123456:ABCdef...`)
3. Start a chat with your new bot
4. Get your Chat ID: visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in browser
5. Look for `"chat":{"id":XXXXXXXXX}` — that number is your Chat ID

In the workflow node **"HTTP: Send Telegram Digest"**, replace:
- `FILL_YOUR_TELEGRAM_BOT_TOKEN` → your bot token
- `FILL_YOUR_TELEGRAM_CHAT_ID` → your chat ID (can be negative for groups)

### Step 4 — Set Up Email (Optional but Recommended)

**Gmail SMTP with App Password:**

1. Go to [myaccount.google.com](https://myaccount.google.com) → Security
2. Enable **2-Step Verification** (required)
3. Go to **App Passwords** → Select "Mail" + "Windows Computer" → Generate
4. Copy the 16-character password

**In n8n:**
1. Settings → Credentials → New → **SMTP**
2. Host: `smtp.gmail.com`
3. Port: `465`
4. SSL: **ON**
5. User: `your@gmail.com`
6. Password: the 16-char App Password (NOT your real password)
7. Name it: `Gmail SMTP (App Password)`

In the workflow node **"HTTP: Send Email via Gmail SMTP"**, replace:
- `FILL_YOUR_GMAIL@gmail.com` (both From and To fields)
- Update the credential ID in the node

### Step 5 — Replace API Keys in Workflow

Open `WF-C-YOUTUBE-AI-DIGEST.json` and replace ALL `FILL_YOUR_*` placeholders:

| Placeholder | Replace With | Where to Get |
|-------------|-------------|-------------|
| `FILL_YOUR_YOUTUBE_API_KEY` | YouTube Data API v3 key (×2) | console.cloud.google.com — FREE |
| `FILL_YOUR_GROQ_API_KEY` | Groq API key (`gsk_...`) | console.groq.com — FREE |
| `FILL_YOUR_TELEGRAM_BOT_TOKEN` | Telegram bot token | @BotFather on Telegram — FREE |
| `FILL_YOUR_TELEGRAM_CHAT_ID` | Your Telegram chat ID | api.telegram.org/bot.../getUpdates — FREE |
| `FILL_YOUR_GMAIL@gmail.com` | Your Gmail address (×2) | Your existing Gmail — FREE |

---

## Import & Activate

1. n8n → **Workflows → Import from File**
2. Select `WF-C-YOUTUBE-AI-DIGEST.json`
3. Set up SMTP credential if using email
4. Toggle **Inactive → Active**
5. First run: **8:00 AM ET** tomorrow

**Manual test:** Click "Test Workflow" to run immediately and verify all steps work.

---

## What the Email Looks Like

```
┌─────────────────────────────────────────┐
│  🤖  AI Tech Daily Digest               │
│      Saturday, May 31, 2026             │
│      "AI is moving fast today."         │
├─────────────────────────────────────────┤
│  📋 TODAY'S BRIEFING — ML Tutorials     │
│  [3-4 sentence executive summary of     │
│   today's biggest AI developments]     │
│                                         │
│  ⭐ TODAY'S TOP PICK                    │
│  [Purple gradient card with must-watch] │
│                                         │
│  📌 Today's Themes: [pill badges]       │
│  🛠 Tools Mentioned: [pill badges]      │
│                                         │
│  📺 All Videos Today (10)               │
│  ┌─────────────────────────────────┐   │
│  │ [thumb] Title of video           │   │
│  │         Channel | 12m | 45K views│   │
│  │         [3-4 line summary]       │   │
│  │         [tag] [tag] [tag]        │   │
│  │         ★★★★★★★★☆☆ Relevance   │   │
│  │  💡 Key Takeaways:               │   │
│  │     • Takeaway 1                 │   │
│  │     • Takeaway 2                 │   │
│  │  [▶ Watch on YouTube]            │   │
│  └─────────────────────────────────┘   │
│  ... (10 videos total) ...             │
└─────────────────────────────────────────┘
```

---

## Telegram Message Format

```
🤖 AI Tech Digest | 10 videos | Saturday, May 31

🔥 Today's theme: ML Tutorials
📺 Top pick: "How to Build AI Agents in 2025"

⚡ Key highlights:
• OpenAI releases new model...
• Anthropic's Claude update...

Check your email for the full digest!
```

---

## Cost Estimate — $0.00/month

| Service | Usage | Cost |
|---------|-------|------|
| YouTube Data API v3 | ~120 units/day (quota: 10,000) | **FREE** |
| Groq AI (Llama 3.3 70B) | 1 request/day (quota: 14,400) | **FREE** |
| Telegram Bot API | 1 message/day | **FREE** |
| Gmail SMTP | 1 email/day | **FREE** |
| n8n (self-hosted) | — | **FREE** |
| **Total** | | **$0.00/month** |

---

## Workflow Architecture

```
Schedule (8AM ET)
    ↓
Code: Build Search Query           ← Rotating AI topic by day of week
    ↓
HTTP: YouTube Search API           ← Search top 15 videos, last 48h  [FREE]
    ↓
Code: Extract & Filter             ← Deduplicate, take top 10
    ↓
HTTP: YouTube Video Details        ← Full stats + description         [FREE]
    ↓
Code: Build Rich Video Profiles    ← Format duration, views, tags
    ↓
HTTP: Groq AI — Generate Digest    ← Llama 3.3 70B summarization      [FREE]
    ↓
Code: Parse Groq Digest            ← JSON parsing + fallback
    ↓
Code: Format HTML Email            ← Beautiful responsive HTML
    ↓ (parallel)
HTTP: Telegram [FREE]       HTTP: Gmail SMTP [FREE]
    ↓                               ↓
             Code: Final Log
```

---

## Cross-Check — Existing Workflows Status

| # | Name | File | Status |
|---|------|------|--------|
| WF-A | Social Blast | `WF-A-SOCIAL-BLAST.json` | ✅ Ready (fill FB/IG IDs) |
| WF-B | Blog v1 (old) | `WF-B-DAILY-BLOG.json` | ⚠️ Superseded by V2 |
| Blog Final | Blog V1 Final | `WF-BLOG-DAILY-FINAL.json` | ✅ Working, 30 topics |
| Blog V2 | Blog V2 Final | `WF-BLOG-V2-FINAL.json` | ✅ **Best — use this** (54 topics, season-aware) |
| **WF-C** | **YouTube AI Digest** | **`WF-C-YOUTUBE-AI-DIGEST.json`** | ✅ **NEW — this file** |
