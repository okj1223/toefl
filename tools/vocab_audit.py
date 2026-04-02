#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path


REQUIRED_LABELS = [
    "핵심 뜻:",
    "부가 뜻:",
    "핵심 느낌:",
    "예문:",
    "해석:",
    "구분:",
]


def audit_file(path: Path) -> dict:
    rows = []
    issues = []
    with path.open(encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, 1):
            line = raw_line.rstrip("\n")
            parts = line.split("\t")
            if len(parts) != 2:
                issues.append(
                    {
                        "file": str(path),
                        "line": line_no,
                        "type": "column_count",
                        "detail": len(parts),
                    }
                )
                continue

            headword, back = parts
            missing = [label for label in REQUIRED_LABELS if label not in back]
            if missing:
                issues.append(
                    {
                        "file": str(path),
                        "line": line_no,
                        "type": "missing_labels",
                        "detail": missing,
                    }
                )

            newline_literals = back.count("\\n")
            if newline_literals != 5:
                issues.append(
                    {
                        "file": str(path),
                        "line": line_no,
                        "type": "newline_literal_count",
                        "detail": newline_literals,
                    }
                )

            rows.append({"headword": headword.strip(), "line": line_no})

    return {"file": str(path), "count": len(rows), "rows": rows, "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pattern",
        default="toefl_*.tsv",
        help="Glob pattern for TSV files to audit.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of a text report.",
    )
    args = parser.parse_args()

    paths = [Path(path) for path in sorted(glob.glob(args.pattern))]
    report = {
        "pattern": args.pattern,
        "files": [],
        "duplicate_headwords": [],
        "summary": {
            "file_count": 0,
            "card_count": 0,
            "issue_count": 0,
        },
    }

    word_locations: dict[str, list[dict]] = defaultdict(list)
    for path in paths:
        file_report = audit_file(path)
        report["files"].append(file_report)
        report["summary"]["file_count"] += 1
        report["summary"]["card_count"] += file_report["count"]
        report["summary"]["issue_count"] += len(file_report["issues"])
        for row in file_report["rows"]:
            word_locations[row["headword"]].append(
                {"file": str(path), "line": row["line"]}
            )

    duplicates = {
        word: locations
        for word, locations in word_locations.items()
        if len(locations) > 1
    }
    report["duplicate_headwords"] = [
        {"headword": word, "locations": locations}
        for word, locations in sorted(duplicates.items())
    ]

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"Pattern: {args.pattern}")
    print(f"Files: {report['summary']['file_count']}")
    print(f"Cards: {report['summary']['card_count']}")
    print(f"Issues: {report['summary']['issue_count']}")
    print(
        "Duplicate headwords: "
        f"{len(report['duplicate_headwords'])}"
    )

    for file_report in report["files"]:
        print(f"\n[{file_report['file']}]")
        print(f"count={file_report['count']} issues={len(file_report['issues'])}")
        for issue in file_report["issues"][:10]:
            print(
                f"  line {issue['line']}: {issue['type']} -> {issue['detail']}"
            )

    if report["duplicate_headwords"]:
        print("\n[duplicates]")
        for item in report["duplicate_headwords"]:
            locations = ", ".join(
                f"{Path(loc['file']).name}:{loc['line']}"
                for loc in item["locations"]
            )
            print(f"  {item['headword']}: {locations}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
