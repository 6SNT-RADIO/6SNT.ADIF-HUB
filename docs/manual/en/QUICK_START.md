# Quick start

6SNT.ADIF-HUB is a local app for cleaning, normalizing, deduplicating and exporting logs to ADIF. It is not a daily logger and does not replace LoTW, eQSL, ClubLog, QRZ, Log4OM, N1MM or other logging systems.

## Before you start

- Work with copies of your original logs.
- Do not share screenshots that expose sensitive records.
- Keep the original file unchanged outside the project folder.

## Fast flow

1. Open the app.
2. In `INGEST`, drag `ADI`, `ADX`, `CBR`, `CSV`, `TSV`, `XLSX` or `JSON` files.
3. Review the ingest queue and file warnings.
4. In `PROCESS`, adjust the mapper if a column was not detected.
5. Run `PROCESS_MAPPING`.
6. In `MERGE`, run `DEDUPE`.
7. Review open conflicts and choose a strategy: use existing, use incoming, merge, use newer or field selection.
8. In `EXPORT`, download the consolidated `ADI` file.
9. Review the result before uploading it to external platforms.

## Expected result

You get a clean ADIF file ready for review and downstream tools. The beta can have limitations with uncommon contests or custom formats, so manual review remains required.

