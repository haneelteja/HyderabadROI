#!/usr/bin/env python3
# ================================================================
# HydROI Pipeline - Main Orchestrator
#
# Run this file to:
#   1. Scrape RERA Telangana + 99acres + govt news
#   2. Feed data into MiroFish (or demo extrapolation)
#   3. Output data.json -> HydROI.html reads this automatically
#
# Usage:
#   python pipeline.py              -> run once
#   python pipeline.py --schedule   -> run every 24 hours (leave terminal open)
#   python pipeline.py --force      -> ignore cache, force fresh scrape
# ================================================================

import json
import os
import sys
import time
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from config import LOCALITIES, OUTPUT_JSON_PATH, DEMO_MODE
from scrapers import run_all_scrapers
from mirofish import generate_predictions, generate_all_predictions_batch, get_full_timeline, LOCALITY_BASELINES

TEXT_FIXUPS = {
    "Ã¢â‚¬â€": "-",
    "Ã¢â‚¬â€œ": "-",
    "Ã¢â€ â€™": "->",
    "Ã¢â€šÂ¹": "Rs ",
    "Ã‚Â·": "Â·",
    "Ã¢â‚¬â„¢": "'",
    "Ã¢â‚¬Å“": '"',
    "Ã¢â‚¬Â": '"',
    "Ã¢â‚¬Ëœ": "'",
    "Ã¢â‚¬Â¦": "...",
    "Ãƒâ€”": "x",
}


