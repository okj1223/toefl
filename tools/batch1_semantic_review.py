#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


RENAMES = {
    "toefl_awl_set_01.tsv": {
        "analyse": "analyze",
        "labour": "labor",
        "maximise": "maximize",
    }
}


REPLACEMENTS = {
    "toefl_awl_set_01.tsv": {
        "analyze": "핵심 뜻: 분석하다\n구분: analyze=구조·원인을 분석하다 / examine=면밀히 살피다 / assess=가치·수준을 평가하다",
        "administrate": "핵심 뜻: 관리하다 / 운영하다\n구분: administrate=행정적으로 관리·운영하다 / administer=관리·집행하다",
        "positive": "핵심 뜻: 긍정적인 / 양의\n구분: positive=긍정적이거나 양의 값인 / favorable=상황이 유리한 / negative=반대 방향·음의",
        "maximize": "핵심 뜻: 극대화하다\n구분: maximize=가능한 한 크게 하다 / increase=늘리다 / optimize=가장 좋게 조정하다",
    },
    "toefl_ets_2026_set_01.tsv": {
        "beneficial": "핵심 뜻: 유익한\n구분: beneficial=실질적 이익이 되는 / helpful=도움이 되는 / favorable=유리한",
        "comparative": "핵심 뜻: 비교의\n구분: comparative=비교를 바탕으로 한 / relative=상대적인 / contrasting=대조적인",
        "conserve": "핵심 뜻: 보존하다 / 절약하다\n구분: conserve=보존·절약하다 / preserve=손상 없이 보존하다",
        "contaminate": "핵심 뜻: 오염시키다\n구분: contaminate=오염시키다 / pollute=환경을 오염시키다 / corrupt=질을 해치다",
        "cumulative": "핵심 뜻: 누적되는\n구분: cumulative=차곡차곡 누적되는 / collective=집단의 / aggregate=합산된",
        "detrimental": "핵심 뜻: 해로운\n구분: detrimental=손해를 주는 / harmful=해로운 / unfavorable=불리한",
        "integral": "핵심 뜻: 필수적인 / 전체를 이루는\n구분: integral=전체에 꼭 필요한 / essential=필수적인 / included=포함된",
        "resolve": "핵심 뜻: 해결하다 / 결심하다\n구분: resolve=문제를 해결하거나 결심하다 / settle=정리하다 / determine=결정하다",
        "strategy": "핵심 뜻: 전략\n구분: strategy=큰 방향의 전략 / tactic=구체적 전술 / policy=정책",
        "sufficient": "핵심 뜻: 충분한\n구분: sufficient=필요 수준을 충족하는 / adequate=간신히 충분한 / abundant=풍부한",
        "temporal": "핵심 뜻: 시간의\n구분: temporal=시간과 관련된 / temporary=일시적인 / spatial=공간의",
    },
    "toefl_ets_2026_set_02.tsv": {
        "accommodate": "핵심 뜻: 수용하다 / 맞추다",
        "amplify": "핵심 뜻: 증폭하다 / 확대하다",
        "circumvent": "핵심 뜻: 우회하다 / 피하다",
        "cultivate": "핵심 뜻: 기르다 / 함양하다",
        "derive": "핵심 뜻: 얻다 / 도출하다",
        "disrupt": "핵심 뜻: 방해하다 / 혼란시키다",
        "facilitate": "핵심 뜻: 촉진하다 / 용이하게 하다\n구분: facilitate=과정을 쉽게 만들다 / accelerate=속도를 높이다",
        "foster": "핵심 뜻: 촉진하다 / 길러 내다\n구분: foster=성장하도록 북돋우다 / facilitate=진행을 쉽게 하다",
        "reconcile": "핵심 뜻: 조화시키다 / 일치시키다",
        "regulate": "핵심 뜻: 규제하다 / 조절하다\n구분: regulate=규칙이나 기준으로 조절하다 / monitor=지켜보다",
        "adaptation": "핵심 뜻: 적응 / 각색",
        "allocation": "핵심 뜻: 할당 / 배분",
        "archive": "핵심 뜻: 기록 보관소 / 보관하다",
        "attribute": "핵심 뜻: 속성 / ~의 탓으로 돌리다\n구분: attribute=속성이거나 원인을 돌리다 / trait=특성 / ascribe=~의 탓으로 돌리다",
        "capacity": "핵심 뜻: 수용력 / 능력",
        "coherence": "핵심 뜻: 일관성 / 응집성\n구분: coherence=내용이 논리적으로 이어짐 / cohesion=표현이 매끄럽게 연결됨",
        "compensation": "핵심 뜻: 보상 / 보수",
        "configuration": "핵심 뜻: 구성 / 배열",
        "correlation": "핵심 뜻: 상관관계\n구분: correlation=함께 움직이는 관련성 / causation=원인과 결과 관계",
        "criterion": "핵심 뜻: 기준\n구분: criterion=판단 기준 하나 / standard=일반적 표준",
        "deficiency": "핵심 뜻: 결핍 / 부족",
        "distinction": "핵심 뜻: 구별 / 차이",
        "emergence": "핵심 뜻: 출현 / 부상",
        "evolution": "핵심 뜻: 진화 / 점진적 변화",
        "implication": "핵심 뜻: 함의 / 영향",
        "indicator": "핵심 뜻: 지표 / 신호",
        "integrity": "핵심 뜻: 정직성 / 완전성",
        "threshold": "핵심 뜻: 문턱 / 기준점\n구분: threshold=판정이 바뀌는 기준선 / limit=허용 한계",
        "accountable": "핵심 뜻: 책임이 있는\n구분: accountable=결과를 설명할 책임이 있는 / responsible=책임 있는",
        "apparent": "핵심 뜻: 분명해 보이는 / 겉으로 드러난\n구분: apparent=겉으로 분명해 보이는 / actual=실제의",
        "coherent": "핵심 뜻: 일관된 / 조리 있는",
        "deficient": "핵심 뜻: 부족한 / 결핍된",
        "dominant": "핵심 뜻: 지배적인 / 우세한",
        "durable": "핵심 뜻: 오래가는 / 내구성 있는",
        "fundamental": "핵심 뜻: 근본적인 / 필수적인",
        "implicit": "핵심 뜻: 암묵적인\n구분: implicit=직접 말하지 않고 깔린 / explicit=명시적인",
        "legitimate": "핵심 뜻: 정당한 / 합법적인",
        "viable": "핵심 뜻: 실행 가능한 / 존속 가능한\n구분: viable=실행 가능하고 지속될 수 있는 / feasible=당장 해볼 수 있는",
        "arguably": "핵심 뜻: 논리적으로 보면 / 어쩌면",
        "largely": "핵심 뜻: 대체로 / 주로",
        "notably": "핵심 뜻: 특히 / 두드러지게",
        "typically": "핵심 뜻: 보통 / 전형적으로",
    },
}


def main() -> int:
    changed_files = 0
    changed_rows = 0
    for rel in ["toefl_awl_set_01.tsv", "toefl_ets_2026_set_01.tsv", "toefl_ets_2026_set_02.tsv"]:
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
                front = RENAMES.get(rel, {}).get(front, front)
                new_back = REPLACEMENTS.get(rel, {}).get(front, back)
                if front != row[0] or new_back != back:
                    changed = True
                    changed_rows += 1
                rows.append([front, new_back])
        if changed:
            changed_files += 1
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter="\t", lineterminator="\n")
                writer.writerows(rows)
    print(f"changed_files={changed_files} changed_rows={changed_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
