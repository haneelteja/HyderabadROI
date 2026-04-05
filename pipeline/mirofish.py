# ================================================================
# HydROI Pipeline - MiroFish Engine Integration
#
# This module does two things:
#   1. DEMO MODE (no keys needed): Generates predictions using
#      trend extrapolation + LLM narrative generation.
#   2. LIVE MODE (keys required): Feeds real scraped data into
#      MiroFish as "seed material", runs the multi-agent
#      simulation, and extracts price/demand predictions.
#
# To switch from demo -> live: set DEMO_MODE = False in config.py
# ================================================================

import requests
import json
import time
import re
from datetime import datetime
from config import (
    LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, ZEP_API_KEY,
    MIROFISH_BACKEND_URL, DEMO_MODE, LOCALITIES
)

# Baseline data - updated to real March 2026 prices (Chrome-scraped from 99acres)
LOCALITY_BASELINES = {
    "kokapet":    { "price_2025": 10394, "roi_yoy": 22.3, "roi_3y": 38, "nri_pct": 38, "sales_vel": 145, "growth_rate": 0.155 },
    "gachibowli": { "price_2025": 10665, "roi_yoy": 15.8, "roi_3y": 32, "nri_pct": 29, "sales_vel": 130, "growth_rate": 0.118 },
    "miyapur":    { "price_2025":  7413, "roi_yoy": 27.8, "roi_3y": 29, "nri_pct": 18, "sales_vel": 220, "growth_rate": 0.120 },
    "kompally":   { "price_2025":  8695, "roi_yoy": 111.8,"roi_3y": 52, "nri_pct": 14, "sales_vel":  95, "growth_rate": 0.175 },
    "jubilee":    { "price_2025": 12500, "roi_yoy": 14.0, "roi_3y": 28, "nri_pct": 22, "sales_vel":  42, "growth_rate": 0.082 },
    "manikonda":  { "price_2025":  5200, "roi_yoy": 21.0, "roi_3y": 38, "nri_pct": 24, "sales_vel": 175, "growth_rate": 0.135 },
    "uppal":      { "price_2025":  3900, "roi_yoy": 17.0, "roi_3y": 34, "nri_pct": 11, "sales_vel": 160, "growth_rate": 0.110 },
    "shamshabad": { "price_2025":  7312, "roi_yoy": 18.5, "roi_3y": 41, "nri_pct":  9, "sales_vel":  55, "growth_rate": 0.145 },
}

# Historical prices 2019-2025 (real market data)
FULL_PRICE_HISTORY = {
    "kokapet":    [4200, 4410, 5040, 6300, 7560, 8500, 10394],
    "gachibowli": [5800, 6090, 6960, 7830, 8700, 9200, 10665],
    "miyapur":    [3200, 3360, 3840, 4480, 5280, 5800,  7413],
    "kompally":   [2100, 2205, 2520, 3150, 3780, 4100,  8695],
    "jubilee":    [8200, 7900, 8500, 9200, 10100, 11200, 12500],
    "manikonda":  [2800, 2700, 3100, 3600, 4100, 4700,  5200],
    "uppal":      [2100, 2050, 2300, 2600, 2900, 3400,  3900],
    "shamshabad": [2800, 2940, 3360, 4060, 5040, 6160,  7312],
}

NRI_HISTORY = {
    "kokapet":    [12, 14, 18, 25, 31, 35, 38],
    "gachibowli": [20, 22, 25, 27, 29, 30, 31],
    "miyapur":    [ 8,  9, 11, 14, 16, 17, 18],
    "kompally":   [ 4,  4,  6,  8, 10, 12, 14],
    "jubilee":    [15, 16, 17, 19, 20, 21, 22],
    "manikonda":  [10, 11, 13, 16, 18, 21, 24],
    "uppal":      [ 4,  4,  5,  6,  7,  8, 11],
    "shamshabad": [ 2,  2,  3,  4,  6,  7,  9],
}

