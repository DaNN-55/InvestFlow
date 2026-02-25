import json

from .config import SOURCES_LOCAL_JSON_PATH


DEFAULT_RSS_SOURCES: list[dict[str, str | bool]] = [
    {
        "name": "CNBC Top News",
        "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "language": "en",
        "enabled": True,
        "source_type": "rss",
        "fetch_body": True,
    },
    {
        "name": "NYT Business",
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
        "language": "en",
        "enabled": True,
        "source_type": "rss",
        "fetch_body": True,
    },
    {
        "name": "Reuters World News",
        "url": "https://feeds.reuters.com/Reuters/worldNews",
        "language": "en",
        "enabled": True,
        "source_type": "rss",
        "fetch_body": True,
    },
    {
        "name": "Reuters Business News",
        "url": "https://feeds.reuters.com/reuters/businessNews",
        "language": "en",
        "enabled": True,
        "source_type": "rss",
        "fetch_body": True,
    },
    {
        "name": "MarketWatch Top Stories",
        "url": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
        "language": "en",
        "enabled": True,
        "source_type": "rss",
        "fetch_body": True,
    },
    {
        "name": "FTChinese Daily (example, verify/update)",
        "url": "https://www.ftchinese.com/rss/feed",
        "language": "zh",
        "enabled": True,
        "source_type": "rss",
        "fetch_body": True,
    },
    {
        "name": "Sina Finance Roll (example, verify/update)",
        "url": "https://finance.sina.com.cn/rss/roll.xml",
        "language": "zh",
        "enabled": True,
        "source_type": "rss",
        "fetch_body": False,
    },
    {
        "name": "36Kr Finance (example, verify/update)",
        "url": "https://36kr.com/feed",
        "language": "zh",
        "enabled": False,
        "source_type": "rss",
        "fetch_body": True,
    },
    {
        "name": "Caixin Global (example, verify/update)",
        "url": "https://www.caixinglobal.com/rss/feed.xml",
        "language": "en",
        "enabled": False,
        "source_type": "rss",
        "fetch_body": True,
    },
]


def all_rss_sources() -> list[dict[str, str | bool]]:
    local_sources = _load_local_sources()
    if not local_sources:
        return DEFAULT_RSS_SOURCES

    merged = list(DEFAULT_RSS_SOURCES)
    seen = {_source_key(s) for s in merged}
    for source in local_sources:
        key = _source_key(source)
        if key in seen:
            # local entry with same url/name overrides the default
            for idx, default_source in enumerate(merged):
                if _source_key(default_source) == key:
                    merged[idx] = {
                        **default_source,
                        **source,
                        "is_custom": True,
                    }
                    break
            continue
        merged.append({**source, "is_custom": True})
        seen.add(key)
    return merged


def enabled_rss_sources() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for source in all_rss_sources():
        if not source.get("enabled", True):
            continue
        result.append(
            {
                "name": str(source["name"]),
                "url": str(source["url"]),
                "language": str(source.get("language", "unknown")),
                "fetch_body": bool(source.get("fetch_body", False)),
                "source_type": str(source.get("source_type", "rss")),
            }
        )
    return result


def add_local_source(source: dict[str, str | bool]) -> dict[str, str | bool]:
    local_sources = _load_local_sources()
    normalized = _normalize_source_record(source)
    key = _source_key(normalized)

    for idx, existing in enumerate(local_sources):
        if _source_key(existing) == key:
            local_sources[idx] = {**existing, **normalized}
            _save_local_sources(local_sources)
            return local_sources[idx]

    local_sources.append(normalized)
    _save_local_sources(local_sources)
    return normalized


def _load_local_sources() -> list[dict[str, str | bool]]:
    if not SOURCES_LOCAL_JSON_PATH.exists():
        return []
    try:
        raw = json.loads(SOURCES_LOCAL_JSON_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(raw, list):
        return []

    normalized: list[dict[str, str | bool]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        url = str(item.get("url", "")).strip()
        if not name or not url:
            continue
        normalized.append(_normalize_source_record(item))
    return normalized


def _save_local_sources(items: list[dict[str, str | bool]]) -> None:
    SOURCES_LOCAL_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    SOURCES_LOCAL_JSON_PATH.write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _normalize_source_record(item: dict[str, object]) -> dict[str, str | bool]:
    return {
        "name": str(item.get("name", "")).strip(),
        "url": str(item.get("url", "")).strip(),
        "language": str(item.get("language", "unknown")),
        "enabled": bool(item.get("enabled", True)),
        "source_type": str(item.get("source_type", "rss")),
        "fetch_body": bool(item.get("fetch_body", False)),
    }


def _source_key(item: dict[str, str | bool]) -> tuple[str, str]:
    return (str(item.get("url", "")).strip().lower(), str(item.get("name", "")).strip().lower())
