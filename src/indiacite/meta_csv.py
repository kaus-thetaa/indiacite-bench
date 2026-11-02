import csv
import json
from dataclasses import asdict

from indiacite.queries import CaseMeta

REQUIRED = ("case_id", "name", "citation", "court", "year")


def read_meta_csv(path: str) -> list[CaseMeta]:
    out = []
    seen = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing columns {missing}")
        for n, row in enumerate(reader, start=2):
            for col in REQUIRED:
                if not (row.get(col) or "").strip():
                    raise ValueError(f"row {n}: empty {col}")
            cid = row["case_id"].strip()
            if cid in seen:
                raise ValueError(f"row {n}: duplicate case_id {cid}")
            seen.add(cid)
            try:
                year = int(row["year"])
            except ValueError as e:
                raise ValueError(f"row {n}: year must be a number") from e
            judge = (row.get("judge") or "").strip() or None
            out.append(
                CaseMeta(
                    cid,
                    row["name"].strip(),
                    row["citation"].strip(),
                    row["court"].strip(),
                    year,
                    judge,
                )
            )
    return out


def write_meta_jsonl(metas: list[CaseMeta], path: str) -> int:
    with open(path, "w", encoding="utf-8") as f:
        for m in metas:
            f.write(json.dumps(asdict(m), ensure_ascii=False) + "\n")
    return len(metas)
