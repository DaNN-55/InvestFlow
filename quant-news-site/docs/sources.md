# Sources (MVP)

Prefer stable RSS/API sources first to reduce maintenance.

## Built-in defaults (`backend/app/sources.py`)

- `CNBC Top News` (enabled)
- `NYT Business` (enabled)
- `FTChinese Daily (example, verify/update)` (disabled by default)
- `Sina Finance Roll (example, verify/update)` (disabled by default)

## Recommended way to add your own sources (no code changes)

1. Copy `quant-news-site/data/sources.local.example.json`
2. Rename it to `quant-news-site/data/sources.local.json`
3. Replace the example Chinese URL with a real RSS/API endpoint
4. Set `"enabled": true`

The backend will use `sources.local.json` first when it exists.

## Source record format

- `name`
- `url`
- `language` (`zh` / `en` / `unknown`)
- `enabled` (`true` / `false`)
- `source_type` (`rss` for MVP)
- `fetch_body` (`true` to try article-page body extraction)
