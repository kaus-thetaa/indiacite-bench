import re
from dataclasses import dataclass

from indiacite.citations import extract_citations

QUERY_KINDS = ("year", "court", "citation", "bench")


@dataclass(frozen=True)
class CaseMeta:
    case_id: str
    name: str
    citation: str
    court: str
    year: int
    judge: str | None = None


@dataclass(frozen=True)
class Query:
    query_id: str
    case_id: str
    kind: str
    prompt: str


def build_queries(meta: CaseMeta) -> list[Query]:
    qs = [
        ("year", f"In which year was {meta.name} decided? Answer in one sentence."),
        ("court", f"Which court decided {meta.name}? Answer in one sentence."),
        (
            "citation",
            f"Give the full law report citation for {meta.name}. Answer in one sentence.",
        ),
    ]
    if meta.judge:
        qs.append(
            ("bench", f"Which judge wrote the judgment in {meta.name}? Answer in one sentence.")
        )
    return [Query(f"{meta.case_id}-{k}", meta.case_id, k, p) for k, p in qs]


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", s).lower()


def score_answer(q: Query, answer: str, meta: CaseMeta) -> str:
    if q.kind == "year":
        years = re.findall(r"\b(1[89]\d{2}|20\d{2})\b", answer)
        if not years:
            return "no_answer"
        return "correct" if str(meta.year) in years else "wrong"
    if q.kind == "court":
        text = _norm(answer)
        if not text:
            return "no_answer"
        return "correct" if _norm(meta.court) in text else "wrong"
    if q.kind == "citation":
        cites = extract_citations(answer)
        if not cites:
            return "no_answer"
        gold = _norm(meta.citation)
        return "correct" if any(_norm(c.raw) == gold for c in cites) else "wrong"
    if q.kind == "bench":
        if not meta.judge:
            raise ValueError("no judge in metadata")
        if not answer.strip():
            return "no_answer"
        surname = meta.judge.split()[-1].lower().strip(".,")
        return "correct" if surname in answer.lower() else "wrong"
    raise ValueError(f"unknown kind {q.kind}")
