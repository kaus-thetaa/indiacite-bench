import json


def dtype_key(version: str) -> str:
    major, minor = (int(x) for x in version.split(".")[:2])
    return "dtype" if (major, minor) >= (4, 56) else "torch_dtype"


def load_model(model_id: str, four_bit: bool, cpu_dtype: str = "float32"):
    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    tok = AutoTokenizer.from_pretrained(model_id)
    key = dtype_key(transformers.__version__)
    kwargs = {}
    if four_bit:
        kwargs["device_map"] = "auto"
        kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )
    elif torch.cuda.is_available():
        kwargs["device_map"] = "auto"
        kwargs[key] = torch.float16
    else:
        # cpu path
        kwargs[key] = getattr(torch, cpu_dtype)
    model = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)
    model.eval()
    return tok, model


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
