from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TASK_FORMAT_BLOCK_OLD = """FORMAT: UTF-8 TSV, no header. Each line:
word<TAB>핵심 뜻: ...\\n부가 뜻: ...\\n핵심 느낌: ...\\n예문: ...\\n해석: ...\\n구분: ...
\\n = literal backslash+n (two characters), NOT actual newline.
"""

TASK_FORMAT_BLOCK_NEW = '''FORMAT: UTF-8 TSV, no header. Each record has 2 columns:
- Column 1: one English headword
- Column 2: a double-quoted multiline back field with EXACTLY these 4 lines, using actual newline characters:
  핵심 뜻: ...
  부가 뜻: ...
  핵심 느낌: ...
  구분: ...
Do NOT include 예문 or 해석.
'''

TASK_RULES_OLD = (
    "Rules: TOEFL 100+ academic vocab, not too basic/specialized, original example sentences, "
    "Korean quick-recall meanings, 핵심 느낌 short vivid hook, American spelling, lemma form, EXACTLY 100 lines.\n"
)

TASK_RULES_NEW = (
    "Rules: TOEFL 100+ academic vocab aligned with post-2026 TOEFL iBT broad academic language, "
    "not too basic/specialized, Korean quick-recall meanings, 핵심 느낌 short vivid hook, "
    "구분 should compare genuinely confusable words, American spelling, lemma form, EXACTLY 100 records.\n"
)

REBUILD_RULES_OLD = (
    "Rules: prioritize modern academic-life relevance, avoid very basic words, avoid hyper-specialized terms, "
    "use original examples, American spelling, lemma form, EXACTLY 100 lines.\n"
)

REBUILD_RULES_NEW = (
    "Rules: prioritize modern academic-life relevance and broad academic language, avoid very basic words, "
    "avoid hyper-specialized terms, no example sentences, American spelling, lemma form, EXACTLY 100 records.\n"
)


def rewrite_task_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = text.replace(TASK_FORMAT_BLOCK_OLD, TASK_FORMAT_BLOCK_NEW)
    text = text.replace(TASK_RULES_OLD, TASK_RULES_NEW)
    text = text.replace(REBUILD_RULES_OLD, REBUILD_RULES_NEW)
    text = text.replace("Write the file, verify 100 lines.\n", "Write the file, verify 100 records and TSV structure.\n")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def rewrite_generation_template() -> bool:
    path = ROOT / ".generation_prompt_template.md"
    text = path.read_text(encoding="utf-8")
    new_text = """You are generating TOEFL vocabulary flashcards for a Korean student targeting TOEFL 100+ / Band 5.

EXISTING WORDS (DO NOT DUPLICATE):
{EXISTING_WORDS}

Generate exactly 100 flashcard entries for file: {FILENAME}

FORMAT: UTF-8 TSV, no header. Column 1 = English headword. Column 2 = double-quoted multiline back content.
Column 2 must contain actual newline characters between labels, not literal \\n text.

Each card back MUST have exactly these 4 lines:
핵심 뜻: [concise Korean meaning]
부가 뜻: [secondary meanings separated by /]
핵심 느낌: [short intuitive memory hook in Korean]
구분: [synonym comparisons in format: word1=뜻1 / word2=뜻2 / word3=뜻3]

SELECTION CRITERIA for set {SET_NUM}:
- Broad academic vocabulary likely in TOEFL Reading/Listening/Writing/Speaking after the 2026 TOEFL iBT update
- NOT too basic (no "go", "make", "big")
- NOT too specialized or passage-defined niche terminology
- Cross-disciplinary academic words and modern academic-life language preferred
- Priority rank range: {PRIORITY_RANGE} (1=highest priority)
- Lemma form, American spelling
- {DOMAIN_FOCUS}

RULES:
- Do NOT include example sentences or translations
- Korean meanings should be exam-friendly (quick recall)
- 핵심 느낌 should be a vivid, short memory hook
- 구분 should focus on commonly confused words, not loose synonyms
- Output ONLY the TSV data, no explanation, no header

Example of ONE TSV record:
entail\t"핵심 뜻: 필연적으로 수반하다
부가 뜻: 필요로 하다 / 초래하다
핵심 느낌: 어떤 일을 하면 그것이 따라온다
구분: require=직접 필요 / cause=일으키다 / involve=포함하다"

Now generate exactly 100 entries for {FILENAME}. Output ONLY TSV records.
"""
    if text != new_text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def rewrite_batch_gen() -> bool:
    path = ROOT / ".batch_gen.sh"
    text = path.read_text(encoding="utf-8")
    new_text = """#!/bin/bash
set -e

WORKDIR="$HOME/toefl-vocab-2026"
cd "$WORKDIR"

SET_NUM=$1
DOMAIN=$2

EXISTING=$(cat .existing_words.txt | tr '\\n' ', ')
FILENAME="toefl_ets_2026_set_$(printf '%02d' $SET_NUM).tsv"

# Priority ranges per set
PSTART=$(( (SET_NUM - 1) * 100 + 1 ))
PEND=$(( SET_NUM * 100 ))

PROMPT="You are generating TOEFL iBT vocabulary flashcards for a Korean student (target: 100+ / Band 5).

WORDS ALREADY USED (DO NOT DUPLICATE ANY OF THESE):
$EXISTING

Generate exactly 100 NEW flashcard entries for file: $FILENAME
Priority rank range: $PSTART-$PEND

FORMAT: UTF-8 TSV, no header row. Column 1 = english headword. Column 2 = double-quoted multiline back content.
Column 2 must use actual newline characters between labels, not literal \\\\n text.

Each card back MUST contain exactly these 4 labeled lines:
핵심 뜻: [concise Korean core meaning]
부가 뜻: [secondary meanings with /]
핵심 느낌: [short vivid memory hook in Korean]
구분: [synonym1=Korean gloss / synonym2=Korean gloss]

DOMAIN FOCUS for this set: $DOMAIN

SELECTION CRITERIA:
- Broad academic vocabulary for TOEFL Reading/Listening/Writing/Speaking
- Cross-disciplinary words that appear across multiple academic fields
- NOT too basic
- NOT hyper-specialized or passage-defined niche terminology
- 2026 TOEFL style: modern academic-life contexts and less culture-bound wording
- Lemma form preferred, American spelling
- If a word has multiple POS with very different meanings, pick the most TOEFL-relevant POS

QUALITY RULES:
- Do NOT include example sentences or translations
- Korean meanings: exam-friendly, quick-recall style
- 핵심 느낌: vivid and short
- 구분: only include words that are genuinely confusing on the test
- Every record must be valid TSV

Output ONLY the 100 TSV records. No headers, no explanations, no markdown."

echo "$PROMPT" | claude --permission-mode bypassPermissions --print -p - 2>/dev/null > "$FILENAME"

# Validate
python3 tools/vocab_audit.py --pattern "$FILENAME"
echo "Generated $FILENAME"
"""
    if text != new_text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = []

    for path in sorted(ROOT.glob(".task_set*.md")) + sorted(ROOT.glob(".task_rebuild_set*.md")):
        if rewrite_task_file(path):
            updated.append(path.name)

    if rewrite_generation_template():
        updated.append(".generation_prompt_template.md")

    if rewrite_batch_gen():
        updated.append(".batch_gen.sh")

    print(f"updated {len(updated)} files")
    for name in updated:
        print(name)


if __name__ == "__main__":
    main()
