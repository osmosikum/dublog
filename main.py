import config
import threading
from pathlib import Path
from datetime import datetime

from model import call_model
from memory import (
    load_memory, extract_memory_tag, append_memory,
    check_convergence, log_conversation,
)
from prompts import build_system_prompt, build_user_message
from identities import load_identity
from projects import ensure_default, create_session


# ── Directory setup ───────────────────────────────────────────────────────────

def setup_dirs(project_dir: Path, session_dir: Path, topic: str, project: str, session_id: str) -> None:
    # Project-level memory (persists across sessions)
    (project_dir / "agent_a").mkdir(parents=True, exist_ok=True)
    (project_dir / "agent_b").mkdir(parents=True, exist_ok=True)
    for subdir in ("agent_a", "agent_b"):
        mem = project_dir / subdir / "memory.md"
        if not mem.exists():
            mem.write_text("", encoding="utf-8")

    # Session-level log (fresh per run)
    session_dir.mkdir(parents=True, exist_ok=True)

    conv = session_dir / "conversation.md"
    if not conv.exists():
        conv.write_text(
            f"# Samtale\n\n"
            f"**Emne:** {topic}\n"
            f"**Projekt:** {project}\n"
            f"**Session:** {session_id}\n"
            f"**Startet:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    run_cfg = session_dir / "run_config.md"
    with open(run_cfg, "w", encoding="utf-8") as f:
        f.write("# Run Config\n\n")
        f.write(f"**Dato:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Projekt:** {project}\n")
        f.write(f"**Session:** {session_id}\n")
        f.write(f"**Emne:** {topic}\n")


# ── Single agent turn ─────────────────────────────────────────────────────────

def run_agent(
    agent_dir: Path,
    model: str,
    other_name: str,
    other_response: str,
    history: list[dict],
    round_num: int,
    topic: str,
    total_rounds: int,
    identity_slug: str,
    language: str,
    length: str,
) -> str:
    ident = load_identity(identity_slug)
    memory = load_memory(agent_dir, config.MAX_MEMORY_LINES)
    system_prompt = build_system_prompt(ident["content"], memory, language, length)
    messages = build_user_message(
        topic=topic,
        other_name=other_name,
        other_response=other_response,
        history=history,
        round_num=round_num,
        total_rounds=total_rounds,
        max_turns=config.MAX_HISTORY_TURNS,
    )
    response = call_model(model, system_prompt, messages)
    memory_entry = extract_memory_tag(response)
    if memory_entry:
        append_memory(agent_dir, memory_entry)
    clean = response.split("[MEMORY]:")[0].strip()
    return clean if clean else response


# ── Orchestrator ──────────────────────────────────────────────────────────────

def run_conversation(
    output_fn=print,
    project: str = "default",
    session_cfg: dict | None = None,
    stop_event: threading.Event | None = None,
):
    """
    Run a full conversation, creating a new session under the project.

    session_cfg keys (all optional — fall back to config.py defaults):
        topic, rounds,
        name_a, model_a, identity_a, language_a, length_a,
        name_b, model_b, identity_b, language_b, length_b
    """
    if session_cfg is None:
        session_cfg = {}

    topic      = session_cfg.get("topic",      config.TOPIC)
    rounds     = int(session_cfg.get("rounds", config.ROUNDS))
    name_a     = session_cfg.get("name_a",     config.AGENT_A["name"])
    model_a    = session_cfg.get("model_a",    config.AGENT_A["model"])
    identity_a = session_cfg.get("identity_a", config.IDENTITY_A)
    language_a = session_cfg.get("language_a", config.LANGUAGE_A)
    length_a   = session_cfg.get("length_a",   config.LENGTH_A)
    name_b     = session_cfg.get("name_b",     config.AGENT_B["name"])
    model_b    = session_cfg.get("model_b",    config.AGENT_B["model"])
    identity_b = session_cfg.get("identity_b", config.IDENTITY_B)
    language_b = session_cfg.get("language_b", config.LANGUAGE_B)
    length_b   = session_cfg.get("length_b",   config.LENGTH_B)

    project_dir = Path("projects") / project
    session_id, session_dir = create_session(project)

    agent_a_dir = project_dir / "agent_a"
    agent_b_dir = project_dir / "agent_b"

    output_fn(f"\n>>> Multi-Agent Sandbox starter")
    output_fn(f">>> Projekt:  {project}  |  Session: {session_id}")
    output_fn(f">>> Emne:     {topic}")
    output_fn(f">>> Runder:   {rounds}")
    output_fn(f">>> {name_a} [{model_a}]  vs  {name_b} [{model_b}]\n")

    setup_dirs(project_dir, session_dir, topic, project, session_id)

    history_a: list[dict] = []
    history_b: list[dict] = []
    last_a = ""
    last_b = ""
    streak = 0

    for round_num in range(1, rounds + 1):
        # Check for stop signal before starting each round
        if stop_event and stop_event.is_set():
            output_fn(f"\n>>> Samtale stoppet af bruger efter runde {round_num - 1}.")
            break

        output_fn(f"\n>>> Runde {round_num}/{rounds} begynder...")

        # ── Agent A ──
        response_a = run_agent(
            agent_a_dir, model_a, name_b, last_b,
            history_a, round_num, topic, rounds,
            identity_a, language_a, length_a,
        )
        output_fn(f"\n{'='*60}")
        output_fn(f"  Runde {round_num} — {name_a}")
        output_fn(f"{'='*60}")
        output_fn(response_a)
        log_conversation(name_a, response_a, round_num, session_dir)

        history_a.append({"role": "assistant", "content": response_a})
        history_b.append({"role": "user",      "content": f"{name_a} sagde: {response_a}"})
        last_a = response_a

        # Check again between agents
        if stop_event and stop_event.is_set():
            output_fn(f"\n>>> Samtale stoppet af bruger.")
            break

        # ── Agent B ──
        response_b = run_agent(
            agent_b_dir, model_b, name_a, last_a,
            history_b, round_num, topic, rounds,
            identity_b, language_b, length_b,
        )
        output_fn(f"\n{'='*60}")
        output_fn(f"  Runde {round_num} — {name_b}")
        output_fn(f"{'='*60}")
        output_fn(response_b)
        log_conversation(name_b, response_b, round_num, session_dir)

        history_b.append({"role": "assistant", "content": response_b})
        history_a.append({"role": "user",      "content": f"{name_b} sagde: {response_b}"})
        last_b = response_b

        # ── Convergence check ──
        if config.CONVERGENCE_CHECK:
            mem_a = load_memory(agent_a_dir, config.MAX_MEMORY_LINES)
            mem_b = load_memory(agent_b_dir, config.MAX_MEMORY_LINES)
            if check_convergence(mem_a, mem_b):
                streak += 1
                output_fn(f"\n>>> [Konvergens streak: {streak}/{config.CONVERGENCE_ROUNDS}]")
                if streak >= config.CONVERGENCE_ROUNDS:
                    output_fn(f"\n>>> Konvergens nået efter runde {round_num} — stopper tidligt.")
                    break
            else:
                streak = 0

    output_fn(f"\n{'='*60}")
    output_fn(f"  Samtale afsluttet  |  Session: {session_id}")
    output_fn(f"{'='*60}\n")
    # Send session_id back so UI can update the session list
    output_fn(f"__SESSION_ID__:{session_id}")


# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    ensure_default()
    run_conversation(project="default")


if __name__ == "__main__":
    main()
