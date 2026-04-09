# Changelog

Convention: every session that changes code, structure or working docs updates
`[Unreleased]` and ends with `Sign-off: Claude` or `Sign-off: Codex`.

## [Unreleased]

_(nothing yet)_

---

## [v0.1.0] - 2026-04-10

First governed release. Clean session architecture, observability, output contracts,
layered memory, and lifecycle hardening — built across MS0–MS5.

### Architecture
- **Session system** (`sessions.py`): `SessionManager` with per-session `queue`,
  `stop_event` and `state`; replaces former global variables in `app.py`; three
  terminal states: `done` / `stopped` / `error`
- **Three-layer memory** (`memory.py`): `session_memory.md` (L1, session-scoped),
  `archive.md` (L2, cross-session), `permanent.md` (L3, manual promotion only);
  `archive_session_memory()` promotes non-trivial, non-duplicate L1 entries to L2
  on session end; `_migrate_legacy_memory()` auto-renames legacy `memory.md` →
  `archive.md` on first load; `load_memory()` serves L1 + L2 combined with section
  headers; `check_loop()` detects repeated responses via MD5 hash over a rolling window

### Observability
- **Telemetry** (`telemetry.py`): `record_call` appends per-call metrics to
  `session_dir/telemetry.jsonl` — round, agent, model, prompt_chars, memory_lines,
  history_turns, output_chars, duration_s, timestamp
- **Debug panel** (`ui/index.html`): collapsible bar below console; polls
  `/api/telemetry` live during runs; shows a compact per-call metrics table
- **Validation log**: `record_validation` appends results to `session_dir/validation.jsonl`;
  failures echo to run output

### Contracts
- **Validators** (`validators.py`): `ValidationResult` dataclass; composable
  `check_*` functions for response emptiness, `[MEMORY]` tag, heuristic length
  (sentence-count bounds per preset), heuristic language (marker-word scoring),
  memory entry length with layer awareness (L1 ≤ 35w, L2 ≤ 30w, both ≥ 4w);
  `validate_response`, `validate_memory_entry(entry, layer)`, `validate_identity`

### Compatibility and English pass
- **Normalization** (`normalization.py`): maps legacy Danish enum values
  (`dansk`→`danish`, `kort`→`short`, identity slugs) transparently so old
  `settings.json` files load without breaking
- All engine code, prompts, docs and example identities translated to English;
  user free-form content treated as content — not normalized

### UI and endpoints
- Stop button with red ⏹ state; `/api/stop` POST endpoint
- Session selector: list, view and delete past sessions; `/api/sessions`,
  `/api/session/log`, `/api/delete/session`, `/api/delete/project`
- `/api/telemetry` GET endpoint
- `/api/status` returns `{ running, state }` — state visible after all exit paths
- `_get_memory` reads `archive.md` (L2) with fallback to legacy `memory.md`

### Governance and docs
- `CLAUDE.md`, `AGENTS.md`: working contracts for Claude and Codex; kept in sync
- `ROADMAP.md`: milestones MS0–MS5 all marked done
- `FUTURE_PATCHES.md`: deliberate parking lot for 20+ deferred ideas
- `.guides/scaling_architecture.md`: memory model, convergence upgrade path,
  infrastructure decision points mapped to dublog's current scale
- `.gitignore`: engine/content boundary; `projects/` and runtime data ignored
- Modular identity system: `identities/examples/` (tracked) + `identities/custom/`
  (gitignored); six example identities in English with canonical frontmatter

Sign-off: Claude

---

## Pre-governance history

The entries below predate the MS0 governance baseline. They are kept for
traceability but the versioning restarts at v0.1.0.

## [v1.2.0] - 2026-04-08
### Added
- `identities/` directory — modular persona files with YAML-like frontmatter (`name`, `language`, `length`)
- Pre-installed identities: Skeptikeren, Optimisten, Moderatoren, Djaevlens Advokat
- `identities.py` — parser and lister for identity files (no external deps)
- `projects.py` — project management: create, list, load/save settings, sanitize names
- `projects/default/` — default project created automatically on boot
- UI: project selector with "+" button to create new projects
- UI: identity dropdown per agent — auto-fills name, language and length on selection
- UI: language dropdown per agent (Danish, English, Norwegian, Swedish, German)
- UI: length dropdown per agent (short / medium / long)
- `/api/projects` GET+POST — list and create projects
- `/api/project/settings` GET+POST — get and save project settings
- `/api/identities` GET — list available identities with metadata
- Project settings saved to `settings.json` on every run (full restore on switch)

### Changed
- `main.py` rewritten: `run_conversation(output_fn, project, session_cfg)` — no global config mutation, thread-safe
- `prompts.py` rewritten: `build_system_prompt(identity_content, memory, language, length)` — identity is now a string, not a file path
- `memory.py`: `log_conversation` now takes a `project_dir` argument instead of a hardcoded `shared/`
- `config.py` cleaned up — static constants only, no runtime state
- `/api/memory/a` and `/api/memory/b` are now project-aware via `?project=` query param
- Backend switch in UI correctly reloads models from the selected backend

## [v1.1.0] - 2026-04-08
### Added
- `app.py` — web server (stdlib `http.server` + `ThreadingMixIn`) on port 7842
- `ui/index.html` — single-file frontend with dark theme, live SSE output and memory panel
- Model discovery endpoints: fetches available models from Ollama and LM Studio
- `/api/memory/a` and `/api/memory/b` — serves agent memory to the frontend
- Memory panel at the bottom of the UI that polls and shows both agents' memory live

### Changed
- `main.py` refactored: all logic gathered in `run_conversation(output_fn=print)` so UI and CLI share the same code
- `main.py` now uses `import config` directly (rather than `from config import`) so runtime changes from the UI take effect

## [v1.0.0] - 2026-04-08
### Added
- Full initial implementation of multi-agent sandbox
- `config.py` — central configuration (topic, agents, backend, budgets, convergence)
- `model.py` — model adapter with support for Ollama, LM Studio and Claude API
- `memory.py` — file-based memory with tags, budget, convergence detection and conversation log
- `prompts.py` — structured prompt builder (identity -> memory -> history -> task)
- `main.py` — orchestrator with main loop, live output and early stop on convergence
- `README.md` with how-to sections
- `CHANGELOG.md` (this file)
