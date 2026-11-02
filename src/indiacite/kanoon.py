import json
import os
import re
import urllib.parse
import urllib.request

from indiacite.baselines import Resolution
from indiacite.citations import Citation, canonical_key, extract_citations
from indiacite.names import names_match

API = "https://api.indiankanoon.org"


def default_transport(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        method="POST",
        headers={"Authorization": f"Token {token}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


class IndianKanoonClient:
    def __init__(self, token: str | None = None, transport=None, base: str = API):
        self.token = token or os.environ.get("IK_API_TOKEN", "")
        if not self.token:
            raise ValueError("set IK_API_TOKEN")
        self.transport = transport or default_transport
        self.base = base

    def search(self, query: str, page: int = 0) -> dict:
        q = urllib.parse.quote_plus(query)
        return self.transport(f"{self.base}/search/?formInput={q}&pagenum={page}", self.token)

    def doc(self, doc_id) -> dict:
        return self.transport(f"{self.base}/doc/{doc_id}/", self.token)


class IndianKanoonResolver:
    def __init__(
        self, client: IndianKanoonClient, max_candidates: int = 3, cache: dict | None = None
    ):
        self.client = client
        self.max_candidates = max_candidates
        self.cache = cache if cache is not None else {}

    def resolve(self, citation: Citation, case_name: str | None = None) -> Resolution:
        key = canonical_key(citation.raw)
        ck = json.dumps(key)
        if ck in self.cache:
            return Resolution(**self.cache[ck])
        if not case_name:
            return Resolution(None, None, "indiankanoon: no case name")
        docs = self.client.search(case_name).get("docs", [])[: self.max_candidates]
        out = Resolution(False, None, "indiankanoon")
        for d in docs:
            title = strip_html(d.get("title", ""))
            if not names_match(case_name, title, 0.6):
                continue
            text = strip_html(self.client.doc(d.get("tid")).get("doc", ""))
            cites = {canonical_key(c.raw) for c in extract_citations(text)}
            verified = True if key in cites else None
            out = Resolution(True, title, "indiankanoon", verified)
            if verified:
                break
        # cache stores outcome only and never judgment text
        self.cache[ck] = {
            "found": out.found,
            "canonical": out.canonical,
            "source": out.source,
            "citation_verified": out.citation_verified,
        }
        return out
