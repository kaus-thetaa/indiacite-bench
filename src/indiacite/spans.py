def char_span_to_tokens(offsets: list[tuple[int, int]], start: int, end: int) -> list[int]:
    return [i for i, (a, b) in enumerate(offsets) if b > a and a < end and b > start]


def pool_rows(hidden, token_ids: list[int], mode: str = "last"):
    if not token_ids:
        raise ValueError("no tokens to pool")
    if mode == "last":
        return hidden[token_ids[-1]]
    if mode == "first":
        return hidden[token_ids[0]]
    if mode == "mean":
        import numpy as np

        return np.asarray(hidden)[token_ids].mean(axis=0)
    raise ValueError(f"unknown mode {mode}")


def citation_rows(full_text, citations, offsets, hidden_by_layer, layers, mode="last"):
    rows = []
    for c in citations:
        toks = char_span_to_tokens(offsets, c["start"], c["end"])
        if not toks:
            continue
        for layer in layers:
            vec = pool_rows(hidden_by_layer[layer], toks, mode)
            rows.append(
                {
                    "raw": c["raw"],
                    "start": c["start"],
                    "end": c["end"],
                    "layer": layer,
                    "n_tokens": len(toks),
                    "vector": [float(x) for x in vec],
                }
            )
    return rows


def confidence_stats(logits, input_ids, token_ids: list[int]) -> dict:
    import numpy as np

    lg = np.asarray(logits, dtype="float64")
    shifted = lg - lg.max(axis=1, keepdims=True)
    logp = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
    lps, ents = [], []
    for i in token_ids:
        if i == 0:
            continue
        lps.append(float(logp[i - 1, input_ids[i]]))
        ents.append(float(-(np.exp(logp[i - 1]) * logp[i - 1]).sum()))
    if not lps:
        return {"mean_logprob": None, "min_logprob": None, "mean_entropy": None}
    return {
        "mean_logprob": sum(lps) / len(lps),
        "min_logprob": min(lps),
        "mean_entropy": sum(ents) / len(ents),
    }
