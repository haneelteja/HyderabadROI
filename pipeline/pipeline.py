#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
# HydROI Pipeline — Main Orchestrator
#
# Run this file to:
#   1. Scrape RERA Telangana + 99acres + govt news
#   2. Feed data into MiroFish (or demo extrapolation)
#   3. Output data.json → HydROI.html reads this automatically
#
# Usage:
#   python pipeline.py              ← run once
#   python pipeline.py --schedule   ← run every 24 hours (leave terminal open)
#   python pipeline.py --force      ← ignore cache, force fresh scrape
# ═══════════════════════════════════════════════════════════════

import json
import os
import sys
import time
from datetime import datetime

from config import LOCALITIES, OUTPUT_JSON_PATH, DEMO_MODE
from scrapers import run_all_scrapers
from mirofish import generate_predictions, generate_all_predictions_batch, get_full_timeline, LOCALITY_BASELINES

# ── Zone metadata (static — doesn't change with scraping) ─────
ZONE_META = {
    "kokapet": {
        "name": "Kokapet", "rank": 1, "lat": 17.407, "lng": 78.330, "radius": 2200,
        "type": "luxury", "segment": "Luxury · HNI · NRI", "color": "#ff3a00",
        "priceRange": "₹1.2 Cr – ₹8 Cr",
        "verdict": "The single best HNI & NRI investment in Hyderabad right now — no debate.",
        "summary": "Kokapet sits immediately adjacent to the Financial District, where Goldman Sachs, Microsoft, Amazon and Google maintain their largest India campuses. This creates a permanently captive luxury rental and resale market. NRI buyers account for 38% of all purchases — the highest in the city.",
        "pros": [
            "Goldman Sachs, Microsoft, Amazon within 2 km — corporate rental demand is unmatched anywhere in Hyderabad",
            "38% of buyers are NRI — highest in city — guarantees robust resale demand at all times",
            "HMDA-approved, zero-encumbrance titles — no legal risk, no litigation history"
        ],
        "cons": [
            "Minimum entry ticket is ₹1.2 Cr for 2BHK — locks out sub-₹50L budgets entirely",
            "Appreciation likely moderates to 18–22% YoY from 2026 as the zone reaches maturity",
            "Secondary road infrastructure in inner lanes still incomplete"
        ],
        "govtInit": [
            {"t": "IT Corridor Extension", "b": "1,200 additional acres notified adjacent to Financial District under HMDA Master Plan 2031 — brings 40,000+ new IT jobs within 3 km"},
            {"t": "ORR Phase-2 Dedicated Exit Ramp", "b": "Dedicated ORR exit ramp for Kokapet under construction — completion Q3 2026, cuts airport commute by 12 minutes"},
            {"t": "HMWSSB Water Grid Phase-2", "b": "Dedicated drinking water pipeline for Kokapet–Narsingi belt — ₹440 Cr project approved"}
        ],
    },
    "gachibowli": {
        "name": "Gachibowli", "rank": 2, "lat": 17.440, "lng": 78.349, "radius": 2000,
        "type": "luxury", "segment": "IT Professionals · NRI · Rental", "color": "#ff8c00",
        "priceRange": "₹1.5 Cr – ₹12 Cr",
        "verdict": "The safest, most liquid premium market in Hyderabad — never had a down quarter since 2016.",
        "summary": "Gachibowli is the established IT hub and the most liquid premium zone in the city. Net rental yield is 4.2% — highest in Hyderabad. It has never recorded a down quarter in sales since 2016.",
        "pros": [
            "4.2% net rental yield — highest in Hyderabad — generates immediate income from purchase day",
            "Zero down quarters in sales since 2016 — most liquid, easiest exit of all premium zones",
            "International schools, hospitals, malls within 3 km — highest end-use demand"
        ],
        "cons": [
            "Highest average price at ₹9,200/sqft — ₹1.5 Cr floor makes it the most expensive entry",
            "Peak appreciation cycle is behind it — upside now 22% vs 35% three years ago",
            "HITEC City main corridor traffic congestion is a permanent structural negative"
        ],
        "govtInit": [
            {"t": "Metro Rail Phase-2 Station", "b": "Gachibowli metro station approved and funded — construction begins Q2 2026, operational target 2029"},
            {"t": "HITECH City Expansion — 800 Acres", "b": "New 800-acre IT park notified adjacent to Gachibowli — 50,000 additional jobs projected"},
            {"t": "Biodiversity Junction Flyover", "b": "TS-iPass approved flyover — addresses the single biggest infrastructure complaint, completion Dec 2026"}
        ],
    },
    "miyapur": {
        "name": "Miyapur", "rank": 3, "lat": 17.498, "lng": 78.340, "radius": 2500,
        "type": "mid", "segment": "Mid-range · Metro-linked · Rental", "color": "#ffd700",
        "priceRange": "₹55 L – ₹2.5 Cr",
        "verdict": "#1 in sales volume citywide — maximum liquidity, lowest resale risk of any zone.",
        "summary": "Miyapur leads all Hyderabad localities in quarterly sales at 220 units — meaning you can always exit when needed. Metro terminus connectivity gives it a permanent commute advantage no competitor can replicate.",
        "pros": [
            "220 units/quarter — highest sales velocity in city — easiest exit, minimum holding risk",
            "Metro terminus station gives a permanent, unbeatable commute advantage over all competing zones",
            "Entry from ₹55 L — widest NRI buyer pool, largest resale market"
        ],
        "cons": [
            "Appreciation ceiling is lower at 19% YoY vs Kokapet or Kompally",
            "Older building stock is mixed quality — individual project due diligence is mandatory",
            "2BHK segment showing saturation signals — 3BHK and above is the play going forward"
        ],
        "govtInit": [
            {"t": "Metro Extension to Patancheru", "b": "Metro line extended from Miyapur terminus — land acquisition 80% complete, opens 15km of new real estate corridor"},
            {"t": "HMDA 3x FAR Designation", "b": "Miyapur–Bachupally belt designated high-density residential — 3x Floor Area Ratio unlocks significant vertical development"},
            {"t": "TSRTC Multimodal Hub", "b": "₹85 Cr multimodal transport hub approved adjacent to Miyapur metro station"}
        ],
    },
    "kompally": {
        "name": "Kompally", "rank": 4, "lat": 17.562, "lng": 78.476, "radius": 2800,
        "type": "emerging", "segment": "Emerging · ORR Belt · Land Investment", "color": "#00ced1",
        "priceRange": "₹40 L – ₹1.8 Cr",
        "verdict": "52% 3-year ROI — fastest appreciating zone in North Hyderabad — still undervalued today.",
        "summary": "Kompally has delivered the highest raw 3-year ROI (52%) of any tracked zone in Hyderabad. Land plots here at ₹40–60K per sq yard are the last affordable large-land opportunity within ORR limits.",
        "pros": [
            "52% 3-year ROI — best raw appreciation in the entire city across the measurement period",
            "Land still available at ₹40–60K/sq yard — last affordable ORR-adjacent land in Hyderabad",
            "TCS, Infosys, Wipro all within 15 km — employee housing demand is building fast"
        ],
        "cons": [
            "Social infra — malls, international schools, specialty hospitals — is 3–5 years away from maturity",
            "Illiquidity risk: takes 60–90 days longer to sell vs HITEC City belt",
            "Some announced government projects are behind original schedule — execution risk is real"
        ],
        "govtInit": [
            {"t": "Medchal Municipal Corporation Upgrade", "b": "Kompally–Medchal elevated to Medchal–Malkajgiri Municipal Corporation — GHMC-level development spending now applies"},
            {"t": "400-Acre IT SEZ Notification", "b": "Telangana IT Dept notified 400-acre SEZ in Kompally — 25,000 direct jobs projected"},
            {"t": "NH-44 6-Lane Expansion", "b": "6-lane widening of NH-44 through Kompally corridor — land values expected to jump 15–20% on completion in 2027"}
        ],
    },
    "shamshabad": {
        "name": "Shamshabad / Pharma City", "rank": 5, "lat": 17.240, "lng": 78.429, "radius": 3500,
        "type": "commercial", "segment": "Industrial · Long-term · Land", "color": "#9b59b6",
        "priceRange": "₹30 L – ₹2 Cr",
        "verdict": "India's largest pharma cluster. A 10-year land play — investors buying today will see 3–5x by 2035.",
        "summary": "Shamshabad is home to a 32,000-acre NIMZ — Pharma City — the largest in India. Land within 5 km of the Pharma City gate today is positioned for a 3–5x return by 2035.",
        "pros": [
            "Pharma City NIMZ — 32,000 acres, ₹1.12 lakh Cr committed investment — government-mandated anchor",
            "Airport adjacency: 8 minutes from RGIA — no other zone in Hyderabad offers this at this price",
            "Lowest entry price at ₹3,200/sqft for a future-premium zone — maximum upside per rupee invested"
        ],
        "cons": [
            "Long gestation period: 8–12 year play — not suitable for investors with a sub-5-year exit horizon",
            "Pharma City Phase-1 execution is 2 years behind the original schedule — bureaucratic risk",
            "Very low current liquidity — a small buyer pool today means a difficult near-term exit if needed"
        ],
        "govtInit": [
            {"t": "Pharma City NIMZ — ₹1.12 Lakh Cr", "b": "32,000-acre NIMZ — 200+ pharma companies onboarded, 1.5 lakh direct jobs projected at full build-out"},
            {"t": "MMTS Rail Extension", "b": "Multi-Modal Transport System extended to Shamshabad — approved in Union Budget 2025 at ₹620 Cr"},
            {"t": "India's 2nd Largest Logistics Park", "b": "8,000-acre integrated logistics park approved adjacent to RGIA — 60,000 direct jobs, captive residential demand"}
        ],
    },
}


