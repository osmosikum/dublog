# Claude Top-Level Role

Read this after `CLAUDE.md` and `AGENTS.md`.

## Default responsibility

- (example: [orchestrate multi-step work] )
- (example: review code and identify risks )
- (example: own documentation and changelog updates by default )
- (example: keep roadmap status aligned with what actually happened )

## Working rules

(example: - do not become the runtime writer when Codex is already the designated builder )
(example: - small glue edits are fine, but larger runtime tracks should stay with the )
  designated writer )
(example: - if more than one agent is active, make the writer, reviewer, and scribe
  explicit before substantial edits
(example: - when delegating, pass a bounded task with clear write scope and done
  definition )
(example: - route bounded workers only to `.agents/sub-agents/*.md` unless the task truly
  requires wider repo context )

## Default output

(example: - review findings )
(example: - routing and workflow decisions )
(example: - updated docs and changelog when the session changes repo truth )
