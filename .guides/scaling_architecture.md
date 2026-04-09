# Scaling Architecture Guide

This guide maps the patterns from the solus framework to dublog's current state.
It answers: **where are we now, what is the natural next step, and what should we
build toward without over-engineering too early?**

Read this before working on Milestone 4+.

---

## Current baseline (end of MS4)

| Layer | What exists |
|-------|-------------|
| Memory L1 | `session_memory.md` per agent — written during run, cleared on archive |
| Memory L2 | `archive.md` per agent — cross-session, grows via `archive_session_memory()` |
| Memory L3 | `permanent.md` — permanent, manual promotion only, not yet read by engine |
| Capture | `[MEMORY]: text` tag in response → `extract_memory_tag` → `append_memory` → L1 |
| Promotion | `archive_session_memory()` — L1 → L2 on session end; ≥ 4 words, no duplicates |
| Validation | `validate_memory_entry(entry, layer)` — layer-aware length bounds; L1 ≤ 35w, L2 ≤ 30w, both ≥ 4w |
| Session | Per-run directory under `sessions/<id>/` with `conversation.md` |
| Observability | `telemetry.jsonl` + `validation.jsonl` per session |
| Convergence | Word-overlap heuristic in `memory.py` (`check_convergence`) |
| Stop | `threading.Event` in `SessionManager` |
| Legacy compat | `memory.md` auto-renamed to `archive.md` on first load |

What we **do not have yet:** structured storage (SQLite), retrieval (RAG),
background harvester, decay, LLM-scored convergence.

---

## The 3-layer memory model (target for MS4+)

The solus framework calls this **M2 — Structured Memory Schema**.
Mapped to dublog's context:

| Layer | Solus name | Dublog meaning | Lifetime |
|-------|-----------|----------------|---------|
| **L1 — Desk** | Working Memory | Active session memory: what the agent is thinking *now* | Session |
| **L2 — Archive** | Session Archive | Cross-session memory: what the agent has learned across runs | Project |
| **L3 — Permanent** | Permanent | Promoted long-term facts that should never decay | Permanent |

### How this maps to the current flat structure

Right now `memory.md` is a hybrid of L1 and L2 — everything lands in the same file,
session-lived notes mixed with permanent conclusions. MS4 separates them:

```
projects/<project>/
    agent_a/
        memory.md           ← today: one flat file (L1+L2 mixed)
    ↓ MS4 target:
        session_memory.md   ← L1: cleared/archived after each session
        archive.md          ← L2: cross-session, grows over time
        permanent.md        ← L3: promoted items, rarely changes
```

**Start simple:** L1/L2 split as two markdown files is enough for MS4.
SQLite + embeddings (M2 full schema) comes later when search becomes necessary.

### Promotion rule (first version, MS4)

A memory entry moves L1 → L2 when a session ends and the entry is non-trivial
(more than N words, not a duplicate of an existing L2 entry).

A memory entry moves L2 → L3 via explicit promotion only — never automatically.
A human or a future moderator agent decides what is permanent.

**Relevant solus patterns:** M5 (echo mining) is overkill before ~50 sessions.
M6 (decay) is overkill before ~1 month of data. Build the split first.

---

## Memory capture: now and later

### Now: inline tag (M1)

Dublog already implements the solus M1 pattern — agents write `[MEMORY]: content`
and `extract_memory_tag` strips and stores it. This is the right base.

### Later: background harvester (R2)

Solus R2 describes a background LLM pass that extracts structured knowledge from
every exchange *without the agent having to tag it explicitly*. This is the natural
upgrade path for memory capture:

- Agent continues to write `[MEMORY]` tags (explicit, high-priority)
- A harvester thread (fire-and-forget, never on critical path) scans each full
  response for additional knowledge items
- Harvested items land in L2 (session archive), tagged items land in L1 first

**Not for MS4** — the explicit tag capture is sufficient while sessions are short.
Add the harvester when explicit tags start to miss too much.

### Key anti-pattern to avoid (AP2)

> Harvester runs synchronously — user waits 3–5 extra seconds after every response.

If/when a harvester is added: it must be `threading.Thread(daemon=True)` or
`asyncio.create_task()`. It must never be on the critical path. If it fails,
log to a dead-letter file — never surface to the user.

---

## Agent isolation and private memory (M3)

Solus AP1 warns:

> If all agents see all memory, they converge toward the dominant interpretation.
> Private memory is not a feature — it is a prerequisite for genuine perspective diversity.

Dublog already has the right structure: `agent_a/memory.md` and `agent_b/memory.md`
are separate. This is M3 implemented at the file level.

**MS4 must preserve this isolation** when splitting L1/L2/L3. Each layer must
remain per-agent, not a shared pool. A shared council layer (M4) is a future option
but requires private banks to exist first.

---

## Convergence: current state and upgrade path

### Current (heuristic word-overlap)

`check_convergence` in `memory.py` compares agent memories with word overlap.
This is a reasonable first check but produces false positives on shared vocabulary.

### Next step (A4 — LLM-scored convergence)

Replace or augment with a small model call that reads both memories and scores
semantic agreement on a 0–1 scale. A cheap model (Haiku or local equivalent)
can do this per round in < 200 tokens.

```python
# Sketch — not for MS4, but the natural upgrade
def llm_convergence_score(mem_a: str, mem_b: str, client) -> float:
    # Cheap model: "Do these two memory banks reflect agreement on
    # the same core conclusions? Score 0.0–1.0."
    # Returns float; caller compares against CONVERGENCE_THRESHOLD
    ...
```

