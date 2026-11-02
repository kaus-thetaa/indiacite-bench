import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict

from indiacite.annotate import (
    build_template,
    merge_annotations,
    pairwise_kappa,
    write_jsonl,
)
from indiacite.baselines import DictResolver, FormatChecker
from indiacite.cascade import Cascade, FormatStage, ResolverStage
from indiacite.charlotin import read_rows, rows_for_country, write_stubs
from indiacite.evaluation import evaluate_records
from indiacite.meta_csv import read_meta_csv, write_meta_jsonl
from indiacite.metrics import prf
from indiacite.queries import CaseMeta, Query, build_queries, score_answer
from indiacite.report import render_markdown
from indiacite.schema import validate_record
from indiacite.taxonomy import ErrorType


def load_jsonl(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def cmd_validate(args) -> int:
    records = load_jsonl(args.path)
    problems = 0
    seen = set()
    for rec in records:
        rid = rec.get("id", "?")
        errs = validate_record(rec)
        if rid in seen:
            errs.append("duplicate id")
        seen.add(rid)
        for e in errs:
            print(f"{rid}: {e}")
        problems += len(errs)
    types = Counter(c.get("error_type") for r in records for c in r.get("citations", []))
    sources = Counter(r.get("source") for r in records)
    print(f"records {len(records)} problems {problems}")
    print(f"sources {dict(sources)}")
    print(f"error types {dict(types)}")
    return 1 if problems else 0


def cmd_eval(args) -> int:
    records = load_jsonl(args.path)
    if args.known or args.flag_not_found:
        stages = [FormatStage()]
        table = {}
        if args.known:
            with open(args.known, encoding="utf-8") as f:
                table = json.load(f)
        stages.append(ResolverStage(DictResolver(table), flag_not_found=args.flag_not_found))
        res = evaluate_records(records, Cascade(stages))
        print(
            f"cascade n {res['n']} precision {res['precision']:.2f} "
            f"recall {res['recall']:.2f} f1 {res['f1']:.2f} "
            f"needs_review {res['needs_review']} mean_cost {res['mean_cost']:.2f}"
        )
        for kind, (hit, total) in res["per_type"].items():
            print(f"  recall {kind}: {hit}/{total}")
        print(f"  coverage gap false alarms: {res['gap_flagged']}/{res['gap_total']}")
        print("note: results on synthetic or demonstration data are not findings")
        return 0
    checker = FormatChecker()
    y_true, y_pred, kinds = [], [], []
    for rec in records:
        for c in rec["citations"]:
            truth = c["error_type"]
            y_true.append("error" if truth != ErrorType.VALID.value else "valid")
            y_pred.append("error" if checker.flag(c["raw"]) else "valid")
            kinds.append(truth)
    p, r, f = prf(y_true, y_pred, "error")
    print(f"baseline {checker.name} n {len(y_true)} precision {p:.2f} recall {r:.2f} f1 {f:.2f}")
    for kind in sorted(set(kinds) - {ErrorType.VALID.value}):
        hits = [yp for k, yp in zip(kinds, y_pred, strict=True) if k == kind]
        print(f"  recall {kind}: {hits.count('error')}/{len(hits)}")
    print("note: sample data is synthetic so scores are not results")
    return 0


def cmd_check(args) -> int:
    with open(args.path, encoding="utf-8") as f:
        text = f.read()
    stages = [FormatStage()]
    if args.known:
        with open(args.known, encoding="utf-8") as f:
            stages.append(ResolverStage(DictResolver(json.load(f))))
    reports = Cascade(stages).check(text)
    for r in reports:
        print(
            f"[{r.outcome}] {r.citation.raw} | {r.case_name or '-'} | "
            f"{r.decided_by or '-'} | {r.error_type or '-'} | {r.reason}"
        )
    print(f"citations {len(reports)} cost {sum(r.cost for r in reports):.1f}")
    print("note: needs_review means a human should check and pass is not a certificate")
    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(render_markdown(reports))
    return 0


def cmd_queries(args) -> int:
    metas = [CaseMeta(**m) for m in load_jsonl(args.meta)]
    n = 0
    with open(args.out, "w", encoding="utf-8") as f:
        for m in metas:
            for q in build_queries(m):
                f.write(json.dumps(asdict(q), ensure_ascii=False) + "\n")
                n += 1
    print(f"wrote {n} queries to {args.out}")
    return 0


def cmd_score(args) -> int:
    metas = {m["case_id"]: CaseMeta(**m) for m in load_jsonl(args.meta)}
    queries = {q["query_id"]: q for q in load_jsonl(args.queries)}
    counts: dict[str, dict[str, int]] = {}
    labelled = []
    for a in load_jsonl(args.answers):
        qd = queries[a["query_id"]]
        label = score_answer(Query(**qd), a["answer"], metas[qd["case_id"]])
        counts.setdefault(qd["kind"], {}).setdefault(label, 0)
        counts[qd["kind"]][label] += 1
        labelled.append(
            {
                "query_id": qd["query_id"],
                "case_id": qd["case_id"],
                "kind": qd["kind"],
                "label": label,
            }
        )
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for row in labelled:
                f.write(json.dumps(row) + "\n")
    for kind, c in sorted(counts.items()):
        total = sum(c.values())
        print(f"{kind}: n {total} " + " ".join(f"{k} {v}" for k, v in sorted(c.items())))
    return 0


def cmd_meta(args) -> int:
    n = write_meta_jsonl(read_meta_csv(args.csv), args.out)
    print(f"wrote {n} cases to {args.out}")
    return 0


def cmd_annotate_template(args) -> int:
    n = build_template(load_jsonl(args.generations), args.out)
    print(f"wrote {n} rows to {args.out}")
    return 0


def cmd_annotate_merge(args) -> int:
    files = dict(a.split("=", 1) for a in args.annotator)
    records, disputes = merge_annotations(files, args.source)
    write_jsonl(records, args.out)
    if args.disputes:
        write_jsonl(disputes, args.disputes)
    print(f"agreed {len(records)} disputed {len(disputes)}")
    return 0


def cmd_agreement(args) -> int:
    kappa, n = pairwise_kappa(args.a, args.b)
    print(f"cohen kappa {kappa:.3f} on {n} rows")
    return 0


def cmd_stubs(args) -> int:
    rows = rows_for_country(read_rows(args.csv), args.country)
    n = write_stubs(rows, args.out)
    print(f"wrote {n} stubs to {args.out}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="indiacite")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("path")
    v.set_defaults(fn=cmd_validate)
    e = sub.add_parser("eval")
    e.add_argument("path")
    e.add_argument("--known")
    e.add_argument("--flag-not-found", action="store_true")
    e.set_defaults(fn=cmd_eval)
    k = sub.add_parser("check")
    k.add_argument("path")
    k.add_argument("--known")
    k.add_argument("--report")
    k.set_defaults(fn=cmd_check)
    qp = sub.add_parser("queries")
    qp.add_argument("--meta", required=True)
    qp.add_argument("--out", required=True)
    qp.set_defaults(fn=cmd_queries)
    sc = sub.add_parser("score")
    sc.add_argument("--meta", required=True)
    sc.add_argument("--queries", required=True)
    sc.add_argument("--answers", required=True)
    sc.add_argument("--out")
    sc.set_defaults(fn=cmd_score)
    mt = sub.add_parser("meta")
    mt.add_argument("--csv", required=True)
    mt.add_argument("--out", required=True)
    mt.set_defaults(fn=cmd_meta)
    at = sub.add_parser("annotate-template")
    at.add_argument("--generations", required=True)
    at.add_argument("--out", required=True)
    at.set_defaults(fn=cmd_annotate_template)
    am = sub.add_parser("annotate-merge")
    am.add_argument("--annotator", action="append", required=True, help="name=path")
    am.add_argument("--out", required=True)
    am.add_argument("--disputes")
    am.add_argument("--source", default="llm_generated")
    am.set_defaults(fn=cmd_annotate_merge)
    ag = sub.add_parser("agreement")
    ag.add_argument("--a", required=True)
    ag.add_argument("--b", required=True)
    ag.set_defaults(fn=cmd_agreement)
    s = sub.add_parser("stubs")
    s.add_argument("--csv", required=True)
    s.add_argument("--country", default="India")
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_stubs)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
