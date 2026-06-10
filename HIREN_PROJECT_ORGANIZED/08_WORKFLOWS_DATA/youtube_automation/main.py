#!/usr/bin/env python3
"""
main.py — YouTube Automation System entry point.

Pipeline per video:
  RSS feed → detect new uploads → fetch transcript → AI processing
  → save to DB + files → send notifications
"""

import logging
import signal
import sys
import threading
import time

import schedule

import config
from ai_summary import generate_ai_content, save_summary_file
from database import (
    get_failed_videos,
    get_pending_videos,
    get_video_stats,
    init_db,
    mark_video_failed,
    update_video_ai_content,
    update_video_status,
    update_video_transcript,
)
from rss_monitor import check_all_channels
from transcript import get_transcript, save_transcript_file
from utils import ensure_directories, notify_processed, setup_logging

# Initialise logging before any other module emits messages
logger = setup_logging()

# Signals graceful shutdown to the scheduler loop
_shutdown = threading.Event()


# ── Per-video pipeline ────────────────────────────────────────────────────────

def process_video(video: dict) -> None:
    video_id    = video["video_id"]
    title       = video.get("title", "Unknown")
    channel     = video.get("channel_name", "Unknown")
    url         = video.get("url", f"https://www.youtube.com/watch?v={video_id}")
    transcript  = video.get("transcript")   # may already exist (status=transcribed)

    logger.info("Processing: %s [%s]", title, video_id)
    update_video_status(video_id, "processing")

    try:
        # ── Step 1: Transcript ────────────────────────────────────────────────
        if not transcript:
            transcript, method = get_transcript(video_id, url)

            if transcript:
                update_video_transcript(video_id, transcript, method)
                save_transcript_file(video_id, title, channel, transcript)
            else:
                mark_video_failed(video_id, "No transcript available from any source.")
                logger.warning("No transcript found — skipping: %s", title)
                return

        # ── Step 2: AI generation ─────────────────────────────────────────────
        ai_data = generate_ai_content(title, channel, transcript)

        # ── Step 3: Persist ───────────────────────────────────────────────────
        update_video_ai_content(video_id, ai_data)
        save_summary_file(video_id, title, channel, ai_data)

        # ── Step 4: Notify ────────────────────────────────────────────────────
        notify_processed(video, ai_data)

        logger.info("Done: %s", title)

    except Exception as exc:
        mark_video_failed(video_id, str(exc))
        logger.error("Failed: %s — %s", title, exc, exc_info=True)


# ── One monitoring cycle ──────────────────────────────────────────────────────

def run_cycle() -> None:
    logger.info("━━━ Monitoring cycle started ━━━")

    # 1. Discover new uploads
    try:
        check_all_channels()
    except Exception as exc:
        logger.error("RSS check error: %s", exc, exc_info=True)

    # 2. Process pending (new + previously pending/transcribed)
    pending = get_pending_videos(limit=20)
    if pending:
        logger.info("Processing %d pending video(s)…", len(pending))
    for video in pending:
        if _shutdown.is_set():
            break
        process_video(video)
        time.sleep(2)   # brief pause between videos to respect rate limits

    # 3. Retry failed videos (up to MAX_RETRIES attempts)
    failed = get_failed_videos(max_retries=config.MAX_RETRIES)
    if failed:
        logger.info("Retrying %d failed video(s)…", len(failed))
    for video in failed:
        if _shutdown.is_set():
            break
        process_video(video)
        time.sleep(config.RETRY_DELAY_SECONDS)

    # 4. Log stats
    stats = get_video_stats()
    logger.info("Stats: %s", stats)
    logger.info("━━━ Monitoring cycle complete ━━━")


# ── Graceful shutdown ─────────────────────────────────────────────────────────

def _handle_signal(sig, frame):   # noqa: ANN001
    logger.info("Shutdown signal received — finishing current task…")
    _shutdown.set()


# ── Entry point ───────────────────────────────────────────────────────────────

_BANNER = """
╔══════════════════════════════════════════════════════════╗
║        YouTube Automation System  v1.0                   ║
║   Transcript Extraction · AI Summaries · Notifications   ║
╚══════════════════════════════════════════════════════════╝"""


def main() -> None:
    print(_BANNER)

    signal.signal(signal.SIGINT,  _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    ensure_directories()
    init_db()

    channel_count = len(config.YOUTUBE_CHANNELS)
    logger.info("Watching %d channel(s) | interval: %d min | model: %s",
                channel_count, config.CHECK_INTERVAL_MINUTES, config.OPENAI_MODEL)

    if channel_count == 0:
        logger.warning(
            "No channels configured! "
            "Add YOUTUBE_CHANNELS=UCxxx:Name to .env and restart."
        )

    # Run once immediately so we don't wait for the first tick
    run_cycle()

    schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(run_cycle)
    logger.info("Scheduler running — next check in %d min.", config.CHECK_INTERVAL_MINUTES)

    while not _shutdown.is_set():
        schedule.run_pending()
        time.sleep(1)

    logger.info("YouTube Automation System stopped.")
    sys.exit(0)


if __name__ == "__main__":
    main()
