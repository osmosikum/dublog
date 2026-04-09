"""
Projects — create, list and manage project directories and sessions.

Disk layout:
    projects/{project}/
        settings.json               # UI config, persisted per project
        agent_a/memory.md           # project-level memory (shared across sessions)
        agent_b/memory.md           # project-level memory (shared across sessions)
        sessions/
            {session_id}/           # one dir per run (YYYYMMDD-HHMMSS)
                conversation.md     # chat log for this session
                run_config.md       # what was configured for this run

Projects hold shared memory. Sessions hold individual chat logs.
Switching sessions keeps memory; switching projects resets both.
"""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

PROJECTS_DIR = Path("projects")

DEFAULT_SETTINGS: dict = {
    "topic":      "Er AI en trussel eller en mulighed for samfundet?",
    "rounds":     6,
    "backend":    "ollama",
    "name_a":     "Agent A",
    "model_a":    "",
    "identity_a": "ent_viktor",
    "language_a": "dansk",
    "length_a":   "medium",
    "name_b":     "Agent B",
    "model_b":    "",
    "identity_b": "ent_maya",
    "language_b": "dansk",
    "length_b":   "medium",
}


# ── Naming ────────────────────────────────────────────────────────────────────

def sanitize_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^\w\-æøåÆØÅ]", "-", name, flags=re.UNICODE)
    name = re.sub(r"-+", "-", name)
    return name.strip("-") or "projekt"


# ── Projects ──────────────────────────────────────────────────────────────────

def list_projects() -> list[str]:
    if not PROJECTS_DIR.exists():
        return []
    return sorted(
        d.name for d in PROJECTS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def load_settings(project: str) -> dict:
    path = PROJECTS_DIR / project / "settings.json"
    if not path.exists():
        return dict(DEFAULT_SETTINGS)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {**DEFAULT_SETTINGS, **data}
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(project: str, settings: dict) -> None:
    path = PROJECTS_DIR / project / "settings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    merged = {**DEFAULT_SETTINGS, **settings}
    path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")


def create_project(name: str) -> str:
    slug = sanitize_name(name)
    project_dir = PROJECTS_DIR / slug
    (project_dir / "agent_a").mkdir(parents=True, exist_ok=True)
    (project_dir / "agent_b").mkdir(parents=True, exist_ok=True)
    (project_dir / "sessions").mkdir(parents=True, exist_ok=True)
    for subdir in ("agent_a", "agent_b"):
        mem = project_dir / subdir / "memory.md"
        if not mem.exists():
            mem.write_text("", encoding="utf-8")
    if not (project_dir / "settings.json").exists():
        save_settings(slug, DEFAULT_SETTINGS)
    return slug


def delete_project(project: str) -> None:
    project_dir = PROJECTS_DIR / project
    if project_dir.exists():
        shutil.rmtree(project_dir)


def ensure_default() -> None:
    if not (PROJECTS_DIR / "default").exists():
        create_project("default")


# ── Sessions ──────────────────────────────────────────────────────────────────

def new_session_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def list_sessions(project: str) -> list[str]:
    sessions_dir = PROJECTS_DIR / project / "sessions"
    if not sessions_dir.exists():
        return []
    return sorted(
        (d.name for d in sessions_dir.iterdir() if d.is_dir()),
        reverse=True  # newest first
    )


def create_session(project: str, session_id: str | None = None) -> tuple[str, Path]:
    if session_id is None:
        session_id = new_session_id()
    session_dir = PROJECTS_DIR / project / "sessions" / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_id, session_dir


def delete_session(project: str, session_id: str) -> None:
    session_dir = PROJECTS_DIR / project / "sessions" / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)


def get_session_log(project: str, session_id: str) -> str:
    path = PROJECTS_DIR / project / "sessions" / session_id / "conversation.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
