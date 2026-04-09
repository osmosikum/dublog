# Changelog

Convention: every session that changes code, structure or working docs updates `[Unreleased]` and ends with `Sign-off: Claude` or `Sign-off: Codex`.

## [Unreleased]
### Added
- `memory.py`: `check_loop(response, recent_hashes, window=3)` — MD5-based loop detection; normalises response text, checks hash against a rolling window, appends hash before returning; callers pass the same list each round and detection is automatic
- `app.py`: `/api/status` now returns `{"running": bool, "state": str}` — state is `"running"` / `"done"` / `"stopped"` / `"error"` / `"idle"`

### Changed
- `sessions.py`: `SessionManager.finish()` now resolves three distinct terminal states — `"error"` on exception, `"stopped"` when `stop_event` was set, `"done"` on clean exit
- `app.py`: `_get_memory` now reads `archive.md` (L2) with fallback to legacy `memory.md` for unmigrated projects
- `main.py`: `check_loop` imported and called after each agent response; per-agent `hashes_a` / `hashes_b` lists initialised in `run_conversation`; `[LOOP DETECTED]` echoed to run output when triggered

### Docs
- `ROADMAP.md`: Milestone 5 all tasks marked `done`
- `CLAUDE.md`: Current Truth updated with MS5 session state model and loop detection

Sign-off: Claude

---

### Changed
- L3 memory layer renamed from "codex" to "permanent" everywhere — `codex.md` → `permanent.md` — to avoid naming confusion with the Codex agent tool; updated in `memory.py`, `CLAUDE.md`, `AGENTS.md`, `ROADMAP.md`, `.guides/scaling_architecture.md`

### Docs
- `AGENTS.md`: fully updated to current state — describes MS1–MS4 architecture (SessionManager, telemetry, validators, three-layer memory model, normalization); adds rule 12 pointing agents to `.guides/scaling_architecture.md` before memory/runtime work; removes all stale MS0-era language about planned-but-not-implemented modules

---

### Added
- `memory.py`: three-layer memory model — `session_memory.md` (L1, session-scoped), `archive.md` (L2, cross-session), `permanent.md` (L3, manual/permanent); `archive_session_memory()` promotes non-trivial (≥ 4 words) non-duplicate L1 entries to L2 and clears L1 at session end; `_migrate_legacy_memory()` auto-renames `memory.md` → `archive.md` on first load for existing projects; `load_memory()` combines L1 + L2 with section headers when both have content; `check_convergence` stop-word list extended with layer header tokens
- `main.py`: `archive_session_memory()` imported and called after the conversation loop; `setup_dirs` creates `archive.md` for new projects instead of `memory.md`; archival result echoed to run output
- `validators.py`: `check_memory_entry_length` and `validate_memory_entry` accept optional `layer` param (`"L1"` default, `"L2"` for archive candidates); L2 entries get stricter upper bound (30 words); both layers share minimum (4 words); `_MEMORY_ENTRY_MIN_WORDS` and `_MEMORY_ARCHIVE_MAX_WORDS` constants added
- `.guides/scaling_architecture.md`: architecture guide distilling the most relevant solus framework patterns for dublog's memory, convergence and infrastructure scaling direction — covers L1/L2/L3 memory model, promotion rules, isolation invariant, convergence upgrade path, infrastructure decision points and a clear "build in this order" table

### Docs
- `CLAUDE.md`: Current Truth updated with L1/L2/L3 model and layer descriptions; structure tree updated to show per-agent memory files; `.guides/scaling_architecture.md` added to tree
- `ROADMAP.md`: Milestone 4 all tasks marked `done`; Milestone 4 expanded to five concrete tasks (L1/L2 split, L1→L2 archival on session end, L2→L3 promotion rule, `validate_memory_entry` layer extension, docs sync); Milestone 5 restructured as session lifecycle hardening with three concrete tasks
- `FUTURE_PATCHES.md`: eleven new deferred tracks added — background harvester, RAG, librarian gate, echo mining, memory decay, SQLite migration, LLM-scored convergence, circuit breaker, budget kill switch, deadlock kill switch, agent drift detection; all with "why later" rationale tied to the solus overkill table
- `.guides/scaling_architecture.md`: baseline table updated to end-of-MS4 state

Sign-off: Claude

