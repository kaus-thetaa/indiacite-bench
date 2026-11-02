# Taxonomy

Six error types plus valid. A citation can carry several problems. Label the most serious one and note the rest in `evidence`.

| type | decide with | typical evidence |
|---|---|---|
| nonexistent | search by name and by citation in two sources | no judgment found, citation unassigned |
| citation_mismatch | the citation resolves to a different case | resolver shows another case at that citation |
| wrong_pinpoint | case is right, page or paragraph is not | text of the paragraph |
| false_quote | words not in the judgment | full text search |
| unsupported_ruling | case exists but does not hold the point | reading the holding |
| stale_statute | provision repealed or replaced at the relevant date | repeal notification or commencement date |

## Indian anchor from primary sources

In 2026 INSC 668 (Supreme Court, 2 July 2026, para 15) the Court verified six authorities relied on by a tribunal and reported, in its own words:

| authority as cited | Court's finding | our label |
|---|---|---|
| State Bank of India v. Shree Ram Urban Infrastructure Ltd., 2020 SCC OnLine SC 341 | wrong citation of an existing reported judgment (correct cause title is different) and a non-existent paragraph | citation_mismatch |
| Everest Kento Cylinders Ltd. v. Union of India, (2015) 2 SCC 1 | correct citation, non-existent paragraph | wrong_pinpoint |
| ICICI Bank Ltd. v. Urban Infrastructure Real Estate Ltd., (2019) 16 SCC 528 | non-existent citation | nonexistent |
| V.S. Dempo & Co. Ltd. v. Reliance Communications Ltd., (2021) 10 SCC 176 | non-existent citation | nonexistent |
| Canara Bank v. N.G. Subbaraya Setty & Anr., (2018) 16 SCC 228 | correct citation, non-existent paragraph | wrong_pinpoint |
| Sarbjit Singh v. Union Bank of India, (2022) 7 SCC 464 | non-existent citation | nonexistent |

In 2026 INSC 947 (Supreme Court, 2 September 2026, para 4) the Court found case laws that were non-existent or carried fake citations, and others that exist but do not lay down the ratio attributed to them. That third kind is our unsupported_ruling. That judgment does not list the items individually.

Observed so far in Indian primary sources: nonexistent, citation_mismatch, wrong_pinpoint, unsupported_ruling. Not yet observed in them: false_quote and stale_statute. They come from US work and from the incident database and stay in the taxonomy until the Indian incidents are read.

## Why the split matters

A lookup that only checks whether a citation exists and whether its case name matches can catch four of the six items above at best. The two correct citations with non-existent paragraphs pass such a check. Catching them needs the judgment text and its paragraph numbering.

## Crosswalk

| this project | US benchmark (LePhantomCite) | incident database |
|---|---|---|
| nonexistent | non-existent citation | Fabricated: Case Law |
| citation_mismatch | case name mismatch | Fabricated, with a description saying the citation points to another case |
| wrong_pinpoint | incorrect pincite | not separate |
| false_quote | verbatim misquote | False Quotes |
| unsupported_ruling | content misrepresentation | Misrepresented |
| stale_statute | not covered | Outdated Advice: Repealed Law |

## India-specific points to verify with a legal collaborator

- Parallel reporters (SCC, AIR, SCR, SCC OnLine) can give several valid citations for one judgment, and the SCC format varies: `(2010) 5 SCC 100` and `2010 (5) SCC 100`. The parser normalises both.
- Neutral citations (INSC) are assumed to start in 2023. Confirm.
- The change from IPC and CrPC to BNS and BNSS applies by offence date. Confirm the rules before labelling.
- Pinpoints are usually paragraph numbers, not pages.
