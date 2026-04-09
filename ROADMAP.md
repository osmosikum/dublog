# Roadmap

This roadmap tracks active work and next natural steps.
It is deliberately narrower than the playbook and narrower than `FUTURE_PATCHES.md`.

## Rules

- Use the status fields `todo`, `doing`, `blocked`, `done`, `deferred`.
- Each task should be small enough for a normal working session.
- `ROADMAP.md` describes active or near-active work.
- `CHANGELOG.md` describes what was actually carried out.
- Ideas that are not yet active are moved to `FUTURE_PATCHES.md`.

## Milestone 0 - Docs and governance baseline
Status: done
Purpose: Make the document layer the project's current operative truth without freezing future architecture too early.

- [x] [DOCS] Update `CLAUDE.md`
  - Status: done
  - Why: the old file described an older baseline and lacked the new governance rules
  - Output: updated working file for Claude
  - Done when: current repo state, doc roles and changelog rule are clear

- [x] [DOCS] Create `AGENTS.md`
  - Status: done
  - Why: Codex and other code agents need a corresponding working file
  - Output: new agent guide
  - Done when: changelog discipline, roadmap use and the project's current state are described

- [x] [DOCS] Create `ROADMAP.md`
  - Status: done
  - Why: active work must be separated from vision and parked ideas
  - Output: this file
  - Done when: milestones and next tracks can be read without guessing

- [x] [DOCS] Create `FUTURE_PATCHES.md`
  - Status: done
  - Why: good ideas must be parkable without becoming false promises
  - Output: separate backlog for later patches
  - Done when: deferred work has a clear home

- [x] [DOCS] Introduce changelog sign-off rule
  - Status: done
  - Why: every working session should be traceable to an agent
  - Output: rule in agent docs and updated changelog format
  - Done when: `CHANGELOG.md` and agent docs use the same sign-off contract

- [x] [OPS] Establish git baseline for the repo
  - Status: done
  - Why: the repo must be version-controlled without runtime noise
  - Output: `.gitignore` and initialisation on `main`
  - Done when: source code and docs can be tracked without runtime data filling the status

- [x] [OPS] Configure remote and first push
  - Status: done
  - Why: the baseline should not only exist locally but also be syncable to GitHub
  - Output: `origin` set and `main` tracked against `origin/main`
  - Done when: the local baseline commit exists on remote and `main` tracks `origin/main`

- [x] [OPS] Set global git default to `main`
  - Status: done
  - Why: new repos should not fall back to `master`
  - Output: `init.defaultBranch=main` in the user's git config
  - Done when: new local repos are created with `main` as default branch

- [x] [DOCS] Create the user's project control guide
  - Status: done
  - Why: management of repo, branches, changelog and agents should be gathered in one place
  - Output: `.guides/project_control.md`
  - Done when: the project's git and docs rhythm can be followed without reading the long reference guide first

- [x] [DOCS] Establish minimal agent workflow baseline
  - Status: done
  - Why: multi-agent work should be governed without being over-designed
  - Output: `AGENTS.md`, `CLAUDE.md` and `.guides/project_control.md` describe roles and single-writer baseline
  - Done when: `AGENTS.md` is global truth and it is clear who writes code in a multi-agent session

- [x] [OPS] Audit `.gitignore` and engine/content boundary
  - Status: done
  - Why: variable files must be out of the repo while templates and examples remain tracked
  - Output: smarter `.gitignore`, identity structure with `examples/` and `custom/`, updated docs
  - Done when: runtime data and local identities are ignored while the repo still ships templates and examples

## Milestone 0.5 - English migration boundary
Status: done — all tasks complete
Purpose: Make it clear what can be translated directly and what requires compatibility first, so no existing runtime data is lost.

- [x] [ARCH] Define English migration boundary and no-data-loss rules
  - Status: done
  - Why: language cleanup must not mix UI text, persisted state and content
  - Output: `.guides/english_migration_scope.md`
  - Done when: engine, persisted values and content are separated into clear migration zones

- [x] [COMPAT] Introduce normalisation for language, length and legacy identity slugs
  - Status: done
  - Why: old projects still use Danish enum values and in some cases retired identity slugs
  - Output: compatibility layer before English canonical values are introduced
  - Done when: old `settings.json` can be read correctly while new English values are also accepted

