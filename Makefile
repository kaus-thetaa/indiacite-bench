.PHONY: test lint validate eval check incidents

test:
	pytest -q

lint:
	ruff check .
	ruff format --check .

validate:
	indiacite validate data/examples/synthetic_sample.jsonl
	indiacite validate data/real_incidents/sc_2026_insc_668.jsonl

eval:
	indiacite eval data/examples/synthetic_sample.jsonl

check:
	indiacite check data/examples/sample_filing.txt --known data/examples/known_sample.json

incidents:
	mkdir -p data/interim
	curl -L -o data/interim/charlotin.csv https://www.damiencharlotin.com/hallucinations/hallucinations/download.csv
	indiacite stubs --csv data/interim/charlotin.csv --country India --out data/real_incidents/stubs.jsonl
