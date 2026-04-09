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
Status: doing
Purpose: Lift the current project-aware runtime to a real session structure without rewriting the whole app at once.

- [x] [ARCH] Define disk layout for `projects/<project>/sessions/<session_id>/`
  - Status: done
  - Why: session data must be separated from the project's long-lived data
  - Output: documented target layout and directory creation
  - Done when:
    - session directory is created with a unique id
    - transcript, debug and metadata can live in the session
    - project data can be preserved without being tied to a single run

- [ ] [ARCH] Create `sessions.py` with first `SessionManager`
  - Status: todo
  - Why: runtime state must not only live as global variables in `app.py`
  - Output: `sessions.py` plus integration in the web-run flow
  - Done when:
    - sessions can be created and marked as running/done/error
    - session paths can be read collectively from the manager

- [ ] [RUNTIME] Move output and status from global queue to session-bound structure
  - Status: todo
  - Why: current `run_queue` and `is_running` are too coarse for the next phase
  - Output: session-aware output/status flow
  - Done when:
    - output is bound to a session
    - status can be read without global truth alone

- [ ] [DOCS] Sync docs when session structure exists
  - Status: todo
  - Why: docs must not write session architecture as true before it is built
  - Output: updated working docs and possibly README notes
  - Done when: the implemented session model is documented

## Milestone 2 - Observability first
Status: todo
Purpose: Make it visible what the system injects, where output drifts, and where models get tired.

- [ ] [ARCH] Create `telemetry.py`
  - Status: todo
  - Why: debuggability should be a core feature
  - Output: unified module for simple runtime metrics
  - Done when: prompt, output and timing data can be recorded per agent call

- [ ] [RUNTIME] Log prompt chars, memory lines, history turns and output chars
  - Status: todo
  - Why: we need to be able to see context pressure and output drift
  - Output: concrete metrics in runtime and file output
  - Done when: minimum metrics can be read without manual guessing

- [ ] [UI] Show a simple debug panel in the UI
  - Status: todo
  - Why: observability is most useful while a session is running
  - Output: live debug display in the browser
  - Done when: key figures and error states are shown during a run

## Milestone 3 - Contracts and validation
Status: todo
Purpose: Make language, length and memory output into enforceable contracts instead of soft labels.

- [ ] [VALIDATION] Create `validators.py`
  - Status: todo
  - Why: output and identity data must be checkable systematically
  - Output: dedicated validation module
  - Done when: empty responses, missing `[MEMORY]` and identity errors can be detected

- [ ] [VALIDATION] Introduce heuristic language check
  - Status: todo
  - Why: local models easily drift between languages
  - Output: simple language detection and deviation marking
  - Done when: the system can flag probable language slips

- [ ] [VALIDATION] Translate `kort/medium/lang` to explicit runtime limits
  - Status: todo
  - Why: length choices should be measurable afterwards
  - Output: clear preset-to-contract mapping
  - Done when: length checks can be compared with actual output

## Milestone 4 - Memory flow and promotion
Status: todo
Purpose: Separate session memory, project memory and later promotion so memory becomes simple and traceable.

- [ ] [MEMORY] Split project memory and session memory physically
  - Status: todo
  - Why: current structure is too flat for longer runs
  - Output: separate storage for temporary and long-lived memory
  - Done when: deleting a session does not destroy the project's long-term memory

- [ ] [MEMORY] Define first promotion rule
  - Status: todo
  - Why: not everything should automatically become permanent memory
  - Output: simple promotion strategy
  - Done when: it is clear what gets promoted and why

- [ ] [DOCS] Describe memory levels and promotion flow
  - Status: todo
  - Why: memory architecture must not become semi-magical
  - Output: updated docs
  - Done when: a new reader can follow the memory flow without reading code first

## Milestone 5 - Streaming and UI hardening
Status: todo
Purpose: Make runs more live and robust without losing the simple base.

- [ ] [UI] Make streaming more session-aware
  - Status: todo
  - Why: output should be displayable continuously per run
  - Output: improved streaming flow
  - Done when: the client can follow a specific session without global confusion

- [ ] [RUNTIME] Clean up cleanup on success, stop and error
  - Status: todo
  - Why: session termination should be clear and robust
  - Output: more explicit cleanup flow
  - Done when: state and files are left consistent after all exit paths

- [ ] [TEST] Verify that live output does not require a complete full response first
  - Status: todo
  - Why: streaming should feel like streaming
  - Output: simple verification or smoke test
  - Done when: streaming behaviour can be documented and reproduced
