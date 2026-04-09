# Identities

`identities/` er delt i tre lag:

- `template.md`: kanonisk skabelon til nye identiteter
- `examples/`: tracked eksempel-identiteter, som repoet shipper med
- `custom/`: lokale identiteter, som appen loader men git ignorerer

Praktisk regel:

- vil du have en delt baseline-identitet i repoet, saa laeg den i `examples/`
- vil du have en lokal eller projekt-specifik identitet, saa laeg den i `custom/`
- vil du bare starte fra bunden, saa kopier `template.md`

Loaderen understotter ogsaa root-level legacy-filer i `identities/`, men nye filer boer laegges i `custom/` eller `examples/`.
