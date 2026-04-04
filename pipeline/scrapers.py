# ═══════════════════════════════════════════════════════════════
# HydROI Pipeline — Scrapers
# Sources: RERA Telangana · 99acres · MagicBricks · Govt news
# ═══════════════════════════════════════════════════════════════

import requests
import json
import time
import re
import os
import warnings
from datetime import datetime, timedelta
from bs4 import BeautifulSoup  # uses Python's built-in html.parser — no lxml needed
# Suppress SSL warnings for government sites with expired/self-signed certs
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

from config import (
    SCRAPE_DELAY_SECONDS, SCRAPE_TIMEOUT, USE_CACHED_ON_FAILURE,
    LOCALITIES, GOVT_NEWS_SOURCES, GOVT_ALERT_KEYWORDS
)

CACHE_DIR = "output/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Standard browser headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,te;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

# Enhanced headers for property portals (helps bypass basic bot detection)
PORTAL_HEADERS = {
    **HEADERS,
    "Referer": "https://www.google.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}


# ───────────────────────────────────────────────────────────────
# HELPERS
# ───────────────────────────────────────────────────────────────

def _get(url, params=None, json_mode=False, verify_ssl=True, use_portal_headers=False):
    """Safe HTTP GET with SSL flexibility and caching on failure."""
    cache_key = re.sub(r'[^a-z0-9]', '_', url.lower())[:80]
    cache_path = os.path.join(CACHE_DIR, cache_key + ".json")
    hdrs = PORTAL_HEADERS if use_portal_headers else HEADERS

    try:
        time.sleep(SCRAPE_DELAY_SECONDS)
        resp = requests.get(url, headers=hdrs, params=params,
                            timeout=SCRAPE_TIMEOUT, verify=verify_ssl)
        resp.raise_for_status()
        data = resp.json() if json_mode else resp.text

        # Save to cache
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"ts": datetime.now().isoformat(), "data": data}, f)

        print(f"  ✓ Fetched: {url[:70]}")
        return data

    except requests.exceptions.SSLError:
        # Retry without SSL verification for government sites with bad certs
        try:
            time.sleep(1)
            resp = requests.get(url, headers=hdrs, params=params,
                                timeout=SCRAPE_TIMEOUT, verify=False)
            resp.raise_for_status()
            data = resp.json() if json_mode else resp.text
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({"ts": datetime.now().isoformat(), "data": data}, f)
            print(f"  ✓ Fetched (SSL bypass): {url[:70]}")
            return data
        except Exception as e2:
            print(f"  ✗ Failed (SSL bypass too): {url[:70]} → {e2}")

    except Exception as e:
        print(f"  ✗ Failed: {url[:70]} → {e}")

    if USE_CACHED_ON_FAILURE and os.path.exists(cache_path):
        print(f"    → Using cached data from {cache_path}")
        with open(cache_path, encoding="utf-8") as f:
            return json.load(f)["data"]
    return None


def _parse_price(text):
    """Extract numeric price from strings like '₹8,500/sqft' or '8500'."""
    if not text:
        return None
    text = str(text).replace(",", "").replace("₹", "").replace(" ", "")
    match = re.search(r'(\d+(?:\.\d+)?)', text)
    return float(match.group(1)) if match else None


# ───────────────────────────────────────────────────────────────
# RERA TELANGANA SCRAPER
# Source: https://rera.telangana.gov.in/
# Data: project registrations, developer names, unit counts, locality
# ───────────────────────────────────────────────────────────────

RERA_BASE_URL = "https://rera.telangana.gov.in"

# Known RERA Telangana API endpoints (try each until one works)
RERA_API_CANDIDATES = [
    "https://rera.telangana.gov.in/api/project/search",
    "https://rera.telangana.gov.in/reraService/api/v1/project/list",
    "https://rera.telangana.gov.in/reraService/getProjectDetails",
]

