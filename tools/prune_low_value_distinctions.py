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

# These comparator words are broad enough that they often make a distinction
# line longer without adding much real study value.
LOW_VALUE_COMPARATORS = {
    "ask",
    "clear",
    "collect",
    "conflict",
    "include",
    "limit",
    "natural",
    "notice",
    "plan",
    "record",
    "save",
    "scale",
    "summary",
    "support",
}


def prune_distinction(distinction: str) -> tuple[str, int]:
    parts = [part.strip() for part in distinction.split(" / ") if part.strip()]
    if len(parts) < 3:
        return distinction, 0

    kept = [parts[0]]
    removed = 0
    for part in parts[1:]:
        head = part.split("=", 1)[0].strip().lower()
        if head in LOW_VALUE_COMPARATORS:
            removed += 1
            continue
        kept.append(part)

    if removed and len(kept) >= 2:
        return " / ".join(kept), removed
    return distinction, 0


def process_back(back: str) -> tuple[str, int]:
    rebuilt = []
    removed = 0
    for line in back.split("\n"):
        if line.startswith("구분:"):
            value = line[len("구분:") :].strip()
            new_value, removed = prune_distinction(value)
            rebuilt.append(f"구분: {new_value}")
        else:
            rebuilt.append(line)
    return "\n".join(rebuilt), removed


def main() -> int:
    files_changed = 0
    rows_changed = 0
    parts_removed = 0

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
                    new_back, removed = process_back(back)
                    updated_rows.append([headword, new_back])
                    if new_back != back:
                        local_changed = True
                        rows_changed += 1
                        parts_removed += removed

            if local_changed:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                    writer.writerows(updated_rows)
                files_changed += 1

    print(f"files_changed={files_changed}")
    print(f"rows_changed={rows_changed}")
    print(f"parts_removed={parts_removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
