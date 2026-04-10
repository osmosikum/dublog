# Multi-Agent Sandbox

Two local AI agents discuss a topic and build memory in layers. The project is
designed to help small local models stay on track while remaining easy to
inspect and debug.

If you are actively managing the repo, also read `.guides/project_control.md`.
If you are coordinating multiple code agents, read `.guides/tri_agent_setup.md`.

---

## 1. How to run

**With UI (recommended):**

```bash
pip install requests
python app.py
# -> open http://localhost:7842
```

**CLI only:**

```bash
pip install requests
python main.py
```

Requires [Ollama](https://ollama.com) installed and a model pulled:

```bash
ollama pull gemma3:4b
```

---

## 2. How to change topic and agents

Open `http://localhost:7842` - everything is configured in the UI:

- topic and number of rounds
- identity, language, and response length per agent
- model per agent
- project (separate directory with memory and session logs)

For CLI: open `config.py` and change `TOPIC`, `ROUNDS`, `AGENT_A["model"]`,
and related defaults.

---

## 3. How to add an identity

New identities should normally go in `identities/custom/`:

```markdown
---
name: My Name
language: danish
length: medium
---

# My Name

[Describe the personality...]

Always speak in the first person.
End your answer with: [MEMORY]: <your most important point from this round>
```

Use `identities/template.md` as a starting point.

Identity structure:

- `identities/template.md` - tracked template
- `identities/examples/*.md` - tracked example identities
- `identities/custom/*.md` - local identities, gitignored but automatically
  loaded

The file will automatically appear in the identity dropdowns on the next page
refresh.

---

## 4. How to switch backend

Select the backend in the UI dropdown (Ollama / LM Studio / Claude API).

For CLI: open `config.py` and change `BACKEND`:

```python
BACKEND = "ollama"    # local Ollama (default)
BACKEND = "lmstudio"  # local LM Studio
BACKEND = "claude"    # Anthropic Claude API
```

For the Claude backend: set the environment variable `ANTHROPIC_API_KEY`.

---

## 5. Projects and sessions

Each project has its own directory under `projects/`:

```text
projects/my-project/
    settings.json
    agent_a/
        session_memory.md
        archive.md
        permanent.md
    agent_b/
        session_memory.md
        archive.md
        permanent.md
    sessions/
        20260410-123456/
            conversation.md
            run_config.md
            telemetry.jsonl
            validation.jsonl
```

Create new projects with the **+** button in the UI. Settings are saved
automatically on every run and restored on project switch.

`projects/` is gitignored - runtime data does not end up in the repo.

---

## 6. Memory model

Agents store notes through the `[MEMORY]:` tag in their responses.

- tagged notes first land in `session_memory.md` (L1)
- at session end, non-trivial and non-duplicate L1 entries are promoted to
  `archive.md` (L2)
- `permanent.md` (L3) exists for manual promotion only and is not yet read by
  the engine

Prompt memory is injected from the current agent's L1 and L2 files, bounded by
`MAX_MEMORY_LINES` in `config.py`.

More detail lives in `.guides/scaling_architecture.md`.

---

## 7. Observability and validation

Each session directory can contain:

- `telemetry.jsonl` - per-call prompt, memory, history, output, and duration
  metrics
- `validation.jsonl` - post-call contract checks such as empty output, missing
  `[MEMORY]`, language drift, and length drift

The UI polls `/api/telemetry` during runs, so you can inspect these metrics
live from the debug panel.

---

## 8. File overview

| File | Purpose |
|------|---------|
| `app.py` | Web server and SSE streaming (port 7842) |
| `main.py` | Conversation orchestrator - `run_conversation(session_cfg)` |
| `sessions.py` | `SessionManager` for runtime lifecycle and state |
| `telemetry.py` | Per-call metrics -> `telemetry.jsonl` |
| `validators.py` | Contract checks -> `validation.jsonl` |
| `normalization.py` | Read-compatibility for legacy Danish enum values |
| `config.py` | Static defaults for CLI runs |
| `model.py` | Model adapter: Ollama, LM Studio, Claude API |
| `prompts.py` | Prompt builder: identity + instructions + memory |
| `memory.py` | Memory IO: load, append, extract, archive, convergence |
| `identities.py` | Parser and lister for identity files from `identities/` |
| `projects.py` | Project management: create, list, load/save settings |
| `.agents/` | Role entry points for top-level agents and bounded sub-agents |
| `.guides/tri_agent_setup.md` | Repo-specific routing baseline for multi-agent work |
| `ui/index.html` | Single-file frontend |
| `projects/<name>/` | Runtime data per project (gitignored) |
