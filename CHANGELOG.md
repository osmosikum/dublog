# Changelog

Convention: Hver session der aendrer kode, struktur eller arbejdsdocs opdaterer `[Unreleased]` og afsluttes med `Sign-off: Claude` eller `Sign-off: Codex`.

## [Unreleased]
### Docs
- Gennemgået og synket hele dokumentlaget: CLAUDE.md, README.md, .gitignore og git-tracking.

Sign-off: Claude

## [baseline] — governance og git-setup
### Added
- `AGENTS.md` som parallel arbejdsfil for Codex og andre kodeagenter.
- `ROADMAP.md` som aktiv milestone-fil for naeste arbejde.
- `FUTURE_PATCHES.md` som parkeringsplads for senere patch-ideer og aabne designspoergsmaal.
- `.gitignore` til at holde runtime-data, caches og lokal stoej ude af repoet.
- `.guides/project_control.md` som projektets korte operative guide til git, docs og arbejdsrytme.

### Changed
- `CLAUDE.md` er skrevet om, saa den afspejler den nuvaerende projekt-aware arkitektur og de nye arbejdsregler.
- Changelog-flowet kraever nu en tydelig agent-sign-off for hver reel sessionopdatering.
- `CLAUDE.md`, `AGENTS.md`, `README.md` og `ROADMAP.md` er synket med en fast git-baseline og always-on dokumentationsregel.
- Repoet er initialiseret som git-repository paa den lokale `main`-branch.
- Global Git default branch er sat til `main` for fremtidige repos.
- `origin` er sat til `https://github.com/osmosikum/dublog.git`, og baseline-commit er pushet til `origin/main`.

### Docs
- Dokumentlaget skelner nu mellem nuvaerende sandhed, aktiv roadmap og parkerede fremtidsideer, saa repoet ikke laases fast for tidligt.
- `.guides/project_control.md` og `ROADMAP.md` afspejler nu at git-setup og foerste push faktisk er gennemfoert.

Sign-off: Codex

## [v1.2.0] - 2026-04-08
### Added
- `identities/` mappe - modulaere persona-filer med YAML-lignende frontmatter (`name`, `language`, `length`)
- Praeinstallerede identiteter: Skeptikeren, Optimisten, Moderatoren, Djaevlens Advokat
- `identities.py` - parser og lister identity-filer (ingen externe deps)
- `projects.py` - project management: opret, list, load/save settings, sanitize navne
- `projects/default/` - default projekt oprettes automatisk ved boot
- UI: projekt-selector med "+" knap til at oprette nye projekter
- UI: identity-dropdown per agent - auto-udfylder navn, sprog og laengde ved valg
- UI: sprog-dropdown per agent (dansk, engelsk, norsk, svensk, tysk)
- UI: laengde-dropdown per agent (kort / medium / lang)
- `/api/projects` GET+POST - list og opret projekter
- `/api/project/settings` GET+POST - hent og gem projekt-settings
- `/api/identities` GET - list tilgaengelige identiteter med metadata
- Projekt-settings gemmes til `settings.json` ved hvert run (fuld restore ved skift)

### Changed
- `main.py` omskrevet: `run_conversation(output_fn, project, session_cfg)` - ingen global config-mutation, traadsikkert
- `prompts.py` omskrevet: `build_system_prompt(identity_content, memory, language, length)` - identity er nu en string, ikke en filsti
- `memory.py`: `log_conversation` tager nu et `project_dir`-argument i stedet for hardkodet `shared/`
- `config.py` ryddet op - kun statiske konstanter, ingen runtime-state
- `/api/memory/a` og `/api/memory/b` er nu projekt-opmaerksomme via `?project=` query param
- Backend-skift i UI genindlaeser korrekt modeller fra den valgte backend

## [v1.1.0] - 2026-04-08
### Added
- `app.py` - web-server (stdlib `http.server` + `ThreadingMixIn`) paa port 7842
- `ui/index.html` - enkeltfils frontend med moerkt tema, live SSE-output og memory-panel
- Model-discovery endpoints: henter tilgaengelige modeller fra Ollama og LM Studio
- `/api/memory/a` og `/api/memory/b` - serverer agent-memory til frontend
- Memory-panel i bunden af UI der poller og viser begge agenters hukommelse live

### Changed
- `main.py` refaktoreret: al logik samlet i `run_conversation(output_fn=print)` saa UI og CLI deler samme kode
- `main.py` bruger nu `import config` direkte (frem for `from config import`) saa runtime-aendringer fra UI slaar igennem

## [v1.0.0] - 2026-04-08
### Added
- Fuld initial implementering af multi-agent sandbox
- `config.py` - central konfiguration (topic, agenter, backend, budgets, konvergens)
- `model.py` - model-adapter med support for Ollama, LM Studio og Claude API
- `memory.py` - fil-baseret memory med tags, budget, konvergens-detection og samtale-log
- `prompts.py` - struktureret prompt-builder (identity -> memory -> history -> task)
- `main.py` - orchestrator med hoved-loop, live output og tidlig stop ved konvergens
- `agent_a/identity.md` og `agent_b/identity.md` - agent-personas
- `agent_a/memory.md` og `agent_b/memory.md` - tomme startfiler
- `shared/` mappe til conversation-log og run-config
- `README.md` med how-to sektioner
- `CHANGELOG.md` (denne fil)

### Changed
- (intet)

### Fixed
- (intet)
