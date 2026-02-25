import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .config import DATA_DIR, NEWS_JSON_PATH
from .models import NewsCreate, NewsItem
from .services.summarizer import fallback_summary


def _ensure_data_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not NEWS_JSON_PATH.exists():
        NEWS_JSON_PATH.write_text("[]", encoding="utf-8")


def _load_raw(path: Path = NEWS_JSON_PATH) -> list[dict]:
    _ensure_data_file()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = []
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def list_news_items() -> list[NewsItem]:
    items = [NewsItem.model_validate(item) for item in _load_raw()]
    return sorted(items, key=lambda x: (x.created_at, x.published_at), reverse=True)


def get_news_item(news_id: int) -> NewsItem | None:
    for item in list_news_items():
        if item.id == news_id:
            return item
    return None


def _next_id(items: list[NewsItem]) -> int:
    if not items:
        return 1
    return max(item.id for item in items) + 1


def upsert_news_items(candidates: list[NewsCreate]) -> tuple[int, int]:
    existing = list_news_items()
    by_url = {item.url: item for item in existing}

    added = 0
    updated = 0
    next_id = _next_id(existing)

    for candidate in candidates:
        if candidate.url in by_url:
            current = by_url[candidate.url]
            changed = False
            if not current.summary_cn and candidate.summary_cn:
                current.summary_cn = candidate.summary_cn
                changed = True
            if current.title != candidate.title and candidate.title:
                current.title = candidate.title
                changed = True
            if not current.content_text and candidate.content_text:
                current.content_text = candidate.content_text
                changed = True
            if changed:
                updated += 1
            continue

        news = NewsItem(
            id=next_id,
            title=candidate.title,
            url=candidate.url,
            source=candidate.source,
            published_at=candidate.published_at,
            language=candidate.language,
            content_text=candidate.content_text,
            summary_cn=candidate.summary_cn,
            created_at=datetime.now(timezone.utc),
        )
        next_id += 1
        existing.append(news)
        by_url[news.url] = news
        added += 1

    _save_news_items(existing)
    return added, updated


def update_summaries(
    summarize_func: Callable[[str, str, str, str], str] | None = None,
    limit: int | None = None,
) -> int:
    items = list_news_items()
    changed = 0
    summarize = summarize_func or fallback_summary
    for item in items:
        if item.summary_cn.strip():
            continue
        item.summary_cn = summarize(item.title, item.source, item.language, item.content_text)
        changed += 1
        if limit is not None and changed >= limit:
            break
    if changed:
        _save_news_items(items)
    return changed


def _save_news_items(items: list[NewsItem]) -> None:
    _ensure_data_file()
    payload = [
        item.model_dump(mode="json")
        for item in sorted(items, key=lambda x: (x.created_at, x.published_at), reverse=True)
    ]
    NEWS_JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_news_items() -> int:
    items = list_news_items()
    count = len(items)
    _save_news_items([])
    return count
