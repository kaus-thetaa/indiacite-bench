# Conclusion (state of the research on 1 November 2026)

This is a conclusion about the literature and the plan. No experiment has been run, so there are no results.

## What is established

1. The problem is documented in India from primary sources. In 2026 INSC 668 the Supreme Court set aside tribunal orders that rested on fake precedents, said citing unverified AI material is misconduct, and told the Bar Council of India to frame norms. In 2026 INSC 947 it set aside a Rs 425 crore customs penalty for the same reason and noted draft Regulations for Use of AI in Courts, 2026. In the first judgment the Court said the cause of hallucination is for engineers and scientists, which is an open call for technical work.
2. Of six authorities the Court itself checked in 2026 INSC 668, three were non-existent, one was a wrong citation of an existing judgment, and two had correct citations with non-existent paragraphs. Existence and name checks can catch at most four of the six.
3. The wider literature, read in full, agrees on four things. Models hallucinate heavily on verifiable legal facts and worst at lower courts. Existence and name mismatches are the easy errors and pinpoints and misrepresentation the hard ones. Absence of support is harder to detect than contradiction. Lookup databases are incomplete, so a miss must not be called fake.
4. Cheap detectors exist in other domains: a string-feature classifier (AUC 0.83 to 0.88 for scholarly references), repetition across samples (88.9% against 28.6%), and hidden-state probes that work within a citation field but transfer poorly across fields on at least one large model.

## What is open

1. No independent Indian benchmark of checking methods was found. US benchmarks exist. Falkor-IRAC is a small generation-time guard, and one commercial Indian checker is described only in a vendor-style article.
2. Nobody was found testing database-free, repetition or probe detection on Indian legal citations, or measuring how hallucination varies across Indian court levels.
3. No Indian equivalent of the US citation parser exists. `citations.py` is a first version.

## Conclusion

The topic is worth doing and it is specific enough to be new. The strongest defensible contribution, given a CPU-only laptop, no budget and no law collaborator, is:

1. an open Indian citation parser and a benchmark built from court-labelled real items plus reference-based generations,
2. a cost-aware document-side cascade evaluated by error type, with explicit coverage-gap false alarms,
3. a measurement of how often models fabricate Indian citations by court level, with repetition and structural detectors as database-free baselines.

Probes and confidence features are a stretch goal because they need a model that gets some citations right and a GPU. Judging whether a real case supports a claim is limited to court findings until a law-trained reviewer joins.

## What would change this conclusion

- The database credits are refused or the live API does not resolve citations as the client assumes.
- Fewer than expected of the 16 Indian incidents name individual citations.
- A vendor or research group publishes an Indian benchmark first.
- Small models answer almost nothing correctly, leaving no signal for detectors to learn from.
- The supervisor judges the scope too large for three months.

## Realistic outcome

A reproducible open repository and a workshop-level paper are plausible if reference-based generation and lookups get done. A top-venue main-track paper is unlikely at this scope. The repository, parser and benchmark have value for the CV and for others regardless of venue.
