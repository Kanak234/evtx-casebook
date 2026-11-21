"""Build an offline session index from verbose Hayabusa timelines."""

import argparse
import csv
import html
import json
import re
from collections import defaultdict
from pathlib import Path


def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        if path.suffix.lower() == ".csv":
            yield from csv.DictReader(stream)
        else:
            yield from (json.loads(line) for line in stream if line.strip())


def sessions(rows):
    groups = defaultdict(list)
    for row in rows:
        # A record number is local to its source. Keep host, channel and file alongside it.
        record = str(row.get("RecordID") or row.get("EventRecordID") or "")
        if not record.isdecimal():
            raise ValueError("Export a Hayabusa verbose timeline containing RecordID")
        detail = row.get("Details", "")
        detail = (
            json.dumps(detail, ensure_ascii=False)
            if isinstance(detail, dict)
            else str(detail)
        )
        match = re.search(
            r'\b(?:TargetLogonId|TgtLogonId|LID|LogonId)["\s]*[:=]\s*"?((?:0x)?[0-9a-f]+)\b',
            detail,
            re.I,
        )
        host = str(row.get("Computer") or "")
        source = str(row.get("EvtxFile") or row.get("Channel") or "unspecified")
        # Unattributed records stay isolated. Host and source constrain the lifetime of a group.
        key = (
            host,
            source,
            match[1].lower() if host and match else "unassigned record " + record,
        )
        groups[key].append(
            (str(row.get("Timestamp", "")), record, str(row.get("EventID", "")), detail)
        )
    return groups


def report(groups, notes):
    esc = lambda value: html.escape(str(value))
    parts = [
        '<!doctype html><meta charset="utf-8"><title>EVTX Casebook</title><h1>EVTX Casebook</h1>'
    ]
    for (host, source, session), events in sorted(groups.items()):
        parts.append(
            f"<section><h2>{esc(host)} · {esc(session)}</h2><p>{esc(source)}</p><ol>"
        )
        for stamp, record, event, detail in sorted(events):
            citation = f"{host}|{source}|{record}"
            parts.append(
                f"<li><b>Record {esc(record)}</b> · {esc(stamp)} · Event {esc(event)}<pre>{esc(detail)}</pre>"
            )
            if citation in notes:
                parts.append(f"<p>Analyst note: {esc(notes[citation])}</p>")
            parts.append("</li>")
        parts.append("</ol></section>")
    return "".join(parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("timeline", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--notes", type=Path)
    args = parser.parse_args()
    notes = json.loads(args.notes.read_text(encoding="utf8")) if args.notes else {}
    args.output.write_text(
        report(sessions(read_rows(args.timeline)), notes), encoding="utf8"
    )