**Relevant solus pattern:** A4 (Convergence Detection), C6 (Circuit Breaker for loops).

### Circuit breaker pattern (C6)

Dublog already has `config.CONVERGENCE_ROUNDS` as a soft circuit breaker —
stop after N consecutive convergent rounds. Solus C6 adds:

- Hash-based exact loop detection (same response appearing again)
- Semantic similarity check (agent is paraphrasing itself)
- Forced intervention text when loop is detected

Low complexity to add to the convergence check loop. Good MS5 candidate.

---

## Control flow: what applies now

### Stop event (C1 partial)

`SessionManager.stop_event` is a manual kill switch — the user can interrupt at
any point. This covers the most important C1 case.

Future C1 additions worth considering:
- Budget kill switch: "if this session exceeds N model calls → stop and warn"
- Deadlock kill switch: "if agents have disagreed M times in a row → halt or escalate"

**AP5 warning:** Kill switch checks must run *before each agent call* in the
orchestrator loop, not only at session start. The current `stop_event.is_set()`
check before each round is correct — keep this pattern.

### No kill switch for convergence deadlock yet

If two agents are locked in a disagreement loop, the current system will run
until `rounds` is exhausted. A future kill switch could detect this and either
halt or inject a moderator message. Parked in `FUTURE_PATCHES.md`.

---

## Infrastructure: what to use and when

### File-based markdown (now)

Correct for the current scale. Simple, debuggable, no dependencies.
Survives crashes, can be read by humans, can be put in git.

### SQLite (when search becomes necessary)

When memory grows beyond ~200 entries per agent, loading the full file per call
becomes wasteful. SQLite is the correct next storage tier:

- No external service, single file, stdlib `sqlite3`
- Enables structured queries: "give me the last 20 facts from L2"
- Enables decay (M6): `UPDATE memory SET weight = weight * 0.95 WHERE ...`
- Enables embeddings via `sqlite-vec` extension for RAG (R3)

**Migration signal:** When `MAX_MEMORY_LINES` starts feeling too blunt as a budget
mechanism, it is time for SQLite.

**Key risk (AP7):** If embeddings are ever added, the embedding model must be stored
alongside the database. Switching models mid-project requires re-embedding the
entire archive. Lock in the model choice early.

### Always use trace (I4 principle)

The existing `telemetry.jsonl` + `validation.jsonl` per session is the equivalent
of I4 (trace). Keep it. Extend it. Never remove it.

Every agent call is already stamped with: round, agent, model, prompt_chars,
memory_lines, history_turns, output_chars, duration_s.

Additions worth making when the system grows:
- Which memory layer was injected
- Whether the harvester ran and how many items it found
- Convergence score per round

---

## Patterns to park (not yet needed)

These solus patterns are relevant to dublog's long-term direction but are
deliberately not in the active roadmap. Each has a `FUTURE_PATCHES.md` entry.

| Pattern | Why it matters | Why it is parked |
|---------|---------------|-----------------|
| R2 Background Harvester | Richer memory capture without agent effort | Explicit tags are enough at current session lengths |
| R3 RAG / cosine search | Find relevant memory without loading everything | Not needed before SQLite migration |
| R1 Librarian Gate | Avoid injecting irrelevant archive context | Not needed before RAG exists |
| M5 Echo Mining | Detect recurring patterns across sessions | < 50 sessions — premature |
| M6 Decay | Old memory loses weight automatically | < 1 month of data — premature |
| A1 Drift Detection | Detect when an agent's voice drifts from its identity | Embedding dependency — add after convergence is upgraded |
| A2 Shadow Workspace | Agent private chain-of-thought before response | CoT can be added to the prompt instead |
| C3 Recursive Council | Diverge → Critique → Converge phases | Requires ≥ 3 agents |
| C5 Cartridge / Phase | Scripted flows with per-phase rules | Only worth it for well-understood session types |
| C7 Values Contradiction | Check requests against stored WHY-memory | No WHY-memory yet |
| I8 Semantic Cache | Cache repeated identical queries | Sessions are unique by design |
| I9 Human-in-the-Loop | Escalate edge cases to human | User is always present in the UI |

---

## The overkill test

Before adding any pattern, ask: **does the system actually need this?**

Solus anti-pattern wisdom condensed:
- Isolation creates divergence. Shared data creates consensus. (Keep memories separate.)
- Background jobs must never block the user. (Fire-and-forget or not at all.)
- Memory without time is noise. (Add decay only when old data actually causes problems.)
- Evaluate output, not only flow. (A run that completes is not a run that works.)
- Start with trace. Always. (telemetry.jsonl is non-negotiable — already done.)

---

## Natural build order (MS4 and beyond)

```
MS4 (now active)
├── Split L1 / L2 per agent (session_memory.md + archive.md)
├── Archive session memory on session end (promotion step 0)
├── Define L2 → L3 promotion rule (manual for now)
└── Update validate_memory_entry() for L1 vs L2 context

MS5 (streaming + cleanup)
├── Cleaner session lifecycle (success / stop / error paths)
├── Optional: circuit breaker hash check inside convergence loop
└── Live streaming verification

Later (when complexity demands it)
├── LLM-scored convergence (A4 upgrade to check_convergence)
├── Budget kill switch (C1 extension in run_conversation)
├── SQLite migration (when > 200 memory items per agent)
├── RAG + Librarian Gate (after SQLite)
└── Background harvester (after RAG proves its value)
```

The governing principle: **build each layer only when the previous layer shows
the strain that makes the next layer necessary.**
