from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .models import JobResponse, NewsItem, SourceCreate, SourceInfo
from .services.jobs import run_fetch_job, run_summarize_job
from .services.summarizer import llm_config_status
from .sources import add_local_source, all_rss_sources
from .storage import clear_news_items, get_news_item, list_news_items


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
FRONTEND_INDEX = FRONTEND_DIR / "index.html"


app = FastAPI(title="Personal News Desk API", version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/news", response_model=list[NewsItem])
def api_list_news(
    limit: int = Query(default=50, ge=1, le=5000),
    source: str | None = None,
    language: str | None = None,
    q: str | None = None,
) -> list[NewsItem]:
    items = list_news_items()
    if source:
        items = [item for item in items if item.source.lower() == source.lower()]
    if language:
        items = [item for item in items if item.language.lower() == language.lower()]
    if q:
        needle = q.lower()
        items = [
            item
            for item in items
            if needle in item.title.lower()
            or needle in item.summary_cn.lower()
            or needle in item.content_text.lower()
        ]
    return items[:limit]


@app.get("/api/news/{news_id}", response_model=NewsItem)
def api_get_news(news_id: int) -> NewsItem:
    item = get_news_item(news_id)
    if item is None:
        raise HTTPException(status_code=404, detail="news item not found")
    return item


@app.post("/api/jobs/fetch", response_model=JobResponse)
def api_trigger_fetch(
    per_source_limit: int | None = Query(default=None, ge=1, le=200),
    total_limit: int | None = Query(default=None, ge=1, le=1000),
) -> JobResponse:
    added, updated, errors = run_fetch_job(per_source_limit=per_source_limit, total_limit=total_limit)
    msg = f"fetch completed: added={added}, updated={updated}"
    if per_source_limit is not None or total_limit is not None:
        msg += f" (limits: per_source={per_source_limit or 'default'}, total={total_limit or 'default'})"
    if errors:
        msg += f", errors={len(errors)}"
    return JobResponse(job="fetch", status="done", message=msg, count=added + updated)


@app.post("/api/jobs/summarize", response_model=JobResponse)
def api_trigger_summarize(
    limit: int | None = Query(default=None, ge=1, le=1000),
) -> JobResponse:
    changed = run_summarize_job(limit=limit)
    return JobResponse(
        job="summarize",
        status="done",
        message=f"summarize completed: updated={changed}{f' (limit={limit})' if limit is not None else ''}",
        count=changed,
    )


@app.post("/api/jobs/clear", response_model=JobResponse)
def api_clear_news() -> JobResponse:
    removed = clear_news_items()
    return JobResponse(
        job="clear",
        status="done",
        message=f"clear completed: removed={removed}",
        count=removed,
    )


@app.get("/api/sources", response_model=list[SourceInfo])
def api_list_sources() -> list[SourceInfo]:
    return [SourceInfo.model_validate(source) for source in all_rss_sources()]


@app.post("/api/sources", response_model=SourceInfo)
def api_add_source(payload: SourceCreate) -> SourceInfo:
    if payload.source_type != "rss":
        raise HTTPException(status_code=400, detail="MVP currently supports rss sources only")
    if not (payload.url.startswith("http://") or payload.url.startswith("https://")):
        raise HTTPException(status_code=400, detail="source url must start with http:// or https://")

    saved = add_local_source(payload.model_dump())
    return SourceInfo.model_validate({**saved, "is_custom": True})


@app.get("/api/meta")
def api_meta() -> dict[str, object]:
    return {
        "service": "quant-news-site-api",
        "version": "0.2.0",
        "llm": llm_config_status(),
        "news_count": len(list_news_items()),
        "cors": "enabled",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def app_index() -> FileResponse:
    if not FRONTEND_INDEX.exists():
        raise HTTPException(status_code=404, detail="frontend index.html not found")
    return FileResponse(FRONTEND_INDEX)
