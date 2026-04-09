# Din superguide til Git og versionsstyring

## Hvad Git egentlig er

Git er et versionsstyringssystem: det gemmer historik over ændringer i filer, så du kan se *hvad* der ændrede sig, *hvornår*, og rulle tilbage, sammenligne og samarbejde uden at miste overblik. citeturn7search14turn5search19

Det særlige ved Git (vs. mange ældre systemer) er, at Git tænker i **snapshots**: hver gang du committer, gemmer Git i praksis “et billede” af projektets tilstand på det tidspunkt. Ændrede filer gemmes som nye snapshots; uændrede filer genbruges effektivt via referencer. citeturn8search0

**Fun fact:** Mange “ser” commits som diffs (ændringer), fordi GitHub og tools viser dem sådan — men diff’en bliver typisk beregnet ved at sammenligne snapshots, ikke gemt som den primære sandhed. citeturn8search19turn8search0

## Grundbegreber du skal have på plads

Hvis du kan disse (uden at kunne alt), bliver Git meget mindre magisk:

**Repo**  
Et Git-repository er i praksis en mappe med en skjult `.git/`-mappe, hvor Git gemmer metadata og historik. `git init` opretter denne struktur. citeturn9view0

**Working tree (arbejdsmappe)**  
Det er de filer, du står og redigerer lige nu.

**Staging area (også kaldet “index”)**  
En mellemstation: du vælger præcis hvilke ændringer, der skal med i næste commit. Git’s egen bog beskriver staging area som en fil i Git-directory’et, som holder hvad der kommer i næste commit. citeturn0search0

**Commit**  
En commit gemmer snapshot’et af det du har staged. En commit indeholder også metadata (forfatter, email, besked) og peger på forrige commit(s) — ved merges kan den have flere “parents”. citeturn7search22

**Branch**  
En branch er i praksis en flytbar reference (pegepind) til en commit; det gør branching letvægtigt i Git. `HEAD` peger på den branch/commit du “står på” lige nu. citeturn1search9turn8search23

**Remote**  
En remote er bare “et andet repo et andet sted” (typisk på GitHub/GitLab eller en server). Du kan have flere remotes, og Git kan hente/pushe mellem dem. citeturn5search1turn5search2

## Første opsætning i praksis

Det her er den mest stabile “første gang”-opsætning, uanset projekt.

**Installér Git og tjek version**  
Den officielle Git-side viser pr. 2026-04-09 en “Latest version” på 2.53.0, og du kan altid tjekke din lokale version med `git --version`. citeturn6search0turn9view0  
Windows kører typisk via “Git for Windows”, som præsenterer sin egen build-version (fx 2.53.0.2). citeturn6search1turn5search25

**Konfigurér din identitet**  
Git putter `user.name` og `user.email` ind i commits, så historik kan spores. citeturn3search20turn3search1

Kør (én gang, globalt):

```bash
git config --global user.name "Dit Navn"
git config --global user.email "din@email.dk"
```

**Sæt default branch til `main`**  
Du har to gode muligheder:

1) Sæt standarden globalt (Git 2.28+ har dette som en officiel mulighed). citeturn3search0turn0search22  
```bash
git config --global init.defaultBranch main
```

2) Vælg branchnavn pr. repo med `git init -b main` (Git dokumenterer `--initial-branch/-b`). citeturn9view0  
```bash
git init -b main
```

**Fun fact:** Git’s `git-init` docs nævner, at default stadig er `master` “currently”, men at det forventes at skifte til `main` ved Git 3.0. citeturn9view0

**Opret repo i dit projekt (fra “ingen git” til “første commit”)**  
I projektets rodmappe:

```bash
git init -b main
git status
```

Tilføj en `.gitignore` (mere om den senere), og lav første commit:

```bash
git add -A
git commit -m "chore: initial commit"
```

Git’s mental model er: du ændrer i working tree → du “stager” udvalgte ændringer → du committer staging area ind i repo-historikken. citeturn0search0turn8search0

## Din daglige arbejdscyklus uden friktion

Når du arbejder, er det her den lille rytme, der holder dig ude af Git-kaos:

