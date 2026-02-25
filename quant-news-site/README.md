# Quant News Site

Financial news aggregation + summary MVP for quant learning.

## Structure

- `backend/` - fetching, summarization, API
- `frontend/` - local preview dashboard page
- `data/` - local JSON data and source overrides
- `scripts/` - manual jobs (`fetch`, `summarize`)
- `docs/` - MVP notes and source config docs

## What works now (MVP)

- RSS fetch (default sources)
- Local JSON storage (`data/news.json`)
- Summary job (LLM if configured, fallback otherwise)
- FastAPI endpoints for news, jobs, sources, meta
- Local preview dashboard (`frontend/index.html`)

## Preview flow (quick)

1. Start backend API (`uvicorn app.main:app --reload`)
2. Open `frontend/index.html` in a browser (or serve `frontend/` with `python -m http.server`)
3. Click `Fetch`, then `Summarize`, then `Refresh`

## Custom sources (recommended)

1. Copy `data/sources.local.example.json` to `data/sources.local.json`
2. Replace example URLs with your real RSS sources
3. Set `"enabled": true`

