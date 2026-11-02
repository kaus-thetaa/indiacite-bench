import pytest

from indiacite.cascade import Cascade, ScoreStage
from indiacite.citations import extract_citations
from indiacite.repetition import RepetitionScorer, citation_agreement

ANSWERS = [
    "See Alpha v. Beta (2010) 5 SCC 100 and Gamma v. Delta (2011) 6 SCC 200.",
    "As in Alpha v. Beta (2010) 5 SCC 100 and Eta v. Theta (2012) 7 SCC 300.",
    "Alpha v. Beta (2010) 5 SCC 100 is the leading case.",
]


def test_agreement_fractions():
    ag = citation_agreement(ANSWERS)
    assert ag["(2010)5scc100"] == 1.0
    assert ag["(2011)6scc200"] == pytest.approx(1 / 3)


def test_empty_answers_rejected():
    with pytest.raises(ValueError):
        citation_agreement([])


def test_scorer_low_for_stable_high_for_one_off():
    scorer = RepetitionScorer(ANSWERS)
    stable = extract_citations("(2010) 5 SCC 100")[0]
    oneoff = extract_citations("(2011) 6 SCC 200")[0]
    unseen = extract_citations("(2013) 8 SCC 400")[0]
    assert scorer(stable) == 0.0
    assert scorer(oneoff) == pytest.approx(2 / 3)
    assert scorer(unseen) == 1.0


def test_works_as_cascade_stage():
    stage = ScoreStage(
        "repetition", RepetitionScorer(ANSWERS), cost=3.0, flag_above=0.6, pass_below=0.1
    )
    text = "Alpha v. Beta (2010) 5 SCC 100 and Gamma v. Delta (2011) 6 SCC 200."
    out = {r.citation.raw: r.outcome for r in Cascade([stage]).check(text)}
    assert out["(2010) 5 SCC 100"] == "pass"
    assert out["(2011) 6 SCC 200"] == "flag"
