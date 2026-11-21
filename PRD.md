# PRD — EVTX Casebook

## Problem
Hayabusa turns Windows `.evtx` logs into a flat timeline. During an incident, an analyst then has to work out by hand which rows belong to the same logon session, and copy record IDs into notes so every claim can be traced back. That step is slow, and it is easy to drop or mis-cite a record.

## Users
- **Primary:** a student or junior DFIR analyst reviewing an exported timeline on an offline machine.
- **Secondary:** a reviewer who has to verify every statement against the source records.

## Goals
1. Group rows into sessions by host + source file/channel + logon ID.
2. Cite every record as `Computer|EvtxFile|RecordID`, and never lose or invent a record.
3. Let the analyst attach notes per record without editing the timeline.
4. Produce one self-contained HTML file that is safe to open (all values escaped).

## Non-goals
- Parsing raw `.evtx` (Hayabusa does that).
- Detection rules or alerting.
- Proving that a group is one real session. Logon IDs can repeat after a reboot, so a group is a lead.

## Features
| Feature | Behaviour |
|---|---|
| Input | Hayabusa verbose CSV, or JSONL (one object per line) |
| Grouping | `(Computer, EvtxFile or Channel, logon ID)`; rows without a logon ID get their own group |
| Citation | Record number plus host and source shown on every entry |
| Notes | Optional `--notes notes.json` keyed by `Computer|EvtxFile|RecordID` |
| Output | `case.html` |
| Verification | `bench.py` counts missing and extra records against the raw export |

## Acceptance criteria
- `python -m pytest -q` passes.
- `bench.py public.csv` reports `missing_records: 0` and `extra_records: 0`.
- A row without a numeric RecordID stops the run with a clear error.
- Any HTML in the input is escaped in the output.

## Open measurement
The timed human review protocol in README.md has not been run yet. No speed claim is made until it is.