- [x] [UI] Translate engine UI to English without breaking persisted values
  - Status: done
  - Why: labels and error text can switch before the data format does
  - Output: English labels, buttons and messages in the app
  - Done when: UI is English but old settings still load correctly

- [x] [DOCS] Translate engine docs and comments to English
  - Status: done
  - Why: operative docs and engine comments should point the same way as UI and defaults
  - Output: English repo docs and English engine comments, while free user input continues to be treated as content
  - Done when: the project's operative engine layer is English without content or chat input being forced along

- [x] [CONTENT] Decide separate strategy for example identities and template
  - Status: done
  - Why: repo-shipped content is content, not just engine text
  - Output: all six example identities and template translated to English; frontmatter values updated to canonical English forms
  - Done when: the content track is resolved explicitly instead of riding along with the engine migration

## Milestone 1 - Session-aware base
Status: done
Purpose: Lift the current project-aware runtime to a real session structure without rewriting the whole app at once.

- [x] [ARCH] Define disk layout for `projects/<project>/sessions/<session_id>/`
  - Status: done
  - Why: session data must be separated from the project's long-lived data
  - Output: documented target layout and directory creation
  - Done when:
    - session directory is created with a unique id
    - transcript, debug and metadata can live in the session
    - project data can be preserved without being tied to a single run

- [x] [ARCH] Create `sessions.py` with first `SessionManager`
  - Status: done
  - Why: runtime state must not only live as global variables in `app.py`
  - Output: `sessions.py` with `Session` and `SessionManager`; integrated in web-run flow
  - Done when:
    - sessions can be created and marked as running/done/error ✓
    - session paths can be read collectively from the manager ✓

- [x] [RUNTIME] Move output and status from global queue to session-bound structure
  - Status: done
  - Why: current `run_queue` and `is_running` are too coarse for the next phase
  - Output: SSE, stop and status endpoints all read from the active Session
  - Done when:
    - output is bound to a session ✓
    - status can be read without global truth alone ✓

- [x] [DOCS] Sync docs when session structure exists
  - Status: done
  - Why: docs must not write session architecture as true before it is built
  - Output: CLAUDE.md structure tree updated; CHANGELOG updated
  - Done when: the implemented session model is documented ✓

## Milestone 2 - Observability first
Status: done
Purpose: Make it visible what the system injects, where output drifts, and where models get tired.

- [x] [ARCH] Create `telemetry.py`
  - Status: done
  - Why: debuggability should be a core feature
  - Output: `telemetry.py` with `record_call` and `load_telemetry`; writes `session_dir/telemetry.jsonl`
  - Done when: prompt, output and timing data can be recorded per agent call ✓

- [x] [RUNTIME] Log prompt chars, memory lines, history turns and output chars
  - Status: done
  - Why: we need to be able to see context pressure and output drift
  - Output: `run_agent` in `main.py` times each model call and records all metrics
  - Done when: minimum metrics can be read without manual guessing ✓

- [x] [UI] Show a simple debug panel in the UI
  - Status: done
  - Why: observability is most useful while a session is running
  - Output: collapsible debug bar below the console; polls `/api/telemetry` live during runs
  - Done when: key figures are shown during a run ✓

## Milestone 3 - Contracts and validation
Status: done
Purpose: Make language, length and memory output into enforceable contracts instead of soft labels.

- [x] [VALIDATION] Create `validators.py`
  - Status: done
  - Why: output and identity data must be checkable systematically
  - Output: `validators.py` with `ValidationResult` dataclass, composable check functions, `validate_response`, `validate_memory_entry`, `validate_identity`, `record_validation`, `load_validation`
  - Done when: empty responses, missing `[MEMORY]` and identity errors can be detected ✓

- [x] [VALIDATION] Introduce heuristic language check
  - Status: done
  - Why: local models easily drift between languages
  - Output: `check_language` scores all languages by marker-word frequency; flags when expected language scores significantly below apparent language
  - Done when: the system can flag probable language slips ✓

- [x] [VALIDATION] Translate `kort/medium/lang` to explicit runtime limits
  - Status: done
  - Why: length choices should be measurable afterwards
  - Output: `_LENGTH_RANGES` in `validators.py` maps `short/medium/long` to sentence-count bounds; `check_length` flags clear violations
  - Done when: length checks can be compared with actual output ✓