def _normalize_text(value):
    if isinstance(value, str):
        for bad, good in TEXT_FIXUPS.items():
            value = value.replace(bad, good)
        return value
    if isinstance(value, list):
        return [_normalize_text(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize_text(item) for key, item in value.items()}
    return value

# â”€â”€ Zone metadata (static â€” doesn't change with scraping) â”€â”€â”€â”€â”€
ZONE_META = {
    "kokapet": {
        "name": "Kokapet", "rank": 1, "lat": 17.407, "lng": 78.330, "radius": 2200,
        "type": "luxury", "segment": "Luxury Â· HNI Â· NRI", "color": "#ff3a00",
        "priceRange": "â‚¹1.2 Cr â€“ â‚¹8 Cr",
        "verdict": "The single best HNI & NRI investment in Hyderabad right now â€” no debate.",
        "summary": "Kokapet sits immediately adjacent to the Financial District, where Goldman Sachs, Microsoft, Amazon and Google maintain their largest India campuses. This creates a permanently captive luxury rental and resale market. NRI buyers account for 38% of all purchases â€” the highest in the city.",
        "pros": [
            "Goldman Sachs, Microsoft, Amazon within 2 km â€” corporate rental demand is unmatched anywhere in Hyderabad",
            "38% of buyers are NRI â€” highest in city â€” guarantees robust resale demand at all times",
            "HMDA-approved, zero-encumbrance titles â€” no legal risk, no litigation history"
        ],
        "cons": [
            "Minimum entry ticket is â‚¹1.2 Cr for 2BHK â€” locks out sub-â‚¹50L budgets entirely",
            "Appreciation likely moderates to 18â€“22% YoY from 2026 as the zone reaches maturity",
            "Secondary road infrastructure in inner lanes still incomplete"
        ],
        "govtInit": [
            {"t": "IT Corridor Extension", "b": "1,200 additional acres notified adjacent to Financial District under HMDA Master Plan 2031 â€” brings 40,000+ new IT jobs within 3 km"},
            {"t": "ORR Phase-2 Dedicated Exit Ramp", "b": "Dedicated ORR exit ramp for Kokapet under construction â€” completion Q3 2026, cuts airport commute by 12 minutes"},
            {"t": "HMWSSB Water Grid Phase-2", "b": "Dedicated drinking water pipeline for Kokapetâ€“Narsingi belt â€” â‚¹440 Cr project approved"}
        ],
    },
    "gachibowli": {
        "name": "Gachibowli", "rank": 2, "lat": 17.440, "lng": 78.349, "radius": 2000,
        "type": "luxury", "segment": "IT Professionals Â· NRI Â· Rental", "color": "#ff8c00",
        "priceRange": "â‚¹1.5 Cr â€“ â‚¹12 Cr",
        "verdict": "The safest, most liquid premium market in Hyderabad â€” never had a down quarter since 2016.",
        "summary": "Gachibowli is the established IT hub and the most liquid premium zone in the city. Net rental yield is 4.2% â€” highest in Hyderabad. It has never recorded a down quarter in sales since 2016.",
        "pros": [
            "4.2% net rental yield â€” highest in Hyderabad â€” generates immediate income from purchase day",
            "Zero down quarters in sales since 2016 â€” most liquid, easiest exit of all premium zones",
            "International schools, hospitals, malls within 3 km â€” highest end-use demand"
        ],
        "cons": [
            "Highest average price at â‚¹9,200/sqft â€” â‚¹1.5 Cr floor makes it the most expensive entry",
            "Peak appreciation cycle is behind it â€” upside now 22% vs 35% three years ago",
            "HITEC City main corridor traffic congestion is a permanent structural negative"
        ],
        "govtInit": [
            {"t": "Metro Rail Phase-2 Station", "b": "Gachibowli metro station approved and funded â€” construction begins Q2 2026, operational target 2029"},
            {"t": "HITECH City Expansion â€” 800 Acres", "b": "New 800-acre IT park notified adjacent to Gachibowli â€” 50,000 additional jobs projected"},
            {"t": "Biodiversity Junction Flyover", "b": "TS-iPass approved flyover â€” addresses the single biggest infrastructure complaint, completion Dec 2026"}
        ],
    },
    "miyapur": {
        "name": "Miyapur", "rank": 3, "lat": 17.498, "lng": 78.340, "radius": 2500,
        "type": "mid", "segment": "Mid-range Â· Metro-linked Â· Rental", "color": "#ffd700",
        "priceRange": "â‚¹55 L â€“ â‚¹2.5 Cr",
        "verdict": "#1 in sales volume citywide â€” maximum liquidity, lowest resale risk of any zone.",
        "summary": "Miyapur leads all Hyderabad localities in quarterly sales at 220 units â€” meaning you can always exit when needed. Metro terminus connectivity gives it a permanent commute advantage no competitor can replicate.",
        "pros": [
            "220 units/quarter â€” highest sales velocity in city â€” easiest exit, minimum holding risk",
            "Metro terminus station gives a permanent, unbeatable commute advantage over all competing zones",
            "Entry from â‚¹55 L â€” widest NRI buyer pool, largest resale market"
        ],
        "cons": [
            "Appreciation ceiling is lower at 19% YoY vs Kokapet or Kompally",
            "Older building stock is mixed quality â€” individual project due diligence is mandatory",
            "2BHK segment showing saturation signals â€” 3BHK and above is the play going forward"
        ],
        "govtInit": [
            {"t": "Metro Extension to Patancheru", "b": "Metro line extended from Miyapur terminus â€” land acquisition 80% complete, opens 15km of new real estate corridor"},
            {"t": "HMDA 3x FAR Designation", "b": "Miyapurâ€“Bachupally belt designated high-density residential â€” 3x Floor Area Ratio unlocks significant vertical development"},
            {"t": "TSRTC Multimodal Hub", "b": "â‚¹85 Cr multimodal transport hub approved adjacent to Miyapur metro station"}
        ],
    },
    "kompally": {
        "name": "Kompally", "rank": 4, "lat": 17.562, "lng": 78.476, "radius": 2800,
        "type": "emerging", "segment": "Emerging Â· ORR Belt Â· Land Investment", "color": "#00ced1",
        "priceRange": "â‚¹40 L â€“ â‚¹1.8 Cr",
        "verdict": "52% 3-year ROI â€” fastest appreciating zone in North Hyderabad â€” still undervalued today.",
        "summary": "Kompally has delivered the highest raw 3-year ROI (52%) of any tracked zone in Hyderabad. Land plots here at â‚¹40â€“60K per sq yard are the last affordable large-land opportunity within ORR limits.",
        "pros": [
            "52% 3-year ROI â€” best raw appreciation in the entire city across the measurement period",
            "Land still available at â‚¹40â€“60K/sq yard â€” last affordable ORR-adjacent land in Hyderabad",
            "TCS, Infosys, Wipro all within 15 km â€” employee housing demand is building fast"
        ],
        "cons": [
            "Social infra â€” malls, international schools, specialty hospitals â€” is 3â€“5 years away from maturity",
            "Illiquidity risk: takes 60â€“90 days longer to sell vs HITEC City belt",
            "Some announced government projects are behind original schedule â€” execution risk is real"
        ],
        "govtInit": [
            {"t": "Medchal Municipal Corporation Upgrade", "b": "Kompallyâ€“Medchal elevated to Medchalâ€“Malkajgiri Municipal Corporation â€” GHMC-level development spending now applies"},
            {"t": "400-Acre IT SEZ Notification", "b": "Telangana IT Dept notified 400-acre SEZ in Kompally â€” 25,000 direct jobs projected"},
            {"t": "NH-44 6-Lane Expansion", "b": "6-lane widening of NH-44 through Kompally corridor â€” land values expected to jump 15â€“20% on completion in 2027"}
        ],
    },
    "jubilee": {
        "name": "Jubilee Hills", "rank": 5, "lat": 17.432, "lng": 78.408, "radius": 1600,
        "type": "luxury", "segment": "Ultra-premium Â· Legacy Â· HNI", "color": "#e040fb",
        "priceRange": "â‚¹3 Cr - â‚¹50 Cr+",
        "verdict": "Hyderabad's prestige address - strongest for capital preservation, not growth-chasing.",
        "summary": "Jubilee Hills remains the city's prestige market. Supply is constrained and buyer demand is reputation-driven, which protects value better than it drives breakout growth.",
        "pros": [
            "Constrained supply supports a durable premium floor",
            "Prestige-driven HNI demand remains structurally strong",
            "Legacy address with resilient brand value"
        ],
        "cons": [
            "Appreciation is slower than emerging corridors",
            "Entry ticket is among the highest in the city",
            "Much of the stock is older and highly project-dependent"
        ],
        "govtInit": [
            {"t": "Road No. 36 Widening", "b": "GHMC road works target one of the locality's chronic traffic pressure points"},
            {"t": "Heritage Residential Controls", "b": "Planning controls help preserve low-supply premium character"},
            {"t": "Underground Cabling", "b": "Infrastructure upgrades improve reliability and streetscape quality"}
        ],
    },
    "manikonda": {
        "name": "Manikonda", "rank": 6, "lat": 17.394, "lng": 78.385, "radius": 1900,
        "type": "mid", "segment": "Affordable premium Â· NRI rental", "color": "#26c6da",
        "priceRange": "â‚¹50 L - â‚¹2.2 Cr",
        "verdict": "Best value zone in the western IT belt for buyers who want rentability without Kokapet pricing.",
        "summary": "Manikonda captures western IT-belt demand at a lower entry point than neighboring premium zones. That combination keeps it attractive for value-focused end users and investors.",
        "pros": [
            "Discounted entry versus adjacent IT-belt premium zones",
            "Healthy rental and NRI interest",
            "Balanced appreciation and affordability profile"
        ],
        "cons": [
            "Drainage and civic infrastructure still lag development",
            "Main-road congestion is a persistent issue",
            "Service consistency varies across jurisdiction boundaries"
        ],
        "govtInit": [
            {"t": "Manikonda-Rajendranagar Flyover", "b": "Approved corridor aimed at reducing travel times toward the ORR"},
            {"t": "Drainage Master Plan", "b": "Storm-water upgrades target one of the locality's main complaints"},
            {"t": "Layout Regularisation", "b": "Planning cleanup improves title confidence for more parcels"}
        ],
    },
    "uppal": {
        "name": "Uppal / Nacharam", "rank": 7, "lat": 17.405, "lng": 78.559, "radius": 2200,
        "type": "emerging", "segment": "East corridor Â· Affordable Â· IT-linked", "color": "#66bb6a",
        "priceRange": "â‚¹35 L - â‚¹1.5 Cr",
        "verdict": "Compelling east-side affordability play, but weaker premium resale demand than west Hyderabad.",
        "summary": "Uppal and Nacharam benefit from lower entry prices, metro connectivity, and east-corridor employment growth. The upside case is affordability plus transit, not premium scarcity.",
        "pros": [
            "Lower entry price than most metro-connected alternatives",
            "Transit support and east-corridor job growth",
            "Wide buyer funnel for budget-conscious households"
        ],
        "cons": [
            "Premium NRI resale depth remains limited",
            "Social infrastructure trails west Hyderabad",
            "Financial District commutes are still long"
        ],
        "govtInit": [
            {"t": "Knowledge City Expansion", "b": "Large employment plans support future housing demand in the east corridor"},
            {"t": "Metro Extensions", "b": "Transit improvements strengthen accessibility over time"},
            {"t": "Industrial SEZ Upgrades", "b": "Employment anchors diversify the area's demand base"}
        ],
    },
    "shamshabad": {
        "name": "Shamshabad / Pharma City", "rank": 8, "lat": 17.240, "lng": 78.429, "radius": 3500,
        "type": "commercial", "segment": "Industrial Â· Long-term Â· Land", "color": "#9b59b6",
        "priceRange": "â‚¹30 L â€“ â‚¹2 Cr",
        "verdict": "India's largest pharma cluster. A 10-year land play â€” investors buying today will see 3â€“5x by 2035.",
        "summary": "Shamshabad is home to a 32,000-acre NIMZ â€” Pharma City â€” the largest in India. Land within 5 km of the Pharma City gate today is positioned for a 3â€“5x return by 2035.",
        "pros": [
            "Pharma City NIMZ â€” 32,000 acres, â‚¹1.12 lakh Cr committed investment â€” government-mandated anchor",
            "Airport adjacency: 8 minutes from RGIA â€” no other zone in Hyderabad offers this at this price",
            "Lowest entry price at â‚¹3,200/sqft for a future-premium zone â€” maximum upside per rupee invested"
        ],
        "cons": [
            "Long gestation period: 8â€“12 year play â€” not suitable for investors with a sub-5-year exit horizon",
            "Pharma City Phase-1 execution is 2 years behind the original schedule â€” bureaucratic risk",
            "Very low current liquidity â€” a small buyer pool today means a difficult near-term exit if needed"
        ],
        "govtInit": [
            {"t": "Pharma City NIMZ â€” â‚¹1.12 Lakh Cr", "b": "32,000-acre NIMZ â€” 200+ pharma companies onboarded, 1.5 lakh direct jobs projected at full build-out"},
            {"t": "MMTS Rail Extension", "b": "Multi-Modal Transport System extended to Shamshabad â€” approved in Union Budget 2025 at â‚¹620 Cr"},
            {"t": "India's 2nd Largest Logistics Park", "b": "8,000-acre integrated logistics park approved adjacent to RGIA â€” 60,000 direct jobs, captive residential demand"}
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


def _source_status(source_name, payload, fallback_sources=None):
    fallback_sources = fallback_sources or set()
    payload = payload or {}
    source = payload.get("source", source_name)
    scraped_at = payload.get("scraped_at")
    status = "live"

    if source in fallback_sources or source in {"baseline", "baseline_estimate"}:
        status = "fallback"
    elif source_name == "rera.telangana.gov.in" and (
        payload.get("total_projects") in ("N/A", None, 0)
        and not payload.get("projects")
    ):
        status = "fallback"

    return {
        "source": source,
        "status": status,
        "scraped_at": scraped_at,
    }


def _build_scrape_summary(scraped):
    localities = scraped.get("localities", {})
    city_stats = _source_status("city_stats", scraped.get("city_stats", {}), {"baseline"})
    govt_alerts = scraped.get("govt_alerts", [])

    summary = {
        "city_stats": city_stats,
        "govt_alerts": {
            "count": len(govt_alerts),
            "sources": sorted({alert.get("source", "unknown") for alert in govt_alerts}),
        },
        "localities": {},
        "totals": {
            "listings_live": 0,
            "listings_fallback": 0,
            "rera_live": 0,
            "rera_fallback": 0,
        },
    }

    for locality_id, loc_data in localities.items():
        listings_status = _source_status("listings", loc_data.get("listings", {}), {"baseline_estimate"})
        rera_status = _source_status("rera.telangana.gov.in", loc_data.get("rera", {}))
        summary["localities"][locality_id] = {
            "listings": listings_status,
            "rera": rera_status,
        }
        summary["totals"][f"listings_{listings_status['status']}"] += 1
        summary["totals"][f"rera_{rera_status['status']}"] += 1

    return summary


def build_output(scraped, predictions_map, govt_alerts):
    """Assemble the final data.json that HydROI.html will read."""

    city_raw = scraped.get("city_stats", {})
    method_summary = _summarize_prediction_methods(predictions_map)
    scrape_summary = _build_scrape_summary(scraped)

    output = {
        "metadata": {
            "last_updated":    datetime.now().isoformat(),
            "pipeline_mode":   method_summary["pipeline_mode"],
            "prediction_engine": method_summary["prediction_engine"],
            "actual_prediction_methods": method_summary["actual_prediction_methods"],
            "data_sources":    ["rera.telangana.gov.in", "99acres.com", "magicbricks.com"],
            "next_refresh":    "Run python pipeline.py to refresh",
            "scrape_summary":  scrape_summary,
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
            "kompally": 628, "jubilee": 98, "manikonda": 410,
            "uppal": 520, "shamshabad": 410
        }.get(lid, 200)

        tl = get_full_timeline(lid, preds)

        # Recalculate YoY ROI from live price vs 1 year ago (index 5 = 2024)
        from mirofish import FULL_PRICE_HISTORY
        price_2024 = FULL_PRICE_HISTORY.get(lid, [0]*7)[5]
        roi_yoy = round((live_price - price_2024) / price_2024 * 100, 1) if price_2024 else base["roi_yoy"]

        # Locality alerts
        loc_alerts = [a for a in govt_alerts if lid in a.get("localities_affected", [])]
        listings_status = scrape_summary["localities"].get(lid, {}).get("listings", {})
        rera_status = scrape_summary["localities"].get(lid, {}).get("rera", {})

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

            # Provenance and fallback reporting
            "dataQuality": {
                "listings": listings_status,
                "rera": rera_status,
                "govt_alert_count": len(loc_alerts),
                "prediction_method": preds.get("method", ""),
            },

            # Locality-specific govt alerts
            "govtAlerts": loc_alerts[:5],
        }

    return _normalize_text(output)


def run_pipeline(force_scrape=False):
    print("\n" + "="*60)
    print("  HydROI DATA PIPELINE")
    print(f"  Mode requested: {'DEMO' if DEMO_MODE else 'LIVE / AUTO'}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # â”€â”€ Step 1: Scrape â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print("\n[1/3] SCRAPING DATA SOURCES...")
    scraped = run_all_scrapers()
    govt_alerts = scraped.get("govt_alerts", [])

    # â”€â”€ Step 2: Generate predictions â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
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

    # â”€â”€ Step 3: Assemble & save output â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print("\n[3/3] ASSEMBLING OUTPUT...")
    output = build_output(scraped, predictions_map, govt_alerts)

    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] data.json saved -> {os.path.abspath(OUTPUT_JSON_PATH)}")
    print(f"  Zones:       {len(output['zones'])} localities processed")
    print(f"  Govt alerts: {len(govt_alerts)} items")
    print(f"  Mode:        {output['metadata']['pipeline_mode']}")
    print(f"  Methods:     {', '.join(output['metadata']['actual_prediction_methods'])}")
    print("\n  Open HydROI.html in your browser - it will load this data automatically.")
    print("="*60)

    return output


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# ENTRY POINT
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if __name__ == "__main__":
    args = sys.argv[1:]
    force = "--force" in args
    schedule = "--schedule" in args

    if schedule:
        interval_hours = 24
        print(f"[SCHEDULE] running every {interval_hours}h. Press Ctrl+C to stop.\n")
        while True:
            run_pipeline(force_scrape=force)
            print(f"\n  Next run in {interval_hours} hours...")
            time.sleep(interval_hours * 3600)
    else:
        run_pipeline(force_scrape=force)
