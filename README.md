# Signoff

Signoff checks, from a photo or video, whether a hands-on procedure step was actually done correctly. It sends the frame and the step's pass criterion to a Meta model and gets back `pass`, `fail` or `unsure`, with a short reason. Entry for the Meta Global AI Developer Hackathon, Indie track, theme "Push the Frontier".

The point is the measurement. A verifier that says "pass" too early is worse than none, so the headline metric is the **false-pass rate**: how often a step that was done wrong is signed off anyway. Signoff reports it with confidence intervals and says plainly how small the data is.

## What is built (and what is not)

| Part | Status |
|---|---|
| Verifier: `muse-spark-1.3` on one frame plus a step spec (`signoff/verifier.py`) | **Built and measured** |
| Frame sampling from video with ffmpeg (`signoff/frames.py`) | Built, self-checked on a synthetic video, **not yet run on real video** |
| Harness: accuracy, false-pass, false-fail, unsure rates with Wilson 95% intervals (`eval/run.py`) | **Built and run on 20 labeled photos** |
| Fried-egg procedure spec, 5 steps (`data/specs/fried-egg.json`) | Built |
| Glasses capture: a patch to Meta's CameraAccess sample plus a local verify server (`signoff/server.py`, `android/`) | Server tested; the patched app builds and streams from the glasses on a Galaxy S25 Ultra and Ray-Ban Meta Gen 2. A photo captured on the glasses has made the full round trip to a verdict in the app (one test, on a non-egg scene; not yet measured on real egg steps) |
| SAM 3.1 crops, model router, spec compiler, step state machine | **Not built.** `signoff/router.py`, `spec_compiler.py` and `state_machine.py` are empty placeholders |
| Open-weight arm (Spark Open via a partner) | Not built, no claim made |

So today Signoff is a verifier plus an honest benchmark of it on still photos. It is not yet an agent loop, and there is no live glasses app. Twenty of the 30 photos were captured with Ray-Ban Meta (Gen 2) glasses (first-person view; ten earlier, ten live through the app); the other 10 with a fixed camera.

Product code calls Meta models only (`muse-spark-1.3` through `https://api.meta.ai/v1/responses`). All code in this repo was written during the hackathon. Nothing was copied from another project.

## Result (config A: Spark on a raw photo, one call per photo)

Run on 30 labeled photos of a fried-egg procedure: 20 earlier photos plus 10 captured live through the glasses app (`results/report.md`):

| metric | k/n | rate | Wilson 95% |
|---|---|---|---|
| accuracy | 29/30 | 0.97 | 0.83 to 0.99 |
| false-pass rate (wrong step called pass) | 0/14 | 0.00 | 0.00 to 0.22 |
| false-fail rate (right step called fail) | 1/16 | 0.06 | 0.01 to 0.28 |
| unsure rate | 0/30 | 0.00 | 0.00 to 0.11 |

By batch: `egg1` 10/10 (glasses stills), `egg2` 10/10 (fixed camera), `egg4` 9/10 (captured live through the app, a different stove and pan). The one miss is a **false fail**: an oiled pan photographed in dim light, before the stove light was turned on, was called dry. The oil is not visible in that frame, so "unsure" would have been the better answer; the same pan passed once the light was on.

- Latency per call: median about 4.1 s, p95 about 8.0 s.
- Tokens recorded across the 30 verdicts: 50,774 input, 9,586 output. **Dollar cost per verdict is not reported**: the API response has no cost field and no price was confirmed, so `cost_usd` is `null`.

**How to read this.** 30 rows from one annotator in two kitchen setups. Zero false passes only bounds the true false-pass rate at about 22% or less (95%), it does not show it is zero. One photo was dropped from the set before the final run because its label was ambiguous (see `docs/decisions.md`, D-013); without that decision the earlier run was 9/10. The live batch has no S4 fail photo: a clearly burnt edge was not captured, and three unclear S4 frames were left out rather than labeled. The photos are stills with clear contrast between pass and fail. Real first-person video, with motion and awkward angles, is untested. Details and limits are in [DATASET_CARD.md](DATASET_CARD.md).

## Rerun

Needs Python 3.11, ffmpeg (only for video input), and a Meta Model API key.

```
pip install -r requirements.txt
echo META_API_KEY=your_key_here > .env      # .env is gitignored
python -m eval.test_selfcheck               # no API calls, prints "selfcheck ok"
python -m eval.run                          # reads data/labels.csv, writes results/results.json and results/report.md
```

- `data/labels.csv` lists each row: step, truth, and the image filename under `data/raw/`. **The 20 egg photos are not published in this repo**, so the 20/20 result cannot be reproduced from a clean clone. To run on your own data, put photos in `data/raw/` and list them in `data/labels.csv` following `data/sop_fried_egg.md`. The self-check needs no photos.
- A full run on the original photos makes 30 API calls. Verdicts are cached in `results/cache/` (keyed on the image bytes, step text, model and prompt version), so a rerun of the same data costs nothing.
- `python -m eval.g1` is the retired engine-oil experiment. It is kept only as a record of a negative finding: Spark returned fail on all 10 photos because the dipstick details were too small to read in wide shots.

## How a verdict is made

1. The step spec gives an instruction and a check, for example "Cook until the whites are fully set. Check: the egg white is opaque white, not clear or glossy."
2. One image goes to `muse-spark-1.3` with `reasoning.effort = low` and a JSON-only reply format.
3. The reply is parsed to `pass | fail | unsure` plus reason and confidence. Unparseable replies count as `unsure`.
4. For video, three frames are sampled from the step's time range and combined: any `fail` makes the step `fail`, any `unsure` makes it `unsure`, otherwise `pass`. This rule leans against false passes and is untuned.

## Privacy

Photos are indoors, no faces, no screens with private data. Some show a forearm or feet and the stove clock. Photos were sent to the Meta Model API for verification; how Meta handles contributor-tier data is governed by Meta's terms and has not been independently checked here.

## Layout

```
signoff/   meta_client.py, verifier.py, frames.py   (router, spec_compiler, state_machine are placeholders)
eval/      run.py (harness), test_selfcheck.py, g1.py (retired)
data/      specs/fried-egg.json, labels.csv, sop_fried_egg.md, raw/ (images, not published)
docs/      decisions.md (what/why/alternatives log), memory.md (project state)
```

License: MIT, see [LICENSE](LICENSE).
