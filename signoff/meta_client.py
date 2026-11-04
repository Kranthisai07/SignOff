"""Client for the Meta Model API (https://api.meta.ai/v1)."""
import os
import time
from pathlib import Path

import httpx

BASE_URL = "https://api.meta.ai/v1"


def _load_env() -> None:
    # shortcut: minimal KEY=VALUE parser, strips one pair of surrounding quotes, no export support; swap for python-dotenv if .env grows
    path = Path(__file__).resolve().parent.parent / ".env"
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                v = v.strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                os.environ.setdefault(k.strip(), v)


def create_response(model: str, input, timeout: float = 60.0, **extra) -> tuple[dict, int]:
    """POST /v1/responses. Returns (raw response JSON, latency_ms). Raises on HTTP error."""
    _load_env()
    key = os.environ.get("META_API_KEY")
    if not key:
        raise RuntimeError("META_API_KEY not set")
    t0 = time.perf_counter()
    r = httpx.post(
        f"{BASE_URL}/responses",
        headers={"Authorization": f"Bearer {key}"},
        json={"model": model, "input": input, **extra},
        timeout=timeout,
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)
    r.raise_for_status()
    return r.json(), latency_ms
