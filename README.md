# indiacite-bench

Research code and benchmark for detecting fabricated and unsupported case citations in Indian legal text.

Status: pre-alpha. No results yet. Sample data is synthetic and exists only to test the pipeline.

## Research question

Courts in India have begun sanctioning unverified AI-generated citations. Existing benchmarks cover US law. We study how well different checking methods work on Indian law, what they cost, and where they fail. The computational questions:

1. Can a database-free structural model flag fabricated Indian citations?
2. Can hidden-state probes flag a fabricated citation at generation time, and do they transfer across models and citation fields?
3. How do database lookup, retrieval-backed LLM checking and probes trade off precision, recall and cost?
4. How badly does incomplete database coverage inflate false alarms?

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

- citation extractor for SCC, AIR, INSC, SCR and SCC OnLine
- case name extraction and fuzzy name matching
- record schema, validator and metrics (precision, recall, kappa, AUROC, bootstrap intervals)
- cost-aware verification cascade with abstention (`cascade.py`)
- structural plausibility model trained without labels (`structural.py`, needs the `ml` extra)
- probe utilities with leave-one-group-out and cross-field transfer (`probes.py`)
- incident stub builder for the public incident database
- 56 tests and CI

## Quickstart

```
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,ml]"
make test
make check
```

`make check` runs the cascade on a synthetic filing. `needs_review` means a human should check. `pass` is not a certificate.

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
