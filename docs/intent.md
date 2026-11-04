# intent.md — Why Signoff exists

## One sentence
Signoff checks, from first-person video on Ray-Ban Meta glasses, whether a hands-on procedure step was **actually done correctly**, and publishes an open benchmark of how well Meta's Muse models do that, including how often they wrongly say "done".

## The problem
AI assistants on glasses can read a procedure aloud (Meta's Live AI already does conversation; the Display glasses show step-by-step guidance). Nobody verifies the work. In repair, inspection, assembly or lab work, a wrong "done" costs time, damages hardware or fails an inspection. Nothing public measures how often a model signs off on a step that is wrong.

## Who benefits
- Field / repair / maintenance technicians and their supervisors (proof of work, fewer rework visits).
- Manufacturing and lab teams following written procedures (quality checks without a second person).
- Developers building on Meta's models, who get an open dataset, harness and recipe to measure verification reliability and cost.

## Hackathon theme
**Push the Frontier** — give a machine a new capability: verifying physical work in the real world with Meta's models. (Secondary read: Build for Your World, since the demo procedure is something the builder does firsthand.)

## What we deliver (maps to the 4 scoring criteria)
| Criterion (weight) | Deliverable |
|---|---|
| Impact (30%) | Clear story for repair/inspection/lab proof-of-work; open dataset + harness others can rerun |
| Use of Meta AI tooling (25%) | Spark compiles SOP to checkable spec; SAM 3.1 crops; Spark verifies; Wonder/Spark tiers as escalation; Spark Open as cheap tier via partner (also targets the open-weights bonus) |
| Demo (25%) | 3-minute video: live glasses check -> deliberate error caught and blocked -> real benchmark chart |
| Technical depth (20%) | Labeled dataset with injected errors, reproducible harness, false-pass rate, cost per correct verdict, router |

## Success definition
- **Must:** a public repo with a working verifier, a labeled dataset (about 25 runs, 2 procedures), a harness that reports real numbers, and a 3-minute demo video submitted before Nov 4 9 PM ET.
- **Should:** the live glasses loop works on camera.
- **Nice:** open-weights tier verified for the $10K bonus, X post engagement for the $20K viral bonus.

## Non-goals (do not build)
- Medical advice, mental-health, nutrition, sports, education chatbots, job screeners, political content (hackathon anti-projects).
- A generic RAG app or a simple image analyzer.
- An iOS app, store publishing, user accounts, a web dashboard beyond what the demo needs.
- Training or fine-tuning models.
- Voice commands, third procedure, Wonder arm, router calibration: cut first (see `plan.md`).

## Honesty stance
Report real, measured numbers only, with the small-sample caveat (single annotator, small dataset). A modest honest result beats an inflated one; judges can rerun it.
