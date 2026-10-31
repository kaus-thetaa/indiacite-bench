import json
from pathlib import Path

from indiacite.charlotin import (
    find_ref,
    read_rows,
    rows_for_country,
    split_items,
    to_stub,
    write_stubs,
)
from indiacite.taxonomy import ErrorType, classify_item

FIX = str(Path(__file__).parent / "fixtures" / "charlotin_sample.csv")


def test_split_items():
    cell = "Fabricated: Case Law | no such case || False Quotes: Case Law | not in text"
    items = split_items(cell)
    assert [(i.category, i.subcategory) for i in items] == [
        ("Fabricated", "Case Law"),
        ("False Quotes", "Case Law"),
    ]


def test_country_filter_handles_multi_state():
    rows = rows_for_country(read_rows(FIX), "India")
    assert [r["Case Name"] for r in rows] == [
        "Fictional One v. Fictional Two",
        "Fictional Three v. Fictional Four",
    ]


def test_classification():
    assert classify_item("Fabricated", "Case Law", "no such case")[0] is ErrorType.NONEXISTENT
    mismatch = classify_item("Fabricated", "Case Law", "the citation corresponds to another case")
    assert mismatch == (ErrorType.CITATION_MISMATCH, False)
    assert classify_item("Outdated Advice", "Repealed Law", "x") == (ErrorType.STALE_STATUTE, True)
    assert classify_item("Weird", "Thing", "x") == (None, False)


def test_stub_has_attribution_and_ref():
    row = rows_for_country(read_rows(FIX))[0]
    stub = to_stub(row, 1)
    assert stub["incident_ref"].startswith("https://www.damiencharlotin.com/documents/")
    assert "CC BY 4.0" in stub["attribution"]
    assert stub["status"] == "todo"
    assert len(stub["items"]) == 2


def test_write_stubs(tmp_path):
    out = tmp_path / "stubs.jsonl"
    n = write_stubs(rows_for_country(read_rows(FIX)), str(out))
    lines = out.read_text(encoding="utf-8").splitlines()
    assert n == 2 and len(lines) == 2
    assert json.loads(lines[0])["stub_id"] == "stub-001"


def test_find_ref_handles_both_layouts():
    assert find_ref({"Source": "/documents/1/a.pdf", "Pointer": "Courtready"}).endswith("/a.pdf")
    assert find_ref({"Pointer": "/documents/2/b.pdf", "Source": ""}).endswith("/b.pdf")
    assert find_ref({"Pointer": "", "Source": "https://example.org/x"}) == "https://example.org/x"
    assert find_ref({}) == ""
