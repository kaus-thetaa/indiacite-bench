# Methods

## Data sources

- A. real incidents: decisions from the public incident database. Labels come from the court's own finding with the paragraph reference.
- B. reference-based generations: ask models factual questions about Indian judgments whose metadata is known from a legal database (court, year, citation, bench). Compare answers with the metadata. This follows the design used for US case law and needs no legal expertise to label.
- C. controlled injections: modify one component of a verified citation (name, volume, page, year) or alter a quotation.

Split by case so that no judgment appears in both training and test data.

## Detectors

| id | detector | needs |
|---|---|---|
| M0 | structural plausibility: features of year, volume and page learned from real citation strings against perturbed negatives | public citation strings only |
| M1 | database resolver: existence and name match; not found is unknown, not fake | legal database access |
| M2 | LLM check with retrieved text | open model and retrieval |
| M3 | hidden-state probe at citation tokens | open model hidden states |
| M4 | proposition support via retrieval and entailment (stretch) | expert-validated subset |

## Cascade

Stages run from cheap to expensive. Each stage returns flag, pass or unknown. Unknown defers to the next stage. A citation nobody decides is `needs_review`. Score-based stages use two thresholds so they can abstain.

## Metrics

- per error type: precision, recall, F1 with bootstrap intervals
- AUROC for score-based detectors
- false positive rate on real citations absent from the database
- cost per document in stage units
- paired bootstrap for differences between detectors

## Baselines

format check only, database only, LLM only without retrieval, and the response length or citation length heuristic. Strong trivial baselines matter because earlier work found simple heuristics can match complex detectors.

## Ethics

Outputs are flags for human review. Excerpts are short and anonymised. See `docs/data-policy.md`.
