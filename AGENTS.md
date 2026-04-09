# AGENTS.md - Arbejdskontrakt for Codex og andre kodeagenter

Denne fil giver Codex og andre kodeagenter samme projektkontekst som `CLAUDE.md`.
Maalet er, at agentarbejde i repoet foelger den samme sandhed, den samme roadmap og den samme changelog-disciplin.

## Formaal

- holde agentarbejde konsistent paa tvaers af Claude, Codex og senere tooling
- undgaa at docs driver vaek fra koden
- sikre at aendringer bliver spoerbare i changeloggen

## Projektets aktuelle tilstand

- Repoet er projekt-aware, men endnu ikke fuldt session-isoleret.
- `app.py` koerer UI, status og SSE-streaming.
- `main.py` driver samtalen med per-run `session_cfg`.
- `projects.py` opretter og persisterer projektdata under `projects/`.
- `identities/` indeholder persona-filer med simpel frontmatter.
- Samtalelog og memory er i dag knyttet til projektmapper, ikke til dedikerede session-mapper.
- Fremtidige moduler som `sessions.py`, `telemetry.py` og `validators.py` er planlagte, ikke implementerede.

## Hvilke docs der styrer hvad

- `AGENTS.md` er den globale agent-sandhed for repoet.
- `CLAUDE.md` og `AGENTS.md` skal pege samme vej. Hvis de divergerer, saa synk dem i samme session.
- `.guides/project_control.md` er brugerens operative guide og maa ikke modsige agentdocs.
- `ROADMAP.md` er den aktive arbejdsliste.
- `FUTURE_PATCHES.md` er den bevidste parkeringsplads.
- `CHANGELOG.md` er den faktiske historik.
- `README.md` er til brugeren, ikke til intern projektsandhed alene.

## Minimal agent-workflow baseline

Disse regler gaelder nu:

- Single Writer Rule: kun en agent maa skrive runtime-kode ad gangen.
- Rolleadskillelse: builder, reviewer og scribe maa ikke vaere samme ansvar i samme arbejdspas.
- Canonical truth > model output: struktur, filer og validatorer vinder over AI-tekst.
- Repo = engine, brugerdata = content: kode, templates og docs tracks; `projects/` og runtime-data goer ikke.

## Aktuel rollefordeling

- Human: scope, prioritet, release og stop.
- Claude Code: orkestrering, review og docs som standard.
- Codex: builder/refactor som standard.
- Andre agenter eller modeller: bruges kun med et afgraenset ansvar, fx review, normalisering eller test.

## Arbejdsregler for kodeagenter

1. Laes `AGENTS.md`, `CLAUDE.md`, `ROADMAP.md` og `CHANGELOG.md` foer stoerre aendringer.
2. Beskriv nuvaerende arkitektur som den er, ikke som vi haaber den bliver.
3. Brug `ROADMAP.md` til det aktive scope. Flyt ikke parkerede ideer ind i aktivt arbejde uden at opdatere roadmap.
4. Opdater `CHANGELOG.md` ved hver reel kode-, struktur- eller docs-aendring.
5. Afslut hver changelog-opdatering med `Sign-off: Codex` eller `Sign-off: Claude`.
6. Hold dependencies minimale og vaelg de mindste meningsfulde skridt.
7. Hvis en opgave ikke kan afsluttes, saa marker den som `blocked` eller `deferred` i stedet for at efterlade uklar status.
8. Hvis du indfoerer en ny regel for arbejdsflowet, skal den afspejles baade i relevant agentdoc og i changeloggen.
9. Behandl dokumentation som en fast del af leverancen, ikke som oprydning til sidst.
10. Hvis flere agenter bruges i samme session, skal det vaere eksplicit hvem der er writer.

## Changelog-regel

Naar en session flytter noget vigtigt for en fremtidig laeser, skal det skrives i `[Unreleased]`.
Sign-off-linjen er obligatorisk, saa det altid er tydeligt hvilken agent der sidst opdaterede historikken.

Eksempel:

```md
## [Unreleased]
### Added
- `FUTURE_PATCHES.md` til senere patch-ideer.
### Docs
- `AGENTS.md` og `CLAUDE.md` blev synket.
Sign-off: Codex
```

## Praktisk tommelfingerregel

- Aktivt nu: `ROADMAP.md`
- Senere maaske: `FUTURE_PATCHES.md`
- Skete faktisk: `CHANGELOG.md`

Det er vigtigere at holde den opdeling skarp end at skrive den perfekte fremtidsplan for tidligt.
