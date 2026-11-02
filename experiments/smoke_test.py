import argparse
import resource
import sys
import time

sys.path.insert(0, "experiments")

from common import load_model  # noqa: E402

TEXT = (
    "The Court in Alpha Traders v. State of Beta (2010) 5 SCC 100 "
    "held that notice must precede seizure."
)


DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model_id", nargs="?", default=DEFAULT_MODEL)
    ap.add_argument("--four-bit", action="store_true")
    ap.add_argument("--cpu-dtype", default="float32", choices=["float32", "bfloat16"])
    args = ap.parse_args()
    if args.model_id == "MODEL_ID":
        sys.exit("replace MODEL_ID with a real model id such as " + DEFAULT_MODEL)

    import torch

    print("python", sys.executable)
    print("torch", torch.__version__, "cuda", torch.cuda.is_available())
    if args.four_bit and not torch.cuda.is_available():
        sys.exit("four bit needs a cuda build of torch")

    from indiacite.citations import extract_citations
    from indiacite.spans import char_span_to_tokens, confidence_stats

    tok, model = load_model(args.model_id, args.four_bit, args.cpu_dtype)
    enc = tok(TEXT, return_offsets_mapping=True, return_tensors="pt", add_special_tokens=False)
    offsets = enc.pop("offset_mapping")[0].tolist()
    enc = enc.to(model.device)
    t0 = time.perf_counter()
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    print("forward seconds", round(time.perf_counter() - t0, 2))
    print(
        "hidden state tensors", len(out.hidden_states), "shape", tuple(out.hidden_states[-1].shape)
    )
    cite = extract_citations(TEXT)[0]
    toks = char_span_to_tokens(offsets, cite.start, cite.end)
    print("citation", cite.raw, "token ids", toks)
    ids = enc["input_ids"][0].tolist()
    print("confidence", confidence_stats(out.logits[0].float().cpu().numpy(), ids, toks))
    print("peak ram gb", round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 2))
    if torch.cuda.is_available():
        print("peak vram gb", round(torch.cuda.max_memory_allocated() / 1e9, 2))


if __name__ == "__main__":
    main()
