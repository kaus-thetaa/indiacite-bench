import csv
import json

import pytest

from indiacite.annotate import build_template, merge_annotations, pairwise_kappa
from indiacite.cli import main
from indiacite.meta_csv import read_meta_csv

HEADER = "case_id,name,citation,court,year,judge\n"


def write(path, text):
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_meta_csv_ok(tmp_path):
    p = write(
        tmp_path / "m.csv",
        HEADER
        + "c1,Alpha v. Beta,(2010) 5 SCC 100,High Court of Beta,2010,A K Rao\n"
        + "c2,X v. Y,(2011) 1 SCC 1,Court,2011,\n",
    )
    metas = read_meta_csv(p)
    assert metas[0].judge == "A K Rao" and metas[1].judge is None and metas[1].year == 2011


@pytest.mark.parametrize(
    "body,msg",
    [
        ("c1,A v. B,(2010) 5 SCC 100,Court,abc,\n", "year must be a number"),
        ("c1,,(2010) 5 SCC 100,Court,2010,\n", "empty name"),
        ("c1,A v. B,x,Court,2010,\nc1,A v. B,y,Court,2010,\n", "duplicate case_id"),
    ],
)
def test_meta_csv_errors(tmp_path, body, msg):
    with pytest.raises(ValueError, match=msg):
        read_meta_csv(write(tmp_path / "m.csv", HEADER + body))


def test_meta_csv_missing_columns(tmp_path):
    with pytest.raises(ValueError, match="missing columns"):
        read_meta_csv(write(tmp_path / "m.csv", "case_id,name\nc1,A\n"))


def test_meta_command(tmp_path, capsys):
    p = write(tmp_path / "m.csv", HEADER + "c1,A v. B,(2010) 5 SCC 100,Court,2010,\n")
    out = tmp_path / "m.jsonl"
    assert main(["meta", "--csv", p, "--out", str(out)]) == 0
    assert json.loads(out.read_text())["case_id"] == "c1"


def gens():
    return [
        {
            "query_id": "q1",
            "answer": "It is Alpha v. Beta (2010) 5 SCC 100 and Gamma v. Delta (2011) 6 SCC 200.",
        }
    ]


def fill(path, labels):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    for r, lab in zip(rows, labels, strict=True):
        r["error_type"] = lab
        r["evidence"] = "checked" if lab != "valid" else ""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def test_template_merge_and_kappa(tmp_path):
    tpl = tmp_path / "t.csv"
    assert build_template(gens(), str(tpl)) == 2
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    for p in (a, b):
        p.write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")
    fill(a, ["valid", "nonexistent"])
    fill(b, ["valid", "citation_mismatch"])
    records, disputes = merge_annotations({"a1": str(a), "a2": str(b)})
    assert len(records) == 1 and len(disputes) == 1
    assert records[0]["citations"][0]["error_type"] == "valid"
    assert {x["annotator"] for x in records[0]["citations"][0]["labels"]} == {"a1", "a2"}
    kappa, n = pairwise_kappa(str(a), str(b))
    assert n == 2 and kappa < 1.0


def test_invalid_label_goes_to_disputes(tmp_path):
    tpl = tmp_path / "t.csv"
    build_template(gens(), str(tpl))
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    for p in (a, b):
        p.write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")
    fill(a, ["valid", "typo"])
    fill(b, ["valid", "typo"])
    records, disputes = merge_annotations({"a1": str(a), "a2": str(b)})
    assert len(records) == 1 and len(disputes) == 1
