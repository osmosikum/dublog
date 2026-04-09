# AGENTS.md - Working Contract for Codex and Other Code Agents

This file gives Codex and other code agents the same project context as `CLAUDE.md`.
The goal is for agent work in this repo to follow the same truth, the same roadmap, and the same changelog discipline.

## Purpose

- keep agent work consistent across Claude, Codex, and later tooling
- prevent docs from drifting away from the code
- ensure changes stay traceable in the changelog

## Current Project State

- The repo is project-aware with session folders for conversation logs, but runtime state is not yet fully session-isolated.
- `app.py` runs the UI, status, and SSE streaming.
- `main.py` drives the conversation with per-run `session_cfg`.
- `projects.py` creates and persists project data under `projects/`.
- `identities/` contains persona files with simple frontmatter.
- Conversation logs live per session under `projects/<project>/sessions/<session_id>/`, while memory still lives at project level.
- The engine layer is still mixed Danish/English, and existing `settings.json` files still contain Danish values that need compatibility before a full English pass is complete.
- Future modules such as `sessions.py`, `telemetry.py`, and `validators.py` are planned but not implemented.

## Which Docs Govern What

- `AGENTS.md` is the global agent truth for the repo.
- `CLAUDE.md` and `AGENTS.md` must point in the same direction. If they diverge, sync them in the same session.
- `.guides/project_control.md` is the user's operative guide and must not contradict the agent docs.
- `ROADMAP.md` is the active worklist.
- `FUTURE_PATCHES.md` is the deliberate parking lot.
- `CHANGELOG.md` is the actual history.
- `README.md` is for the user, not only for internal project truth.

## Minimal Agent Workflow Baseline

These rules apply now:

- Single Writer Rule: only one agent may write runtime code at a time.
- Role separation: builder, reviewer, and scribe must not be the same responsibility in the same work session.
- Canonical truth > model output: structure, files, and validators win over AI text.
- Repo = engine, user data = content: code, templates, and docs are tracked; `projects/` and runtime data are not.
- English boundary: engine, UI, docs, and structured system values should converge to English; the user's free-form text is content and may remain in the language the user writes in.

## Current Role Split

- Human: scope, priority, release, and stop.
- Claude Code: orchestration, review, and docs by default.
- Codex: builder/refactor by default.
- Other agents or models: only used with a bounded responsibility, for example review, normalization, or testing.

## Working Rules for Code Agents

1. Read `AGENTS.md`, `CLAUDE.md`, `ROADMAP.md`, and `CHANGELOG.md` before larger changes.
2. Describe the current architecture as it is, not as we hope it becomes.
3. Use `ROADMAP.md` for active scope. Do not pull parked ideas into active work without updating the roadmap.
4. Update `CHANGELOG.md` for every real code, structure, or docs change.
5. End every changelog update with `Sign-off: Codex` or `Sign-off: Claude`.
6. Keep dependencies minimal and choose the smallest meaningful steps.
7. If a task cannot be completed, mark it as `blocked` or `deferred` instead of leaving unclear status.
8. If you introduce a new workflow rule, it must be reflected in both the relevant agent doc and the changelog.
9. Treat documentation as part of the deliverable, not cleanup at the end.
10. If multiple agents are used in the same session, it must be explicit who the writer is.
11. Do not translate the user's free-form text or other content fields just because the engine layer is becoming English.

## Changelog Rule

When a session moves something important for a future reader, it must be written into `[Unreleased]`.
The sign-off line is mandatory so it is always clear which agent last updated the history.

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
