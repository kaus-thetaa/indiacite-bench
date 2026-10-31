import csv
import json
from dataclasses import dataclass

from indiacite.taxonomy import classify_item

BASE_URL = "https://www.damiencharlotin.com"
ATTRIBUTION = "AI Hallucination Cases Database, Damien Charlotin, CC BY 4.0"


@dataclass(frozen=True)
class Item:
    category: str
    subcategory: str
    description: str


def split_items(cell: str) -> list[Item]:
    items = []
    for chunk in cell.split(" || "):
        chunk = chunk.strip()
        if not chunk:
            continue
        head, _, desc = chunk.partition(" | ")
        cat, _, sub = head.partition(": ")
        items.append(Item(cat.strip(), sub.strip(), desc.strip()))
    return items


def read_rows(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rows_for_country(rows: list[dict], country: str = "India") -> list[dict]:
    want = country.lower()
    out = []
    for r in rows:
        states = [s.strip().lower() for s in r.get("State(s)", "").replace(";", ",").split(",")]
        if want in states:
            out.append(r)
    return out


def find_ref(row: dict) -> str:
    # the real csv puts the document path under source and a site name under pointer
    for key in ("Source", "Pointer"):
        val = row.get(key, "").strip()
        if val.startswith("/documents/"):
            return BASE_URL + val
        if val.startswith("http"):
            return val
    return ""


def to_stub(row: dict, idx: int) -> dict:
    items = []
    for it in split_items(row.get("Hallucination Items", "")):
        etype, confident = classify_item(it.category, it.subcategory, it.description)
        items.append(
            {
                "category": it.category,
                "subcategory": it.subcategory,
                "suggested_type": etype.value if etype else None,
                "confident": confident,
                "summary": it.description,
            }
        )
    ref = find_ref(row)
    return {
        "stub_id": f"stub-{idx:03d}",
        "incident_ref": ref,
        "court": row.get("Court", ""),
        "date": row.get("Date", ""),
        "party_role": row.get("Party(ies)", ""),
        "items": items,
        "status": "todo",
        "attribution": ATTRIBUTION,
    }


def write_stubs(rows: list[dict], out_path: str) -> int:
    with open(out_path, "w", encoding="utf-8") as f:
        for i, r in enumerate(rows, 1):
            f.write(json.dumps(to_stub(r, i), ensure_ascii=False) + "\n")
    return len(rows)
