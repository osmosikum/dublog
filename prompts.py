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
    "short": "Svar kortfattet - maksimalt 3 saetninger.",
    "medium": "Svar i passende laengde - 4-6 saetninger.",
    "long": "Svar uddybende og detaljeret - 7-10 saetninger.",
}


def build_system_prompt(
    identity_content: str,
    memory: str,
    language: str = "dansk",
    length: str = "medium",
) -> str:
    parts = [identity_content]
    normalized_language = normalize_language(language)
    normalized_length = normalize_length(length)

    instructions: list[str] = []
    if normalized_language:
        instructions.append(f"Svar altid paa {prompt_language_label(normalized_language)}.")

    hint = _LENGTH_HINTS.get(normalized_length)
    if hint:
        instructions.append(hint)

    if instructions:
        parts.append("## Sproglige krav\n" + "\n".join(f"- {item}" for item in instructions))

    if memory:
        parts.append(f"## Hvad du husker\n{memory}")

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
            f"## Emne\n{topic}\n\n"
            f"## {other_name} sagde\n{other_response}\n\n"
            f"## Din opgave\n"
            f"Runde {round_num} af {total_rounds}. "
            f"Svar direkte og konkret paa det {other_name} sagde.\n"
            f"Slut dit svar med: [MEMORY]: <din vigtigste pointe fra denne runde>"
        )
    else:
        task = (
            f"## Emne\n{topic}\n\n"
            f"## Din opgave\n"
            f"Runde {round_num} af {total_rounds}. "
            f"Aabn diskussionen med dit perspektiv. Vaer praecis og konkret.\n"
            f"Slut dit svar med: [MEMORY]: <din vigtigste pointe fra denne runde>"
        )

    return messages + [{"role": "user", "content": task}]
