# Multi-Agent Sandbox

Two local AI agents discuss a topic and build memory in layers.
Designed to help small local models stay on track.

If you are actively managing the repo, also read `.guides/project_control.md`.

---

## 1. How to run

**With UI (recommended):**
```bash
pip install requests
python app.py
# → open http://localhost:7842
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

Open `http://localhost:7842` — everything is configured in the UI:
- Topic and number of rounds
- Identity, language and response length per agent
- Model per agent
- Project (separate directory with memory and log)

For CLI: open `config.py` and change `TOPIC`, `ROUNDS`, `AGENT_A["model"]` etc.

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

- `identities/template.md` — tracked template
- `identities/examples/*.md` — tracked example identities
- `identities/custom/*.md` — local identities, gitignored but automatically loaded

The file will automatically appear in the identity dropdowns on the next page refresh.

---

## 4. How to switch backend

Select the backend in the UI dropdown (Ollama / LM Studio / Claude API).

For CLI: open `config.py` and change `BACKEND`:
```python
BACKEND = "ollama"      # local Ollama (default)
BACKEND = "lmstudio"   # local LM Studio
BACKEND = "claude"     # Anthropic Claude API
```

For the Claude backend: set the environment variable `ANTHROPIC_API_KEY`.

---

## 5. Projects

Each project has its own directory under `projects/`:

```
projects/my-project/
    agent_a/memory.md
    agent_b/memory.md
    settings.json
    sessions/
        20260409-123456/
            conversation.md
            run_config.md
```

Create new projects with the **＋** button in the UI. Settings are saved automatically on every run and restored on project switch.

`projects/` is gitignored — runtime data does not end up in the repo.

---

## 6. Memory format

Agents store notes continuously in `projects/<project>/agent_x/memory.md` via the `[MEMORY]:` tag in their responses.

Memory is re-injected into every prompt (budget-limited to `MAX_MEMORY_LINES` in `config.py`).

---

## 7. File overview

| File | Purpose |
|------|---------|
| `app.py` | Web server and SSE streaming (port 7842) |
| `main.py` | Conversation orchestrator — `run_conversation(session_cfg)` |
| `config.py` | Static defaults for CLI runs |
| `model.py` | Model adapter: Ollama, LM Studio, Claude API |
| `prompts.py` | Prompt builder: identity + instructions + memory |
| `memory.py` | Memory IO: load, append, extract, convergence check |
| `identities.py` | Parser and lister for identity files from `identities/` |
| `projects.py` | Project management: create, list, load/save settings |
| `identities/README.md` | Explains the difference between template, examples and custom |
| `identities/examples/*.md` | Repo-shipped example identities |
| `identities/custom/*.md` | Local identities (gitignored) |
| `identities/template.md` | Template for new identities |
| `ui/index.html` | Single-file frontend |
| `projects/<name>/` | Runtime data per project (gitignored) |
