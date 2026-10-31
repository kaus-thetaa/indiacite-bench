# Annotation guide

## Who

At least two annotators per citation. At least one must be law-trained for unsupported_ruling, wrong_pinpoint and stale_statute.

## Steps

1. Read the excerpt and mark the exact citation string. It must appear verbatim.
2. Find the authority in two independent sources. A single database miss is not enough to call a citation nonexistent, because coverage is partial.
3. Pick one error type from `docs/taxonomy.md` or valid.
4. Write evidence in one or two sentences with where you looked.
5. Annotate alone first. Compare only after both have finished.

## Agreement

Report Cohen's kappa on the first 50 citations and again at the end. If kappa is below 0.6 on the pilot, revise this guide before labelling more.

## Adjudication

A third person resolves disagreements and records the final label. Keep the individual labels in `labels`.

## Rules

- Never label from memory alone.
- Remove party names and personal data from excerpts.
- If unsure, mark for review in `note` and do not guess.
