# Roadmap

Denne roadmap tracker aktivt arbejde og naeste naturlige skridt.
Den er bevidst smallere end playbooken og smallere end `FUTURE_PATCHES.md`.

## Regler

- Brug statusfelterne `todo`, `doing`, `blocked`, `done`, `deferred`.
- Hver opgave skal vaere lille nok til en almindelig arbejdssession.
- `ROADMAP.md` beskriver aktivt eller naer-aktivt arbejde.
- `CHANGELOG.md` beskriver det der faktisk blev udfoert.
- Ideer der ikke er aktive endnu, flyttes til `FUTURE_PATCHES.md`.

## Milestone 0 - Docs og governance baseline
Status: done
Formaal: Goere dokumentlaget til projektets nuvaerende operative sandhed uden at fryse fremtidig arkitektur for tidligt.

- [x] [DOCS] Opdatere `CLAUDE.md`
  - Status: done
  - Hvorfor: den gamle fil beskrev en aeldre baseline og manglede de nye styringsregler
  - Output: opdateret arbejdsfil for Claude
  - Done naar: nuvaerende repo-tilstand, docs-roller og changelog-regel er tydelige

- [x] [DOCS] Oprette `AGENTS.md`
  - Status: done
  - Hvorfor: Codex og andre kodeagenter skal have en tilsvarende arbejdsfil
  - Output: ny agent-guide
  - Done naar: changelog-disciplin, roadmap-brug og projektets aktuelle tilstand er beskrevet

- [x] [DOCS] Oprette `ROADMAP.md`
  - Status: done
  - Hvorfor: aktivt arbejde skal skilles fra vision og parkerede ideer
  - Output: denne fil
  - Done naar: milestones og naeste spor kan laeses uden at gaette

- [x] [DOCS] Oprette `FUTURE_PATCHES.md`
  - Status: done
  - Hvorfor: gode ideer skal kunne parkeres uden at blive falske loefter
  - Output: separat backlog for senere patches
  - Done naar: deferred arbejde har et tydeligt hjem

- [x] [DOCS] Indfoere changelog sign-off-regel
  - Status: done
  - Hvorfor: hver arbejdsession skal kunne spores til agent
  - Output: regel i agentdocs og opdateret changelog-format
  - Done naar: `CHANGELOG.md` og agentdocs bruger samme sign-off-kontrakt

- [x] [OPS] Etablere git-baseline for repoet
  - Status: done
  - Hvorfor: repoet skal kunne versionsstyres uden runtime-stoej
  - Output: `.gitignore` og initialisering paa `main`
  - Done naar: kildekode og docs kan trackes uden at runtime-data fylder status

- [x] [OPS] Konfigurere remote og foerste push
  - Status: done
  - Hvorfor: baseline skal ikke kun findes lokalt, men ogsaa kunne synkes til GitHub
  - Output: `origin` sat og `main` tracket mod `origin/main`
  - Done naar: den lokale baseline-commit findes paa remote, og `main` tracker `origin/main`

- [x] [OPS] Saette global git-default til `main`
  - Status: done
  - Hvorfor: nye repos skal ikke falde tilbage til `master`
  - Output: `init.defaultBranch=main` i brugerens git-config
  - Done naar: nye lokale repos oprettes med `main` som default branch

- [x] [DOCS] Oprette brugerens projektstyringsguide
  - Status: done
  - Hvorfor: styring af repo, branches, changelog og agents skal vaere samlet et sted
  - Output: `.guides/project_control.md`
  - Done naar: projektets git- og docs-rytme kan foelges uden at laese den lange referenceguide foerst

- [x] [DOCS] Etablere minimal agent-workflow baseline
  - Status: done
  - Hvorfor: multi-agent arbejde skal vaere styret uden at blive overdesignet
  - Output: `AGENTS.md`, `CLAUDE.md` og `.guides/project_control.md` beskriver roller og single-writer baseline
  - Done naar: `AGENTS.md` er global sandhed, og det er tydeligt hvem der skriver kode i en multi-agent session