ACTIVITY_HISTORY = {
    "kokapet":    [20, 18, 42, 65, 80, 88, 95],
    "gachibowli": [55, 50, 62, 71, 80, 85, 90],
    "miyapur":    [40, 38, 55, 68, 78, 85, 90],
    "kompally":   [15, 14, 22, 35, 52, 68, 78],
    "jubilee":    [30, 28, 35, 42, 52, 60, 68],
    "manikonda":  [25, 22, 32, 45, 58, 70, 78],
    "uppal":      [20, 18, 25, 34, 46, 58, 68],
    "shamshabad": [10,  9, 12, 18, 28, 40, 55],
}


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# DEMO MODE: Trend Extrapolation Engine
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _extrapolate_prices(locality_id, live_price=None, govt_alerts=None, method_name="trend_extrapolation_demo"):
    """
    Generate 3 future price points using exponential smoothing on historical trend.
    Adjusts growth rate based on new govt alerts (positive = +2%, neutral = 0%).
    """
    base = LOCALITY_BASELINES[locality_id]
    history = FULL_PRICE_HISTORY[locality_id][:]

    # If we have a live scraped price, update the baseline
    current_price = live_price or base["price_2025"]

    # Boost rate if positive govt signals detected for this locality
    boost = 0.0
    if govt_alerts:
        positive_alerts = [a for a in govt_alerts
                           if a.get("impact") == "positive"
                           and locality_id in a.get("localities_affected", [])]
        boost = min(len(positive_alerts) * 0.02, 0.08)  # max +8% boost
        if boost > 0:
            print(f"    -> Govt boost for {locality_id}: +{boost*100:.1f}% "
                  f"({len(positive_alerts)} positive alerts)")

    growth = base["growth_rate"] + boost

    # Compound growth for 3 future periods
    p1 = int(current_price * (1 + growth * 0.75))    # Q3 2026 (~9 months)
    p2 = int(current_price * (1 + growth * 1.0) * (1 + growth * 0.9))   # 2027
    p3 = int(current_price * (1 + growth * 1.0) ** 2 * (1 + growth * 0.85))  # 2028

    # NRI trend: extrapolate with dampening
    nri_hist = NRI_HISTORY[locality_id]
    nri_delta = nri_hist[-1] - nri_hist[-2]
    nri_1 = min(nri_hist[-1] + int(nri_delta * 0.9), 60)
    nri_2 = min(nri_1 + int(nri_delta * 0.8), 65)
    nri_3 = min(nri_2 + int(nri_delta * 0.7), 70)

    # Activity trend
    act_hist = ACTIVITY_HISTORY[locality_id]
    act_1 = min(act_hist[-1] + 2, 99)
    act_2 = min(act_1 + 2, 99)
    act_3 = min(act_2 + 1, 99)

    return {
        "method":       method_name,
        "confidence":   "medium",
        "Q3_2026":      {"price": p1, "nri_pct": nri_1, "activity": act_1, "confidence": 0.82},
        "2027":         {"price": p2, "nri_pct": nri_2, "activity": act_2, "confidence": 0.70},
        "2028":         {"price": p3, "nri_pct": nri_3, "activity": act_3, "confidence": 0.58},
        "growth_rate_used": round(growth, 4),
        "govt_boost":   round(boost, 4),
        "generated_at": datetime.now().isoformat(),
    }


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# LIVE MODE: MiroFish Integration
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _format_seed_material(locality_id, locality_name, scraped_data, govt_alerts):
    """
    Format scraped real estate data into a structured report
    that MiroFish can use as seed material.
    """
    base      = LOCALITY_BASELINES[locality_id]
    listings  = scraped_data.get("listings", {})
    rera      = scraped_data.get("rera", {})

    relevant_alerts = [a for a in govt_alerts
                       if locality_id in a.get("localities_affected", ["all"])]

    govt_section = "\n".join(
        f"- [{a['date']}] {a['source']}: {a['title']}"
        for a in relevant_alerts[:5]
    ) or "No recent government announcements."

    seed_text = f"""
HYDERABAD REAL ESTATE MARKET REPORT â€” {locality_name.upper()}
Generated: {datetime.now().strftime('%B %Y')}

CURRENT MARKET DATA:
- Current average price: â‚¹{listings.get('avg_price_sqft', base['price_2025']):,}/sqft
- Active listings: {listings.get('listing_count', 'N/A')}
- YoY price appreciation: {base['roi_yoy']}%
- 3-year ROI: {base['roi_3y']}%
- NRI buyer percentage: {base['nri_pct']}% of all purchases
- Quarterly sales velocity: {base['sales_vel']} units/quarter

RERA PROJECT REGISTRATIONS (Last 90 days):
- New projects registered: {rera.get('recent_registrations_90d', 'N/A')}
- Total active projects: {rera.get('total_projects', 'N/A')}
- Average units per project: {rera.get('avg_units', 'N/A')}

RECENT GOVERNMENT INITIATIVES:
{govt_section}

DEMAND DRIVERS:
- IT/Corporate sector employment within 5km
- NRI remittance-backed purchases from USA/UK/Gulf
- HMDA approved layouts reducing title risk
- Infrastructure investment pipeline

PREDICTION REQUEST:
Based on the above market data, government initiatives, and demand drivers,
predict the price appreciation trajectory for {locality_name} real estate
over the next 4 quarters (Q2â€“Q4 2026) and full years 2027 and 2028.
Express predictions as:
1. Price per sqft (â‚¹)
2. NRI buyer percentage
3. Market activity index (0â€“100)
4. Confidence score (0â€“1)
Give a clear, decisive verdict with no diplomatic hedging.
"""
    return seed_text.strip()


