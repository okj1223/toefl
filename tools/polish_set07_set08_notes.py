#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

UPDATES = {
    "advancement": {
        "핵심 뜻": "진전 / 발전",
        "핵심 느낌": "앞으로 한 단계 나아간 상태",
    },
    "alignment": {
        "핵심 뜻": "정렬 / 기준 맞춤",
        "핵심 느낌": "따로 있던 요소가 같은 방향으로 맞아드는 상태",
    },
    "applicability": {
        "핵심 느낌": "아이디어가 실제 상황에도 먹히는 정도",
    },
    "assignment": {
        "핵심 느낌": "해야 할 일이 몫으로 주어진 상태",
    },
    "clarification": {
        "핵심 뜻": "명확화 / 설명 보강",
        "핵심 느낌": "흐리던 걸 또렷하게 풀어 주는 것",
    },
    "collaboration": {
        "핵심 뜻": "협업 / 공동 작업",
        "핵심 느낌": "혼자보다 역할을 나눠 함께 밀어가는 것",
    },
    "communication": {
        "핵심 느낌": "정보가 오가며 서로 이해가 맞춰지는 흐름",
    },
    "consistency": {
        "핵심 느낌": "앞뒤가 흔들리지 않고 같은 기준을 유지함",
    },
    "continuity": {
        "핵심 느낌": "끊기지 않고 흐름이 이어지는 상태",
    },
    "contribution": {
        "핵심 뜻": "기여 / 보탠 몫",
        "핵심 느낌": "전체 결과에 내 몫을 얹는 것",
    },
    "coordination": {
        "핵심 뜻": "조율 / 조정",
        "핵심 느낌": "여러 사람과 요소를 한 박자로 맞추는 일",
    },
    "discussion": {
        "핵심 느낌": "의견을 주고받으며 쟁점을 좁혀 가는 과정",
    },
    "documentation": {
        "핵심 뜻": "문서화 / 기록 자료",
        "핵심 느낌": "나중에 확인하게 근거와 과정을 문서로 남기는 것",
    },
    "effectiveness": {
        "핵심 뜻": "효과성 / 목표 달성도",
        "핵심 느낌": "실제로 원하는 결과를 내는 힘",
    },
    "enhancement": {
        "핵심 뜻": "향상 / 개선",
        "핵심 느낌": "이미 있는 것을 한 단계 더 좋게 끌어올림",
    },
    "explanation": {
        "핵심 뜻": "설명 / 풀이",
        "핵심 느낌": "낯선 내용을 이해되게 풀어 주는 것",
    },
    "feasibility": {
        "핵심 뜻": "실행 가능성",
        "핵심 느낌": "아이디어가 현실에서 실제로 굴러갈 수 있는 정도",
    },
    "implementation": {
        "핵심 뜻": "실행 / 구현",
        "핵심 느낌": "계획을 말에서 끝내지 않고 실제로 돌리는 단계",
    },
    "instruction": {
        "핵심 뜻": "지시 / 안내",
        "핵심 느낌": "무엇을 어떻게 할지 방향을 짚어 주는 말",
    },
    "interaction": {
        "핵심 뜻": "상호작용",
        "핵심 느낌": "한쪽이 아니라 주고받으며 서로 영향을 주는 흐름",
    },
    "interpretation": {
        "핵심 뜻": "해석",
        "핵심 느낌": "같은 자료에서도 무슨 뜻인지 읽어내는 방식",
    },
    "organization": {
        "핵심 뜻": "구성 / 조직",
        "핵심 느낌": "흩어진 것을 순서와 틀 안에 묶어 세우는 것",
    },
    "participation": {
        "핵심 뜻": "참여 / 관여",
        "핵심 느낌": "구경꾼이 아니라 과정 안으로 직접 들어감",
    },
    "preparation": {
        "핵심 뜻": "준비 / 사전 대비",
        "핵심 느낌": "본게임 전에 필요한 걸 미리 갖춰 두는 단계",
    },
    "prioritization": {
        "핵심 뜻": "우선순위화 / 먼저 할 것 정하기",
        "핵심 느낌": "다 할 수 없을 때 먼저 손댈 것을 고르는 일",
    },
    "revision": {
        "핵심 뜻": "수정 / 재검토",
        "핵심 느낌": "초안을 다시 보며 더 낫게 고치는 과정",
    },
}

TARGETS = [
    ROOT / "toefl_ets_2026_set_07.tsv",
    ROOT / "toefl_ets_2026_set_08.tsv",
]


def main() -> int:
    changed = 0
    for path in TARGETS:
        rows = []
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            for headword, back in reader:
                lines = back.split("\n")
                if headword in UPDATES:
                    new_lines = []
                    for line in lines:
                        label, _, value = line.partition(":")
                        if label in UPDATES[headword]:
                            updated = f"{label}: {UPDATES[headword][label]}"
                            if updated != line:
                                changed += 1
                            new_lines.append(updated)
                        else:
                            new_lines.append(line)
                    rows.append([headword, "\n".join(new_lines)])
                else:
                    rows.append([headword, back])

        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerows(rows)

    print(f"changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
