"""Verify casebook record coverage against the raw Hayabusa export."""

from pathlib import Path
import sys
from collections import Counter
from casebook import read_rows, sessions, report

rows = list(read_rows(Path(sys.argv[1])))
groups = sessions(rows)
raw = Counter(str(r.get("RecordID") or r["EventRecordID"]) for r in rows)
indexed = Counter(r[1] for events in groups.values() for r in events)
print(
    dict(
        raw_rows=len(rows),
        groups=len(groups),
        missing_records=sum((raw - indexed).values()),
        extra_records=sum((indexed - raw).values()),
        html_bytes=len(report(groups, {}).encode()),
    )
)
