# Security Policy

6SNT.ADIF-HUB is a local-first tool for processing radio log data. Logs can
contain personal operating history, station details, comments, locations and
private paths.

## Sensitive Data

Do not publish or attach real logs, full ADIF exports, SQLite databases,
screenshots with private callsign data, credentials, cookies, API keys or local
station configuration.

For public issues and pull requests, use only small sanitized fixtures under
`backend/tests/fixtures` or clearly fictional examples under `sample_logs`.

## Reporting Sensitive Problems

If a problem involves private logbook data or a security concern, do not open a
public issue with the data attached. Report only the minimal technical
description needed to reproduce the issue, and keep the private file local until
the maintainer asks for a sanitized sample.

## Supported Scope

This project does not control radios, PTT, TUNE, TX audio or unattended
transmission. If radio-control features are added in the future, they must be
reviewed under the 6SNT radio safety rules before release.

