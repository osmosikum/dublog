# Identities

`identities/` is split into three layers:

- `template.md`: canonical template for new identities
- `examples/`: tracked example identities shipped with the repo
- `custom/`: local identities that the app loads but git ignores

Practical rule:

- if you want a shared baseline identity in the repo, put it in `examples/`
- if you want a local or project-specific identity, put it in `custom/`
- if you just want to start from scratch, copy `template.md`

The loader also supports root-level legacy files in `identities/`, but new files should go in `custom/` or `examples/`.
