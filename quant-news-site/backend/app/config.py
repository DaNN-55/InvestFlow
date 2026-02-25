import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=False)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
NEWS_JSON_PATH = DATA_DIR / "news.json"
SOURCES_LOCAL_JSON_PATH = DATA_DIR / "sources.local.json"

LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "").strip() or "https://api.openai.com/v1"
LLM_MODEL = os.getenv("LLM_MODEL", "").strip()
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "30"))

FETCH_HTTP_TIMEOUT_SECONDS = float(os.getenv("FETCH_HTTP_TIMEOUT_SECONDS", "12"))
FETCH_ARTICLE_BODY = os.getenv("FETCH_ARTICLE_BODY", "1").strip() not in {"0", "false", "False"}
FETCH_MAX_ITEMS_PER_SOURCE = int(os.getenv("FETCH_MAX_ITEMS_PER_SOURCE", "10"))
FETCH_MAX_TOTAL_ITEMS_PER_RUN = int(os.getenv("FETCH_MAX_TOTAL_ITEMS_PER_RUN", "50"))
SUMMARIZE_MAX_ITEMS_PER_RUN = int(os.getenv("SUMMARIZE_MAX_ITEMS_PER_RUN", "20"))
