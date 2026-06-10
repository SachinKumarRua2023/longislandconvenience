"""
Image Downloader: downloads competitor product images and saves them
to the website's images/ subfolder inside ScrappedMaterial.
"""

import os
import re
import time
import hashlib
import requests
from pathlib import Path
from urllib.parse import urlparse
from typing import List, Optional
from io import BytesIO

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from config import HEADERS, DELAY_BETWEEN_REQUESTS, IMAGE_MAX_SIZE


def _safe_filename(url: str, index: int) -> str:
    """Generate a safe filename from a URL."""
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        ext = ".jpg"
    # Use URL hash for uniqueness
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    return f"img_{index:03d}_{url_hash}{ext}"


def download_image(
    url: str,
    save_path: Path,
    filename: str,
    resize: bool = True,
) -> Optional[str]:
    """
    Download a single image and save it to save_path/filename.
    Returns the saved filename, or None on failure.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, stream=True)
        if resp.status_code != 200:
            return None

        content = resp.content
        if len(content) < 1000:
            return None

        filepath = save_path / filename

        if PIL_AVAILABLE and resize:
            try:
                img = Image.open(BytesIO(content))
                img = img.convert("RGB")
                img.thumbnail(IMAGE_MAX_SIZE, Image.LANCZOS)
                # Always save as JPEG for consistency
                jpeg_name = filename.rsplit(".", 1)[0] + ".jpg"
                img.save(save_path / jpeg_name, "JPEG", quality=85)
                return jpeg_name
            except Exception:
                pass

        with open(filepath, "wb") as f:
            f.write(content)
        return filename

    except Exception as e:
        return None


def download_competitor_images(
    image_urls: List[str],
    output_dir: Path,
    competitor_name: str,
    max_images: int = 15,
) -> List[dict]:
    """
    Download all images for a competitor and return a list of
    {url, filename, saved_path, status} records.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []

    safe_name = re.sub(r"[^\w\-]", "_", competitor_name.lower())[:30]

    for i, img_url in enumerate(image_urls[:max_images]):
        filename = f"{safe_name}_{i+1:03d}.jpg"
        saved = download_image(img_url, output_dir, filename)
        records.append({
            "competitor": competitor_name,
            "image_url": img_url,
            "saved_filename": saved or "",
            "status": "OK" if saved else "FAILED",
        })
        time.sleep(DELAY_BETWEEN_REQUESTS * 0.5)

    ok_count = sum(1 for r in records if r["status"] == "OK")
    print(f"      Images: {ok_count}/{len(image_urls[:max_images])} saved to {output_dir.name}/")
    return records
