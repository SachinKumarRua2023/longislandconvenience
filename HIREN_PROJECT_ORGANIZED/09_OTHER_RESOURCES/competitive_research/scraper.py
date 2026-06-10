"""
Product & Contact Scraper: visits competitor websites and extracts
product names, prices, descriptions, contact info, and image URLs.
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional, Tuple
from config import HEADERS, DELAY_BETWEEN_REQUESTS, MAX_PRODUCTS_PER_COMPETITOR


def _get_page(url: str, timeout: int = 12) -> Optional[BeautifulSoup]:
    """Fetch a URL and return parsed BeautifulSoup, or None on failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, "lxml")
        return None
    except Exception as e:
        print(f"      Fetch failed {url}: {e}")
        return None


def _clean_price(text: str) -> Optional[str]:
    """Extract a price string from messy text."""
    match = re.search(r"\$\s*(\d{1,4}(?:[.,]\d{2,3})?)", text)
    if match:
        return "$" + match.group(1).replace(",", "")
    return None


def _clean_text(text: str) -> str:
    return " ".join(text.split()).strip()


def extract_products(url: str, competitor_name: str, categories: List[str]) -> List[Dict]:
    """
    Scrape products (name, price, description, image_url) from a competitor site.
    Tries /shop, /products, /store, /menu, /services pages first.
    """
    products: List[Dict] = []
    base_url = url if url.endswith("/") else url + "/"
    parsed = urlparse(url)
    base_domain = f"{parsed.scheme}://{parsed.netloc}"

    candidate_paths = [
        "", "/shop", "/products", "/store", "/menu",
        "/services", "/catalog", "/collections/all",
        "/product-category/all", "/items", "/order",
    ]

    tried_urls: set = set()

    for path in candidate_paths:
        if len(products) >= MAX_PRODUCTS_PER_COMPETITOR:
            break
        target = base_domain + path
        if target in tried_urls:
            continue
        tried_urls.add(target)

        soup = _get_page(target)
        if not soup:
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        found = _parse_products_from_page(soup, target, competitor_name)
        products.extend(found)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        if len(products) >= 5:
            break

    # Deduplicate by name
    seen_names: set = set()
    unique: List[Dict] = []
    for p in products:
        key = p.get("name", "").lower()
        if key and key not in seen_names:
            seen_names.add(key)
            unique.append(p)

    return unique[:MAX_PRODUCTS_PER_COMPETITOR]


def _parse_products_from_page(soup: BeautifulSoup, page_url: str, competitor: str) -> List[Dict]:
    """Extract product data from a BeautifulSoup page."""
    products: List[Dict] = []
    parsed_base = urlparse(page_url)
    base = f"{parsed_base.scheme}://{parsed_base.netloc}"

    # WooCommerce / generic product cards
    product_selectors = [
        "li.product", "div.product", "article.product",
        ".product-item", ".product-card", ".product-tile",
        ".item-product", "[class*='product']",
        ".menu-item", ".service-item", ".service-card",
        "[class*='service']", "[class*='item']",
        "div.card", "article.post",
    ]

    items = []
    for sel in product_selectors:
        items = soup.select(sel)
        if len(items) >= 3:
            break

    if not items:
        # Fallback: look for price-containing elements
        items = soup.find_all(True, string=re.compile(r"\$\s*\d+"))

    for item in items[:MAX_PRODUCTS_PER_COMPETITOR]:
        try:
            # Name
            name_el = (
                item.select_one("h1,h2,h3,h4,h5,.product-title,.product-name,.item-title,.service-title,.card-title")
                or item.select_one("[class*='title'], [class*='name']")
            )
            name = _clean_text(name_el.get_text()) if name_el else ""
            if not name or len(name) < 2:
                continue

            # Price
            price_el = item.select_one(
                ".price, .product-price, [class*='price'], .amount, ins .amount"
            )
            raw_price = price_el.get_text() if price_el else ""
            price = _clean_price(raw_price) or ""

            # Description
            desc_el = item.select_one(
                ".description, .product-description, .excerpt, p, [class*='desc']"
            )
            description = _clean_text(desc_el.get_text()) if desc_el else ""
            description = description[:200]

            # Image
            img_el = item.select_one("img")
            img_url = ""
            if img_el:
                src = img_el.get("src") or img_el.get("data-src") or img_el.get("data-lazy-src") or ""
                if src and not src.startswith("data:"):
                    img_url = urljoin(page_url, src)

            # Product URL
            link_el = item.select_one("a[href]")
            product_url = urljoin(page_url, link_el["href"]) if link_el else page_url

            products.append({
                "competitor": competitor,
                "name": name,
                "price": price,
                "description": description,
                "image_url": img_url,
                "product_url": product_url,
                "source_page": page_url,
            })
        except Exception:
            continue

    return products


