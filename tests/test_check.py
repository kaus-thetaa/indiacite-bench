from pathlib import Path

from indiacite.citations import extract_case_name, extract_citations
from indiacite.cli import main

ROOT = Path(__file__).resolve().parents[1]
FILING = str(ROOT / "data" / "examples" / "sample_filing.txt")
KNOWN = str(ROOT / "data" / "examples" / "known_sample.json")


def test_check_command_output(capsys):
    assert main(["check", FILING, "--known", KNOWN]) == 0
    out = capsys.readouterr().out
    assert "[flag] (1900) 99 SCC 999" in out
    assert "[pass] (2010) 5 SCC 100" in out
    assert "citation_mismatch" in out
    assert "[needs_review] (2012) 7 SCC 300" in out
    assert "not a certificate" in out


def test_check_without_known_only_uses_format(capsys):
    assert main(["check", FILING]) == 0
    out = capsys.readouterr().out
    assert "[flag] (1900) 99 SCC 999" in out
    assert "[pass]" not in out


def test_extract_case_name_trims_lead_words():
    text = "In Alpha Traders v. State of Beta (2010) 5 SCC 100 the Court held"
    c = extract_citations(text)[0]
    assert extract_case_name(text, c) == "Alpha Traders v. State of Beta"


def test_extract_case_name_none_without_party_separator():
    text = "See the rule in (2010) 5 SCC 100"
    assert extract_case_name(text, extract_citations(text)[0]) is None


def test_extract_case_name_ignores_sentence_words():
    text = "It also cites Gamma Mills v. Delta Board (1900) 99 SCC 999 on delay."
    c = extract_citations(text)[0]
    assert extract_case_name(text, c) == "Gamma Mills v. Delta Board"
    text2 = "A further authority is Omega v. Sigma (2012) 7 SCC 300, which"
    c2 = extract_citations(text2)[0]
    assert extract_case_name(text2, c2) == "Omega v. Sigma"


def test_extract_case_name_drops_leading_connector():
    text = "cited A v. B (2001) 1 SCC 1 and Epsilon v. Zeta (2011) 6 SCC 200"
    c = extract_citations(text)[1]
    assert extract_case_name(text, c) == "Epsilon v. Zeta"


def test_extract_case_name_handles_capital_vs_forms():
    for sep in ("Vs.", "vs.", "V.", "versus", "v."):
        text = f"Canara Bank {sep} N.G. Subbaraya Setty & Anr., (2018) 16 SCC 228"
        name = extract_case_name(text, extract_citations(text)[0])
        assert name is not None and name.startswith("Canara Bank v. N.G. Subbaraya")
