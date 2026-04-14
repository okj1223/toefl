#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REPLACEMENTS = {
    "toefl_ets_2026_set_09.tsv": {
        "utilization": "핵심 뜻: 활용 / 이용\n구분: utilization=실제로 활용되는 정도 / usage=사용 방식·빈도 / application=구체적 적용",
        "decision": "핵심 뜻: 결정 / 판단\n구분: decision=선택 후 내린 결론 / choice=선택지 또는 선택 행위 / judgment=판단력·판정",
        "trajectory": "핵심 뜻: 진행 경로 / 궤적",
        "magnitude": "핵심 뜻: 규모 / 크기",
        "rotation": "핵심 뜻: 회전 / 자전",
        "deposition": "핵심 뜻: 퇴적 / 침착",
        "fracture": "핵심 뜻: 균열 / 파쇄",
        "legible": "핵심 뜻: 읽기 쉬운 / 판독 가능한",
        "terrain": "핵심 뜻: 지형 / 지대",
        "aerosol": "핵심 뜻: 에어로졸 / 공기 중 미세입자",
        "emission": "핵심 뜻: 배출 / 방출",
    },
    "toefl_ets_2026_set_10.tsv": {
        "abstain": "핵심 뜻: 삼가다 / 기권하다\n구분: abstain=의식적으로 삼가거나 기권하다 / refrain=행동을 참다 / avoid=피하다",
        "acclaim": "핵심 뜻: 찬사 / 호평\n구분: acclaim=널리 받는 찬사 / praise=칭찬 / applause=박수갈채",
        "accrue": "핵심 뜻: 누적되다 / 쌓이다\n구분: accrue=시간 따라 누적되다 / accumulate=모아 쌓다 / amass=많이 모으다",
        "adversarial": "핵심 뜻: 대립적인",
        "amenable": "핵심 뜻: 순응하는 / 수용적인",
        "analog": "핵심 뜻: 대응물 / 유사한 것",
        "appraisal": "핵심 뜻: 평가 / 감정",
        "augment": "핵심 뜻: 늘리다 / 보강하다",
        "contemplation": "핵심 뜻: 숙고 / 깊은 생각",
        "conviction": "핵심 뜻: 확신 / 신념",
        "curtail": "핵심 뜻: 줄이다 / 제한하다",
        "depict": "핵심 뜻: 묘사하다 / 그려내다",
        "deviation": "핵심 뜻: 편차 / 일탈",
        "dilemma": "핵심 뜻: 딜레마 / 진퇴양난",
        "discern": "핵심 뜻: 분별하다 / 알아차리다",
        "disclose": "핵심 뜻: 공개하다 / 드러내다",
        "discretion": "핵심 뜻: 재량 / 신중함",
        "divert": "핵심 뜻: 다른 데로 돌리다 / 전환하다",
        "doctrine": "핵심 뜻: 교리 / 원칙",
        "endorsement": "핵심 뜻: 지지 / 승인",
        "impetus": "핵심 뜻: 추진력 / 계기",
        "insulate": "핵심 뜻: 차단하다 / 격리하다",
        "inventory": "핵심 뜻: 재고 / 목록",
        "meticulous": "핵심 뜻: 꼼꼼한 / 세심한",
        "nominal": "핵심 뜻: 명목상의 / 이름뿐인",
        "novelty": "핵심 뜻: 새로움 / 참신함",
        "paramount": "핵심 뜻: 가장 중요한 / 최우선의",
        "permeate": "핵심 뜻: 스며들다 / 퍼지다",
        "pertinent": "핵심 뜻: 관련 있는 / 적절한",
        "procure": "핵심 뜻: 조달하다 / 확보하다",
    },
    "toefl_ets_2026_set_11.tsv": {
        "deliverable": "핵심 뜻: 제출 산출물 / 결과물\n구분: deliverable=제출 가능한 산출물 / outcome=결과 일반 / output=생산된 결과물",
        "milestone": "핵심 뜻: 이정표 / 중요한 단계\n구분: milestone=중요한 중간 성취점 / checkpoint=점검 지점 / deadline=마감 시점",
        "progress": "핵심 뜻: 진전 / 발전\n구분: progress=목표 방향의 진전 / improvement=질적 향상",
        "intrusion": "핵심 뜻: 침범 / 끼어듦",
        "proposal": "핵심 뜻: 제안 / 제안서",
        "review": "핵심 뜻: 검토 / 재검토하다\n구분: review=다시 검토·평가 / evaluate=기준에 따라 평가 / revise=검토 후 고치다",
        "teamwork": "핵심 뜻: 팀워크 / 협업\n구분: teamwork=팀 단위 협업 / collaboration=공동 작업 / cooperation=협조",
        "variance": "핵심 뜻: 분산 / 변동",
        "reflection": "핵심 뜻: 성찰 / 되돌아보기",
        "foundational": "핵심 뜻: 기초가 되는 / 토대의",
        "recommendation": "핵심 뜻: 권고 / 추천",
        "preservation": "핵심 뜻: 보존 / 유지",
        "comparison": "핵심 뜻: 비교 / 대조",
        "recharge": "핵심 뜻: 다시 채우다 / 재충전되다",
        "replenish": "핵심 뜻: 다시 채우다 / 보충하다",
        "guidance": "핵심 뜻: 지도 / 안내",
        "orientation": "핵심 뜻: 방향 설정 / 오리엔테이션",
        "stewardship": "핵심 뜻: 책임 있는 관리 / 보전 관리",
        "thaw": "핵심 뜻: 녹다 / 해빙되다",
        "adjustment": "핵심 뜻: 조정 / 수정",
        "observational": "핵심 뜻: 관찰 기반의 / 관찰용의",
    },
    "toefl_ets_2026_set_12.tsv": {
        "awareness": "핵심 뜻: 인식 / 자각\n구분: awareness=알아차리고 의식하는 상태 / attention=한 대상에 주의를 모음",
        "belief": "핵심 뜻: 믿음 / 신념\n구분: belief=사실처럼 받아들이는 믿음 / assumption=검증 전 가정",
        "emotion": "핵심 뜻: 감정",
        "expectation": "핵심 뜻: 기대 / 예상\n구분: expectation=앞으로 그렇게 될 거라는 예상 / hope=바라는 마음",
        "judgment": "핵심 뜻: 판단\n구분: judgment=따져 본 뒤 내린 판단 / opinion=의견",
        "recognition": "핵심 뜻: 인식 / 알아봄\n구분: recognition=보고 알아봄 / recall=단서 없이 떠올림",
        "withdrawal": "핵심 뜻: 철회 / 물러남",
        "confidence": "핵심 뜻: 자신감 / 확신\n구분: confidence=해낼 수 있다는 자신감 / certainty=사실이라고 보는 확실성",
        "discipline": "핵심 뜻: 자기절제 / 규율",
    },
}


def main() -> int:
    targets = [
        "toefl_ets_2026_set_09.tsv",
        "toefl_ets_2026_set_10.tsv",
        "toefl_ets_2026_set_11.tsv",
        "toefl_ets_2026_set_12.tsv",
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
                new_back = REPLACEMENTS.get(rel, {}).get(front, back)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