- [x] [OPS] Auditere `.gitignore` og engine/content-graense
  - Status: done
  - Hvorfor: variable filer skal ud af repoet, mens templates og eksempler forbliver tracked
  - Output: smartere `.gitignore`, identity-struktur med `examples/` og `custom/`, opdaterede docs
  - Done naar: runtime-data og lokale identities ignoreres, mens repoet stadig shipper templates og eksempler

## Milestone 0.5 - English migration boundary
Status: doing
Formaal: Goere det klart hvad der kan oversaettes direkte, og hvad der foerst kraever compatibility, saa ingen eksisterende runtime-data gaar tabt.

- [x] [ARCH] Definere English migration boundary og no-data-loss-regler
  - Status: done
  - Hvorfor: sprogrydning maa ikke blande UI-tekst, persisted state og content sammen
  - Output: `.guides/english_migration_scope.md`
  - Done naar: engine, persisted values og content er skilt i tydelige migrationszoner

- [ ] [COMPAT] Indfoere normalisering for language, length og legacy identity-slugs
  - Status: done
  - Hvorfor: gamle projekter bruger stadig danske enum-vaerdier og i nogle tilfalde udgaaede identity-slugs
  - Output: kompatibilitetslag foer canonical engelske values indfoeres
  - Done naar: gamle `settings.json` kan laeses korrekt samtidig med at nye engelske vaerdier accepteres

- [ ] [UI] Oversaette engine-UI til engelsk uden at bryde persisted values
  - Status: done
  - Hvorfor: labels og fejltekster kan skifte foer dataformatet goer det
  - Output: engelske labels, knapper og beskeder i appen
  - Done naar: UI er engelsk, men gamle settings loader stadig korrekt

- [ ] [DOCS] Oversaette engine-docs og kommentarer til engelsk
  - Status: todo
  - Hvorfor: operative docs og engine-kommentarer boer pege samme vej som UI og defaults
  - Output: engelske repo-docs og engelske engine-kommentarer
  - Done naar: projektets operative engine-lag er engelsk uden at content tvinges med

- [ ] [CONTENT] Beslutte separat strategi for example identities og template
  - Status: todo
  - Hvorfor: repo-shippet indhold er content, ikke bare engine-tekst
  - Output: bevidst beslutning om examples/template skal forblive danske, blive engelske eller eksistere i begge versioner
  - Done naar: content-sporet er afgjort eksplicit i stedet for at ride med engine-migrationen

## Milestone 1 - Session-aware base
Status: doing
Formaal: Loefte den nuvaerende projekt-aware runtime til en reel session-struktur uden at omskrive hele appen paa en gang.

- [x] [ARCH] Definere disk-layout for `projects/<project>/sessions/<session_id>/`
  - Status: done
  - Hvorfor: session-data skal skilles fra projektets langlivede data
  - Output: dokumenteret maallayout og mappeoprettelse
  - Done naar:
    - sessionmappe oprettes med unik id
    - transcript, debug og metadata kan ligge i sessionen
    - projektdata kan bevares uden at vaere bundet til en enkelt koersel

- [ ] [ARCH] Oprette `sessions.py` med foerste `SessionManager`
  - Status: todo
  - Hvorfor: runtime-state maa ikke kun leve som globale variabler i `app.py`
  - Output: `sessions.py` plus integration i web-run flow
  - Done naar:
    - sessioner kan oprettes og markeres som running/done/error
    - session paths kan laeses samlet fra manageren

- [ ] [RUNTIME] Flytte output og status fra global queue til session-bundet struktur
  - Status: todo
  - Hvorfor: nuvaerende `run_queue` og `is_running` er for grove til naeste fase
  - Output: session-aware output/status flow
  - Done naar:
    - output er bundet til en session
    - status kan laeses uden global sandhed alene

- [ ] [DOCS] Synke docs naar session-strukturen findes
  - Status: todo
  - Hvorfor: docs maa ikke skrive session-arkitektur som sand foer den er bygget
  - Output: opdaterede arbejdsdocs og evt. README-noter
  - Done naar: den implementerede session-model er dokumenteret

