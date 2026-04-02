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

PROMPT="You are generating TOEFL iBT vocabulary flashcards for a Korean student (target: 100+, band 5).

WORDS ALREADY USED (DO NOT DUPLICATE ANY OF THESE):
$EXISTING

Generate exactly 100 NEW flashcard entries for file: $FILENAME
Priority rank range: $PSTART-$PEND

FORMAT: UTF-8 TSV, no header row. Each line: english_word<TAB>back_content
Back side content uses literal backslash-n (the two characters \ and n) for line breaks within the cell.

Each card back MUST contain exactly 6 labeled lines separated by \\n:
핵심 뜻: [concise Korean core meaning]
부가 뜻: [secondary meanings with /]
핵심 느낌: [short vivid memory hook in Korean]
예문: [original TOEFL-style academic sentence in English]
해석: [natural Korean translation of the example]
구분: [synonym1=Korean gloss / synonym2=Korean gloss]

DOMAIN FOCUS for this set: $DOMAIN

SELECTION CRITERIA:
- Academic vocabulary for TOEFL Reading/Listening/Writing/Speaking
- Cross-disciplinary words that appear across multiple academic fields
- NOT too basic (exclude high-school level words like 'important', 'develop')
- NOT hyper-specialized (exclude words typically defined in passage like 'photosynthesis')
- 2026 TOEFL style: modern academic-life contexts
- Lemma form preferred, American spelling
- If a word has multiple POS with very different meanings, pick the most TOEFL-relevant POS

QUALITY RULES:
- Create ORIGINAL example sentences (never copy from ETS materials)
- Korean meanings: exam-friendly, quick-recall style (not dictionary definitions)
- 핵심 느낌: vivid and short (under 15 chars ideally), helps snap-recall
- Examples: use university lecture, research, campus life, academic discussion contexts
- 구분: only include synonyms that are genuinely confusing on the test
- Every line must be valid TSV (no unescaped tabs in content)

Output ONLY the 100 TSV lines. No headers, no explanations, no markdown."

echo "$PROMPT" | claude --permission-mode bypassPermissions --print -p - 2>/dev/null > "$FILENAME"

# Validate
LINES=$(wc -l < "$FILENAME")
echo "Generated $FILENAME with $LINES lines"
