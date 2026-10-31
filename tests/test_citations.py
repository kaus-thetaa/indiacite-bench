from indiacite.citations import extract_citations, is_plausible


def test_extracts_each_scheme():
    text = (
        "see (2004) 7 SCC 528 and AIR 1978 SC 597 and 2024 INSC 12 "
        "and [1978] 2 SCR 621 and 2021 SCC OnLine SC 345"
    )
    schemes = [c.scheme for c in extract_citations(text)]
    assert schemes == ["scc", "air", "insc", "scr", "scc_online"]


def test_no_overlap_and_order():
    cites = extract_citations("2021 SCC OnLine SC 345 then (2004) 7 SCC 528")
    assert [c.start for c in cites] == sorted(c.start for c in cites)
    assert len(cites) == 2


def test_scc_sub_series():
    cites = extract_citations("(2012) 1 SCC (Cri) 100")
    assert len(cites) == 1 and cites[0].scheme == "scc"


def test_plausibility_bounds():
    scc_old = extract_citations("(1900) 99 SCC 999")[0]
    insc_old = extract_citations("2019 INSC 5")[0]
    ok = extract_citations("(2004) 7 SCC 528")[0]
    future = extract_citations("(2999) 7 SCC 528")[0]
    assert not is_plausible(scc_old)
    assert not is_plausible(insc_old)
    assert is_plausible(ok)
    assert not is_plausible(future)


def test_plain_text_has_no_citations():
    assert extract_citations("no citation here") == []
