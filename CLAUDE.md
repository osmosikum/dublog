# CLAUDE.md - Working Contract for Multi-Agent Sandbox

This file is the operative guide for Claude Code in this repo.
It must reflect the current truth and the nearest direction without locking the project into architecture that has not been built yet.

## Purpose

- keep code, docs, and changelog in sync
- separate current structure, active work, and later ideas
- make it clear what is implemented now and what is only planned

## Current Truth

- The project is a local multi-agent sandbox in Python with stdlib plus `requests`.
- `app.py` serves the web UI and SSE output.
- `main.py` runs conversations from a per-run `session_cfg`, but runtime state is not yet fully session-isolated.
- `projects.py` manages project directories and `settings.json`.
- `identities.py` loads persona files from `identities/`.
- Memory lives at the project level under `projects/<project>/agent_x/memory.md` and is shared across sessions.
- Conversation logs live per session under `projects/<project>/sessions/<session_id>/conversation.md`.
- `sessions.py` holds the `SessionManager` singleton with the active session's `queue`, `stop_event` and `state`; `app.py` no longer holds global runtime state for these.
- Existing `settings.json` files may still contain legacy Danish values; `normalization.py` handles read-compatibility transparently.
- The user may still write free-form input to the agent in Danish or any other chosen language; that is content, not engine state.
- `telemetry.py` records per-call metrics to `session_dir/telemetry.jsonl`; the debug panel in `ui/index.html` polls `/api/telemetry` live during runs.
- Dedicated modules such as `validators.py` do not exist yet.

## Document Roles

- `README.md`: user-facing introduction and run instructions.
- `AGENTS.md`: global agent truth for the repo.
- `CLAUDE.md`: Claude-specific working file that complements `AGENTS.md`.
- `.guides/project_control.md`: the user's operative guide for git and project control.
- `ROADMAP.md`: active milestones and concrete next tasks.
- `FUTURE_PATCHES.md`: intentionally parked ideas and later patches.
- `CHANGELOG.md`: what actually changed.

## Current Structure

```text
dublog/
|-- app.py               # web server and SSE streaming (port 7842)
|-- main.py              # conversation orchestrator, run_conversation(session_cfg)
|-- sessions.py          # SessionManager: runtime lifecycle (queue, stop_event, state)
|-- telemetry.py         # per-call metrics: record_call → telemetry.jsonl, load_telemetry
|-- config.py            # static defaults for CLI runs
|-- model.py             # model adapter: Ollama, LM Studio, Claude API
|-- prompts.py           # prompt builder: identity + instructions + memory
|-- memory.py            # memory IO: load, append, extract, convergence
|-- identities.py        # parser and lister for identity files
|-- projects.py          # project management: create, list, settings
|-- CLAUDE.md
|-- AGENTS.md
|-- ROADMAP.md
|-- FUTURE_PATCHES.md
|-- CHANGELOG.md
|-- README.md
|-- identities/          # templates, examples, and local custom identities
|   |-- README.md
|   |-- template.md
|   |-- examples/
|   |   `-- *.md
|   `-- custom/
|       `-- *.md         # local identities, gitignored
|-- projects/            # runtime data, gitignored
|   `-- <project>/
|       |-- settings.json
|       |-- agent_a/
|       |   `-- memory.md
|       |-- agent_b/
|       |   `-- memory.md
|       `-- sessions/
|           `-- <session_id>/
|               |-- conversation.md
|               `-- run_config.md
`-- ui/
    `-- index.html       # single-file frontend
```

## Working Rules for Claude Code

1. Read `CLAUDE.md`, `ROADMAP.md`, and `CHANGELOG.md` before larger work.
2. If you change code, structure, or working docs, update `CHANGELOG.md` in the same session.
3. Every changelog update must end with `Sign-off: Claude` or `Sign-off: Codex`.
4. Use `ROADMAP.md` for active work. Use `FUTURE_PATCHES.md` for ideas that are good but not active yet.
5. Do not write future architecture as if it already exists in the codebase.
6. Keep dependencies minimal and prefer small, verifiable steps.
7. If code and docs point in different directions, bring them into sync in the same workflow.
8. If a task does not get finished, mark it as `blocked` or `deferred` in the roadmap instead of leaving status implicit.
9. State uncertain assumptions clearly.
10. Done beats perfect, but never at the cost of structural truth.
11. Treat documentation as always-on: relevant docs are updated in the same session as the change.
12. Keep the English pass sharp: system layers and docs become English, but the user's free-form text must not be auto-translated or normalized as if it were engine data.

## Claude Role in Multi-Agent Mode

By default, Claude Code is:

- orchestrator
- reviewer
- scribe

Claude may still make smaller glue changes, but if a larger runtime track can be delegated cleanly, the Builder role should stay separate.
If multiple agents are used at the same time, the Single Writer Rule from `AGENTS.md` applies.

## Changelog Contract

Use `CHANGELOG.md` as actual history, not as a wishlist.

- `Added` for new files, flows, or features
- `Changed` for changed behavior or structure
- `Fixed` for bug fixes
- `Docs` for documentation or workflow rules

For every real change, `[Unreleased]` must be updated, and the session notes must end with a clear sign-off line.

Example:

```md
## [Unreleased]
### Changed
- Runtime became project-aware in `main.py`.
### Docs
- `ROADMAP.md` was updated to the new milestone structure.
Sign-off: Claude
```

## Workflow Per Session

### Before Work

- read relevant working docs
- choose the milestone or subtask being worked on
- mark large active tasks as `doing`

### During Work

- implement in small coherent batches
- update docs in the same session if behavior or structure moves
- keep the line clear between current truth and next direction

### After Work

- run or describe relevant verification
- set finished roadmap tasks to `done`
- update `CHANGELOG.md`
- state the next natural step briefly and concretely

## Next Direction

The active direction lives in `ROADMAP.md`, but the largest tracks are:

- real session structure instead of only project-aware runtime
- observability and debug data as a core feature
- clearer contracts for language, length, and memory output
- a sharper split between session memory, project memory, and later promotion

If an idea is not active yet, it should stay in `FUTURE_PATCHES.md` instead of spreading through the document layer.
