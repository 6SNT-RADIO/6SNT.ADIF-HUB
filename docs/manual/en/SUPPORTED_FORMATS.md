# Supported formats

## ADI

Basic support for text ADIF. Common fields and `APP_*` extensions can be preserved.

## ADX

Simple XML support. Full XSD validation is pending.

## Cabrillo

Supports `CONTEST:` header and several common templates. Contests with special columns may need new templates.

## CSV and TSV

Supported with column detection and mapper. Inconsistent delimiters or quoting may require cleanup first.

## XLSX

Supported through local spreadsheet reading. Empty sheets, unusual date serials or multiple tables per sheet can require manual preparation.

## JSON

Supports an array of objects or compatible root object. Invalid root shape is reported as an error.

## Known limitations

- Not every ADIF field is exposed in the UI.
- Deduplication is conservative, not infallible.
- The beta should not modify your only master log without backup.

