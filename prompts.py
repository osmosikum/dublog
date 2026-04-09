"""
Prompt builder.

build_system_prompt — combines identity body + language/length instructions + memory.
build_user_message  — builds the conversation turn as a messages list.

Prompt layer order (fixed):
  1. Identity       — who the agent is (re-injected every round)
  2. Instructions   — language + response length constraints
  3. Memory         — budget-capped recent entries
  4. Task           — what to do this round (appended as user message)
"""

_LENGTH_HINTS = {
    "kort":   "Svar kortfattet — maksimalt 3 sætninger.",
    "medium": "Svar i passende længde — 4-6 sætninger.",
    "lang":   "Svar uddybende og detaljeret — 7-10 sætninger.",
}


def build_system_prompt(
    identity_content: str,
    memory: str,
    language: str = "dansk",
    length: str = "medium",
) -> str:
    parts = [identity_content]

    instructions: list[str] = []
    if language:
        instructions.append(f"Svar altid på {language}.")
    hint = _LENGTH_HINTS.get(length)
    if hint:
        instructions.append(hint)
    if instructions:
        parts.append("## Sproglige krav\n" + "\n".join(f"- {i}" for i in instructions))

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
            f"Svar direkte og konkret på det {other_name} sagde.\n"
            f"Slut dit svar med: [MEMORY]: <din vigtigste pointe fra denne runde>"
        )
    else:
        task = (
            f"## Emne\n{topic}\n\n"
            f"## Din opgave\n"
            f"Runde {round_num} af {total_rounds}. "
            f"Åbn diskussionen med dit perspektiv. Vær præcis og konkret.\n"
            f"Slut dit svar med: [MEMORY]: <din vigtigste pointe fra denne runde>"
        )

    return messages + [{"role": "user", "content": task}]
