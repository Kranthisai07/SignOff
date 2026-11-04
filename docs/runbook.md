# runbook.md — When something breaks, do this

Work top-down: find the symptom, do the first action, record the outcome in `memory.md`, and log a decision if you change approach. If two actions fail, stop and ask the user. Never burn credits retrying blindly.

## Meta Model API
| Symptom | Likely cause (hypothesis, test it) | Action |
|---|---|---|
| 401 / 403 | Key missing, wrong env var, credits not applied, no payment method on file | Check `.env` is loaded (print only "set/not set"). Billing page must show credits and a card. Claim form submitted? |
| 429 / rate limit | Contributor tier token window (U) or burst | Back off with jitter; cache; run sweeps in small batches; switch tier only after asking |
| 404 model not found | Wrong id | Use ids in `specs.md`; check https://dev.meta.ai/docs/models |
| Invalid JSON verdict | Model ignored schema | Retry once with the schema in the prompt and "JSON only"; lower temperature; if still invalid, record as `unsure` and count it |
| Image rejected / too large | Size/format limits (U) | Downscale to <= 1280 px long edge JPEG; record the working limit in memory.md |
| Cost higher than estimated | Image tokens larger than assumed | Stop the sweep; record measured cost per call; shrink sample; ask user before continuing |
| Credits nearly gone | | Freeze sweeps; use cached results only; request more via Discord #questions (not guaranteed) |

## OpenRouter / Claude Code (dev tooling)
| Symptom | Action |
|---|---|
| Auth error / 401 | Define `OPENROUTER_API_KEY` before `ANTHROPIC_AUTH_TOKEN`; `ANTHROPIC_API_KEY` must be empty; `/logout` if an Anthropic login exists; relaunch `claude` |
| `/status` shows wrong base URL or key source | Env vars not loaded in this shell; set them in the same PowerShell window and relaunch (do not rely on `.env`) |
| "model not found" | Set every model-slot variable you use (`ANTHROPIC_DEFAULT_SONNET_MODEL`, `_OPUS_`, `_HAIKU_`, `CLAUDE_CODE_SUBAGENT_MODEL`) to a valid slug |
| Tool calls fail / agent loops / edits wrong files | Likely model-compat issue (OpenRouter warns about non-Anthropic models). Try `qwen/qwen3-coder` or `qwen3-coder-next`; shrink the task; if still failing after 2 attempts, ask the user to switch to Sonnet for this task |
| Context errors on long sessions | Claude Code assumes 200k; start a fresh session and reload from `memory.md` |
| Wrong model billed | Check the OpenRouter Activity dashboard model column |
| Dev cost spike | Stop; check the Activity dashboard; shorten prompts; ask the user to raise or keep the spend limit |

## SAM 3.1
| Symptom | Action |
|---|---|
| No mask / empty result | Try 2 other text prompts ("flat flex cable", "connector"); if still nothing, use bounding box or skip crops (config B becomes A) |
| Mask covers wrong object | Add a second prompt to disambiguate; log failure in the failure gallery (useful for the demo) |

## Glasses / Android
| Symptom | Action |
|---|---|
| App cannot register with glasses | Developer Mode on? Glasses connected in Meta AI app (v254+), firmware v20+? Callback URL scheme set? IDs are "0"? |
| Gradle can't resolve `com.meta.wearable` | `mavenCentral()` in `settings.gradle.kts`; check the version on Maven Central |
| No frames / black frames | Try the phone-camera mock device to isolate app vs glasses; check Bluetooth permissions; reduce requested resolution/fps |
| Low fps / blurry | Expected over Bluetooth (up to 720p/30 fps, auto-reduced); capture fewer, sharper frames at step end |
| Not working by **end of Wed Oct 28** | Invoke fallback: record with the glasses' built-in capture, sync via Meta AI app, upload clips. Log decision. Drop the live loop |
| Emulator suggested | Do not rely on it — glasses pair over Bluetooth with a real phone |

## Backend / harness
| Symptom | Action |
|---|---|
| Results differ between runs | Fix seeds, cache by (frame hash, model, prompt version); report variance |
| False-pass rate looks too good | Check label leakage (labels in prompt?), tiny N, duplicate frames; report confidence intervals |
| Harness slow / expensive | Cache first; sample frames; run overnight |

## Process
| Situation | Action |
|---|---|
| New model session / switched model | Read `CLAUDE.md` then `memory.md`. Do not trust your own recollection |
| Docs and code disagree | Trust code; fix docs; note in memory.md |
| Unsure whether something is allowed | Check `rules.md`; if still unsure ask in Discord #questions and the user |
| About to commit | Confirm diff = intended files only, no secrets, no AI attribution lines |
| Out of time | Apply the cut list in `plan.md`; protect: labeled data, harness numbers, demo video, submission |
