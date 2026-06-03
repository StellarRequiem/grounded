"""Fetch a URL and reduce it to plain text, cached on disk. Stdlib only."""
from __future__ import annotations

import hashlib
import re
import urllib.request
from pathlib import Path

_CACHE = Path.home() / ".cache" / "grounded"
_UA = {"User-Agent": "grounded/0.1 (citation-grounding-check)"}


def _strip_html(html: str) -> str:
    html = re.sub(r"(?is)<(script|style|head|nav|footer).*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"&[#a-z0-9]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch(url: str, timeout: int = 15, use_cache: bool = True) -> str:
    _CACHE.mkdir(parents=True, exist_ok=True)
    key = _CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".txt")
    if use_cache and key.exists():
        return key.read_text(encoding="utf-8", errors="ignore")
    try:
        req = urllib.request.Request(url, headers=_UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(2_000_000).decode("utf-8", "ignore")
        text = _strip_html(raw)
    except Exception:
        text = ""
    key.write_text(text, encoding="utf-8")
    return text
