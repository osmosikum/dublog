import json
import os
import queue
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs, urlparse

import requests as req_lib

from sessions import session_manager

os.chdir(Path(__file__).parent)

PORT = 7842


def fetch_ollama_models() -> tuple[list[str], str]:
    try:
        response = req_lib.get("http://localhost:11434/api/tags", timeout=3)
        response.raise_for_status()
        return [model["name"] for model in response.json().get("models", [])], ""
    except req_lib.exceptions.ConnectionError:
        return [], "Could not connect to Ollama on port 11434 - run 'ollama serve'"
    except Exception as exc:
        return [], str(exc)


def fetch_lmstudio_models() -> tuple[list[str], str]:
    try:
        response = req_lib.get("http://localhost:1234/v1/models", timeout=3)
        response.raise_for_status()
        return [model["id"] for model in response.json().get("data", [])], ""
    except req_lib.exceptions.ConnectionError:
        return [], "Could not connect to LM Studio on port 1234"
    except Exception as exc:
        return [], str(exc)


def make_output_fn(out_queue: queue.Queue):
    def fn(message: str):
        for line in str(message).split("\n"):
            out_queue.put(line)
    return fn


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        self._qp = parse_qs(parsed.query)

        routes = {
            "/": lambda: self._serve_file("ui/index.html", "text/html; charset=utf-8"),
            "/index.html": lambda: self._serve_file("ui/index.html", "text/html; charset=utf-8"),
            "/api/models": self._get_models,
            "/api/config": self._get_config,
            "/api/stream": self._stream,
            "/api/status": self._get_status,
            "/api/projects": self._get_projects,
            "/api/project/settings": self._get_project_settings,
            "/api/sessions": self._get_sessions,
            "/api/session/log": self._get_session_log,
            "/api/identities": self._get_identities,
            "/api/memory/a": lambda: self._get_memory("agent_a"),
            "/api/memory/b": lambda: self._get_memory("agent_b"),
            "/api/telemetry": self._get_telemetry,
        }
        handler = routes.get(path)
        if handler:
            handler()
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        routes = {
            "/api/run": self._start_run,
            "/api/stop": self._stop_run,
            "/api/projects": self._create_project,
            "/api/project/settings": self._save_project_settings,
            "/api/delete/project": self._delete_project,
            "/api/delete/session": self._delete_session,
        }
        handler = routes.get(path)
        if handler:
            handler()
        else:
            self.send_error(404)

    def _serve_file(self, filepath: str, content_type: str):
        path = Path(filepath)
        if not path.exists():
            self.send_error(404)
            return

        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _get_models(self):
        ollama_models, ollama_err = fetch_ollama_models()
        lmstudio_models, lmstudio_err = fetch_lmstudio_models()
        self._json({
            "ollama": ollama_models,
            "ollama_error": ollama_err,
            "lmstudio": lmstudio_models,
            "lmstudio_error": lmstudio_err,
        })

    def _get_config(self):
        import config

        self._json({
            "topic": config.TOPIC,
            "rounds": config.ROUNDS,
            "backend": config.BACKEND,
            "agent_a": config.AGENT_A,
            "agent_b": config.AGENT_B,
        })

    def _get_status(self):
        self._json({"running": session_manager.is_running()})

    def _get_projects(self):
        from projects import ensure_default, list_projects

        ensure_default()
        self._json(list_projects())

    def _get_project_settings(self):
        project = self._qp.get("project", ["default"])[0]
        from projects import load_settings

        self._json(load_settings(project))

    def _get_sessions(self):
        project = self._qp.get("project", ["default"])[0]
        from projects import list_sessions

        self._json(list_sessions(project))

    def _get_session_log(self):
        project = self._qp.get("project", ["default"])[0]
        session_id = self._qp.get("session", [""])[0]
        from projects import get_session_log

        text = get_session_log(project, session_id)
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _get_identities(self):
        from identities import list_identities

        self._json(list_identities())

    def _get_memory(self, agent: str):
        project = self._qp.get("project", ["default"])[0]
        path = Path("projects") / project / agent / "memory.md"
        text = path.read_text(encoding="utf-8").strip() if path.exists() else ""
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _get_telemetry(self):
        project    = self._qp.get("project", ["default"])[0]
        session_id = self._qp.get("session", [""])[0]
        if not session_id:
            self._json([])
            return
        from telemetry import load_telemetry
        session_dir = Path("projects") / project / "sessions" / session_id
        self._json(load_telemetry(session_dir))

    def _stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        session = session_manager.current()
        if session is None:
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()
            return
        try:
            while True:
                try:
                    message = session.queue.get(timeout=60)
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    continue

                if message is None:
                    self.wfile.write(b"data: [DONE]\n\n")
                    self.wfile.flush()
                    break

                encoded = message.replace("\\", "\\\\")
                self.wfile.write(f"data: {encoded}\n\n".encode("utf-8"))
                self.wfile.flush()
        except Exception:
            pass

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _start_run(self):
        if session_manager.is_running():
            self._json({"error": "A conversation is already running"})
            return

        body = self._read_body()

        session_cfg = {
            "topic": body.get("topic", ""),
            "rounds": body.get("rounds", 6),
            "name_a": body.get("name_a", "Agent A"),
            "model_a": body.get("model_a", ""),
            "identity_a": body.get("identity_a", "ent_kasper"),
            "language_a": body.get("language_a", "danish"),
            "length_a": body.get("length_a", "medium"),
            "name_b": body.get("name_b", "Agent B"),
            "model_b": body.get("model_b", ""),
            "identity_b": body.get("identity_b", "ent_leon"),
            "language_b": body.get("language_b", "danish"),
            "length_b": body.get("length_b", "medium"),
        }
        project = body.get("project", "default")

        import config as cfg
        from projects import create_session, save_settings

        cfg.BACKEND = body.get("backend", cfg.BACKEND)
        save_settings(project, {**session_cfg, "backend": body.get("backend", cfg.BACKEND)})

        session_id, session_dir = create_session(project)
        session = session_manager.start(session_id, session_dir)

        def run():
            try:
                import main

                main.run_conversation(
                    output_fn=make_output_fn(session.queue),
                    project=project,
                    session_cfg=session_cfg,
                    stop_event=session.stop_event,
                    session_id=session_id,
                    session_dir=session_dir,
                )
            except Exception as exc:
                session.queue.put(f"[ERROR] {exc}")
                session_manager.finish(error=exc)
            else:
                session_manager.finish()
            finally:
                session.queue.put(None)

        threading.Thread(target=run, daemon=True).start()
        self._json({"status": "started", "session_id": session_id})

    def _stop_run(self):
        session = session_manager.current()
        if session is not None:
            session.stop_event.set()
        self._json({"status": "stopping"})

    def _create_project(self):
        body = self._read_body()
        name = body.get("name", "").strip()
        if not name:
            self._json({"error": "Name must not be empty"})
            return

        from projects import create_project

        slug = create_project(name)
        self._json({"status": "created", "slug": slug})

    def _save_project_settings(self):
        body = self._read_body()
        project = body.get("project", "default")
        settings = body.get("settings", {})
        from projects import save_settings

        save_settings(project, settings)
        self._json({"status": "saved"})

    def _delete_project(self):
        body = self._read_body()
        project = body.get("project", "")
        if not project or project == "default":
            self._json({"error": "Cannot delete the default project"})
            return

        from projects import delete_project

        delete_project(project)
        self._json({"status": "deleted"})

    def _delete_session(self):
        body = self._read_body()
        project = body.get("project", "")
        session_id = body.get("session", "")
        if not project or not session_id:
            self._json({"error": "Missing project or session"})
            return

        from projects import delete_session

        delete_session(project, session_id)
        self._json({"status": "deleted"})

    def _json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


def main():
    from projects import ensure_default

    ensure_default()
    server = ThreadedHTTPServer(("localhost", PORT), Handler)
    print(f"Multi-Agent Sandbox UI -> http://localhost:{PORT}")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
