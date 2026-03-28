# HyderabadROI

HyderabadROI is a lightweight real-estate intelligence prototype for Hyderabad.
It combines:

- a browser-based dashboard built with plain HTML, CSS, and JavaScript
- a Python pipeline that scrapes public sources and generates `pipeline/output/data.json`
- a live-data merge layer in the frontend that updates the dashboard when fresh pipeline output exists

## Current structure

```text
.
|-- HydROI.html
|-- styles.css
|-- app.js
|-- pipeline/
|   |-- .env.example
|   |-- config.py
|   |-- mirofish.py
|   |-- pipeline.py
|   |-- requirements.txt
|   |-- scrapers.py
|   `-- output/
|       `-- data.json
`-- README.md
```

## Frontend

The dashboard includes:

- ranked investment zones
- Leaflet map overlays
- detail panel per zone
- side-by-side comparison mode
- timeline slider for historical and projected values
- investment calculator

Entry files:

- [HydROI.html](C:\Users\Haneel Teja\Cursor Applications\Hyderabad ROI\HydROI.html)
- [styles.css](C:\Users\Haneel Teja\Cursor Applications\Hyderabad ROI\styles.css)
- [app.js](C:\Users\Haneel Teja\Cursor Applications\Hyderabad ROI\app.js)

## Pipeline

The Python pipeline:

1. scrapes public sources
2. applies prediction logic
3. writes `pipeline/output/data.json`

Main files:

- [config.py](C:\Users\Haneel Teja\Cursor Applications\Hyderabad ROI\pipeline\config.py)
- [scrapers.py](C:\Users\Haneel Teja\Cursor Applications\Hyderabad ROI\pipeline\scrapers.py)
- [mirofish.py](C:\Users\Haneel Teja\Cursor Applications\Hyderabad ROI\pipeline\mirofish.py)
- [pipeline.py](C:\Users\Haneel Teja\Cursor Applications\Hyderabad ROI\pipeline\pipeline.py)

## Setup

Install Python dependencies:

```bash
cd pipeline
pip install -r requirements.txt
```

Optional environment setup:

```bash
copy .env.example .env
```

Run the pipeline:

```bash
python pipeline.py
```

Then open [HydROI.html](C:\Users\Haneel Teja\Cursor Applications\Hyderabad ROI\HydROI.html) in a browser.

## Prediction modes

The pipeline reports the actual mode used in `data.json` metadata:

- `DEMO`: trend extrapolation only
- `LIVE`: at least one live prediction path succeeded
- `FALLBACK`: scraping ran, but prediction services fell back

## Current status

Implemented:

- frontend split into separate files
- 8-zone coverage in the pipeline
- env-based secret loading
- more truthful pipeline metadata
- compare-mode winner tags

Still rough:

- some narrative/source strings still deserve a fuller normalization pass
- public-site scraping is fragile and often falls back under restricted network conditions
- the product is still prototype-grade rather than production-ready

## Next likely improvements

1. finish source-text normalization across all remaining files
2. improve compare-mode summaries and styling
3. add output validation tests for `data.json`
4. harden scraper provenance and cache reporting
