import argparse
import sys

sys.path.insert(0, "experiments")

from common import load_model, read_jsonl  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--generations", required=True)
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--four-bit", action="store_true")
    ap.add_argument("--cpu-dtype", default="float32", choices=["float32", "bfloat16"])
    ap.add_argument("--layers", help="comma separated, default quarter points")
    ap.add_argument("--pool", default="last", choices=["last", "first", "mean"])
    args = ap.parse_args()

    import torch

    from indiacite.citations import extract_citations
    from indiacite.features_io import save_features
    from indiacite.spans import citation_rows, confidence_stats

    tok, model = load_model(args.model_id, args.four_bit, args.cpu_dtype)
    n_layers = model.config.num_hidden_layers
    layers = (
        [int(x) for x in args.layers.split(",")]
        if args.layers
        else [n_layers // 4, n_layers // 2, (3 * n_layers) // 4, n_layers]
    )
    index_rows = []
    vectors = {layer: [] for layer in layers}
    for rec in read_jsonl(args.generations):
        base = len(rec["prompt_text"])
        full = rec["prompt_text"] + rec["answer"]
        cites = [
            {"raw": c.raw, "start": base + c.start, "end": base + c.end}
            for c in extract_citations(rec["answer"])
        ]
        if not cites:
            continue
        enc = tok(full, return_offsets_mapping=True, return_tensors="pt", add_special_tokens=False)
        offsets = enc.pop("offset_mapping")[0].tolist()
        enc = enc.to(model.device)
        with torch.no_grad():
            out = model(**enc, output_hidden_states=True)
        hidden = {k: out.hidden_states[k][0].float().cpu().numpy() for k in layers}
        logits = out.logits[0].float().cpu().numpy()
        ids = enc["input_ids"][0].tolist()
        rows = citation_rows(full, cites, offsets, hidden, layers, args.pool)
        seen = set()
        for r in rows:
            vectors[r["layer"]].append(r["vector"])
            key = (r["start"], r["end"])
            if key in seen:
                continue
            seen.add(key)
            toks = [
                i for i, (a, b) in enumerate(offsets) if b > a and a < r["end"] and b > r["start"]
            ]
            index_rows.append(
                {
                    "query_id": rec["query_id"],
                    "case_id": rec["case_id"],
                    "model": rec["model"],
                    "raw": r["raw"],
                    "n_tokens": r["n_tokens"],
                    **confidence_stats(logits, ids, toks),
                }
            )
    save_features(args.out_prefix + ".npz", args.out_prefix + ".jsonl", index_rows, vectors)
    print("rows", len(index_rows), "layers", layers)


if __name__ == "__main__":
    main()