## [Unreleased — MS0–MS3]
### Added
- `validators.py`: `ValidationResult` dataclass; composable `check_*` functions for response emptiness, `[MEMORY]` tag, heuristic length (sentence-count ranges per preset) and heuristic language (marker-word scoring); `validate_response`, `validate_memory_entry` (primary extension point for MS4+ memory work), `validate_identity`; `record_validation` → `session_dir/validation.jsonl`; `load_validation`
- `telemetry.py`: `record_call` appends one JSONL entry per agent call to `session_dir/telemetry.jsonl`; `load_telemetry` reads entries back as a list of dicts; fields: `round`, `agent`, `model`, `prompt_chars`, `memory_lines`, `history_turns`, `output_chars`, `duration_s`, `timestamp`
- `/api/telemetry` GET endpoint: returns telemetry entries for a given project + session
- Debug panel in `ui/index.html`: collapsible bar below the console; polls `/api/telemetry` every 4 s during a run and after completion; shows a compact per-call metrics table
- `sessions.py`: `Session` and `SessionManager` — runtime session lifecycle with per-session `queue`, `stop_event` and `state` (`running` / `done` / `error`); process-level `session_manager` singleton

### Changed
- `app.py`: global `run_queue`, `run_lock`, `stop_event` and `is_running` removed; all runtime state now lives in the active `Session` object from `session_manager`; SSE stream, stop endpoint and status endpoint read from the session rather than globals; session is created in `app.py` before the thread starts and passed into `run_conversation`; `/api/run` response now includes `session_id`
- `main.py`: `run_conversation` accepts optional `session_id` and `session_dir`; `run_agent` gains `agent_name` and `session_dir` params, times the model call and records all metrics via `telemetry.record_call`; `_validate_and_echo` helper runs all checks after each agent call, records to `validation.jsonl` and echoes failures to the run output; if provided (web-run flow) it uses them directly; if absent (CLI flow) it creates a new session as before
- `identities/examples/*.md`: all six example identities translated to English; frontmatter `language` and `length` values updated to canonical English forms (`danish`, `short` etc.)
- `identities/template.md`: translated to English
- `model.py`: unknown backend error message translated to English
- `config.py`: all Danish comments and default values translated to English; default identity slugs updated to canonical (`ent_kasper`, `ent_leon`); default languages updated to `"danish"`
- `normalization.py`: `PROMPT_LANGUAGE_LABELS` now returns English language names (`"Danish"`, `"English"`, etc.) instead of Danish words
- `prompts.py`: all Danish prompt strings translated to English — `_LENGTH_HINTS`, section headers (`## Language requirements`, `## What you remember`) and task instructions
- `memory.py`: conversation log header translated (`"Round"` replaces `"Runde"`)
- `main.py`: history injection messages translated (`"said:"` replaces `"sagde:"`)
- `identities.py`: docstring field descriptions, `_DEFAULTS["language"]` and fallback identity content translated to English
- `projects.py`: `DEFAULT_SETTINGS` topic and language defaults translated to English; empty-name fallback changed from `"projekt"` to `"project"`

### Docs
- `ROADMAP.md`: Milestone 3 all tasks marked `done`; Milestone 2 all tasks marked `done`; Milestone 1 session and runtime tasks marked `done`; Milestone 0.5 docs task marked `done`; fully translated to English
- `CLAUDE.md`: structure tree updated with `sessions.py`, `telemetry.py`, `normalization.py` and `validators.py`; Current Truth updated for all three milestones
- `FUTURE_PATCHES.md`: stronger language detection, memory entry quality check and validation UI panel parked as deferred tracks
- `FUTURE_PATCHES.md`: output drift visualisation parked as deferred telemetry track
- `README.md` fully translated to English
- `.guides/project_control.md` fully translated to English
- `.guides/english_migration_scope.md` fully translated to English
- `identities/README.md` fully translated to English
- `CHANGELOG.md` fully translated to English

Sign-off: Claude

## [Unreleased — prior session]
### Added
- Stop button: run button switches to red "⏹ Stop" during a run and sends a stop signal to the server
- Session system: each conversation run creates a unique session (`YYYYMMDD-HHMMSS`) under the project
- Session selector in UI: view and switch between earlier sessions, click to reload log
- Delete button per session and delete button per project (with confirm dialog)
- `/api/stop` — POST endpoint that sets `stop_event` and cleanly aborts a running conversation
- `/api/sessions` — GET endpoint that lists sessions for a project (newest first)
- `/api/session/log` — GET endpoint that returns `conversation.md` for a given session
- `/api/delete/project` and `/api/delete/session` — POST endpoints for deletion
- `identities/README.md` and `identities/custom/.gitkeep` separating tracked examples from local identities

