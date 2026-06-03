"""Parsing claims+citations and grounding-against-source must be correct."""
from grounded.ground import grounding, key_terms
from grounded.parse import footnotes, parse


def test_parse_inline_and_footnote():
    text = ("Sales hit 5 million in 2024 ([rpt](https://a.com/x)).\n"
            "Growth was 40% [1].\n\n[1]: https://b.com/y")
    claims = parse(text)
    srcs = [s for c in claims for s in c["sources"]]
    assert any("a.com/x" in s for s in srcs)
    assert any("b.com/y" in s for s in srcs)
    assert footnotes(text)["1"] == "https://b.com/y"


def test_grounding_supported():
    src = ["the market reached 5 million users and grew 40 percent in 2024"]
    g = grounding("The market grew 40% in 2024 to 5 million users.", src)
    assert g["verdict"] in ("SUPPORTED", "WEAK")
    assert g["num_hit"] == g["nums"]            # all numbers present in source


def test_grounding_fabricated_citation():
    src = ["this page is about cooking recipes and has no statistics whatsoever"]
    g = grounding("Revenue grew 250% to $9 billion in 2023.", src)
    assert g["verdict"] == "UNSUPPORTED"        # source has none of the numbers
    assert g["num_hit"] == 0


def test_unsourced():
    assert grounding("The figure was 42 percent.", [])["verdict"] == "UNSOURCED"


def test_key_terms_drops_stopwords():
    nums, terms = key_terms("The revenue was 5 billion in 2024.")
    assert "5" in nums and "2024" in nums
    assert "revenue" in terms and "the" not in terms and "was" not in terms
