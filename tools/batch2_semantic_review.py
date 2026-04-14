#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


RENAMES = {
    "toefl_awl_set_02.tsv": {
        "licence": "license",
        "utilise": "utilize",
    },
    "toefl_awl_set_03.tsv": {
        "minimise": "minimize",
    },
}


REPLACEMENTS = {
    "toefl_awl_set_02.tsv": {
        "academy": "핵심 뜻: 학계 / 학술 기관\n구분: academy=학계·학술 기관 / school=학교 일반 / institute=전문 기관",
        "challenge": "핵심 뜻: 도전 과제 / 이의를 제기하다\n구분: challenge=도전 과제이거나 이의를 제기하다 / difficulty=어려움 / dispute=반박하다",
        "implicate": "핵심 뜻: 연루시키다 / 함축하다\n구분: implicate=연루나 함의를 시사하다 / imply=암시하다 / accuse=고발하다",
        "prime": "핵심 뜻: 주요한 / 준비시키다\n구분: prime=주요하거나 미리 준비시키다 / primary=주요한 / prepare=준비하다",
        "license": "핵심 뜻: 면허 / 허가\n구분: license=공식 허가·면허 / permit=허가증 / freedom=자유",
        "file": "핵심 뜻: 파일 / 제출하다\n구분: file=자료 파일이거나 공식 제출하다 / document=문서 / submit=제출하다",
        "classic": "핵심 뜻: 고전적인 / 전형적인\n구분: classic=고전의 가치가 있거나 전형적인 / classical=고전 시대의·고전주의의 / typical=전형적인",
        "utilize": "핵심 뜻: 활용하다\n구분: utilize=자원·방법을 활용하다 / use=쓰다 일반 / apply=특정 목적에 적용하다",
        "globe": "핵심 뜻: 지구 / 전 세계\n구분: globe=지구 또는 전 세계 / earth=지구 / world=세계",
        "ultimate": "핵심 뜻: 궁극적인 / 최종의\n구분: ultimate=궁극적이거나 최종적인 / final=마지막의 / fundamental=근본적인",
    },
    "toefl_awl_set_03.tsv": {
        "prospect": "핵심 뜻: 전망 / 가능성\n구분: prospect=미래 전망·가능성 / outlook=전망 / possibility=가능성",
        "manual": "핵심 뜻: 설명서 / 수동의\n구분: manual=설명서이거나 수동의 / handbook=안내서 / automatic=자동의",
        "medium": "핵심 뜻: 매체 / 수단\n구분: medium=전달 매체나 수단 / method=방법 / environment=주변 환경",
        "minimize": "핵심 뜻: 최소화하다\n구분: minimize=가능한 한 줄이다 / reduce=줄이다 / downplay=덜 중요하게 보이게 하다",
        "vehicle": "핵심 뜻: 수단 / 매개체 / 차량\n구분: vehicle=운반 수단이나 전달 매개 / transport=운송 수단 / medium=매체",
        "likewise": "핵심 뜻: 마찬가지로 / 또한\n구분: likewise=마찬가지로 / similarly=유사하게 / also=또한",
    },
    "toefl_ets_2026_set_03.tsv": {
        "adjacent": "핵심 뜻: 인접한\n구분: adjacent=바로 옆의 / nearby=가까운 / neighboring=이웃한",
        "alter": "핵심 뜻: 바꾸다\n구분: alter=바꾸다 / modify=부분 수정하다 / transform=크게 바꾸다",
        "considerable": "핵심 뜻: 상당한\n구분: considerable=상당한 규모의 / substantial=실질적으로 큰",
        "definite": "핵심 뜻: 분명한\n구분: definite=분명한 / certain=확실한 / specific=구체적인",
        "explicit": "핵심 뜻: 명시적인\n구분: explicit=분명히 드러난 / implicit=암묵적인 / specific=구체적인",
        "hence": "핵심 뜻: 따라서\n구분: hence=따라서 / therefore=그러므로 / thus=그리하여",
        "overall": "핵심 뜻: 전체적인 / 전반적으로",
    },
    "toefl_ets_2026_set_04.tsv": {
        "access": "핵심 뜻: 접근 / 이용할 수 있음\n구분: access=접근하거나 이용할 수 있음 / entrance=들어가는 입구 / permission=허가",
        "aid": "핵심 뜻: 돕다 / 도움\n구분: aid=도움을 주거나 도움 / assist=돕다 / relief=구호",
        "commission": "핵심 뜻: 위원회 / 의뢰하다\n구분: commission=위원회를 구성하거나 일을 맡기다 / committee=위원회 / assign=맡기다",
        "confer": "핵심 뜻: 수여하다 / 협의하다\n구분: confer=공식 수여하거나 협의하다 / grant=주다 / discuss=논의하다",
        "display": "핵심 뜻: 보여 주다 / 전시하다\n구분: display=보여 주거나 전시하다 / exhibit=전시하다 / reveal=드러내다",
        "dispose": "핵심 뜻: 처리하다 / 배치하다\n구분: dispose=처리하거나 배치하다 / discard=버리다 / arrange=배치하다",
        "fund": "핵심 뜻: 기금 / 자금을 대다\n구분: fund=기금이거나 자금 지원하다 / finance=재정 조달하다 / sponsor=후원하다",
        "label": "핵심 뜻: 꼬리표 / 분류하다\n구분: label=이름 붙이거나 분류하다 / classify=분류하다 / identify=확인하다",
        "permit": "핵심 뜻: 허용하다 / 허가증\n구분: permit=허용하거나 허가증 / allow=허용하다 / authorize=공식 허가하다",
        "quote": "핵심 뜻: 인용하다 / 인용문\n구분: quote=인용하거나 인용문 / cite=출처를 언급하다 / mention=언급하다",
        "sustain": "핵심 뜻: 유지하다 / 지탱하다\n구분: sustain=지속시키거나 지탱하다 / maintain=유지하다 / support=떠받치다",
    },
}


def main() -> int:
    targets = [
        "toefl_awl_set_02.tsv",
        "toefl_awl_set_03.tsv",
        "toefl_ets_2026_set_03.tsv",
        "toefl_ets_2026_set_04.tsv",
    ]
    changed_files = 0
    changed_rows = 0

    for rel in targets:
        path = ROOT / rel
        rows = []
        changed = False
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if len(row) != 2:
                    rows.append(row)
                    continue
                front, back = row
                new_front = RENAMES.get(rel, {}).get(front, front)
                new_back = REPLACEMENTS.get(rel, {}).get(new_front, back)
                if new_front != front or new_back != back:
                    changed = True
                    changed_rows += 1
                rows.append([new_front, new_back])
        if changed:
            changed_files += 1
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter="\t", lineterminator="\n")
                writer.writerows(rows)

    print(f"changed_files={changed_files} changed_rows={changed_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
