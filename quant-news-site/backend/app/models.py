from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    id: int
    title: str
    url: str
    source: str
    published_at: datetime
    language: Literal["zh", "en", "unknown"] = "unknown"
    content_text: str = ""
    summary_cn: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NewsCreate(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime
    language: Literal["zh", "en", "unknown"] = "unknown"
    content_text: str = ""
    summary_cn: str = ""


class JobResponse(BaseModel):
    job: str
    status: str
    message: str
    count: int = 0
    triggered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SourceInfo(BaseModel):
    name: str
    url: str
    language: Literal["zh", "en", "unknown"] = "unknown"
    enabled: bool = True
    source_type: Literal["rss", "api", "web"] = "rss"
    fetch_body: bool = False
    is_custom: bool = False


class SourceCreate(BaseModel):
    name: str
    url: str
    language: Literal["zh", "en", "unknown"] = "unknown"
    enabled: bool = True
    source_type: Literal["rss", "api", "web"] = "rss"
    fetch_body: bool = False
