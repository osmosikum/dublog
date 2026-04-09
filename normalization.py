"""
Compatibility helpers for legacy Danish values and future English canon.

This module keeps runtime reads tolerant while the repo transitions to
English-facing engine values. It does not force storage migration by itself.
"""

LANGUAGE_ALIASES = {
    "dansk": "danish",
    "danish": "danish",
    "engelsk": "english",
    "english": "english",
    "norsk": "norwegian",
    "norwegian": "norwegian",
    "svensk": "swedish",
    "swedish": "swedish",
}

LENGTH_ALIASES = {
    "kort": "short",
    "short": "short",
    "medium": "medium",
    "lang": "long",
    "long": "long",
}

IDENTITY_ALIASES = {
    "skeptikeren": "ent_kasper",
    "optimisten": "ent_leon",
    "moderatoren": "ent_maya",
    "djaevlens-advokat": "ent_viktor",
}

PROMPT_LANGUAGE_LABELS = {
    "danish": "dansk",
    "english": "engelsk",
    "norwegian": "norsk",
    "swedish": "svensk",
}


def _normalized_key(value, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip().lower()
    return text or default


def normalize_language(value, default: str = "danish") -> str:
    return LANGUAGE_ALIASES.get(_normalized_key(value, default), default)


def normalize_length(value, default: str = "medium") -> str:
    return LENGTH_ALIASES.get(_normalized_key(value, default), default)


def resolve_identity_slug(slug: str, default: str = "") -> str:
    key = _normalized_key(slug, default)
    return IDENTITY_ALIASES.get(key, key)


def prompt_language_label(value, default: str = "danish") -> str:
    canonical = normalize_language(value, default=default)
    return PROMPT_LANGUAGE_LABELS.get(canonical, PROMPT_LANGUAGE_LABELS[default])


def normalize_session_cfg(session_cfg: dict | None) -> dict:
    if not session_cfg:
        return {}

    normalized = dict(session_cfg)
    for suffix in ("a", "b"):
        identity_key = f"identity_{suffix}"
        language_key = f"language_{suffix}"
        length_key = f"length_{suffix}"

        if identity_key in normalized:
            normalized[identity_key] = resolve_identity_slug(normalized.get(identity_key, ""))
        if language_key in normalized:
            normalized[language_key] = normalize_language(normalized.get(language_key))
        if length_key in normalized:
            normalized[length_key] = normalize_length(normalized.get(length_key))

    return normalized


def normalize_settings_for_ui(settings: dict) -> dict:
    """
    Keep today's UI values intact, but map stale identity slugs to currently
    shipped identity options so older projects still load into the dropdowns.
    """
    normalized = dict(settings)
    for suffix in ("a", "b"):
        key = f"identity_{suffix}"
        normalized[key] = resolve_identity_slug(normalized.get(key, ""))
    return normalized
