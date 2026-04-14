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
    "alternatively": "대신에",
    "namely": "즉",
    "inquiry": "탐구",
    "competency": "역량",
    "retention": "기억 유지",
    "mastery": "숙달",
    "immersion": "몰입",
    "collaborative": "협동적인",
    "affective": "정의적인",
    "prerequisite": "선수 조건",
    "aptitude": "적성",
    "articulate": "명확히 표현하다",
    "adaptive": "적응적인",
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
