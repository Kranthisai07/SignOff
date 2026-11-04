# Dataset card: Signoff fried-egg step photos

## Summary
30 labeled still photos of a fried-egg procedure, used to measure how often a Meta model (`muse-spark-1.3`) wrongly signs off a step that was done wrong. Each row is one photo judged against one step of a 5-step spec. Labels are `pass` or `fail`.

| Step | Instruction | pass rows | fail rows |
|---|---|---|---|
| S1 | Put oil in the pan | 4 | 3 (dry pan x2; water droplets, not oil) |
| S2 | Crack the egg in, no shell | 3 | 3 (shell fragment on or in the egg) |
| S3 | Cook until the whites are fully set | 3 | 3 (whites clear and glossy; whites half set; raw whites) |
| S4 | Finish without burning | 3 | 2 (dark brown or black edges; one side black) |
| S5 | Plate the egg | 3 | 3 (egg still in the pan, plate empty) |

Files: `data/labels.csv` (one row per photo, columns `run_id, procedure_id, step_id, truth, error_type, annotator, notes, video, t_start, t_end`), `data/specs/fried-egg.json` (step text and checks), `data/sop_fried_egg.md` (what pass and fail look like), images named `egg_s<step>_<pass|fail>_<n>.jpg` under `data/raw/`. **The images are not published**; the repo holds the labels, specs and results only.

## How it was collected
- **Batch `egg1` (10 photos):** first-person photos captured with Ray-Ban Meta (Gen 2) glasses while cooking at the stove, looking down at the pan (the annotator's forearm is sometimes in frame). Original files were mostly portrait, up to about 1200 px wide.
- **Batch `egg2` (10 photos):** taken with a fixed camera on a stand, which is why the angle and the egg outline are the same across them. Originals were 1536 x 1024.
- **Batch `egg4` (10 photos):** captured live with Ray-Ban Meta (Gen 2) glasses through the Signoff app (`android/`) while cooking, in a second kitchen setup (a different stove and pan, dimmer light). The app resized each frame to at most 1288 px; labels come from the annotator's notes at capture time. One of the ten (an oiled pan photographed in dim light before the stove light was on, `egg_s1_pass_4b`) is a model miss, kept in on purpose; the oil is not visible in that frame, so "unsure" would have been the better answer. No clearly burnt-edge (S4 fail) frame was captured. Left out of the labeled set: three S4 frames where the annotator saw a black edge but the egg edge looked pale in the photo, two non-egg frames, one broken-egg frame, two near-duplicate S3 fails of the same egg, and one repeat dry-pan S1 frame.
- Images were resized to at most 1288 px on the long side before being sent to the model (batch 2 was converted to JPEG for that; batch 1 was already smaller).
- Failures were staged on purpose (dry pan, shell added, undercooked whites, overcooked edges, egg left in the pan).

## Labels
- One annotator, the person who took the photos. There is no second rater, so label noise cannot be measured.
- Truth for most rows comes from the annotator's own filename for each photo. Three labels were mapped by the builder from a filename that did not say pass or fail, and are borderline: "crisp brown edge" labeled S4 fail, "half sets white" labeled S3 fail, "Crispy-Edged Sunny-Side-Up Egg" labeled S4 pass. Treat those three as the weakest rows.
- **One photo was removed** from the set after a first run ("Brown Edge", intended as S4 fail): neither the annotator nor the builder could see dark edges on the egg, so the label was doubtful. It was the only photo the model got wrong, so removing it moved accuracy from 9/10 to 9/9 on the first 10 rows. The file is kept in the raw folder but not in `labels.csv`. See `docs/decisions.md`, D-013.

## What it is good for, and what it is not
- Good for: a first, small measurement of false-pass and false-fail rates for one model on obvious-to-subtle visual differences in one cooking task, with confidence intervals.
- Not good for: claims about real first-person video, other kitchens, other pans or lighting, other procedures, or other models. The 30 photos come from two stove and pan setups (batches 1 and 2 share one; batch 4 is another). Contrast between pass and fail is mostly clear. The 95% interval on the false-pass rate is 0 to 0.22 even with 0 observed errors.
- No dollar cost per verdict: the API returns token counts but no price, and no price was confirmed.

## Privacy and consent
Indoors, alone, no faces and no screens with private data. Some batch 1 photos show the annotator's forearm or feet and the stove's clock. No other people. The photos were sent to the Meta Model API to get verdicts; use of that data is governed by Meta's terms, which have not been independently checked here.

## License
Code is MIT (see `LICENSE`). The photos are not published, so no image license applies.
