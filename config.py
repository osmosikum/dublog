# ── Static server config ──────────────────────────────────────────────────────
# These values are used as defaults when running main.py from the CLI.
# When using the web UI (app.py), all settings are passed per-run via session_cfg
# and stored in projects/{name}/settings.json — this file is not mutated at runtime.

# === SAMTALE ===
TOPIC  = "Er AI en trussel eller en mulighed for samfundet?"
ROUNDS = 6

# === CLI AGENT DEFAULTS ===
AGENT_A = {
    "name":  "Skeptikeren",
    "model": "gemma3:4b",
}

AGENT_B = {
    "name":  "Optimisten",
    "model": "gemma3:4b",
}

# === CLI IDENTITY DEFAULTS ===
IDENTITY_A = "skeptikeren"
IDENTITY_B = "optimisten"
LANGUAGE_A = "dansk"
LANGUAGE_B = "dansk"
LENGTH_A   = "medium"
LENGTH_B   = "medium"

# === MODEL BACKEND ===
BACKEND = "ollama"  # "ollama" | "lmstudio" | "claude"

OLLAMA_URL   = "http://localhost:11434/api/chat"
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
# CLAUDE_API_KEY hentes fra env: ANTHROPIC_API_KEY

# === MEMORY BUDGET ===
MAX_MEMORY_LINES  = 10
MAX_HISTORY_TURNS = 4

# === KONVERGENS ===
CONVERGENCE_CHECK  = True
CONVERGENCE_ROUNDS = 2
