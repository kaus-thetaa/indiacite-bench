import json
from pathlib import Path

from indiacite.cli import main

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = str(ROOT / "data" / "examples" / "synthetic_sample.jsonl")
FIX = str(ROOT / "tests" / "fixtures" / "charlotin_sample.csv")


def test_validate_sample_ok(capsys):
    assert main(["validate", SAMPLE]) == 0
    assert "problems 0" in capsys.readouterr().out


def test_validate_bad_file_fails(tmp_path, capsys):
    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps({"id": "x", "source": "nope"}) + "\n")
    assert main(["validate", str(bad)]) == 1


def test_duplicate_ids_flagged(tmp_path, capsys):
    rec = json.loads(Path(SAMPLE).read_text().splitlines()[0])
    dup = tmp_path / "dup.jsonl"
    dup.write_text(json.dumps(rec) + "\n" + json.dumps(rec) + "\n")
    assert main(["validate", str(dup)]) == 1
    assert "duplicate id" in capsys.readouterr().out


def test_eval_runs(capsys):
    assert main(["eval", SAMPLE]) == 0
    out = capsys.readouterr().out
    assert "baseline format" in out and "synthetic" in out


def test_stubs_command(tmp_path, capsys):
    out = tmp_path / "stubs.jsonl"
    assert main(["stubs", "--csv", FIX, "--out", str(out)]) == 0
    assert len(out.read_text().splitlines()) == 2
