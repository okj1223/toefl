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
DISTINCTION_LENGTH_THRESHOLD = 60


def should_remove_extra(extra: str) -> bool:
    if not extra:
        return False
    if len(extra) <= 10:
        return True
    if len(extra) <= 18 and any(sep in extra for sep in [" / ", "; ", ", "]):
        return True
    return False


def shorten_distinction(distinction: str) -> str:
    if not distinction or len(distinction) < DISTINCTION_LENGTH_THRESHOLD:
        return distinction
    parts = [part.strip() for part in distinction.split(" / ") if part.strip()]
    if len(parts) >= 3:
        return " / ".join(parts[:2])
    return distinction


def process_back(back: str) -> tuple[str, dict[str, int]]:
    values = {}
    order = []
    for line in back.split("\n"):
        label, _, value = line.partition(":")
        values[label] = value.strip()
        order.append(label)

    changes = {"extra_removed": 0, "dist_trimmed": 0}

    extra = values.get("부가 뜻", "")
    if extra and should_remove_extra(extra):
        values.pop("부가 뜻", None)
        order = [label for label in order if label != "부가 뜻"]
        changes["extra_removed"] = 1

    distinction = values.get("구분", "")
    trimmed = shorten_distinction(distinction)
    if trimmed != distinction:
        values["구분"] = trimmed
        changes["dist_trimmed"] = 1

    rebuilt = []
    for label in order:
        if label in values:
            rebuilt.append(f"{label}: {values[label]}")
    return "\n".join(rebuilt), changes


def main() -> int:
    files_changed = 0
    rows_changed = 0
    extra_removed = 0
    dist_trimmed = 0

    for pattern in PATTERNS:
        for rel_path in sorted(glob.glob(pattern)):
            path = ROOT / rel_path
            updated_rows = []
            local_changed = False

            with path.open(encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle, delimiter="\t")
                for headword, back in reader:
                    new_back, changes = process_back(back)
                    updated_rows.append([headword, new_back])
                    if new_back != back:
                        local_changed = True
                        rows_changed += 1
                        extra_removed += changes["extra_removed"]
                        dist_trimmed += changes["dist_trimmed"]

            if local_changed:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                    writer.writerows(updated_rows)
                files_changed += 1

    print(f"files_changed={files_changed}")
    print(f"rows_changed={rows_changed}")
    print(f"extra_removed={extra_removed}")
    print(f"dist_trimmed={dist_trimmed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