def _summarize_prediction_methods(predictions_map):
    methods = sorted({pred.get("method", "unknown") for pred in predictions_map.values()})
    live_methods = {"llm_batch", "llm_direct", "mirofish_multi_agent_simulation"}

    if not methods:
        pipeline_mode = "DEMO"
        prediction_engine = "trend_extrapolation_demo"
    elif any(method in live_methods for method in methods):
        pipeline_mode = "LIVE"
        prediction_engine = methods[0] if len(methods) == 1 else "mixed"
    elif methods == ["trend_extrapolation_demo"]:
        pipeline_mode = "DEMO"
        prediction_engine = "trend_extrapolation_demo"
    else:
        pipeline_mode = "FALLBACK"
        prediction_engine = methods[0] if len(methods) == 1 else "mixed"

    return {
        "pipeline_mode": pipeline_mode,
        "prediction_engine": prediction_engine,
        "actual_prediction_methods": methods,
    }


def build_output(scraped, predictions_map, govt_alerts):
    """Assemble the final data.json that HydROI.html will read."""

    city_raw = scraped.get("city_stats", {})
    method_summary = _summarize_prediction_methods(predictions_map)

    output = {
        "metadata": {
            "last_updated":    datetime.now().isoformat(),
            "pipeline_mode":   method_summary["pipeline_mode"],
            "prediction_engine": method_summary["prediction_engine"],
            "actual_prediction_methods": method_summary["actual_prediction_methods"],
            "data_sources":    ["rera.telangana.gov.in", "99acres.com", "magicbricks.com"],
            "next_refresh":    "Run python pipeline.py to refresh",
        },
        "city_stats": {
            "avg_price_sqft":    city_raw.get("avg_price_sqft",   6840),
            "quarterly_sales":   city_raw.get("quarterly_sales",  4820),
            "nri_investment_cr": city_raw.get("nri_investment_cr", 2840),
            "active_projects":   city_raw.get("active_projects",  1240),
            "unsold_inventory":  city_raw.get("unsold_inventory", 28400),
        },
        "zones": {},
        "govt_alerts": govt_alerts[:20],  # top 20 most recent
    }

    for loc in LOCALITIES:
        lid   = loc["id"]
        meta  = ZONE_META[lid]
        base  = LOCALITY_BASELINES[lid]
        preds = predictions_map[lid]
        loc_scraped = scraped.get("localities", {}).get(lid, {})
        listings = loc_scraped.get("listings", {})
        rera     = loc_scraped.get("rera", {})

        # Use live price if available; fall back to baseline
        live_price = listings.get("avg_price_sqft") or base["price_2025"]
        live_listings = listings.get("listing_count") or {
            "kokapet": 342, "gachibowli": 218, "miyapur": 489,
            "kompally": 628, "shamshabad": 410
        }.get(lid, 200)

        tl = get_full_timeline(lid, preds)

        # Recalculate YoY ROI from live price vs 1 year ago (index 5 = 2024)
        from mirofish import FULL_PRICE_HISTORY
        price_2024 = FULL_PRICE_HISTORY.get(lid, [0]*7)[5]
        roi_yoy = round((live_price - price_2024) / price_2024 * 100, 1) if price_2024 else base["roi_yoy"]

        # Locality alerts
        loc_alerts = [a for a in govt_alerts if lid in a.get("localities_affected", [])]

        output["zones"][lid] = {
            # Identity & map
            "id":        lid,
            "name":      meta["name"],
            "rank":      meta["rank"],
            "lat":       meta["lat"],
            "lng":       meta["lng"],
            "radius":    meta["radius"],
            "type":      meta["type"],
            "segment":   meta["segment"],
            "color":     meta["color"],

            # Live market data
            "avgPrice":       live_price,
            "priceRange":     meta["priceRange"],
            "listings":       live_listings,
            "roiYoY":         roi_yoy,
            "roi3Y":          base["roi_3y"],
            "nriPct":         base["nri_pct"],
            "salesVel":       base["sales_vel"],

            # RERA data
            "rera": {
                "total_projects":           rera.get("total_projects", "N/A"),
                "recent_registrations_90d": rera.get("recent_registrations_90d", "N/A"),
            },

            # Narrative content
            "verdict":   meta["verdict"],
            "summary":   meta["summary"],
            "pros":      meta["pros"],
            "cons":      meta["cons"],
            "govtInit":  meta["govtInit"],

            # Full timeline (7 historical + 3 predicted)
            "tl": tl,

            # Prediction details
            "predictions": {
                "method":     preds.get("method", ""),
                "confidence": preds.get("confidence", ""),
                "Q3_2026":    preds.get("Q3_2026", {}),
                "2027":       preds.get("2027", {}),
                "2028":       preds.get("2028", {}),
            },

            # Locality-specific govt alerts
            "govtAlerts": loc_alerts[:5],
        }

    return output


