"""
config.py — Centralized configuration loaded from environment variables.
All runtime settings live here; nothing else reads .env directly.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Resolve the project root so paths work regardless of CWD
BASE_DIR = Path(__file__).parent.resolve()
load_dotenv(BASE_DIR / ".env")

# ── OpenAI ────────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ── YouTube Channels ──────────────────────────────────────────────────────────
# .env format:  YOUTUBE_CHANNELS=UCxxx:Channel Name,UCyyy:Another Channel
_channels_raw: str = os.getenv("YOUTUBE_CHANNELS", "")
YOUTUBE_CHANNELS: list[str] = [c.strip() for c in _channels_raw.split(",") if c.strip()]

# ── Scheduling ────────────────────────────────────────────────────────────────
CHECK_INTERVAL_MINUTES: int = int(os.getenv("CHECK_INTERVAL_MINUTES", "15"))

# ── Paths (all relative to BASE_DIR) ─────────────────────────────────────────
DATA_DIR: str        = str(BASE_DIR / "data")
LOGS_DIR: str        = str(BASE_DIR / "logs")
TRANSCRIPTS_DIR: str = str(BASE_DIR / "transcripts")
SUMMARIES_DIR: str   = str(BASE_DIR / "summaries")
YTDLP_AUDIO_DIR: str = str(BASE_DIR / "data" / "audio")
DB_PATH: str         = str(BASE_DIR / "data" / "youtube_automation.db")

# ── Whisper ───────────────────────────────────────────────────────────────────
# tiny | base | small | medium | large   (larger = more accurate, slower)
WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")

# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID: str   = os.getenv("TELEGRAM_CHAT_ID", "")

# ── Discord ───────────────────────────────────────────────────────────────────
DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")

# ── Email ─────────────────────────────────────────────────────────────────────
EMAIL_SMTP_HOST: str = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_USER: str      = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD: str  = os.getenv("EMAIL_PASSWORD", "")
EMAIL_TO: str        = os.getenv("EMAIL_TO", "")

# ── Notion ────────────────────────────────────────────────────────────────────
NOTION_API_KEY: str      = os.getenv("NOTION_API_KEY", "")
NOTION_DATABASE_ID: str  = os.getenv("NOTION_DATABASE_ID", "")

# ── Retry / Rate-limit ────────────────────────────────────────────────────────
MAX_RETRIES: int           = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY_SECONDS: int   = int(os.getenv("RETRY_DELAY_SECONDS", "60"))
REQUEST_TIMEOUT_SECONDS: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
