# Experiment plan and preregistration

Fill the status column as work is done. Do not change hypotheses after seeing test results. Record deviations at the bottom.

## Hypotheses

| id | hypothesis | primary metric | decision rule |
|---|---|---|---|
| H1 | structural model M0 beats the format-only baseline on injected errors | AUROC | difference above zero with 95% interval |
| H2 | M0 is weak on real incidents because real fabrications look plausible | AUROC on real incidents | report whatever is found |
| H3 | probes transfer worse across models than within a model | leave-one-model-out AUROC against within-model AUROC | report both with intervals |
| H4 | a database-only checker raises false alarms on real citations missing from the database | false positive rate on the coverage-gap set | report rate with interval |
| H5 | the cascade reaches similar recall to the full pipeline at lower cost | recall at matched precision and cost | report the curve |

## Analysis rules

- splits by case, fixed seed, set before any test result is seen
- three seeds for anything trained
- 95% bootstrap intervals on every reported metric
- no tuning on the real-incident split
- labels from the court finding or two independent annotators with kappa reported

## Status

| step | status |
|---|---|
| stubs for India built | done |
| annotation guide agreed | todo |
| splits frozen | todo |
| generation run | todo |
| labels adjudicated | todo |
| detectors run | todo |

## Deviations

none yet
