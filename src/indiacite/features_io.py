import json

from indiacite.probes import fit_probe, probe_auroc
from indiacite.splits import group_split


def save_features(npz_path, index_path, index_rows, vectors_by_layer):
    import numpy as np

    arrays = {f"layer{k}": np.asarray(v, dtype="float32") for k, v in vectors_by_layer.items()}
    np.savez_compressed(npz_path, **arrays)
    with open(index_path, "w", encoding="utf-8") as f:
        for row in index_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_features(npz_path, index_path):
    import numpy as np

    data = np.load(npz_path)
    layers = {int(k.removeprefix("layer")): data[k] for k in data.files}
    with open(index_path, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    return rows, layers


def join_labels(index_rows, labels: dict[str, str]):
    keep, y = [], []
    for i, row in enumerate(index_rows):
        lab = labels.get(row["query_id"])
        if lab == "correct":
            keep.append(i)
            y.append(0)
        elif lab == "wrong":
            keep.append(i)
            y.append(1)
    return keep, y


def evaluate_layers(index_rows, layers, labels, test_frac=0.3, seed=0):
    keep, y = join_labels(index_rows, labels)
    groups = [index_rows[i]["case_id"] for i in keep]
    train, test = group_split(groups, test_frac, seed)
    out = {}
    for layer, x in layers.items():
        xs = [x[i] for i in keep]
        ytr = [y[i] for i in train]
        yte = [y[i] for i in test]
        if len(set(ytr)) < 2 or len(set(yte)) < 2:
            out[layer] = None
            continue
        model = fit_probe([xs[i] for i in train], ytr, seed)
        out[layer] = probe_auroc(model, [xs[i] for i in test], yte)
    return out
