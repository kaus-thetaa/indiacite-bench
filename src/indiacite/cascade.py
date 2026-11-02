from dataclasses import dataclass
from enum import Enum
from typing import Callable, Protocol

from indiacite.baselines import Resolver
from indiacite.citations import Citation, extract_case_name, extract_citations, is_plausible
from indiacite.names import names_match


class Verdict(str, Enum):
    FLAG = "flag"
    PASS = "pass"
    UNKNOWN = "unknown"


@dataclass
class StageResult:
    verdict: Verdict
    reason: str = ""
    error_type: str | None = None
    score: float | None = None


class Stage(Protocol):
    name: str
    cost: float

    def run(self, citation: Citation, context: str) -> StageResult: ...


@dataclass
class Report:
    citation: Citation
    case_name: str | None
    outcome: str
    decided_by: str | None
    reason: str
    error_type: str | None
    cost: float


class FormatStage:
    name = "format"
    cost = 0.0

    def run(self, citation: Citation, context: str) -> StageResult:
        if not is_plausible(citation):
            return StageResult(
                Verdict.FLAG, "year outside the range for this series", "nonexistent"
            )
        return StageResult(Verdict.UNKNOWN, "format plausible")


class ResolverStage:
    name = "resolver"
    cost = 1.0

    def __init__(self, resolver: Resolver, flag_not_found: bool = False):
        self.resolver = resolver
        self.flag_not_found = flag_not_found

    def run(self, citation: Citation, context: str) -> StageResult:
        cited = extract_case_name(context, citation)
        res = self.resolver.resolve(citation, cited)
        if res.found is True:
            if res.citation_verified is True:
                return StageResult(Verdict.PASS, "found and citation confirmed")
            if cited and res.canonical:
                if names_match(cited, res.canonical):
                    return StageResult(Verdict.PASS, "found and name matches")
                return StageResult(
                    Verdict.FLAG, f"name differs from {res.canonical}", "citation_mismatch"
                )
            return StageResult(Verdict.UNKNOWN, "found but name not checked")
        if res.found is False:
            if self.flag_not_found:
                return StageResult(Verdict.FLAG, "not found", "nonexistent")
            return StageResult(Verdict.UNKNOWN, "not found and coverage may be partial")
        return StageResult(Verdict.UNKNOWN, "lookup unavailable")


class ScoreStage:
    def __init__(
        self,
        name: str,
        scorer: Callable[[Citation, str], float],
        cost: float,
        flag_above: float = 0.8,
        pass_below: float = 0.2,
    ):
        self.name = name
        self.cost = cost
        self.scorer = scorer
        self.flag_above = flag_above
        self.pass_below = pass_below

    def run(self, citation: Citation, context: str) -> StageResult:
        s = self.scorer(citation, context)
        if s >= self.flag_above:
            return StageResult(Verdict.FLAG, f"score {s:.2f}", None, s)
        if s <= self.pass_below:
            return StageResult(Verdict.PASS, f"score {s:.2f}", None, s)
        return StageResult(Verdict.UNKNOWN, f"score {s:.2f} in abstain band", None, s)


class Cascade:
    def __init__(self, stages: list[Stage]):
        self.stages = stages

    def check(self, text: str) -> list[Report]:
        reports = []
        for c in extract_citations(text):
            name = extract_case_name(text, c)
            spent = 0.0
            final = None
            decided = None
            for st in self.stages:
                spent += st.cost
                res = st.run(c, text)
                if res.verdict is not Verdict.UNKNOWN:
                    final, decided = res, st.name
                    break
            if final is None:
                reports.append(
                    Report(c, name, "needs_review", None, "no stage decided", None, spent)
                )
            else:
                outcome = "flag" if final.verdict is Verdict.FLAG else "pass"
                reports.append(
                    Report(c, name, outcome, decided, final.reason, final.error_type, spent)
                )
        return reports
