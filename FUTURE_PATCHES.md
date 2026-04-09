# Future Patches

Denne fil er parkeringspladsen for gode ideer, senere patches og aabne designspoergsmaal.
Indhold her er bevidst ikke aktivt roadmap-arbejde endnu.

## Regler

- Brug denne fil til ideer der er lovende, men ikke aktive nu.
- Flyt foerst noget til `ROADMAP.md` naar det er naeste eller naer-naeste reelle arbejde.
- Tilfoej kort hvorfor noget er parkeret, saa vi ikke skal gaette senere.

## Parkerede patch-kandidater

- [ ] [CLI] CLI-flags for topic, rounds, models og project
  - Status: deferred
  - Hvorfor senere: nyttigt, men mindre vigtigt end session-arkitektur og observability

- [ ] [UI] Mere visuel debug-konsol og metrics-panel
  - Status: deferred
  - Hvorfor senere: boer bygge oven paa rigtig telemetry, ikke foer

- [ ] [RUNTIME] Flere samtidige sessioner i samme app-instans
  - Status: deferred
  - Hvorfor senere: kraever at enkelt-session flow er rent foerst

- [ ] [MEMORY] Mere avanceret promotion med manuel eller semiautomatisk approval
  - Status: deferred
  - Hvorfor senere: promotion-reglen skal vaere enkel foer den bliver smart

- [ ] [MEMORY] Event-log som `jsonl` ved siden af laesbare markdown-filer
  - Status: deferred
  - Hvorfor senere: god ide, men boer landes sammen med sessions og telemetry

- [ ] [VALIDATION] Staerkere sprogdetektion end simpel heuristik
  - Status: deferred
  - Hvorfor senere: foerste version skal bare kunne markere tydelige afvigelser

- [ ] [IDENTITY] Model-specifikke overrides i identity-frontmatter
  - Status: deferred
  - Hvorfor senere: nyttigt for lokale modeller, men ikke noedvendigt for at faa basen sand

- [ ] [SUMMARY] Tredje agent eller moderator til eftersummering
  - Status: deferred
  - Hvorfor senere: persona-lag er ikke hovedsporet foer runtime og observability er renere

- [ ] [EXPORT] Analyse- eller snapshot-eksporter pr. session
  - Status: deferred
  - Hvorfor senere: giver mest mening naar sessions er foerste-klasses objekter

- [ ] [TEST] Mere systematiske smoke-tests for backends og kontrakter
  - Status: deferred
  - Hvorfor senere: validation og telemetry boer lande foer teststrategien udvides

- [ ] [OPS] Agent Ledger for model, task, varighed og filer aendret
  - Status: deferred
  - Hvorfor senere: godt til cost/traceability, men ikke kritisk foer runtime og docs er mere stabile

- [ ] [WORKFLOW] Diff gate med eksplicit reviewer-pass foer merge
  - Status: deferred
  - Hvorfor senere: god disciplin, men boer bygge paa en enklere review-rytme foerst

- [ ] [WORKFLOW] GEMINI.md og normalizer-pipeline for research/import
  - Status: deferred
  - Hvorfor senere: nyttigt til lange inputspor, men ikke noedvendigt for dagens kerneflow

- [ ] [WORKFLOW] Strammere context isolation per agent
  - Status: deferred
  - Hvorfor senere: vigtigt paa sigt, men boer indfoeres sammen med mere moden delegation

## Aabne designspoergsmaal

1. Skal foerste stabile version kun koere en session ad gangen, eller skal fler-session support med tidligt?
2. Skal dansk vaere haardt krav i foerste version, eller skal engelsk vaere eksplicit fallback?
3. Skal project-memory promotion vaere manuel, semiautomatisk eller automatisk i den foerste stabile base?
4. Skal event-log primaert vaere markdown, `jsonl`, eller begge dele?
5. Skal identity-filer senere kunne have backend- eller model-specifikke overrides?

Indtil de spoergsmaal bliver aktive, bliver de her og ikke i den operative roadmap.
