# HydROI Data Pipeline Setup Guide

## What this pipeline does

Each run:
1. Scrapes RERA Telangana for project registrations
2. Scrapes 99acres and falls back when portal scraping is blocked
3. Monitors HMDA, TSIIC, Telangana Govt, and RERA news pages
4. Generates predictions using one of these paths:
   - `DEMO`: trend extrapolation only
   - `LIVE`: batch LLM, direct LLM, or MiroFish simulation
   - `FALLBACK`: deterministic extrapolation because live services were unavailable
5. Saves `output/data.json`, which `HydROI.html` loads automatically

## Step 1 - Install Python dependencies

Open a terminal in `pipeline/` and run:

```bash
pip install -r requirements.txt
```

That installs:
- `requests`
- `beautifulsoup4`

## Step 2 - Configure environment

Copy the example file and fill in what you need:

```bash
copy .env.example .env
```

Important variables:
- `LLM_API_KEY`: required for live LLM-backed predictions
- `LLM_BASE_URL`: defaults to OpenAI-compatible API format
- `LLM_MODEL`: defaults to `gpt-4o-mini`
- `MIROFISH_BACKEND_URL`: optional, used only if you are running MiroFish
- `DEMO_MODE`: optional override; if omitted, the pipeline automatically uses demo mode when no `LLM_API_KEY` is present

## Step 3 - Run in Demo Mode

If `LLM_API_KEY` is empty, the pipeline automatically runs in demo mode.

Run:

```bash
python pipeline.py
```

Expected result:
- `output/data.json` is generated
- HydROI shows a yellow `DEMO DATA` badge

## Step 4 - Run with Live Predictions

To enable live prediction paths:
1. Set `LLM_API_KEY` in `.env`
2. Optionally set `MIROFISH_BACKEND_URL` if you have MiroFish running
3. Run:

```bash
python pipeline.py
```

Prediction priority:
1. Batch LLM prediction
2. MiroFish simulation
3. Direct LLM call
4. Trend extrapolation fallback

Expected badges in HydROI:
- Green `LIVE DATA`: at least one live prediction path succeeded
- Orange `FALLBACK DATA`: scraping worked, but prediction services fell back
- Yellow `DEMO DATA`: demo-only mode

## Step 5 - Schedule or force runs

Run every 24 hours:

```bash
python pipeline.py --schedule
```

Force a fresh scrape:

```bash
python pipeline.py --force
```

## File structure

```text
pipeline/
|-- .env.example
|-- config.py
|-- mirofish.py
|-- pipeline.py
|-- requirements.txt
|-- scrapers.py
|-- SETUP.md
`-- output/
    |-- data.json
    `-- cache/
```

## Notes

- `HydROI.html` still contains hardcoded seed content for some zones; live data merges into that baseline.
- The pipeline currently covers 5 localities, while the UI contains more hardcoded zones.
- `output/data.json` metadata now reports the actual methods used for the run.

## Troubleshooting

**No `data.json` yet**
- Run `python pipeline.py` from the `pipeline/` folder first.

**Badge shows `FALLBACK DATA`**
- Scraping worked, but no live prediction service completed successfully.
- Check `LLM_API_KEY`, network access, and MiroFish availability.

**MiroFish is not running**
- The pipeline can still use direct LLM or fallback extrapolation.

**Portal scraping is thin or stale**
- Some property sites block scraping.
- The pipeline will reuse cache or baseline data when needed.
