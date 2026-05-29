# Contributing

Thanks for helping improve 6SNT.ADIF-HUB.

## Bugs

When reporting a bug, include:

- the app version or commit;
- operating system;
- input format involved (`ADI`, `ADX`, `Cabrillo`, `CSV`, `TSV`, `XLSX`,
  `JSON`);
- expected result;
- actual result;
- a small sanitized fixture when possible.

Do not attach real logs, full ADIF exports, private SQLite databases, screenshots
with sensitive data, credentials or station-private files.

## Improvements

Feature proposals should describe the operator workflow, the source format or
ADIF fields involved, and how the result should be validated. 6SNT.ADIF-HUB is
not a daily logger; keep proposals focused on local import, normalization,
deduplication, conflict review and export.

## Fixtures

Use only sanitized fixtures in `backend/tests/fixtures` or fictional files in
`sample_logs`. Keep ADIF field names and technical tokens in their standard
English form, for example `CALL`, `FREQ`, `MODE`, `BAND`, `QSO_DATE`,
`TIME_ON`, `LoTW`, `eQSL`, `POTA` and `SOTA`.

## Local Checks

Before opening a pull request, run the checks that are available for the area you
changed:

```powershell
cd backend
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\ruff check app tests
```

```powershell
cd frontend
npm run build
```

The frontend currently has no `lint` script.

