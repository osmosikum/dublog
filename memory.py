import re
from pathlib import Path
from datetime import datetime


def load_memory(agent_dir: str, max_lines: int) -> str:
    path = Path(agent_dir) / "memory.md"
    if not path.exists():
        return ""
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return "\n".join(lines[-max_lines:])


def extract_memory_tag(response: str) -> str:
    match = re.search(r'\[MEMORY\]:\s*(.+)', response, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def append_memory(agent_dir: str, entry: str, tag: str = "FACT") -> None:
    if not entry:
        return
    path = Path(agent_dir) / "memory.md"
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{tag.upper()}] {entry}\n")


def check_convergence(memory_a: str, memory_b: str, threshold: float = 0.4) -> bool:
    if not memory_a or not memory_b:
        return False
    stop_words = {
        "er", "og", "at", "en", "et", "den", "det", "de", "jeg", "ikke",
        "the", "is", "a", "an", "and", "that", "it", "in", "to", "of"
    }
    words_a = set(memory_a.lower().split()) - stop_words
    words_b = set(memory_b.lower().split()) - stop_words
    if not words_a or not words_b:
        return False
    return len(words_a & words_b) / min(len(words_a), len(words_b)) >= threshold


def log_conversation(speaker: str, content: str, round_num: int, project_dir) -> None:
    path = Path(project_dir) / "shared" / "conversation.md"
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n---\n**Runde {round_num} | {speaker}** _{timestamp}_\n\n{content}\n")