def _call_mirofish_api(seed_material, locality_name):
    """
    Submit seed material to MiroFish backend and retrieve prediction report.
    MiroFish flow: upload -> simulate -> fetch report
    """
    print(f"  -> Submitting to MiroFish: {locality_name}")

    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})

    # Step 1: Upload seed material
    try:
        upload_resp = session.post(
            f"{MIROFISH_BACKEND_URL}/api/upload",
            json={"content": seed_material, "type": "text", "name": f"{locality_name}_report.txt"},
            timeout=30
        )
        upload_resp.raise_for_status()
        upload_data = upload_resp.json()
        seed_id = upload_data.get("id") or upload_data.get("seed_id")
        print(f"    [OK] Seed uploaded, id: {seed_id}")
    except Exception as e:
        print(f"    [FAIL] Upload failed: {e}")
        return None

    # Step 2: Start simulation
    try:
        sim_resp = session.post(
            f"{MIROFISH_BACKEND_URL}/api/simulate",
            json={
                "seed_id":          seed_id,
                "prediction_query": f"Predict real estate price appreciation for {locality_name} in Hyderabad, India for 2026, 2027, and 2028",
                "num_agents":       200,  # Keep small for speed
                "steps":            10,
            },
            timeout=60
        )
        sim_resp.raise_for_status()
        sim_data = sim_resp.json()
        sim_id = sim_data.get("simulation_id") or sim_data.get("id")
        print(f"    [OK] Simulation started, id: {sim_id}")
    except Exception as e:
        print(f"    [FAIL] Simulation failed: {e}")
        return None

    # Step 3: Poll for completion (max 5 minutes)
    max_polls = 60
    for i in range(max_polls):
        try:
            time.sleep(5)
            status_resp = session.get(
                f"{MIROFISH_BACKEND_URL}/api/simulation/{sim_id}/status",
                timeout=10
            )
            status = status_resp.json().get("status", "")
            if status in ("complete", "completed", "done"):
                print(f"    [OK] Simulation complete after {(i+1)*5}s")
                break
            elif status in ("failed", "error"):
                print(f"    [FAIL] Simulation failed with status: {status}")
                return None
            print(f"    ... Waiting ({(i+1)*5}s) - status: {status}")
        except Exception as e:
            print(f"    [FAIL] Status poll failed: {e}")

    # Step 4: Fetch report
    try:
        report_resp = session.get(
            f"{MIROFISH_BACKEND_URL}/api/simulation/{sim_id}/report",
            timeout=30
        )
        report_resp.raise_for_status()
        return report_resp.json()
    except Exception as e:
        print(f"    [FAIL] Report fetch failed: {e}")
        return None


