#!/usr/bin/env python3
from __future__ import annotations

import csv
import glob
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN = "toefl_ets_2026_set_[0-9][0-9].tsv"
THRESHOLD = 85


def main() -> int:
    changed = 0
    touched_files = 0
    for rel_path in sorted(glob.glob(PATTERN)):
        path = ROOT / rel_path
        rows = []
        file_changed = False
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            for headword, back in reader:
                lines = back.split("\n")
                if "-" not in headword:
                    rows.append([headword, back])
                    continue

                rebuilt = []
                removed = False
                for line in lines:
                    if line.startswith("구분:"):
                        value = line.split(":", 1)[1].strip()
                        if len(value) >= THRESHOLD:
                            removed = True
                            continue
                    rebuilt.append(line)

                if removed:
                    changed += 1
                    file_changed = True
                    rows.append([headword, "\n".join(rebuilt)])
                else:
                    rows.append([headword, back])

        if file_changed:
            touched_files += 1
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                writer.writerows(rows)

    print(f"changed={changed}")
    print(f"touched_files={touched_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
