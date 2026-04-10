# Tri-Agent Routing Baseline for `dublog`

This guide turns the repo's current multi-agent rules into a concrete routing
map. It is intentionally narrower than a general "AI architecture" essay.

The goal is simple:

- keep top-level agent responsibilities separate
- keep bounded sub-agents small and clean
- make it obvious which files are global truth and which are role prompts
- implement only the parts that the repo can support right now

## What is implemented now

The current baseline is documentation-based routing, not runtime automation.

- `AGENTS.md` is the shared contract for Codex and other code agents.
- `CLAUDE.md` is Claude Code's tool-native entry point and must stay aligned
  with `AGENTS.md`.
- `.agents/*.md` holds repo-specific role files for top-level agents.
- `.agents/sub-agents/*.md` holds bounded entry points for spawned or
  task-specific workers.
- The Single Writer Rule still applies: only one agent writes runtime code at a
  time.

What is **not** implemented yet:

- automatic agent detection or prompt routing in runtime code
- automatic file locking between tools
- scripted agent spawning from inside the app
- persistent sub-agent orchestration state

Those may come later, but they are not part of the current repo baseline.

## Current role split

The project already has a default responsibility split:

- Human: scope, priority, release, and stop
- Claude Code: orchestration, review, docs, and scribe by default
- Codex: builder and refactor by default
- Third top-level agent or external model: reviewer, tester, or specialist by
  default unless explicitly promoted to writer

This guide makes that split concrete by pointing each top-level role to a real
file under `.agents/`.

## Routing rules

### Top-level agents

Top-level agents work with project-wide context and may touch shared docs.

- Codex route: `AGENTS.md` -> `.agents/codex_builder.md`
- Claude route: `CLAUDE.md` -> `AGENTS.md` -> `.agents/claude_orchestrator.md`
- Third top-level agent route: `AGENTS.md` -> `.agents/external_reviewer.md`

All top-level agents follow the same repo governance:

- read the relevant working docs before larger work
- keep docs and code in sync in the same session
- update `CHANGELOG.md` for real repo changes
- respect the writer, reviewer, and scribe split

### Bounded sub-agents

Bounded sub-agents are different. They are not full repo participants.

- They do **not** route through `AGENTS.md` or `CLAUDE.md` by default.
- They receive only the smallest useful entry point from
  `.agents/sub-agents/`.
- They do not own `ROADMAP.md`, `CHANGELOG.md`, or governance docs unless the
  parent task explicitly says so.
- They should return concrete output to the parent agent: changed files, test
  result, blockers, or review findings.

This keeps their context small and stops them from trying to "run the repo"
instead of solving the bounded task.

## Repo layout

```text
dublog/
|-- AGENTS.md
|-- CLAUDE.md
|-- .agents/
|   |-- claude_orchestrator.md
|   |-- codex_builder.md
|   |-- external_reviewer.md
|   `-- sub-agents/
|       |-- bounded_worker.md
|       `-- qa_reviewer.md
`-- .guides/
    |-- project_control.md
    |-- scaling_architecture.md
    `-- tri_agent_setup.md
```

## Ownership model

Use this as the default decision table:

| Area | Default owner |
|------|---------------|
| Runtime code | designated writer, usually Codex |
| Review findings | Claude or other reviewer |
| `CHANGELOG.md` | scribe, usually Claude unless the session is Codex-only |
| `ROADMAP.md` | orchestrator or scribe |
| Role files under `.agents/` | whichever top-level agent is updating workflow rules |
| Bounded worker output | parent top-level agent integrates it |

Important constraint:

- bounded workers should not update shared docs just because they changed code
- top-level agents remain responsible for integrating bounded work into the
  repo's official history

## Delegation packet

When a top-level agent delegates work, the handoff should include:

- goal: what outcome is needed
- write scope: exactly which files or folders may be edited
- read scope: any extra files the worker may consult
- done definition: what counts as finished
- verification: what should be checked before returning
- doc ownership: whether the worker may touch changelog or roadmap

This is the minimum needed to keep bounded workers useful instead of noisy.

## Safe baseline for `dublog`

The safe implementation for this repo is:

1. keep routing in docs and file structure
2. keep runtime orchestration unchanged
3. keep one runtime writer at a time
4. let top-level agents own changelog and roadmap updates
5. use bounded sub-agents only for tightly scoped work

That gives you sharper multi-agent coordination now without risking breakage in
the app itself.
