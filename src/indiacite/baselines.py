from dataclasses import dataclass
from typing import Protocol

from indiacite.citations import Citation, extract_citations, is_plausible


@dataclass
class Resolution:
    found: bool | None
    canonical: str | None = None
    source: str = ""


class Resolver(Protocol):
    def resolve(self, citation: Citation) -> Resolution: ...


class DictResolver:
    def __init__(self, table: dict[str, str]):
        self.table = table

    def resolve(self, citation: Citation) -> Resolution:
        if citation.raw in self.table:
            return Resolution(True, self.table[citation.raw], "dict")
        return Resolution(False, None, "dict")


class FormatChecker:
    name = "format"

    def flag(self, raw: str) -> bool:
        cites = extract_citations(raw)
        return any(not is_plausible(c) for c in cites)


class ExistenceChecker:
    name = "existence"

    def __init__(self, resolver: Resolver, flag_unknown: bool = False):
        self.resolver = resolver
        self.flag_unknown = flag_unknown

    def flag(self, raw: str) -> bool:
        for c in extract_citations(raw):
            res = self.resolver.resolve(c)
            # not found is weak evidence when coverage is partial
            if res.found is False or (res.found is None and self.flag_unknown):
                return True
        return False
