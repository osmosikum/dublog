# AGENTS.md - Working Contract for Codex and Other Code Agents

This file gives Codex and other code agents the same project context as
`CLAUDE.md`. The goal is to keep runtime changes, documentation, and changelog
updates aligned.

## Purpose

- keep agent work consistent across Claude, Codex, and later tooling
- prevent docs from drifting away from the code
- ensure changes stay traceable in the changelog

## Role Routing

- Top-level agents use the global contract plus one repo-specific role file
  under `.agents/`.
- Codex: read this file, then `.agents/codex_builder.md`.
- Claude Code: uses `CLAUDE.md` as its tool-native entry point and should stay
  aligned with this file plus `.agents/claude_orchestrator.md`.
- A third top-level agent or external model should use
  `.agents/external_reviewer.md` unless explicitly assigned a different role.
- Bounded sub-agents do not route through `AGENTS.md`; they receive only their
  assigned `.agents/sub-agents/*.md` entry point unless the parent agent
  explicitly expands scope.

## Current Project State

- The project is a local multi-agent sandbox in Python with stdlib plus
  `requests`.
- `app.py` serves the web UI and SSE output on port 7842.
- `main.py` runs conversations from a per-run `session_cfg`.
- `sessions.py` holds the `SessionManager` singleton and `app.py` reads from
  the active session.
- `telemetry.py` records per-call metrics (prompt size, memory lines, history
  turns, output size, duration) to `session_dir/telemetry.jsonl`.
- `validators.py` runs contract checks after each agent call and records
  results to `session_dir/validation.jsonl`; failures echo to the run output.
- `normalization.py` maps legacy Danish enum values to current English
  canonical values so old `settings.json` files load without breaking.
- Memory is split into three layers per agent under
  `projects/<project>/agent_x/`:
  - `session_memory.md` (L1) - written during a run; promoted and cleared on
    session end
  - `archive.md` (L2) - cross-session knowledge; grows via
    `archive_session_memory()`
  - `permanent.md` (L3) - permanent facts; manual promotion only; not read yet
  - existing projects with `memory.md` are auto-migrated to `archive.md` on
    first load
- Conversation logs live per session under `projects/<project>/sessions/<id>/`.
- `.agents/` holds role entry points for top-level agents and bounded
  sub-agents. This is a documentation routing layer only; runtime orchestration
  is unchanged.
- The engine, UI, docs, and structured values are English. User free-form
  content is treated as content, not normalized or translated by the engine.

## Which Docs Govern What

- `AGENTS.md` is the global agent truth for the repo.
- `CLAUDE.md` and `AGENTS.md` must point in the same direction. If they
  diverge, sync them in the same session.
- `.guides/project_control.md` is the user's operative guide and must not
  contradict the agent docs.
- `.guides/tri_agent_setup.md` describes the implemented routing baseline and
  the line between top-level agents and bounded sub-agents.
- `.guides/scaling_architecture.md` describes the memory model, convergence
  upgrade path, and infrastructure decision points. Read it before working on
  memory or runtime.
- `.agents/*.md` are role files for top-level agents.
- `.agents/sub-agents/*.md` are bounded entry points for spawned or
  task-specific agents.
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
- **Repo = engine, user data = content:** code, templates, and docs are
  tracked; `projects/` and runtime data are not.
- **English boundary:** engine, UI, docs, and structured system values are
  English; the user's free-form text is content and stays in whatever language
  the user writes in.
- **Top-level routing:** top-level agents follow the global contract plus their
  own `.agents/*.md` role file.
- **Bounded routing:** bounded sub-agents receive only the smallest relevant
  `.agents/sub-agents/*.md` entry point and do not inherit roadmap or changelog
  duties unless explicitly tasked.
- **Shared docs stay owned:** `CHANGELOG.md`, `ROADMAP.md`, `AGENTS.md`, and
  `CLAUDE.md` belong to the designated scribe by default, not to bounded
  workers.

## Current Role Split

- Human: scope, priority, release, and stop.
- Claude Code: orchestration, review, docs, and scribe by default.
- Codex: builder and refactor by default.
- Third top-level agent or external model: reviewer, tester, or specialist by
  default unless explicitly promoted to writer.
- Bounded sub-agents: isolated workers for narrowly scoped implementation or
  review tasks.

## Working Rules for Code Agents

1. Read `AGENTS.md`, `CLAUDE.md`, `ROADMAP.md`, and `CHANGELOG.md` before
   larger changes.
2. Describe the current architecture as it is, not as we hope it becomes.
3. Use `ROADMAP.md` for active scope. Do not pull parked ideas into active work
   without updating the roadmap.
4. Update `CHANGELOG.md` for every real code, structure, or docs change.
5. End every changelog update with `Sign-off: Codex` or `Sign-off: Claude`.
6. Keep dependencies minimal and choose the smallest meaningful steps.
7. If a task cannot be completed, mark it as `blocked` or `deferred` instead of
   leaving unclear status.
8. If you introduce a new workflow rule, reflect it in the relevant agent docs,
   `.guides/project_control.md`, and the changelog.
9. Treat documentation as part of the deliverable, not cleanup at the end.
10. If multiple agents are used in the same session, make the writer explicit.
11. Do not translate the user's free-form text or other content fields just
    because the engine layer is English.
12. Read `.guides/scaling_architecture.md` before working on memory,
    convergence, or infrastructure.
13. When delegating to a bounded sub-agent, pass a goal, write scope, read
    scope, done definition, and verification expectation.

## Changelog Rule

When a session moves something important for a future reader, it must be
written into `[Unreleased]`. The sign-off line is mandatory so it is always
clear which agent last updated the history.

Example:

```md
## [Unreleased]
### Added
- `.agents/` role files for top-level routing.
### Docs
- `AGENTS.md` and `CLAUDE.md` were synced.
Sign-off: Codex
```

## Practical Rule of Thumb

- Active now: `ROADMAP.md`
- Maybe later: `FUTURE_PATCHES.md`
- Actually happened: `CHANGELOG.md`

Keeping that split sharp matters more than writing the perfect future plan too
early.
