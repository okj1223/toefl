#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rows(pattern: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for path in sorted(ROOT.glob(pattern)):
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if len(row) == 2:
                    rows.append(row)
    return rows


def rebalance(rows: list[list[str]], sizes: list[int], prefix: str) -> None:
    if sum(sizes) != len(rows):
        raise ValueError(f"{prefix}: size mismatch {sum(sizes)} != {len(rows)}")

    existing = sorted(ROOT.glob(f"{prefix}_*.tsv"))
    for path in existing:
        path.unlink()

    cursor = 0
    for idx, size in enumerate(sizes, start=1):
        chunk = rows[cursor:cursor + size]
        cursor += size
        path = ROOT / f"{prefix}_{idx:02d}.tsv"
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t", lineterminator="\n")
            writer.writerows(chunk)


def main() -> int:
    ets_rows = read_rows("toefl_ets_2026_set_*.tsv")
    awl_rows = read_rows("toefl_awl_set_*.tsv")

    ets_sizes = [79] * 17 + [78] * 8
    awl_sizes = [70, 70, 69, 69]

    rebalance(ets_rows, ets_sizes, "toefl_ets_2026_set")
    rebalance(awl_rows, awl_sizes, "toefl_awl_set")

    print(
        f"ETS files={len(ets_sizes)} total={len(ets_rows)} sizes={ets_sizes[:3]}...{ets_sizes[-3:]}"
    )
    print(f"AWL files={len(awl_sizes)} total={len(awl_rows)} sizes={awl_sizes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
