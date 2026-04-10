# Project control for `dublog`

This guide is the short, operative manual for how you manage this repo in
practice. It builds on `.guides/github_superguide.md`, but is written for this
specific project.

## What is the source of truth?

Use the documents like this:

- `README.md`: how the project runs and what it is
- `ROADMAP.md`: active work and next technical steps
- `CHANGELOG.md`: what has actually been changed
- `CLAUDE.md`: working rules for Claude Code
- `AGENTS.md`: working rules for Codex and other code agents
- `.guides/tri_agent_setup.md`: repo-specific routing baseline for top-level
  agents and bounded sub-agents
- `.agents/*.md`: top-level role entry points
- `.agents/sub-agents/*.md`: bounded worker entry points, not global truth
- `.guides/github_superguide.md`: general Git reference and explanations
- `.guides/project_control.md`: this file, i.e. the practical operational guide
  for the repo

If two documents say different things, they should be brought into sync
immediately.

## Standard for this repo

- `main` is the baseline branch
- `origin` is the GitHub remote for the repo
- local `main` tracks `origin/main`
- larger work happens in branches, not directly on `main`
- runtime data should not go in git
- documentation always runs alongside changes, not after
- `CHANGELOG.md` is updated on every real code, structure, or docs change

## Multi-agent baseline

If you use multiple agents on the same day, keep it simple:

- only one writer at a time on runtime code
- be explicit about who is builder, reviewer, and scribe
- top-level agents read the shared contract plus their `.agents/*.md` role file
- bounded sub-agents get only one `.agents/sub-agents/*.md` entry point unless
  the parent explicitly expands scope
- do not let two agents write in the same runtime track at the same time
- shared docs stay with the designated scribe unless deliberately delegated
- if workflow rules change, update `AGENTS.md`, `CLAUDE.md`, and the changelog
  in the same session

Practical standard right now:

- Claude Code = orchestrator, review, docs, and scribe
- Codex = builder and refactor
- third top-level agent = reviewer, tester, or specialist unless explicitly
  promoted to writer
- you = scope, priority, release, and kill switch

## What should not go in Git?

This repo should track source code, docs, and configuration decisions. It
should not track ongoing runtime output.

Ignored things in this repo:

- `projects/` - project data, memory, settings, and conversation logs from runs
- `identities/custom/` - local identities that the app loads but the repo
  should not track
- root-level user identities in `identities/` - ignored by default; use
  `custom/`
- `shared/` - legacy runtime logs in the repo root
- `agent_a/memory.md` and `agent_b/memory.md` - legacy runtime memory
- `__pycache__/`, virtual environments, and editor noise

If you want to save important output, export it deliberately to a documented
file, rather than letting it end up in the runtime directories.

Tracked identity files in the repo should only be:

- `identities/template.md`
- `identities/examples/*.md`
- documentation in `identities/`

## Rule for English migration

Language cleanup in this repo must not be treated as plain text replacement.

- engine text and operative docs can be translated directly
- persisted runtime values must not be renamed without compatibility
- `projects/**`, memory, and session logs must not be mass-translated
- example identities and template are a content track and must be decided
  explicitly
- the user's free text may remain in Danish or another language
- chat input, topics, and other free content fields must not be auto-translated
  as a side effect of the English pass

The concrete boundary is in `.guides/english_migration_scope.md`.

## Daily working rhythm

Use this rhythm as standard:

1. Start with `git status --short --branch`.
2. If there is a remote, run `git pull --ff-only` on the branch you are
   working on.
3. Read `ROADMAP.md` and `CHANGELOG.md` if you are continuing existing work.
4. Create a branch if the work is larger than a small docs or hotfix change.
5. If more than one agent is involved, make the writer and scribe explicit
   before substantial edits.
6. Implement the change.
7. Update docs in the same session:
   - `ROADMAP.md` if active work or status changes
   - `CHANGELOG.md` always on a real change
   - `CLAUDE.md`, `AGENTS.md`, or `.agents/*.md` if workflow rules shift
8. Review with `git diff`.
9. Stage and commit in coherent, logical chunks.

## Branching rule

Branch if at least one of these is true:

- the change is larger than a small text correction
- you are experimenting
- you could break something along the way
- you want to work in multiple tracks at the same time

Practical branch names:

- `feature/session-manager`
- `fix/sse-cleanup`
- `docs/git-baseline`
- `refactor/project-runtime`

If an agent creates the branch, `codex/...` or `claude/...` is also fine, but
the intent should still be clear.

## Commit standard

Keep commits small enough to make sense on their own. Use a simple
conventional-commit style:

- `feat: ...`
- `fix: ...`
- `docs: ...`
- `refactor: ...`
- `chore: ...`

Examples:

- `docs: add project control guide and git baseline`
- `feat: introduce session manager skeleton`
- `fix: keep SSE output tied to active session`

## What you should never do routinely

- do not use `git reset --hard` as standard cleanup
- do not force-push `main`
- do not commit the runtime directories just because they are new
- do not let `ROADMAP.md` and `CHANGELOG.md` fall behind the code
- do not write future architecture into docs as if it already exists

## Git setup for this repo

Current status:

- the repo is initialised locally
- default working branch is `main`
- `origin` points to `https://github.com/osmosikum/dublog.git`
- the first baseline has already been pushed, and `main` tracks `origin/main`

The repo should be initialised on `main`. If you want to push to GitHub later:

```bash
git remote add origin <REMOTE_URL>
git push -u origin main
```

Before commits work stably on a new machine, your Git identity must be set:

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

If you want to set the global default branch to `main` going forward:

```bash
git config --global init.defaultBranch main
```

## Versioning and release rule

Until the base is stable, `0.x` is a reasonable version track. When you want
to mark a baseline, use annotated tags:

```bash
git tag -a v0.1.0 -m "First baseline"
git push origin v0.1.0
```

The version number should match `CHANGELOG.md`.

## How code agents should be used

If you use a code agent in this repo, it must as a minimum:

- read relevant governance docs before larger work
- keep docs and code in sync in the same session
- update `CHANGELOG.md` on real changes
- keep active work in `ROADMAP.md`
- let parked ideas stay in `FUTURE_PATCHES.md`
- respect top-level versus bounded routing instead of giving every worker the
  whole repo context

This is not optional extra work. It is part of how the project is managed.