**Se hvad der sker**  
`git status` er din bedste ven. Pro Git viser også en “short status” med `git status -s`, hvis du vil have det kompakt. citeturn8search2

**Se forskellen før du gemmer**  
`git diff` kan vise forskellen mellem working tree ↔ staging area, og `git diff --staged` viser staging ↔ sidste commit. citeturn8search16turn4search17

**Stage selektivt (når du vil være skarp)**  
`git add -p` lader dig stage “hunks” (dele af en fil), så du kan lave commits der hver især er én idé. (Det gør dit changelog og debugging meget lettere.) citeturn4search17

**Commit småt, men færdigt**  
En commit er et snapshot af det staged — så begræns dig gerne til ét “tema” pr. commit. Det er en praksis mere end en regel, men det passer godt med Git’s snapshot-model. citeturn8search0turn7search22

**Når du bliver afbrudt midt i noget**  
Brug `git stash`: den kan gemme din nuværende working tree + index “på en stak”, så du kan hoppe væk og tilbage igen. Git-dokumentationen beskriver præcis dette formål: gem nuværende tilstand, gå tilbage til en ren working directory, og “apply/pop” senere. citeturn4search2turn4search6

### Hvordan du fortryder uden at smadre historik

Der er tre “familier” af fortrydelse, og de gør **ikke** det samme:

**Restore (fortryd filer/unstage) — moderne og safe**  
Git har `git restore` (introduceret i Git 2.23) som et mere målrettet alternativ til mange “undo”-cases, især for filer og staging. citeturn12search5turn12search6

**Revert (fortryd en commit ved at lave en ny commit)**  
`git revert` laver nye commit(s), der ophæver effekten af tidligere commit(s). Det er derfor standard-valget, når du allerede har delt/pushet noget og vil rette uden at omskrive historik. citeturn12search0turn12search9

**Reset (flyt HEAD baglæns; kan være farligt)**  
`git reset --hard` kan overskrive filer og i praksis destruere lokale ændringer. Pro Git kalder eksplicit `--hard` den farlige variant og understreger, at den kan ødelægge data ved at overskrive working directory. citeturn12search7turn12search3

En god tommelfingerregel:  
Hvis det er “offentligt” (andre kan have trukket det), så brug **revert**. Hvis det er “privat” (kun hos dig), kan du overveje reset — men med respekt. citeturn12search9turn12search4

## Branching og merging uden drama

### Det enkle svar på “hvornår skal jeg branche?”

Hvis *én* af disse er sand, så branch:

- ændringen kan ødelægge noget undervejs  
- du vil eksperimentere eller refaktorere stort  
- du vil arbejde i flere spor samtidig  
- du vil kunne “shippe” hurtigt fra `main` uden at blande halvfærdige ting ind

GitHub Flow er et bevidst simpelt svar: lav en branch, commit der, få feedback/review, merge tilbage. GitHub beskriver flowet som et let, branch-baseret workflow, der virker ikke kun for kode, men også docs og roadmaps. citeturn1search8

### Sådan gør du branches med moderne Git-kommandoer

Git anbefaler `git switch` til branch-skift, og den dokumenterer også at `-c` kan oprette branch og skifte i ét hug. citeturn1search1turn4search17

```bash
git switch -c feature/session-isolation
# ... arbejd ...
git add -A
git commit -m "feat: isolate sessions from projects"
```

Når du er klar til at samle:

```bash
git switch main
git merge feature/session-isolation
```

`git merge` er standardværktøjet til at inkorporere ændringer fra en branch ind i en anden. citeturn1search25

### Merge vs. rebase

De to store måder at “holde en feature-branch opdateret” på er merge og rebase — og de har forskellige tradeoffs.

Pro Git beskriver rebase sådan: den “genafspiller” commits fra én linje oven på en anden; merge samler endpoints og laver en historik, der viser forgreningen (ofte via en merge commit). Snapshot’et du ender med kan være identisk, men historikken bliver forskellig. citeturn1search10turn1search5

Som noob-best-practice:  
Start med merges. Tag rebase ind, når du *bevidst* vil holde historik “lineær”, og især når du ved, hvad det betyder for delte branches.