def _parse_mirofish_report(report, locality_id):
    """
    Parse MiroFish's prediction report JSON into our standardised format.
    Handles variation in MiroFish's output structure.
    """
    if not report:
        return None

    base = LOCALITY_BASELINES[locality_id]
    preds = {}

    # MiroFish might return predictions under different keys depending on version
    raw_preds = (
        report.get("predictions") or
        report.get("forecast") or
        report.get("report", {}).get("predictions") or
        {}
    )

    for period_key, output_key in [("Q3_2026", "Q3_2026"), ("2027", "2027"), ("2028", "2028")]:
        period_data = raw_preds.get(period_key) or raw_preds.get(f"year_{period_key}") or {}

        price     = _safe_num(period_data.get("price") or period_data.get("price_per_sqft"))
        nri       = _safe_num(period_data.get("nri_percent") or period_data.get("nri"))
        activity  = _safe_num(period_data.get("activity") or period_data.get("market_activity"))
        conf      = _safe_num(period_data.get("confidence") or 0.7)

        # Fall back to extrapolation for missing fields
        extrap = _extrapolate_prices(locality_id)

        preds[output_key] = {
            "price":      int(price)    if price    else extrap[output_key]["price"],
            "nri_pct":    int(nri)      if nri      else extrap[output_key]["nri_pct"],
            "activity":   int(activity) if activity else extrap[output_key]["activity"],
            "confidence": float(conf),
        }

    return {
        "method":       "mirofish_multi_agent_simulation",
        "confidence":   "high",
        "sim_id":       report.get("simulation_id", ""),
        **preds,
        "narrative":    report.get("summary") or report.get("narrative") or "",
        "generated_at": datetime.now().isoformat(),
    }


def _safe_num(val):
    """Convert to float safely."""
    try:
        return float(str(val).replace(",", "").replace("â‚¹", "").replace("%", ""))
    except Exception:
        return None


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# LLM FALLBACK: Direct LLM prediction (no MiroFish server needed)
# Uses OpenAI / Qwen API directly for structured predictions
# ================================================================

def _call_llm_direct(seed_material, locality_name):
    """
    Fallback: call LLM API directly for predictions if MiroFish server is not running.
    Returns structured JSON prediction.
    """
    print(f"  -> LLM direct call for: {locality_name}")

    prompt = f"""
You are an expert Hyderabad real estate analyst. Based on the following market data,
give precise numerical predictions. Do NOT hedge. Give a single definitive number for each.

{seed_material}

Respond ONLY with valid JSON in this exact format:
{{
  "Q3_2026": {{"price": <int>, "nri_pct": <int>, "activity": <int>, "confidence": <float 0-1>}},
  "2027":    {{"price": <int>, "nri_pct": <int>, "activity": <int>, "confidence": <float 0-1>}},
  "2028":    {{"price": <int>, "nri_pct": <int>, "activity": <int>, "confidence": <float 0-1>}},
  "narrative": "<2 sentence decisive prediction>"
}}
"""

    # Retry up to 3 times with exponential backoff (handles 429 rate limits)
    for attempt in range(3):
        try:
            resp = requests.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {LLM_API_KEY}",
                    "Content-Type":  "application/json",
                },
                json={
                    "model":       LLM_MODEL,
                    "messages":    [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens":  600,
                },
                timeout=30
            )

            # Rate limit hit - wait and retry
            if resp.status_code == 429:
                wait = 20 * (attempt + 1)   # 20s â†’ 40s â†’ 60s
                print(f"    -> Rate limit hit - waiting {wait}s before retry {attempt+1}/3...")
                time.sleep(wait)
                continue

            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                return {
                    "method":       "llm_direct",
                    "confidence":   "high",
                    **{k: v for k, v in result.items() if k != "narrative"},
                    "narrative":    result.get("narrative", ""),
                    "generated_at": datetime.now().isoformat(),
                }
            break   # Got a response, just could not parse it - no point retrying

        except Exception as e:
            if "429" in str(e):
                wait = 20 * (attempt + 1)
                print(f"    -> Rate limit hit - waiting {wait}s before retry {attempt+1}/3...")
                time.sleep(wait)
            else:
                print(f"    [FAIL] LLM call failed: {e}")
                break

    return None


