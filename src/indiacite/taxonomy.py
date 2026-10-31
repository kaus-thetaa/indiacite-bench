from enum import Enum


class ErrorType(str, Enum):
    VALID = "valid"
    NONEXISTENT = "nonexistent"
    CITATION_MISMATCH = "citation_mismatch"
    WRONG_PINPOINT = "wrong_pinpoint"
    FALSE_QUOTE = "false_quote"
    UNSUPPORTED_RULING = "unsupported_ruling"
    STALE_STATUTE = "stale_statute"


DEFINITIONS = {
    ErrorType.VALID: "authority exists and supports the use made of it",
    ErrorType.NONEXISTENT: "no such judgment or provision exists",
    ErrorType.CITATION_MISMATCH: "real case but wrong name reporter or neutral citation",
    ErrorType.WRONG_PINPOINT: "real case but cited page or paragraph does not hold the point",
    ErrorType.FALSE_QUOTE: "quoted words do not appear in the cited authority",
    ErrorType.UNSUPPORTED_RULING: "real case that does not say what it is cited for",
    ErrorType.STALE_STATUTE: "provision repealed replaced or renumbered at the relevant date",
}

ERROR_TYPES = [t for t in ErrorType if t is not ErrorType.VALID]

# crosswalk to the incident database categories
CHARLOTIN_MAP = {
    ("fabricated", "case law"): ErrorType.NONEXISTENT,
    ("fabricated", "legal norm"): ErrorType.NONEXISTENT,
    ("false quotes", "case law"): ErrorType.FALSE_QUOTE,
    ("false quotes", "legal norm"): ErrorType.FALSE_QUOTE,
    ("misrepresented", "case law"): ErrorType.UNSUPPORTED_RULING,
    ("misrepresented", "legal norm"): ErrorType.UNSUPPORTED_RULING,
    ("outdated advice", "repealed law"): ErrorType.STALE_STATUTE,
}

MISMATCH_HINTS = (
    "corresponds to",
    "belongs to",
    "instead refer",
    "led to",
    "actually refer",
    "different case",
    "unrelated case",
)


def classify_item(category: str, subcategory: str, description: str):
    key = (category.strip().lower(), subcategory.strip().lower())
    base = CHARLOTIN_MAP.get(key)
    if base is None:
        return None, False
    text = description.lower()
    if base is ErrorType.NONEXISTENT and any(h in text for h in MISMATCH_HINTS):
        return ErrorType.CITATION_MISMATCH, False
    return base, base is not ErrorType.NONEXISTENT
