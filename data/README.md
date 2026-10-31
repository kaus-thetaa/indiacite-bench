# Data

## Files

- `schema/record.schema.json` one labelled record
- `examples/synthetic_sample.jsonl` fictional records for pipeline tests only. Citations in it may collide with real ones by accident and must never be used as evidence about any real case.
- `real_incidents/stubs.jsonl` generated, one stub per decision from the public incident database for India

## Record

Each record has an `id`, a `source`, a short `excerpt` (600 characters at most), and `citations`. Each citation has the exact `raw` string, an `error_type`, `evidence` for any error, and optional `labels` from individual annotators. Real incidents also need `incident_ref` and `anonymized: true`.

## Building real records

1. Run `make incidents` to create stubs.
2. Open the linked decision. Copy only the short passage that shows the citation. Remove party names.
3. Two annotators label every citation independently, then adjudicate. See `docs/annotation-guide.md`.
4. Run `indiacite validate` before committing.

## Attribution

Incident stubs derive from the AI Hallucination Cases Database by Damien Charlotin, licensed CC BY 4.0, https://www.damiencharlotin.com/hallucinations/. Keep the attribution field on every stub.

## Legal databases

The Indian Kanoon API terms require attribution and prepaid use, and say nothing about bulk redistribution. Do not publish fetched judgment text. Publish citation strings, identifiers and labels only, and read the current terms before any bulk use.
