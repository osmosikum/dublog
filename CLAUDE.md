# CLAUDE.md - Working Contract for Multi-Agent Sandbox

This file is the operative guide for Claude Code in this repo. It must reflect
the current truth and the nearest direction without writing future architecture
as if it already exists.

## Purpose

- keep code, docs, and changelog in sync
- separate current structure, active work, and later ideas
- make it clear what is implemented now and what is only planned

## Routing

- Claude Code uses this file as its tool-native entry point.
- For top-level work, treat `AGENTS.md` as the shared contract and
  `.agents/claude_orchestrator.md` as Claude's repo-specific role file.
- If Claude is started as a bounded sub-agent, do not load the full repo stack
  by default; use only the assigned `.agents/sub-agents/*.md` entry point
  unless the parent task explicitly expands scope.

## Current Truth

- The project is a local multi-agent sandbox in Python with stdlib plus
  `requests`.
- `app.py` serves the web UI and SSE output on port 7842.
- `main.py` runs conversations from a per-run `session_cfg`.
- `projects.py` manages project directories and `settings.json`.
- `identities.py` loads persona files from `identities/`.
- `sessions.py` holds the `SessionManager` singleton with the active session's
  queue, `stop_event`, and state; `app.py` no longer owns that runtime state.
- Memory is split into three layers per agent under `projects/<project>/agent_x/`:
  - `session_memory.md` (L1) - written during a run; archived and cleared on
    session end
  - `archive.md` (L2) - cross-session knowledge; grows via
    `archive_session_memory()`
  - `permanent.md` (L3) - permanent facts; manual promotion only; not yet read
    by the engine
  - existing projects with `memory.md` are auto-migrated to `archive.md` on
    first load
- Conversation logs live per session under
  `projects/<project>/sessions/<session_id>/conversation.md`.
- Existing `settings.json` files may still contain legacy Danish values;
  `normalization.py` handles read compatibility transparently.
- The user may still write free-form input to the agent in Danish or any other
  chosen language; that is content, not engine state.
- `telemetry.py` records per-call metrics to `session_dir/telemetry.jsonl`; the
  debug panel in `ui/index.html` polls `/api/telemetry` live during runs.
- `validators.py` runs contract checks after each agent call; results go to
  `session_dir/validation.jsonl` and failures echo to the run output.
- `SessionManager.finish()` resolves three terminal states: `done`,
  `stopped`, and `error`; `/api/status` returns both `running` and `state`.
- `check_loop()` in `memory.py` detects repeated responses via MD5 hash over a
  rolling window and flags them as `[LOOP DETECTED]`.
- `.agents/` provides role entry points for top-level agents and bounded
  sub-agents. This is a documentation routing layer only; runtime orchestration
  is unchanged.

## Document Roles

- `README.md`: user-facing introduction and run instructions.
- `AGENTS.md`: global agent truth for the repo.
- `CLAUDE.md`: Claude-specific working file that complements `AGENTS.md`.
- `.guides/project_control.md`: the user's operative guide for git and project
  control.
- `.guides/tri_agent_setup.md`: repo-specific routing baseline for top-level
  agents and bounded sub-agents.
- `.guides/scaling_architecture.md`: memory model, convergence upgrade path,
  and infrastructure decision points.
- `.agents/*.md`: role files for top-level agents.
- `.agents/sub-agents/*.md`: bounded entry points for spawned or task-specific
  workers.
- `ROADMAP.md`: active milestones and concrete next tasks.
- `FUTURE_PATCHES.md`: intentionally parked ideas and later patches.
- `CHANGELOG.md`: what actually changed.

## Current Structure

```text
dublog/
|-- app.py               # web server and SSE streaming (port 7842)
|-- main.py              # conversation orchestrator, run_conversation(session_cfg)
|-- sessions.py          # SessionManager: runtime lifecycle (queue, stop_event, state)
|-- telemetry.py         # per-call metrics -> telemetry.jsonl
|-- normalization.py     # read compatibility for legacy Danish enum values
|-- validators.py        # contract checks -> validation.jsonl
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
|-- .agents/
|   |-- claude_orchestrator.md
|   |-- codex_builder.md
|   |-- external_reviewer.md
|   `-- sub-agents/
|       |-- bounded_worker.md
|       `-- qa_reviewer.md
|-- .guides/
|   |-- project_control.md
|   |-- english_migration_scope.md
|   |-- scaling_architecture.md
|   `-- tri_agent_setup.md
|-- identities/
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
|       |   |-- session_memory.md
|       |   |-- archive.md
|       |   `-- permanent.md
|       |-- agent_b/
|       |   |-- session_memory.md
|       |   |-- archive.md
|       |   `-- permanent.md
|       `-- sessions/
|           `-- <session_id>/
|               |-- conversation.md
|               |-- run_config.md
|               |-- telemetry.jsonl
|               `-- validation.jsonl
`-- ui/
    `-- index.html       # single-file frontend
```

## Working Rules for Claude Code

1. Read `CLAUDE.md`, `AGENTS.md`, `ROADMAP.md`, and `CHANGELOG.md` before
   larger work.
2. If you change code, structure, or working docs, update `CHANGELOG.md` in the
   same session.
3. Every changelog update must end with `Sign-off: Claude` or
   `Sign-off: Codex`.
4. Use `ROADMAP.md` for active work. Use `FUTURE_PATCHES.md` for ideas that are
   good but not active yet.
5. Do not write future architecture as if it already exists in the codebase.
6. Keep dependencies minimal and prefer small, verifiable steps.
7. If code and docs point in different directions, bring them into sync in the
   same workflow.
8. If a task does not get finished, mark it as `blocked` or `deferred` in the
   roadmap instead of leaving status implicit.
9. State uncertain assumptions clearly.
10. Done beats perfect, but never at the cost of structural truth.
11. Treat documentation as always-on: relevant docs are updated in the same
    session as the change.
12. Keep the English pass sharp: system layers and docs become English, but the
    user's free-form text must not be auto-translated or normalized as if it
    were engine data.
13. Route bounded workers only to `.agents/sub-agents/*.md` unless the task
    truly requires wider repo context.

## Claude Role in Multi-Agent Mode

By default, Claude Code is:

- orchestrator
- reviewer
- scribe

Claude may still make smaller glue changes, but if a larger runtime track can
be delegated cleanly, the builder role should stay separate. If Codex is the
designated runtime writer, Claude should not compete for the same code path.

When Claude delegates:

- make the writer explicit
- keep bounded tasks narrow
- keep shared docs with the scribe unless deliberately delegated

## Changelog Contract

Use `CHANGELOG.md` as actual history, not as a wishlist.

- `Added` for new files, flows, or features
- `Changed` for changed behavior or structure
- `Fixed` for bug fixes
- `Docs` for documentation or workflow rules

For every real change, `[Unreleased]` must be updated, and the session notes
must end with a clear sign-off line.

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

The active direction lives in `ROADMAP.md`. The scaling target is described in
`.guides/scaling_architecture.md`.

The current routing baseline is documentation-first:

- role entry points live under `.agents/`
- top-level agents use the global contract plus their role file
- bounded sub-agents stay isolated from the global governance stack

Runtime automation for agent routing is deliberately deferred until the repo
shows strain that justifies it.
