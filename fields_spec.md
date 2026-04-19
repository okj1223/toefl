# Fields Spec

All card files are stored as UTF-8 TSV with:

- no header
- column 1 = English headword on line 1, with optional line 2 as `[IPA pronunciation]`
- column 2 = card back content
- delimiter = tab
- internal line breaks in either column are stored as actual newlines inside a quoted TSV field

## Card Back Structure

Every card back now uses a compact structure:

1. `핵심 뜻:` required
2. `구분:` optional

The card back may therefore have 1 or 2 lines.

## Card Front Structure

The card front always keeps the canonical English headword on line 1.

- line 2 is optional and may contain a bracketed IPA pronunciation such as `[əˈlaɪn]`
- duplicate headword checks are based on the line-1 headword, not the optional pronunciation line

## Meaning Count Policy

There is no fixed target count for how many glosses or contrast points a card must contain.

- `핵심 뜻:` may contain one meaning or several TOEFL-relevant senses when those senses are all genuinely reusable on the test
- `구분:` is used only when the confusion risk is real, and it may compare against one or two nearby words depending on what is actually helpful

Cards should therefore be driven by study value, not by symmetric formatting.

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
- after pruning/review, files are rebalanced into roughly even sections instead of fixed 100-card blocks
- current section sizing is `79/78` for ETS and `70/70/69/69` for AWL

## Validation Rules

- exactly 2 TSV columns per row
- column 1 must contain a headword on line 1, with optional line 2 in bracketed IPA format
- column 2 must contain actual line breaks, not escaped `\n` text
- 1 to 2 labeled lines in the allowed order
- `핵심 뜻:` must always be present
- `부가 뜻:` and `핵심 느낌:` must not appear in the front-facing TSV cards
- no empty files
- no duplicate headwords within a set family after cleanup
