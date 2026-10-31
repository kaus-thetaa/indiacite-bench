from indiacite.baselines import DictResolver
from indiacite.cascade import Cascade, FormatStage, ResolverStage, ScoreStage

TEXT = (
    "Relied on Alpha Traders v. State of Beta (2010) 5 SCC 100 and "
    "Gamma Mills v. Delta Board (1900) 99 SCC 999 and "
    "Epsilon v. Zeta (2011) 6 SCC 200 and Omega v. Sigma (2012) 7 SCC 300."
)
KNOWN = {
    "(2010) 5 SCC 100": "Alpha Traders v. State of Beta",
    "(2011) 6 SCC 200": "Eta v. Theta",
}


def by_raw(reports):
    return {r.citation.raw: r for r in reports}


def test_format_then_resolver():
    cascade = Cascade([FormatStage(), ResolverStage(DictResolver(KNOWN))])
    out = by_raw(cascade.check(TEXT))
    assert out["(1900) 99 SCC 999"].outcome == "flag"
    assert out["(1900) 99 SCC 999"].decided_by == "format"
    assert out["(2010) 5 SCC 100"].outcome == "pass"
    assert out["(2011) 6 SCC 200"].error_type == "citation_mismatch"
    assert out["(2012) 7 SCC 300"].outcome == "needs_review"


def test_not_found_is_not_flagged_by_default():
    out = by_raw(Cascade([ResolverStage(DictResolver({}))]).check(TEXT))
    assert all(r.outcome == "needs_review" for r in out.values())


def test_flag_not_found_option():
    stage = ResolverStage(DictResolver({}), flag_not_found=True)
    out = by_raw(Cascade([stage]).check(TEXT))
    assert all(r.outcome == "flag" for r in out.values())


def test_cost_accumulates_only_until_decision():
    cascade = Cascade([FormatStage(), ResolverStage(DictResolver(KNOWN))])
    out = by_raw(cascade.check(TEXT))
    assert out["(1900) 99 SCC 999"].cost == 0.0
    assert out["(2010) 5 SCC 100"].cost == 1.0


def test_score_stage_abstain_band():
    scores = {"(2010) 5 SCC 100": 0.05, "(2011) 6 SCC 200": 0.5, "(2012) 7 SCC 300": 0.95}
    stage = ScoreStage("probe", lambda c, ctx: scores.get(c.raw, 0.5), cost=2.0)
    out = by_raw(Cascade([stage]).check(TEXT))
    assert out["(2010) 5 SCC 100"].outcome == "pass"
    assert out["(2011) 6 SCC 200"].outcome == "needs_review"
    assert out["(2012) 7 SCC 300"].outcome == "flag"
