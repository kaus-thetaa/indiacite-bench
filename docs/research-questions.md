# Research questions

| id | question | why it matters | evidence that answers it |
|---|---|---|---|
| RQ1 | How often do general LLMs fabricate or mis-cite Indian case law on reference-based questions, and how does it vary by court level, case prominence and year? | no Indian measurement exists in what we found; US work found worse results at lower courts | rates per model, task and court level with intervals |
| RQ2 | Can a model trained on real LLM-generated citation strings flag fabricated citations without a database, and does it generalise across models? | database access costs money and has coverage gaps; a scholarly study reached AUC 0.83 to 0.88 | AUROC on held-out cases and on real incidents, leave-one-model-out, against trivial baselines |
| RQ3 | Does repetition across samples (M2b) identify unreliable citations for Indian law? | cheapest generation-side detector, no database | agreement against the metadata label |
| RQ4 | Do hidden-state probes and token-confidence features flag a fabricated citation at generation time, and do probes transfer across citation fields, question types and sources? | probes from different models cannot be compared directly; prior cross-field transfer was near chance on one model | within-set and cross-set AUROC; leave-one-model-out only for model-agnostic features |
| RQ5 | What accuracy, coverage and cost trade-off does a cascade of cheap to expensive checks achieve, and how much does incomplete database coverage inflate false alarms? | courts and clinics have limited budgets; a real citation absent from a database must not be called fake | accuracy-cost-coverage curves; false alarm rate on the coverage-gap set |
| RQ6 | Which errors do existence and name checks miss? | in the six items of 2026 INSC 668 two were correct citations with non-existent paragraphs | recall by error type on real items and generations; retrieval-backed check on a small expert-validated set |

## Risks

- RQ4 needs a model whose hidden states you can read and that gets some citations right. Tiny models fabricate nearly everything, which leaves no correct class to learn from. Measure the correct-answer rate in the pilot before spending time on probes. Larger models need a GPU, for example a free cloud notebook (check current limits) or a lab machine.
- RQ6 needs the judgment text and a law-trained reviewer for the hard cases.
- Few real Indian incidents exist. Use them as the real-world test split, not the training set.
- A vendor or a US group may publish first. Release the parser and benchmark early.
