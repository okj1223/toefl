#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


def collect(pattern: str) -> list[str]:
    words: set[str] = set()
    for path in sorted(Path(".").glob(pattern)):
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            for row in reader:
                if len(row) == 2:
                    words.add(row[0].strip())
    return sorted(word for word in words if word)


def write_lines(path: str, lines: list[str]) -> None:
    Path(path).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def main() -> int:
    ets_words = collect("toefl_ets_2026_set_*.tsv")
    awl_words = collect("toefl_awl_set_*.tsv")
    write_lines("all_ets_headwords.txt", ets_words)
    write_lines("all_awl_headwords.txt", awl_words)
    combined = sorted(set(ets_words) | set(awl_words))
    write_lines("all_headwords.txt", combined)
    print(f"ETS={len(ets_words)} AWL={len(awl_words)} ALL={len(combined)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
