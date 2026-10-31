# Paper walkthrough

Plain-language notes for rewriting the draft in your own words. Each section lists what it must do and the words to learn first.

## Abstract
Say the problem, the gap, what you built, what you found. Write it last. Leave results as placeholders until they exist.

## 1 Introduction
- What a citation is and why a fake one does damage.
- Evidence the problem is real: US studies measured it; Indian courts sanctioned it in 2026.
- The gap: US benchmarks exist; none found for India.
- Why it is a computing problem: databases are incomplete, checks cost money, a model may show warning signs before it writes a fake.
- Your contributions in three or four plain lines.

## 2 Related work
Group papers by idea, not by date: measuring the problem, benchmarks, detection from signals, Indian legal NLP. For every paper write one line: what it did and what it left open. The table shows where your work differs.

## 3 Problem formulation
Define the objects: a document, its citations, the true label of each, a detector that outputs a flag or a score and a cost. Define the cascade and the three outcomes: flag, pass, needs review. The key idea to explain in your own words: not found is not the same as fake.

## 4 Research questions
Copy the list from `docs/research-questions.md` and explain in one sentence why each matters.

## 5 Benchmark
Three sources of data and why you need all three: real incidents are realistic but few; reference questions scale; injections give control. Explain the split by case and why leakage would inflate results.

## 6 Methods
One paragraph per detector: what it looks at, what it costs, what it cannot do. Terms to learn: AUROC, probe, hidden state, entailment.

## 7 Experimental protocol
Metrics, intervals, seeds, baselines. State the decision rules in advance.

## 8 Results
Empty until experiments run. Do not write conclusions you do not have.

## 9 Discussion and limits
Be honest about few real incidents, label quality, one jurisdiction, and that a flag is not a verdict.

## Terms to learn first
citation, reporter, neutral citation, precedent, hallucination, AUROC, precision, recall, bootstrap interval, hidden state, linear probe, retrieval, entailment.