def run_pipeline(force_scrape=False):
    print("\n" + "═"*60)
    print("  HydROI DATA PIPELINE")
    print(f"  Mode requested: {'DEMO' if DEMO_MODE else 'LIVE / AUTO'}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═"*60)

    # ── Step 1: Scrape ────────────────────────────────────────
    print("\n[1/3] SCRAPING DATA SOURCES...")
    scraped = run_all_scrapers()
    govt_alerts = scraped.get("govt_alerts", [])

    # ── Step 2: Generate predictions ─────────────────────────
    print("\n[2/3] GENERATING PREDICTIONS...")

    # Batch call: all 5 zones in ONE OpenAI request (avoids free-tier rate limits)
    all_loc_data = {loc["id"]: scraped.get("localities", {}).get(loc["id"], {})
                   for loc in LOCALITIES}
    batch_used = generate_all_predictions_batch(all_loc_data, govt_alerts)
    if batch_used:
        print("  Batch prediction path is available for this run.")

    predictions_map = {}
    for loc in LOCALITIES:
        lid = loc["id"]
        loc_data = all_loc_data[lid]
        predictions_map[lid] = generate_predictions(
            lid, loc["name"], loc_data, govt_alerts
        )

    # ── Step 3: Assemble & save output ───────────────────────
    print("\n[3/3] ASSEMBLING OUTPUT...")
    output = build_output(scraped, predictions_map, govt_alerts)

    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✓ data.json saved → {os.path.abspath(OUTPUT_JSON_PATH)}")
    print(f"  Zones:       {len(output['zones'])} localities processed")
    print(f"  Govt alerts: {len(govt_alerts)} items")
    print(f"  Mode:        {output['metadata']['pipeline_mode']}")
    print(f"  Methods:     {', '.join(output['metadata']['actual_prediction_methods'])}")
    print(f"\n  Open HydROI.html in your browser — it will load this data automatically.")
    print("═"*60)

    return output


# ───────────────────────────────────────────────────────────────
# ENTRY POINT
# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    force = "--force" in args
    schedule = "--schedule" in args

    if schedule:
        interval_hours = 24
        print(f"⏱  Scheduled mode: running every {interval_hours}h. Press Ctrl+C to stop.\n")
        while True:
            run_pipeline(force_scrape=force)
            print(f"\n  Next run in {interval_hours} hours...")
            time.sleep(interval_hours * 3600)
    else:
        run_pipeline(force_scrape=force)
