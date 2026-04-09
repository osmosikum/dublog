import json
import os
import queue
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

import requests as req_lib

os.chdir(Path(__file__).parent)

PORT = 7842

run_queue:  queue.Queue    = queue.Queue()
run_lock:   threading.Lock = threading.Lock()
stop_event: threading.Event = threading.Event()
is_running: bool = False


# ── Model discovery ───────────────────────────────────────────────────────────

def fetch_ollama_models() -> tuple[list[str], str]:
    try:
        r = req_lib.get("http://localhost:11434/api/tags", timeout=3)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])], ""
    except req_lib.exceptions.ConnectionError:
        return [], "Kan ikke forbinde til Ollama på port 11434 — kør 'ollama serve'"
    except Exception as e:
        return [], str(e)


def fetch_lmstudio_models() -> tuple[list[str], str]:
    try:
        r = req_lib.get("http://localhost:1234/v1/models", timeout=3)
        r.raise_for_status()
        return [m["id"] for m in r.json().get("data", [])], ""
    except req_lib.exceptions.ConnectionError:
        return [], "Kan ikke forbinde til LM Studio på port 1234"
    except Exception as e:
        return [], str(e)


def make_output_fn(q: queue.Queue):
    def fn(msg: str):
        for line in str(msg).split("\n"):
            q.put(line)
    return fn


# ── HTTP handler ──────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        parsed    = urlparse(self.path)
        path      = parsed.path
        self._qp  = parse_qs(parsed.query)

        routes = {
            "/":                     lambda: self._serve_file("ui/index.html", "text/html; charset=utf-8"),
            "/index.html":           lambda: self._serve_file("ui/index.html", "text/html; charset=utf-8"),
            "/api/models":           self._get_models,
            "/api/config":           self._get_config,
            "/api/stream":           self._stream,
            "/api/status":           self._get_status,
            "/api/projects":         self._get_projects,
            "/api/project/settings": self._get_project_settings,
            "/api/sessions":         self._get_sessions,
            "/api/session/log":      self._get_session_log,
            "/api/identities":       self._get_identities,
            "/api/memory/a":         lambda: self._get_memory("agent_a"),
            "/api/memory/b":         lambda: self._get_memory("agent_b"),
        }
        handler = routes.get(path)
        if handler:
            handler()
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        routes = {
            "/api/run":              self._start_run,
            "/api/stop":             self._stop_run,
            "/api/projects":         self._create_project,
            "/api/project/settings": self._save_project_settings,
            "/api/delete/project":   self._delete_project,
            "/api/delete/session":   self._delete_session,
        }
        handler = routes.get(path)
        if handler:
            handler()
        else:
            self.send_error(404)

    # ── GET endpoints ──

    def _serve_file(self, filepath: str, content_type: str):
        p = Path(filepath)
        if not p.exists():
            self.send_error(404)
            return
        data = p.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _get_models(self):
        ollama_models,   ollama_err   = fetch_ollama_models()
        lmstudio_models, lmstudio_err = fetch_lmstudio_models()
        self._json({
            "ollama":         ollama_models,
            "ollama_error":   ollama_err,
            "lmstudio":       lmstudio_models,
            "lmstudio_error": lmstudio_err,
        })

    def _get_config(self):
        import config
        self._json({
            "topic":   config.TOPIC,
            "rounds":  config.ROUNDS,
            "backend": config.BACKEND,
            "agent_a": config.AGENT_A,
            "agent_b": config.AGENT_B,
        })

    def _get_status(self):
        self._json({"running": is_running})

    def _get_projects(self):
        from projects import list_projects, ensure_default
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
        project    = self._qp.get("project",  ["default"])[0]
        session_id = self._qp.get("session",  [""])[0]
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

    def _stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        try:
            while True:
                try:
                    msg = run_queue.get(timeout=60)
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    continue
                if msg is None:
                    self.wfile.write(b"data: [DONE]\n\n")
                    self.wfile.flush()
                    break
                encoded = msg.replace("\\", "\\\\")
                self.wfile.write(f"data: {encoded}\n\n".encode("utf-8"))
                self.wfile.flush()
        except Exception:
            pass

    # ── POST endpoints ──

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _start_run(self):
        global is_running
        body = self._read_body()

        with run_lock:
            if is_running:
                self._json({"error": "En samtale kører allerede"})
                return
            is_running = True

        # Reset stop signal and clear leftover output
        stop_event.clear()
        while not run_queue.empty():
            try:
                run_queue.get_nowait()
            except queue.Empty:
                break

        session_cfg = {
            "topic":      body.get("topic",      ""),
            "rounds":     body.get("rounds",     6),
            "name_a":     body.get("name_a",     "Agent A"),
            "model_a":    body.get("model_a",    ""),
            "identity_a": body.get("identity_a", "skeptikeren"),
            "language_a": body.get("language_a", "dansk"),
            "length_a":   body.get("length_a",   "medium"),
            "name_b":     body.get("name_b",     "Agent B"),
            "model_b":    body.get("model_b",    ""),
            "identity_b": body.get("identity_b", "optimisten"),
            "language_b": body.get("language_b", "dansk"),
            "length_b":   body.get("length_b",   "medium"),
        }
        project = body.get("project", "default")

        import config as cfg
        cfg.BACKEND = body.get("backend", cfg.BACKEND)

        from projects import save_settings
        save_settings(project, {**session_cfg, "backend": body.get("backend", cfg.BACKEND)})

        def run():
            global is_running
            try:
                import main
                main.run_conversation(
                    output_fn=make_output_fn(run_queue),
                    project=project,
                    session_cfg=session_cfg,
                    stop_event=stop_event,
                )
            except Exception as e:
                run_queue.put(f"[FEJL] {e}")
            finally:
                run_queue.put(None)
                is_running = False

        threading.Thread(target=run, daemon=True).start()
        self._json({"status": "started"})

    def _stop_run(self):
        stop_event.set()
        self._json({"status": "stopping"})

    def _create_project(self):
        body = self._read_body()
        name = body.get("name", "").strip()
        if not name:
            self._json({"error": "Navn må ikke være tomt"})
            return
        from projects import create_project
        slug = create_project(name)
        self._json({"status": "created", "slug": slug})

    def _save_project_settings(self):
        body = self._read_body()
        project  = body.get("project",  "default")
        settings = body.get("settings", {})
        from projects import save_settings
        save_settings(project, settings)
        self._json({"status": "saved"})

    def _delete_project(self):
        body    = self._read_body()
        project = body.get("project", "")
        if not project or project == "default":
            self._json({"error": "Kan ikke slette default-projektet"})
            return
        from projects import delete_project
        delete_project(project)
        self._json({"status": "deleted"})

    def _delete_session(self):
        body       = self._read_body()
        project    = body.get("project",  "")
        session_id = body.get("session",  "")
        if not project or not session_id:
            self._json({"error": "Mangler project eller session"})
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
    print(f"Multi-Agent Sandbox UI → http://localhost:{PORT}")
    print("Tryk Ctrl+C for at stoppe.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stoppet.")


if __name__ == "__main__":
    main()
