#!/usr/bin/env python3
from __future__ import annotations

import csv
import glob
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    "toefl_ets_2026_set_[0-9][0-9].tsv",
    "toefl_awl_set_[0-9][0-9].tsv",
]

CORE_OVERRIDES = {
    "alteration": "변경",
    "beneficial": "유익한",
    "capability": "능력",
    "clarity": "명확성",
    "comparative": "비교의",
    "complexity": "복잡성",
    "controversy": "논란",
    "efficient": "효율적인",
    "emphasis": "강조",
    "ideology": "이념",
    "abate": "약해지다",
    "affluent": "부유한",
    "attest": "입증하다",
    "candid": "솔직한",
    "exhaustive": "철저한",
    "inception": "시작",
    "requisite": "필수의",
    "tentative": "잠정적인",
    "guideline": "지침",
    "shortage": "부족",
    "nutrient": "영양분",
    "summary": "요약",
    "storage": "저장",
    "completion": "완료",
    "interpretive": "해석의",
    "finite": "유한한",
    "degradation": "악화",
    "delay": "지연",
    "submission": "제출",
}


def process_back(headword: str, back: str) -> tuple[str, bool]:
    if headword not in CORE_OVERRIDES:
        return back, False

    lines = back.split("\n")
    rebuilt = []
    changed = False
    for line in lines:
        if line.startswith("핵심 뜻:"):
            new_line = f"핵심 뜻: {CORE_OVERRIDES[headword]}"
            rebuilt.append(new_line)
            changed = changed or (new_line != line)
        else:
            rebuilt.append(line)
    new_back = "\n".join(rebuilt)
    return new_back, changed


def main() -> int:
    files_changed = 0
    rows_changed = 0

    for pattern in PATTERNS:
        for rel_path in sorted(glob.glob(pattern)):
            path = ROOT / rel_path
            updated_rows = []
            local_changed = False

            with path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle, delimiter="\t", quotechar='"')
                for row in reader:
                    if len(row) != 2:
                        updated_rows.append(row)
                        continue
                    headword, back = row
                    new_back, changed = process_back(headword, back)
                    updated_rows.append([headword, new_back])
                    if changed:
                        local_changed = True
                        rows_changed += 1

            if local_changed:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                    writer.writerows(updated_rows)
                files_changed += 1

    print(f"files_changed={files_changed}")
    print(f"rows_changed={rows_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
