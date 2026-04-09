import config
import threading
from datetime import datetime
from pathlib import Path

from identities import load_identity
from memory import (
    append_memory,
    check_convergence,
    extract_memory_tag,
    load_memory,
    log_conversation,
)
from model import call_model
from normalization import normalize_session_cfg
from projects import create_session, ensure_default
from prompts import build_system_prompt, build_user_message


def setup_dirs(project_dir: Path, session_dir: Path, topic: str, project: str, session_id: str) -> None:
    # Project-level memory persists across sessions.
    (project_dir / "agent_a").mkdir(parents=True, exist_ok=True)
    (project_dir / "agent_b").mkdir(parents=True, exist_ok=True)
    for subdir in ("agent_a", "agent_b"):
        mem = project_dir / subdir / "memory.md"
        if not mem.exists():
            mem.write_text("", encoding="utf-8")

    # Session-level files are fresh per run.
    session_dir.mkdir(parents=True, exist_ok=True)

    conv = session_dir / "conversation.md"
    if not conv.exists():
        conv.write_text(
            f"# Conversation\n\n"
            f"**Topic:** {topic}\n"
            f"**Project:** {project}\n"
            f"**Session:** {session_id}\n"
            f"**Started:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    run_cfg = session_dir / "run_config.md"
    with open(run_cfg, "w", encoding="utf-8") as f:
        f.write("# Run Config\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Project:** {project}\n")
        f.write(f"**Session:** {session_id}\n")
        f.write(f"**Topic:** {topic}\n")


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


def run_conversation(
    output_fn=print,
    project: str = "default",
    session_cfg: dict | None = None,
    stop_event: threading.Event | None = None,
):
    """
    Run a full conversation, creating a new session under the project.

    session_cfg keys (all optional - fall back to config.py defaults):
        topic, rounds,
        name_a, model_a, identity_a, language_a, length_a,
        name_b, model_b, identity_b, language_b, length_b
    """
    if session_cfg is None:
        session_cfg = {}

    runtime_cfg = normalize_session_cfg({
        "topic": session_cfg.get("topic", config.TOPIC),
        "rounds": session_cfg.get("rounds", config.ROUNDS),
        "name_a": session_cfg.get("name_a", config.AGENT_A["name"]),
        "model_a": session_cfg.get("model_a", config.AGENT_A["model"]),
        "identity_a": session_cfg.get("identity_a", config.IDENTITY_A),
        "language_a": session_cfg.get("language_a", config.LANGUAGE_A),
        "length_a": session_cfg.get("length_a", config.LENGTH_A),
        "name_b": session_cfg.get("name_b", config.AGENT_B["name"]),
        "model_b": session_cfg.get("model_b", config.AGENT_B["model"]),
        "identity_b": session_cfg.get("identity_b", config.IDENTITY_B),
        "language_b": session_cfg.get("language_b", config.LANGUAGE_B),
        "length_b": session_cfg.get("length_b", config.LENGTH_B),
    })

    topic = runtime_cfg["topic"]
    rounds = int(runtime_cfg["rounds"])
    name_a = runtime_cfg["name_a"]
    model_a = runtime_cfg["model_a"]
    identity_a = runtime_cfg["identity_a"]
    language_a = runtime_cfg["language_a"]
    length_a = runtime_cfg["length_a"]
    name_b = runtime_cfg["name_b"]
    model_b = runtime_cfg["model_b"]
    identity_b = runtime_cfg["identity_b"]
    language_b = runtime_cfg["language_b"]
    length_b = runtime_cfg["length_b"]

    project_dir = Path("projects") / project
    session_id, session_dir = create_session(project)

    agent_a_dir = project_dir / "agent_a"
    agent_b_dir = project_dir / "agent_b"

    output_fn("\n>>> Multi-Agent Sandbox starting")
    output_fn(f">>> Project:  {project}  |  Session: {session_id}")
    output_fn(f">>> Topic:    {topic}")
    output_fn(f">>> Rounds:   {rounds}")
    output_fn(f">>> {name_a} [{model_a}]  vs  {name_b} [{model_b}]\n")

    setup_dirs(project_dir, session_dir, topic, project, session_id)

    history_a: list[dict] = []
    history_b: list[dict] = []
    last_a = ""
    last_b = ""
    streak = 0

    for round_num in range(1, rounds + 1):
        if stop_event and stop_event.is_set():
            output_fn(f"\n>>> Conversation stopped by user after round {round_num - 1}.")
            break

        output_fn(f"\n>>> Round {round_num}/{rounds} starting...")

        response_a = run_agent(
            agent_a_dir,
            model_a,
            name_b,
            last_b,
            history_a,
            round_num,
            topic,
            rounds,
            identity_a,
            language_a,
            length_a,
        )
        output_fn(f"\n{'=' * 60}")
        output_fn(f"  Round {round_num} - {name_a}")
        output_fn(f"{'=' * 60}")
        output_fn(response_a)
        log_conversation(name_a, response_a, round_num, session_dir)

        history_a.append({"role": "assistant", "content": response_a})
        history_b.append({"role": "user", "content": f"{name_a} said: {response_a}"})
        last_a = response_a

        if stop_event and stop_event.is_set():
            output_fn("\n>>> Conversation stopped by user.")
            break

        response_b = run_agent(
            agent_b_dir,
            model_b,
            name_a,
            last_a,
            history_b,
            round_num,
            topic,
            rounds,
            identity_b,
            language_b,
            length_b,
        )
        output_fn(f"\n{'=' * 60}")
        output_fn(f"  Round {round_num} - {name_b}")
        output_fn(f"{'=' * 60}")
        output_fn(response_b)
        log_conversation(name_b, response_b, round_num, session_dir)

        history_b.append({"role": "assistant", "content": response_b})
        history_a.append({"role": "user", "content": f"{name_b} said: {response_b}"})
        last_b = response_b

        if config.CONVERGENCE_CHECK:
            mem_a = load_memory(agent_a_dir, config.MAX_MEMORY_LINES)
            mem_b = load_memory(agent_b_dir, config.MAX_MEMORY_LINES)
            if check_convergence(mem_a, mem_b):
                streak += 1
                output_fn(f"\n>>> [Convergence streak: {streak}/{config.CONVERGENCE_ROUNDS}]")
                if streak >= config.CONVERGENCE_ROUNDS:
                    output_fn(f"\n>>> Convergence reached after round {round_num} - stopping early.")
                    break
            else:
                streak = 0

    output_fn(f"\n{'=' * 60}")
    output_fn(f"  Conversation finished  |  Session: {session_id}")
    output_fn(f"{'=' * 60}\n")
    output_fn(f"__SESSION_ID__:{session_id}")


def main():
    ensure_default()
    run_conversation(project="default")


if __name__ == "__main__":
    main()
