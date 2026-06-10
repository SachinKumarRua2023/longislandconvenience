"""
transcript.py — Three-tier transcript extraction pipeline.

Priority order:
  1. youtube-transcript-api  (instant, no download needed)
  2. Auto-generated captions via youtube-transcript-api
  3. yt-dlp audio download → OpenAI Whisper STT  (fallback, slower)
"""

import os
import logging
from typing import Optional

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

import config

logger = logging.getLogger(__name__)


# ── Tier 1 & 2: youtube-transcript-api ───────────────────────────────────────

def _fetch_via_api(video_id: str) -> Optional[str]:
    """Grab the best available transcript through the transcript API."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except (TranscriptsDisabled, VideoUnavailable, NoTranscriptFound) as exc:
        logger.debug("Transcript API unavailable for %s: %s", video_id, exc)
        return None
    except Exception as exc:
        logger.warning("Transcript API error for %s: %s", video_id, exc)
        return None

    # Prefer manual transcripts, then fall back to auto-generated
    for prefer_generated in (False, True):
        for t in transcript_list:
            if t.is_generated == prefer_generated:
                try:
                    data = t.fetch()
                    text = " ".join(seg["text"] for seg in data).strip()
                    kind = "auto-generated" if prefer_generated else "manual"
                    logger.info("Transcript via API (%s): %s", kind, video_id)
                    return text
                except Exception as exc:
                    logger.debug("Failed fetching transcript segment: %s", exc)
                    continue
    return None


# ── Tier 3a: yt-dlp audio download ────────────────────────────────────────────

def _download_audio(video_url: str, video_id: str) -> Optional[str]:
    """Download best-quality audio to YTDLP_AUDIO_DIR; return file path."""
    try:
        import yt_dlp
    except ImportError:
        logger.error("yt-dlp not installed — run: pip install yt-dlp")
        return None

    os.makedirs(config.YTDLP_AUDIO_DIR, exist_ok=True)
    out_template = os.path.join(config.YTDLP_AUDIO_DIR, f"{video_id}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }
        ],
        "quiet": True,
        "no_warnings": True,
        "retries": 3,
        "socket_timeout": config.REQUEST_TIMEOUT_SECONDS,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as exc:
        logger.error("yt-dlp download failed for %s: %s", video_id, exc)
        return None

    # Locate the downloaded file
    for ext in ("mp3", "m4a", "webm", "opus", "wav"):
        path = os.path.join(config.YTDLP_AUDIO_DIR, f"{video_id}.{ext}")
        if os.path.exists(path):
            logger.info("Audio downloaded: %s", path)
            return path

    logger.warning("Audio file not found after yt-dlp download for %s", video_id)
    return None


# ── Tier 3b: Whisper STT ──────────────────────────────────────────────────────

def _whisper_transcribe(audio_path: str) -> Optional[str]:
    """Run OpenAI Whisper on the audio file and return the transcript."""
    try:
        import whisper
    except ImportError:
        logger.error("Whisper not installed — run: pip install openai-whisper")
        return None

    try:
        logger.info("Loading Whisper model '%s'…", config.WHISPER_MODEL)
        model = whisper.load_model(config.WHISPER_MODEL)
        logger.info("Transcribing %s…", audio_path)
        result = model.transcribe(audio_path)
        text = result.get("text", "").strip()
        if text:
            logger.info("Whisper transcription complete (%d chars)", len(text))
            return text
        logger.warning("Whisper returned empty text for %s", audio_path)
        return None
    except Exception as exc:
        logger.error("Whisper failed on %s: %s", audio_path, exc, exc_info=True)
        return None


# ── Public interface ──────────────────────────────────────────────────────────

def get_transcript(video_id: str, video_url: str) -> tuple[Optional[str], str]:
    """
    Full fallback chain.  Returns (transcript_text, method_used).
    method_used is one of: 'api' | 'auto_generated' | 'whisper' | 'none'
    """
    # Tier 1 + 2: transcript API
    text = _fetch_via_api(video_id)
    if text:
        # Distinguish manual vs auto-generated already logged inside helper
        # We mark both as 'api' for simplicity; re-check if detail matters
        method = "api"
        return text, method

    # Tier 3: download audio + Whisper
    logger.info("Falling back to yt-dlp + Whisper for %s", video_id)
    audio_path = _download_audio(video_url, video_id)
    if audio_path:
        text = _whisper_transcribe(audio_path)
        # Clean up audio to save disk space
        try:
            os.remove(audio_path)
        except OSError:
            pass
        if text:
            return text, "whisper"

    logger.warning("All transcript methods exhausted for %s", video_id)
    return None, "none"


def save_transcript_file(
    video_id: str, title: str, channel_name: str, transcript: str
) -> str:
    """Write transcript to /transcripts/<video_id>_<title>.txt."""
    os.makedirs(config.TRANSCRIPTS_DIR, exist_ok=True)
    safe = "".join(c if (c.isalnum() or c in " -_") else "_" for c in title)[:80]
    path = os.path.join(config.TRANSCRIPTS_DIR, f"{video_id}_{safe}.txt")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"Video ID : {video_id}\n")
        fh.write(f"Channel  : {channel_name}\n")
        fh.write(f"Title    : {title}\n")
        fh.write(f"URL      : https://www.youtube.com/watch?v={video_id}\n")
        fh.write("=" * 60 + "\n\n")
        fh.write(transcript)

    logger.info("Transcript saved → %s", path)
    return path
