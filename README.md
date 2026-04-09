# Multi-Agent Sandbox

To lokale AI-agenter diskuterer et emne og husker i lag.
Designet til at hjælpe små lokale modeller holde kursen.

Hvis du styrer repoet aktivt, så læs også `.guides/project_control.md`.

---

## 1. How to run

```bash
pip install requests
ollama serve
python main.py
```

Kræver [Ollama](https://ollama.com) installeret og en model pullet, f.eks.:
```bash
ollama pull gemma3:4b
```

---

## 2. How to change topic

Åbn `config.py` og skift `TOPIC`:

```python
TOPIC = "Dit emne her"
```

---

## 3. How to swap model

Åbn `config.py` og skift `model` under `AGENT_A` eller `AGENT_B`:

```python
AGENT_A = {
    "name": "Skeptikeren",
    "model": "mistral:7b",   # ← skift her
    "dir": "agent_a"
}
```

Modellen skal være tilgængelig via den valgte backend.

---

## 4. How to switch backend

Åbn `config.py` og skift `BACKEND`:

```python
BACKEND = "ollama"      # lokal Ollama (default)
BACKEND = "lmstudio"   # lokal LM Studio
BACKEND = "claude"     # Anthropic Claude API
```

For Claude-backend: sæt miljøvariablen `ANTHROPIC_API_KEY` og skift model til f.eks. `"claude-sonnet-4-6"`.

---

## 5. Memory format

Hver agent gemmer løbende pointer i `agent_x/memory.md` med tags:

| Tag | Betydning |
|-----|-----------|
| `[FACT]` | Faktuel observation fra samtalen |
| `[WHY]` | Agentens begrundelse eller motivation |
| `[STANCE]` | Agentens overordnede holdning |

Eksempel:
```
[FACT] AI erstatter allerede lavkvalifikationsjobs.
[WHY] Jeg er skeptisk fordi historisk disruption rammer skævt.
[STANCE] Neutral teknologi — kontekst bestemmer konsekvens.
```

Memory re-injiceres i hvert prompt (budgetbegrænset til `MAX_MEMORY_LINES`).

---

## 6. File overview

| Fil | Formål |
|-----|--------|
| `config.py` | Al konfiguration — topic, agenter, backend, budgets |
| `model.py` | Model-adapter til Ollama, LM Studio og Claude API |
| `memory.py` | Læs, skriv, udtræk og konvergens-check på memory |
| `prompts.py` | Bygger strukturerede system-prompts og user-messages |
| `main.py` | Orchestrator og hoved-loop |
| `agent_a/identity.md` | Skeptikerens persona (re-injiceres hver runde) |
| `agent_b/identity.md` | Optimistens persona (re-injiceres hver runde) |
| `agent_a/memory.md` | Skeptikerens akkumulerede hukommelse |
| `agent_b/memory.md` | Optimistens akkumulerede hukommelse |
| `shared/conversation.md` | Fuld samtale-log med timestamps |
| `shared/run_config.md` | Hvad der faktisk kørte (gemmes ved hvert run) |
