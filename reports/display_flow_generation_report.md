# Display-flow generation report

| metric | value |
|---|---:|
| schema | ldc-display-flow-generation-report-v1 |
| corpus_version | G036-AFLP-R1B-UWR2 |
| paragraphs | 74348 |
| entries | 2312 |
| dash_joins_ledger | 23530 |
| dash_joins_predicted | 23530 |
| dash_only_predicted | 0 |
| dash_only_ledger | 0 |
| non_dash_candidates | 57 |
| non_dash_approved | 57 |
| cross_role_reviewed | 88 |
| flow_groups | 11498 |
| flow_members | 35085 |
| approved_pairs | 23587 |
| approved_pairs_placed | 23587 |
| paragraphs_in_two_groups | 0 |
| screenshot_cases_represented | 5 |

## Method

The runtime dash merger (classifyLists Pass 1) was independently reproduced on
CANONICAL text and compared against dash_merge_full_ledger.csv:
**23,530 predicted vs 23,530 in the ledger, exact set match, 0 divergences**.
Flow groups are then assembled from those approved joins plus the 57 reviewed
non-dash continuations. Canonical IDs, text, fingerprints and speaker offsets
are untouched: flow data is derived display metadata only.