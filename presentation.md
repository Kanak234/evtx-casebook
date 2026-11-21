# Presentation — EVTX Casebook

1. I began with a public Hayabusa timeline in public.csv.
2. I preserved the host, source file and record number in casebook.py.
3. I grouped records with a logon ID and kept unattributed records separate.
4. I verified provenance and HTML escaping in test_casebook.py.
5. I compared the report with the source export using bench.py.

**Main limitation.** An identifier can recur after reboot. Group membership is a lead requiring analyst review.
