"""
Identities — load and list persona files from the identities/ folder.

File format (identities/{slug}.md):
    ---
    name: Skeptikeren
    language: dansk
    length: medium
    ---

    # Skeptikeren

    Identity body here...

Fields:
    name     — Display name shown in UI
    language — Default language for responses (e.g. "dansk", "engelsk")
    length   — Default response length: "kort" | "medium" | "lang"
"""

from pathlib import Path

_IDENTITIES_DIR = Path("identities")

_DEFAULTS = {
    "language": "dansk",
    "length": "medium",
}


def load_identity(slug: str) -> dict:
    """
    Load a single identity by slug (filename without .md).
    Returns dict with keys: slug, name, language, length, content.
    Falls back gracefully if file is missing.
    """
    path = _IDENTITIES_DIR / f"{slug}.md"
    name_fallback = slug.replace("-", " ").title()

    if not path.exists():
        return {
            "slug": slug,
            "name": name_fallback,
            **_DEFAULTS,
            "content": (
                f"# {name_fallback}\n\n"
                "Du er en agent i en diskussion. Bidrag aktivt med dit perspektiv.\n\n"
                "Tal altid i første person. Vær konsekvent.\n"
                "Slut dit svar med: [MEMORY]: <din vigtigste pointe fra denne runde>"
            ),
        }

    text = path.read_text(encoding="utf-8").strip()
    meta = {"slug": slug, "name": name_fallback, **_DEFAULTS}

    if text.startswith("---"):
        rest = text[3:]
        if "---" in rest:
            front, body = rest.split("---", 1)
            for line in front.strip().splitlines():
                line = line.strip()
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip()
            meta["content"] = body.strip()
        else:
            meta["content"] = text
    else:
        meta["content"] = text

    # Ensure name falls back to slug-derived if frontmatter had no name
    if "name" not in meta or not meta["name"]:
        meta["name"] = name_fallback

    return meta


def list_identities() -> list[dict]:
    """
    Return a sorted list of identity metadata dicts (no content body).
    Each entry: {slug, name, language, length}
    """
    if not _IDENTITIES_DIR.exists():
        return []
    result = []
    for p in sorted(_IDENTITIES_DIR.glob("*.md")):
        ident = load_identity(p.stem)
        result.append({
            "slug":     ident["slug"],
            "name":     ident["name"],
            "language": ident["language"],
            "length":   ident["length"],
        })
    return result
