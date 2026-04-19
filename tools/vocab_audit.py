#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import glob
import json
import re
from collections import defaultdict
from pathlib import Path

from front_utils import extract_headword


CANONICAL_LABELS = [
    "핵심 뜻:",
    "구분:",
]

REQUIRED_LABELS = {
    "핵심 뜻:",
}

FORBIDDEN_LABELS = [
    "부가 뜻:",
    "핵심 느낌:",
    "예문:",
    "해석:",
]

FRONT_PRONUNCIATION_RE = re.compile(r"^\[[^\[\]\n]+\]$")


def audit_file(path: Path) -> dict:
    rows = []
    issues = []
    with path.open(encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row_no, parts in enumerate(reader, 1):
            if len(parts) != 2:
                issues.append(
                    {
                        "file": str(path),
                        "line": row_no,
                        "type": "column_count",
                        "detail": len(parts),
                    }
                )
                continue

            front, back = parts
            front_lines = front.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            headword = extract_headword(front)
            back_lines = back.split("\n")

            if not 1 <= len(front_lines) <= 2:
                issues.append(
                    {
                        "file": str(path),
                        "line": row_no,
                        "type": "front_line_count",
                        "detail": len(front_lines),
                    }
                )

            if not headword:
                issues.append(
                    {
                        "file": str(path),
                        "line": row_no,
                        "type": "empty_headword",
                        "detail": front,
                    }
                )

            if len(front_lines) == 2:
                pronunciation = front_lines[1].strip()
                if not FRONT_PRONUNCIATION_RE.fullmatch(pronunciation):
                    issues.append(
                        {
                            "file": str(path),
                            "line": row_no,
                            "type": "front_pronunciation_format",
                            "detail": pronunciation,
                        }
                    )

            if "\\n" in back:
                issues.append(
                    {
                        "file": str(path),
                        "line": row_no,
                        "type": "escaped_newline_literal",
                        "detail": "\\n",
                    }
                )

            if not 1 <= len(back_lines) <= len(CANONICAL_LABELS):
                issues.append(
                    {
                        "file": str(path),
                        "line": row_no,
                        "type": "back_line_count",
                        "detail": len(back_lines),
                    }
                )

            labels = []
            for line in back_lines:
                label = next(
                    (candidate for candidate in CANONICAL_LABELS if line.startswith(candidate)),
                    None,
                )
                if label is None:
                    issues.append(
                        {
                            "file": str(path),
                            "line": row_no,
                            "type": "unknown_label",
                            "detail": line,
                        }
                    )
                    labels = []
                    break
                if not line[len(label) :].strip():
                    issues.append(
                        {
                            "file": str(path),
                            "line": row_no,
                            "type": "empty_label_value",
                            "detail": label,
                        }
                    )
                labels.append(label)

            if labels:
                order = [CANONICAL_LABELS.index(label) for label in labels]
                if order != sorted(order) or len(set(labels)) != len(labels):
                    issues.append(
                        {
                            "file": str(path),
                            "line": row_no,
                            "type": "label_order",
                            "detail": labels,
                        }
                    )
                if not REQUIRED_LABELS.issubset(set(labels)):
                    issues.append(
                        {
                            "file": str(path),
                            "line": row_no,
                            "type": "missing_required_labels",
                            "detail": sorted(REQUIRED_LABELS - set(labels)),
                        }
                    )

            forbidden = [label for label in FORBIDDEN_LABELS if label in back]
            if forbidden:
                issues.append(
                    {
                        "file": str(path),
                        "line": row_no,
                        "type": "forbidden_labels",
                        "detail": forbidden,
                    }
                )

            rows.append({"headword": headword, "line": row_no})

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
