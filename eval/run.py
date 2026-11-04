"""Harness config A (Spark on raw frames). Usage: python -m eval.run   (reads data/labels.csv)

labels.csv `video` is a path under data/raw/: a video (uses t_start..t_end) or a single photo (jpg/png).
"""
import csv
import json
import math
import statistics
from pathlib import Path

from signoff import frames, verifier

RAW = Path("data/raw")
N_FRAMES = 3  # frames sampled per step from a video
PHOTO = {".jpg", ".jpeg", ".png"}


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return None
    p, d = k / n, 1 + z * z / n
    c, h = p + z * z / (2 * n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 3), round((c + h) / d, 3)]


def rate(k: int, n: int) -> dict:
    return {"k": k, "n": n, "rate": round(k / n, 3) if n else None, "wilson95": wilson(k, n)}


def score(rows: list[dict]) -> dict:
    """rows: {truth: pass|fail, verdict: pass|fail|unsure}. Unsure counts as not correct."""
    fails = [r for r in rows if r["truth"] == "fail"]
    passes = [r for r in rows if r["truth"] == "pass"]
    return {
        "accuracy": rate(sum(r["verdict"] == r["truth"] for r in rows), len(rows)),
        "false_pass_rate": rate(sum(r["verdict"] == "pass" for r in fails), len(fails)),
        "false_fail_rate": rate(sum(r["verdict"] == "fail" for r in passes), len(passes)),
        "unsure_rate": rate(sum(r["verdict"] == "unsure" for r in rows), len(rows)),
    }


def main() -> None:
    specs = {s["procedure_id"]: s for s in (json.loads(p.read_text()) for p in Path("data/specs").glob("*.json"))}
    out, lat, tok_in, tok_out = [], [], 0, 0
    for lab in csv.DictReader(open("data/labels.csv", newline="")):
        step = next(s for s in specs[lab["procedure_id"]]["steps"] if s["id"] == int(lab["step_id"]))
        media = RAW / lab["video"]
        if media.suffix.lower() in PHOTO:
            paths = [media]
        else:
            paths = frames.extract(media, float(lab["t_start"]), float(lab["t_end"]), N_FRAMES,
                                   RAW / "frames", f"{lab['run_id']}_s{lab['step_id']}")
        per = [verifier.verify_frame(p, f"{step['instruction']} Check: {step['check']}") for p in paths]
        lat += [v["latency_ms"] for v in per]
        tok_in += sum(v["usage"]["input_tokens"] for v in per)
        tok_out += sum(v["usage"]["output_tokens"] for v in per)
        out.append({"run_id": lab["run_id"], "step_id": int(lab["step_id"]), "truth": lab["truth"],
                    "error_type": lab["error_type"], "verdict": verifier.combine([v["verdict"] for v in per]),
                    "frame_verdicts": [v["verdict"] for v in per], "reasons": [v["reason"][:160] for v in per]})
    by_run = {r: score([o for o in out if o["run_id"] == r]) for r in sorted({o["run_id"] for o in out})}
    res = {"config": "A (Spark raw frames)", "model": verifier.MODEL, "prompt_version": verifier.PROMPT_VERSION,
           "annotator": "single (the user)", "rows": len(out), **score(out),
           "frame_latency_ms": {"p50": statistics.median(lat), "p95": sorted(lat)[int(0.95 * (len(lat) - 1))]} if lat else None,
           "tokens": {"input": tok_in, "output": tok_out}, "cost_usd": None, "by_run": by_run, "per_step": out}
    Path("results").mkdir(exist_ok=True)
    Path("results/results.json").write_text(json.dumps(res, indent=2))
    md = ["# Config A report", "", f"Rows: {len(out)} | single annotator | cost_usd not measured (null)", "",
          "| metric | k/n | rate | Wilson 95% |", "|---|---|---|---|"]
    md += [f"| {m} | {v['k']}/{v['n']} | {v['rate']} | {v['wilson95']} |"
           for m, v in res.items() if isinstance(v, dict) and "wilson95" in v]
    md += ["", "By batch (`run_id`):", "", "| batch | rows | accuracy | false-pass | false-fail | unsure |", "|---|---|---|---|---|---|"]
    md += [f"| {r} | {s['accuracy']['n']} | {s['accuracy']['k']}/{s['accuracy']['n']} | {s['false_pass_rate']['k']}/{s['false_pass_rate']['n']} "
           f"| {s['false_fail_rate']['k']}/{s['false_fail_rate']['n']} | {s['unsure_rate']['k']} |" for r, s in by_run.items()]
    Path("results/report.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
