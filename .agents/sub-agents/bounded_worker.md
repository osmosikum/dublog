# Bounded Worker Entry Point

This file is for task-specific workers only.

Rules:

- do not load `AGENTS.md`, `CLAUDE.md`, `ROADMAP.md`, or `CHANGELOG.md` unless
  the parent task explicitly requires it
- work only inside the write scope given by the parent agent
- do not expand the task on your own
- do not update shared governance docs by default
- return concrete results, not repo strategy

Return format:

- files changed
- checks run
- blockers or assumptions
