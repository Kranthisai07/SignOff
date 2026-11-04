# plan.md — Phases, gates, cut list

Solo builder, Windows + Android phone, limited API credits (**$150 Meta, partner credits not guaranteed**). Deadline **Wed Nov 4, 9:00 PM ET**; target submit by **6 PM**. Tick boxes as work completes and mirror status in `memory.md`. Hours per day are unconfirmed (U) — ask the user and record in memory.md.

## Scope tiers
- **MUST (the project):** 2 procedures; about 25 recorded runs (roughly a third with injected errors); hand labels; harness comparing config A (model alone) vs B (model + SAM crops) reporting false-pass rate, accuracy, latency, cost; working end-to-end verifier on recorded clips; public repo; 3-minute demo video; submission.
- **SHOULD:** live glasses loop (capture -> verdict -> spoken/printed result -> audit log); router D with a cheap tier and escalation; open-weights tier through Baseten (bonus).
- **CUT FIRST, in this order:** voice commands -> Wonder arm (config C) -> router threshold calibration -> third procedure -> extra polish. Never cut: the labeled data, the harness, the demo video, the submission.

## Budget rules
- Total Meta credits $150. Reserve $30 for final reruns + demo. Any sweep estimated above $10 requires asking the user. Cache SAM outputs and verdicts keyed by (frame hash, model, prompt version) so reruns cost nothing.
- Sample 3-5 frames per step, not every frame.

## Dev-tooling budget (separate from the Meta runtime budget)
The coding agent runs on Qwen via OpenRouter. The user sets an OpenRouter spend limit before starting; record the limit and spend in `memory.md`. Prefer small prompts, re-read files instead of long chat history, and refresh context from `memory.md` often. Escalate to a stronger model only after 2 failed attempts and only with the user's OK.

## Gates (a gate is passed only with evidence recorded in memory.md)
| Gate | Test | Pass condition | If it fails |
|---|---|---|---|
| **G-1** (30 min) | Qwen via OpenRouter inside Claude Code | `/status` shows base URL `https://openrouter.ai/api`; Qwen completes one small tool-using task (read a file, edit it, run a command and report real output); one subagent call works; Activity dashboard shows the Qwen slug | Set all model-slot vars + `CLAUDE_CODE_SUBAGENT_MODEL`; try `qwen/qwen3-coder` or `qwen3-coder-next`; else use Sonnet for this repo and note the extra cost |
| **G0** | Credits claimed, key works | One successful `muse-spark-1.3` call; billing shows credits | Escalate to user / Discord #questions |
| **G1** | Spark on 10 hand-labeled photos | Valid JSON verdict; >= 7/10 correct | Switch to steps with clearer visual end-states; try standard instead of contributor tier |
| **G2** | SAM 3.1 on "ribbon cable" photo | Usable mask in <= 3 prompt tries | Skip crops (use bounding box or no crops); keep SAM for evidence overlay only |
| **G3** | One frame from glasses into backend (Android app, Developer Mode, IDs "0") | A frame file saved on the PC from the glasses | **Hard deadline: end of Wed Oct 28.** Fall back to glasses clips uploaded after recording; drop live loop |
| **G4** | First full harness run | Real numbers for A and B on >= 15 steps | Fix data/labels first, then prompts |

## Schedule (ET)
| Date | Focus | Exit condition |
|---|---|---|
| Mon Oct 26 (evening) | Setup: claim all credits, new repo, Android Studio, Developer Mode, G0/G1/G2 | G0, G1, G2 recorded in memory.md |
| Tue Oct 27 | Spec compiler + schema; write 2 SOPs; start G3 (clone CameraAccess sample, run with "0" IDs); attend Agents 101 | spec.json validates; G3 attempt logged |
| Wed Oct 28 | G3 decision by EOD; attend Agents 102 (verifiable agents); record first 10 runs | G3 pass/fail decided; 10 labeled runs |
| Thu Oct 29 | Record remaining runs, label everything; verifier configs A, B | 25 runs labeled; A/B code runs |
| Fri Oct 30 | Full sweep A vs B; error analysis of false passes; request Baseten credits if not done | G4 passed; first results |
| Sat Oct 31 | Router D (tier 1 cheap, tier 2 Spark 1.3); open-weights tier if Baseten approved | D results or documented cut |
| Sun Nov 1 | Live loop end-to-end if G3 passed; rehearse demo procedure 5 times | demo runs 3 times in a row |
| Mon Nov 2 | **Feature freeze.** Dataset card, README with one-command rerun, cleanup | `make eval` reproduces numbers |
| Tue Nov 3 | Record 3-minute demo + backup take; post demo on X; submit draft on platform | video uploaded, link opens logged-out |
| Wed Nov 4 | Final checks; **submit by 6 PM**; Discord final office hours | Submission confirmed on platform |

## Definition of done per gate
Code runs from a clean checkout, result recorded in `memory.md` with the command used and the measured output, decision logged if an approach changed, no secrets in the diff.

## Risks and standing mitigations
- Glasses toolkit too hard -> G3 fallback; the benchmark is the main deliverable.
- Model cannot separate good/bad states -> pick procedures with larger visual differences (latch open/closed, cable present/absent) before adding subtle ones.
- Credits run out -> smaller sample, cache, escalate to user; never spend past the reserve silently.
- Looks like a Live AI clone -> demo opens with a model failure and the false-pass number.
- Single annotator / small N -> say so in the dataset card and use confidence intervals.
