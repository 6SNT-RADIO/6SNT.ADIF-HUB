# Post templates EN

## Discovery

I am working on a local tool to clean and consolidate ham radio logs before uploading to platforms like LoTW/eQSL/ClubLog. Which format causes you the most trouble today: ADIF, Cabrillo, CSV, Excel or something else?

## ADIF explanation

ADIF is a strong interchange format, but many problems happen before export: incomplete columns, duplicates, time differences and mixed sources. I am testing a local review flow before upload.

## Cabrillo

Cabrillo logs are great for contests, but reusing them as general logs can be hard because exchanges vary by contest. I am validating a local mapper to ADIF with manual review.

## Excel/CSV

Many operators keep historical QSOs in Excel or CSV. The hard part is not opening the file, but mapping columns and avoiding duplicates before exporting ADIF.

## Closed beta invite

I am looking for a small number of operators for a closed beta of a local ADIF cleanup app. I do not need public real logs: feedback is enough, and if there is a bug, a minimal sanitized case helps.

## Deduplication demo

Technical demo: import, normalize, detect likely duplicates and resolve conflicts before exporting `ADI`. The goal is not blind automation, but operator control.

## Release notes

New beta build: improvements in formats, mapper, deduplication and documentation. Known limitations are documented. Technical feedback welcome.

