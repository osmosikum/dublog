"""
Identities — load and list persona files from the identities/ folder.

Tracked structure:
    identities/
        template.md
        examples/*.md
        custom/.gitkeep

Runtime support:
    - repo-shipped examples in identities/examples/
    - local custom identities in identities/custom/ (gitignored)
    - legacy root-level identities in identities/ (except template/docs files)

Fields:
    name     — Display name shown in UI
    language — Default language for responses (e.g. "dansk", "engelsk")
    length   — Default response length: "kort" | "medium" | "lang"
"""

from pathlib import Path

_IDENTITIES_DIR = Path("identities")
_EXAMPLES_DIR = _IDENTITIES_DIR / "examples"
_CUSTOM_DIR = _IDENTITIES_DIR / "custom"
_SKIP_FILENAMES = {"template.md", "README.md", "AGENTS.md"}

_DEFAULTS = {
    "language": "dansk",
    "length": "medium",
}


def _identity_paths() -> dict[str, Path]:
    """
    Resolve available identity files by slug.

    Precedence:
        1. repo examples
        2. legacy root-level identities
        3. local custom identities

    Later entries win on slug collisions, so local custom files can override
    shipped examples without changing loader code.
    """
    paths: dict[str, Path] = {}

    if _EXAMPLES_DIR.exists():
        for path in sorted(_EXAMPLES_DIR.glob("*.md")):
            if path.name not in _SKIP_FILENAMES:
                paths[path.stem] = path

    if _IDENTITIES_DIR.exists():
        for path in sorted(_IDENTITIES_DIR.glob("*.md")):
            if path.name not in _SKIP_FILENAMES:
                paths[path.stem] = path

    if _CUSTOM_DIR.exists():
        for path in sorted(_CUSTOM_DIR.rglob("*.md")):
            if path.name not in _SKIP_FILENAMES:
                paths[path.stem] = path

    return paths


def load_identity(slug: str) -> dict:
    """
    Load a single identity by slug (filename without .md).
    Returns dict with keys: slug, name, language, length, content.
    Falls back gracefully if file is missing.
    """
    path = _identity_paths().get(slug)
    name_fallback = slug.replace("-", " ").title()

    if path is None or not path.exists():
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
    result = []
    for slug in sorted(_identity_paths()):
        ident = load_identity(slug)
        result.append({
            "slug":     ident["slug"],
            "name":     ident["name"],
            "language": ident["language"],
            "length":   ident["length"],
        })
    return result
