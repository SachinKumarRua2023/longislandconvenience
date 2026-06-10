"""
Competitor Discovery: uses DuckDuckGo search to find top competitors
for each of the 7 Hiren Kumar websites.
"""

import time
import re
from urllib.parse import urlparse
from typing import List, Dict, Optional
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
from config import DELAY_BETWEEN_REQUESTS, TOP_N_COMPETITORS


def _extract_domain(url: str) -> str:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return url


def _is_valid_competitor(url: str, own_domain: str, blacklist: List[str]) -> bool:
    """Filter out irrelevant results like social media, directories, news."""
    skip_domains = [
        "facebook.com", "instagram.com", "twitter.com", "x.com",
        "youtube.com", "linkedin.com", "pinterest.com", "tiktok.com",
        "yelp.com", "yellowpages.com", "bbb.org", "tripadvisor.com",
        "google.com", "bing.com", "yahoo.com", "wikipedia.org",
        "reddit.com", "nextdoor.com", "thumbtack.com", "angi.com",
        "homeadvisor.com", "angieslist.com", "houzz.com",
        "craigslist.org", "offerup.com", "mercari.com",
        "amazon.com", "ebay.com", "walmart.com", "target.com",
    ]
    domain = _extract_domain(url)
    if domain == own_domain:
        return False
    for skip in skip_domains + blacklist:
        if skip in domain:
            return False
    return True


def search_competitors(
    site_key: str,
    site_config: Dict,
    max_results: int = TOP_N_COMPETITORS,
) -> List[Dict]:
    """
    Search DuckDuckGo for top competitors for a given website niche.
    Returns list of competitor dicts with name, url, domain, snippet.
    """
    own_domain = site_config["domain"]
    queries = site_config["search_queries"]
    seen_domains: set = set()
    competitors: List[Dict] = []

    print(f"\n  Searching competitors for: {site_config['business_name']}")

    with DDGS() as ddgs:
        for query in queries:
            if len(competitors) >= max_results:
                break
            try:
                print(f"    DDG query: \"{query}\"")
                results = list(ddgs.text(
                    query,
                    region="us-en",
                    safesearch="off",
                    max_results=15,
                ))
                time.sleep(DELAY_BETWEEN_REQUESTS)

                for r in results:
                    if len(competitors) >= max_results:
                        break
                    url = r.get("href", "")
                    if not url:
                        continue
                    domain = _extract_domain(url)
                    if domain in seen_domains:
                        continue
                    if not _is_valid_competitor(url, own_domain, []):
                        continue
                    seen_domains.add(domain)
                    competitors.append({
                        "rank": len(competitors) + 1,
                        "name": r.get("title", domain).strip(),
                        "url": url,
                        "domain": domain,
                        "snippet": r.get("body", "").strip(),
                        "source_query": query,
                    })

            except Exception as e:
                print(f"    Search error for '{query}': {e}")
                time.sleep(DELAY_BETWEEN_REQUESTS * 2)

    # Also add known competitors if not already found
    for known in site_config.get("known_competitors", []):
        known_domain = _extract_domain("http://" + known)
        if known_domain not in seen_domains and len(competitors) < max_results + 3:
            competitors.append({
                "rank": len(competitors) + 1,
                "name": known_domain.replace(".com", "").replace("-", " ").title(),
                "url": f"https://{known_domain}",
                "domain": known_domain,
                "snippet": "Known industry competitor",
                "source_query": "manual",
            })
            seen_domains.add(known_domain)

    # Re-rank
    for i, c in enumerate(competitors):
        c["rank"] = i + 1

    print(f"  Found {len(competitors)} competitors for {site_config['business_name']}")
    return competitors
