# Related work

Legal hallucination measurement
- Dahl, Magesh, Suzgun and Ho, Large Legal Fictions, J. Legal Analysis 16 (2024). Reference-based questions on US federal cases; hallucination between 69% and 88% for the models tested in the preprint; models often cannot tell when they are hallucinating.
- Magesh et al., Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools, J. Empirical Legal Studies 22 (2025). Preregistered audit; commercial tools hallucinated between 17% and 33% despite vendor claims.

Citation verification benchmarks
- Who Checks the Citations? (LePhantomCite), arXiv 2606.21155. US brief excerpts with injected errors; existence and name mismatch are easy, pincites and content misrepresentation are hard; models flag many real citations missing from the lookup database.
- When Citations Mislead? (PARCEL), arXiv 2610.10971. Claim-level benchmark from New York Court of Appeals briefs; missing support is harder to detect than contradiction.

Detection from internal signals and structure
- Where Fake Citations Are Made, arXiv 2604.18880. Probes detect field-level hallucination in scholarly references; cross-field and cross-dataset transfer is limited.
- How LLMs Cite and Why It Matters, arXiv 2603.03299. A classifier on citation metadata alone reaches AUC 0.876 in cross-validation and 0.834 leave-one-model-out for scholarly references.
- Farquhar et al., semantic entropy, Nature 630 (2024); Kossen et al., semantic entropy probes, arXiv 2406.15927; Manakul et al., SelfCheckGPT, EMNLP 2023.
- Janiak et al., The Illusion of Progress, EMNLP 2025. Use validated labels and strong trivial baselines.

Indian legal NLP
- Joshi et al., IL-TUR, ACL 2024. Benchmark with a public leaderboard.
- Falkor-IRAC, arXiv 2605.14665. Small proof of concept for graph-constrained generation. It checks existence in its own graph and does not test whether a case supports a claim.
- AI Hallucination Cases Database, Damien Charlotin. CC BY 4.0. Listed 16 Indian decisions among 2,241 on 29 Oct 2026.
- Indian Kanoon API pricing and terms. Non-commercial use can get free credits after verification; attribution required.

Gap: no independent benchmark of citation-checking methods for Indian law was found in this search, and no study of database-free or probe-based detection on Indian legal citations. Search again before each release.
