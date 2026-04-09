# Multi-Agent Sandbox

To lokale AI-agenter diskuterer et emne og husker i lag.
Designet til at hjælpe små lokale modeller holde kursen.

Hvis du styrer repoet aktivt, så læs også `.guides/project_control.md`.

---

## 1. How to run

**Med UI (anbefalet):**
```bash
pip install requests
python app.py
# → åbn http://localhost:7842
```

**CLI kun:**
```bash
pip install requests
python main.py
```

Kræver [Ollama](https://ollama.com) installeret og en model pullet:
```bash
ollama pull gemma3:4b
```

---

## 2. How to change topic and agents

Åbn `http://localhost:7842` — alt konfigureres i UI:
- Emne og antal runder
- Identitet, sprog og svarlængde per agent
- Model per agent
- Projekt (eget mapperum med memory og log)

For CLI: åbn `config.py` og skift `TOPIC`, `ROUNDS`, `AGENT_A["model"]` etc.

---

## 3. How to add an identity

Opret en ny fil i `identities/`:

```markdown
---
name: Mit Navn
language: dansk
length: medium
---

# Mit Navn

[Beskriv personligheden...]

Tal altid i første person.
Slut altid dit svar med: [MEMORY]: <din vigtigste pointe fra denne runde>
```

Brug `identities/template.md` som udgangspunkt.
Filen dukker automatisk op i identity-dropdowns ved næste sideopdatering.

---

## 4. How to switch backend

Vælg backend i UI-dropdownen (Ollama / LM Studio / Claude API).

For CLI: åbn `config.py` og skift `BACKEND`:
```python
BACKEND = "ollama"      # lokal Ollama (default)
BACKEND = "lmstudio"   # lokal LM Studio
BACKEND = "claude"     # Anthropic Claude API
```

For Claude-backend: sæt miljøvariablen `ANTHROPIC_API_KEY`.

---

## 5. Projects

Hvert projekt har sit eget mapperum under `projects/`:

```
projects/mit-projekt/
    agent_a/memory.md
    agent_b/memory.md
    shared/conversation.md
    settings.json
```

Opret nye projekter med **＋**-knappen i UI. Settings gemmes automatisk ved hvert run og restores ved projektwitch.

`projects/` er gitignored — runtime-data ryger ikke i repoet.

---

## 6. Memory format

Agenter gemmer pointer løbende i `agent_x/memory.md` via `[MEMORY]:`-tagget i svarene.

Memory re-injiceres i hvert prompt (budgetbegrænset til `MAX_MEMORY_LINES` i `config.py`).

---

## 7. File overview

| Fil | Formål |
|-----|--------|
| `app.py` | Web-server og SSE-streaming (port 7842) |
| `main.py` | Samtale-orchestrator — `run_conversation(session_cfg)` |
| `config.py` | Statiske defaults til CLI-kørsel |
| `model.py` | Model-adapter: Ollama, LM Studio, Claude API |
| `prompts.py` | Prompt-builder: identity + instruktioner + memory |
| `memory.py` | Memory-IO: load, append, extract, konvergens-check |
| `identities.py` | Parser og lister identity-filer fra `identities/` |
| `projects.py` | Projekt-management: opret, list, load/save settings |
| `identities/*.md` | Persona-filer med frontmatter |
| `identities/template.md` | Skabelon til nye identiteter |
| `ui/index.html` | Enkeltfils frontend |
| `projects/<navn>/` | Runtime-data per projekt (gitignored) |
