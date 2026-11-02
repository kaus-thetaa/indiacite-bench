# Related work

Everything below was read in full unless marked otherwise.

## Legal hallucination measurement

- Dahl, Magesh, Suzgun and Ho, Large Legal Fictions (J. Legal Analysis, 2024). Reference-based questions built from structured US case metadata, fourteen tasks from existence and court to central holding. Hallucination between 69% and 88% in the preprint models, higher at lower courts, for less prominent cases and very old or new cases. Models often cannot tell when they hallucinate. Existence questions about real cases are answered yes almost always, so fake cases are needed as controls. Citation equality is tested with the eyecite parser, for which no Indian equivalent exists.
- Magesh et al., Hallucination-Free? (J. Empirical Legal Studies, 2025). Preregistered audit of commercial legal research tools, which hallucinated between 17% and 33% of the time despite vendor claims. Read as a snippet only.

## Citation verification benchmarks

- LePhantomCite, arXiv 2606.21155 (US, mostly injected errors). Existence and name mismatch are easy for agents, pincites and content misrepresentation are hard, and weak models flag real citations that are missing from a free lookup database. Authors ask for naturally occurring examples.
- PARCEL, arXiv 2610.10971, Demir and Canbaz, ICAIL 2026 (3,396 synthetic claims from New York Court of Appeals briefs and decisions). Models reach 0.90 to 0.97 accuracy overall but false entailment on absent claims is much higher than on contradicted ones, and phantom citations are the hardest strategy. They also found models using their own legal knowledge instead of the text. They suggest ensembles and verifier cascades.

## Detection from internal signals, structure and repetition

- Chen et al., Where Fake Citations Are Made, arXiv 2604.18880. Nine models, 108,000 scholarly references. Author names fail most. Linear probes on a 32B model reach in-field AUC 0.81 to 0.92 but cross-field AUC 0.46 to 0.59. A 24B model transfers more. Their labels combine a database lookup with a web-grounded second stage, and two experts agreed with it on 93% of 200 cases. Probes use character offsets mapped to tokens, as in our `spans.py`.
- Naser, How LLMs Cite and Why It Matters, arXiv 2603.03299. 69,557 citations from ten models. A gradient-boosted classifier on string features alone reaches AUC 0.876 in cross-validation and 0.834 leaving one model out. A citation repeated in at least two of three samples matched a real work 88.9% of the time against 28.6% for one-off citations. Most bad citations were distortions of real ones (58% probable real, 31% near misses, 6% outright fabrications).
- Farquhar et al., semantic entropy (Nature, 2024); Kossen et al., semantic entropy probes; Manakul et al., SelfCheckGPT; Janiak et al., The Illusion of Progress (use validated labels and strong trivial baselines).

## Indian legal NLP and sources

- Supreme Court of India, 2026 INSC 668 (2 July 2026) and 2026 INSC 947 (2 September 2026). Zero tolerance for unverified AI precedents. The first lists six checked authorities. The second notes draft Regulations for Use of Artificial Intelligence in Courts, 2026.
- Joshi et al., IL-TUR (ACL 2024). Indian legal tasks and a leaderboard.
- Falkor-IRAC, arXiv 2605.14665. Small proof of concept that checks existence inside its own graph. It does not test whether a case supports a claim.
- AI Hallucination Cases Database, Damien Charlotin (CC BY 4.0). Listed 16 Indian decisions among 2,241 on 29 Oct 2026.
- Indian Kanoon API documentation, pricing and terms.

## Gap

No independent benchmark of citation-checking methods for Indian law was found, and no study of database-free, repetition or probe-based detection on Indian legal citations. An Indian upload-and-check product for Supreme Court citations exists, according to a vendor-style article, and its claims are untested. Search again before each release.
