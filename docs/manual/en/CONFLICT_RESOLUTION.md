# Conflict resolution

## Strategies

- `USE_EXISTING`: keep the record already in the local database.
- `USE_INCOMING`: replace content with the imported record.
- `MERGE`: fill empty fields, promote useful confirmations and combine comments when applicable.
- `USE_NEWER`: use the record that appears newer from available metadata.
- Field selection: the operator chooses incoming or existing value per displayed field.

## When to use each

Use existing when your master log is more trusted. Use incoming when the imported file is better curated. Use merge when both records add useful data. Use newer only when source timestamps are reliable. Use field selection for sensitive differences such as `RST_SENT`, `RST_RCVD`, `COMMENT`, POTA/SOTA references or contest data.

## Practical rule

If the QSO will be uploaded externally, manually review any conflict that changes contact identity: `CALL`, `QSO_DATE`, `TIME_ON`, `BAND`, `FREQ`, `MODE` or `CONTEST_ID`.

