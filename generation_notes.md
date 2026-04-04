# Generation Notes

## ETS-Based Principle

There is no official ETS-published "TOEFL 3000 word list," so this project treats "ETS-based" as a curated vocabulary set aligned to official/public TOEFL materials and test descriptions rather than a claimed official inventory.

The ETS-facing selection logic prioritizes:

- vocabulary that recurs across reading, listening, speaking, and writing
- university lecture, seminar, project, and campus-life contexts
- academic words that remain useful across multiple disciplines
- medium-high to high-utility words appropriate for TOEFL iBT overall band `5` on the post-January 21, 2026 scale

## Count Policy

The previous "3000 ETS-based cards" target is no longer treated as a hard quota.

ETS does not publish a canonical TOEFL 3000-word inventory, and forcing the tail of a 3000-item list can lower quality by pulling in overly basic near-duplicates or narrow technical terms. The working policy is therefore:

- build a high-confidence ETS-based core first
- stop expanding when added words become too specialized, too low-utility, or too duplicate-prone
- keep 100-card file chunking, but allow the final number of ETS files to reflect quality gates instead of forcing exactly 30 files
- keep AWL as a separate headword inventory

## Prompt File Policy

Future ETS set prompts should not be pre-generated all the way to `.task_set30.md`.

- keep historical `.task_setXX.md` files only for already completed or actively reviewed sets
- use `.task_next.md` as the single current prompt for the next immediate ETS expansion step
- revise that next-set focus after each new set if topic skew or specialist-word drift appears
- this keeps the build aligned with the quality-gated, non-3000-forced count policy

## 2026 TOEFL Update Reflection

This build is oriented to the TOEFL iBT scoring/content direction in effect from January 21, 2026:

- multistage adaptive Reading and Listening
- more modern and equitable topics
- stronger emphasis on real academic settings such as group discussion and project work
- score interpretation aligned to the new 1-6 scale, where the former 100-point target maps approximately to overall band 5

These changes push the vocabulary mix toward modern academic-life usage rather than older niche or culturally narrow topics.

## Old-vs-New TOEFL Comparison Policy

Pruning was done against ETS's own before/after January 21, 2026 content description:

- pre-2026: traditional reading/listening passages, 4 speaking tasks, 2 writing tasks, and broader legacy academic passage topics
- post-2026: adaptive Reading/Listening, more modern and relatable language, `Read in Daily Life`, `Write an Email`, `Take an Interview`, and content less centered on traditional narrow topics such as Greek mythology

Operationally, this means:

- delete narrow one-field specialist words that feel closer to old passage-specific topic banks than to reusable academic-life vocabulary
- delete multi-word front entries because they violate the one-headword lemma rule and are better omitted than forced into phrase cards
- do not refill deleted ETS slots just to preserve 100 cards per file

## AWL Handling Principle

The AWL set is built around AWL headwords, not by exploding every derivative into separate cards.

- one card per headword by default
- sublist order is preserved in file sequencing and metadata
- related forms may be referenced only as support information when useful
- current AWL Korean glosses are machine-generated draft text and should receive a Claude quality-pass before final study use

## Specialized Vocabulary Exclusion Rule

Words were excluded or deprioritized when they were:

- too basic for the target band
- too specialized for likely TOEFL reuse
- likely to be defined directly in a passage rather than assumed as known vocabulary
- near-duplicates of already stronger, more reusable headwords

## Card-Back Style Principle

Cards now omit example sentences and translations.

- prioritize concise Korean meaning, semantic nuance, and differentiation from near-synonyms
- avoid copying ETS source wording
- keep back-side text compact and review-friendly

## Current Status

As of this draft:

- ETS sets `01` to `24` exist, and after the 2026-pruning pass plus a practical/data supplement pass the ETS-based total is now 2076 cards
- that second pruning pass deleted outdated, over-specialized, and multi-word front entries without backfilling
- set `23` adds practical post-2026 academic-life language for email, scheduling, campus services, interviews, and file workflows
- set `24` adds transferable quantitative/data language for trends, dispersion, uncertainty, approximation, and interpretation
- AWL sets `01` to `03` now contain 278 AWL headwords repacked into 100/100/78 records after ETS-overlap removal
- automated TSV validation is in place
- AWL generation is structurally complete and a first-pass Korean meaning polish has been applied, but manual spot review is still recommended
- duplicate cleanup has started and is tracked in `duplicates_removed.tsv`
- with sets `23` and `24` added, there is no obvious remaining domain gap for a band-5-oriented single-headword core, but final meaning-quality spot review is still recommended
