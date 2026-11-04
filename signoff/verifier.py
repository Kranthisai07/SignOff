"""Verify a step from frames with Spark. Verdicts are cached by (frame, step text, model, prompt version)."""
import base64
import hashlib
import json
from pathlib import Path

from signoff.meta_client import create_response

MODEL = "muse-spark-1.3"
PROMPT_VERSION = "v1"  # bump when FORMAT or the prompt wording changes
CACHE = Path("results/cache")
FORMAT = 'Reply with JSON only: {"verdict":"pass|fail|unsure","reason":"...","confidence":0.0}'


def parse(text: str) -> dict:
    try:
        return json.loads(text.strip().removeprefix("```json").removesuffix("```").strip())
    except json.JSONDecodeError:
        return {"verdict": "invalid", "reason": text[:200], "confidence": None}


def verify_frame(path, step_text: str, model: str = MODEL) -> dict:
    img = Path(path).read_bytes()
    key = hashlib.sha256(img + f"|{step_text}|{model}|{PROMPT_VERSION}".encode()).hexdigest()
    cached = CACHE / f"{key}.json"
    if cached.exists():
        return json.loads(cached.read_text())
    prompt = f"Procedure step: {step_text} Judge from the photo whether this step was done correctly. {FORMAT}"
    inp = [{"role": "user", "content": [
        {"type": "input_text", "text": prompt},
        {"type": "input_image", "image_url": "data:image/jpeg;base64," + base64.b64encode(img).decode()}]}]
    data, ms = create_response(model, inp, reasoning={"effort": "low"})
    text = next(c["text"] for o in data["output"] if o["type"] == "message" for c in o["content"])
    row = {"model": model, "prompt_version": PROMPT_VERSION, "latency_ms": ms, "usage": data["usage"], **parse(text)}
    CACHE.mkdir(parents=True, exist_ok=True)
    cached.write_text(json.dumps(row))
    return row


def combine(verdicts: list[str]) -> str:
    """Step verdict from frame verdicts, biased against false passes: any fail -> fail, any unsure/invalid -> unsure."""
    if "fail" in verdicts:
        return "fail"
    return "pass" if verdicts and all(v == "pass" for v in verdicts) else "unsure"
