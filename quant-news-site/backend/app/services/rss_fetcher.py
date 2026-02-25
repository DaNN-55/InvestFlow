from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser

from ..config import FETCH_MAX_ITEMS_PER_SOURCE, FETCH_MAX_TOTAL_ITEMS_PER_RUN
from ..models import NewsCreate
from .article_parser import extract_entry_text, fetch_article_text
from ..sources import enabled_rss_sources


def fetch_default_sources(
    per_source_limit: int | None = None,
    total_limit: int | None = None,
) -> tuple[list[NewsCreate], list[str]]:
    all_items: list[NewsCreate] = []
    errors: list[str] = []
    per_source_limit = _sanitize_limit(per_source_limit, FETCH_MAX_ITEMS_PER_SOURCE)
    total_limit = _sanitize_limit(total_limit, FETCH_MAX_TOTAL_ITEMS_PER_RUN)

    for source in enabled_rss_sources():
        if total_limit is not None and len(all_items) >= total_limit:
            break
        try:
            remaining = None if total_limit is None else max(total_limit - len(all_items), 0)
            source_cap = per_source_limit
            if remaining is not None:
                source_cap = remaining if source_cap is None else min(source_cap, remaining)
            all_items.extend(fetch_rss_source(source, max_items=source_cap))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{source['name']}: {exc}")
    return all_items, errors


def fetch_rss_source(source: dict[str, object], max_items: int | None = None) -> list[NewsCreate]:
    parsed = feedparser.parse(source["url"])
    if getattr(parsed, "bozo", 0):
        # feedparser sets bozo for malformed feeds; keep processing if entries exist.
        if not getattr(parsed, "entries", None):
            raise ValueError(f"failed to parse feed: {source['url']}")

    items: list[NewsCreate] = []
    for entry in getattr(parsed, "entries", []):
        if max_items is not None and len(items) >= max_items:
            break
        title = (getattr(entry, "title", "") or "").strip()
        link = (getattr(entry, "link", "") or "").strip()
        if not title or not link:
            continue

        published_at = _extract_published(entry)
        content_text = extract_entry_text(entry)
        if bool(source.get("fetch_body")) and len(content_text) < 200:
            fetched_text = fetch_article_text(link)
            if fetched_text:
                content_text = fetched_text
        items.append(
            NewsCreate(
                title=title,
                url=link,
                source=str(source["name"]),
                published_at=published_at,
                language=str(source.get("language", "unknown")),  # type: ignore[arg-type]
                content_text=content_text,
                summary_cn="",
            )
        )
    return items


def _sanitize_limit(requested: int | None, default_value: int) -> int | None:
    if requested is None:
        requested = default_value
    if requested <= 0:
        return None
    return requested


def _extract_published(entry: object) -> datetime:
    for field in ("published", "updated", "created"):
        value = getattr(entry, field, None)
        if not value:
            continue
        try:
            dt = parsedate_to_datetime(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:  # noqa: BLE001
            continue
    return datetime.now(timezone.utc)