## Remote repos, sync og login

### Remote i klare ord

En remote er en “hostet udgave” af dit repo et andet sted. Du kan have flere, men den typiske første hedder `origin`. citeturn5search1turn5search2

Tilføj remote:

```bash
git remote add origin <REMOTE_URL>
git remote -v
```

`git remote`-dokumentationen beskriver `add` som måden at registrere en remote, og at `git fetch <name>` derefter kan skabe/opdatere remote-tracking branches. citeturn5search2

### Fetch vs. pull vs. push

**Pull**  
Git docs beskriver `git pull` som: den kører først `git fetch` og integrerer derefter den hentede gren ind i din nuværende branch (hvordan integrationen sker afhænger af merge/rebase-indstillinger). citeturn1search2turn1search25

**Push**  
GitHub docs beskriver `git push` som en kommando, hvor du typisk angiver remote-navn (`origin`) og branch (`main`). citeturn10search3turn5search0

Første push (typisk) ser sådan ud:

```bash
git push -u origin main
```

### Login til GitHub uden at blive sindssyg

GitHub har fjernet password-baseret autentificering til Git-operations; du bruger typisk **Personal Access Token (PAT)** over HTTPS eller en **SSH key**. citeturn0search7turn0search3turn0search11

**PAT (HTTPS)**
- GitHub siger direkte, at en personal access token kan bruges i stedet for password i CLI. citeturn0search3
- De anbefaler at behandle tokens som passwords og bruge udløbsdato. citeturn0search3

**SSH**
- GitHub har en officiel guide til at forbinde med SSH (generér key, tilføj til konto, test forbindelsen). citeturn0search11

**Credential helpers (anbefalet hvis du vil have det simpelt)**  
GitHub anbefaler GitHub CLI eller Git Credential Manager for at cache credentials ved HTTPS. citeturn6search3turn6search6  
Git Credential Manager beskrives som en sikker, cross-platform credential helper med støtte for bl.a. GitHub. citeturn6search2turn6search7

## .gitignore og repo-hygiejne

### Hvad er .gitignore (og hvad er det ikke)?

En `.gitignore` fortæller Git hvilke **intentionelt utrackede** filer Git skal ignorere. Filer der allerede er tracked påvirkes ikke af `.gitignore`. citeturn2view0

Hvis du *allerede har committet* noget, og nu vil ignorere det, skal du fjerne det fra index (uden at slette filen lokalt) med `git rm --cached`. Det står både i gitignore-dokumentationen og i Git’s cheat sheet. citeturn2view0turn4search17

### Hvor kommer ignore-regler fra?

Git docs beskriver, at ignore-patterns kan komme fra flere kilder (bl.a. `.gitignore` i mapper, `$GIT_DIR/info/exclude`, og en global fil via `core.excludesFile`), med en prioriteringsrækkefølge. citeturn2view0

Det giver dig en universal opskrift:

- Ting *alle* på projektet skal ignorere → commit i repoets `.gitignore` citeturn2view0turn4search19  
- Ting kun *du* skal ignorere i lige netop dette repo → `.git/info/exclude` citeturn2view0  
- Ting du vil ignorere i *alle* dine repos (fx editor-backup-filer) → global ignore via `core.excludesFile` citeturn2view0  

**Fun fact:** Git’s docs nævner default placering for global ignore via XDG (`~/.config/git/ignore`), hvis du ikke sætter noget andet. citeturn2view0

### Hvordan finder jeg ud af hvorfor noget bliver ignoreret?

Brug `git check-ignore` til at debugge ignore-systemet; den er lavet til præcis det. citeturn0search25

### Hvad “skal” stå i en .gitignore?

Det afhænger af stack og tooling, men der er nogle klassikere:

- build artifacts og caches  
- lokale virtual environments  
- logs og runtime-output  
- editor/IDE-filer  
- secrets (.env osv.)

GitHub vedligeholder en stor samling `.gitignore`-templates (bl.a. en Python-template), og den er et godt udgangspunkt for “universal defaults”. citeturn4search4turn4search0

