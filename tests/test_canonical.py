from indiacite.citations import canonical_key, extract_citations, normalize_citation


def test_two_scc_formats_have_same_key():
    assert canonical_key("(2010) 5 SCC 100") == canonical_key("2010 (5) SCC 100")


def test_different_citations_differ():
    assert canonical_key("(2010) 5 SCC 100") != canonical_key("(2010) 5 SCC 101")
    assert canonical_key("(2010) 5 SCC 100") != canonical_key("AIR 2010 SC 100")


def test_alt_format_is_extracted():
    cites = extract_citations("see 2010 (5) SCC 100 for this")
    assert len(cites) == 1 and cites[0].scheme == "scc" and cites[0].year == 2010


def test_no_key_for_plain_text():
    assert canonical_key("not a citation") is None


def test_normalize_citation_ignores_spacing_and_case():
    assert normalize_citation("(2010)  5 SCC 100") == normalize_citation("(2010) 5 scc 100")
