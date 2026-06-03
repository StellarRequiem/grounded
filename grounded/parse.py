"""Parse a markdown report into claims, each with the source URLs it cites.

Handles inline links — ``[text](https://…)`` — and footnote refs — ``claim [1].``
with a ``[1]: https://…`` definition elsewhere in the doc.
"""
from __future__ import annotations

import re

_INLINE = re.compile(r"\[[^\]]*\]\((https?://[^)]+)\)")
_BARE = re.compile(r"(?<!\])(?<!\()\bhttps?://[^\s)\]]+")
_FOOTREF = re.compile(r"\[(\d+)\]")
_FOOTDEF = re.compile(r"^\s*\[(\d+)\]:?\s+(https?://\S+)", re.M)


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]


def footnotes(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2).rstrip(".,);") for m in _FOOTDEF.finditer(text)}


def parse(text: str) -> list[dict]:
    notes = footnotes(text)
    out = []
    for s in split_sentences(text):
        if s.startswith("#") or _FOOTDEF.match(s):
            continue  # heading or a footnote-definition line, not a claim
        urls = [u.rstrip(".,);") for u in _INLINE.findall(s)]
        urls += [u.rstrip(".,);") for u in _BARE.findall(s)]
        urls += [notes[r] for r in _FOOTREF.findall(s) if r in notes]
        out.append({"claim": s, "sources": list(dict.fromkeys(urls))})
    return out
