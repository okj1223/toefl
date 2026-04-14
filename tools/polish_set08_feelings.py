#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "toefl_ets_2026_set_08.tsv"

FEELINGS = {
    "inquiry": "질문에서 출발해 답을 찾아가는 배움",
    "feedback": "해본 결과에 대해 무엇을 고칠지 되돌려 받는 말",
    "benchmark": "도달 여부를 가늠하는 기준선",
    "elaboration": "새 정보에 이유와 연결을 붙여 살을 붙이는 과정",
    "procedural": "무엇인지보다 어떻게 하는지 아는 쪽",
    "diagnostic": "어디서 막혔는지 먼저 짚어 보는 진단용",
    "analogy": "낯선 것을 익숙한 것에 빗대 이해시키는 방식",
    "reflective": "지나간 생각과 행동을 다시 돌아보는 쪽",
    "exemplar": "따라갈 품질 수준을 보여 주는 본보기",
    "reinforce": "좋은 반응을 더 자주 나오게 단단히 굳히는 것",
}


def main() -> int:
    rows = []
    changed = 0
    with PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for headword, back in reader:
            lines = back.split("\n")
            updated = []
            for line in lines:
                if line.startswith("핵심 느낌:") and headword in FEELINGS:
                    new_line = f"핵심 느낌: {FEELINGS[headword]}"
                    if new_line != line:
                        changed += 1
                    updated.append(new_line)
                else:
                    updated.append(line)
            rows.append([headword, "\n".join(updated)])

    with PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    print(f"changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
