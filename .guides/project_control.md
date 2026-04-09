# Projektstyring for `dublog`

Denne guide er den korte, operative manual for hvordan du styrer dette repo i praksis.
Den bygger oven paa `.guides/github_superguide.md`, men er skrevet til dette konkrete projekt.

## Hvad er kilden til sandhed?

Brug dokumenterne saadan:

- `README.md`: hvordan projektet koerer og hvad det er.
- `ROADMAP.md`: aktivt arbejde og naeste tekniske skridt.
- `CHANGELOG.md`: det der faktisk er blevet aendret.
- `CLAUDE.md`: arbejdsregler for Claude Code.
- `AGENTS.md`: arbejdsregler for Codex og andre kodeagenter.
- `.guides/github_superguide.md`: generel Git-reference og forklaringer.
- `.guides/project_control.md`: denne fil, dvs. den praktiske driftsguide for repoet.

Hvis to dokumenter siger noget forskelligt, skal de bringes i sync med det samme.

## Standard for dette repo

- `main` er baseline-branch.
- `origin` er GitHub-remoten for repoet.
- lokal `main` tracker `origin/main`.
- Stoerre arbejde sker i branches, ikke direkte paa `main`.
- Runtime-data skal ikke i git.
- Dokumentation koerer altid sammen med aendringer, ikke bagefter.
- `CHANGELOG.md` opdateres ved hver reel kode-, struktur- eller docs-aendring.

## Multi-agent baseline

Hvis du bruger flere agenter samme dag, saa hold det simpelt:

- kun en writer ad gangen paa runtime-kode
- vaer eksplicit om hvem der er builder, reviewer og scribe
- lad ikke to agenter skrive i samme runtime-spor samtidig
- hvis workflow-reglerne aendrer sig, saa opdater `AGENTS.md`, `CLAUDE.md` og changelog i samme session

Praktisk standard lige nu:

- Claude Code = orchestrator, review og docs
- Codex = builder og refactor
- du = scope, prioritet, release og kill switch

## Hvad skal ikke i Git?

Dette repo skal tracke kildekode, docs og konfigurationsbeslutninger.
Det skal ikke tracke loebende runtime-output.

Ignorerede ting i dette repo:

- `projects/` - projektdata, memory, settings og samtalelogs fra koersel
- `identities/custom/` - lokale identities, som appen loader men repoet ikke skal tracke
- root-level brugeridentities i `identities/` - ignoreres som standard; brug `custom/`
- `shared/` - legacy runtime-logs i repo-roden
- `agent_a/memory.md` og `agent_b/memory.md` - legacy runtime-memory
- `__pycache__/`, virtuelle miljoeer og editor-stoej

Hvis du vil gemme et vigtigt output, skal det eksporteres bevidst til en dokumenteret fil, ikke bare ende i runtime-mapperne.

Tracked identity-filer i repoet boer kun vaere:

- `identities/template.md`
- `identities/examples/*.md`
- dokumentation i `identities/`

## Regel for English migration

Sprogrydning i dette repo maa ikke behandles som ren tekstudskiftning.

- engine-tekst og operative docs kan oversaettes direkte
- persisted runtime-values maa ikke omdoebes uden compatibility
- `projects/**`, memory og session-logs maa ikke masseoversaettes
- example identities og template er content-spor og skal afgoeres eksplicit

Den konkrete afgraensning ligger i `.guides/english_migration_scope.md`.

## Daglig arbejdsrytme

Brug denne rytme som standard:

1. Start med `git status --short --branch`.
2. Hvis der er en remote, koer `git pull --ff-only` paa den branch du arbejder paa.
3. Laes `ROADMAP.md` og `CHANGELOG.md` hvis du skal videre paa eksisterende arbejde.
4. Opret en branch hvis arbejdet er stoerre end en lille docs- eller hotfix-aendring.
5. Implementer aendringen.
6. Opdater docs i samme session:
   - `ROADMAP.md` hvis aktivt arbejde eller status aendrer sig
   - `CHANGELOG.md` altid ved reel aendring
   - `CLAUDE.md` eller `AGENTS.md` hvis arbejdsreglerne flytter sig
7. Review med `git diff`.
8. Stage og commit i samlede, logiske bidder.

## Branching-regel

Branch hvis mindst en af disse er sand:

- aendringen er stoerre end en lille tekstrettelse
- du eksperimenterer
- du kan bryde noget undervejs
- du vil arbejde i flere spor samtidig

Praktiske branch-navne:

- `feature/session-manager`
- `fix/sse-cleanup`
- `docs/git-baseline`
- `refactor/project-runtime`

Hvis en agent laver branchen, er `codex/...` eller `claude/...` ogsaa fint, men meningen skal stadig vaere tydelig.

## Commit-standard

Hold commits smaae nok til at give mening hver for sig.
Brug gerne en enkel conventional-commit-stil:

- `feat: ...`
- `fix: ...`
- `docs: ...`
- `refactor: ...`
- `chore: ...`

Eksempler:

- `docs: add project control guide and git baseline`
- `feat: introduce session manager skeleton`
- `fix: keep SSE output tied to active session`

## Hvad du aldrig skal goere rutinemæssigt

- lav ikke `git reset --hard` som standard-oprydning
- force-push ikke `main`
- commit ikke runtime-mapperne bare fordi de er nye
- lad ikke `ROADMAP.md` og `CHANGELOG.md` blive bagefter koden
- skriv ikke fremtidig arkitektur ind i docs som om den allerede findes

## Git-opsætning for dette repo

Nuværende status:

- repoet er initialiseret lokalt
- default arbejdsbranch er `main`
- `origin` peger paa `https://github.com/osmosikum/dublog.git`
- foerste baseline er allerede pushet, og `main` tracker `origin/main`

Repoet skal initialiseres paa `main`.
Hvis du senere vil pushe til GitHub:

```bash
git remote add origin <REMOTE_URL>
git push -u origin main
```

Foer commits virker stabilt paa en ny maskine, skal din Git-identitet vaere sat:

```bash
git config --global user.name "Dit Navn"
git config --global user.email "din@email.dk"
```

Hvis du vil saette global default branch til `main` fremover:

```bash
git config --global init.defaultBranch main
```

## Versions- og release-regel

Indtil basen er stabil, er `0.x` et rimeligt versionsspor.
Naar du vil markere en baseline, brug annotated tags:

```bash
git tag -a v0.1.0 -m "First baseline"
git push origin v0.1.0
```

Versionsnummeret skal passe med `CHANGELOG.md`.

## Hvordan Claude og Codex skal bruges

Hvis du bruger en kodeagent i dette repo, skal den som minimum:

- laese relevante styringsdocs foer stoerre arbejde
- holde docs og kode i sync i samme session
- opdatere `CHANGELOG.md` ved reelle aendringer
- holde aktivt arbejde i `ROADMAP.md`
- lade parkerede ideer blive i `FUTURE_PATCHES.md`

Det er ikke valgfrit ekstraarbejde. Det er en del af hvordan projektet styres.