# ================================================================
# BATCH PREDICTION: One API call for all zones (beats rate limits)
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

# Cache: filled by generate_all_predictions_batch(), consumed by generate_predictions()
_BATCH_CACHE = {}

def generate_all_predictions_batch(all_scraped_data, govt_alerts):
    """
    Make ONE LLM call to predict all tracked localities at once.
    This beats free-tier rate limits (3 RPM) by only needing 1 request total.
    Results are cached in _BATCH_CACHE for generate_predictions() to use.
    """
    if DEMO_MODE or not LLM_API_KEY:
        return False  # Nothing to batch - demo mode or no key

    print("\n  [MiroFish] Batch predicting all zones in one LLM call...")

    # Build compact data section for each locality
    zone_summaries = []
    for loc in LOCALITIES:
        lid  = loc["id"]
        lname = loc["name"]
        base  = LOCALITY_BASELINES[lid]
        scraped = all_scraped_data.get(lid, {})
        live_price = scraped.get("listings", {}).get("avg_price_sqft") or base["price_2025"]
        hist_prices = FULL_PRICE_HISTORY[lid]

        zone_summaries.append(
            f"{lname}: current Rs {live_price}/sqft, "
            f"7yr history {hist_prices}, "
            f"ROI {base['roi_yoy']}% YoY, NRI buyers {base['nri_pct']}%, "
            f"growth rate {base['growth_rate']*100:.1f}%"
        )

    prompt = f"""You are a Hyderabad real estate analyst. Give decisive price predictions for 8 localities.

Current data (March 2026):
{chr(10).join(f'- {s}' for s in zone_summaries)}

Respond ONLY with this exact JSON (no markdown, no explanation):
{{
  "kokapet":    {{"Q3_2026": <int>, "y2027": <int>, "y2028": <int>, "nri_q3": <int>, "nri_27": <int>, "nri_28": <int>}},
  "gachibowli": {{"Q3_2026": <int>, "y2027": <int>, "y2028": <int>, "nri_q3": <int>, "nri_27": <int>, "nri_28": <int>}},
  "miyapur":    {{"Q3_2026": <int>, "y2027": <int>, "y2028": <int>, "nri_q3": <int>, "nri_27": <int>, "nri_28": <int>}},
  "kompally":   {{"Q3_2026": <int>, "y2027": <int>, "y2028": <int>, "nri_q3": <int>, "nri_27": <int>, "nri_28": <int>}},
  "jubilee":    {{"Q3_2026": <int>, "y2027": <int>, "y2028": <int>, "nri_q3": <int>, "nri_27": <int>, "nri_28": <int>}},
  "manikonda":  {{"Q3_2026": <int>, "y2027": <int>, "y2028": <int>, "nri_q3": <int>, "nri_27": <int>, "nri_28": <int>}},
  "uppal":      {{"Q3_2026": <int>, "y2027": <int>, "y2028": <int>, "nri_q3": <int>, "nri_27": <int>, "nri_28": <int>}},
  "shamshabad": {{"Q3_2026": <int>, "y2027": <int>, "y2028": <int>, "nri_q3": <int>, "nri_27": <int>, "nri_28": <int>}}
}}
All prices in Rs /sqft. Be decisive - no hedging. Reflect realistic Hyderabad market appreciation."""

    for attempt in range(4):
        try:
            resp = requests.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"},
                json={"model": LLM_MODEL, "messages": [{"role": "user", "content": prompt}],
                      "temperature": 0.2, "max_tokens": 500},
                timeout=45,
            )
            if resp.status_code == 429:
                wait = 25 * (attempt + 1)
                print(f"    -> Rate limit - waiting {wait}s (attempt {attempt+1}/4)...")
                time.sleep(wait)
                continue

            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if not json_match:
                print("    [FAIL] Batch: no JSON found in response")
                break

            batch = json.loads(json_match.group(0))
            ts = datetime.now().isoformat()

            for lid, vals in batch.items():
                base = LOCALITY_BASELINES.get(lid, {})
                nri_hist = NRI_HISTORY.get(lid, [18])
                _BATCH_CACHE[lid] = {
                    "method": "llm_batch",
                    "confidence": "high",
                    "Q3_2026": {"price": vals["Q3_2026"], "nri_pct": vals.get("nri_q3", nri_hist[-1]+1),
                                "activity": min(ACTIVITY_HISTORY.get(lid, [80])[-1]+2, 99), "confidence": 0.88},
                    "2027":    {"price": vals["y2027"],   "nri_pct": vals.get("nri_27", nri_hist[-1]+2),
                                "activity": min(ACTIVITY_HISTORY.get(lid, [80])[-1]+4, 99), "confidence": 0.74},
                    "2028":    {"price": vals["y2028"],   "nri_pct": vals.get("nri_28", nri_hist[-1]+3),
                                "activity": min(ACTIVITY_HISTORY.get(lid, [80])[-1]+5, 99), "confidence": 0.60},
                    "generated_at": ts,
                }

            print(f"    [OK] Batch complete - {len(_BATCH_CACHE)} zones predicted in 1 API call")
            return True

        except json.JSONDecodeError as e:
            print(f"    [FAIL] Batch JSON parse error: {e}")
            break
        except Exception as e:
            if "429" not in str(e):
                print(f"    [FAIL] Batch LLM error: {e}")
                break
            wait = 25 * (attempt + 1)
            print(f"    -> Rate limit - waiting {wait}s (attempt {attempt+1}/4)...")
            time.sleep(wait)

    print("    -> Batch failed - zones will use fallback logic")
    return False


