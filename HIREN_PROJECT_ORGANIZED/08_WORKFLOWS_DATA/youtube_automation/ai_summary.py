"""
ai_summary.py — OpenAI-powered content generation from a video transcript.

One API call produces: summary, key points, hashtags, LinkedIn post,
Twitter/X post, and a blog outline — all returned as a typed dict.
"""

import json
import logging
import os
from typing import Optional

import config

logger = logging.getLogger(__name__)

# Maximum transcript characters sent to the model.
# gpt-4o-mini handles ~16k tokens; 12 000 chars ≈ 3 000 tokens, leaves room for output.
_MAX_TRANSCRIPT_CHARS = 12_000

_PROMPT_TEMPLATE = """You are a professional content strategist and copywriter.

A YouTube video titled "{title}" was published by "{channel}".

Transcript (may be truncated):
{transcript}

Produce the following in valid JSON (no markdown fences, no extra keys):

{{
  "summary":       "3-5 clear sentences summarising the main topic and takeaways",
  "key_points":    "Numbered list of 5-7 key insights, one per line",
  "hashtags":      "15-20 relevant hashtags as a single space-separated string (include #)",
  "linkedin_post": "Professional LinkedIn post 200-300 words with insights and a CTA",
  "twitter_post":  "Tweet under 280 chars with the sharpest insight + 3 hashtags",
  "blog_outline":  "Full blog post outline using ## H2 and ### H3 headings"
}}

Return ONLY the JSON object."""


def _empty() -> dict:
    return {
        "summary": "",
        "key_points": "",
        "hashtags": "",
        "linkedin_post": "",
        "twitter_post": "",
        "blog_outline": "",
    }


def _parse_json_safe(raw: str) -> Optional[dict]:
    """Try to parse JSON; fall back to extracting the first {...} block."""
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(raw[start:end])
            except json.JSONDecodeError:
                pass
    return None


def generate_ai_content(title: str, channel_name: str, transcript: str) -> dict:
    """
    Call OpenAI and return a dict with all generated content fields.
    If OPENAI_API_KEY is absent or the call fails, returns empty strings.
    """
    if not config.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set — skipping AI generation.")
        return _empty()

    try:
        from openai import OpenAI
    except ImportError:
        logger.error("openai package not installed — run: pip install openai")
        return _empty()

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    # Trim transcript to stay within token budget
    truncated = transcript[:_MAX_TRANSCRIPT_CHARS]
    if len(transcript) > _MAX_TRANSCRIPT_CHARS:
        truncated += "\n[… transcript truncated …]"

    prompt = _PROMPT_TEMPLATE.format(
        title=title,
        channel=channel_name,
        transcript=truncated,
    )

    try:
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2_000,
        )
        raw_content = response.choices[0].message.content or ""
        data = _parse_json_safe(raw_content)
        if data:
            logger.info("AI content generated for: %s", title)
            return data
        logger.warning("Could not parse AI JSON response for: %s", title)
        logger.debug("Raw AI response: %s", raw_content[:500])
        return _empty()

    except Exception as exc:
        logger.error("OpenAI API error for '%s': %s", title, exc, exc_info=True)
        return _empty()


def save_summary_file(
    video_id: str, title: str, channel_name: str, ai: dict
) -> str:
    """Write AI-generated content to /summaries/<video_id>_<title>_summary.txt."""
    os.makedirs(config.SUMMARIES_DIR, exist_ok=True)
    safe = "".join(c if (c.isalnum() or c in " -_") else "_" for c in title)[:80]
    path = os.path.join(config.SUMMARIES_DIR, f"{video_id}_{safe}_summary.txt")

    sections = [
        ("SUMMARY",        ai.get("summary", "")),
        ("KEY POINTS",     ai.get("key_points", "")),
        ("HASHTAGS",       ai.get("hashtags", "")),
        ("LINKEDIN POST",  ai.get("linkedin_post", "")),
        ("TWITTER/X POST", ai.get("twitter_post", "")),
        ("BLOG OUTLINE",   ai.get("blog_outline", "")),
    ]

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"Video   : {title}\n")
        fh.write(f"Channel : {channel_name}\n")
        fh.write(f"URL     : https://www.youtube.com/watch?v={video_id}\n")
        fh.write("=" * 60 + "\n")
        for heading, body in sections:
            fh.write(f"\n{heading}\n{'-' * len(heading)}\n")
            fh.write((body or "N/A") + "\n")

    logger.info("Summary saved → %s", path)
    return path
