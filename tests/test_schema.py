import copy

from indiacite.schema import MAX_EXCERPT_CHARS, validate_record

GOOD = {
    "id": "t-1",
    "source": "synthetic",
    "excerpt": "As held in X v. Y (2010) 5 SCC 100 the rule applies.",
    "citations": [{"raw": "(2010) 5 SCC 100", "error_type": "valid"}],
}


def test_good_record_passes():
    assert validate_record(GOOD) == []


def test_missing_field():
    bad = copy.deepcopy(GOOD)
    del bad["excerpt"]
    assert any("missing field" in e for e in validate_record(bad))


def test_long_excerpt_rejected():
    bad = copy.deepcopy(GOOD)
    bad["excerpt"] = "x" * (MAX_EXCERPT_CHARS + 1)
    assert any("longer than" in e for e in validate_record(bad))


def test_raw_must_be_in_excerpt():
    bad = copy.deepcopy(GOOD)
    bad["citations"][0]["raw"] = "(1999) 1 SCC 1"
    assert any("not found in excerpt" in e for e in validate_record(bad))


def test_error_needs_evidence():
    bad = copy.deepcopy(GOOD)
    bad["citations"][0]["error_type"] = "nonexistent"
    assert any("needs evidence" in e for e in validate_record(bad))


def test_real_incident_needs_ref_and_anonymized():
    bad = copy.deepcopy(GOOD)
    bad["source"] = "real_incident"
    errs = validate_record(bad)
    assert any("incident_ref" in e for e in errs)
    assert any("anonymized" in e for e in errs)


def test_bad_source():
    bad = copy.deepcopy(GOOD)
    bad["source"] = "scraped"
    assert any("source must be" in e for e in validate_record(bad))
