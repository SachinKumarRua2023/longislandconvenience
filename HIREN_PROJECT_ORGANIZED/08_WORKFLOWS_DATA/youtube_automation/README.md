# YouTube Automation System

Fully automated YouTube transcript extraction, AI summarisation, and multi-channel notification system.

---

## What It Does

1. **Monitors** multiple YouTube channels via public RSS feeds — no API key needed.
2. **Fetches transcripts** (caption API → auto-generated → Whisper STT fallback).
3. **Generates AI content** via OpenAI: summary, key points, hashtags, LinkedIn post, Twitter/X post, blog outline.
4. **Stores everything** in SQLite + saves `.txt` files for transcripts and summaries.
5. **Notifies you** via Telegram, Discord, Email, and/or Notion.
6. **Runs 24/7** with a built-in scheduler and automatic retry on failures.

---

## Folder Structure

```
youtube_automation/
├── main.py            # Scheduler + orchestration entry point
├── config.py          # All settings loaded from .env
├── database.py        # SQLite persistence layer
├── rss_monitor.py     # YouTube RSS feed polling
├── transcript.py      # 3-tier transcript extraction
├── ai_summary.py      # OpenAI content generation
├── utils.py           # Logging, notifications, Notion export
├── requirements.txt
├── .env.example       # Copy to .env and fill in values
├── logs/              # Auto-created; daily log files
├── data/              # Auto-created; SQLite DB + temp audio
├── transcripts/       # Auto-created; one .txt per video
└── summaries/         # Auto-created; one summary .txt per video
```

---

## Quick Start (Local)

### 1. Prerequisites

- Python 3.10 or newer
- FFmpeg (only needed for Whisper fallback)

```bash
# Windows
winget install Gyan.FFmpeg

# Ubuntu / Debian
sudo apt install ffmpeg python3-pip python3-venv

# macOS
brew install ffmpeg
```

### 2. Clone / download the project

```bash
cd youtube_automation
```

### 3. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If you want Whisper fallback (speech-to-text for videos without captions):

```bash
pip install openai-whisper
```

### 5. Configure environment variables

```bash
cp .env.example .env
# Open .env in any editor and fill in your values
```

Minimum required settings:

```env
OPENAI_API_KEY=sk-...
YOUTUBE_CHANNELS=UCxxxxxx:My Channel
```

### 6. Run

```bash
python main.py
```

The system will immediately scan all channels, process any new videos it finds, then check again every `CHECK_INTERVAL_MINUTES` minutes.

---

## How to Find a YouTube Channel ID

1. Open the YouTube channel in your browser.
2. Right-click anywhere on the page → **View Page Source**.
3. Press `Ctrl+F` and search for `"channelId"`.
4. Copy the value — it starts with `UC` and is 24 characters long.

Alternatively, visit `https://www.youtube.com/@ChannelHandle/about` and look at the URL in the share button.

---

## Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI secret key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model used for content generation |
| `YOUTUBE_CHANNELS` | *(required)* | `UCxxx:Name,UCyyy:Name` |
| `CHECK_INTERVAL_MINUTES` | `15` | How often to poll RSS feeds |
| `WHISPER_MODEL` | `base` | `tiny/base/small/medium/large` |
| `TELEGRAM_BOT_TOKEN` | *(optional)* | Telegram bot token |
| `TELEGRAM_CHAT_ID` | *(optional)* | Your Telegram chat/group ID |
| `DISCORD_WEBHOOK_URL` | *(optional)* | Discord channel webhook URL |
| `EMAIL_USER` | *(optional)* | Gmail sender address |
| `EMAIL_PASSWORD` | *(optional)* | Gmail App Password |
| `EMAIL_TO` | *(optional)* | Recipient email address |
| `NOTION_API_KEY` | *(optional)* | Notion integration token |
| `NOTION_DATABASE_ID` | *(optional)* | Target Notion database ID |
| `MAX_RETRIES` | `3` | Max retry attempts for failed videos |

---

## Deploy on a VPS / Server (Ubuntu)

### 1. Provision a server

