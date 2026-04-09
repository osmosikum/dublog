"""
Validators — lightweight contract checks for agent responses and memory entries.

Design principles
-----------------
- Each check is a standalone function returning a single ValidationResult.
- Composite validators (validate_response, validate_memory_entry) call check
  functions and return a list — easy to extend by appending new checks.
- ValidationResult is a plain dataclass: serialisable to dict, no external deps.
- Validation never hard-fails a run; it records and echoes deviations.
- Memory validation is deliberately kept as a separate function so it can grow
  independently as memory architecture matures (Milestone 4+).

Output
------
Results are written to session_dir/validation.jsonl (one JSON object per
agent call) by record_validation(). Failures are echoed to the run output
by the caller (run_conversation in main.py).

Adding a new check
------------------
1. Write a check_* function that returns ValidationResult.
2. Call it inside validate_response() or validate_memory_entry().
That is all.
"""

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


# ── Core type ─────────────────────────────────────────────────────────────────

@dataclass
class ValidationResult:
    check:   str         # machine-readable name, e.g. "memory_tag_present"
    passed:  bool
    level:   str         # "error" | "warning" | "info"
    message: str         # human-readable description
    value:   str | None = None  # what was actually found (populated on failure)


# ── Response checks ───────────────────────────────────────────────────────────

def check_not_empty(response: str) -> ValidationResult:
    passed = bool(response and response.strip())
    return ValidationResult(
        check="response_not_empty",
        passed=passed,
        level="error",
        message="Response is empty" if not passed else "Response has content",
    )


def check_memory_tag(response: str) -> ValidationResult:
    """Verify that [MEMORY]: is present and has non-empty content."""
    match = re.search(r'\[MEMORY\]:\s*(.+)', response, re.IGNORECASE)
    content = match.group(1).strip() if match else ""
    passed = bool(content)
    return ValidationResult(
        check="memory_tag_present",
        passed=passed,
        level="warning",
        message="[MEMORY] tag missing or empty" if not passed else "[MEMORY] tag present",
        value=None if passed else "(empty)" if match else "(absent)",
    )


# ── Length check ──────────────────────────────────────────────────────────────

# Inclusive sentence ranges per canonical length preset.
# A response is flagged only when clearly outside the range — the bounds are
# intentionally generous so models get slack for topic-specific variation.
_LENGTH_RANGES: dict[str, tuple[int, int]] = {
    "short":  (1, 5),
    "medium": (2, 10),
    "long":   (5, 18),
}


def _count_sentences(text: str) -> int:
    """Rough sentence count: split on terminal punctuation followed by space."""
    segments = re.split(r'[.!?]+(?:\s|$)', text.strip())
    return len([s for s in segments if s.strip()])


def check_length(response: str, expected: str) -> ValidationResult:
    """Flag responses clearly outside the expected sentence-count range."""
    bounds = _LENGTH_RANGES.get(expected)
    if bounds is None:
        return ValidationResult(
            check="length_in_range",
            passed=True,
            level="info",
            message=f"Unknown length preset '{expected}' — skipped",
        )
    lo, hi = bounds
    count = _count_sentences(response)
    passed = lo <= count <= hi
    return ValidationResult(
        check="length_in_range",
        passed=passed,
        level="warning",
        message=(
            f"Response has ~{count} sentences (expected {lo}–{hi} for '{expected}')"
            if not passed
            else f"Response length OK (~{count} sentences for '{expected}')"
        ),
        value=str(count) if not passed else None,
    )


# ── Language check ────────────────────────────────────────────────────────────

# Common short words that are reliable markers for each language.
# The lists overlap deliberately — we score all languages and compare.
_LANGUAGE_MARKERS: dict[str, set[str]] = {
    "danish": {
        "og", "er", "at", "en", "et", "den", "det", "de", "ikke", "men",
        "har", "vil", "kan", "med", "til", "som", "fra", "der", "jeg",
        "du", "vi", "på", "af", "sig", "var", "blev", "hvis",
    },
    "english": {
        "the", "is", "are", "and", "that", "this", "with", "have", "will",
        "can", "from", "not", "but", "for", "you", "we", "they", "be",
        "to", "of", "in", "it", "was", "has", "if", "by",
    },
    "norwegian": {
        "og", "er", "at", "en", "et", "den", "det", "ikke", "men",
        "har", "vil", "kan", "med", "til", "som", "fra", "jeg",
        "du", "vi", "på", "av", "seg", "var", "ble", "hvis",
    },
    "swedish": {
        "och", "är", "att", "en", "ett", "den", "det", "inte", "men",
        "har", "vill", "kan", "med", "till", "som", "från", "jag",
        "du", "vi", "på", "av", "sig", "var", "blev", "om",
    },
}

# Minimum word count before triggering the language check.
# Short responses are too unreliable for heuristic detection.
_LANG_MIN_WORDS = 20

# Expected-language score must be at least this fraction of the top scorer's
# score to pass. Tuned to allow topic-specific English terms in a Danish text.
_LANG_SCORE_RATIO = 0.50


