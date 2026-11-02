# indiacite-bench

Research code and benchmark for detecting fabricated and unsupported case citations in Indian legal text.

Status: pre-alpha. No results yet. Sample data is synthetic and exists only to test the pipeline.

## Research question

Courts in India have begun sanctioning unverified AI-generated citations. Existing benchmarks cover US law. We study how well different checking methods work on Indian law, what they cost, and where they fail. The computational questions:

1. How often do models fabricate Indian citations, and how does it vary by court level?
2. Can database-free detectors (structural model, repetition across samples) flag fabricated citations?
3. How do lookup, retrieval-backed checking and probes trade off precision, recall and cost, and how badly does incomplete database coverage inflate false alarms?
4. Which errors do existence and name checks miss?

See `docs/research-questions.md` and `docs/methods.md`.

## Error types

| type | meaning |
|---|---|
| nonexistent | no such judgment or provision |
| citation_mismatch | real case with wrong name, reporter or neutral citation |
| wrong_pinpoint | real case but the page or paragraph does not hold the point |
| false_quote | quoted words are not in the authority |
| unsupported_ruling | real case that does not say what it is cited for |
| stale_statute | repealed or replaced provision |

## What exists now

- Indian citation parser for SCC (both formats), AIR, INSC, SCR and SCC OnLine, with normalisation and canonical keys
- case name extraction and fuzzy name matching
- court-labelled real items from 2026 INSC 668 in `data/real_incidents/`
- record schema, validator and metrics (precision, recall, kappa, AUROC, bootstrap intervals)
- cost-aware verification cascade with abstention, plus cascade evaluation with coverage-gap false alarms
- Indian Kanoon client and resolver with a fake-transport test (not yet run against the live API)
- structural plausibility model, repetition-across-samples detector, probe utilities
- reference-question builder and answer scorer, metadata CSV import, annotation templates, two-annotator merge and kappa
- markdown report for a checked document
- GPU and CPU scripts for generation, feature extraction and probe training in `experiments/`
- research notes: `docs/conclusion.md`, `docs/research-questions.md`, `docs/methods.md`, `docs/experiment-plan.md`
- 105 tests and CI

## Quickstart

```
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,ml]"
make test
make check
```

`make check` runs the cascade on a synthetic filing. `needs_review` means a human should check. `pass` is not a certificate. Add `--report out.md` to write a markdown report.

## Build incident stubs for India

```
make incidents
```

## Layout

```
src/indiacite/   package
data/            schema, synthetic examples, real incident stubs
docs/            research questions, methods, experiment plan, taxonomy, data policy, roadmap
tests/           pytest suite
```

## Data policy

No judgment text is redistributed beyond short excerpts. Real incidents are anonymised and linked. See `docs/data-policy.md`.

## Not legal advice

This project measures tools. A flag means a human should check. A missing flag does not mean a citation is correct.

## Licence

Code is MIT. Annotations are CC BY 4.0. Incident-derived fields carry the attribution of the source database.