def extract_contact_info(url: str) -> Dict:
    """
    Extract public business contact info from a website's contact/about pages.
    Returns dict with email, phone, address, contact_page_url.
    """
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    contact_paths = [
        "/contact", "/contact-us", "/about", "/about-us",
        "/get-in-touch", "/reach-us", "/info", "/location",
    ]

    best: Dict = {
        "email": "",
        "phone": "",
        "address": "",
        "contact_page": "",
    }

    # Also check homepage
    pages_to_check = [base] + [base + p for p in contact_paths]

    for page_url in pages_to_check:
        soup = _get_page(page_url)
        if not soup:
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        text = soup.get_text(" ", strip=True)

        # Email
        if not best["email"]:
            email_matches = re.findall(
                r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6}", text
            )
            # Filter out social media / image extensions
            skip_patterns = ["@2x", "@3x", ".png", ".jpg", ".gif", "noreply", "example.com"]
            for em in email_matches:
                if not any(s in em.lower() for s in skip_patterns):
                    best["email"] = em.lower()
                    best["contact_page"] = page_url
                    break

        # Phone
        if not best["phone"]:
            phone_matches = re.findall(
                r"(?:\+1[\s\-.]?)?\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{4}", text
            )
            if phone_matches:
                best["phone"] = phone_matches[0].strip()
                best["contact_page"] = page_url

        # Address (look for NY / street patterns)
        if not best["address"]:
            addr_match = re.search(
                r"\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Blvd|Lane|Ln|Way|Place|Pl)"
                r"[,\s]+[A-Za-z\s]+,\s*NY[\s,]*\d{5}",
                text, re.IGNORECASE
            )
            if addr_match:
                best["address"] = addr_match.group(0).strip()

        time.sleep(DELAY_BETWEEN_REQUESTS)

        if best["email"] and best["phone"]:
            break

    return best


def get_all_images_from_site(url: str, limit: int = 15) -> List[str]:
    """
    Collect product/category image URLs from a competitor's homepage + shop page.
    Returns list of absolute image URLs.
    """
    image_urls: List[str] = []
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    pages = [base, base + "/shop", base + "/products", base + "/menu", base + "/services"]

    seen: set = set()
    skip_patterns = [
        "logo", "icon", "favicon", "banner-bg", "avatar",
        "placeholder", "pixel", "blank", "sprite",
    ]

    for page_url in pages:
        if len(image_urls) >= limit:
            break
        soup = _get_page(page_url)
        if not soup:
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        for img in soup.find_all("img"):
            if len(image_urls) >= limit:
                break
            src = (
                img.get("src") or img.get("data-src")
                or img.get("data-lazy-src") or img.get("data-original") or ""
            )
            if not src or src.startswith("data:"):
                continue
            full_url = urljoin(page_url, src)
            if full_url in seen:
                continue
            lower = full_url.lower()
            if any(p in lower for p in skip_patterns):
                continue
            # Only images with meaningful extensions
            if not any(lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]):
                if "?" in lower:
                    base_path = lower.split("?")[0]
                    if not any(base_path.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                        continue
                else:
                    continue
            seen.add(full_url)
            image_urls.append(full_url)

        time.sleep(DELAY_BETWEEN_REQUESTS)

    return image_urls[:limit]
