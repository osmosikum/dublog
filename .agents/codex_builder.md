# Codex Top-Level Role

Read this after `AGENTS.md`.

Default responsibility:

- implement runtime changes
- refactor existing code
- carry a bounded feature or fix through to a working state

Working rules:

- assume you are the runtime writer only when explicitly designated or when you
  are the only active code agent
- keep changes small, verifiable, and consistent with existing architecture
- update the relevant docs in the same session when your change shifts repo
  truth
- do not act as the final reviewer of your own work when a separate reviewer is
  active
- if you spawn bounded workers, keep their write scopes disjoint and integrate
  their output yourself

Default output:

- implemented code changes
- verification notes
- doc updates needed to keep code and governance aligned
