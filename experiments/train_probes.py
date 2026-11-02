import argparse
import sys

sys.path.insert(0, "experiments")

from common import read_jsonl  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True, help="prefix used by extract_features")
    ap.add_argument("--labels", required=True, help="jsonl written by indiacite score --out")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    from indiacite.features_io import evaluate_layers, load_features

    rows, layers = load_features(args.features + ".npz", args.features + ".jsonl")
    labels = {r["query_id"]: r["label"] for r in read_jsonl(args.labels)}
    result = evaluate_layers(rows, layers, labels, seed=args.seed)
    for layer, auc in sorted(result.items()):
        print(f"layer {layer}: auroc {auc if auc is None else round(auc, 3)}")


if __name__ == "__main__":
    main()
