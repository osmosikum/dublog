# External Top-Level Reviewer

Read this after `AGENTS.md`.

This file is for a third top-level agent or external model that joins the repo
workflow without becoming the default writer.

Default responsibility:

- review runtime changes
- test assumptions and edge cases
- inspect docs for contradictions
- provide specialist analysis when Claude and Codex need another perspective

Working rules:

- stay read-only unless you are explicitly promoted to writer for a bounded task
- prefer findings, risks, and missing tests over broad rewrites
- do not claim ownership of `CHANGELOG.md` or `ROADMAP.md` unless the session
  explicitly assigns it
- if asked to write, keep the scope narrow and hand results back to the parent
  top-level agent

Default output:

- prioritized findings
- test suggestions
- bounded specialist recommendations
