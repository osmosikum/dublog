"""
Memory IO — three-layer model (L1 / L2 / L3).

Layer summary
-------------
L1  session_memory.md   Written during a run. Cleared after archive_session_memory().
L2  archive.md          Cross-session knowledge. Grows via L1 promotion on session end.
L3  permanent.md        Permanent facts. Manual promotion only. Not read here yet.

Public API
----------
load_memory(agent_dir, max_archive_lines)
    Combine L1 + L2 for prompt injection. L1 always fully included.
    L2 capped at max_archive_lines most-recent entries.

append_memory(agent_dir, entry, tag)
    Write a new entry to L1 (session_memory.md).

archive_session_memory(agent_dir, min_words)
    Promote non-trivial, non-duplicate L1 entries to L2 (archive.md).
    Clear L1. Return count of promoted entries.

extract_memory_tag(response)
    Parse [MEMORY]: text from a model response.

check_convergence(memory_a, memory_b, threshold)
    Heuristic word-overlap convergence check across two memory strings.

log_conversation(speaker, content, round_num, session_dir)
    Append a conversation turn to session_dir/conversation.md.

Legacy migration
----------------
If a project has memory.md but not archive.md, _migrate_legacy_memory() renames
memory.md → archive.md on first access. No manual intervention needed.
"""

import re
from pathlib import Path
from datetime import datetime


# ── Legacy migration ───────────────────────────────────────────────────────────

def _migrate_legacy_memory(agent_dir: Path) -> None:
    """
    One-time migration: rename memory.md → archive.md if archive.md does not
    yet exist. Keeps existing projects working without manual intervention.
    """
    legacy  = agent_dir / "memory.md"
    archive = agent_dir / "archive.md"
    if legacy.exists() and not archive.exists():
        legacy.rename(archive)


# ── Internal helpers ───────────────────────────────────────────────────────────

def _read_lines(path: Path) -> list[str]:
    """Return non-empty stripped lines from a file. Empty list if file absent."""
    if not path.exists():
        return []
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


# ── Public API ─────────────────────────────────────────────────────────────────

def load_memory(agent_dir: str, max_archive_lines: int) -> str:
    """
    Return combined L1 (session) + L2 (archive) memory for prompt injection.

    L1 (session_memory.md) is fully included — it is session-scoped and small.
    L2 (archive.md) is capped at max_archive_lines most-recent entries.

    When both layers have content the returned string has section headers so the
    agent can distinguish current-session notes from long-term knowledge:

        [Archive]
        [FACT] ...

        [This session]
        [FACT] ...

    If only one layer has content, no headers are added — the memory reads
    naturally as a plain list of facts.
    """
    dir_path = Path(agent_dir)
    _migrate_legacy_memory(dir_path)

    l2_lines = _read_lines(dir_path / "archive.md")[-max_archive_lines:]
    l1_lines = _read_lines(dir_path / "session_memory.md")

    if l2_lines and l1_lines:
        return (
            "[Archive]\n"        + "\n".join(l2_lines)  +
            "\n\n[This session]\n" + "\n".join(l1_lines)
        )
    if l2_lines:
        return "\n".join(l2_lines)
    if l1_lines:
        return "\n".join(l1_lines)
    return ""


def extract_memory_tag(response: str) -> str:
    """Parse [MEMORY]: text from a model response. Returns empty string if absent."""
    match = re.search(r'\[MEMORY\]:\s*(.+)', response, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def append_memory(agent_dir: str, entry: str, tag: str = "FACT") -> None:
    """
    Write a new entry to L1 (session_memory.md).

    Called during a run after each [MEMORY] tag is extracted.
    L1 entries are promoted to L2 at session end via archive_session_memory().
    """
    if not entry:
        return
    dir_path = Path(agent_dir)
    _migrate_legacy_memory(dir_path)
    path = dir_path / "session_memory.md"
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{tag.upper()}] {entry}\n")


def archive_session_memory(agent_dir: str, min_words: int = 4) -> int:
    """
    Promote L1 (session_memory.md) entries to L2 (archive.md).

    Promotion rules — first version (L2 → L3 is manual only):
    - Entry must have at least min_words words  (filters noise / one-liners).
    - Entry must not already appear in the archive (exact match, case-insensitive).

    Clears session_memory.md after promotion.
    Returns the number of entries promoted.
    """
    dir_path = Path(agent_dir)
    _migrate_legacy_memory(dir_path)

    l1_path = dir_path / "session_memory.md"
    l2_path = dir_path / "archive.md"

    l1_lines = _read_lines(l1_path)
    if not l1_lines:
        return 0

    l2_existing = {l.lower() for l in _read_lines(l2_path)}

    promoted = 0
    with open(l2_path, "a", encoding="utf-8") as f:
        for line in l1_lines:
            if len(line.split()) < min_words:
                continue                    # Too short — discard
            if line.lower() in l2_existing:
                continue                    # Duplicate — skip
            f.write(line + "\n")
            l2_existing.add(line.lower())
            promoted += 1

    l1_path.write_text("", encoding="utf-8")  # Clear L1 — session is over
    return promoted


def check_loop(response: str, recent_hashes: list, window: int = 3) -> bool:
    """
    Detect whether a response is a near-exact repeat of a recent one.

    Computes an MD5 hash of the normalised response text and checks it against
    the last `window` entries in recent_hashes. Appends the new hash before
    returning so the list grows automatically — callers just pass the same list
    each round without managing it themselves.

    Returns True (loop detected) when the hash matches any entry in the window.

    Usage in run_conversation:
        hashes_a: list = []
        ...
        if check_loop(response_a, hashes_a):
            output_fn(">>> [LOOP DETECTED] Agent A repeated a near-identical response.")
    """
    import hashlib
    normalised = " ".join(response.lower().split())
    h = hashlib.md5(normalised.encode()).hexdigest()
    detected = h in recent_hashes[-window:]
    recent_hashes.append(h)
    return detected


def check_convergence(memory_a: str, memory_b: str, threshold: float = 0.4) -> bool:
    """
    Heuristic convergence: flag when the two agents' memories share enough
    non-trivial vocabulary. Operates on the full combined string returned by
    load_memory() so both L1 and L2 content contributes to the score.
    """
    if not memory_a or not memory_b:
        return False
    stop_words = {
        "er", "og", "at", "en", "et", "den", "det", "de", "jeg", "ikke",
        "the", "is", "a", "an", "and", "that", "it", "in", "to", "of",
        # Layer headers — exclude so they don't inflate the overlap score
        "[archive]", "[this", "session]",
    }
    words_a = set(memory_a.lower().split()) - stop_words
    words_b = set(memory_b.lower().split()) - stop_words
    if not words_a or not words_b:
        return False
    return len(words_a & words_b) / min(len(words_a), len(words_b)) >= threshold


def log_conversation(speaker: str, content: str, round_num: int, session_dir) -> None:
    """Append a conversation turn to session_dir/conversation.md."""
    path = Path(session_dir) / "conversation.md"
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n---\n**Round {round_num} | {speaker}** _{timestamp}_\n\n{content}\n")
