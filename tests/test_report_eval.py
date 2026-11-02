from indiacite.baselines import DictResolver
from indiacite.cascade import Cascade, FormatStage, ResolverStage
from indiacite.cli import main
from indiacite.evaluation import evaluate_records
from indiacite.report import render_markdown

TEXT = "Relied on Alpha v. Beta (2010) 5 SCC 100 and Gamma v. Delta (1900) 99 SCC 999."


def test_report_markdown(tmp_path):
    reports = Cascade([FormatStage()]).check(TEXT)
    md = render_markdown(reports)
    assert "| flag | (1900) 99 SCC 999 |" in md
    assert "not a certificate" in md and "flagged 1" in md


def test_check_writes_report(tmp_path):
    src = tmp_path / "f.txt"
    src.write_text(TEXT, encoding="utf-8")
    out = tmp_path / "r.md"
    assert main(["check", str(src), "--report", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("# Citation check report")


def records():
    return [
        {
            "excerpt": "Alpha v. Beta (2010) 5 SCC 100",
            "citations": [{"raw": "(2010) 5 SCC 100", "error_type": "valid", "in_database": False}],
        },
        {
            "excerpt": "Gamma v. Delta (1900) 99 SCC 999",
            "citations": [{"raw": "(1900) 99 SCC 999", "error_type": "nonexistent"}],
        },
        {
            "excerpt": "Epsilon v. Zeta (2011) 6 SCC 200",
            "citations": [{"raw": "(2011) 6 SCC 200", "error_type": "citation_mismatch"}],
        },
    ]


def test_evaluate_records_defaults_do_not_flag_database_misses():
    cascade = Cascade(
        [FormatStage(), ResolverStage(DictResolver({"(2011) 6 SCC 200": "Eta v. Theta"}))]
    )
    res = evaluate_records(records(), cascade)
    assert res["per_type"] == {"citation_mismatch": (1, 1), "nonexistent": (1, 1)}
    assert res["gap_flagged"] == 0 and res["gap_total"] == 1
    assert res["needs_review"] == 1


def test_flag_not_found_inflates_coverage_gap_false_alarms():
    cascade = Cascade([FormatStage(), ResolverStage(DictResolver({}), flag_not_found=True)])
    res = evaluate_records(records(), cascade)
    assert res["gap_flagged"] == 1 and res["gap_total"] == 1


def test_eval_command_cascade_mode(tmp_path, capsys):
    import json

    data = tmp_path / "d.jsonl"
    data.write_text(
        "\n".join(
            json.dumps({**r, "id": str(i), "source": "synthetic"}) for i, r in enumerate(records())
        )
        + "\n"
    )
    assert main(["eval", str(data), "--flag-not-found"]) == 0
    out = capsys.readouterr().out
    assert "cascade n 3" in out and "coverage gap false alarms: 1/1" in out
