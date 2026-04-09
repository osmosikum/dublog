# Future Patches

This file is the parking lot for good ideas, later patches and open design questions.
Content here is deliberately not active roadmap work yet.

## Rules

- Use this file for ideas that are promising but not active now.
- Only move something to `ROADMAP.md` when it is the next or near-next real piece of work.
- Add a short note on why something is parked so we do not have to guess later.

## Parked patch candidates

- [ ] [CLI] CLI flags for topic, rounds, models and project
  - Status: deferred
  - Why later: useful, but less important than session architecture and observability

- [ ] [UI] More visual debug console and metrics panel
  - Status: deferred
  - Why later: should build on real telemetry, not before

- [ ] [RUNTIME] Multiple concurrent sessions in the same app instance
  - Status: deferred
  - Why later: requires the single-session flow to be clean first

- [ ] [MEMORY] More advanced promotion with manual or semi-automatic approval
  - Status: deferred
  - Why later: the promotion rule should be simple before it gets smart

- [ ] [MEMORY] Event log as `jsonl` alongside readable markdown files
  - Status: deferred
  - Why later: good idea, but should land together with sessions and telemetry

- [ ] [VALIDATION] Stronger language detection than a simple heuristic
  - Status: deferred
  - Why later: the first version just needs to be able to flag obvious deviations; a proper solution would use a lightweight library (langdetect) or an LLM-assisted check

- [ ] [VALIDATION] Memory entry quality check (semantic, not just length)
  - Status: deferred
  - Why later: length is a good first proxy; semantic quality (is the entry actually useful?) likely needs an LLM-assisted pass or at least a keyword-density heuristic — good candidate for when memory architecture matures in MS4+

- [ ] [VALIDATION] Validation results visible in UI debug panel
  - Status: deferred
  - Why later: failures already echo to console; a table view alongside telemetry makes sense once the debug panel is more established

- [ ] [IDENTITY] Model-specific overrides in identity frontmatter
  - Status: deferred
  - Why later: useful for local models, but not necessary to get the base right

- [ ] [TELEMETRY] Output drift visualisation across rounds
  - Status: deferred
  - Why later: `output_chars` is already recorded per call; trending it (is agent B getting shorter each round?) needs multi-round comparison and a small chart or trend indicator in the debug panel — good idea but a separate UI track

- [ ] [SUMMARY] Third agent or moderator for post-summary
  - Status: deferred
  - Why later: the persona layer is not the main track before runtime and observability are cleaner

- [ ] [EXPORT] Analysis or snapshot exports per session
  - Status: deferred
  - Why later: makes most sense when sessions are first-class objects

- [ ] [TEST] More systematic smoke tests for backends and contracts
  - Status: deferred
  - Why later: validation and telemetry should land before the test strategy expands

- [ ] [OPS] Agent Ledger for model, task, duration and files changed
  - Status: deferred
  - Why later: good for cost/traceability, but not critical before runtime and docs are more stable

- [ ] [WORKFLOW] Diff gate with explicit reviewer pass before merge
  - Status: deferred
  - Why later: good discipline, but should build on a simpler review rhythm first

- [ ] [WORKFLOW] GEMINI.md and normalizer pipeline for research/import
  - Status: deferred
  - Why later: useful for long input tracks, but not necessary for today's core flow

- [ ] [WORKFLOW] Tighter context isolation per agent
  - Status: deferred
  - Why later: important in the long run, but should be introduced alongside more mature delegation

- [ ] [MEMORY] Background harvester (R2 pattern)
  - Status: deferred
  - Why later: explicit `[MEMORY]` tags are sufficient at current session lengths; a background LLM pass that extracts knowledge without agent tagging becomes valuable when sessions grow longer or agents miss too much — must always run fire-and-forget, never on the critical path

- [ ] [MEMORY] RAG / cosine similarity search in memory archive (R3 pattern)
  - Status: deferred
  - Why later: loading the full memory.md per call is fine while entries stay below ~200; vector search makes sense after SQLite migration is in place

- [ ] [MEMORY] Librarian gate before archive injection (R1 pattern)
  - Status: deferred
  - Why later: only meaningful once RAG exists; the gate prevents injecting irrelevant archive context and saves tokens

- [ ] [MEMORY] Echo mining across sessions (M5 pattern)
  - Status: deferred
  - Why later: recurring patterns across sessions become detectable at ~50+ sessions; premature before that

- [ ] [MEMORY] Memory decay with type-aware half-lives (M6 pattern)
  - Status: deferred
  - Why later: decay is only meaningful after ~1 month of data; old entries lose weight automatically so outdated facts do not compete with recent ones

- [ ] [MEMORY] SQLite migration for structured storage
  - Status: deferred
  - Why later: markdown files are correct at current scale; SQLite becomes necessary when MAX_MEMORY_LINES feels too blunt — enables decay, structured queries, and later embeddings; lock in embedding model before adding vectors (AP7 risk)

- [ ] [RUNTIME] LLM-scored convergence detection (A4 pattern)
  - Status: deferred
  - Why later: the current word-overlap heuristic is a correct first approximation; LLM-scored semantic agreement becomes valuable when heuristic produces too many false positives

- [ ] [RUNTIME] Circuit breaker for response loops (C6 pattern)
  - Status: deferred
  - Why later: adds hash-based exact loop detection and semantic similarity check on top of the existing convergence rounds counter; good MS5+ candidate

- [ ] [RUNTIME] Budget kill switch (C1 extension)
  - Status: deferred
  - Why later: "stop if session exceeds N model calls or costs > threshold" — useful once model costs or local resource limits become a practical concern; the stop_event pattern is already in place so the wiring is simple

- [ ] [RUNTIME] Deadlock kill switch — escalate if agents disagree N times consecutively (C1 pattern)
  - Status: deferred
  - Why later: requires tracking consecutive disagreement count per agent pair; useful when debates stall without convergence; a moderator message or human escalation is the natural action

- [ ] [MEMORY] Agent drift detection via embedding baseline (A1 pattern)
  - Status: deferred
  - Why later: embeddings add a dependency; useful when an agent's voice drifts measurably from its identity baseline across rounds; augments the current language heuristic with a semantic dimension

## Open design questions

1. Should the first stable version only run one session at a time, or should multi-session support come in early?
2. Should Danish be a hard requirement in the first version, or should English be an explicit fallback?
3. Should project-memory promotion be manual, semi-automatic or automatic in the first stable base?
4. Should the event log primarily be markdown, `jsonl`, or both?
5. Should identity files later be able to have backend- or model-specific overrides?

Until those questions become active, they stay here and not in the operative roadmap.
