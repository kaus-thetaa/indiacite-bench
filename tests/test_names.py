from indiacite.names import name_similarity, names_match, normalize_name


def test_normalize_handles_versus_variants():
    assert normalize_name("Alpha Traders vs. State of Beta") == "alpha traders v state of beta"
    assert normalize_name("Alpha Traders v State of Beta") == "alpha traders v state of beta"
    assert (
        normalize_name("ALPHA  TRADERS  VERSUS  STATE OF BETA") == "alpha traders v state of beta"
    )


def test_match_and_mismatch():
    assert names_match("Alpha Traders v. State of Beta", "Alpha Traders vs State of Beta")
    assert not names_match("Epsilon v. Zeta", "Eta v. Theta")


def test_similarity_bounds():
    assert name_similarity("a v b", "a v b") == 1.0
    assert 0.0 <= name_similarity("a v b", "x v y") < 1.0