def check_language(response: str, expected: str) -> ValidationResult:
    """
    Heuristic: score each language by how many of its marker words appear
    in the response. Flag if the expected language scores significantly
    lower than the apparent language.
    """
    words = re.findall(r'\b\w+\b', response.lower())
    if len(words) < _LANG_MIN_WORDS:
        return ValidationResult(
            check="language_match",
            passed=True,
            level="info",
            message=f"Response too short for language check ({len(words)} words)",
        )

    word_set = set(words)
    scores: dict[str, float] = {}
    for lang, markers in _LANGUAGE_MARKERS.items():
        hits = len(word_set & markers)
        scores[lang] = hits / len(markers)

    top_lang  = max(scores, key=lambda k: scores[k])
    top_score = scores[top_lang]
    exp_score = scores.get(expected, 0.0)

    # Pass if expected language leads or is within the ratio threshold.
    passed = (top_lang == expected) or (top_score == 0) or (exp_score >= top_score * _LANG_SCORE_RATIO)

    return ValidationResult(
        check="language_match",
        passed=passed,
        level="warning",
        message=(
            f"Apparent language '{top_lang}' (score {top_score:.2f}) "
            f"vs expected '{expected}' (score {exp_score:.2f})"
            if not passed
            else f"Language check OK (expected '{expected}', score {exp_score:.2f})"
        ),
        value=top_lang if not passed else None,
    )


# ── Composite response validator ──────────────────────────────────────────────

def validate_response(
    response: str,
    expected_language: str = "danish",
    expected_length: str = "medium",
) -> list[ValidationResult]:
    """
    Run all response-level checks. Add new check_* calls here to extend.
    Order matters: empty check runs first so later checks skip gracefully.
    """
    results = [
        check_not_empty(response),
        check_memory_tag(response),
        check_length(response, expected_length),
        check_language(response, expected_language),
    ]
    return results


# ── Memory entry validator ────────────────────────────────────────────────────

# Word-count bounds per memory layer.
# L1 (session) entries are ephemeral working notes — generous upper bound.
# L2 (archive) candidates should be tighter: concise, distilled key points.
# Both layers share a minimum so noise / one-word entries are caught early.
_MEMORY_ENTRY_MIN_WORDS   =  4   # Below this: too short to be meaningful
_MEMORY_ENTRY_MAX_WORDS   = 35   # L1 session entries
_MEMORY_ARCHIVE_MAX_WORDS = 30   # L2 archive candidates (stricter upper bound)


def check_memory_entry_length(entry: str, layer: str = "L1") -> ValidationResult:
    """
    Check memory entry word count.

    layer: "L1" for entries written during a run (default),
           "L2" for entries being promoted to the archive.

    L2 entries get a 5-word stricter upper bound. Both layers share the
    same minimum so noise entries are caught regardless of destination.
    """
    words = len(entry.split())
    max_words = _MEMORY_ARCHIVE_MAX_WORDS if layer == "L2" else _MEMORY_ENTRY_MAX_WORDS

    too_long  = words > max_words
    too_short = words < _MEMORY_ENTRY_MIN_WORDS
    passed    = not too_long and not too_short

    if too_long:
        message = (
            f"Memory entry is {words} words "
            f"(max {max_words} for {layer})"
        )
    elif too_short:
        message = (
            f"Memory entry is {words} words — "
            f"too short to be meaningful (min {_MEMORY_ENTRY_MIN_WORDS})"
        )
    else:
        message = f"Memory entry length OK ({words} words, {layer})"

    return ValidationResult(
        check="memory_entry_length",
        passed=passed,
        level="warning",
        message=message,
        value=str(words) if not passed else None,
    )


def validate_memory_entry(entry: str, layer: str = "L1") -> list[ValidationResult]:
    """
    Run all memory-entry-level checks.

    layer: "L1" for entries written during a run (default),
           "L2" for entries being promoted to the archive.

    This is the designated extension point for MS4+ memory work — add new
    check_* calls here to extend validation for either or both layers.
    """
    return [
        check_memory_entry_length(entry, layer),
    ]


# ── Identity validator ────────────────────────────────────────────────────────

_REQUIRED_IDENTITY_FIELDS = ("name", "language", "length", "content")


def validate_identity(identity: dict) -> list[ValidationResult]:
    """
    Check that an identity dict has all required fields with non-empty values.
    Intended for load-time use; not wired into the run flow in this milestone.
    """
    results = []
    for field in _REQUIRED_IDENTITY_FIELDS:
        present = bool(identity.get(field, ""))
        results.append(ValidationResult(
            check=f"identity_has_{field}",
            passed=present,
            level="warning",
            message=(
                f"Identity missing or empty field: '{field}'"
                if not present
                else f"Identity field '{field}' present"
            ),
        ))
    return results


# ── IO ────────────────────────────────────────────────────────────────────────

def record_validation(
    session_dir: Path,
    round_num: int,
    agent: str,
    results: list[ValidationResult],
) -> None:
    """Append one JSONL entry per agent call to session_dir/validation.jsonl."""
    entry = {
        "round":   round_num,
        "agent":   agent,
        "results": [asdict(r) for r in results],
    }
    path = Path(session_dir) / "validation.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def load_validation(session_dir: Path) -> list[dict]:
    """Read validation.jsonl back as a list of dicts. Skips malformed lines."""
    path = Path(session_dir) / "validation.jsonl"
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