### Changed
- Disk layout: conversation log moved from `projects/{proj}/shared/` to `projects/{proj}/sessions/{id}/`
- Memory remains at project level (`agent_a/memory.md`, `agent_b/memory.md`) — shared across sessions
- `projects.py` extended with: `create_session`, `list_sessions`, `delete_session`, `delete_project`, `get_session_log`, `new_session_id`
- `main.py`: `run_conversation` now accepts `stop_event` and creates a session automatically
- `memory.py`: `log_conversation` takes `session_dir` instead of `project_dir`
- Legacy v1 directories (`agent_a/`, `agent_b/`, `shared/` in the root) deleted from disk
- `.gitignore` now covers `agent_a/` and `agent_b/` directory level (not just individual files)
- `AGENTS.md`, `CLAUDE.md` and `.guides/project_control.md` now use a minimal agent-workflow baseline with single-writer rule and clear role separation
- `.gitignore` now distinguishes between engine and content, so local identities and runtime data are ignored by default
- `identities.py` now loads repo examples, local custom identities and root-level legacy identities without showing template files in the UI
- `normalization.py` introduces read-compatibility for legacy `language`, `length` and identity slugs so old and new values can be used side by side
- `projects.py` normalises old identity slugs on settings load so existing projects still load into the current UI
- `main.py`, `prompts.py` and `identities.py` now accept both old Danish enum values and new English canonical values at runtime
- `app.py`, `main.py` and `ui/index.html` now show English UI and runtime messages while existing persisted option values can still be read unchanged

### Docs
- `CLAUDE.md` structure tree updated to match current codebase
- `README.md` now documents `identities/examples/`, `identities/custom/` and correct session layout under `projects/`
- `CHANGELOG.md` cleaned up: baseline section has its own name
- `ROADMAP.md` now marks the minimal agent-workflow baseline as completed
- `FUTURE_PATCHES.md` parks agent ledger, diff gate, normaliser track and context isolation as later workflow improvements
- `.guides/english_migration_scope.md` defines the English migration in engine, compatibility and content zones so persisted data is not mixed with text cleanup
- `ROADMAP.md`, `AGENTS.md`, `CLAUDE.md` and `.guides/project_control.md` now describe the English pass as a compatibility track and correct session docs to the actual codebase
- `ROADMAP.md` marks the compatibility layer as landed while UI translation and write migration still remain
- `ROADMAP.md` now marks the UI translation as landed while write migration and docs/content pass still remain
- `AGENTS.md`, `CLAUDE.md`, `.guides/english_migration_scope.md` and `.guides/project_control.md` pin the rule about English system layer and free user input as content
- `CLAUDE.md` and `AGENTS.md` are now fully translated to English so Claude and Codex can read their working docs without mixed system language

Sign-off: Codex

## [baseline] — governance and git setup
### Added
- `AGENTS.md` as a parallel working file for Codex and other code agents.
- `ROADMAP.md` as the active milestone file for next work.
- `FUTURE_PATCHES.md` as a parking lot for later patch ideas and open design questions.
- `.gitignore` to keep runtime data, caches and local noise out of the repo.
- `.guides/project_control.md` as the project's short operative guide for git, docs and work rhythm.

### Changed
- `CLAUDE.md` rewritten to reflect the current project-aware architecture and new working rules.
- The changelog flow now requires a clear agent sign-off for every real session update.
- `CLAUDE.md`, `AGENTS.md`, `README.md` and `ROADMAP.md` synced with a fixed git baseline and always-on documentation rule.
- The repo is initialised as a git repository on the local `main` branch.
- Global Git default branch set to `main` for future repos.
- `origin` set to `https://github.com/osmosikum/dublog.git` and baseline commit pushed to `origin/main`.

### Docs
- The document layer now distinguishes between current truth, active roadmap and parked future ideas so the repo is not locked down too early.
- `.guides/project_control.md` and `ROADMAP.md` now reflect that git setup and first push have actually been completed.
- `ROADMAP.md` now marks the entire git track as completed, including global default branch on `main`.

Sign-off: Codex

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
- `agent_a/identity.md` and `agent_b/identity.md` — agent personas
- `agent_a/memory.md` and `agent_b/memory.md` — empty starting files
- `shared/` directory for conversation log and run config
- `README.md` with how-to sections
- `CHANGELOG.md` (this file)

### Changed
- (none)

### Fixed
- (none)
