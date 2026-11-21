# Tested edge cases
- absent or non-numeric RecordID (fails explicitly)
- empty timelines
- host collisions (same logon ID on two hosts stays separate)
- unsafe HTML in Details (escaped)
- blank JSONL lines (skipped)
- public record provenance (citations match the source CSV)
- one record matched by two rules (both kept; multiset bench still exact)
