# Semantic Review Tracker

## Compact Review Standard

Current front-facing card format:

- required: `핵심 뜻:`
- optional: `구분:`

Each card is reviewed against these rules:

- `핵심 뜻` is fast, natural Korean for actual TOEFL recall
- keep multiple core senses only when they are genuinely reusable
- delete or tighten vague glosses that read like dictionary padding
- `구분` stays only when confusion risk is real
- `구분` should sharpen a useful contrast, not restate an easy generic word
- avoid over-technical, old-TOEFL-leaning, or low-transfer wording

## Batch Plan

- Batch 1: `toefl_awl_set_01.tsv`, `toefl_ets_2026_set_01.tsv`, `toefl_ets_2026_set_02.tsv`
- Batch 2: `toefl_awl_set_02.tsv`, `toefl_awl_set_03.tsv`, `toefl_ets_2026_set_03.tsv`, `toefl_ets_2026_set_04.tsv`
- Batch 3: `toefl_ets_2026_set_05.tsv` to `toefl_ets_2026_set_08.tsv`
- Batch 4: `toefl_ets_2026_set_09.tsv` to `toefl_ets_2026_set_12.tsv`
- Batch 5: `toefl_ets_2026_set_13.tsv` to `toefl_ets_2026_set_16.tsv`
- Batch 6: `toefl_ets_2026_set_17.tsv` to `toefl_ets_2026_set_20.tsv`
- Batch 7: `toefl_ets_2026_set_21.tsv` to `toefl_ets_2026_set_24.tsv`

## Progress

- Batch 1: completed
- Batch 2: completed
- Batch 3: completed
- Batch 4: completed
- Batch 5: completed
- Batch 6: completed
- Batch 7: completed

## Batch 1 Notes

- reviewed `toefl_awl_set_01.tsv`, `toefl_ets_2026_set_01.tsv`, and `toefl_ets_2026_set_02.tsv`
- corrected American spelling in AWL heads such as `analyze`, `labor`, and `maximize`
- tightened several filler-like dual glosses in ETS `01`
- restored missing core senses and a few high-value distinctions in ETS `02`
- revalidated the full TSV set after the batch-1 edits

## Batch 2 Notes

- reviewed `toefl_awl_set_02.tsv`, `toefl_awl_set_03.tsv`, `toefl_ets_2026_set_03.tsv`, and `toefl_ets_2026_set_04.tsv`
- corrected American spelling in AWL heads such as `license`, `utilize`, and `minimize`
- removed a few low-value tail senses such as `prospect=잠재 고객`
- sharpened several compact cores in ETS `03`, including `adjacent`, `alter`, `considerable`, `explicit`, and `hence`
- repaired a few meaning/distinction mismatches in ETS `04`, especially `access`, `aid`, `commission`, `confer`, `permit`, and `sustain`
- revalidated the full TSV set after the batch-2 edits

## Batch 3 Notes

- reviewed `toefl_ets_2026_set_05.tsv` through `toefl_ets_2026_set_08.tsv`
- tightened many older semicolon/comma-style glosses into faster compact cores
- removed low-value tail senses in law, policy, and finance cards such as `dividend`, `default`, and `verdict`
- clarified social-science cards in ETS `06`, especially `gender`, `institution`, and `empirical`
- sharpened health/system vocabulary in ETS `07`, including `adverse`, `transmission`, `resistance`, `valid`, and `prevalence`
- restored high-value learning/cognition contrasts in ETS `08`, especially `competency`, `retention`, `retrieval`, `intrinsic`, `extrinsic`, `quantitative`, `sample`, and `variable`
- revalidated the full TSV set after the batch-3 edits

## Batch 4 Notes

- reviewed `toefl_ets_2026_set_09.tsv` through `toefl_ets_2026_set_12.tsv`
- tightened several process/data/science cards in ETS `09`, including `utilization`, `trajectory`, `magnitude`, `rotation`, `deposition`, and `emission`
- cleaned up many overly padded dual glosses in ETS `10`, especially `accrue`, `amenable`, `augment`, `curtail`, `depict`, `discern`, `disclose`, `impetus`, `meticulous`, and `pertinent`
- clarified project/campus-task vocabulary in ETS `11`, including `deliverable`, `milestone`, `proposal`, `guidance`, `orientation`, and `stewardship`
- sharpened cognition/psychology wording in ETS `12`, especially `awareness`, `belief`, `emotion`, `expectation`, `judgment`, `recognition`, `withdrawal`, and `confidence`
- revalidated the full TSV set after the batch-4 edits

