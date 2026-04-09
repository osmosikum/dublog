"""
Projects — create, list and manage project directories.

Structure:
    projects/{name}/
        agent_a/memory.md
        agent_b/memory.md
        shared/conversation.md
        shared/run_config.md
        settings.json

settings.json holds all per-project UI config so sessions are fully
restorable when switching between projects.
"""

import json
import re
from pathlib import Path

PROJECTS_DIR = Path("projects")

# These are the defaults written to every new project's settings.json.
# They mirror the values in config.py so CLI and UI stay consistent.
DEFAULT_SETTINGS: dict = {
    "topic":      "Er AI en trussel eller en mulighed for samfundet?",
    "rounds":     6,
    "backend":    "ollama",
    "name_a":     "Skeptikeren",
    "model_a":    "gemma3:4b",
    "identity_a": "skeptikeren",
    "language_a": "dansk",
    "length_a":   "medium",
    "name_b":     "Optimisten",
    "model_b":    "gemma3:4b",
    "identity_b": "optimisten",
    "language_b": "dansk",
    "length_b":   "medium",
}


# ── Naming ────────────────────────────────────────────────────────────────────

def sanitize_name(name: str) -> str:
    """Convert a user-supplied project name to a safe directory name."""
    name = name.strip().lower()
    # Allow letters (including æøå), digits and hyphens
    name = re.sub(r"[^\w\-æøåÆØÅ]", "-", name, flags=re.UNICODE)
    name = re.sub(r"-+", "-", name)
    return name.strip("-") or "projekt"


# ── CRUD ──────────────────────────────────────────────────────────────────────

def list_projects() -> list[str]:
    """Return sorted list of existing project names."""
    if not PROJECTS_DIR.exists():
        return []
    return sorted(
        d.name for d in PROJECTS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def load_settings(project: str) -> dict:
    """
    Load settings for a project.
    Missing keys are filled in from DEFAULT_SETTINGS so the schema
    is always complete even for older projects.
    """
    path = PROJECTS_DIR / project / "settings.json"
    if not path.exists():
        return dict(DEFAULT_SETTINGS)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {**DEFAULT_SETTINGS, **data}
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(project: str, settings: dict) -> None:
    """Persist settings to projects/{project}/settings.json."""
    path = PROJECTS_DIR / project / "settings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    merged = {**DEFAULT_SETTINGS, **settings}
    path.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def create_project(name: str) -> str:
    """
    Create a new project directory with the default structure.
    Returns the sanitized project slug.
    """
    slug = sanitize_name(name)
    project_dir = PROJECTS_DIR / slug

    (project_dir / "agent_a").mkdir(parents=True, exist_ok=True)
    (project_dir / "agent_b").mkdir(parents=True, exist_ok=True)
    (project_dir / "shared").mkdir(parents=True, exist_ok=True)

    for subdir in ("agent_a", "agent_b"):
        mem = project_dir / subdir / "memory.md"
        if not mem.exists():
            mem.write_text("", encoding="utf-8")

    if not (project_dir / "settings.json").exists():
        save_settings(slug, DEFAULT_SETTINGS)

    return slug


def ensure_default() -> None:
    """Boot-time guard — ensures the 'default' project always exists."""
    if not (PROJECTS_DIR / "default").exists():
        create_project("default")
