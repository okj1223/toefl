#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    for path in sorted(ROOT.glob("toefl_awl_set_[0-9][0-9].tsv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.reader(handle, delimiter="\t"):
                if len(row) == 2:
                    rows.append(row)
    return rows


def write_rows(rows: list[list[str]], chunk_size: int = 100) -> list[str]:
    for path in sorted(ROOT.glob("toefl_awl_set_[0-9][0-9].tsv")):
        path.unlink()

    names: list[str] = []
    for index, start in enumerate(range(0, len(rows), chunk_size), 1):
        name = f"toefl_awl_set_{index:02d}.tsv"
        names.append(name)
        with (ROOT / name).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerows(rows[start : start + chunk_size])
    return names


def main() -> int:
    rows = read_rows()
    names = write_rows(rows)
    print(f"rows={len(rows)}")
    print("files=" + ", ".join(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
