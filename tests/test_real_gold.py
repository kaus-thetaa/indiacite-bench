import json
from pathlib import Path

from indiacite.baselines import DictResolver
from indiacite.cascade import Cascade, FormatStage, ResolverStage
from indiacite.evaluation import evaluate_records
from indiacite.schema import validate_record

PATH = Path(__file__).resolve().parents[1] / "data" / "real_incidents" / "sc_2026_insc_668.jsonl"

# built from the court's own findings so this is a demonstration of mechanics and not a result
KNOWN = {
    "2020 SCC OnLine SC 341": "M. Subramaniam v. S. Janaki",
    "(2015) 2 SCC 1": "Everest Kento Cylinders Ltd. v. Union of India",
    "(2018) 16 SCC 228": "Canara Bank v. N.G. Subbaraya Setty & Anr.",
}


def load():
    return [json.loads(line) for line in PATH.read_text(encoding="utf-8").splitlines()]


def test_records_validate_and_labels_match_the_court_findings():
    recs = load()
    assert all(validate_record(r) == [] for r in recs)
    labels = sorted(r["citations"][0]["error_type"] for r in recs)
    assert labels == [
        "citation_mismatch",
        "nonexistent",
        "nonexistent",
        "nonexistent",
        "wrong_pinpoint",
        "wrong_pinpoint",
    ]


def test_lookup_catches_mismatch_but_misses_wrong_pinpoints():
    cascade = Cascade([FormatStage(), ResolverStage(DictResolver(KNOWN))])
    res = evaluate_records(load(), cascade)
    assert res["per_type"]["citation_mismatch"] == (1, 1)
    assert res["per_type"]["wrong_pinpoint"] == (0, 2)
    assert res["per_type"]["nonexistent"] == (0, 3)
    assert res["needs_review"] == 3


def test_flagging_not_found_catches_nonexistent_but_not_wrong_pinpoints():
    cascade = Cascade([FormatStage(), ResolverStage(DictResolver(KNOWN), flag_not_found=True)])
    res = evaluate_records(load(), cascade)
    assert res["per_type"]["nonexistent"] == (3, 3)
    assert res["per_type"]["wrong_pinpoint"] == (0, 2)
