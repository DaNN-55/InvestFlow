from ..config import FETCH_MAX_ITEMS_PER_SOURCE, FETCH_MAX_TOTAL_ITEMS_PER_RUN, SUMMARIZE_MAX_ITEMS_PER_RUN
from .rss_fetcher import fetch_default_sources
from .summarizer import summarize_news_to_cn
from ..storage import upsert_news_items, update_summaries


def run_fetch_job(
    per_source_limit: int | None = None,
    total_limit: int | None = None,
) -> tuple[int, int, list[str]]:
    fetched_items, errors = fetch_default_sources(
        per_source_limit=per_source_limit if per_source_limit is not None else FETCH_MAX_ITEMS_PER_SOURCE,
        total_limit=total_limit if total_limit is not None else FETCH_MAX_TOTAL_ITEMS_PER_RUN,
    )
    added, updated = upsert_news_items(fetched_items)
    return added, updated, errors


def run_summarize_job(limit: int | None = None) -> int:
    effective_limit = SUMMARIZE_MAX_ITEMS_PER_RUN if limit is None else limit
    return update_summaries(summarize_func=summarize_news_to_cn, limit=effective_limit)
