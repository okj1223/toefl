#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


CARDS = [
    ("awareness", "인식 / 자각"),
    ("arousal", "각성 / 흥분 상태"),
    ("attachment", "애착 / 강한 정서적 유대"),
    ("aversion", "혐오 / 강한 기피감"),
    ("behavioral", "행동의 / 행동과 관련된"),
    ("belief", "믿음 / 신념"),
    ("burnout", "번아웃 / 소진 상태"),
    ("concentration", "집중 / 정신을 모으기"),
    ("conformity", "동조 / 집단 규범을 따름"),
    ("curiosity", "호기심 / 알고 싶어 하는 마음"),
    ("deliberation", "숙고 / 신중한 검토"),
    ("dependency", "의존성 / 기대어 있는 상태"),
    ("distraction", "주의 산만 / 집중을 빼앗는 것"),
    ("emotion", "감정 / 정서"),
    ("empathy", "공감 / 타인의 감정을 이해함"),
    ("expectation", "기대 / 예상"),
    ("framing", "틀 짓기 / 제시 방식"),
    ("gratification", "만족감 / 욕구 충족"),
    ("habit", "습관 / 반복된 행동 패턴"),
    ("identity", "정체성 / 자기 인식"),
    ("impulsive", "충동적인 / 즉흥적으로 반응하는"),
    ("intention", "의도 / 하려는 마음"),
    ("judgment", "판단 / 분별"),
    ("learning", "학습 / 경험을 통한 습득"),
    ("memory", "기억 / 저장된 정보"),
    ("mindfulness", "마음챙김 / 현재에 주의를 두는 태도"),
    ("misconception", "오해 / 잘못된 개념"),
    ("aspiration", "열망 / 더 높은 목표를 향한 바람"),
    ("personality", "성격 / 개인의 비교적 안정된 특성"),
    ("preference", "선호 / 더 좋아하는 선택 경향"),
    ("priming", "점화 효과 / 미리 준 자극의 영향"),
    ("reasoning", "추론 / 논리적으로 따져 생각하기"),
    ("recognition", "인식 / 알아봄"),
    ("self-control", "자기통제 / 충동을 누르고 조절함"),
    ("self-regulation", "자기조절 / 감정과 행동을 스스로 관리함"),
    ("self-esteem", "자존감 / 스스로에 대한 가치감"),
    ("strain", "부담 / 긴장과 압박"),
    ("temperament", "기질 / 타고난 정서·반응 성향"),
    ("tendency", "경향 / 자주 그쪽으로 기우는 성향"),
    ("uncertainty", "불확실성 / 확신하기 어려운 상태"),
    ("willpower", "의지력 / 스스로 버티며 선택을 지키는 힘"),
    ("withdrawal", "철회 / 물러남"),
    ("attribution", "원인 귀속 / 이유를 어디에 돌리는 해석"),
    ("avoidance", "회피 / 피하려는 행동"),
    ("commitment", "헌신 / 계속 책임지려는 약속"),
    ("conditioning", "조건형성 / 자극과 반응이 연결되는 학습"),
    ("confidence", "자신감 / 확신"),
    ("coping", "대처 / 스트레스나 문제를 다루는 방식"),
    ("disengagement", "이탈 / 관여를 거두는 상태"),
    ("expectancy", "기대치 / 결과를 예상하는 믿음"),
    ("fixation", "고착 / 한 대상이나 생각에 지나치게 묶임"),
    ("attentiveness", "주의 깊음 / 집중해서 살피는 태도"),
    ("frustration", "좌절감 / 막힘에서 오는 불만"),
    ("habituation", "습관화 / 반복 노출로 반응이 약해짐"),
    ("imitation", "모방 / 남의 행동을 따라함"),
    ("inferential", "추론적인 / 단서로 결론을 끌어내는"),
    ("inhibition", "억제 / 반응이나 행동을 눌러 막음"),
    ("introspection", "내성 / 자기 생각과 감정을 들여다봄"),
    ("intuition", "직관 / 즉각적으로 떠오르는 판단감"),
    ("optimism", "낙관주의 / 좋은 결과를 기대하는 경향"),
    ("pessimism", "비관주의 / 나쁜 결과를 예상하는 경향"),
    ("persuasion", "설득 / 생각이나 태도를 바꾸게 함"),
    ("rationalization", "합리화 / 그럴듯한 이유를 붙여 정당화함"),
    ("reinforcement", "강화 / 보상으로 행동을 더 굳히기"),
    ("reward", "보상 / 좋은 결과로 행동을 강화하는 것"),
    ("rumination", "반추 / 같은 생각을 반복해 곱씹음"),
    ("situational", "상황적인 / 맥락에 좌우되는"),
    ("socialization", "사회화 / 사회 규범과 역할을 익히는 과정"),
    ("threat", "위협 / 위험 신호"),
    ("vigilance", "경계심 / 주의를 유지하며 살피는 태도"),
    ("workload", "업무량 / 처리해야 할 일의 부담"),
    ("choice", "선택 / 여러 대안 중 고름"),
    ("impulse", "충동 / 즉각 튀어나오는 욕구나 반응"),
    ("meaning", "의미 / 어떤 것이 지니는 뜻"),
    ("pattern", "패턴 / 반복적으로 나타나는 구조"),
    ("risk", "위험 / 손실 가능성"),
    ("self-directed", "자기주도적인 / 스스로 방향을 정하는"),
    ("goal-oriented", "목표 지향적인 / 목표 달성에 초점을 둔"),
    ("task-focused", "과제 중심의 / 해야 할 일에 초점을 둔"),
    ("value-based", "가치 기반의 / 기준 가치에 따라 판단하는"),
    ("uncertainty-reduction", "불확실성 감소 / 모호함을 줄이기"),
    ("agency", "주체성 / 스스로 행동을 선택하는 힘"),
    ("ambition", "야망 / 더 높은 목표를 이루려는 욕구"),
    ("appetite", "욕구 / 강한 선호나 식욕"),
    ("assertion", "단언 / 자신 있게 내세우는 주장"),
    ("association", "연상 / 둘 사이의 연결"),
    ("calm", "차분함 / 안정된 상태"),
    ("delay", "지연 / 늦춤"),
    ("desire", "욕구 / 강하게 원함"),
    ("discipline", "자기절제 / 규율"),
    ("drive", "추진력 / 강한 동기"),
    ("engagement", "몰입 / 적극적 관여"),
    ("exposure", "노출 / 자극이나 경험에 접함"),
    ("fatigue", "피로 / 지친 상태"),
    ("flexibility", "유연성 / 상황에 맞게 바꿀 수 있음"),
    ("independence", "독립성 / 스스로 판단하고 행동함"),
    ("instinct", "본능 / 거의 자동적으로 나오는 반응"),
    ("mood", "기분 / 비교적 지속되는 정서 상태"),
    ("patience", "인내심 / 기다리며 버티는 힘"),
    ("restraint", "자제 / 충동을 억누름"),
]


