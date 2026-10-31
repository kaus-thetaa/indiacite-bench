# Roadmap

About 12 weeks from 2 Nov 2026. Dates are a plan, not a promise.

## Scope v0.1

Label only what can be verified without legal training: nonexistent, citation_mismatch, false_quote, and stale_statute where an official notification gives the date. For real incidents the label comes from the court's finding with the paragraph reference. unsupported_ruling and wrong_pinpoint are included where a court found them, plus a small expert-reviewed set when a reviewer is found.

| week | goal |
|---|---|
| 1 | repo live, OpenReview and ORCID accounts, email the supervisor, apply for free non-commercial database credits, read the six core papers |
| 2 | read the India stubs, freeze taxonomy v1, write the preregistration in `docs/experiment-plan.md` |
| 3 | design reference-based questions from database metadata, pilot 50 queries |
| 4 | generate answers with two or more models, extract citations, build the resolver |
| 5 | label from court findings and lookups, train the structural model M0 |
| 6 | go or no go with the supervisor: enough labelled citations across at least three error types, or scale down |
| 7 | resolver and LLM baselines, cascade |
| 8 | extract hidden states on a free GPU notebook, train probes |
| 9 | leave-one-model-out and cross-field probe analysis |
| 10 | coverage-gap and cost analysis, expert review of the hard subset if a reviewer exists |
| 11 | write the paper |
| 12 | release v0.1, advisor feedback, check venue calls |

Risks: the US authors or vendors cover the same ground, too few real Indian incidents, label quality, database terms, GPU limits.
