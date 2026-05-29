# User guide

## What the app does

6SNT.ADIF-HUB takes scattered logs, converts them to a common representation, lets you review mapping, detects semantic duplicates and exports one consolidated `ADI`. The working database is local SQLite.

## Navigation

- `INGEST`: load files and inspect the queue.
- `PROCESS`: map columns and normalize records into ADIF fields.
- `MERGE`: detect duplicates and resolve conflicts.
- `EXPORT`: generate the final ADIF.

## Ingest

Drag one or more files into the drop zone. The app tries to detect format, record count, columns and an initial mapping. Review warnings before moving on.

## Mapper

The mapper connects source columns to ADIF fields such as `CALL`, `QSO_DATE`, `TIME_ON`, `BAND`, `FREQ` and `MODE`. If automapping is incomplete, select the correct field manually.

## Normalization

When the mapping is processed, the app applies cleanup rules: date/time shapes, known modes, band from frequency when enabled, Maidenhead data and contest fields when the parser recognizes them.

## Preview

The preview table shows up to 100 normalized rows. Use the top search to filter by callsign, date, time, band, frequency, mode or status.

## Deduplication

Deduplication compares QSOs with contextual rules. General contacts use callsign, band, mode and a time window. Contests prioritize `CONTEST_ID`. POTA/SOTA records can consider activity references when present.

## Conflicts

A conflict appears when two records probably represent the same QSO but contain relevant differences. Resolve with a global strategy or field-by-field choices.

## Export

When normalized QSOs exist, the `EXPORT` view downloads an `ADI` file. Open conflicts should not be merged without review.

