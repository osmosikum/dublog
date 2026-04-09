"""
SessionManager — runtime session lifecycle for the web-run flow.

A Session holds the in-memory state for one active conversation run:
    - output queue read by the SSE stream
    - stop event sent by the stop endpoint
    - state: "running" | "done" | "error"
    - session_id and session_dir from projects.py

The module exposes a single process-level SessionManager instance
(session_manager) that app.py imports and uses directly.

CLI runs (main.py called standalone) bypass the manager entirely and
create their own session via projects.create_session.
"""

import queue
import threading
from pathlib import Path


class Session:
    def __init__(self, session_id: str, session_dir: Path) -> None:
        self.session_id = session_id
        self.session_dir = session_dir
        self.queue: queue.Queue = queue.Queue()
        self.stop_event: threading.Event = threading.Event()
        self.state: str = "running"  # "running" | "done" | "error"


class SessionManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._current: Session | None = None

    def start(self, session_id: str, session_dir: Path) -> Session:
        """Create and register a new running session."""
        with self._lock:
            session = Session(session_id, session_dir)
            self._current = session
            return session

    def current(self) -> Session | None:
        """Return the most recent session, or None if none has started."""
        return self._current

    def is_running(self) -> bool:
        """True only while a session is in the 'running' state."""
        s = self._current
        return s is not None and s.state == "running"

    def finish(self, error: Exception | None = None) -> None:
        """Mark the current session done or error."""
        s = self._current
        if s is not None:
            s.state = "error" if error else "done"


session_manager = SessionManager()
