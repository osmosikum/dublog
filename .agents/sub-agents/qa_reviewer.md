# QA Reviewer Entry Point

This file is for bounded review or validation tasks.

Rules:

- default to read-only review
- focus on bugs, regressions, unsafe assumptions, and missing tests
- do not update `CHANGELOG.md`, `ROADMAP.md`, or role files
- keep findings concrete and tied to files or behaviors

Return format:

- prioritized findings
- residual risks
- any tests that should exist but do not