## Batch 5 Notes

- reviewed `toefl_ets_2026_set_13.tsv` through `toefl_ets_2026_set_16.tsv`
- corrected several campus/academic-life cards in ETS `13`, including `floor`, `citation`, `recipient`, `validation`, `outreach`, and `group-wide`
- repaired historical/social-science wording in ETS `14`, especially `trace`, `recovery`, `landmark`, `leadership`, `caravan`, and `urbanism`
- normalized a few digital/practical items in ETS `15`, including `plugin`, `query`, `auto-save`, and `platform`, and removed low-value items such as `log-in`, `infostream`, and `two-factor`
- pruned several narrow biology/ecology compounds from ETS `16`, including `cross-adaptation`, `sink-source`, `threshold-sensitive`, `density-dependent`, `disturbance-tolerant`, `chemosensory`, `photoperiodic`, and `bioenergetic`
- revalidated the full TSV set after the batch-5 edits

## Batch 6 Notes

- reviewed `toefl_ets_2026_set_17.tsv` through `toefl_ets_2026_set_20.tsv`
- kept the policy/governance core in ETS `17` but removed several low-transfer bureaucratic items such as `administrability`, `caseworker`, `deliverable-based`, `adjudicator`, and `whole-of-government`
- preserved the high-value argument/reading core in ETS `18` while pruning several meta-analytic study-label compounds such as `text-to-context`, `premise-checking`, `quote-heavy`, `reason-giving`, `rebuttal-ready`, and `statement-level`
- trimmed project/product jargon in ETS `19`, removing items such as `proof-of-concept`, `make-or-buy`, `milestone-driven`, `outage-prone`, `backward-compatible`, and `upgrade-ready`
- kept the reusable arts/humanities interpretation core in ETS `20` while pruning medium-specific tails such as `voiceover`, `chiaroscuro`, `mise-en-scene`, `dramaturgical`, `soundscape`, and `offscreen`
- refreshed a few remaining high-value cores in ETS `17` to `20`, including `eligibility`, `rollout`, `citizen-facing`, `assertive`, `backing`, `salience`, `fallback`, `human-centered`, `backdrop`, `composition`, `resonance`, and `embody`
- revalidated the full TSV set after the batch-6 edits

## Batch 7 Notes

- reviewed `toefl_ets_2026_set_21.tsv` through `toefl_ets_2026_set_24.tsv`
- kept the reusable discussion/social core in ETS `21` while trimming lower-value process compounds such as `bridge-building`, `trust-building`, `status-seeking`, `consent-based`, and `volunteer-based`
- tightened the climate supplement in ETS `22`, keeping broad high-transfer terms such as `carbon-neutral`, `preparedness`, `greenwashing`, `future-proofing`, and `resource-efficient` while pruning several jargon-heavy descriptor compounds
- leanified the practical supplement in ETS `23`, preserving high-value campus/admin verbs and nouns such as `reschedule`, `shortlist`, `waiver`, `stipend`, `availability`, `registrar`, and `turnaround` while removing many low-payoff UI/basic labels
- trimmed the data-interpretation supplement in ETS `24`, keeping reusable analysis vocabulary such as `approximation`, `outlier`, `forecast`, `dispersion`, `plateau`, `breakdown`, and `volatility` while pruning math-/diagnostics-specific tails such as `denominator`, `numerator`, `sensitivity`, `specificity`, and `thresholding`
- revalidated the full TSV set after the batch-7 edits

## Post-Review Rebalance

- preserved the reviewed card order and redistributed ETS cards into `25` files of `79/78` cards each
- redistributed AWL cards into `4` files of `70/70/69/69` cards to reduce file-size variance after overlap pruning
- revalidated the full TSV set after the section rebalance
