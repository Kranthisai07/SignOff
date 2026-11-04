# Storyboard v4: Signoff showcase (3:00)

Built with HyperFrames in `D:/signoff-video/film` (outside the repo; frames are unpublished): one composition per scene, rendered at 1920x1080 30 fps h264, joined losslessly by `merge.py`, voiceover by ElevenLabs (Sarah on `eleven_v4`, Chris for the user's request) from `script.json`, mixed to -16 LUFS. Order lives in `order.json`.

This cut is a product showcase. Limitations (the dropped label, the dim-light miss, the engine-oil attempt, the missing live burnt-edge photo, confidence intervals) are documented in README and DATASET_CARD, not in the video. Rules that still hold: every number and quote on screen comes from the logs by script; scene 2 keeps the VISION chip until the guided start is built and recorded; no claims about SAM, an agent loop, open weights or cost.

| # | Scene | Time | What is on screen |
|---|---|---|---|
| 1 | `scene01` | 0:00.0-0:12.0 | Hook: YOUR GLASSES SEE EVERYTHING YOU DO, then DO THEY KNOW IF YOU DID IT RIGHT? |
| 2 | `scene02` | 0:12.0-0:30.0 | Meet Signoff (VISION chip: the guided voice start is not built yet): 'Hey Meta, help me make a fried egg', the plan slides in, MEET SIGNOFF. |
| 3 | `scene03plan` | 0:30.0-1:00.0 | FIVE STEPS. FIVE CHECKS.: one card per step with the instruction, its DONE RIGHT check and the real glasses PASS frame |
| 4 | `scene03` | 1:00.0-1:25.0 | How Signoff sees: glasses, phone app, local server, Muse Spark, verdict |
| 5 | `scene04` | 1:25.0-2:20.0 | The real cook: S1-S5 HUD over the live glasses frames, ending SIGNED OFF (tagged 'recorded run, real verdicts') |
| 6 | `scene05` | 2:20.0-2:45.0 | Proof: 30 photos, 29 correct; 0 / 14 wrong steps signed off; 4.1 s median; 20 / 30 from the glasses |
| 7 | `scene07` | 2:45.0-3:00.0 | Close: SIGNOFF. DONE RIGHT. SIGNED OFF. Credits incl. 'Voiceover: AI voice (ElevenLabs)' |

## Voiceover (generated from `script.json`)

| Time | Scene | Line |
|---|---|---|
| 0:00.3 | `scene01` | Your glasses see everything you do. Every step, every slip. |
| 0:05.1 | `scene01` | But do they actually know if you did it right? That's exactly the question we set out to answer. |
| 0:12.6 | `scene02` | Hey Meta, help me make a fried egg. *(user)* |
| 0:15.2 | `scene02` | And just like that, it builds a plan for you, step by step. |
| 0:19.7 | `scene02` | Meet Signoff. A second pair of eyes for anything you do with your hands. It plans the steps, watches each one, and signs off only when it's right. |
| 0:30.3 | `scene03plan` | Here's the plan: five steps, each with its own picture of done right. |
| 0:36.0 | `scene03plan` | First, oil in the pan. Done right means a visible sheen. |
| 0:40.7 | `scene03plan` | Second, crack the egg in, with no shell along for the ride. |
| 0:45.0 | `scene03plan` | Third, the one everyone rushes: whites fully set. |
| 0:49.5 | `scene03plan` | Fourth, finish it golden, never burnt, right to the edges. |
| 0:54.1 | `scene03plan` | Fifth, onto the plate. |
| 0:56.4 | `scene03plan` | And Signoff checks every single one. |
| 1:00.3 | `scene03` | So how does it know? After each step, your glasses snap a photo. |
| 1:05.7 | `scene03` | Your phone passes it to Signoff, and Muse Spark checks it against that step. |
| 1:11.6 | `scene03` | Seconds later, a clear answer: pass or fail, and always the reason why. |
| 1:17.6 | `scene03` | And it all runs from your own phone and laptop, so your API key never leaves your hands. |
| 1:25.3 | `scene04` | A real cook, seen through Ray-Ban Meta glasses. |
| 1:29.2 | `scene04` | It won't let you start on a dry pan. Oil in, and now it passes. |
| 1:35.0 | `scene04` | When a piece of shell slips into the egg, Signoff spots it right away. A clean egg goes in, and only then can you move on. |
| 1:44.5 | `scene04` | Then comes the part most people get wrong: the whites. |
| 1:48.2 | `scene04` | Signoff keeps checking as the egg cooks, and holds the step open until the whites are fully set. |
| 1:56.0 | `scene04` | Clear and glossy means not yet. Opaque and white means done. |
| 2:01.6 | `scene04` | There it is. Fully set. |
| 2:04.5 | `scene04` | Golden edges, nothing burnt, so step four is signed off too. |
| 2:09.5 | `scene04` | And until the egg is actually on that plate, the last step stays open. |
| 2:15.0 | `scene04` | Onto the plate. Five steps, five checks, all signed off. |
| 2:20.3 | `scene05` | And it isn't just a nice demo. We tested it. |
| 2:23.8 | `scene05` | Across thirty labeled photos, it got twenty-nine right. |
| 2:28.5 | `scene05` | And whenever a step was done wrong, it never once signed it off. |
| 2:34.0 | `scene05` | Answers land in about four seconds, and twenty of the photos came straight off the glasses. |
| 2:40.8 | `scene05` | That's the confidence you want before you sign off. |
| 2:45.3 | `scene07` | Signoff. |
| 2:46.6 | `scene07` | Done right. Signed off. |
| 2:48.7 | `scene07` | Your second pair of eyes, for every step. |
| 2:51.7 | `scene07` | Built with Muse Spark and Ray-Ban Meta. It's open source, so go ahead, try it yourself. |

Measured on the final mix: 180.0 s, -15.9 LUFS, -1.5 dBTP; every cue fits its slot; longest pause 2.3 s (end card).

## Checks before upload
- The video link plays in a logged-out window; text readable on a phone.
- No faces or other people, no private screens.