## Milestone 4 - Memory layers and promotion
Status: done
Purpose: Separate session memory from project memory so the two can evolve independently. Introduce a first explicit promotion rule. Keep storage simple — markdown files, no new dependencies.

Design reference: `.guides/scaling_architecture.md` — L1/L2/L3 model; promotion rule; isolation invariant.

- [x] [MEMORY] Split L1 (session) and L2 (archive) memory per agent
  - Status: done
  - Why: current flat `memory.md` mixes working notes and cross-session conclusions; session deletions risk destroying long-term knowledge
  - Output: `agent_x/session_memory.md` (L1) + `agent_x/archive.md` (L2) replacing the current single file; `memory.py` updated to read/write both; legacy `memory.md` auto-migrated on first load
  - Done when: a deleted session does not touch the agent's archive; a new session starts with a clean L1 and inherits L2 ✓

- [x] [MEMORY] Archive session memory on session end (L1 → L2 promotion step 0)
  - Status: done
  - Why: L1 entries that survive a session should graduate to L2 rather than being discarded or kept cluttered in a single file
  - Output: `archive_session_memory()` called at the end of `run_conversation`; non-trivial (≥ 4 words), non-duplicate L1 entries appended to L2; L1 cleared
  - Done when: after each run, L2 grows and L1 is empty ✓

- [x] [MEMORY] Define and document the L2 → L3 promotion rule
  - Status: done
  - Why: not everything should become permanent; the first rule must be simple and explicit, not automatic
  - Output: promotion is manual-only — operator appends to `permanent.md` explicitly; rule documented in `memory.py` module docstring and `.guides/scaling_architecture.md`
  - Done when: it is clear what triggers promotion and who can do it ✓

- [x] [VALIDATION] Extend `validate_memory_entry()` for L1 vs L2 context
  - Status: done
  - Why: validation should know which layer a memory entry is targeting; L2 entries should meet a higher bar than transient L1 notes
  - Output: `validate_memory_entry(entry, layer="L1")` accepts optional layer hint; `check_memory_entry_length` applies stricter upper bound (30 words) for L2 and shared minimum (4 words) for both layers
  - Done when: the validator can distinguish session notes from archive candidates ✓

- [x] [DOCS] Update all docs to reflect the new memory model
  - Status: done
  - Output: `CLAUDE.md` structure tree updated; `.guides/scaling_architecture.md` baseline section updated; `CHANGELOG.md` updated
  - Done when: a new reader can follow the memory flow without reading code first ✓

## Milestone 5 - Session lifecycle hardening
Status: done
Purpose: Make session start, stop and error paths consistent and clean. Verify that streaming output is live during a run, not buffered. Optionally add a simple circuit breaker to the convergence loop.

- [x] [RUNTIME] Clean up state on success, stop and error
  - Status: done
  - Why: the three exit paths from `run_conversation` (natural end, stop_event, exception) should leave the session in a consistent documented state
  - Output: `SessionManager.finish()` now resolves `stopped` when `stop_event` is set, `error` on exception, `done` on clean exit; `/api/status` returns both `running` and `state`
  - Done when: the status endpoint returns a meaningful state after every exit path ✓

- [x] [TEST] Verify that live output reaches the client before a round completes
  - Status: done
  - Why: SSE should stream output line by line, not buffer until a model response is complete
  - Output: verified by code inspection — `output_fn` → `queue.put(line)` → `wfile.write() + flush()` per message; round-start banners, validation warnings and archival results stream immediately; model responses arrive as one block when `call_model()` returns (correct for non-streaming backends); behaviour documented here
  - Done when: streaming behaviour is documented and the result is reproducible ✓

- [x] [RUNTIME] Hash-based loop detection (C6 lite)
  - Status: done
  - Why: the convergence check detects agreement but not repetition — an agent repeating the same response should be flagged
  - Output: `check_loop(response, recent_hashes)` in `memory.py` — MD5 of normalised response text checked against a rolling window of 3; `[LOOP DETECTED]` echoed to run output when triggered; per-agent hash lists initialised in `run_conversation`
  - Done when: the system can detect and log a response loop without semantic similarity ✓