Hvis du bygger Python-projekter ofte, er “Python.gitignore” netop lavet til typiske caches og tooling (mypy, pytype, ruff osv.) — og du kan også tilføje editor-specifikke ignore-lister globalt. citeturn4search0turn2view0

### Store filer og Git LFS

Hvis du har store binære filer (video, dataset, osv.), er Git LFS en standard løsning: i stedet for at gemme selve filen i Git historikken, gemmes en pointer, og indholdet ligger i LFS storage. citeturn4search1turn4search9turn4search5

## Releases, versions og “første version” i dit repo

### Hvad en “version” bør betyde

Semantic Versioning (SemVer) er den mest udbredte, klare model: **MAJOR.MINOR.PATCH**, hvor major er breaking changes, minor er nye features bagudkompatibelt, patch er bugfixes bagudkompatibelt. citeturn11view0

SemVer har også to pointer, som er guld værd for din disciplin:

- **0.y.z** er “initial development”; ting kan ændre sig når som helst, og API bør ikke betragtes som stabil. citeturn11view0  
- Når en version er released, bør indholdet af den version ikke “ændres” (i praksis: du laver en ny version). citeturn11view0

### Git tags er dine “release-markører”

Git tags er lavet til at markere vigtige punkter i historikken, typisk releases. citeturn13view0  
Git docs skelner især mellem:

- **Lightweight tags**: bare en pointer til en commit citeturn13view0  
- **Annotated tags**: gemmes som objekter med tagger, dato, besked og kan signeres — og Pro Git anbefaler annotated tags til releases netop pga. metadata. citeturn13view0turn3search6  

Du kan også signere tags (GPG/SSH/S/MIME) hvis du på sigt vil have stærkere provenance. citeturn3search21turn3search6

### Pushing af tags er en klassisk fælde

Som standard skubber `git push` ikke dine tags til remote. Pro Git siger direkte, at du skal pushe tags eksplicit (fx `git push origin <tagname>`), og forklarer også `--tags` og `--follow-tags`. citeturn14view0turn10search17

### Din “første release” opskrift

Her er den simplest mulige opskrift på at erklære “første version” (og gøre den reproducerbar):

1) Sørg for at `main` bygger/kører (eller i det mindste “starter”) og at `CHANGELOG.md` matcher det du vil kalde versionen.  
2) Commit changelog-opdateringen sammen med eventuelle sidste små rettelser.  
3) Lav en annotated tag på *den commit*.  
4) Push branch og tag til remote.

Eksempel:

```bash
# på main
git status
git add -A
git commit -m "chore: release prep"

# vælg et versionsnavn
git tag -a v0.1.0 -m "First tagged baseline"
# eller v1.0.0 hvis du mener API/brug er “stabilt”
```

Bemærk: SemVer siger, at “v1.2.3” ofte bruges som tag-navn, men at SemVer-versionen egentlig er “1.2.3”. Det er helt normalt at bruge `v`-prefix i tags. citeturn11view0

Push:

```bash
git push -u origin main
git push origin v0.1.0
```

At tags ikke pushes automatisk, og at `git push origin <tagname>` er den konkrete løsning, står i Pro Git tagging-kapitlet. citeturn14view0

**Bonus-fælde du undgår ved at vide det:** Hvis du “checker en tag ud”, ender du i detached HEAD. Pro Git forklarer både advarslen og hvordan du laver en branch ud fra en tag, hvis du vil fortsætte arbejde derfra. citeturn14view0

### Et workflow der passer til dit “modulære base”-mål

Hvis du vil bygge modulært og branche i mange retninger senere, så er et noob-robust workflow typisk:

- `main` er baseline (og helst altid nogenlunde kørende) citeturn1search8turn1search19  
- arbejde sker i feature-branches  
- merges tilbage til `main` i små bidder  
- releases markeres med **annotated tags**  
- versionsnummer følger SemVer (selv hvis du starter i 0.y.z) citeturn11view0turn13view0  

Hvis du senere vil automatisere changelog/versionsbump, er “Conventional Commits” en specifikation til commit-beskeder, netop for at gøre historikken maskinlæsbar og spille sammen med SemVer. citeturn7search1turn11view0