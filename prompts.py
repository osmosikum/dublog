"""
Prompt builder.

build_system_prompt combines identity body, language/length instructions,
and recent memory.
build_user_message builds the conversation turn as a messages list.

Prompt layer order (fixed):
  1. Identity
  2. Instructions
  3. Memory
  4. Task
"""

from normalization import normalize_language, normalize_length, prompt_language_label

_LENGTH_HINTS = {
    "short": "Respond briefly - maximum 3 sentences.",
    "medium": "Respond at a reasonable length - 4-6 sentences.",
    "long": "Respond in depth and detail - 7-10 sentences.",
}


def build_system_prompt(
    identity_content: str,
    memory: str,
    language: str = "danish",
    length: str = "medium",
) -> str:
    parts = [identity_content]
    normalized_language = normalize_language(language)
    normalized_length = normalize_length(length)

    instructions: list[str] = []
    if normalized_language:
        instructions.append(f"Always respond in {prompt_language_label(normalized_language)}.")

    hint = _LENGTH_HINTS.get(normalized_length)
    if hint:
        instructions.append(hint)

    if instructions:
        parts.append("## Language requirements\n" + "\n".join(f"- {item}" for item in instructions))

    if memory:
        parts.append(f"## What you remember\n{memory}")

    return "\n\n".join(parts)


def build_user_message(
    topic: str,
    other_name: str,
    other_response: str,
    history: list[dict],
    round_num: int,
    total_rounds: int,
    max_turns: int,
) -> list[dict]:
    messages = history[-(max_turns * 2):] if history else []

    if other_response:
        task = (
            f"## Topic\n{topic}\n\n"
            f"## {other_name} said\n{other_response}\n\n"
            f"## Your task\n"
            f"Round {round_num} of {total_rounds}. "
            f"Respond directly and concretely to what {other_name} said.\n"
            f"End your answer with: [MEMORY]: <your most important point from this round>"
        )
    else:
        task = (
            f"## Topic\n{topic}\n\n"
            f"## Your task\n"
            f"Round {round_num} of {total_rounds}. "
            f"Open the discussion with your perspective. Be precise and concrete.\n"
            f"End your answer with: [MEMORY]: <your most important point from this round>"
        )

    return messages + [{"role": "user", "content": task}]
