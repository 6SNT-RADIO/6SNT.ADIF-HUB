# ADIF-HUB concepts

## Not a logger

The app is not designed for live operating and does not replace your main logger. It acts as a local hub for cleanup, consolidation and export.

## ADI and ADX

- `ADI`: plain-text ADIF with fields such as `<CALL:5>EA1AA`.
- `ADX`: XML ADIF, more structured and stricter about document shape.

## Cabrillo

`Cabrillo` is used for contests. It is useful for score submission, but exchanges vary by contest. The parser uses templates and may need additions for uncovered events.

## CSV, TSV, XLSX and JSON

These formats usually come from spreadsheets, custom exports or personal tools. They need mapping because column names are not always ADIF-compatible.

## Semantic deduplication

Two records can be the same QSO even if they are not byte-identical. The app compares key fields and time tolerance to find likely duplicates.

## ADIF 3.1.7

Normalization targets fields and conventions compatible with ADIF 3.1.7. Full coverage of every field and extension is not promised in beta.

