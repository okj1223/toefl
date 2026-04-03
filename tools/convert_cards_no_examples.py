#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import glob
from pathlib import Path


KEEP_LABELS = [
    "핵심 뜻:",
    "부가 뜻:",
    "핵심 느낌:",
    "구분:",
]


def normalize_back(back: str) -> str:
    text = back.replace("\\n", "\n")
    picked: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        for label in KEEP_LABELS:
            if line.startswith(label):
                picked[label] = line
                break

    missing = [label for label in KEEP_LABELS if label not in picked]
    if missing:
        raise ValueError(f"missing labels: {missing}")

    return "\n".join(picked[label] for label in KEEP_LABELS)


def convert_file(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        rows = list(reader)

    converted = []
    for row_index, row in enumerate(rows, 1):
        if len(row) != 2:
            raise ValueError(f"{path}:{row_index}: expected 2 columns, got {len(row)}")
        headword, back = row
        converted.append([headword.strip(), normalize_back(back)])

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(converted)

    return len(converted)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pattern",
        default="toefl_*.tsv",
        help="Glob pattern for TSV files to rewrite.",
    )
    args = parser.parse_args()

    for name in sorted(glob.glob(args.pattern)):
        count = convert_file(Path(name))
        print(f"converted {name}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
