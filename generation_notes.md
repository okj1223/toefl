# Generation Notes

## ETS-Based Principle

There is no official ETS-published "TOEFL 3000 word list," so this project treats "ETS-based" as a curated vocabulary set aligned to official/public TOEFL materials and test descriptions rather than a claimed official inventory.

The ETS-facing selection logic prioritizes:

- vocabulary that recurs across reading, listening, speaking, and writing
- university lecture, seminar, project, and campus-life contexts
- academic words that remain useful across multiple disciplines
- medium-high to high-utility words appropriate for a TOEFL 100+ target

## 2026 TOEFL Update Reflection

This build is oriented to the January 2026 TOEFL direction announced by ETS on May 29, 2025:

- multistage adaptive Reading and Listening
- more modern and equitable topics
- stronger emphasis on real academic settings such as group discussion and project work

These changes push the vocabulary mix toward modern academic-life usage rather than older niche or culturally narrow topics.

## AWL Handling Principle

The AWL set is built around AWL headwords, not by exploding every derivative into separate cards.

- one card per headword by default
- sublist order is preserved in file sequencing and metadata
- related forms may be referenced only as support information when useful

## Specialized Vocabulary Exclusion Rule

Words were excluded or deprioritized when they were:

- too basic for the target band
- too specialized for likely TOEFL reuse
- likely to be defined directly in a passage rather than assumed as known vocabulary
- near-duplicates of already stronger, more reusable headwords

## Example Sentence Principle

All example sentences are newly written for this project.

- no long copying from ETS source wording
- campus, lecture, discussion, and research contexts preferred
- natural Korean translations prioritize fast exam recall over dictionary-style completeness

## Current Status

As of this draft:

- ETS sets `01` to `09` exist
- automated TSV validation is in place
- duplicate cleanup has started and is tracked in `duplicates_removed.tsv`
- remaining ETS sets, AWL sets, and final manifest still need completion
