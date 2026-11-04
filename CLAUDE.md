# CLAUDE.md — Signoff

Entry point for any AI model working in this repo. Signoff is a solo Indie-track entry for the Meta Global AI Developer Hackathon. **Submission is due Wed Nov 4, 2026, 9:00 PM ET.** Time is the scarcest resource.

## Read order (every session, every model, before touching anything)
1. `docs/memory.md` — what is done, in progress, next, blocked. Start here.
2. `docs/plan.md` — the current gate and the cut list.
3. `docs/rules.md` — hackathon rules, scoring, prizes. Non-negotiable.
4. `docs/specs.md` — architecture, schemas, model tiers, verified facts.
5. Only when needed: `docs/intent.md`, `docs/eval-protocol.md`, `docs/demo-and-submission.md`, `docs/decisions.md`.
6. **When something fails: `docs/runbook.md` first**, then ask the user.

## Hard rules
- **New work only.** Never copy or import code from the user's SourceMind project (`d:\Source Mind`). This repo starts fresh; it must be public.
- **Never claim without evidence.** Say "verified now" (you ran it), "reported earlier" (a doc or someone said so), or "unknown". Never invent numbers, costs, accuracy or model behavior. Items marked (U) in docs are unverified until measured.
- **Secrets:** never print, log, commit or paste an API key or token. Keys live in `.env` (gitignored) or the OS keychain. Check `.gitignore` before the first commit.
- **Credits are limited.** Before any sweep that calls Meta/partner APIs, estimate the call count and cost, log it in `docs/memory.md`, and ask the user if it exceeds the per-run budget in `docs/plan.md`.
- **Smallest diff** that finishes the current gate. No features outside `docs/plan.md` Must/Should lists.
- **Commits:** no AI attribution — no `Co-Authored-By`, no "Generated with" lines, ever. Confirm the diff contains only the intended files before committing.
- **Privacy:** record only indoors, alone, no faces, no screens with private data. Contributor-tier model calls may be used by Meta to improve products (U — confirm in terms).

## Update protocol (do this at the time of the change, not at the end)
- After finishing or blocking on anything: edit `docs/memory.md` (Done / In progress / Next 3 / Blockers).
- After any real decision, bug found, or approach swap: append to `docs/decisions.md` (what, why, alternatives).
- Before ending a session or when the user says wrap up: make sure `docs/memory.md` has an accurate "Last session" block so the next model (Sonnet, Qwen, Muse, anyone) can continue cold.

## Model switching
The user will switch models mid-project. Assume you have **no memory** of earlier sessions. Everything you need is in `docs/`. If `docs/memory.md` and the code disagree, trust the code, say so, and fix the doc.

## Model & cost policy
- **Two budgets, never mixed.** (1) *Product runtime*: the Meta Model API credits (about $150) pay for Muse Spark / SAM 3.1 calls made by Signoff itself. (2) *Dev tooling*: the coding agent (Qwen via OpenRouter, with an OpenRouter spend limit set by the user) pays for building.
- **Qwen is the builder's tool, never part of the product.** Signoff's verifier, spec compiler and router must call Meta models only (Muse Spark, SAM 3.1, Wonder, Spark Open via a partner). Hackathon Stage 1 is pass/fail on using Meta's models. Never add a Qwen/OpenAI/Anthropic call to the product code path.
- **Escalate, don't thrash.** After 2 failed attempts at the same problem, stop, write what you tried (as hypotheses) in `docs/memory.md`, and ask the user whether to switch to a stronger model (e.g. Sonnet) for that task.
- **Weaker-model guardrails:** work in small steps (one file or one function at a time); run the code or test after every change and quote the real output; do not trust your own earlier summaries; re-read the file before editing it; if the context feels long, stop and refresh from `docs/memory.md`.
- **Never print, log or commit the OpenRouter or Meta key.** Env vars only; `.claude/settings.local.json` and `.env` stay gitignored.

## Agent
Use the `signoff-builder` subagent (`.claude/agents/signoff-builder.md`) for build work. It already follows this file.
