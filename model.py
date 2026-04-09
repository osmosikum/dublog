import os
import requests


def call_model(model: str, system_prompt: str, messages: list[dict]) -> str:
    from config import BACKEND
    if BACKEND == "ollama":
        return _call_ollama(model, system_prompt, messages)
    elif BACKEND == "lmstudio":
        return _call_lmstudio(model, system_prompt, messages)
    elif BACKEND == "claude":
        return _call_claude(model, system_prompt, messages)
    else:
        raise ValueError(f"Ukendt backend: {BACKEND}")


def _call_ollama(model, system_prompt, messages):
    from config import OLLAMA_URL
    r = requests.post(OLLAMA_URL, json={
        "model": model,
        "stream": False,
        "messages": [{"role": "system", "content": system_prompt}] + messages
    }, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


def _call_lmstudio(model, system_prompt, messages):
    from config import LMSTUDIO_URL
    r = requests.post(LMSTUDIO_URL, json={
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}] + messages
    }, timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def _call_claude(model, system_prompt, messages):
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=messages
    )
    return response.content[0].text.strip()
