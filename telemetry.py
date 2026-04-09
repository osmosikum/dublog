"""
Telemetry — per-call metrics appended to session_dir/telemetry.jsonl.

Each line is a JSON object recorded after every agent model call:

    round          — conversation round number (1-based)
    agent          — agent display name
    model          — model identifier string
    prompt_chars   — total characters in system prompt + all messages sent
    memory_lines   — number of memory lines injected into the prompt
    history_turns  — number of prior conversation turns sent as context
    output_chars   — response length in characters (before [MEMORY] strip)
    duration_s     — model call wall-clock duration in seconds
    timestamp      — ISO 8601 timestamp (second precision)

load_telemetry returns the entries as a list of dicts, skipping any
malformed lines silently.
"""

import json
from datetime import datetime
from pathlib import Path


def record_call(
    session_dir: Path,
    round_num: int,
    agent: str,
    model: str,
    prompt_chars: int,
    memory_lines: int,
    history_turns: int,
    output_chars: int,
    duration_s: float,
) -> None:
    entry = {
        "round":         round_num,
        "agent":         agent,
        "model":         model,
        "prompt_chars":  prompt_chars,
        "memory_lines":  memory_lines,
        "history_turns": history_turns,
        "output_chars":  output_chars,
        "duration_s":    round(duration_s, 2),
        "timestamp":     datetime.now().isoformat(timespec="seconds"),
    }
    path = Path(session_dir) / "telemetry.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def load_telemetry(session_dir: Path) -> list[dict]:
    path = Path(session_dir) / "telemetry.jsonl"
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries
