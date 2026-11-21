# Technical design
Read UTF-8 CSV or one JSON object per line. Require RecordID, index by computer, source and logon ID, escape all HTML, and retain unassigned records.

Missing IDs fail explicitly. Logon IDs may recur after reboot and grouped evidence requires analyst review. Next add boot-boundary evidence.
