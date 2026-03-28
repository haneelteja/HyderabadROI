import os
from pathlib import Path


def _load_dotenv():
    """Load simple KEY=VALUE pairs from pipeline/.env if it exists."""
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()


# HydROI Pipeline Configuration
# Set values in environment variables or pipeline/.env before running pipeline.py.

# MiroFish / LLM
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
ZEP_API_KEY = os.getenv("ZEP_API_KEY", "")

# MiroFish Backend
MIROFISH_BACKEND_URL = os.getenv("MIROFISH_BACKEND_URL", "http://localhost:5001")

# Scraping
SCRAPE_DELAY_SECONDS = int(os.getenv("SCRAPE_DELAY_SECONDS", "2"))
SCRAPE_TIMEOUT = int(os.getenv("SCRAPE_TIMEOUT", "15"))
USE_CACHED_ON_FAILURE = os.getenv("USE_CACHED_ON_FAILURE", "true").lower() in ("1", "true", "yes", "on")

# Output
OUTPUT_JSON_PATH = os.getenv("OUTPUT_JSON_PATH", "output/data.json")

# Demo mode
_demo_override = os.getenv("DEMO_MODE")
if _demo_override is None:
    DEMO_MODE = not bool(LLM_API_KEY)
else:
    DEMO_MODE = _demo_override.lower() in ("1", "true", "yes", "on")

# Localities to track
LOCALITIES = [
    {"id": "kokapet", "name": "Kokapet", "rera_keyword": "Kokapet", "acres_keyword": "kokapet"},
    {"id": "gachibowli", "name": "Gachibowli", "rera_keyword": "Gachibowli", "acres_keyword": "gachibowli"},
    {"id": "miyapur", "name": "Miyapur", "rera_keyword": "Miyapur", "acres_keyword": "miyapur"},
    {"id": "kompally", "name": "Kompally", "rera_keyword": "Kompally", "acres_keyword": "kompally"},
    {"id": "jubilee", "name": "Jubilee Hills", "rera_keyword": "Jubilee Hills", "acres_keyword": "jubilee-hills"},
    {"id": "manikonda", "name": "Manikonda", "rera_keyword": "Manikonda", "acres_keyword": "manikonda"},
    {"id": "uppal", "name": "Uppal", "rera_keyword": "Uppal", "acres_keyword": "uppal"},
    {"id": "shamshabad", "name": "Shamshabad", "rera_keyword": "Shamshabad", "acres_keyword": "shamshabad"},
]

# Govt sources to monitor
GOVT_NEWS_SOURCES = [
    {"name": "HMDA", "url": "https://www.hmda.gov.in/whats-new", "type": "html"},
    {"name": "TSIIC", "url": "https://tsiic.telangana.gov.in/news", "type": "html"},
    {"name": "Telangana Govt", "url": "https://www.telangana.gov.in/news", "type": "html"},
    {"name": "RERA TG News", "url": "https://rera.telangana.gov.in/news", "type": "html"},
]

# Keyword triggers: if any of these appear in a govt article, flag it on the map
GOVT_ALERT_KEYWORDS = [
    "metro", "flyover", "IT park", "SEZ", "NIMZ", "HMDA", "ORR",
    "pharma city", "housing", "residential", "infrastructure", "approval",
    "layout", "notification", "master plan", "smart city", "TSRTC",
]
