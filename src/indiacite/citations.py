import datetime
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Citation:
    raw: str
    scheme: str
    year: int
    start: int
    end: int


_PATTERNS = [
    (
        "scc",
        re.compile(
            r"\((?P<year>\d{4})\)\s+(?P<vol>\d{1,3})\s+SCC"
            r"(?:\s+\((?:Cri|L&S|Civ|Tax|Supp)\))?\s+(?P<page>\d{1,4})"
        ),
    ),
    (
        "scc",
        re.compile(r"\b(?P<year>\d{4})\s+\((?P<vol>\d{1,3})\)\s+SCC\s+(?P<page>\d{1,4})\b"),
    ),
    (
        "air",
        re.compile(
            r"\bAIR\s+(?P<year>\d{4})\s+(?P<court>[A-Z][A-Za-z&]{1,5})\s+(?P<page>\d{1,4})\b"
        ),
    ),
    ("insc", re.compile(r"\b(?P<year>\d{4})\s+INSC\s+(?P<num>\d{1,4})\b")),
    (
        "scr",
        re.compile(r"\[(?P<year>\d{4})\]\s+(?:Supp\s+)?\(?\d{1,2}\)?\s+SCR\s+(?P<page>\d{1,4})"),
    ),
    (
        "scc_online",
        re.compile(
            r"\b(?P<year>\d{4})\s+SCC\s+OnLine\s+(?P<court>[A-Za-z&]{2,6})\s+(?P<num>\d{1,5})\b"
        ),
    ),
]

# earliest plausible year per scheme
# insc start year needs checking with a legal collaborator
MIN_YEAR = {"scc": 1969, "air": 1914, "insc": 2023, "scr": 1950, "scc_online": 1900}


def extract_citations(text: str) -> list[Citation]:
    found = []
    for scheme, pattern in _PATTERNS:
        for m in pattern.finditer(text):
            found.append(Citation(m.group(0), scheme, int(m.group("year")), m.start(), m.end()))
    found.sort(key=lambda c: (c.start, -(c.end - c.start)))
    kept = []
    last_end = -1
    for c in found:
        if c.start >= last_end:
            kept.append(c)
            last_end = c.end
    return kept


def is_plausible(c: Citation, max_year: int | None = None) -> bool:
    top = max_year if max_year is not None else datetime.date.today().year
    return MIN_YEAR[c.scheme] <= c.year <= top


_SEP = re.compile(r"\s+(?:v\.?|vs\.?|versus)\s+", re.I)
_LEAD_STOP = {"In", "See", "As", "Held", "Cf", "Also", "Reliance", "Following"}
_CONNECT = {"of", "and", "the", "for", "&", "de", "ors", "ors.", "anr", "anr."}


def _is_name_word(w: str) -> bool:
    return w[:1].isupper() or w.lower() in _CONNECT


def extract_case_name(text: str, c: Citation, window: int = 140) -> str | None:
    before = text[max(0, c.start - window) : c.start].rstrip(" ,([")
    seps = list(_SEP.finditer(before))
    if not seps:
        return None
    m = seps[-1]
    left = []
    for w in reversed(before[: m.start()].split()):
        if not _is_name_word(w):
            break
        left.append(w)
    left.reverse()
    while left and (left[0] in _LEAD_STOP or left[0][:1].islower()):
        left.pop(0)
    right = []
    for w in before[m.end() :].split():
        if not _is_name_word(w):
            break
        right.append(w)
    if not left or not right:
        return None
    return " ".join(left) + " v. " + " ".join(right)


def normalize_citation(raw: str) -> str:
    return re.sub(r"\s+", "", raw).lower()


def canonical_key(raw: str):
    cites = extract_citations(raw)
    if not cites:
        return None
    c = cites[0]
    nums = tuple(int(x) for x in re.findall(r"\d+", c.raw))
    letters = tuple(re.findall(r"[A-Za-z]+", c.raw))
    if c.scheme == "scc":
        letters = ()
    return (c.scheme, nums, letters)
