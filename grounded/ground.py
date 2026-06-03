"""Grounding check — does a claim's cited source actually contain its key facts?

Deterministic baseline: a claim's numbers and significant terms must appear in the
source text. A claim with numbers whose source contains NONE of them is almost
certainly a fabricated/mismatched citation → UNSUPPORTED. This catches the worst,
most common failure; semantic entailment is the LLM layer above it.
"""
from __future__ import annotations

import re

_STOP = set(
    "the a an of to in on and or for with is are was were be been being it this that "
    "these those as by at from into over under not no will can could would should may "
    "might do does did has have had its their his her our your my we you they he she i "
    "than then so but if about more most some all each per via using used also".split())
_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")   # number with optional decimal — no trailing dot
_WORD = re.compile(r"[A-Za-z][A-Za-z\-]{2,}")


def key_terms(claim: str) -> tuple[list[str], list[str]]:
    nums = list(dict.fromkeys(_NUM.findall(claim)))
    terms = [w.lower() for w in _WORD.findall(claim)]
    terms = list(dict.fromkeys(t for t in terms if t not in _STOP))
    return nums, terms


def grounding(claim: str, source_texts: list[str]) -> dict:
    nums, terms = key_terms(claim)
    if not source_texts:
        return {"verdict": "UNSOURCED", "nums": len(nums), "terms": len(terms),
                "num_hit": 0, "term_hit": 0}
    blob = " ".join(source_texts).lower()
    num_hit = sum(1 for n in nums if n.lower() in blob)
    term_hit = sum(1 for t in terms if t in blob)
    term_frac = term_hit / len(terms) if terms else 1.0

    if nums and num_hit == 0:
        verdict = "UNSUPPORTED"           # the figures aren't in the cited source at all
    elif (not nums or num_hit == len(nums)) and term_frac >= 0.6:
        verdict = "SUPPORTED"
    elif num_hit > 0 or term_frac >= 0.3:
        verdict = "WEAK"
    else:
        verdict = "UNSUPPORTED"
    return {"verdict": verdict, "nums": len(nums), "terms": len(terms),
            "num_hit": num_hit, "term_hit": term_hit}