def scrape_rera(locality_name):
    """
    Fetch registered real estate projects in a locality from RERA Telangana.
    Returns: { total_projects, recent_registrations_90d, avg_units_per_project, projects[] }
    """
    print(f"\n[RERA] Scraping: {locality_name}")
    projects = []

    # Try each known API endpoint
    for api_url in RERA_API_CANDIDATES:
        try:
            time.sleep(SCRAPE_DELAY_SECONDS)
            resp = requests.post(
                api_url,
                headers={**HEADERS,
                         "Content-Type": "application/json",
                         "X-Requested-With": "XMLHttpRequest"},
                json={"district": "Hyderabad", "mandal": locality_name,
                      "start": 0, "length": 50},
                timeout=SCRAPE_TIMEOUT,
                verify=False
            )
            if resp.status_code == 200:
                data = resp.json()
                projects = data.get("data") or data.get("projects") or []
                if projects:
                    print(f"  ✓ RERA API responded: {api_url[:60]}")
                    break
        except Exception:
            pass

    # Fallback: scrape the main search page HTML
    if not projects:
        search_url = f"{RERA_BASE_URL}/projectSearch"
        html = _get(search_url, verify_ssl=False)
        if html:
            projects = _parse_rera_html(html, locality_name)

    # Calculate stats
    now = datetime.now()
    recent_threshold = now - timedelta(days=90)
    recent = []
    total_units = 0

    parsed_projects = []
    for p in projects[:30]:
        reg_date_str = p.get("registrationDate") or p.get("RegDate") or ""
        try:
            reg_date = datetime.strptime(reg_date_str[:10], "%Y-%m-%d")
            is_recent = reg_date >= recent_threshold
        except Exception:
            is_recent = False

        units = int(p.get("noOfUnits") or p.get("NoOfUnits") or 0)
        total_units += units

        project_info = {
            "name":      p.get("projectName") or p.get("ProjectName") or "Unknown",
            "developer": p.get("promoterName") or p.get("PromoterName") or "Unknown",
            "units":     units,
            "reg_date":  reg_date_str[:10],
            "is_recent": is_recent,
        }
        parsed_projects.append(project_info)
        if is_recent:
            recent.append(project_info)

    result = {
        "total_projects":              len(parsed_projects),
        "recent_registrations_90d":    len(recent),
        "avg_units":                   int(total_units / len(parsed_projects)) if parsed_projects else 0,
        "projects":                    parsed_projects[:10],  # top 10 for the report
        "source":                      "rera.telangana.gov.in",
        "scraped_at":                  datetime.now().isoformat(),
    }

    print(f"  → {result['total_projects']} projects, {result['recent_registrations_90d']} recent (90d)")
    return result


def _parse_rera_html(html, locality_name):
    """Fallback: parse RERA project list HTML."""
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    projects = []
    for row in soup.select("table tbody tr"):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cols) >= 3 and locality_name.lower() in html.lower():
            projects.append({
                "projectName":    cols[1] if len(cols) > 1 else "",
                "promoterName":   cols[2] if len(cols) > 2 else "",
                "noOfUnits":      cols[4] if len(cols) > 4 else "0",
                "registrationDate": cols[5] if len(cols) > 5 else "",
            })
    return projects


# ───────────────────────────────────────────────────────────────
# 99ACRES SCRAPER
# Source: https://www.99acres.com
# Data: current listings, avg price/sqft, price range
# ───────────────────────────────────────────────────────────────

def scrape_99acres(locality_keyword):
    """
    Scrape current property listings from 99acres for a Hyderabad locality.
    Tries multiple URL patterns and falls back to MagicBricks if blocked.
    Returns: { avg_price_sqft, min_price, max_price, listing_count, price_trend }
    """
    print(f"\n[99acres] Scraping: {locality_keyword}")

    # 99acres uses different URL patterns — try each
    url_candidates = [
        f"https://www.99acres.com/property-for-sale-in-{locality_keyword}-hyderabad-ffid",
        f"https://www.99acres.com/search/property/buy/{locality_keyword}-hyderabad",
        f"https://www.99acres.com/property-rates-and-price-trends-in-{locality_keyword}-proptypeid-10-city-18",
    ]

    html = None
    for url in url_candidates:
        html = _get(url, use_portal_headers=True)
        if html and len(html) > 5000:  # got a real page, not a redirect/error
            break
        time.sleep(1)

    if not html or len(html) < 5000:
        return _fallback_listing_data(locality_keyword)

    soup = BeautifulSoup(html, "html.parser")
    prices = []

    # 99acres embeds property data in script tags as JSON
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            obj = json.loads(script.string or "")
            if isinstance(obj, list):
                for item in obj:
                    price_str = item.get("offers", {}).get("price") or item.get("price")
                    if price_str:
                        p = _parse_price(price_str)
                        if p and 1000 < p < 50000:  # sanity check: ₹1k–₹50k/sqft
                            prices.append(p)
        except Exception:
            pass

    # Also try scraping visible price tags
    for el in soup.select("[class*='price'], [data-price], .priceVal"):
        text = el.get_text(strip=True)
        if "sqft" in text.lower() or "sq" in text.lower():
            p = _parse_price(text)
            if p and 1000 < p < 50000:
                prices.append(p)

    if prices:
        result = {
            "avg_price_sqft": int(sum(prices) / len(prices)),
            "min_price_sqft": int(min(prices)),
            "max_price_sqft": int(max(prices)),
            "listing_count":  len(prices),
            "source":         "99acres.com",
            "scraped_at":     datetime.now().isoformat(),
        }
    else:
        print(f"  → No structured prices found, using MagicBricks fallback...")
        result = scrape_magicbricks(locality_keyword)

    print(f"  → Avg: ₹{result.get('avg_price_sqft','?')}/sqft from {result.get('listing_count','?')} listings")
    return result


