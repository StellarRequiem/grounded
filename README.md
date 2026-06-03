# grounded

**Research you can't hallucinate — verify that every claim in a cited report is actually supported by the source it cites.**

AI research tools cite confidently and wrongly: a claim with a footnote whose source says nothing of the kind. `grounded` reads a cited report, fetches each source, and flags any claim whose source doesn't even contain its key facts or numbers — **fabricated and mismatched citations**, the failure that makes AI research untrustworthy.

Deterministic. No API.

## Use it

```sh
pip install "git+https://github.com/StellarRequiem/grounded"
grounded report.md
cat report.md | grounded
```

## What it does

```
GROUNDED — citation check

✅ [SUPPORTED  ] Python was first released in 1991 by Guido van Rossum.
⛔ [UNSUPPORTED] Bitcoin reached a price of $999,999 in 2021.
      ↳ cited source doesn't contain the claim's facts: ['https://en.wikipedia.org/wiki/Python...']
 · [UNSOURCED  ] The global market grew by exactly 73.4% last year.

Grounding score: 50% (1/2 supported) · 1 unsupported (likely fabricated cite) · 1 unsourced
```

- **✅ SUPPORTED** — the cited source contains the claim's numbers and key terms.
- **⛔ UNSUPPORTED** — the source doesn't contain the claim's facts: a fabricated or mismatched citation. Exit code `1`.
- **· UNSOURCED** — a specific claim with no citation at all.

The **grounding score** is the share of factual claims actually backed by their sources.

## The pipeline

`grounded` is the *verify* stage of a trustworthy-research loop: **research** (gather sources) → **ground** (this tool — every claim must trace to a source that supports it) → **report** (the grounding score, ungrounded claims flagged, never hidden).

## The honest boundary

The deterministic check is **term + number grounding**: a claim's facts must appear in its cited source. This catches the *egregious, common* failure — a citation that doesn't even mention the claim. It does **not** judge semantic entailment ("does this source truly support this nuanced argument") — that's the LLM layer above it. What v1 guarantees: **no claim rides on a citation that doesn't mention it.**

## Tests

```sh
pip install -e ".[dev]"
pytest
```

No dependencies — pure standard library.

## License

Apache-2.0. Built by [@StellarRequiem](https://github.com/StellarRequiem).
