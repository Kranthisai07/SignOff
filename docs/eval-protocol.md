# eval-protocol.md — Dataset, labeling, harness, honesty rules

The benchmark is the main deliverable. Quality of data and honesty of numbers decide Technical Depth and Impact scores.

## Procedures (default; user may change)
Pick procedures with clear, visible end-states. Start easy; add subtle cases only if the model handles the easy ones (gate G1).
1. **Jetson Orin Nano camera install:** fan connector seated; camera ribbon cable inserted with correct orientation; connector latch closed; microSD inserted. (Needs the board — confirm the user has it; else substitute.)
2. **One laptop/PC task** with visible states (e.g. RAM stick seated and clips closed; cable connected). Confirm with the user.
Each procedure: 4-6 steps, one visually checkable outcome per step.

## Recording protocol
- Alone, indoors, good light, no faces, no personal screens. Keep the glasses' capture LED visible/on.
- Each run = one full pass through a procedure. Target about 25 runs total (about 12 per procedure).
- **About one third of runs contain one deliberate error** (skipped step, wrong order, wrong orientation, not fully seated, latch open). Vary the error type. Record which step is wrong.
- Per step, save 3-5 still frames taken after the user finishes the step (plus the raw clip). Name: `data/frames/<run_id>_s<step>_f<nn>.jpg`.
- Record some runs with the phone as backup POV camera. Note the source in `labels.csv`.

## Labeling
- Single annotator (the user). Label **truth** for every step instance: `pass` or `fail`, plus `error_type` for fails. Label before looking at any model output.
- Relabel a random 20% a day later; compute self-agreement and report it in the dataset card.
- Keep labels in `data/labels.csv` (schema in `specs.md`). Never put labels in model prompts.

## Harness configurations
| Id | Pipeline | Required? |
|---|---|---|
| A | Spark (contributor or standard) on raw frames + step check text | Must |
| B | Spark on SAM 3.1 crops + full frame + step check | Must |
| C | Wonder + SAM crops | Cut first |
| D | Router: tier 1 cheap (Spark Open via Baseten or contributor) -> tier 2 Spark 1.3 on unsure | Should |

## Metrics (per config, per procedure and overall)
- Accuracy, **false-pass rate** (truth=fail, verdict=pass) — the headline metric, false-fail rate, unsure rate.
- Latency p50/p95, and **cost per correct verdict** from measured usage only.
- Confidence intervals (Wilson) on every rate. Report N next to every number.
- A **failure gallery**: 4-6 steps where every config failed, with the reason (occlusion, glare, thin cable, ambiguous state).

## Honesty rules
- Only publish numbers produced by the harness on the committed data. No rounding up, no cherry-picking configs.
- State plainly: single annotator, small N, two procedures, one lighting setup.
- If B is not better than A, say so — that is a finding.
- Cost figures must come from logged usage; if unknown, write "not measured".

## Deliverables
`data/` (frames + labels + dataset card), `eval/` (harness + configs), `results/` (results.json, report.md, frontier plot), one command to rerun (cached, so it costs nothing after the first run).
