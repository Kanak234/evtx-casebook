# TRD — EVTX Casebook

## Stack
Python 3.11+ standard library only (csv, json, html, re). pytest is the only dev dependency. There is no network access at run time.

## Data flow
1. `read_rows(path)`: CSV via `csv.DictReader` (`utf-8-sig` strips Excel's BOM), anything else as JSONL, skipping blank lines.
2. `sessions(rows)`:
   - Require a decimal `RecordID` (or `EventRecordID`); otherwise raise.
   - Serialize `Details` (a dict for JSONL) to a string.
   - Extract a logon ID with the regex `TargetLogonId|TgtLogonId|LID|LogonId` and lowercase it.
   - Key = `(host, source, logon ID)`. If the host or the logon ID is missing, the key becomes `unassigned record <id>`, so the row never merges with others.
3. `report(groups, notes)`: sorted sections → sorted events, every field run through `html.escape`, with notes looked up by citation string.
4. `bench.py`: compares a `Counter` of raw record IDs with a `Counter` of indexed record IDs. That is multiset-exact, so a record matched by two rules counts twice on both sides.

## Key decisions
- **Scope by host and source.** A record number is only unique within one log file, and a logon ID only within one boot of one host.
- **Unassigned rows stay isolated**, so no false linkage is created.
- **No deduplication.** When two Hayabusa rules hit the same record (5315 in the sample), both rows are kept because they carry different rule titles.

## Security
All output is escaped, and the tests feed `<script>` through it. There is no shell-out and no network access.

## Limits and roadmap
Logon IDs can recur after a reboot. Next, add boot-boundary evidence (event 4608/6005) to split groups.
