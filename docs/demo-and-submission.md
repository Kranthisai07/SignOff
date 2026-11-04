# demo-and-submission.md — Demo script and submission checklist

The 3-minute demo video is a primary artifact for judging (Demo 25%, and the final round is judged from videos). It may show **only what was built during the hackathon**; say so on screen.

## 3-minute script (adjust to real results; never show invented numbers)
| Time | Beat | Show |
|---|---|---|
| 0:00-0:20 | Problem: assistants talk you through tasks; nobody checks the work. One sentence on Signoff. | Title card + glasses on desk |
| 0:20-1:00 | Live: user does a step with the glasses, says/triggers "check", hears/sees **pass** with evidence frame + SAM mask | Glasses POV + laptop |
| 1:00-1:40 | Deliberate error (cable backwards). Signoff **fails** the step, explains why, blocks the next step. Fix it, re-check, pass | Same |
| 1:40-2:25 | Benchmark: false-pass rate and cost per correct verdict for configs A/B/(D), N shown, real numbers only | Frontier plot + table |
| 2:25-2:50 | Failure gallery: two cases where models failed and why; honesty caveats (single annotator, small N) | Screenshots |
| 2:50-3:00 | Open source: public repo, dataset, one-command rerun; built with Muse Spark / SAM 3.1 (/ Spark Open) | End card with repo URL |

If the live loop is not working (G3 failed): replace beats 2-3 with clips recorded on the glasses and replayed through the real pipeline; say "recorded on Ray-Ban Meta, verified by Signoff". Do not fake a live demo.

## Recording tips
Record the screen and glasses POV separately and edit; do a backup take; narrate clearly; keep text on screen readable at phone size; 3:00 is a hard cap; open the video link in a logged-out window to confirm it plays.

## X post (for the $20K Most Viral bonus; counts likes, reposts, comments to Nov 8 EOD)
- Post the demo video (short cut) on the user's X account after the submission is safe, with the repo link and the hackathon handle/hashtags the guide or Discord announces.
- Submit the post link on the hackathon platform. Lead with the failure moment (the caught error), not the happy path.

## Open-weights bonus ($10K) checklist
- A tier of the pipeline actually runs `meta-models/muse-spark-open-1026` via Baseten (or Modal/Fireworks) — not just mentioned.
- README states which step uses it and how to verify. Partner verifies eligibility; keep a log of calls.

## Agentic bonus ($5K) checklist
- README and video describe the agent loop: plan (spec) -> act (check) -> decide (advance/block/escalate) -> audit; autonomy level and practical use.

## Submission checklist (do by Wed Nov 4, 6 PM; deadline 9 PM ET)
- [ ] Meta API credits were claimed before Nov 4 9 PM
- [ ] Repo is **public**; README with setup, one-command rerun, what was built during the hackathon vs what is third-party (Meta SDK samples cited)
- [ ] No secrets in repo history (scan before making public)
- [ ] LICENSE added; dataset card included; consent/privacy note included
- [ ] Demo video <= 3:00, uploaded, link opens logged-out
- [ ] Everyone who worked on the project listed on the submission page (solo)
- [ ] Track = Indie; theme stated (Push the Frontier)
- [ ] X post link attached (if pursuing Viral)
- [ ] Submit at https://cerebralvalley.ai/e/meta-ai-developer-hackathon/hackathon/submit and confirm the platform shows it submitted
- [ ] Community vote: after submission, share the gallery link (one vote per verified account)
- [ ] `memory.md` updated with the final state
