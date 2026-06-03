"""grounded — verify a cited report is grounded in its sources."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .fetch import fetch
from .ground import grounding
from .parse import parse

_ICON = {"SUPPORTED": "✅", "WEAK": "⚠️ ", "UNSUPPORTED": "⛔", "UNSOURCED": " ·"}


def check(text: str, net: bool = True) -> list[dict]:
    cache: dict[str, str] = {}
    rows = []
    for c in parse(text):
        srcs = []
        if net:
            for u in c["sources"]:
                cache.setdefault(u, fetch(u))
                srcs.append(cache[u])
        rows.append({**c, **grounding(c["claim"], srcs if c["sources"] else [])})
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="grounded", description="verify a cited report is grounded in its sources")
    ap.add_argument("file", nargs="?", help="markdown report (default: stdin)")
    ap.add_argument("--no-net", action="store_true", help="don't fetch sources (parse only)")
    a = ap.parse_args(argv)
    text = Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read()
    rows = check(text, net=not a.no_net)

    # only report sentences that are factual claims (cite a source or state a number)
    factual = [r for r in rows if r["sources"] or r["nums"] > 0]
    print("GROUNDED — citation check\n")
    if not factual:
        print("  no cited or numeric claims found.")
        return 0
    bad = 0
    for r in factual:
        print(f"{_ICON[r['verdict']]} [{r['verdict']:<11}] {r['claim'][:84]}")
        if r["verdict"] == "UNSUPPORTED" and r["sources"]:
            print(f"      ↳ cited source doesn't contain the claim's facts: {r['sources']}")
            bad += 1
        elif r["verdict"] == "UNSOURCED":
            print("      ↳ a specific claim with no citation")
    n = len(factual)
    supp = sum(r["verdict"] == "SUPPORTED" for r in factual)
    unsourced = sum(r["verdict"] == "UNSOURCED" for r in factual)
    print(f"\nGrounding score: {round(100 * supp / n)}% ({supp}/{n} supported) · "
          f"{bad} unsupported (likely fabricated cite) · {unsourced} unsourced")
    return 1 if bad else 0