VERBS = set()


ADJECTIVES = {
    "behavioral",
    "impulsive",
    "inferential",
    "situational",
    "self-directed",
    "goal-oriented",
    "task-focused",
    "value-based",
}


def build_back(word: str, core: str) -> str:
    if word in VERBS:
        return "\n".join(
            [
                f"핵심 뜻: {core}",
                f"부가 뜻: 주의를 한곳에 모으다 / 핵심 대상에 초점을 맞추다",
                f"핵심 느낌: 주변 잡음을 줄이고 중요한 한 지점으로 시선을 모으는 느낌",
                f"구분: {word}=주의를 집중 / concentrate=정신을 모음 / attend=주의를 기울임",
            ]
        )
    if word in ADJECTIVES:
        return "\n".join(
            [
                f"핵심 뜻: {core}",
                f"부가 뜻: 그런 성향이나 기준을 가진 / 특정 맥락에서 그렇게 작동하는",
                f"핵심 느낌: 판단이나 행동이 {core} 쪽으로 기울어 있는 느낌",
                f"구분: {word}=그 성질을 직접 나타냄 / cognitive=사고 과정 관련 / emotional=감정 반응 관련",
            ]
        )
    return "\n".join(
        [
            f"핵심 뜻: {core}",
            f"부가 뜻: 심리 상태·행동 경향·판단 과정에서 나타나는 관련 의미",
            f"핵심 느낌: 사람의 생각과 행동이 {core} 쪽으로 움직이는 방식을 잡는 느낌",
            f"구분: {word}=해당 심리·행동 개념 / attitude=태도 / behavior=겉으로 드러난 행동",
        ]
    )


def main() -> int:
    existing = set(Path("all_headwords.txt").read_text(encoding="utf-8").split())
    rows = []
    for word, core in CARDS:
        if word in existing:
            raise RuntimeError(f"duplicate headword: {word}")
        rows.append([word, build_back(word, core)])
    if len(rows) != 100:
        raise RuntimeError(f"expected 100 rows, got {len(rows)}")

    with Path("toefl_ets_2026_set_12.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    print("written toefl_ets_2026_set_12.tsv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
