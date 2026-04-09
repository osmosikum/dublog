# ── Static server config ──────────────────────────────────────────────────────
# These values are used as defaults when running main.py from the CLI.
# When using the web UI (app.py), all settings are passed per-run via session_cfg
# and stored in projects/{name}/settings.json — this file is not mutated at runtime.

# === CONVERSATION ===
TOPIC  = "Is AI a threat or an opportunity for society?"
ROUNDS = 6

# === CLI AGENT DEFAULTS ===
AGENT_A = {
    "name":  "The Skeptic",
    "model": "gemma3:4b",
}

AGENT_B = {
    "name":  "The Optimist",
    "model": "gemma3:4b",
}

# === CLI IDENTITY DEFAULTS ===
IDENTITY_A = "ent_kasper"
IDENTITY_B = "ent_leon"
LANGUAGE_A = "danish"
LANGUAGE_B = "danish"
LENGTH_A   = "medium"
LENGTH_B   = "medium"

# === MODEL BACKEND ===
BACKEND = "ollama"  # "ollama" | "lmstudio" | "claude"

OLLAMA_URL   = "http://localhost:11434/api/chat"
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
# CLAUDE_API_KEY is read from env: ANTHROPIC_API_KEY

# === MEMORY BUDGET ===
MAX_MEMORY_LINES  = 10
MAX_HISTORY_TURNS = 4

# === CONVERGENCE ===
CONVERGENCE_CHECK  = True
CONVERGENCE_ROUNDS = 2