def scrape_magicbricks(locality_keyword):
    """Fallback scraper for MagicBricks property prices."""
    print(f"\n[MagicBricks] Scraping: {locality_keyword}")

    url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&cityName=Hyderabad&localityName={locality_keyword}"
    html = _get(url, use_portal_headers=True)

    if not html:
        return _fallback_listing_data(locality_keyword)

    soup = BeautifulSoup(html, "html.parser")
    prices = []

    for el in soup.select(".mb-srp__card--price, .price, [data-price]"):
        text = el.get_text(strip=True)
        p = _parse_price(text)
        if p and 1000 < p < 50000:
            prices.append(p)

    if prices:
        return {
            "avg_price_sqft": int(sum(prices) / len(prices)),
            "min_price_sqft": int(min(prices)),
            "max_price_sqft": int(max(prices)),
            "listing_count":  len(prices),
            "source":         "magicbricks.com",
            "scraped_at":     datetime.now().isoformat(),
        }

    return _fallback_listing_data(locality_keyword)


def _fallback_listing_data(locality_keyword):
    """
    Last resort: return last known prices from cache or baseline estimates.
    These are updated manually until live scraping is fully stable.
    """
    # Real prices sourced via Chrome browser scraping of 99acres.com — March 2026
    BASELINE = {
        "kokapet":    {"avg_price_sqft": 10394, "listing_count": 912},
        "gachibowli": {"avg_price_sqft": 10665, "listing_count": 523},
        "miyapur":    {"avg_price_sqft":  7413, "listing_count": 932},
        "kompally":   {"avg_price_sqft":  8695, "listing_count": 758},
        "jubilee-hills": {"avg_price_sqft": 12500, "listing_count": 98},
        "manikonda":  {"avg_price_sqft":  5200, "listing_count": 410},
        "uppal":      {"avg_price_sqft":  3900, "listing_count": 520},
        "shamshabad": {"avg_price_sqft":  7312, "listing_count": 300},
    }
    base = BASELINE.get(locality_keyword, {"avg_price_sqft": 5000, "listing_count": 100})
    return {
        **base,
        "min_price_sqft": int(base["avg_price_sqft"] * 0.75),
        "max_price_sqft": int(base["avg_price_sqft"] * 1.40),
        "source":         "baseline_estimate",
        "scraped_at":     datetime.now().isoformat(),
    }


# ───────────────────────────────────────────────────────────────
# GOVERNMENT NEWS MONITOR
# Sources: HMDA · TSIIC · Telangana Govt · RERA News
# ───────────────────────────────────────────────────────────────

def scrape_govt_alerts(locality_id=None):
    """
    Scrape recent government announcements and filter for real-estate-relevant items.
    Returns: list of { title, body, source, url, date, impact, localities_affected }
    """
    print("\n[Govt Monitor] Scraping government sources...")
    all_alerts = []

    for source in GOVT_NEWS_SOURCES:
        print(f"  → {source['name']}: {source['url']}")
        html = _get(source["url"], verify_ssl=False)  # govt sites often have SSL issues
        if not html:
            continue

        alerts = _parse_news_html(html, source["name"], source["url"])
        all_alerts.extend(alerts)

    # Deduplicate by title similarity
    seen_titles = set()
    unique_alerts = []
    for a in all_alerts:
        key = a["title"].lower()[:40]
        if key not in seen_titles:
            seen_titles.add(key)
            unique_alerts.append(a)

    # Tag which localities each alert affects
    for alert in unique_alerts:
        alert["localities_affected"] = _tag_localities(alert["title"] + " " + alert["body"])

    print(f"  → {len(unique_alerts)} unique govt alerts found")
    return unique_alerts


