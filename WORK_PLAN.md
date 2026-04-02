# TOEFL Vocab Build Plan

## Current Audit

- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_08.tsv`
- Current ETS row count: 752
- File count mismatch:
  - `set_01`: 102 rows
  - `set_02`: 50 rows
- Exact-format validation: passed for all 8 existing files
- Current duplicate headwords across ETS files: 8
  - `commodity`, `cohort`, `disparity`, `enforce`, `mortality`, `prohibit`, `stratify`, `subsidy`

## Official-Source Direction To Preserve

- Use ETS official/public TOEFL pages and samples as the primary orientation for topic and register.
- Reflect the May 29, 2025 ETS announcement for January 2026 changes:
  - multistage adaptive Reading and Listening
  - more modern and equitable topics
  - stronger academic-life relevance such as group discussions and project work
- Avoid claiming any non-existent "ETS official 3000 word list."

## Build Sequence

1. Stabilize the current ETS base.
2. Lock an ETS-based candidate policy:
   - cross-disciplinary academic vocabulary first
   - very basic words removed
   - hyper-specialized terms excluded or pushed down
   - modern academic/campus/lecture contexts preferred
3. Generate ETS files in 100-card batches with duplicate checks after every batch.
4. Generate the AWL headword set separately by sublist order.
5. Emit metadata and review files:
   - `manifest.json`
   - `fields_spec.md`
   - `generation_notes.md`
   - `rejected_candidates.tsv`
   - `duplicates_removed.tsv`
6. Run final validation:
   - row counts
   - duplicate headwords
   - label completeness
   - literal `\n` count
   - empty file check

## Immediate Next Actions

1. Repair `set_01` and `set_02` counts without breaking priority order.
2. Regenerate or complete `set_09` and `set_10` using the same format.
3. Extend the generator workflow so sets `11` to `30` can be created reproducibly.
4. Build the AWL headword pipeline with sublist metadata retained in notes or manifest.
