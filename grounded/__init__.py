"""grounded — research you can't hallucinate.

Verifies that every claim in a cited report is actually supported by the source
it cites. Parses claims + citations, fetches each source, and flags any claim
whose source doesn't even contain its key facts/numbers — i.e. fabricated or
mismatched citations, the #1 failure mode of AI research.

Deterministic, no API. (Semantic entailment — "does this source truly support
this nuanced claim" — is the documented LLM layer; v1 guarantees no claim rides
on a citation that doesn't mention it.)
"""
from .ground import grounding
from .parse import parse

__version__ = "0.1.0"
__all__ = ["parse", "grounding"]