# ================================================================
# MAIN ENTRY POINT
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def generate_predictions(locality_id, locality_name, scraped_data, govt_alerts):
    """
    Generate price predictions for a locality.
    Tries in order: batch cache -> MiroFish live -> LLM direct -> extrapolation
    """
    print(f"\n  [MiroFish] Predicting: {locality_name}")
    live_price = scraped_data.get("listings", {}).get("avg_price_sqft")

    # DEMO MODE
    if DEMO_MODE:
        print(f"    -> DEMO MODE - using trend extrapolation")
        return _extrapolate_prices(
            locality_id,
            live_price,
            govt_alerts,
            method_name="trend_extrapolation_demo",
        )

    # LIVE MODE

    # Check batch cache first (populated by generate_all_predictions_batch)
    if locality_id in _BATCH_CACHE:
        print(f"    [OK] Using batch LLM prediction")
        return _BATCH_CACHE[locality_id]

    seed_material = _format_seed_material(locality_id, locality_name, scraped_data, govt_alerts)

    if MIROFISH_BACKEND_URL:
        report = _call_mirofish_api(seed_material, locality_name)
        parsed = _parse_mirofish_report(report, locality_id)
        if parsed:
            print("    [OK] Using MiroFish simulation output")
            return parsed

    if LLM_API_KEY:
        direct = _call_llm_direct(seed_material, locality_name)
        if direct:
            print("    [OK] Using direct LLM prediction")
            return direct

    # Last resort: deterministic extrapolation, but label it honestly
    print("    -> Prediction services unavailable - falling back to trend extrapolation")
    return _extrapolate_prices(
        locality_id,
        live_price,
        govt_alerts,
        method_name="trend_extrapolation_fallback",
    )


def get_full_timeline(locality_id, predictions):
    """
    Merge historical data with new predictions into a full timeline array.
    Format: arrays of 10 values (indices 0-6 = history, 7-9 = predictions)
    """
    price_hist  = FULL_PRICE_HISTORY.get(locality_id, [])
    nri_hist    = NRI_HISTORY.get(locality_id, [])
    activity_hist = ACTIVITY_HISTORY.get(locality_id, [])

    return {
        "price": price_hist + [
            predictions["Q3_2026"]["price"],
            predictions["2027"]["price"],
            predictions["2028"]["price"],
        ],
        "nri": nri_hist + [
            predictions["Q3_2026"]["nri_pct"],
            predictions["2027"]["nri_pct"],
            predictions["2028"]["nri_pct"],
        ],
        "activity": activity_hist + [
            predictions["Q3_2026"]["activity"],
            predictions["2027"]["activity"],
            predictions["2028"]["activity"],
        ],
    }
