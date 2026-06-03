# Examples — grounded auditing a real research report

`ai-verification-report.md` is a real report produced by a multi-agent deep-research
run (107 agents, 25 sources, claims 3-vote adversarially verified). Running `grounded`:

```
grounded ai-verification-report.md
→ Grounding score: 64% (7/11 supported) · 1 unsupported · 3 unsourced  (exit 1)
```

Two *independent* verification layers catching *different* things:

- **7 SUPPORTED** — DeepEval's ~15.9k stars, HHEM's 106,917 downloads, Galileo's $45M
  Series B, etc. were found verbatim in their cited sources. ✅
- **1 UNSUPPORTED — caught a claim deep-research had *confirmed*.** "LM-Polygraph
  implements over 40 UQ methods" was verified upstream by *counting README rows* (54),
  but the source never states "40 methods" — so `grounded` flags it: a reasonable
  *inference*, not a verbatim-grounded fact. The two layers disagree, usefully.
- **3 UNSOURCED** — including the two claims deep-research itself *refuted*; with no
  citation, `grounded` correctly flags them as untrustworthy.

The honest boundary on display: `grounded` checks whether a source textually contains a
claim's facts. It can't tell a sound inference from a fabrication — but it *can* tell you
which claims aren't verbatim-backed and need a human's eye. That's the whole job.
