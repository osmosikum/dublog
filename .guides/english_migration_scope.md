# English Migration Scope

Denne guide afgraenser hvordan repoet goeres engelsk uden at miste eksisterende data eller skjule breaking changes bag en tekstoprydning.

## Formaal

- goere engine, UI og projektets operative docs engelske
- undgaa at eksisterende `projects/`-data gaar tabt eller skifter betydning
- skille tekstoversaettelse fra reel data- og kontraktmigration

## Zone A - oversaettes direkte

Disse dele er engine eller operative docs og kan oversaettes bevidst:

- UI-labels, knaptekster, alerts og tom-state-tekster i `ui/index.html`
- server- og statusbeskeder i `app.py` og `main.py`
- prompt-instruktioner, comments og docstrings i `prompts.py`, `memory.py`, `projects.py`, `config.py` og beslægtede engine-filer
- repo-docs som `README.md`, `CLAUDE.md`, `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`, `FUTURE_PATCHES.md` og `.guides/*`

## Zone B - kraever compatibility foerst

Disse dele ligner tekst, men fungerer reelt som data eller kontrakter:

- gemte settings-vaerdier i `projects/*/settings.json`
- default-vaerdier i `config.py` og `projects.py`
- UI-select values for language og length
- identity-slugs der allerede er persisteret i gamle projekter

Kendte legacy-vaerdier i runtime-data lige nu:

- languages: `dansk`, `engelsk`, `norsk`, `svensk`
- lengths: `kort`, `medium`, `lang`
- gamle identity-slugs: `skeptikeren`, `optimisten`

Regel: laes gamle vaerdier, normaliser dem i koden, og skift foerst senere til engelske canonical values naar read-compatibility er landet.

## Zone C - maa ikke auto-oversaettes

Disse dele er runtimehistorik eller brugerindhold:

- `projects/**` som historiske `settings.json`, memory-filer, session-logs og conversation logs
- `identities/custom/**`
- tracked eksempelindhold i `identities/examples/**`, indtil vi tager en separat content-pass
- `identities/template.md`, hvis vi ikke samtidig beslutter hvilken sprogbaseline nye identities skal have

Regel: ingen blind masseoversaettelse af content eller historik.

## No-data-loss regler

- eksisterende `projects/*/settings.json` maa fortsat kunne laeses efter migrationen
- UI maa gerne blive engelsk foer persisted values bliver engelske
- hvis write-formatet skifter til engelsk, skal legacy-vaerdier stadig accepteres ved load
- memory og session-logs maa ikke overskrives eller backfill-oversaettes
- identity-mening maa ikke aendres utilsigtet som sideeffekt af sprogrydning

## Konkret compatibility-krav

Foer vi skifter canonical engine-vaerdier til engelsk, skal appen kunne mappe mindst:

- `dansk` -> `danish`
- `engelsk` -> `english`
- `norsk` -> `norwegian`
- `svensk` -> `swedish`
- `kort` -> `short`
- `lang` -> `long`

Derudover skal gamle identity-slugs haandteres eksplicit. Enten:

- vi mapper dem til nuvaerende shippede identities
- eller vi shipper legacy identity-shims

Uden et af de to spor vil nogle gamle projekter falde tilbage til generisk identity-adfaerd.

## Anbefalet raekkefoelge

1. Indfoer normalisering for language, length og legacy identity-slugs.
2. Oversaet UI-labels og serverbeskeder til engelsk uden at bryde gamle persisted values.
3. Skift defaults og save-path til engelske canonical values.
4. Oversaet repo-docs, comments og docstrings.
5. Tag en separat beslutning om repoets example-identities og template ogsaa skal blive engelske.

## Ikke en del af denne migration

- at oversaette gamle conversation logs eller memory-filer
- at masseopdatere brugerens lokale identities
- at blande session-arkitektur eller telemetry-arbejde ind i sprogmigrationen

## Praktisk tommelfingerregel

Hvis en streng kun er tekst for en laeser, kan den oversaettes.
Hvis en streng bruges som lagret state, option value, slug eller kontrakt, skal der foerst laves compatibility.
