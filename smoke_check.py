#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INDEX_HTML = ROOT / "index.html"
APP_JS = ROOT / "app.js"
STYLES = ROOT / "styles.css"
FAVICON = ROOT / "favicon.svg"
DATA_JSON = ROOT / "pipeline" / "output" / "data.json"


def fail(errors, message):
    errors.append(message)


def main():
    errors = []

    for path in [INDEX_HTML, APP_JS, STYLES, FAVICON]:
        if not path.exists():
            fail(errors, f"missing required file: {path.name}")

    if INDEX_HTML.exists():
        html = INDEX_HTML.read_text(encoding="utf-8")
        for token in [
            'id="map"',
            'id="zlist"',
            'id="live-badge"',
            'id="load-state"',
            'href="styles.css"',
            'src="app.js"',
            'href="favicon.svg"',
        ]:
            if token not in html:
                fail(errors, f"index.html missing `{token}`")

    if APP_JS.exists():
        js = APP_JS.read_text(encoding="utf-8")
        for token in [
            "function buildMap()",
            "function renderSB(",
            "function loadLiveData()",
            "function setLoadState(",
            "fetch('pipeline/output/data.json')",
        ]:
            if token not in js:
                fail(errors, f"app.js missing `{token}`")

    if DATA_JSON.exists():
        data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
        zones = data.get("zones", {})
        if len(zones) != 8:
            fail(errors, f"expected 8 zones in data.json, found {len(zones)}")
        metadata = data.get("metadata", {})
        if "pipeline_mode" not in metadata:
            fail(errors, "data.json metadata missing `pipeline_mode`")
    else:
        fail(errors, "pipeline/output/data.json is missing")

    if errors:
        print("SMOKE CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("SMOKE CHECK OK")
    print(f"- entry: {INDEX_HTML}")
    print(f"- assets: styles.css, app.js, favicon.svg")
    print(f"- data: {DATA_JSON}")


if __name__ == "__main__":
    main()
