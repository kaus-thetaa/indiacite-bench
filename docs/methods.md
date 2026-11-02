# Methods

## Two kinds of detector

- Document-side: work on any text you are handed, such as a petition, a brief or an order. Format and structural checks, lookup, retrieval-backed checking. These are what a court registry, a clerk or a defence lawyer can use.
- Generation-side: need the model that wrote the text, such as hidden-state probes, token confidence and repetition across samples. These are for people who build or host legal AI.

Both are studied. The product story for courts rests on the first kind.

## Data sources

- A. real incidents: decisions that name fake citations. Labels come from the court's own finding with the paragraph. Six items from 2026 INSC 668 are already in `data/real_incidents/sc_2026_insc_668.jsonl`.
- B. reference-based generations: ask models factual questions about Indian judgments whose metadata is known (court, year, citation, bench). Compare answers with the metadata. This design comes from the US study and needs no legal expertise to label. Include fake-case existence questions as negative controls, because models tend to answer yes to existence questions about real cases.
- C. controlled injections: modify one component of a verified citation or quotation. Easier than natural errors, so used for control, not as the main test.

Split by case so that no judgment appears in both training and test data. Report results by court level, because the US study found worse hallucination at lower courts.

## Detectors

| id | detector | kind | needs |
|---|---|---|---|
| M0 | structural plausibility model | document-side | public citation strings and real LLM outputs |
| M1 | database lookup, existence and name match | document-side | legal database access |
| M2 | LLM check with retrieved text | document-side | open model and retrieval |
| M2b | repetition across samples (agreement of citations) | generation-side | several samples per prompt |
| M3 | hidden-state probes and token-confidence features | generation-side | open model hidden states and logits |
| M4 | proposition support via retrieval and entailment | document-side | expert-validated subset |

M0 training note. Train on citations that real models produced, labelled by the metadata, not only on perturbed strings. A study of scholarly references found a classifier on string features alone reached AUC 0.876 in cross-validation and 0.834 leaving one model out, and that most bad citations were distortions of real ones, not pure inventions. Perturbations are for augmentation and controls.

M2b note. In the same study a citation that recurred in at least two of three samples matched a real work 88.9% of the time against 28.6% for one-off citations. We test whether the same holds for Indian citations.

## Cascade

Stages run from cheap to expensive. Each returns flag, pass or unknown. Unknown defers to the next stage. A citation nobody decides is `needs_review`. Score stages use two thresholds so they can abstain. A lookup miss is unknown unless the database is known to be complete.

## Metrics

- per error type: recall, plus precision for error versus valid, with bootstrap intervals
- AUROC for score-based detectors
- false alarm rate on real citations missing from the database
- cost per document in stage units
- paired bootstrap for differences between detectors

## Baselines

Format check only, database only, LLM only without retrieval, and the length heuristic. Strong trivial baselines matter because simple heuristics have matched complex detectors in earlier work.

## Transfer

Probes are trained per model because hidden sizes differ. We test transfer across citation fields, question types and data sources. Leave-one-model-out is used for model-agnostic detectors (M0, token confidence, repetition). Earlier work found probe transfer across fields near chance on one large model and higher on another, so we report it and do not assume it.

## Ethics

Outputs are flags for human review. Excerpts are short and anonymised. See `docs/data-policy.md`.
