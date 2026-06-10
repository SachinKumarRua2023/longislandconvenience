"""
rss_monitor.py — Polls YouTube RSS feeds to discover new uploads.

YouTube exposes a public Atom feed per channel:
  https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxxxx

No API key required. Checked every CHECK_INTERVAL_MINUTES minutes.
"""

import logging
from datetime import datetime
from typing import Optional

import feedparser

import config
from database import video_exists, insert_video, upsert_channel_last_checked

logger = logging.getLogger(__name__)

_RSS_TEMPLATE = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def _parse_channel_str(raw: str) -> tuple[str, str]:
    """
    Accept two formats:
      'UCxxxxxx'              → id=UCxxxxxx, name=UCxxxxxx
      'UCxxxxxx:My Channel'   → id=UCxxxxxx, name=My Channel
    """
    parts = raw.strip().split(":", 1)
    channel_id = parts[0].strip()
    channel_name = parts[1].strip() if len(parts) > 1 else channel_id
    return channel_id, channel_name


def _parse_published(entry: feedparser.FeedParserDict) -> str:
    """Convert feedparser's time_struct to ISO 8601 string."""
    if entry.get("published_parsed"):
        try:
            return datetime(*entry.published_parsed[:6]).isoformat()
        except Exception:
            pass
    return entry.get("published", datetime.utcnow().isoformat())


def fetch_channel_videos(channel_id: str, channel_name: str) -> list[dict]:
    """Return all video metadata from the channel's RSS feed."""
    rss_url = _RSS_TEMPLATE.format(channel_id=channel_id)
    logger.debug("Fetching RSS: %s", rss_url)

    feed = feedparser.parse(rss_url)

    # bozo=True means the feed had a parse error
    if feed.bozo and not feed.entries:
        logger.warning(
            "RSS parse error for %s (%s): %s",
            channel_name, channel_id, feed.get("bozo_exception", "unknown"),
        )
        return []

    videos: list[dict] = []
    for entry in feed.entries:
        video_id: Optional[str] = entry.get("yt_videoid")
        if not video_id:
            link: str = entry.get("link", "")
            if "v=" in link:
                video_id = link.split("v=")[-1].split("&")[0]
        if not video_id:
            continue

        videos.append({
            "video_id":     video_id,
            "channel_id":   channel_id,
            "channel_name": channel_name,
            "title":        entry.get("title", "Unknown Title"),
            "url":          f"https://www.youtube.com/watch?v={video_id}",
            "published_at": _parse_published(entry),
        })

    logger.info("  [%s] %d video(s) in feed", channel_name, len(videos))
    return videos


def check_all_channels() -> list[dict]:
    """
    Iterate every configured channel, insert unseen videos, and return
    the list of brand-new videos discovered this cycle.
    """
    if not config.YOUTUBE_CHANNELS:
        logger.warning(
            "No channels configured — set YOUTUBE_CHANNELS in .env"
        )
        return []

    new_videos: list[dict] = []

    for raw in config.YOUTUBE_CHANNELS:
        channel_id, channel_name = _parse_channel_str(raw)
        logger.info("Checking channel: %s (%s)", channel_name, channel_id)

        try:
            videos = fetch_channel_videos(channel_id, channel_name)
        except Exception as exc:
            logger.error("Failed to fetch %s: %s", channel_name, exc, exc_info=True)
            continue

        for video in videos:
            if not video_exists(video["video_id"]):
                insert_video(video)
                new_videos.append(video)
                logger.info(
                    "  NEW: %s [%s]", video["title"], video["video_id"]
                )

        upsert_channel_last_checked(channel_id, channel_name)

    logger.info(
        "Channel scan complete — %d new video(s) queued.", len(new_videos)
    )
    return new_videos
