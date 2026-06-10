"""
utils.py — Logging setup, notifications (Telegram/Discord/Email), Notion export,
           and misc helpers used by main.py.
"""

import logging
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import requests

import config

# ── Logging ───────────────────────────────────────────────────────────────────

def setup_logging() -> logging.Logger:
    """Configure root logger with rotating daily file + console output."""
    os.makedirs(config.LOGS_DIR, exist_ok=True)
    log_file = os.path.join(
        config.LOGS_DIR,
        f"yt_automation_{datetime.now().strftime('%Y%m%d')}.log",
    )

    fmt = "%(asctime)s | %(levelname)-8s | %(name)-22s | %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    # Silence noisy third-party libraries
    for lib in ("urllib3", "httpcore", "httpx", "openai", "feedparser"):
        logging.getLogger(lib).setLevel(logging.WARNING)

    return logging.getLogger("main")


def ensure_directories() -> None:
    """Create all required project directories."""
    for d in (
        config.DATA_DIR,
        config.LOGS_DIR,
        config.TRANSCRIPTS_DIR,
        config.SUMMARIES_DIR,
        config.YTDLP_AUDIO_DIR,
    ):
        os.makedirs(d, exist_ok=True)


# ── Telegram ──────────────────────────────────────────────────────────────────

def send_telegram(message: str) -> None:
    if not (config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID):
        return
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        resp = requests.post(
            url,
            json={
                "chat_id": config.TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
        resp.raise_for_status()
        logging.getLogger(__name__).info("Telegram notification sent.")
    except Exception as exc:
        logging.getLogger(__name__).warning("Telegram failed: %s", exc)


# ── Discord ───────────────────────────────────────────────────────────────────

def send_discord(message: str, embed: Optional[dict] = None) -> None:
    if not config.DISCORD_WEBHOOK_URL:
        return
    payload: dict = {"content": message}
    if embed:
        payload["embeds"] = [embed]
    try:
        resp = requests.post(
            config.DISCORD_WEBHOOK_URL, json=payload, timeout=10
        )
        resp.raise_for_status()
        logging.getLogger(__name__).info("Discord notification sent.")
    except Exception as exc:
        logging.getLogger(__name__).warning("Discord failed: %s", exc)


# ── Email ─────────────────────────────────────────────────────────────────────

def send_email(subject: str, html_body: str) -> None:
    if not all([config.EMAIL_USER, config.EMAIL_PASSWORD, config.EMAIL_TO]):
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["From"]    = config.EMAIL_USER
        msg["To"]      = config.EMAIL_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP(config.EMAIL_SMTP_HOST, config.EMAIL_SMTP_PORT) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            srv.send_message(msg)

        logging.getLogger(__name__).info("Email sent to %s", config.EMAIL_TO)
    except Exception as exc:
        logging.getLogger(__name__).warning("Email failed: %s", exc)


# ── Notion ────────────────────────────────────────────────────────────────────

def export_to_notion(video: dict, ai: dict) -> None:
    if not (config.NOTION_API_KEY and config.NOTION_DATABASE_ID):
        return

    headers = {
        "Authorization": f"Bearer {config.NOTION_API_KEY}",
        "Content-Type":  "application/json",
        "Notion-Version": "2022-06-28",
    }

    def _text(s: str) -> list:
        return [{"text": {"content": s[:2000]}}]

    payload = {
        "parent": {"database_id": config.NOTION_DATABASE_ID},
        "properties": {
            "Title":          {"title":     _text(video.get("title", ""))},
            "Channel":        {"rich_text": _text(video.get("channel_name", ""))},
            "URL":            {"url":       video.get("url", "")},
            "Summary":        {"rich_text": _text(ai.get("summary", ""))},
            "Hashtags":       {"rich_text": _text(ai.get("hashtags", ""))},
            "Processed Date": {"date":      {"start": datetime.utcnow().isoformat()}},
        },
        "children": [
            _notion_heading("Key Points"),
            _notion_paragraph(ai.get("key_points", "")),
            _notion_heading("LinkedIn Post"),
            _notion_paragraph(ai.get("linkedin_post", "")),
            _notion_heading("Twitter / X Post"),
            _notion_paragraph(ai.get("twitter_post", "")),
            _notion_heading("Blog Outline"),
            _notion_paragraph(ai.get("blog_outline", "")),
        ],
    }

    try:
        resp = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        logging.getLogger(__name__).info(
            "Exported to Notion: %s", video.get("title")
        )
    except Exception as exc:
        logging.getLogger(__name__).warning("Notion export failed: %s", exc)


def _notion_heading(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": text}}]},
    }


def _notion_paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"text": {"content": (text or "")[:2000]}}]},
    }


# ── Unified notifier ──────────────────────────────────────────────────────────

def notify_processed(video: dict, ai: dict) -> None:
    """Fire all configured notification channels for a fully processed video."""
    title   = video.get("title", "Unknown")
    channel = video.get("channel_name", "Unknown")
    url     = video.get("url", "")
    summary = ai.get("summary", "No summary available.")

    # Telegram
    send_telegram(
        f"<b>✅ New Video Processed</b>\n\n"
        f"<b>Channel:</b> {channel}\n"
        f"<b>Title:</b> {title}\n"
        f"<b>URL:</b> {url}\n\n"
        f"<b>Summary:</b>\n{summary[:600]}"
    )

    # Discord
    send_discord(
        f"New video processed: **{title}**",
        embed={
            "title":       title,
            "url":         url,
            "description": summary[:4096],
            "color":       0xFF0000,
            "fields": [{"name": "Channel", "value": channel, "inline": True}],
            "footer": {"text": "YouTube Automation Bot"},
        },
    )

    # Email
    send_email(
        subject=f"YouTube Summary: {title}",
        html_body=f"""
        <h2>{title}</h2>
        <p><b>Channel:</b> {channel} &nbsp;|&nbsp;
           <b>URL:</b> <a href="{url}">{url}</a></p>
        <h3>Summary</h3><p>{summary}</p>
        <h3>Key Points</h3><p>{ai.get('key_points','').replace(chr(10),'<br>')}</p>
        <h3>Hashtags</h3><p>{ai.get('hashtags','')}</p>
        <h3>Twitter / X</h3><p>{ai.get('twitter_post','')}</p>
        <hr><p><small>Generated by YouTube Automation System</small></p>
        """,
    )

    # Notion
    export_to_notion(video, ai)
