import argparse
import json
import os
import sys

sys.path.insert(0, "experiments")

from common import load_model, read_jsonl  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--queries", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--four-bit", action="store_true")
    ap.add_argument("--cpu-dtype", default="float32", choices=["float32", "bfloat16"])
    ap.add_argument("--max-new", type=int, default=80)
    args = ap.parse_args()

    import torch

    done = set()
    if os.path.exists(args.out):
        done = {r["query_id"] for r in read_jsonl(args.out)}
    tok, model = load_model(args.model_id, args.four_bit, args.cpu_dtype)
    with open(args.out, "a", encoding="utf-8") as f:
        for q in read_jsonl(args.queries):
            if q["query_id"] in done:
                continue
            msgs = [{"role": "user", "content": q["prompt"]}]
            prompt_text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            enc = tok(prompt_text, return_tensors="pt", add_special_tokens=False).to(model.device)
            with torch.no_grad():
                gen = model.generate(**enc, max_new_tokens=args.max_new, do_sample=False)
            answer = tok.decode(gen[0][enc["input_ids"].shape[1] :], skip_special_tokens=True)
            row = {
                "query_id": q["query_id"],
                "case_id": q["case_id"],
                "kind": q["kind"],
                "model": args.model_id,
                "prompt_text": prompt_text,
                "answer": answer,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()


if __name__ == "__main__":
    main()
