# Beta validation plan

## Goal

Validate whether 6SNT.ADIF-HUB helps real operators clean, deduplicate and export logs while keeping control of their data.

## Scope

Closed beta with 10 to 20 operators over 2 to 4 weeks. This document does not contact users and does not publish in communities.

## Entry criteria

- Local app installer or executable available.
- Minimum ES/EN documentation ready.
- Sanitized fixtures for internal tests.
- Clear backup warning.

## Success criteria

- Operators complete import, mapping, dedupe and export.
- Declared confidence is enough to review the generated ADI.
- Reproducible errors are documented with sanitized data.
- No uncontrolled privacy risks appear.

## Blocking criteria

- Corrupted ADIF export.
- Record loss without warning.
- Ambiguous conflict resolution.
- UI prevents review before export.
- Unsafe handling of real logs or SQLite databases.

## Metrics

- Formats tested.
- Approximate QSOs per batch.
- Time to first export.
- Number of conflicts and manual decisions.
- Confidence level from 1 to 5.
- Errors by area.

