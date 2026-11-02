# Data access

## Indian Kanoon API

- Endpoints in the official documentation: search (`/search/?formInput=<query>&pagenum=<n>`), document (`/doc/<docid>/`), court copy (`/origdoc/<docid>/`), document fragments, document metadata. Authentication is a header `Authorization: Token <token>`.
- Pricing page: prepaid, and non-commercial use can get free monthly credits after the administrator verifies the use case. Apply early.
- Terms: attribution required, including for retrieval and fine-tuning use. The terms say nothing about bulk redistribution, so release identifiers and labels only.
- Third-party sources quote per-call prices (search about Rs 0.50, document about Rs 0.20). Treat them as unverified.

## How `kanoon.py` is meant to be used

Set `IK_API_TOKEN` in the environment. Never put the token in a file in the repo.

The resolver searches by case title, picks candidates whose title is close to the cited name, fetches each candidate and checks whether the cited reporter citation appears in the text. It caches outcomes only, never judgment text.

Status: tested only against a fake transport. The first live call is a test.

## Pitfalls

- A full-text search for a citation string returns documents that contain the string. That includes later judgments that merely cite it, and the very judgments that list a fake citation to condemn it. Searching by citation alone cannot prove existence. Search by case title, then confirm.
- Coverage is partial. Not found is not the same as fake. The cascade treats it as unknown unless told otherwise.
- Documents may not print the reporter citation in the text. In that case a found case stays unconfirmed, not wrong.

## Other sources

- Incident database: https://www.damiencharlotin.com/hallucinations/ (CC BY 4.0, attribution on every derived record). Build stubs with `make incidents`.
- Primary judgments: the Supreme Court publishes judgments on its own site. Quote short items only.
- Hand collection: if credits are slow, fill `data/templates/meta_template.csv` by hand for 50 to 100 cases and run `indiacite meta`.
