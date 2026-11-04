"""Gate G1: run Spark on hand-labeled photos, cache verdicts. Usage: python -m eval.g1"""
import base64
import json
from pathlib import Path

from signoff.meta_client import create_response

MODEL = "muse-spark-1.3"
RAW = Path("data/raw")
OUT = Path("runs/g1/verdicts.jsonl")

STEPS = {
    "S1": "After pulling the dipstick out, it must be wiped completely clean with a rag so no oil film remains on the rod.",
    "S2": ("Oil level reading: the dipstick has two holes marking the low and full limits. After wiping and re-dipping, "
           "the oil on the rod must reach between the two holes. A clean, dry rod, or any photo where the oil level on "
           "the rod cannot be seen, does not count as a valid reading."),
}
FORMAT = 'Reply with JSON only: {"verdict":"pass|fail|unsure","reason":"...","confidence":0.0}'

PHOTOS = [
    ("after_wipe_stick_photo", "S1"), ("stick_after_wiping", "S1"), ("stick_with_oil", "S1"),
    ("full_stick_with_oil_without_wiping", "S1"), ("fullstick_without_wiping2", "S1"),
    ("oil_check_photo", "S2"), ("oil_check_photo_2", "S2"), ("low_oil_photo", "S2"),
    ("low_oil_photo_2", "S2"), ("reinsert_stick_photo", "S2"),
]


def parse(text: str) -> dict:
    try:
        return json.loads(text.strip().removeprefix("```json").removesuffix("```").strip())
    except json.JSONDecodeError:
        return {"verdict": "invalid", "reason": text[:200], "confidence": None}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = {(r["photo"], r["step"]) for r in map(json.loads, OUT.read_text().splitlines())} if OUT.exists() else set()
    for photo, step in PHOTOS:
        if (photo, step) in done:
            continue
        b64 = base64.b64encode((RAW / f"{photo}.jpg").read_bytes()).decode()
        prompt = f"Procedure step: {STEPS[step]} Judge from the photo whether this step was done correctly. {FORMAT}"
        inp = [{"role": "user", "content": [{"type": "input_text", "text": prompt},
                                            {"type": "input_image", "image_url": "data:image/jpeg;base64," + b64}]}]
        data, ms = create_response(MODEL, inp, reasoning={"effort": "low"})
        text = next(c["text"] for o in data["output"] if o["type"] == "message" for c in o["content"])
        row = {"photo": photo, "step": step, "model": MODEL, "latency_ms": ms, "usage": data["usage"], **parse(text)}
        with OUT.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(photo, step, row["verdict"], row["confidence"], "|", row["reason"][:110])


if __name__ == "__main__":
    main()
