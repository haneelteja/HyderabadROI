#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from config import OUTPUT_JSON_PATH


REQUIRED_ZONE_FIELDS = [
    "id",
    "name",
    "rank",
    "lat",
    "lng",
    "radius",
    "type",
    "segment",
    "color",
    "avgPrice",
    "priceRange",
    "listings",
    "roiYoY",
    "roi3Y",
    "nriPct",
    "salesVel",
    "verdict",
    "summary",
    "pros",
    "cons",
    "govtInit",
    "tl",
    "predictions",
    "dataQuality",
    "govtAlerts",
]

TIMELINE_KEYS = ["price", "nri", "activity"]
PREDICTION_KEYS = ["Q3_2026", "2027", "2028"]


def fail(errors, message):
    errors.append(message)


def validate_zone(zone_id, zone, errors):
    for field in REQUIRED_ZONE_FIELDS:
        if field not in zone:
            fail(errors, f"{zone_id}: missing field `{field}`")

    tl = zone.get("tl", {})
    for key in TIMELINE_KEYS:
        values = tl.get(key)
        if not isinstance(values, list):
            fail(errors, f"{zone_id}: timeline `{key}` is not a list")
            continue
        if len(values) != 10:
            fail(errors, f"{zone_id}: timeline `{key}` must have 10 values, found {len(values)}")
        if key == "price" and any((not isinstance(v, (int, float))) or v <= 0 for v in values):
            fail(errors, f"{zone_id}: timeline `{key}` contains non-positive values")

    predictions = zone.get("predictions", {})
    for key in PREDICTION_KEYS:
        if key not in predictions:
            fail(errors, f"{zone_id}: missing prediction period `{key}`")
            continue
        period = predictions[key]
        for metric in ["price", "nri_pct", "activity", "confidence"]:
            if metric not in period:
                fail(errors, f"{zone_id}: prediction `{key}` missing `{metric}`")

    numeric_fields = ["avgPrice", "listings", "roiYoY", "roi3Y", "nriPct", "salesVel"]
    for field in numeric_fields:
        value = zone.get(field)
        if not isinstance(value, (int, float)):
            fail(errors, f"{zone_id}: `{field}` must be numeric")
        elif field in ("avgPrice", "listings", "salesVel") and value < 0:
            fail(errors, f"{zone_id}: `{field}` must be non-negative")

    dq = zone.get("dataQuality", {})
    if not isinstance(dq, dict):
        fail(errors, f"{zone_id}: `dataQuality` must be an object")
    else:
        for channel in ["listings", "rera"]:
            source_info = dq.get(channel)
            if not isinstance(source_info, dict):
                fail(errors, f"{zone_id}: dataQuality `{channel}` must be an object")
                continue
            for key in ["source", "status", "scraped_at", "fetch_state", "fallback_reason"]:
                if key not in source_info:
                    fail(errors, f"{zone_id}: dataQuality `{channel}` missing `{key}`")


def main():
    output_path = Path(OUTPUT_JSON_PATH)
    if not output_path.exists():
        print(f"ERROR: output file not found: {output_path}")
        sys.exit(1)

    data = json.loads(output_path.read_text(encoding="utf-8"))
    errors = []

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        fail(errors, "metadata section is missing or invalid")
    else:
        for key in ["last_updated", "pipeline_mode", "prediction_engine", "actual_prediction_methods", "scrape_summary"]:
            if key not in metadata:
                fail(errors, f"metadata missing `{key}`")
        methods = metadata.get("actual_prediction_methods", [])
        if not isinstance(methods, list) or not methods:
            fail(errors, "metadata.actual_prediction_methods must be a non-empty list")
        scrape_summary = metadata.get("scrape_summary", {})
        if not isinstance(scrape_summary, dict):
            fail(errors, "metadata.scrape_summary must be an object")
        else:
            for key in ["city_stats", "govt_alerts", "localities", "totals"]:
                if key not in scrape_summary:
                    fail(errors, f"metadata.scrape_summary missing `{key}`")
            totals = scrape_summary.get("totals", {})
            for key in ["listings_live", "listings_cached", "listings_fallback", "rera_live", "rera_cached", "rera_fallback", "govt_live", "govt_cached", "govt_fallback"]:
                if key not in totals:
                    fail(errors, f"metadata.scrape_summary.totals missing `{key}`")
            govt_alerts = scrape_summary.get("govt_alerts", {})
            if "source_checks" not in govt_alerts or not isinstance(govt_alerts.get("source_checks"), list):
                fail(errors, "metadata.scrape_summary.govt_alerts missing `source_checks` list")

    zones = data.get("zones")
    if not isinstance(zones, dict) or not zones:
        fail(errors, "zones section is missing or empty")
    else:
        for zone_id, zone in zones.items():
            validate_zone(zone_id, zone, errors)

    city_stats = data.get("city_stats")
    if not isinstance(city_stats, dict):
        fail(errors, "city_stats section is missing or invalid")
    else:
        for key in ["avg_price_sqft", "quarterly_sales", "nri_investment_cr", "active_projects", "unsold_inventory"]:
            if key not in city_stats:
                fail(errors, f"city_stats missing `{key}`")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print(f"VALIDATION OK: {output_path}")
    print(f"- zones: {len(zones)}")
    print(f"- pipeline mode: {metadata['pipeline_mode']}")
    print(f"- methods: {', '.join(metadata['actual_prediction_methods'])}")


if __name__ == "__main__":
    main()
