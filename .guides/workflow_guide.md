# Software project documentation workflow for solo Python developers and AI agents

**The most impactful thing a solo developer can do to level up their project is adopt a small set of widely-used documentation standards — Keep a Changelog, Semantic Versioning, Conventional Commits, and GitHub Flow — and enforce them through CLAUDE.md/AGENTS.md files that both humans and AI coding agents read.** These standards are battle-tested across thousands of open-source projects and, when used together, form an interlocking system: conventional commits feed the changelog, the changelog mirrors git tags, and tags drive the release process. What follows is a practical, example-heavy guide to each of these disciplines, tuned specifically for a solo developer working with AI coding agents on a small Python project.

---

## 1. Changelog discipline: write for humans, not machines

The **Keep a Changelog** format (v1.1.0) is the dominant standard. The file is named `CHANGELOG.md`, lives at the project root, and follows this structure:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `--verbose` flag for CLI output

## [0.3.0] - 2026-04-10

### Added
- CSV export via `export_to_csv()` function

### Fixed
- Crash when input file is empty (#42)

## [0.2.0] - 2026-03-20

### Changed
- Default timeout increased from 30s to 60s

[Unreleased]: https://github.com/user/repo/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/user/repo/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/user/repo/releases/tag/v0.2.0
```

The **`[Unreleased]` section** is the staging area. Changes accumulate here during development. At release time, you rename it to a versioned section with today's date, create a fresh empty `[Unreleased]` above it, and update the comparison links at the bottom. The version header omits the `v` prefix (`[0.3.0]`), while git tags and links use it (`v0.3.0`).

**The six categories** each serve a distinct purpose. **Added** is for new features (`add CSV export for user reports`). **Changed** is for modifications to existing behavior (`process_data() now returns a dataclass instead of a dict`). **Fixed** is for bug fixes (`corrected off-by-one error in pagination`). **Deprecated** signals upcoming removals (`load_from_file() deprecated; use load() instead — removal in 2.0.0`). **Removed** confirms deletions (`dropped Python 3.8 support`). **Security** flags vulnerability patches (`updated requests to 2.31.0 to patch CVE-2023-32681`). Only include categories that have entries — omit empty ones.

**Update frequency** matters. Per-commit updates generate noise; batch-at-release-time risks forgetting things. The practical middle ground: **update `[Unreleased]` whenever you complete a meaningful unit of work** (a feature, a bug fix, the end of a coding session), then polish the language at release time. This ensures nothing is forgotten while keeping entries readable. The Common Changelog project argues for writing entries only at release time with a "bird's-eye view," but for projects with AI agents doing work across sessions, accumulating entries as you go prevents information loss.

**When the file gets long**, don't split prematurely. A single `CHANGELOG.md` works well up to roughly **500–1,000 lines**. When it exceeds that, the most practical approach for a small project is to archive older entries to `CHANGELOG-archive.md` with a note at the top of the main file: `> For changes before v2.0, see [CHANGELOG-archive.md](CHANGELOG-archive.md)`. Larger projects use per-version files (Symfony uses `CHANGELOG-8.0.md`, `CHANGELOG-7.2.md`) or per-release doc pages (Django puts individual files in `docs/releases/`). FastAPI takes the opposite extreme — a single massive auto-generated file with thousands of entries. For a small project, the archive-file approach hits the right balance of simplicity and cleanliness.

---

## 2. Semantic versioning and the 0.x question

Semantic Versioning (SemVer 2.0.0) uses the format **`MAJOR.MINOR.PATCH`**. The rules are straightforward: increment **PATCH** for backward-compatible bug fixes, **MINOR** for new backward-compatible features (resetting PATCH to 0), and **MAJOR** for any backward-incompatible change (resetting MINOR and PATCH to 0).

For a Python project, concrete examples clarify the boundaries:

| What happened | Bump | Example |
|---|---|---|
| Fixed a bug in `parse_config()` | PATCH: 0.2.3 → 0.2.4 | Existing code unaffected |
| Added new `export_csv()` function | MINOR: 0.2.3 → 0.3.0 | New capability, nothing breaks |
| Added optional parameter with default | MINOR: 0.2.3 → 0.3.0 | Default preserves compatibility |
| Renamed module `utils` → `helpers` | MAJOR: 0.2.3 → 1.0.0 | Existing `import mylib.utils` breaks |
| Removed deprecated function | MAJOR | Code using that function breaks |
| Dropped Python 3.9 support | MAJOR | Breaking for 3.9 users |

**The 0.x pre-stable period** has special rules. The SemVer spec states: "Major version zero is for initial development. Anything may change at any time." In practice, a de facto convention has emerged: during 0.x, **MINOR bumps may contain breaking changes** (0.2.0 → 0.3.0 might break things), while **PATCH bumps should be safe** (0.2.0 → 0.2.1 is just a bug fix). The "left-most non-zero digit" effectively acts as the major version — so in `0.3.1`, the `3` functions like a major version number.

Start your project at **`0.1.0`**, not `0.0.1`. Your first release contains features, not just bug fixes. Move to **1.0.0** when three conditions are met: the public API is defined and you know what you're exposing, someone (including yourself) uses it in production, and you're ready to commit to not breaking things without a major bump. A common anti-pattern is staying on 0.x forever out of fear — if the interface is settled, ship 1.0.0.

**Git tags should be annotated** (not lightweight) and use the `v` prefix. Annotated tags store the tagger name, email, date, and message, and are recognized by `git describe` and tools like `setuptools-scm`. The commands:

```bash
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0
```

The changelog and tags form a **1:1 mapping**: every `## [0.3.0] - 2026-04-10` heading in the changelog corresponds to a `v0.3.0` git tag, and the comparison links at the bottom use these tag names to generate diff URLs.

---

## 3. Commit message discipline ties everything together

The **Conventional Commits** specification (v1.0.0) structures every commit message as `<type>[optional scope]: <description>`, with an optional body and footer separated by blank lines. This format directly maps to SemVer: `feat:` correlates with MINOR, `fix:` with PATCH, and `BREAKING CHANGE:` in the footer (or `!` after the type) with MAJOR.

**The type hierarchy**, from the widely-adopted Angular convention, follows a clear decision tree. Ask: does it change what the user sees or the API? Then it's `feat` or `fix`. Does it restructure code without changing behavior? `refactor`. Improve performance specifically? `perf`. Only touch tests? `test`. Only touch docs? `docs`. Affect build tooling or dependencies? `build`. Affect CI? `ci`. Everything else is `chore`.

Here are concrete examples for a Python project:

```
feat: add CSV export for user reports
feat(api): add pagination to /users endpoint
fix: prevent division by zero in calculate_average
fix(auth): handle expired JWT tokens gracefully
docs: add installation instructions for uv
refactor: extract database connection logic into pool
perf: use dict comprehension for config parsing
test: add unit tests for CSV export edge cases
build: upgrade pydantic from v1 to v2
ci: add Python 3.12 to test matrix
chore: update .gitignore to exclude .venv
feat(api)!: change response format to paginated object

BREAKING CHANGE: GET /users now returns {items, total, page}
instead of a plain list.
```

**The 50/72 rule** governs formatting: keep the subject line under **50 characters** (72 is the hard limit), wrap the body at **72 characters**, and always use imperative mood ("add feature" not "added feature"). With conventional commits, the type prefix counts toward the 50 characters, so descriptions need to be concise.

The body explains **what and why**, not how — the diff shows how. Reference issues with `Closes #42` or `Fixes #156` in the footer.

**The relationship between commits and changelog entries** is central. Only `feat` and `fix` commits typically appear in the changelog; `docs`, `refactor`, `test`, `build`, `ci`, `style`, and `chore` are usually hidden from users. Tools like **python-semantic-release** and **commitizen** can auto-generate changelogs from conventional commits, but **auto-generated changelogs are no substitute for hand-crafted ones**. Commit messages serve developers; changelogs serve users. The best workflow is to use conventional commits as raw material, then write human-friendly changelog entries that explain *why it matters*.

For enforcement, **commitizen** (`pip install commitizen`) is the most popular Python tool — it provides an interactive commit wizard (`cz commit`), a linter (`cz check`), version bumping (`cz bump`), and changelog generation (`cz changelog`). The **conventional-pre-commit** hook can validate messages automatically in a `.pre-commit-config.yaml`.

---

## 4. Branching strategy: keep it simple

For a solo developer with AI agents, **GitHub Flow** (or simplified trunk-based development) is the right choice. Git Flow — with its `develop`, `release/*`, and `hotfix/*` branches — is designed for large teams managing multiple parallel releases and adds unnecessary overhead for small projects.

GitHub Flow has one rule: **`main` is always deployable**. All work happens on short-lived feature branches that merge back via pull request. The full workflow:

```bash
git checkout main && git pull
git checkout -b feat/add-csv-export
# ... work, commit ...
git push -u origin feat/add-csv-export
gh pr create --fill
# After CI passes:
gh pr merge --squash --delete-branch
```

**When to branch vs. commit directly to main**: branch for anything that takes more than a trivial edit, any work done by an AI agent, or any change you'd want CI to validate before merging. Commit directly to main only for truly atomic fixes — a typo in docs, a one-line config change. The DORA research confirms that teams with three or fewer active branches and daily trunk merges achieve the highest delivery performance.

**Branch naming** follows the pattern `<type>/<short-description-in-kebab-case>`:

- `feat/add-csv-export`
- `fix/prevent-division-by-zero`
- `docs/update-installation-guide`
- `refactor/extract-connection-pool`

Note the convention difference: branches use the full word `feature/` (though `feat/` is also common), while commits use the abbreviation `feat:`. With issue numbers, the pattern becomes `feat/42-add-csv-export`.

**For AI agents**, specify branch naming in CLAUDE.md and use **git worktrees** to isolate parallel agent work. Claude Code natively supports `claude --worktree feat/add-validation`, which creates an isolated working directory on its own branch. This prevents the most common multi-agent failure mode: two agents editing the same files simultaneously.

---

## 5. Roadmap discipline keeps the project focused

A `ROADMAP.md` file works best when structured by **priority level** rather than dates, because solo projects rarely hit fixed deadlines. The practical format:

```markdown
# Roadmap

## Progress Convention
- `[ ]` Todo  |  `[-]` In Progress  |  `[x]` Done  |  `[!]` Blocked

## High Priority
- [-] **Input validation** — Add CLI argument validation 🏗️
- [ ] **Error messages** — Improve error output for common failures

## Medium Priority
- [ ] **Config file support** — Load settings from .toml file
- [ ] **Async processing** — Convert core pipeline to async

## Low Priority / Ideas
- [ ] **Plugin system** — Allow user-defined processors
- [ ] **Web dashboard** — Visualization for processing results

## Recently Completed
- [x] **CSV export** — Export results to CSV ✅ 2026-04-08
- [x] **Python 3.13 support** — Test and certify ✅ 2026-03-25
```

The **Active vs. Backlog** distinction maps naturally to priority sections: High Priority items are your active roadmap (3–5 items maximum), Medium Priority is the groomed backlog, and Low Priority/Ideas is the icebox. Move items up when you complete active work and have capacity, when a blocking dependency resolves, or when external factors change priority.

**Completed milestones** should live in a "Recently Completed" section (keep **5–10 items** for motivation and context), then get periodically archived to `docs/roadmap-archive.md`. Delete roadmap items that are abandoned — git history preserves them if you need them later.

**Status conventions** that work in plain Markdown: `[ ]` for todo, `[-]` for in progress, `[x]` for done, and either `[!]` or 🚫 for blocked. Add dates to in-progress and completed items for tracking. For deferred items, use `[~]` or the ⏸️ emoji with a reason.

The ROADMAP.md is preferable to GitHub Issues or Projects for AI agent workflows because **agents can read and edit it as a plain text file** without API calls. The roadmap can reference issues when needed: `- [ ] Fix auth bug (#42)`.

---

## 6. File length management and archiving strategies

Documentation files have practical length thresholds. **Under 300 lines** is ideal for any single file. **300–500 lines** warrants adding a table of contents or collapsible sections. **500–1,000 lines** means you should consider splitting. **Over 1,000 lines** strongly warrants archiving or restructuring.

The recommended archiving approach for each file type:

**CHANGELOG.md**: Keep current and recent versions (2–3 major versions) in the main file. Move older entries to `CHANGELOG-archive.md` with a reference at the top: `> For changes before v2.0, see [CHANGELOG-archive.md](CHANGELOG-archive.md)`. If the project grows substantially, adopt Symfony's pattern of per-version files (`CHANGELOG-1.x.md`, `CHANGELOG-2.x.md`).

**ROADMAP.md**: Keep the active roadmap under **100–150 lines**. Periodically move completed items older than a month or two to `docs/roadmap-archive.md`. Delete abandoned items.

**CLAUDE.md / AGENTS.md**: Keep under **200 lines** (HumanLayer's production CLAUDE.md is under 60 lines). Use **progressive disclosure** — reference separate docs files rather than inlining everything: `### API Architecture — @docs/api-architecture.md / Read when: Adding or modifying API endpoints`.

For GitHub-rendered Markdown, **collapsible sections** keep long content accessible without visual clutter:

```markdown
<details>
<summary>v1.x Changes (archived)</summary>

### [1.2.0] - 2025-01-15
- Added feature X
</details>
```

The governing principle: **main files stay focused and scannable; history lives in archive files; git preserves everything**. Never delete history, just relocate it.

---

## 7. The release process in nine steps

At release time, a small Python project needs a clear, repeatable sequence. Here is the minimal process that covers everything:

1. **Ensure all tests pass**: `pytest` or `uv run pytest -v`
2. **Review `[Unreleased]`** in CHANGELOG.md — polish entries for clarity
3. **Move `[Unreleased]` content** to a new `## [X.Y.Z] - YYYY-MM-DD` section; create a fresh empty `[Unreleased]` above it; update comparison links at the bottom
4. **Update version** in `pyproject.toml` (the single source of truth)
5. **Commit**: `git commit -am "chore: release v0.3.0"`
6. **Tag**: `git tag -a v0.3.0 -m "Release v0.3.0"`
7. **Push**: `git push origin main && git push origin v0.3.0`
8. **Create GitHub Release** (optional but recommended): `gh release create v0.3.0 --title "v0.3.0" --notes "See CHANGELOG.md"`
9. **Publish to PyPI** (if applicable): `python -m build && twine upload dist/*`

**GitHub Releases vs. git tags**: a git tag is the fundamental, portable version marker stored in the repository. A GitHub Release is a platform feature built on top of tags that adds rich markdown notes, binary asset attachments, visibility in user feeds, and RSS notifications. For anything user-facing, create both. GitHub's auto-generated release notes (from PR titles) can supplement your hand-written changelog.

**For `__version__` in Python**, the modern best practice is to **not hardcode it**. Use `importlib.metadata`:

```python
# src/mypackage/__init__.py
from importlib.metadata import version
__version__ = version(__package__)
```

This reads the version from installed package metadata (sourced from `pyproject.toml`), so you maintain the version number in exactly one place.

---

## 8. Multi-agent documentation discipline is the new frontier

When multiple AI agents (Claude Code, Codex, Cursor) work on the same project, coordination becomes the bottleneck. The emerging conventions center on three ideas: **agent instruction files, the single-writer rule, and session handoffs**.

**CLAUDE.md** is Claude Code's project-specific instruction file, read at the start of every conversation. **AGENTS.md** is the cross-tool open standard (now under the Linux Foundation's Agentic AI Foundation, adopted by **60,000+ repositories**), read by Codex, Jules, Cursor, Factory, and others. If you use multiple tools, maintain an AGENTS.md and symlink it: `ln -s AGENTS.md CLAUDE.md`. A well-structured instruction file looks like:

```markdown
# Project Name
Python CLI tool for data processing. Uses uv for package management.

## Commands
- Install: `uv sync`
- Test: `uv run pytest -v`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## Git Workflow
- Conventional Commits: feat:, fix:, docs:, refactor:, test:, chore:
- Branch naming: feat/<description>, fix/<description>
- Keep subject lines under 72 characters, imperative mood
- Run tests before committing

## Documentation Requirements
- Update CHANGELOG.md [Unreleased] section after completing any feature or fix
- Update ROADMAP.md status when starting or finishing roadmap items

## Code Conventions
- Python 3.11+, type hints everywhere
- Use dataclasses or Pydantic models
- Follow existing patterns in the codebase
```

**Critical guidance for these files**: keep them under 200 lines, hand-craft them (ETH Zurich research found LLM-generated context files *reduced* task success by ~3% while increasing costs 20%+), prefer pointers over inline content, and prune ruthlessly — if an agent already does something correctly without the instruction, delete it.

**The single-writer rule** — borrowed from distributed systems — means **one file, one owner; never let two agents edit the same file**. Addy Osmani (Google) puts it bluntly: "Conflicts kill velocity." In practice, this means partitioning work so each agent owns specific directories or files. For shared files like CHANGELOG.md, designate one agent (or the human) as the sole updater. Claude Code's Agent Teams feature enforces this via file locking; for manual workflows, scope each agent session to specific directories in CLAUDE.md.

**Git worktrees** are the primary isolation mechanism for parallel agent work. Each worktree is a separate working directory with its own branch: `claude --worktree feat/add-validation` creates an isolated environment. This prevents merge conflicts at the filesystem level.

**Attribution conventions** are settling into a standard. Claude Code automatically appends `Co-Authored-By: Claude <noreply@anthropic.com>` to commits. The emerging three-tier convention: use **Assisted-by** for minor AI involvement (suggestions, completions), **Co-authored-by** for substantial collaboration, and **Generated-by** for majority AI-generated code. The practical approach: leave Claude Code's default attribution on, and add `--author="AI <ai@example.com>"` for agents that don't self-attribute.

**Session handoffs** solve the cold-start problem — every new AI session has no memory of the last. The proven pattern uses two files: CLAUDE.md for permanent project context and **HANDOVER.md** for session narrative. The handoff document must include what was completed, what remains, **what approaches failed and why** (this alone saves hours), key decisions with rationale, and concrete next steps. Failed approaches are mandatory — "Tried passport.js, it conflicted with our Express middleware; switched to oauth4webapi" prevents the next session from repeating dead ends.

---

## Conclusion: the interlocking system

These eight disciplines form a single coherent workflow, not isolated practices. **Conventional commits** feed the **changelog** with structured entries. The changelog's versioned sections mirror **semantic version** numbers. Those versions correspond 1:1 to **annotated git tags**. Tags trigger the **release process**, which updates `pyproject.toml` and CHANGELOG.md. The **roadmap** tracks what's coming; the **branching strategy** isolates work in progress. And **CLAUDE.md/AGENTS.md** encode all of these conventions so AI agents follow the same rules as the human developer.

For a solo developer adopting this level of discipline for the first time, the priority order is: start with Conventional Commits and a CHANGELOG.md (immediate, high-impact habits), add CLAUDE.md with your project conventions (makes every AI session productive from the first prompt), adopt semantic versioning and a release checklist (brings professionalism to shipping), then layer on roadmap discipline and file maintenance as the project grows. The goal is not bureaucratic overhead — it's a system where **every piece of documentation earns its keep by making the next coding session, human or AI, faster and less error-prone**.