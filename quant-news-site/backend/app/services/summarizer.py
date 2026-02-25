from __future__ import annotations

import httpx

from ..config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_TIMEOUT_SECONDS


def summarize_news_to_cn(title: str, source: str, language: str, content_text: str = "") -> str:
    if not LLM_API_KEY or not LLM_MODEL:
        return fallback_summary(title, source, language, content_text)

    content_hint = (content_text or "").strip()
    if len(content_hint) > 1800:
        content_hint = content_hint[:1800] + "..."
    prompt = (
        "You are a financial news summarizer. "
        "Summarize the following financial news into concise Chinese (2-4 sentences), "
        "do not invent facts, mention uncertainty if details are limited.\n\n"
        f"Source: {source}\n"
        f"Language: {language}\n"
        f"Headline: {title}\n"
        f"Content (may be partial): {content_hint or '[not available]'}\n"
    )

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "Return only Chinese summary text. No bullets unless necessary."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=LLM_TIMEOUT_SECONDS) as client:
            resp = client.post(f"{LLM_BASE_URL.rstrip('/')}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return content or fallback_summary(title, source, language, content_text)
    except Exception:
        return fallback_summary(title, source, language, content_text)


def fallback_summary(title: str, source: str, language: str, content_text: str = "") -> str:
    details = ""
    if content_text:
        snippet = content_text.replace("\n", " ").strip()
        if len(snippet) > 180:
            snippet = snippet[:177].rstrip() + "..."
        if snippet:
            details = f" | snippet: {snippet}"
    if language == "en":
        return f"[MVP summary] {source}: {title} (connect LLM for Chinese summary){details}"
    return f"[MVP summary] {source}: {title}{details}"


def llm_config_status() -> dict[str, str | bool]:
    return {
        "llm_enabled": bool(LLM_API_KEY and LLM_MODEL),
        "llm_base_url": LLM_BASE_URL,
        "llm_model": LLM_MODEL or "",
    }
