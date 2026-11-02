from indiacite.cascade import Cascade
from indiacite.citations import normalize_citation
from indiacite.metrics import prf
from indiacite.taxonomy import ErrorType


def evaluate_records(records: list[dict], cascade: Cascade) -> dict:
    rows = []
    for rec in records:
        by_key = {normalize_citation(r.citation.raw): r for r in cascade.check(rec["excerpt"])}
        for c in rec["citations"]:
            r = by_key.get(normalize_citation(c["raw"]))
            rows.append(
                {
                    "truth": c["error_type"],
                    "outcome": r.outcome if r else "not_extracted",
                    "cost": r.cost if r else 0.0,
                    "in_db": c.get("in_database"),
                }
            )
    valid = ErrorType.VALID.value
    y_true = ["error" if r["truth"] != valid else "valid" for r in rows]
    y_pred = ["error" if r["outcome"] == "flag" else "valid" for r in rows]
    prec, rec_, f1 = prf(y_true, y_pred, "error")
    per_type = {}
    for t in sorted({r["truth"] for r in rows} - {valid}):
        sub = [r for r in rows if r["truth"] == t]
        per_type[t] = (sum(1 for r in sub if r["outcome"] == "flag"), len(sub))
    gap = [r for r in rows if r["truth"] == valid and r["in_db"] is False]
    return {
        "n": len(rows),
        "precision": prec,
        "recall": rec_,
        "f1": f1,
        "per_type": per_type,
        "needs_review": sum(1 for r in rows if r["outcome"] == "needs_review"),
        "gap_flagged": sum(1 for r in gap if r["outcome"] == "flag"),
        "gap_total": len(gap),
        "mean_cost": sum(r["cost"] for r in rows) / len(rows) if rows else 0.0,
    }
