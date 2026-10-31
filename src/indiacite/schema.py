from indiacite.taxonomy import ErrorType

MAX_EXCERPT_CHARS = 600
SOURCES = {"real_incident", "llm_generated", "injected", "synthetic"}
VALID_TYPES = {t.value for t in ErrorType}


def validate_record(rec: dict) -> list[str]:
    errs = []
    for key in ("id", "source", "excerpt", "citations"):
        if key not in rec:
            errs.append(f"missing field {key}")
    if errs:
        return errs
    if not isinstance(rec["id"], str) or not rec["id"].strip():
        errs.append("id must be a non empty string")
    if rec["source"] not in SOURCES:
        errs.append(f"source must be one of {sorted(SOURCES)}")
    excerpt = rec["excerpt"]
    if not isinstance(excerpt, str) or not excerpt.strip():
        errs.append("excerpt must be a non empty string")
        excerpt = ""
    elif len(excerpt) > MAX_EXCERPT_CHARS:
        errs.append(f"excerpt longer than {MAX_EXCERPT_CHARS} chars")
    cites = rec["citations"]
    if not isinstance(cites, list) or not cites:
        errs.append("citations must be a non empty list")
        cites = []
    for i, c in enumerate(cites):
        errs.extend(_validate_citation(c, i, excerpt))
    if rec.get("source") == "real_incident":
        if not rec.get("incident_ref"):
            errs.append("real_incident needs incident_ref")
        if rec.get("anonymized") is not True:
            errs.append("real_incident needs anonymized true")
    return errs


def _validate_citation(c: dict, i: int, excerpt: str) -> list[str]:
    where = f"citations[{i}]"
    errs = []
    raw = c.get("raw")
    if not isinstance(raw, str) or not raw:
        return [f"{where} missing raw"]
    if excerpt and raw not in excerpt:
        errs.append(f"{where} raw not found in excerpt")
    etype = c.get("error_type")
    if etype not in VALID_TYPES:
        errs.append(f"{where} bad error_type {etype}")
    elif etype != ErrorType.VALID.value and not c.get("evidence"):
        errs.append(f"{where} needs evidence for {etype}")
    for j, lab in enumerate(c.get("labels", [])):
        if lab.get("error_type") not in VALID_TYPES or not lab.get("annotator"):
            errs.append(f"{where} labels[{j}] malformed")
    return errs
