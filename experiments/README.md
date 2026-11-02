# Experiments

These scripts need a GPU and model downloads. They are not run in CI and were not run by the author of this repo at the time of writing, so treat the first run as a test.

## Setup

Use a virtual environment for this project, not a tool-managed one such as PlatformIO's. Check with `which python` before installing.

```
pip install -e ".[dev,ml,cpu]"
```

For a CPU-only machine install the CPU build of PyTorch first: `pip install torch --index-url https://download.pytorch.org/whl/cpu`. With an NVIDIA GPU use `.[dev,ml,gpu]` and the CUDA build from pytorch.org instead.

With an NVIDIA GPU install the CUDA build of PyTorch from pytorch.org. On a 6 GB GPU start with a model of 1 to 3 billion parameters; 7 to 8 billion in 4 bit is borderline. Check `nvidia-smi` and `python -c "import torch; print(torch.cuda.is_available())"` first.

## No usable NVIDIA GPU

The scripts also run on the CPU if you leave out `--four-bit`. Start with `Qwen/Qwen2.5-0.5B-Instruct`, which needs about 2 GB of memory in float32. A 1.5 billion parameter model needs about 6 GB in float32 or about 3 GB with `--cpu-dtype bfloat16`, which can be slower. Close other programs, and measure the time and peak memory of the smoke test before planning runs. Integrated Intel or AMD graphics are not used by the standard PyTorch build, so on those machines the work runs on the CPU anyway.

## Order of work

1. smoke test: `python experiments/smoke_test.py --four-bit` prints the python path, torch and cuda status, hidden state shapes, token ids for a citation and peak memory. The default model is `Qwen/Qwen2.5-1.5B-Instruct` (Apache 2.0, ungated). Pass another Hugging Face model id as the first argument to change it
2. questions: `indiacite queries --meta data/private/meta.jsonl --out data/private/queries.jsonl`
3. answers: `python experiments/generate.py --model-id MODEL_ID --queries data/private/queries.jsonl --out data/private/gen_MODEL.jsonl --four-bit`
4. labels: `indiacite score --meta data/private/meta.jsonl --queries data/private/queries.jsonl --answers data/private/gen_MODEL.jsonl --out data/private/labels_MODEL.jsonl`
5. features: `python experiments/extract_features.py --model-id MODEL_ID --generations data/private/gen_MODEL.jsonl --out-prefix data/private/feat_MODEL --four-bit`
6. probes: `python experiments/train_probes.py --features data/private/feat_MODEL --labels data/private/labels_MODEL.jsonl`

`data/private/` is ignored by git. Metadata from legal databases stays there unless the database terms allow release.

Replace `MODEL_ID` in the commands below with a real Hugging Face model id, for example `Qwen/Qwen2.5-1.5B-Instruct`.

## Metadata file

One json object per line with fields `case_id`, `name`, `citation`, `court`, `year` and optional `judge`.

## Notes

- A wrong citation here means wrong for this case. Whether it is nonexistent or belongs to another case needs a database lookup.
- Probes are trained per model. Do not mix hidden states from different models.