def _parse_news_html(html, source_name, source_url):
    """Parse news items from a government HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    alerts = []

    # Try common news listing patterns
    selectors = [
        "article", ".news-item", ".announcement", "li.news",
        "div.news", "tr td a", ".latest-news li", ".whats-new li"
    ]

    items_found = []
    for sel in selectors:
        items = soup.select(sel)
        if items:
            items_found = items[:20]
            break

    if not items_found:
        # Fallback: grab all links with keywords
        items_found = [a for a in soup.find_all("a", href=True)
                       if any(kw.lower() in a.get_text(strip=True).lower()
                              for kw in GOVT_ALERT_KEYWORDS)][:15]

    for item in items_found:
        title = item.get_text(strip=True)[:200]
        if not title or len(title) < 15:
            continue

        # Only keep alerts relevant to real estate
        title_lower = title.lower()
        if not any(kw.lower() in title_lower for kw in GOVT_ALERT_KEYWORDS):
            continue

        # Try to find a date nearby
        date_str = _extract_date(item) or datetime.now().strftime("%Y-%m-%d")

        # Determine sentiment (positive = investment signal)
        impact = "positive" if any(w in title_lower for w in
                                    ["approved", "launch", "open", "complete", "award",
                                     "inaugurate", "notif", "allot"]) else "neutral"

        alerts.append({
            "title":   title,
            "body":    title,  # Summary — full body needs detail page fetch
            "source":  source_name,
            "url":     source_url,
            "date":    date_str,
            "impact":  impact,
        })

    return alerts


def _extract_date(element):
    """Try to find a date string near an HTML element."""
    text = element.get_text(" ", strip=True)
    patterns = [
        r'\d{2}[/-]\d{2}[/-]\d{4}',
        r'\d{4}[/-]\d{2}[/-]\d{2}',
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(0)
    return None


def _tag_localities(text):
    """Return list of locality IDs mentioned in the text."""
    text_lower = text.lower()
    tags = []
    locality_map = {
        "kokapet":    ["kokapet", "financial district", "nanakramguda"],
        "gachibowli": ["gachibowli", "hitech city", "hitec city", "biodiversity"],
        "miyapur":    ["miyapur", "bachupally", "patancheru", "kondapur"],
        "kompally":   ["kompally", "medchal", "bowrampet", "nh44", "nh-44"],
        "jubilee":    ["jubilee hills", "jubilee", "banjara hills", "road no. 36"],
        "manikonda":  ["manikonda", "lanco hills", "khajaguda", "raidurgam"],
        "uppal":      ["uppal", "nacharam", "nagole", "lb nagar", "knowledge city"],
        "shamshabad": ["shamshabad", "pharma city", "rgia", "airport", "ibrahimpatnam"],
    }
    for loc_id, keywords in locality_map.items():
        if any(kw in text_lower for kw in keywords):
            tags.append(loc_id)
    return tags if tags else ["all"]


# ───────────────────────────────────────────────────────────────
# CITY-LEVEL STATS SCRAPER
# ───────────────────────────────────────────────────────────────

def scrape_city_stats():
    """
    Scrape top-level Hyderabad market stats from Knight Frank / PropEquity reports
    and RERA Telangana aggregate data.
    """
    print("\n[City Stats] Scraping city-level stats...")

    # Try RERA aggregate stats
    rera_html = _get("https://rera.telangana.gov.in/dashboard", verify_ssl=False)
    city_stats = {
        "avg_price_sqft":     6840,
        "quarterly_sales":    4820,
        "nri_investment_cr":  2840,
        "active_projects":    1240,
        "unsold_inventory":   28400,
        "source":             "baseline",
        "scraped_at":         datetime.now().isoformat(),
    }

    if rera_html:
        soup = BeautifulSoup(rera_html, "html.parser")
        # Try to extract registration counts from RERA dashboard
        for el in soup.select(".count, .total, .stat-value, .dashboard-number"):
            text = el.get_text(strip=True)
            n = _parse_price(text)
            if n:
                if 500 < n < 5000:
                    city_stats["active_projects"] = int(n)
                    city_stats["source"] = "rera.telangana.gov.in"
                    break

    print(f"  → City avg: ₹{city_stats['avg_price_sqft']}/sqft, "
          f"{city_stats['quarterly_sales']} units/qtr")
    return city_stats


# ───────────────────────────────────────────────────────────────
# MAIN — run scrapers for all localities
# ───────────────────────────────────────────────────────────────

def run_all_scrapers():
    """
    Run all scrapers and return a structured data dict.
    Called by pipeline.py
    """
    print("\n" + "═"*60)
    print("  RUNNING ALL SCRAPERS")
    print("═"*60)

    results = {
        "city_stats":  scrape_city_stats(),
        "localities":  {},
        "govt_alerts": scrape_govt_alerts(),
    }

    for loc in LOCALITIES:
        lid = loc["id"]
        print(f"\n{'─'*50}")
        print(f"  LOCALITY: {loc['name']}")
        print(f"{'─'*50}")

        rera_data    = scrape_rera(loc["rera_keyword"])
        listing_data = scrape_99acres(loc["acres_keyword"])

        results["localities"][lid] = {
            "rera":     rera_data,
            "listings": listing_data,
        }

    print("\n" + "═"*60)
    print("  SCRAPING COMPLETE")
    print("═"*60)
    return results


if __name__ == "__main__":
    import json
    data = run_all_scrapers()
    with open("output/raw_scraped.json", "w") as f:
        json.dump(data, f, indent=2)
    print("\n✓ Saved to output/raw_scraped.json")