Any VPS with 1 GB RAM works. Free options:
- **Oracle Cloud Always Free** — 2 AMD VMs with 1 GB RAM each, free forever.
- **Google Cloud Free Tier** — 1 e2-micro in us-central1.
- **Fly.io** — Free tier with 256 MB RAM (enough for `base` Whisper model).

### 2. SSH into your server and set up the project

```bash
sudo apt update && sudo apt install -y python3-pip python3-venv ffmpeg git
git clone <your-repo-url> youtube_automation
cd youtube_automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # fill in your values
```

### 3. Run 24/7 with systemd (recommended)

Create a service file:

```bash
sudo nano /etc/systemd/system/yt-automation.service
```

Paste:

```ini
[Unit]
Description=YouTube Automation System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/youtube_automation
ExecStart=/home/ubuntu/youtube_automation/venv/bin/python main.py
Restart=on-failure
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable yt-automation
sudo systemctl start yt-automation

# Check status
sudo systemctl status yt-automation

# Watch live logs
sudo journalctl -u yt-automation -f
```

### 4. Alternative: run inside screen (simpler)

```bash
screen -S yt-bot
source venv/bin/activate
python main.py
# Detach with Ctrl+A then D
# Re-attach later with:
screen -r yt-bot
```

---

## Run 24/7 on Windows

Use Task Scheduler to run at startup:

1. Open **Task Scheduler** → Create Basic Task.
2. Trigger: **At startup**.
3. Action: **Start a program**.
4. Program: `C:\path\to\youtube_automation\venv\Scripts\python.exe`
5. Arguments: `C:\path\to\youtube_automation\main.py`
6. Start in: `C:\path\to\youtube_automation`

---

## Free Hosting Options

| Platform | Free Tier | Notes |
|---|---|---|
| **Oracle Cloud Always Free** | 2 × 1 GB VMs | Best option — truly unlimited |
| **Google Cloud Free** | 1 e2-micro | 30 GB disk, US regions only |
| **Fly.io** | 3 shared VMs | Good for lightweight workloads |
| **Railway** | 500 hrs/month | Easy deploy, sleeps when idle |
| **PythonAnywhere** | 1 CPU + always-on tasks | Free plan allows scheduled tasks |

---

## Notion Setup

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) → **New Integration** → copy the token.
2. In Notion, create a database with these properties:
   - `Title` (Title type)
   - `Channel` (Text)
   - `URL` (URL)
   - `Summary` (Text)
   - `Hashtags` (Text)
   - `Processed Date` (Date)
3. Open the database page → click **...** (top right) → **Add connections** → select your integration.
4. Copy the database ID from the URL (`notion.so/workspace/<DATABASE_ID>?v=...`).
5. Add both values to `.env`.

---

## Telegram Bot Setup

1. Message [@BotFather](https://t.me/BotFather) on Telegram.
2. Send `/newbot` and follow the prompts — copy the token.
3. Start a conversation with your new bot, then open:
   `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Copy the `chat.id` value from the response.
5. Add both to `.env`.

---

## Troubleshooting

**No transcripts found**
- Some channels disable captions. Whisper fallback requires FFmpeg and `openai-whisper` installed.
- Check `logs/yt_automation_YYYYMMDD.log` for detail.

**OpenAI rate limit errors**
- Increase `RETRY_DELAY_SECONDS` or switch to `gpt-3.5-turbo`.

**RSS feed returns no videos**
- Double-check the Channel ID (must start with `UC`, 24 chars).
- Test manually: `https://www.youtube.com/feeds/videos.xml?channel_id=UCXXXXXXX`

**Database locked**
- Only one instance of `main.py` should run at a time.
- WAL mode is enabled, which greatly reduces lock contention.

---

## Tech Stack

| Component | Library |
|---|---|
| RSS monitoring | `feedparser` |
| Transcript API | `youtube-transcript-api` |
| Audio download | `yt-dlp` |
| Speech-to-text | `openai-whisper` |
| AI summarisation | `openai` |
| Scheduling | `schedule` |
| Database | `sqlite3` (stdlib) |
| HTTP | `requests` |
| Config | `python-dotenv` |
