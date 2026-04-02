#!/usr/bin/env python3
from __future__ import annotations

import glob
from pathlib import Path


def main() -> int:
    for name in sorted(glob.glob("toefl_*.tsv")):
        path = Path(name)
        text = path.read_text(encoding="utf-8")
        if text and not text.endswith("\n"):
            path.write_text(text + "\n", encoding="utf-8")
            print(f"normalized {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
