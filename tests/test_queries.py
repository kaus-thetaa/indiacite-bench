import json

import pytest

from indiacite.cli import main
from indiacite.queries import CaseMeta, build_queries, score_answer

META = CaseMeta(
    "c1",
    "Alpha Traders v. State of Beta",
    "(2010) 5 SCC 100",
    "High Court of Beta",
    2010,
    "A. K. Rao",
)


def q(kind):
    return next(x for x in build_queries(META) if x.kind == kind)


def test_build_queries_kinds_and_ids():
    qs = build_queries(META)
    assert [x.kind for x in qs] == ["year", "court", "citation", "bench"]
    assert qs[0].query_id == "c1-year"
    no_judge = CaseMeta("c2", "X v. Y", "(2011) 1 SCC 1", "Court", 2011)
    assert [x.kind for x in build_queries(no_judge)] == ["year", "court", "citation"]


def test_year_scoring():
    assert score_answer(q("year"), "It was decided in 2010.", META) == "correct"
    assert score_answer(q("year"), "Decided in 1999.", META) == "wrong"
    assert score_answer(q("year"), "I am not sure.", META) == "no_answer"


def test_court_and_bench_scoring():
    assert score_answer(q("court"), "The High Court of Beta decided it.", META) == "correct"
    assert score_answer(q("court"), "The Supreme Court did.", META) == "wrong"
    assert score_answer(q("bench"), "Justice Rao wrote it.", META) == "correct"
    assert score_answer(q("bench"), "Justice Mehta wrote it.", META) == "wrong"


def test_citation_scoring_ignores_spacing():
    assert score_answer(q("citation"), "It is (2010)  5 SCC 100.", META) == "correct"
    assert score_answer(q("citation"), "It is (2010) 5 SCC 101.", META) == "wrong"
    assert score_answer(q("citation"), "I do not know.", META) == "no_answer"


def test_bench_without_judge_raises():
    meta = CaseMeta("c2", "X v. Y", "(2011) 1 SCC 1", "Court", 2011)
    bench = build_queries(CaseMeta("c2", "X v. Y", "(2011) 1 SCC 1", "Court", 2011, "J Doe"))[-1]
    with pytest.raises(ValueError):
        score_answer(bench, "anything", meta)


def test_queries_and_score_commands(tmp_path, capsys):
    meta = tmp_path / "meta.jsonl"
    meta.write_text(json.dumps(META.__dict__) + "\n")
    qs = tmp_path / "q.jsonl"
    assert main(["queries", "--meta", str(meta), "--out", str(qs)]) == 0
    answers = tmp_path / "a.jsonl"
    answers.write_text(
        json.dumps({"query_id": "c1-year", "answer": "2010"})
        + "\n"
        + json.dumps({"query_id": "c1-citation", "answer": "(2010) 5 SCC 999"})
        + "\n"
    )
    out = tmp_path / "labels.jsonl"
    assert (
        main(
            [
                "score",
                "--meta",
                str(meta),
                "--queries",
                str(qs),
                "--answers",
                str(answers),
                "--out",
                str(out),
            ]
        )
        == 0
    )
    text = capsys.readouterr().out
    assert "year: n 1 correct 1" in text and "citation: n 1 wrong 1" in text
    labels = [json.loads(x) for x in out.read_text().splitlines()]
    assert {x["label"] for x in labels} == {"correct", "wrong"}
