# Roadmap

About 12 weeks from 2 Nov 2026. Dates are a plan, not a promise.

## Scope v0.1

Core: Indian citation parser, benchmark from three data sources, document-side cascade, coverage-gap analysis, a reference-based generation study. Stretch: probes and confidence features, which need a model that gets some citations right and a GPU. Out until a reviewer is found: judgements on whether a real case supports a claim, beyond what courts have already found.

Compute: the laptop is CPU-only. Start with small models for plumbing. Measure the correct-answer rate before investing in probes. Ask the supervisor about lab compute and check free cloud notebooks.

| week | goal |
|---|---|
| 1 | repo live, OpenReview and ORCID accounts, email the supervisor, apply for free non-commercial database credits, collect 30 to 50 case records by hand as a fallback, read the core papers |
| 2 | read the India stubs, freeze taxonomy v1, finish the preregistration in `docs/experiment-plan.md` |
| 3 | pilot 50 reference questions on one small model, measure time and the correct-answer rate, go or no go for probes |
| 4 | generate with two or more models, extract citations, first live database test |
| 5 | label from court findings and lookups, two annotators on a sample and report kappa, train M0 |
| 6 | go or no go with the supervisor: enough labelled citations across at least three error types, or scale down |
| 7 | resolver and repetition baselines, cascade, coverage-gap analysis |
| 8 | optional: probes on a GPU if available |
| 9 | analysis by court level, error type and model |
| 10 | cost curves, error analysis, expert review of the hard subset if a reviewer exists |
| 11 | write the paper |
| 12 | release v0.1, advisor feedback, check venue calls |

Risks: a vendor or US group covers the same ground, too few real Indian incidents, label quality, database terms and untested API, no GPU.
