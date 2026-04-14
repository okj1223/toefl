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

# Keep dual-sense heads where the second chunk carries a genuinely useful
# alternate use or part-of-speech shift.
KEEP_HEADWORDS = {
    "access",
    "chemical",
    "comment",
    "design",
    "finance",
    "research",
    "survey",
}

MARKERS = (
    "관련",
    "정함",
    "상태",
    "과정",
    "방식",
    "정도",
    "기준",
    "구조",
    "체계",
    "영향",
    "작용",
    "형태",
    "능력",
    "태도",
    "관계",
    "범위",
    "현상",
    "요소",
    "조건",
    "지향",
    "기반",
    "중심",
    "가능",
    "하는",
    "되는",
    "하기",
    "하기 위한",
    "맞춘",
    "맞춰",
    "남긴",
    "드러나는",
    "이어지는",
    "비해",
    "통한",
    "위한",
    "에 관한",
    "로 인한",
)


def split_core(core: str) -> tuple[str | None, list[str]]:
    for sep in (" / ", "; "):
        if sep in core:
            return sep, [part.strip() for part in core.split(sep) if part.strip()]
    return None, [core]


def should_prune(headword: str, parts: list[str]) -> bool:
    if headword in KEEP_HEADWORDS or len(parts) != 2:
        return False

    first, second = parts

    if len(second.split()) >= 2 and len(first.split()) <= 2:
        return True

    if len(second) >= 8 and len(first) <= 6:
        return True

    if any(marker in second for marker in MARKERS) and len(first) <= 12:
        return True

    return False


def process_back(headword: str, back: str) -> tuple[str, bool]:
    lines = back.split("\n")
    rebuilt = []
    changed = False

    for line in lines:
        if line.startswith("핵심 뜻:"):
            core = line[len("핵심 뜻:") :].strip()
            sep, parts = split_core(core)
            if sep and should_prune(headword, parts):
                rebuilt.append(f"핵심 뜻: {parts[0]}")
                changed = True
                continue
        rebuilt.append(line)

    new_back = "\n".join(rebuilt)
    return new_back, changed and new_back != back


def main() -> int:
    files_changed = 0
    rows_changed = 0
    core_parts_pruned = 0

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
                        core_parts_pruned += 1

            if local_changed:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                    writer.writerows(updated_rows)
                files_changed += 1

    print(f"files_changed={files_changed}")
    print(f"rows_changed={rows_changed}")
    print(f"core_parts_pruned={core_parts_pruned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
