# AGENTS.md - Working Contract for Codex and Other Code Agents

This file gives Codex and other code agents the same project context as `CLAUDE.md`.
The goal is for agent work in this repo to follow the same truth, the same roadmap,
and the same changelog discipline.

## Purpose

- keep agent work consistent across Claude, Codex, and later tooling
- prevent docs from drifting away from the code
- ensure changes stay traceable in the changelog

## Current Project State

- The project is a local multi-agent sandbox in Python with stdlib plus `requests`.
- `app.py` serves the web UI and SSE output on port 7842.
- `main.py` runs conversations from a per-run `session_cfg`.
- `sessions.py` holds the `SessionManager` singleton — replaces former global
  `run_queue`, `stop_event` and `is_running`; `app.py` reads from the active session.
- `telemetry.py` records per-call metrics (prompt size, memory lines, history turns,
  output size, duration) to `session_dir/telemetry.jsonl`.
- `validators.py` runs contract checks after each agent call and records results
  to `session_dir/validation.jsonl`; failures echo to the run output.
- `normalization.py` maps legacy Danish enum values to current English canonical
  values so old `settings.json` files load without breaking.
- Memory is split into three layers per agent under `projects/<project>/agent_x/`:
  - `session_memory.md` (L1) — written during a run; promoted and cleared on session end.
  - `archive.md` (L2) — cross-session knowledge; grows via `archive_session_memory()`.
  - `permanent.md` (L3) — permanent facts; manual promotion only; not read yet.
  - Existing projects with `memory.md` are auto-migrated to `archive.md` on first load.
- Conversation logs live per session under `projects/<project>/sessions/<id>/`.
- The engine, UI, docs and structured values are English. User free-form content
  is treated as content — not normalized or translated by the engine.

## Which Docs Govern What

- `AGENTS.md` is the global agent truth for the repo.
- `CLAUDE.md` and `AGENTS.md` must point in the same direction. If they diverge,
  sync them in the same session.
- `.guides/project_control.md` is the user's operative guide and must not
  contradict the agent docs.
- `.guides/scaling_architecture.md` describes the memory model, convergence upgrade
  path and infrastructure decision points — read before working on memory or runtime.
- `ROADMAP.md` is the active worklist.
- `FUTURE_PATCHES.md` is the deliberate parking lot.
- `CHANGELOG.md` is the actual history.
- `README.md` is for the user, not only for internal project truth.

## Minimal Agent Workflow Baseline

These rules apply now:

- **Single Writer Rule:** only one agent may write runtime code at a time.
- **Role separation:** builder, reviewer, and scribe must not be the same
  responsibility in the same work session.
- **Canonical truth > model output:** structure, files, and validators win over
  AI text.
- **Repo = engine, user data = content:** code, templates, and docs are tracked;
  `projects/` and runtime data are not.
- **English boundary:** engine, UI, docs, and structured system values are English;
  the user's free-form text is content and stays in whatever language the user writes in.

## Current Role Split

- Human: scope, priority, release, and stop.
- Claude Code: orchestration, review, and docs by default.
- Codex: builder/refactor by default.
- Other agents or models: only used with a bounded responsibility — for example
  review, normalization, or testing.

## Working Rules for Code Agents

1. Read `AGENTS.md`, `CLAUDE.md`, `ROADMAP.md`, and `CHANGELOG.md` before larger changes.
2. Describe the current architecture as it is, not as we hope it becomes.
3. Use `ROADMAP.md` for active scope. Do not pull parked ideas into active work
   without updating the roadmap.
4. Update `CHANGELOG.md` for every real code, structure, or docs change.
5. End every changelog update with `Sign-off: Codex` or `Sign-off: Claude`.
6. Keep dependencies minimal and choose the smallest meaningful steps.
7. If a task cannot be completed, mark it as `blocked` or `deferred` instead of
   leaving unclear status.
8. If you introduce a new workflow rule, it must be reflected in both the relevant
   agent doc and the changelog.
9. Treat documentation as part of the deliverable, not cleanup at the end.
10. If multiple agents are used in the same session, it must be explicit who the
    writer is.
11. Do not translate the user's free-form text or other content fields just because
    the engine layer is English.
12. Read `.guides/scaling_architecture.md` before working on memory, convergence,
    or infrastructure — it describes what patterns are appropriate at the current
    scale and what is deliberately deferred.

## Changelog Rule

When a session moves something important for a future reader, it must be written
into `[Unreleased]`. The sign-off line is mandatory so it is always clear which
agent last updated the history.

Example:

```md
## [Unreleased]
### Added
- `FUTURE_PATCHES.md` for later patch ideas.
### Docs
- `AGENTS.md` and `CLAUDE.md` were synced.
Sign-off: Codex
```

## Practical Rule of Thumb

- Active now: `ROADMAP.md`
- Maybe later: `FUTURE_PATCHES.md`
- Actually happened: `CHANGELOG.md`

Keeping that split sharp matters more than writing the perfect future plan too early.
