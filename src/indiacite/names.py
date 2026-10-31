import difflib
import re

_VS = re.compile(r"\b(?:versus|vs|v)\b\.?", re.I)
_NOISE = re.compile(r"[^a-z0-9 ]")


def normalize_name(name: str) -> str:
    s = _VS.sub(" v ", name.lower())
    s = _NOISE.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def name_similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, normalize_name(a), normalize_name(b)).ratio()


def names_match(a: str, b: str, threshold: float = 0.8) -> bool:
    return name_similarity(a, b) >= threshold
