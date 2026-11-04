# specs.md — Architecture, contracts, verified facts

**(V)** = verified from official pages on Oct 26, 2026. **(U)** = unverified; measure or confirm before relying on it.

## 1. System overview
```
SOP text --(Muse Spark)--> spec.json (per-step checks)
Glasses camera --(DAT toolkit, Android app)--> frames --> backend (FastAPI)
backend: for step N:
   SAM 3.1 (text prompts from spec) -> crops/masks
   verifier tier 1 (cheap)  -> verdict {pass|fail|unsure, reason, confidence}
   if unsure/low confidence -> tier 2 (stronger) -> verdict
   state machine: advance on pass, block on fail, ask re-check on unsure
   audit log: verdict + evidence frame + mask + model + cost + latency
Offline: harness replays labeled clips through configs A-D and writes metrics.
```
Components: (1) Android capture app (Kotlin, thin), (2) Python backend + verifier + router, (3) spec compiler, (4) eval harness + dataset, (5) demo UI (minimal; terminal or one web page).

## 2. Models and tiers
| Role | Model id | Notes |
|---|---|---|
| Spec compiler, verifier tier 2, default | `muse-spark-1.3` | via Meta Model API (V id) |
| Cheap verifier / sweeps | `muse-spark-1.3-contributor` | discounted; (U) contributor calls may be used by Meta to improve products — keep faces/screens out of frame, confirm terms |
| Escalation / reference judge | `muse-wonder-1.0` | "in preview" (V); cut first if credits are short |
| Segmentation / crops | `sam-3.1` | text prompt + image/video in, boxes + masks out (V); endpoints `POST /v1/responses`, `POST /v1/files` (V) |
| Open-weights tier 1 (bonus) | `meta-models/muse-spark-open-1026` | served by **Baseten** (V). Spark Open and Glimmer are **not** served by Meta Model API (V) |
| Voice (optional, cut first) | `muse-voice-transcribe-1.0` | $0.18/hour audio (V) |

Meta Model API: base URL `https://api.meta.ai/v1`, bearer-token auth, same for all models (V). Image input is supported for Spark ("image understanding", V) but format/size limits and **per-image cost and rate limits are (U)** — measure in gate G1 and write real numbers into `memory.md`.

## 2b. Dev tooling vs product runtime
| | Dev tooling (builds the code) | Product runtime (what Signoff calls) |
|---|---|---|
| Models | Qwen coder via OpenRouter (default slug `qwen/qwen3-coder-plus`; alternatives that exist on OpenRouter: `qwen/qwen3-coder`, `qwen/qwen3-coder-next`, `qwen/qwen3-coder-flash`). Prices, context size and quality vs Sonnet are (U) until gate G-1 and a real task | Meta only: `muse-spark-1.3`, `muse-spark-1.3-contributor`, `sam-3.1`, optional Wonder; Spark Open via Baseten |
| Billing | OpenRouter account (user sets a spend limit) | Meta Model API credits (about $150) |
| Fallback | Sonnet for hard debugging (ask the user first) | none; Meta models are a hackathon requirement |

Claude Code on OpenRouter (V, OpenRouter docs): `ANTHROPIC_BASE_URL=https://openrouter.ai/api` (no `/v1`), `ANTHROPIC_AUTH_TOKEN=<OpenRouter key>`, `ANTHROPIC_API_KEY=""` (must be empty). Set every model slot you use: `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, and `CLAUDE_CODE_SUBAGENT_MODEL`. Claude Code assumes a 200k context unless the slug ends in `[1m]`. Verify with `/status` (expect auth token from `ANTHROPIC_AUTH_TOKEN` and base URL `https://openrouter.ai/api`) and the OpenRouter Activity dashboard. OpenRouter warns Claude Code "may not work correctly with other providers"; tool use, subagents and caching with Qwen are (U) until tested.

PowerShell (user runs this themselves; never paste the real key into a doc or chat):
```powershell
$env:OPENROUTER_API_KEY = "<paste key here, locally only>"
$env:ANTHROPIC_BASE_URL = "https://openrouter.ai/api"
$env:ANTHROPIC_AUTH_TOKEN = $env:OPENROUTER_API_KEY
$env:ANTHROPIC_API_KEY = ""
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "qwen/qwen3-coder-plus"
$env:CLAUDE_CODE_SUBAGENT_MODEL = "qwen/qwen3-coder-plus"
claude
```
If previously logged in with an Anthropic account: `/logout`, quit, relaunch.

