from collections import Counter

from indiacite.citations import Citation, extract_citations, normalize_citation


def citation_agreement(answers: list[str]) -> dict[str, float]:
    if not answers:
        raise ValueError("need at least one answer")
    counts: Counter = Counter()
    for a in answers:
        counts.update({normalize_citation(c.raw) for c in extract_citations(a)})
    return {k: v / len(answers) for k, v in counts.items()}


class RepetitionScorer:
    def __init__(self, answers: list[str]):
        self.agreement = citation_agreement(answers)

    def __call__(self, citation: Citation, context: str = "") -> float:
        return 1.0 - self.agreement.get(normalize_citation(citation.raw), 0.0)
