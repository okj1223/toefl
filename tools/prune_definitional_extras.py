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

DEFINITIONAL_ENDINGS = (
    "것",
    "상태",
    "정도",
    "과정",
    "사람",
    "성질",
    "방식",
    "구조",
    "범위",
    "조건",
    "흐름",
    "단계",
    "결과",
    "집합",
    "표시",
    "활동",
    "능력",
    "자리",
    "용량",
    "규모",
    "환경",
    "기준",
    "설명",
    "안내",
    "집단",
    "자료",
    "성분",
    "영역",
)

DEFINITIONAL_MARKERS = (
    "위해",
    "통해",
    "아니라",
    "이라는",
    "이거나",
    "으로서",
    "관련된",
    "뜻보다",
    "문맥에 따라",
    "상태인",
)


def core_is_already_multisense(core: str) -> bool:
    return " / " in core or ";" in core or "," in core


def looks_definitional(extra: str, core: str) -> bool:
    if not extra:
        return False
    if len(extra) < 22:
        return False
    if len(extra) >= 28 and " / " not in extra and "; " not in extra and core_is_already_multisense(core):
        return True
    if " / " in extra or "; " in extra:
        return False
    if extra.endswith("인"):
        return True
    if any(extra.endswith(ending) for ending in DEFINITIONAL_ENDINGS):
        return True
    if any(marker in extra for marker in DEFINITIONAL_MARKERS):
        return True
    return False


def process_back(back: str) -> tuple[str, bool]:
    lines = back.split("\n")
    core = next(
        (line[len("핵심 뜻:") :].strip() for line in lines if line.startswith("핵심 뜻:")),
        "",
    )
    rebuilt = []
    changed = False
    for line in lines:
        if line.startswith("부가 뜻:"):
            extra = line[len("부가 뜻:") :].strip()
            if looks_definitional(extra, core):
                changed = True
                continue
        rebuilt.append(line)
    new_back = "\n".join(rebuilt)
    return new_back, changed and new_back != back


def main() -> int:
    files_changed = 0
    rows_changed = 0
    extras_removed = 0

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
                    new_back, changed = process_back(back)
                    updated_rows.append([headword, new_back])
                    if changed:
                        local_changed = True
                        rows_changed += 1
                        extras_removed += 1

            if local_changed:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                    writer.writerows(updated_rows)
                files_changed += 1

    print(f"files_changed={files_changed}")
    print(f"rows_changed={rows_changed}")
    print(f"extras_removed={extras_removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
