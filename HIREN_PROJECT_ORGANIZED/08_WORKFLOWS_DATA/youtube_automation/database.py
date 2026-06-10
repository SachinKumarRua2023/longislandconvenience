"""
database.py — SQLite persistence layer.
All DB calls go through this module; nothing else imports sqlite3 directly.
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional

import config

logger = logging.getLogger(__name__)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # better write concurrency
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Create tables and indexes if they don't exist."""
    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS channels (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id   TEXT    UNIQUE NOT NULL,
                channel_name TEXT,
                added_at     TEXT    DEFAULT (datetime('now')),
                last_checked TEXT,
                is_active    INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS videos (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id          TEXT UNIQUE NOT NULL,
                channel_id        TEXT NOT NULL,
                channel_name      TEXT,
                title             TEXT,
                url               TEXT,
                published_at      TEXT,
                -- transcript state
                transcript        TEXT,
                transcript_method TEXT,           -- api | auto_generated | whisper | none
                -- AI-generated content
                summary           TEXT,
                key_points        TEXT,
                hashtags          TEXT,
                linkedin_post     TEXT,
                twitter_post      TEXT,
                blog_outline      TEXT,
                -- workflow state
                status            TEXT DEFAULT 'pending',
                retry_count       INTEGER DEFAULT 0,
                error_message     TEXT,
                processed_at      TEXT,
                created_at        TEXT DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_videos_status     ON videos(status);
            CREATE INDEX IF NOT EXISTS idx_videos_channel_id ON videos(channel_id);
            CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos(created_at);
        """)
    logger.info("Database initialised: %s", config.DB_PATH)


# ── Read helpers ──────────────────────────────────────────────────────────────

def video_exists(video_id: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM videos WHERE video_id = ?", (video_id,)
        ).fetchone()
    return row is not None


def get_pending_videos(limit: int = 20) -> list[dict]:
    """Return videos that still need transcript or AI processing."""
    with _connect() as conn:
        rows = conn.execute(
            """SELECT * FROM videos
               WHERE status IN ('pending', 'transcribed')
               ORDER BY created_at ASC
               LIMIT ?""",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_failed_videos(max_retries: int = 3) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            """SELECT * FROM videos
               WHERE status = 'failed' AND retry_count < ?
               ORDER BY created_at ASC""",
            (max_retries,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_video_stats() -> dict[str, int]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT status, COUNT(*) AS cnt FROM videos GROUP BY status"
        ).fetchall()
    return {r["status"]: r["cnt"] for r in rows}


# ── Write helpers ─────────────────────────────────────────────────────────────

def insert_video(video: dict) -> None:
    """Insert a new video row; silently skip if already exists."""
    with _connect() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO videos
               (video_id, channel_id, channel_name, title, url, published_at, status)
               VALUES (?, ?, ?, ?, ?, ?, 'pending')""",
            (
                video["video_id"],
                video["channel_id"],
                video.get("channel_name", ""),
                video.get("title", ""),
                video.get("url", ""),
                video.get("published_at", datetime.utcnow().isoformat()),
            ),
        )


def update_video_status(video_id: str, status: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE videos SET status = ? WHERE video_id = ?",
            (status, video_id),
        )


def update_video_transcript(video_id: str, transcript: str, method: str) -> None:
    with _connect() as conn:
        conn.execute(
            """UPDATE videos
               SET transcript = ?, transcript_method = ?, status = 'transcribed'
               WHERE video_id = ?""",
            (transcript, method, video_id),
        )


def update_video_ai_content(video_id: str, ai: dict) -> None:
    with _connect() as conn:
        conn.execute(
            """UPDATE videos
               SET summary        = ?,
                   key_points     = ?,
                   hashtags       = ?,
                   linkedin_post  = ?,
                   twitter_post   = ?,
                   blog_outline   = ?,
                   status         = 'done',
                   processed_at   = ?
               WHERE video_id = ?""",
            (
                ai.get("summary", ""),
                ai.get("key_points", ""),
                ai.get("hashtags", ""),
                ai.get("linkedin_post", ""),
                ai.get("twitter_post", ""),
                ai.get("blog_outline", ""),
                datetime.utcnow().isoformat(),
                video_id,
            ),
        )


def mark_video_failed(video_id: str, error: str) -> None:
    with _connect() as conn:
        conn.execute(
            """UPDATE videos
               SET status = 'failed',
                   error_message = ?,
                   retry_count   = retry_count + 1
               WHERE video_id = ?""",
            (error[:1000], video_id),
        )


def upsert_channel_last_checked(channel_id: str, channel_name: str = "") -> None:
    now = datetime.utcnow().isoformat()
    with _connect() as conn:
        conn.execute(
            """INSERT INTO channels (channel_id, channel_name, last_checked)
               VALUES (?, ?, ?)
               ON CONFLICT(channel_id)
               DO UPDATE SET last_checked = excluded.last_checked""",
            (channel_id, channel_name, now),
        )
