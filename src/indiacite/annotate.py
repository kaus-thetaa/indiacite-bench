import csv
import json

from indiacite.citations import extract_citations
from indiacite.metrics import cohen_kappa
from indiacite.schema import MAX_EXCERPT_CHARS, VALID_TYPES

COLUMNS = ["id", "excerpt", "raw", "error_type", "evidence"]


def build_template(generations: list[dict], out_path: str) -> int:
    n = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for g in generations:
            answer = g["answer"][:MAX_EXCERPT_CHARS]
            for i, c in enumerate(extract_citations(answer)):
                w.writerow(
                    {
                        "id": f"{g['query_id']}#{i}",
                        "excerpt": answer,
                        "raw": c.raw,
                        "error_type": "",
                        "evidence": "",
                    }
                )
                n += 1
    return n


def read_annotations(path: str) -> dict[str, dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def merge_annotations(files: dict[str, str], source: str = "llm_generated"):
    tables = {name: read_annotations(p) for name, p in files.items()}
    ids = sorted(set.intersection(*(set(t) for t in tables.values())))
    records, disputes = [], []
    for rid in ids:
        rows = {name: t[rid] for name, t in tables.items()}
        labels = {name: r["error_type"].strip() for name, r in rows.items()}
        bad = [v for v in labels.values() if v not in VALID_TYPES]
        first = next(iter(rows.values()))
        if bad or len(set(labels.values())) > 1:
            disputes.append(
                {"id": rid, "raw": first["raw"], **{f"label_{k}": v for k, v in labels.items()}}
            )
            continue
        label = next(iter(labels.values()))
        evidence = " | ".join(r["evidence"].strip() for r in rows.values() if r["evidence"].strip())
        cite = {
            "raw": first["raw"],
            "error_type": label,
            "labels": [{"annotator": k, "error_type": v} for k, v in labels.items()],
        }
        if evidence:
            cite["evidence"] = evidence
        records.append(
            {"id": rid, "source": source, "excerpt": first["excerpt"], "citations": [cite]}
        )
    return records, disputes


def write_jsonl(rows: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def pairwise_kappa(path_a: str, path_b: str) -> tuple[float, int]:
    a, b = read_annotations(path_a), read_annotations(path_b)
    ids = sorted(set(a) & set(b))
    ids = [i for i in ids if a[i]["error_type"].strip() and b[i]["error_type"].strip()]
    if not ids:
        raise ValueError("no commonly labelled rows")
    return cohen_kappa(
        [a[i]["error_type"].strip() for i in ids], [b[i]["error_type"].strip() for i in ids]
    ), len(ids)
