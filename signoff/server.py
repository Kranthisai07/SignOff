"""Local verify endpoint for the glasses demo: python -m signoff.server  (run from the repo root).

POST /verify?step=<1-5> with a JPEG body -> JSON verdict. Binds to 127.0.0.1 only; the phone reaches it
over USB with `adb reverse tcp:8000 tcp:8000`, so the Meta API key never leaves this machine.
Each frame and verdict is kept under runs/live/ (gitignored) as an audit trail.
"""
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from signoff import verifier

PORT = 8000
MAX_BYTES = 8_000_000
LIVE = Path("runs/live")
SPEC = json.loads(Path("data/specs/fried-egg.json").read_text())
STEPS = {s["id"]: s for s in SPEC["steps"]}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict) -> None:
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self) -> None:
        url = urlparse(self.path)
        if url.path != "/verify":
            return self._send(404, {"error": "not found"})
        try:
            step = STEPS[int(parse_qs(url.query).get("step", [""])[0])]
        except (ValueError, KeyError):
            return self._send(400, {"error": f"step must be one of {sorted(STEPS)}"})
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BYTES:
            return self._send(413 if n > MAX_BYTES else 400, {"error": "body must be 1 byte to 8 MB"})
        img = self.rfile.read(n)
        if img[:2] != b"\xff\xd8":
            return self._send(400, {"error": "body must be a JPEG"})
        LIVE.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        frame = LIVE / f"{stamp}_s{step['id']}.jpg"
        frame.write_bytes(img)
        try:
            row = verifier.verify_frame(frame, f"{step['instruction']} Check: {step['check']}")
        except Exception as e:  # network/API failure: report it, never turn it into a verdict
            return self._send(502, {"error": f"verifier failed: {type(e).__name__}"})
        out = {"step": step["id"], "verdict": row["verdict"], "reason": row["reason"],
               "confidence": row["confidence"], "latency_ms": row["latency_ms"]}
        with open(LIVE / "log.jsonl", "a") as f:
            f.write(json.dumps({"frame": frame.name, **out}) + "\n")
        self._send(200, out)

    def log_message(self, fmt, *args) -> None:
        sys.stderr.write("[signoff] " + fmt % args + "\n")


if __name__ == "__main__":
    print(f"Signoff verify server on http://127.0.0.1:{PORT}  (adb reverse tcp:{PORT} tcp:{PORT})")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
