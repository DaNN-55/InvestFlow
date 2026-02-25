# Backend (MVP)

FastAPI backend with:

- RSS fetching
- optional article-body extraction
- local JSON storage (`../data/news.json`)
- summary generation (LLM if configured, fallback otherwise)
- manual fetch/summarize job endpoints

## Setup

```powershell
cd quant-news-site/backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run API

```powershell
uvicorn app.main:app --reload
```

API base URL: `http://127.0.0.1:8000`

## Endpoints

- `GET /health`
- `GET /api/meta`
- `GET /api/sources`
- `GET /api/news`
- `GET /api/news/{id}`
- `POST /api/jobs/fetch`
- `POST /api/jobs/summarize`

## Manual scripts (from `quant-news-site/`)

```powershell
python .\scripts\fetch_news.py
python .\scripts\summarize_news.py
```

## LLM configuration (optional)

Create `quant-news-site/.env` (or set environment variables) and configure:

- `LLM_API_KEY`
- `LLM_MODEL`
- optional `LLM_BASE_URL`
- optional `LLM_TIMEOUT_SECONDS`

If not configured, the app uses a fallback summary generator.

## Source configuration (recommended)

Use `quant-news-site/data/sources.local.json` to override built-in sources.
Start from `quant-news-site/data/sources.local.example.json`.
