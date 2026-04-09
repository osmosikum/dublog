# English Migration Scope

This guide defines how the repo is made English without losing existing data or hiding breaking changes behind a text cleanup.

## Purpose

- make the engine, UI and the project's operative docs English
- avoid existing `projects/` data being lost or changing meaning
- separate text translation from real data and contract migration

## Language boundary

This repo follows this main rule:

- structured system stuff = English
- human free text = the user's chosen language

That means:

- UI labels, docs, code comments, server messages, enums and the canonical save format should be English
- chat input, topics, project names, local note tracks and other free user content may remain in Danish or another language
- the user's free text must not be auto-translated just to make the repo look cleaner
- content fields must not be treated as system contracts

## Zone A - translate directly

These parts are engine or operative docs and can be translated deliberately:

- UI labels, button text, alerts and empty-state text in `ui/index.html`
- server and status messages in `app.py` and `main.py`
- prompt instructions, comments and docstrings in `prompts.py`, `memory.py`, `projects.py`, `config.py` and related engine files
- repo docs such as `README.md`, `CLAUDE.md`, `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`, `FUTURE_PATCHES.md` and `.guides/*`

## Zone B - requires compatibility first

These parts look like text but actually function as data or contracts:

- saved settings values in `projects/*/settings.json`
- default values in `config.py` and `projects.py`
- UI select values for language and length
- identity slugs already persisted in old projects

Known legacy values in runtime data:

- languages: `dansk`, `engelsk`, `norsk`, `svensk`
- lengths: `kort`, `medium`, `lang`
- old identity slugs: `skeptikeren`, `optimisten`

Rule: read old values, normalise them in code, and only switch to English canonical values later when read-compatibility has landed.

## Zone C - must not be auto-translated

These parts are runtime history or user content:

- `projects/**` such as historical `settings.json`, memory files, session logs and conversation logs
- `identities/custom/**`
- tracked example content in `identities/examples/**`, until we take a separate content pass
- `identities/template.md`, unless we simultaneously decide which language baseline new identities should have
- free user input such as topics, chat messages, project names and ad hoc instructions

Rule: no blind mass-translation of content or history.

## No-data-loss rules

- existing `projects/*/settings.json` must still be readable after the migration
- the UI may become English before persisted values do
- if the write format switches to English, legacy values must still be accepted on load
- memory and session logs must not be overwritten or backfill-translated
- identity meaning must not change unintentionally as a side effect of the language cleanup

## Concrete compatibility requirement

Before we switch canonical engine values to English, the app must be able to map at least:

- `dansk` -> `danish`
- `engelsk` -> `english`
- `norsk` -> `norwegian`
- `svensk` -> `swedish`
- `kort` -> `short`
- `lang` -> `long`

In addition, old identity slugs must be handled explicitly. Either:

- we map them to currently shipped identities
- or we ship legacy identity shims

Without one of those two tracks, some old projects will fall back to generic identity behaviour.

## Recommended order

1. Introduce normalisation for language, length and legacy identity slugs.
2. Translate UI labels and server messages to English without breaking old persisted values.
3. Switch defaults and save path to English canonical values.
4. Translate repo docs, comments and docstrings.
5. Make a separate decision about whether the repo's example identities and template should also become English.

## Not part of this migration

- translating old conversation logs or memory files
- mass-updating the user's local identities
- mixing session architecture or telemetry work into the language migration

## Practical rule of thumb

If a string is only text for a reader, it can be translated.
If a string is used as stored state, option value, slug or contract, compatibility must come first.
If a string comes from the user as free text, treat it as content and let it keep the user's language.
