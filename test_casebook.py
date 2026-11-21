import pytest
from pathlib import Path
from casebook import read_rows, report, sessions


def test_public_export_has_full_provenance():
    rows = list(read_rows(Path(__file__).with_name("public.csv")))
    groups = sessions(rows)
    # Each exported detection must retain the reference to its source event.
    expected = sorted((r["Computer"], r["EvtxFile"], r["RecordID"]) for r in rows)
    actual = sorted(
        (host, source, event[1])
        for (host, source, _), events in groups.items()
        for event in events
    )
    assert actual == expected and actual


def test_jsonl(tmp_path):
    path = tmp_path / "timeline.jsonl"
    path.write_text('{"Computer":"lab","RecordID":2,"Details":{"LogonId":"0x42"}}\n\n')
    assert list(sessions(read_rows(path)))[0][2] == "0x42"


def test_missing_record():
    with pytest.raises(ValueError):
        sessions([{}])


def test_empty():
    assert sessions([]) == {}


def test_group_and_escape():
    row = dict(
        RecordID="12", Computer="lab", Details="LID: 0xab <tag>", Channel="Security"
    )
    grouped = sessions([row, dict(row, RecordID="13"), dict(row, Computer="other")])
    assert len(grouped) == 2
    page = report(grouped, {"lab|Security|12": "<note>"})
    assert "&lt;note&gt;" in page and "<tag>" not in page and "Record 13" in page
