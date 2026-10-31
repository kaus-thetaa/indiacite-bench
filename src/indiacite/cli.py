import argparse
import json
import sys
from collections import Counter

from indiacite.baselines import DictResolver, FormatChecker
from indiacite.cascade import Cascade, FormatStage, ResolverStage
from indiacite.charlotin import read_rows, rows_for_country, write_stubs
from indiacite.metrics import prf
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
    e.set_defaults(fn=cmd_eval)
    k = sub.add_parser("check")
    k.add_argument("path")
    k.add_argument("--known")
    k.set_defaults(fn=cmd_check)
    s = sub.add_parser("stubs")
    s.add_argument("--csv", required=True)
    s.add_argument("--country", default="India")
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_stubs)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
