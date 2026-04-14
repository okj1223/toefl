#!/usr/bin/env python3
from __future__ import annotations

import csv
import glob
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    "toefl_ets_2026_set_[0-9][0-9].tsv",
    "toefl_awl_set_[0-9][0-9].tsv",
]

EXTRA_FILLERS = {
    "심리 상태·행동 경향·판단 과정에서 나타나는 관련 의미",
    "관련된 개념·절차·결과 / 문맥에 따라 구체적 대상이 달라짐",
    "그런 성향이나 기준을 가진 / 특정 맥락에서 그렇게 작동하는",
}

DISTINCTION_FILLERS = (
    "관련 어휘와는 의미 범위·강조점·쓰임으로 구분",
    "해당 개념 자체 / process=진행 절차 / outcome=결과",
    "해당 심리·행동 개념 / attitude=태도 / behavior=겉으로 드러난 행동",
    "그 성질을 직접 나타냄 / cognitive=사고 과정 관련 / emotional=감정 반응 관련",
)


def normalize_tokens(text: str) -> set[str]:
    cleaned = re.sub(r"[;,.·()]", " ", text)
    return {
        token.strip()
        for token in re.split(r"[/ ]+", cleaned)
        if token.strip()
    }


def should_drop_extra(core: str, extra: str) -> bool:
    if extra in EXTRA_FILLERS:
        return True

    core_tokens = normalize_tokens(core)
    extra_tokens = normalize_tokens(extra)
    if not core_tokens or not extra_tokens:
        return False

    overlap = len(core_tokens & extra_tokens) / len(core_tokens | extra_tokens)
    return overlap >= 0.6


def should_drop_distinction(distinction: str) -> bool:
    if not distinction:
        return True
    if not re.search(r"[A-Za-z]", distinction):
        return True
    return any(filler in distinction for filler in DISTINCTION_FILLERS)


def compact_back(back: str) -> tuple[str, dict[str, int]]:
    values = {}
    for line in back.split("\n"):
        label, _, value = line.partition(":")
        values[label] = value.strip()

    lines = [f"핵심 뜻: {values['핵심 뜻']}"]
    changes = {"extra_removed": 0, "distinction_removed": 0}

    extra = values.get("부가 뜻", "")
    if extra and not should_drop_extra(values["핵심 뜻"], extra):
        lines.append(f"부가 뜻: {extra}")
    elif extra:
        changes["extra_removed"] = 1

    lines.append(f"핵심 느낌: {values['핵심 느낌']}")

    distinction = values.get("구분", "")
    if distinction and not should_drop_distinction(distinction):
        lines.append(f"구분: {distinction}")
    elif distinction:
        changes["distinction_removed"] = 1

    return "\n".join(lines), changes


def main() -> int:
    files_changed = 0
    rows_changed = 0
    extra_removed = 0
    distinction_removed = 0

    for pattern in PATTERNS:
        for rel_path in sorted(glob.glob(pattern)):
            path = ROOT / rel_path
            updated_rows = []
            local_changed = False

            with path.open(encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle, delimiter="\t")
                for row in reader:
                    headword, back = row
                    compacted, changes = compact_back(back)
                    updated_rows.append([headword, compacted])
                    if compacted != back:
                        local_changed = True
                        rows_changed += 1
                        extra_removed += changes["extra_removed"]
                        distinction_removed += changes["distinction_removed"]

            if local_changed:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                    writer.writerows(updated_rows)
                files_changed += 1

    print(f"files_changed={files_changed}")
    print(f"rows_changed={rows_changed}")
    print(f"extra_removed={extra_removed}")
    print(f"distinction_removed={distinction_removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
