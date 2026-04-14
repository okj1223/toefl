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
- rebalance final file chunking to keep section sizes reasonably even after pruning, targeting roughly 80 cards per ETS section when practical
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

Cards now use a compact front-facing style.

- omit example sentences and translations
- omit `부가 뜻` entirely
- omit `핵심 느낌` entirely
- prioritize concise Korean meaning and only high-value differentiation from near-synonyms
- omit `구분` when it is just a part-of-speech tag, a field tag, or a generic comparison shell
- avoid copying ETS source wording
- keep back-side text compact and review-friendly

## Flexible Meaning Policy

Card content is no longer trimmed toward an artificial fixed shape.

- if a headword has one dominant TOEFL sense, keep one
- if it has two or three recurring TOEFL senses, keep two or three
- do not force extra glosses just to make the card look balanced
- do not force three comparison targets in `구분:` when one or two is enough
- when a comparison line contains only a very easy generic word that adds little study value, trim that comparator and keep the sharper contrast

## Current Status

As of this draft:

- ETS sets `01` to `25` exist, and after the full 2026-pruning/review pass the ETS-based total is now 1967 cards
- that second pruning pass deleted outdated, over-specialized, and multi-word front entries without backfilling
- a later strict review also removed 10 narrow late-stage science, art, and building-maintenance compounds and cleaned residual English-reference phrasing that added study fatigue
- set `23` adds practical post-2026 academic-life language for email, scheduling, campus services, interviews, and file workflows
- set `24` adds transferable quantitative/data language for trends, dispersion, uncertainty, approximation, and interpretation
- after the full semantic review, ETS files were rebalanced into `79/78`-card sections to avoid late-stage count collapse while preserving ordering
- AWL sets `01` to `04` now contain 278 AWL headwords repacked into `70/70/69/69` records after ETS-overlap removal and later count rebalancing
- automated TSV validation is in place
- AWL generation is structurally complete and repeated Korean meaning cleanup passes have been applied, but periodic manual spot review is still recommended
- duplicate cleanup has started and is tracked in `duplicates_removed.tsv`
- with sets `23` and `24` added, there is no obvious remaining domain gap for a band-5-oriented single-headword core, but final meaning-quality spot review is still recommended
- a later compact pass stripped all remaining `부가 뜻` and `핵심 느낌` lines from AWL `01` through ETS `24`, leaving only `핵심 뜻` plus optional `구분`
