# Fields Spec

All card files are stored as UTF-8 TSV with:

- no header
- column 1 = English headword only
- column 2 = card back content
- delimiter = tab
- internal line breaks in column 2 are stored as actual newlines inside a quoted TSV field

## Card Back Required Structure

Every card back must contain exactly these 4 labeled lines in this order:

1. `핵심 뜻:`
2. `부가 뜻:`
3. `핵심 느낌:`
4. `구분:`

Example sentences and translations are intentionally excluded from the front-facing TSV cards.

## Internal Review Fields

The following review fields are tracked during generation and validation, but are not required to appear on the front-facing TSV cards:

- `source_type`
- `source_detail`
- `cefr_estimate`
- `difficulty_rank`
- `priority_rank`
- `duplicate_group`
- `confidence`
- `notes`

## Sorting Rules

- ETS-based sets: priority-first ordering
- AWL sets: sublist 1 to 10, then utility within each sublist
- files split in blocks of 100 cards

## Validation Rules

- exactly 2 TSV columns per row
- column 2 must contain actual line breaks, not escaped `\n` text
- exactly 4 labeled lines in the required order
- no empty files
- no duplicate headwords within a set family after cleanup
