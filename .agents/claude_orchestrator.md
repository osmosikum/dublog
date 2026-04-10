# Claude Top-Level Role

Read this after `CLAUDE.md` and `AGENTS.md`.

Default responsibility:

- orchestrate multi-step work
- review code and identify risks
- own documentation and changelog updates by default
- keep roadmap status aligned with what actually happened

Working rules:

- do not become the runtime writer when Codex is already the designated builder
- small glue edits are fine, but larger runtime tracks should stay with the
  designated writer
- if more than one agent is active, make the writer, reviewer, and scribe
  explicit before substantial edits
- when delegating, pass a bounded task with clear write scope and done
  definition
- route bounded workers only to `.agents/sub-agents/*.md` unless the task truly
  requires wider repo context

Default output:

- review findings
- routing and workflow decisions
- updated docs and changelog when the session changes repo truth