## Milestone 2 - Observability foerst
Status: todo
Formaal: Goere det synligt hvad systemet injicerer, hvor output driver, og hvor modellerne bliver traette.

- [ ] [ARCH] Oprette `telemetry.py`
  - Status: todo
  - Hvorfor: debugbarhed skal vaere en kernefeature
  - Output: samlet modul til simple runtime-metrics
  - Done naar: prompt-, output- og timingdata kan registreres pr. agentkald

- [ ] [RUNTIME] Logge prompt chars, memory lines, history turns og output chars
  - Status: todo
  - Hvorfor: vi skal kunne se konteksttryk og outputdrift
  - Output: konkrete metrics i runtime og filoutput
  - Done naar: minimumsmetrikker kan laeses uden manuel gaetning

- [ ] [UI] Vise et simpelt debug-panel i UI
  - Status: todo
  - Hvorfor: observability er mest nyttig mens en session koerer
  - Output: live debug-visning i browseren
  - Done naar: noegletal og fejltilstande vises under koersel

## Milestone 3 - Contracts og validation
Status: todo
Formaal: Goere language, length og memory-output til haandhaevelige kontrakter i stedet for bloede labels.

- [ ] [VALIDATION] Oprette `validators.py`
  - Status: todo
  - Hvorfor: output og identity-data skal kunne tjekkes systematisk
  - Output: dedikeret valideringsmodul
  - Done naar: tomme svar, manglende `[MEMORY]` og identitetsfejl kan detekteres

- [ ] [VALIDATION] Indfoere heuristisk language-check
  - Status: todo
  - Hvorfor: lokale modeller driver let mellem sprog
  - Output: simpel sprogdetektion og afvigelsesmarkering
  - Done naar: systemet kan markere sandsynlige sprogglidninger

- [ ] [VALIDATION] Oversaette `kort/medium/lang` til eksplicitte runtimegraenser
  - Status: todo
  - Hvorfor: laengdevalg skal kunne maales bagefter
  - Output: tydelig preset-til-kontrakt mapping
  - Done naar: length checks kan sammenholdes med faktisk output

## Milestone 4 - Memory flow og promotion
Status: todo
Formaal: Adskille session-memory, projekt-memory og senere promotion, saa memory bliver simpel og sporbar.

- [ ] [MEMORY] Splitte projekt-memory og session-memory fysisk
  - Status: todo
  - Hvorfor: nuvaerende struktur er for flad til laengere forloeb
  - Output: separat lagring for midlertidig og langlivet memory
  - Done naar: session-sletning ikke oedelaegger projektets langtidshukommelse

- [ ] [MEMORY] Definere foerste promotion-regel
  - Status: todo
  - Hvorfor: ikke alt skal automatisk blive permanent memory
  - Output: enkel promotion-strategi
  - Done naar: det er tydeligt hvad der flyttes op og hvorfor

- [ ] [DOCS] Beskrive memory-levels og promotionflow
  - Status: todo
  - Hvorfor: memory-arkitektur maa ikke blive semi-magisk
  - Output: opdaterede docs
  - Done naar: en ny laeser kan foelge memory-flowet uden at laese kode foerst

## Milestone 5 - Streaming og UI-hardening
Status: todo
Formaal: Goere koerslen mere levende og robust uden at miste den simple base.

- [ ] [UI] Goere streaming mere session-aware
  - Status: todo
  - Hvorfor: output skal kunne vises loebende pr. koersel
  - Output: forbedret streamingflow
  - Done naar: klienten kan foelge en konkret session uden global forvirring

- [ ] [RUNTIME] Rydde op i cleanup ved success, stop og fejl
  - Status: todo
  - Hvorfor: sessionafslutning skal vaere tydelig og robust
  - Output: mere eksplicit cleanup-flow
  - Done naar: state og filer efterlades konsistent efter alle udgange

- [ ] [TEST] Verificere at live output ikke kraever faerdigt helsvar foerst
  - Status: todo
  - Hvorfor: streaming skal opleves som streaming
  - Output: enkel verifikation eller smoke-test
  - Done naar: streamingadfaerd kan dokumenteres og gentages