## 3. Glasses integration (V unless marked)
- SDK: Meta Wearables Device Access Toolkit (DAT) for Android, from **Maven Central**, group `com.meta.wearable`; modules incl. core, camera, mockdevice, speech. Repo: https://github.com/facebook/meta-wearables-dat-android (has `samples/`, CameraAccess sample referenced in Meta docs). Gradle example pins `mwdat = "1.0.1"`; confirm latest on Maven Central. Developer preview — cannot publish to stores (irrelevant for the demo).
- Supported glasses: Ray-Ban Meta Gen 1/2, Ray-Ban Meta Optics, Meta Ray-Ban Display, Oakley Meta HSTN/Vanguard.
- Requirements: Android 10+, Android Studio (Flamingo or newer), Meta AI app v254+, glasses firmware v20+ (Ray-Ban Meta). Supported-country requirement (US is fine).
- **Developer Mode**: Meta AI app -> Settings -> App Info -> tap App version 5 times -> toggle Developer Mode on -> Enable. Glasses must be connected. The app then shows under App connections -> Developer mode apps.
- **In Developer Mode set `APPLICATION_ID` and `CLIENT_TOKEN` to `"0"`** (manifest placeholders `mwdat_application_id`, `mwdat_client_token`); no attestation. Real IDs only for non-Developer-Mode apps via the Wearables Developer Center. No approval is needed to build/test on your own glasses.
- Manifest: Bluetooth + Bluetooth-connect + Internet permissions; a custom callback URL scheme so Meta AI can return to the app. Optional phone-camera mock device feed for testing without glasses.
- Camera stream: up to **720p, 30 FPS over Bluetooth**, auto-reduced when bandwidth is limited (V from third-party article, older version — measure real fps/resolution in G3). Mic/speakers go through normal Bluetooth profiles.
- Dev machine: Windows + Android Studio + a physical Android phone. iPhone/Mac are fallbacks only (iOS needs Xcode).
- Fallback path if streaming fails: record with the glasses' built-in capture, sync via Meta AI app, upload clips (clip length limit (U) about 60 s — check).

## 4. Data contracts
### spec.json (output of the spec compiler)
```json
{
  "procedure_id": "jetson-camera-install",
  "title": "Install camera ribbon cable on Jetson Orin Nano",
  "steps": [
    {
      "id": 2,
      "instruction": "Insert the camera ribbon cable with contacts facing the board",
      "check": "Ribbon cable fully seated; stiffener faces away from the board; latch closed",
      "sam_prompts": ["ribbon cable", "camera connector"],
      "failure_modes": ["inserted backwards", "not fully seated", "latch open"],
      "depends_on": [1]
    }
  ]
}
```
Validate with a JSON schema on every compile; retry once on invalid output.

### verdict.json (output of a verifier call)
```json
{
  "run_id": "r012", "step_id": 2, "tier": "spark-1.3-contributor",
  "verdict": "fail",
  "reason": "contacts face upward; stiffener is toward the board",
  "confidence": 0.82,
  "evidence": {"frame": "frames/r012_s2_f03.jpg", "mask": "masks/r012_s2_f03.png"},
  "cost_usd": null, "latency_ms": 0
}
```
`verdict` is exactly `pass | fail | unsure`. `cost_usd` is filled only from measured token/image usage; keep `null` if unknown. Never fabricate.

### label row (hand-labeled ground truth, `data/labels.csv`)
`run_id, procedure_id, step_id, truth (pass|fail), error_type, annotator, notes`

### audit log
One JSON line per verdict, append-only, at `runs/<run_id>/audit.jsonl`.

## 5. Router policy
1. Tier 1 verdict. 2. If `unsure` or `confidence < T`, escalate to tier 2. 3. If still unsure, state machine asks the user to re-check (new frames). **T is calibrated in the harness** to hit a target false-pass rate (e.g. <= 5%) at the lowest cost — only if the Should/Stretch scope is reached; otherwise use a fixed T and say so.

## 6. Harness configurations and metrics
- A: Spark on raw frames. B: Spark + SAM crops. C: Wonder + SAM crops (cut first). D: router (tier 1 Spark Open or contributor, tier 2 Spark 1.3).
- Metrics per config: accuracy, **false-pass rate** (truth=fail, verdict=pass), false-fail rate, unsure rate, p50/p95 latency, **cost per correct verdict**, with confidence intervals (small N: use Wilson intervals; state single annotator).
- Output: `results/results.json` + `results/report.md` + frontier plot PNG. One command reruns everything (`make eval` or `python -m signoff.eval`).

## 7. Repo layout (target)
```
signoff/            python package: spec compiler, verifier, router, state machine, meta client
android/            thin Kotlin capture app (from Meta's CameraAccess sample)
data/               raw clips (gitignored if large), frames, labels.csv, dataset card
eval/               harness, configs, results
docs/               these project docs
```
Tech: Python 3.11+, FastAPI, httpx, pydantic. Keep dependencies minimal. Secrets in `.env` (gitignored).

## 8. Open items (U) — resolve and record in memory.md
Per-image / per-token cost; rate limits; Spark image size limits; contributor-tier terms; real fps/resolution from glasses; whether SAM 3.1 returns a usable mask for thin cables; Baseten credit approval.
