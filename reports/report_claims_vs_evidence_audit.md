# Report claims versus evidence (Pass 3)

Every numeric claim below was **recomputed from the files in this tree**.
A claim is VERIFIED only where the recomputed value equals the claimed value.

- verified: **33**
- mismatches: **0**
- not statically verifiable: **4**

| source | claim | claimed | recomputed | verdict |
|---|---|---|---|---|
| corpus/manifest.json | total_paragraphs | 74348 | 74348 | VERIFIED |
| corpus/manifest.json | total_entries | 2312 | 2312 | VERIFIED |
| corpus/manifest.json | speaker_layer.total_segments | 65107 | 65107 | VERIFIED |
| corpus/manifest.json | speaker_layer.jesus | 59007 | 59007 | VERIFIED |
| README.md | paragraph count | True | True | VERIFIED |
| README.md | entry count | True | True | VERIFIED |
| README.md | speaker segment count | True | True | VERIFIED |
| corpus/manifest.json | display_flow_layer.groups | 11498 | 11498 | VERIFIED |
| corpus/manifest.json | display_flow_layer.members | 35085 | 35085 | VERIFIED |
| corpus/manifest.json | display_flow_layer.boundaries | 23587 | 23587 | VERIFIED |
| reports/display_flow_members.csv | row count | 35085 | 35085 | VERIFIED |
| corpus/manifest.json | display_transform_layer.total_operations | 25193 | 25193 | VERIFIED |
| corpus/manifest.json | display_transform_layer.app_derived_section_markers | 1054 | 1054 | VERIFIED |
| corpus/manifest.json | display_transform_layer.handoff_operations | 24139 | 24139 | VERIFIED |
| display layer | every source_token matches canonical text | 0 | 0 | VERIFIED |
| reports/approved_display_suppressions.csv | row count | 24900 | 24900 | VERIFIED |
| reports/paragraph_local_vs_flow_level_run_counts.json | paragraph_local_styled_runs | 57966 | 57966 | VERIFIED |
| reports/paragraph_local_vs_flow_level_run_counts.json | approved_cross_fragment_run_links | 20467 | 20467 | VERIFIED |
| reports/paragraph_local_vs_flow_level_run_counts.json | flow_level_displayed_styled_runs | 37499 | 37499 | VERIFIED |
| corpus/manifest.json | reader_architecture.paragraph_local_styled_runs | 57966 | 57966 | VERIFIED |
| corpus/manifest.json | reader_architecture.cross_fragment_run_links | 20467 | 20467 | VERIFIED |
| reports/cross_fragment_speech_run_links.csv | row count | 20467 | 20467 | VERIFIED |
| reports/render_model_character_reconstruction.csv | reconstruction_failures | 0 | 0 | VERIFIED |
| display layer | canonical text recoverable from atom ranges | 0 | 0 | VERIFIED |
| corpus data | paragraph fingerprint mismatches | 0 | 0 | VERIFIED |
| package | canonical corpus DATA files changed vs baseline | 0 | 0 | VERIFIED |
| metadata/package_manifest.json | canonical_corpus_mutations | 0 | 0 | VERIFIED |
| version lockstep | sw.js cache key matches index.html | ldc-v2.11.0-R1B | ldc-v2.11.0-R1B | VERIFIED |
| version lockstep | corpus/manifest.json app_version | v2.11.0-R1B | v2.11.0-R1B | VERIFIED |
| version lockstep | package_manifest app_version | v2.11.0-R1B | v2.11.0-R1B | VERIFIED |
| version lockstep | README title version | True | True | VERIFIED |
| metadata/package_manifest.json | release_pass_issued is False | False | False | VERIFIED |
| corpus/manifest.json | status says NOT_DEPLOYED | True | True | VERIFIED |
| reports/highlight_note_anchor_regression.csv | interaction matrix results | - | - | NOT_STATICALLY_VERIFIABLE |
| reports/user_data_migration_regression.csv | user-data migration fixtures | - | - | NOT_STATICALLY_VERIFIABLE |
| reports/render_visible_text_integrity.csv | rendered visible text equals the display projection | - | - | NOT_STATICALLY_VERIFIABLE |
| README.md / package_manifest.json | physical-device validation | - | - | NOT_STATICALLY_VERIFIABLE |

## Claims that cannot be settled from files alone

- **reports/highlight_note_anchor_regression.csv** — interaction matrix results: requires a live DOM; executed in-browser against the served package and recorded in the Stage F evidence, not recomputable from files alone
- **reports/user_data_migration_regression.csv** — user-data migration fixtures: requires IndexedDB; executed in-browser with synthetic fixtures. Real user data cannot be proven without an exported live database
- **reports/render_visible_text_integrity.csv** — rendered visible text equals the display projection: requires a DOM renderer; executed in-browser over all 74,348 paragraphs
- **README.md / package_manifest.json** — physical-device validation: no iPad/iPhone Safari run has been performed