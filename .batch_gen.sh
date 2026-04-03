#!/bin/bash
set -e

WORKDIR="$HOME/toefl-vocab-2026"
cd "$WORKDIR"

SET_NUM=$1
DOMAIN=$2

EXISTING=$(cat .existing_words.txt | tr '\n' ', ')
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
Column 2 must use actual newline characters between labels, not literal \\n text.

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
