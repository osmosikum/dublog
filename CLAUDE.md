# CLAUDE.md - Arbejdskontrakt for Multi-Agent Sandbox

Denne fil er den operative guide for Claude Code i dette repo.
Den skal afspejle den nuvaerende sandhed og den naermeste retning, uden at laase projektet fast i arkitektur der endnu ikke er bygget.

## Formaal

- holde kode, docs og changelog i sync
- skelne mellem nuvaerende struktur, aktivt arbejde og senere ideer
- gore det tydeligt hvad der er implementeret nu, og hvad der kun er planlagt

## Nuværende sandhed

- Projektet er en lokal multi-agent sandbox i Python med stdlib plus `requests`.
- `app.py` serverer web-UI og SSE-output.
- `main.py` koerer samtaler ud fra en `session_cfg`, men runtime er endnu ikke fuldt session-isoleret.
- `projects.py` haandterer projektmapper og `settings.json`.
- `identities.py` loader persona-filer fra `identities/`.
- Memory ligger paa projektniveau under `projects/<project>/agent_x/memory.md` og deles paa tvaers af sessioner.
- Samtale-log ligger per session under `projects/<project>/sessions/<session_id>/conversation.md`.
- `app.py` har global runtime-state (`run_queue`, `run_lock`, `stop_event`, `is_running`) — et kendt naeste arkitekturtrin er at flytte dette til `sessions.py`.
- Der findes endnu ikke dedikerede moduler som `sessions.py`, `telemetry.py` eller `validators.py`.

## Dokumenternes roller

- `README.md`: brugerrettet introduktion og koersel.
- `AGENTS.md`: global agent-sandhed for repoet.
- `CLAUDE.md`: Claude-specifik arbejdsfil der supplerer `AGENTS.md`.
- `.guides/project_control.md`: brugerens operative guide til git og projektstyring.
- `ROADMAP.md`: aktive milestones og konkrete naeste opgaver.
- `FUTURE_PATCHES.md`: bevidst parkerede ideer og senere patches.
- `CHANGELOG.md`: det der faktisk blev aendret.

## Aktuel struktur

```text
dublog/
|-- app.py               # web-server og SSE-streaming (port 7842)
|-- main.py              # samtale-orchestrator, run_conversation(session_cfg)
|-- config.py            # statiske defaults til CLI-koersel
|-- model.py             # model-adapter: Ollama, LM Studio, Claude API
|-- prompts.py           # prompt-builder: identity + instruktioner + memory
|-- memory.py            # memory-IO: load, append, extract, konvergens
|-- identities.py        # parser og lister identity-filer
|-- projects.py          # projekt-management: opret, list, settings
|-- CLAUDE.md
|-- AGENTS.md
|-- ROADMAP.md
|-- FUTURE_PATCHES.md
|-- CHANGELOG.md
|-- README.md
|-- identities/          # persona-filer med frontmatter (name, language, length)
|   |-- template.md
|   `-- *.md
|-- projects/            # runtime-data, gitignored
|   `-- <project>/
|       |-- settings.json
|       |-- agent_a/
|       |   `-- memory.md
|       |-- agent_b/
|       |   `-- memory.md
|       `-- shared/
|           `-- conversation.md
`-- ui/
    `-- index.html       # enkeltfils frontend
```

## Arbejdsregler for Claude Code

1. Laes `CLAUDE.md`, `ROADMAP.md` og `CHANGELOG.md` foer stoerre arbejde.
2. Hvis du aendrer kode, struktur eller arbejdsdocs, saa opdater `CHANGELOG.md` i samme session.
3. Hver changelog-opdatering skal slutte med `Sign-off: Claude` eller `Sign-off: Codex`.
4. Brug `ROADMAP.md` til aktivt arbejde. Brug `FUTURE_PATCHES.md` til alt der er godt, men ikke aktivt endnu.
5. Skriv ikke fremtidig arkitektur som om den allerede er sand i kodebasen.
6. Hold dependencies minimale og foretraek smaae, verificerbare skridt.
7. Hvis kode og docs peger i hver sin retning, bring dem i sync i samme arbejdsflow.
8. Hvis en opgave ikke bliver faerdig, saa marker den som `blocked` eller `deferred` i roadmap i stedet for at lade status vaere implicit.
9. Skriv usikre antagelser tydeligt.
10. Faerdig > perfekt, men aldrig paa bekostning af strukturel sandhed.
11. Antag at dokumentation er always-on: relevante docs opdateres i samme session som aendringen.

## Claude-rolle i multi-agent mode

Som standard er Claude Code:

- orchestrator
- reviewer
- scribe

Claude maa godt lave mindre glue-aendringer, men hvis et stoerre runtime-spor kan delegeres rent, saa boer Builder-rollen holdes separat.
Hvis flere agenter bruges samtidigt, gaelder Single Writer Rule fra `AGENTS.md`.

## Changelog-kontrakt

Brug `CHANGELOG.md` som faktisk historik, ikke som oenskeliste.

- `Added` for nye filer, flows eller features
- `Changed` for aendret adfaerd eller struktur
- `Fixed` for fejlrettelser
- `Docs` for dokumentation eller arbejdsregler

Ved hver reel aendring skal `[Unreleased]` opdateres, og sessionens noter skal afsluttes med en tydelig sign-off-linje.

Eksempel:

```md
## [Unreleased]
### Changed
- Runtime blev gjort projekt-aware i `main.py`.
### Docs
- `ROADMAP.md` blev opdateret til ny milepaelsstruktur.
Sign-off: Claude
```

## Arbejdsflow pr. session

### Foer arbejdet

- laes relevante arbejdsdocs
- vaelg den milestone eller delopgave der arbejdes paa
- marker store aktive opgaver som `doing`

### Under arbejdet

- implementer i smaae sammenhaengende bidder
- opdater docs samme session hvis adfaerd eller struktur flytter sig
- hold forskellen tydelig mellem nuvaerende sandhed og naeste retning

### Efter arbejdet

- koer eller beskriv relevant verifikation
- saet faerdige roadmap-opgaver til `done`
- opdater `CHANGELOG.md`
- skriv naeste naturlige skridt kort og konkret

## Naeste retning

Den aktive retning ligger i `ROADMAP.md`, men de stoerste spor er:

- reel session-struktur frem for kun projekt-aware runtime
- observability og debug-data som kernefeature
- tydelige contracts for language, length og memory-output
- skarpere split mellem session-memory, projekt-memory og senere promotion

Hvis en ide ikke er aktiv endnu, skal den blive i `FUTURE_PATCHES.md` i stedet for at brede sig ind i hele dokumentlaget.
