# Release checklist

Use this checklist before publishing a public release of 6SNT.ADIF-HUB.

## Repository hygiene

- [ ] Confirm the repository is public only when the release is ready.
- [ ] Confirm `README.md` explains the product in the first screen.
- [ ] Confirm `README.md` says the app is not a daily logger.
- [ ] Confirm `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md` and `CHANGELOG.md` exist.
- [ ] Confirm `docs/INDEX.md` links to user manuals and validation material.

## Private data check

- [ ] Do not commit real operator logs.
- [ ] Do not commit private ADIF, ADX, Cabrillo, CSV, TSV or spreadsheet exports.
- [ ] Do not commit SQLite databases, local runtime folders, tokens or `.env` files.
- [ ] Do not commit generated binaries or packaged archives.
- [ ] Use only fictional sample files and sanitized fixtures.

## Screenshots

- [ ] Check screenshots before release.
- [ ] Remove callsigns, names, paths, emails and real QSO data from screenshots.
- [ ] Use `assets/screenshots/adif-hub-en.png` and `assets/screenshots/adif-hub-es.png` as public screenshots.
- [ ] Do not use root `screen.png` as a public product screenshot.

## Build and validation

Backend:

```powershell
cd backend
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\ruff check app tests
```

Frontend:

```powershell
cd frontend
npm run build
```

Packaging:

```powershell
pwsh -File scripts\build_exe.ps1
```

## Release notes

- [ ] Update `CHANGELOG.md`.
- [ ] State clearly whether the release is beta, preview or stable.
- [ ] Mention known limitations.
- [ ] Remind users to work with copies of their logs.

## GitHub metadata

Suggested description:

```text
Local-first ADIF/Cabrillo log cleanup, deduplication and export tool for amateur radio operators.
```

Suggested topics:

```text
ham-radio, amateur-radio, adif, cabrillo, logbook, qso, lotw, eqsl, pota, sota, radio-tools, windows, local-first
```
