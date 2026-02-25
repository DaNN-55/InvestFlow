from __future__ import annotations

import html
import re

import httpx

from ..config import FETCH_ARTICLE_BODY, FETCH_HTTP_TIMEOUT_SECONDS


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL)
BLOCK_RE = re.compile(r"</?(p|div|br|li|h\d|article|section)[^>]*>", re.IGNORECASE)


def extract_entry_text(entry: object) -> str:
    pieces: list[str] = []

    for attr in ("summary", "description"):
        value = getattr(entry, attr, None)
        if isinstance(value, str) and value.strip():
            pieces.append(_clean_html_to_text(value))

    contents = getattr(entry, "content", None)
    if isinstance(contents, list):
        for item in contents:
            if isinstance(item, dict):
                raw = item.get("value")
                if isinstance(raw, str) and raw.strip():
                    pieces.append(_clean_html_to_text(raw))

    merged = " ".join(p for p in pieces if p)
    return _trim_text(merged, 1600)


def fetch_article_text(url: str) -> str:
    if not FETCH_ARTICLE_BODY:
        return ""
    try:
        with httpx.Client(timeout=FETCH_HTTP_TIMEOUT_SECONDS, follow_redirects=True) as client:
            resp = client.get(url, headers={"User-Agent": "quant-news-site-mvp/0.1"})
            resp.raise_for_status()
            ctype = resp.headers.get("content-type", "")
            if "html" not in ctype:
                return ""
            return _extract_html_main_text(resp.text)
    except Exception:
        return ""


def _extract_html_main_text(raw_html: str) -> str:
    text = SCRIPT_STYLE_RE.sub(" ", raw_html)
    text = BLOCK_RE.sub("\n", text)
    text = TAG_RE.sub(" ", text)
    text = html.unescape(text)
    lines = [SPACE_RE.sub(" ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if len(line) >= 25]
    if not lines:
        return ""
    joined = "\n".join(lines[:20])
    return _trim_text(joined, 2500)


def _clean_html_to_text(value: str) -> str:
    value = html.unescape(value)
    value = BLOCK_RE.sub("\n", value)
    value = TAG_RE.sub(" ", value)
    value = SPACE_RE.sub(" ", value).strip()
    return value


def _trim_text(text: str, max_chars: int) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."

