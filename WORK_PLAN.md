# TOEFL Vocab Build Plan

## Current Audit

- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_22.tsv`
- Current ETS row count after pruning and dedupe cleanup: 2194
- Required format policy is changing:
  - remove `예문:` and `해석:` from every card
  - store actual line breaks inside quoted TSV fields instead of escaped `\\n` text
- Current target policy is also changing:
  - do not force 3000 ETS-based cards if the tail quality drops
  - prioritize a defensible high-utility academic core for post-2026 TOEFL band 5

## Official-Source Direction To Preserve

- Use ETS official/public TOEFL pages and samples as the primary orientation for topic and register.
- Reflect the May 29, 2025 ETS announcement for January 2026 changes:
  - multistage adaptive Reading and Listening
  - more modern and equitable topics
  - stronger academic-life relevance such as group discussions and project work
- Reflect the January 21, 2026 score-report transition:
  - the former 100-point goal maps approximately to overall band 5
- Avoid claiming any non-existent "ETS official 3000 word list."

## Build Sequence

1. Stabilize the current ETS base.
2. Lock an ETS-based candidate policy:
   - cross-disciplinary academic vocabulary first
   - very basic words removed
   - hyper-specialized terms excluded or pushed down
   - modern academic/campus/lecture contexts preferred
   - no hard 3000-card quota if quality gates say stop
3. Convert existing TSVs to the 4-line no-example format with real multiline fields.
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
   - actual multiline TSV formatting
   - empty file check

## Set Architecture Redesign

- Avoid "one set = one school subject" design.
- Use function-centered and discourse-centered set focuses: evidence, cause-effect, comparison, interpretation, project coordination, data explanation, policy reasoning, and academic response language.
- Allow topic variety inside each set, but cap any one narrow specialist subdomain to roughly 15 cards so biology/history/engineering clusters do not take over.
- Prefer transferable academic wording that can reappear in multiple TOEFL sections and passage types.
- Do not pre-create all future `.task_setXX.md` files up to 30 sets, because 3000 cards is not a hard quota and future focuses should stay adjustable.
- Keep completed-set task files as historical records, but use `.task_next.md` as the only active prompt spec for the next immediate ETS set.

## Immediate Next Actions

1. Generate the next ETS file from `.task_next.md`, then update `.task_next.md` for only the following set.
2. Re-run validation after each rewritten/generated set and repair malformed cards immediately.
3. Periodically rebalance earlier ETS sets if any subject silo or meaning-quality drift appears.
4. Do a semantic polishing pass on machine-generated AWL glosses before final study use.
