# Research questions

| id | question | why it matters | evidence that answers it |
|---|---|---|---|
| RQ1 | How often do general LLMs fabricate or mis-cite Indian case law when asked reference-based questions, and which error types dominate? | no Indian measurement exists in what we found; US studies report high rates | rates per model and error type with intervals |
| RQ2 | Can a model trained only on public citation strings and perturbed negatives flag fabricated citations without any database? | database access costs money and has coverage gaps | AUROC on held-out real incidents and injected errors, against a trivial baseline |
| RQ3 | Do hidden-state probes read fabrication off the model before output, and do they transfer across models and across citation fields? | cheap generation-time warning; prior work on scholarly references suggests transfer is weak | leave-one-model-out and cross-field AUROC |
| RQ4 | What is the accuracy, coverage and cost trade-off of a cascade of cheap to expensive checks with abstention? | courts and clinics have limited budgets | accuracy-cost-coverage curves |
| RQ5 | How much does missing database coverage inflate false alarms? | a real citation absent from a database must not be called fake | false positive rate on real citations known to be missing |
| RQ6 (stretch) | Can retrieval plus entailment checks tell whether a real case supports a stated proposition? | the error courts struck down in 2026 | accuracy on a small expert-validated set |

## Risks

- RQ3 needs GPU time. Plan for a 7 to 8 billion parameter model in 4 bit on free notebooks and measure first.
- RQ6 needs a law-trained reviewer.
- Few real Indian incidents exist. Use them as the real-world test split, not the training set.
