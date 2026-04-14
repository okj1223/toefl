#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REMOVE = {
    "toefl_awl_set_04.tsv": {
        "drama", "induce", "tense", "uniform", "vehicle", "commence", "devote",
        "mature", "relax", "rigid", "colleague", "enormous", "forthcoming",
        "likewise", "odd", "straightforward"
    },
    "toefl_ets_2026_set_01.tsv": {
        "align", "analogous", "artificial", "capability", "collaborate", "compelling",
        "competent", "conceptual", "detrimental", "domain", "ideology", "incorporate",
        "inspect", "interact", "persistent", "predominant", "proceed"
    },
    "toefl_ets_2026_set_04.tsv": {
        "extract", "incentive", "inhibit", "internal", "monitor", "nuclear",
        "outcome", "previous", "primary", "professional", "react", "resource"
    },
    "toefl_ets_2026_set_09.tsv": {
        "systemwide", "buffer", "safeguard", "summarize", "update", "modification",
        "component", "driver", "node", "networked", "regulator", "throughput",
        "substrate", "malleability", "circuit", "signal", "profile", "progression",
        "eliminate", "intake", "backbone", "procedure", "synopsis", "yardstick",
        "stepwise", "holistic", "competency", "retention"
    },
    "toefl_ets_2026_set_16.tsv": {
        "adjourn", "chairperson", "discussion-based", "coordinator", "disseminate",
        "extension", "handbook", "instructor", "mentor", "nomination", "outline",
        "rapport", "referral", "repository", "seminar", "submission", "timetable"
    },
}


def main() -> int:
    changed_files = 0
    changed_rows = 0
    for rel, words in REMOVE.items():
        path = ROOT / rel
        rows = []
        changed = False
        with path.open(encoding="utf-8", newline="") as f:
            for front, back in csv.reader(f, delimiter="\t"):
                new_back = back
                if front in words and "\n구분:" in back:
                    new_back = back.split("\n구분:", 1)[0]
                if new_back != back:
                    changed = True
                    changed_rows += 1
                rows.append([front, new_back])
        if changed:
            changed_files += 1
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter="\t", lineterminator="\n")
                writer.writerows(rows)
    print(f"changed_files={changed_files} changed_rows={changed_rows}")


if __name__ == "__main__":
    main()
