import json

import pytest

from indiacite.baselines import DictResolver  # noqa: F401
from indiacite.cascade import Cascade, ResolverStage
from indiacite.citations import extract_citations
from indiacite.kanoon import IndianKanoonClient, IndianKanoonResolver, strip_html


class FakeTransport:
    def __init__(self, docs, texts):
        self.docs, self.texts, self.calls = docs, texts, []

    def __call__(self, url, token):
        self.calls.append((url, token))
        if "/search/" in url:
            return {"docs": self.docs}
        doc_id = url.rstrip("/").split("/")[-1]
        return {"doc": self.texts.get(doc_id, "")}


def make(docs, texts):
    t = FakeTransport(docs, texts)
    return IndianKanoonResolver(IndianKanoonClient(token="tok", transport=t)), t


def cite(raw):
    return extract_citations(raw)[0]


def test_token_required(monkeypatch):
    monkeypatch.delenv("IK_API_TOKEN", raising=False)
    with pytest.raises(ValueError):
        IndianKanoonClient()


def test_requests_carry_token_and_encoded_query():
    res, t = make([], {})
    res.client.search("Alpha Traders v. State of Beta")
    url, token = t.calls[0]
    assert token == "tok" and "formInput=Alpha+Traders+v.+State+of+Beta" in url


def test_found_and_verified():
    docs = [{"tid": 11, "title": "Alpha Traders vs State Of Beta on 5 May, 2010"}]
    res, _ = make(docs, {"11": "<p>Equivalent citations: 2010 (5) SCC 100</p>"})
    r = res.resolve(cite("(2010) 5 SCC 100"), "Alpha Traders v. State of Beta")
    assert r.found is True and r.citation_verified is True


def test_found_but_citation_not_confirmed_is_unknown_not_false():
    docs = [{"tid": 11, "title": "Alpha Traders vs State Of Beta"}]
    res, _ = make(docs, {"11": "<p>no reporter details here</p>"})
    r = res.resolve(cite("(2010) 5 SCC 100"), "Alpha Traders v. State of Beta")
    assert r.found is True and r.citation_verified is None


def test_no_matching_title_means_not_found():
    docs = [{"tid": 5, "title": "Completely Different Matter"}]
    res, _ = make(docs, {})
    r = res.resolve(cite("(2010) 5 SCC 100"), "Alpha Traders v. State of Beta")
    assert r.found is False


def test_no_case_name_gives_unknown():
    res, t = make([], {})
    r = res.resolve(cite("(2010) 5 SCC 100"), None)
    assert r.found is None and t.calls == []


def test_cache_avoids_second_call_and_holds_no_text():
    docs = [{"tid": 11, "title": "Alpha Traders vs State Of Beta"}]
    res, t = make(docs, {"11": "2010 (5) SCC 100"})
    c = cite("(2010) 5 SCC 100")
    res.resolve(c, "Alpha Traders v. State of Beta")
    n = len(t.calls)
    res.resolve(c, "Alpha Traders v. State of Beta")
    assert len(t.calls) == n
    blob = json.dumps(res.cache)
    assert "SCC 100" not in blob and "Equivalent" not in blob


def test_works_inside_cascade():
    docs = [{"tid": 11, "title": "Alpha Traders vs State Of Beta"}]
    res, _ = make(docs, {"11": "2010 (5) SCC 100"})
    text = "Relied on Alpha Traders v. State of Beta (2010) 5 SCC 100."
    out = Cascade([ResolverStage(res)]).check(text)
    assert out[0].outcome == "pass"


def test_strip_html():
    assert strip_html("<b>a</b>  <i>b</i>") == "a b"
