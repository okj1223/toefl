#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REPLACEMENTS = {
    "toefl_ets_2026_set_05.tsv": {
        "austerity": "핵심 뜻: 긴축 정책 / 긴축",
        "deficit": "핵심 뜻: 적자 / 부족분\n구분: deficit=적자·부족분 / surplus=남는 몫·흑자",
        "surplus": "핵심 뜻: 흑자 / 잉여분\n구분: surplus=남는 몫·흑자 / deficit=부족분·적자",
        "concession": "핵심 뜻: 양보\n구분: concession=한발 물러선 양보 / compromise=서로 조금씩 물러섬",
        "fiscal": "핵심 뜻: 재정의\n구분: fiscal=정부 재정과 예산의 / monetary=통화와 화폐의",
        "monetary": "핵심 뜻: 통화의\n구분: monetary=통화와 화폐의 / fiscal=정부 재정과 예산의",
        "liability": "핵심 뜻: 부채 / 법적 책임\n구분: liability=부채·법적 책임 / asset=자산",
        "dividend": "핵심 뜻: 배당금",
        "speculate": "핵심 뜻: 투기하다 / 추측하다",
        "depreciate": "핵심 뜻: 가치가 하락하다 / 감가상각하다",
        "collateral": "핵심 뜻: 담보 / 부수적 피해",
        "default": "핵심 뜻: 채무 불이행",
        "acquisition": "핵심 뜻: 인수 / 취득",
        "constitution": "핵심 뜻: 헌법 / 구성",
        "legislation": "핵심 뜻: 입법 / 법률",
        "mandate": "핵심 뜻: 권한 / 명령하다",
        "veto": "핵심 뜻: 거부권 / 거부하다",
        "coalition": "핵심 뜻: 연합 / 연립",
        "incumbent": "핵심 뜻: 현직자 / 현직의",
        "ballot": "핵심 뜻: 투표용지 / 투표",
        "treaty": "핵심 뜻: 조약\n구분: treaty=국가 간 조약 / agreement=합의 일반",
        "mediate": "핵심 뜻: 중재하다\n구분: mediate=양측을 중재하다 / arbitrate=판단을 내려 재정하다",
        "verdict": "핵심 뜻: 평결",
        "convict": "핵심 뜻: 유죄 판결하다",
        "prosecution": "핵심 뜻: 기소 / 검찰 측",
        "indictment": "핵심 뜻: 기소 / 기소장",
        "testimony": "핵심 뜻: 증언",
        "accountability": "핵심 뜻: 책임성 / 설명 책임\n구분: accountability=결과를 설명하고 책임지는 의무 / responsibility=책임 일반",
        "corruption": "핵심 뜻: 부패",
        "fraud": "핵심 뜻: 사기 / 부정행위",
        "amendment": "핵심 뜻: 수정안 / 개정",
        "delegate": "핵심 뜻: 대표 / 위임하다",
        "electorate": "핵심 뜻: 유권자 집단",
        "governance": "핵심 뜻: 통치 / 운영 체계",
        "authority": "핵심 뜻: 권위 / 권한",
        "revenue": "핵심 뜻: 수입 / 세입",
        "expenditure": "핵심 뜻: 지출",
        "asset": "핵심 뜻: 자산 / 강점",
        "quota": "핵심 뜻: 할당량",
        "comply": "핵심 뜻: 준수하다",
        "authorize": "핵심 뜻: 승인하다 / 권한을 부여하다",
        "denounce": "핵심 뜻: 규탄하다 / 비난하다",
        "rationale": "핵심 뜻: 근거 / 논리",
    },
    "toefl_ets_2026_set_06.tsv": {
        "affiliation": "핵심 뜻: 소속 / 제휴",
        "ancestry": "핵심 뜻: 혈통 / 조상 계통",
        "cohort": "핵심 뜻: 동질 집단 / 동기 집단",
        "custom": "핵심 뜻: 관습",
        "demographic": "핵심 뜻: 인구 통계의",
        "diffuse": "핵심 뜻: 퍼뜨리다 / 확산시키다",
        "ethnic": "핵심 뜻: 민족의",
        "gender": "핵심 뜻: 젠더 / 성별\n구분: gender=사회적·정체성 차원의 성 / sex=생물학적 성별",
        "heritage": "핵심 뜻: 유산 / 문화유산",
        "homogeneous": "핵심 뜻: 동질적인",
        "infrastructure": "핵심 뜻: 기반 시설 / 인프라",
        "institution": "핵심 뜻: 제도 / 기관\n구분: institution=사회 제도 또는 기관 / organization=조직",
        "mortality": "핵심 뜻: 사망률",
        "municipality": "핵심 뜻: 지방자치단체",
        "narrative": "핵심 뜻: 서사 / 이야기",
        "population": "핵심 뜻: 인구 / 집단",
        "territory": "핵심 뜻: 영토 / 영역",
        "zone": "핵심 뜻: 구역 / 권역",
        "empirical": "핵심 뜻: 실증적인 / 경험적인\n구분: empirical=자료·관찰에 근거한 / theoretical=이론 중심의",
    },
    "toefl_ets_2026_set_07.tsv": {
        "acute": "핵심 뜻: 급성의 / 심각한\n구분: acute=갑작스럽고 심각한 / chronic=오랫동안 지속되는 / severe=심각한 정도",
        "susceptibility": "핵심 뜻: 취약성 / 민감성\n구분: susceptibility=영향받기 쉬운 취약성 / vulnerability=손상되기 쉬운 취약함",
        "adverse": "핵심 뜻: 해로운 / 불리한\n구분: adverse=해로운 결과를 낳는 / side effect=부수적 효과 / toxic=독성이 있는",
        "method": "핵심 뜻: 방법\n구분: method=체계적 방법 / approach=접근법 / technique=구체적 기법",
        "moderate": "핵심 뜻: 중간 정도의 / 완만한\n구분: moderate=중간 정도이거나 완만한 / mild=강도가 약한 / extreme=극단적인",
        "practical": "핵심 뜻: 실용적인 / 실제적인\n구분: practical=현실 적용 가능 / theoretical=이론 중심 / feasible=실행 가능",
        "transmission": "핵심 뜻: 전파 / 전달\n구분: transmission=전파 과정 / contagion=전염성 자체 / spread=확산(일반어)",
        "susceptible": "핵심 뜻: 취약한 / 영향받기 쉬운\n구분: susceptible=저항력 없이 영향받기 쉬운 / vulnerable=광범위하게 취약한 / prone=특정 것에 경향이 있는",
        "resistance": "핵심 뜻: 저항 / 내성\n구분: resistance=저항 또는 내성 / tolerance=내성(양 증가로 효과 감소)",
        "valid": "핵심 뜻: 타당한 / 유효한\n구분: valid=논리·기준상 타당한 / legitimate=정당하고 인정된 / reliable=일관되게 믿을 만한",
        "advancement": "핵심 뜻: 진전 / 향상",
        "alignment": "핵심 뜻: 정렬 / 일치",
        "applicability": "핵심 뜻: 적용 가능성",
        "assignment": "핵심 뜻: 과제 / 배정",
        "collaboration": "핵심 뜻: 협업 / 협력",
        "communication": "핵심 뜻: 의사소통 / 전달",
        "cognition": "핵심 뜻: 인지\n구분: cognition=사고·기억·판단 전반 / perception=감각 정보 해석",
        "continuity": "핵심 뜻: 연속성 / 지속성",
        "contribution": "핵심 뜻: 기여 / 기여분",
        "prevalence": "핵심 뜻: 유병률 / 만연\n구분: prevalence=현재 존재 비율 / incidence=새 발생 비율 / morbidity=질병률 전반",
    },
    "toefl_ets_2026_set_08.tsv": {
        "coordination": "핵심 뜻: 조율 / 조정",
        "competency": "핵심 뜻: 역량\n구분: competency=실제로 해낼 수 있는 역량 / proficiency=숙달 정도",
        "proficiency": "핵심 뜻: 숙달 / 능숙함",
        "retention": "핵심 뜻: 기억 유지\n구분: retention=배운 내용을 계속 유지함 / retrieval=기억을 다시 꺼냄",
        "retrieval": "핵심 뜻: 기억 인출\n구분: retrieval=저장된 기억을 꺼냄 / retention=배운 내용을 계속 유지함",
        "encode": "핵심 뜻: 부호화하다 / 기억에 입력하다",
        "schema": "핵심 뜻: 스키마 / 인지 틀",
        "motivation": "핵심 뜻: 동기",
        "feedback": "핵심 뜻: 피드백 / 반응",
        "benchmark": "핵심 뜻: 기준점 / 비교 기준",
        "inclusion": "핵심 뜻: 포용 / 통합 교육",
        "accommodation": "핵심 뜻: 조정 / 편의 제공",
        "simulation": "핵심 뜻: 시뮬레이션 / 모의 실험",
        "consolidate": "핵심 뜻: 공고히 하다 / 통합하다",
        "rehearsal": "핵심 뜻: 반복 연습 / 예행연습",
        "elaboration": "핵심 뜻: 정교화 / 상세화",
        "enhancement": "핵심 뜻: 향상 / 개선",
        "explanation": "핵심 뜻: 설명 / 풀이",
        "attention": "핵심 뜻: 주의 / 집중",
        "mindset": "핵심 뜻: 사고방식 / 마음가짐",
        "intrinsic": "핵심 뜻: 내재적인 / 본질적인\n구분: intrinsic=대상 안에 본래 들어 있는 / extrinsic=바깥 보상이나 조건에서 오는",
        "extrinsic": "핵심 뜻: 외재적인\n구분: extrinsic=바깥 보상이나 조건에서 오는 / intrinsic=대상 안에 본래 들어 있는",
        "synthesis": "핵심 뜻: 종합 / 통합",
        "evaluation": "핵심 뜻: 평가 / 판단",
        "performance": "핵심 뜻: 수행 / 성취도",
        "implementation": "핵심 뜻: 실행 / 구현",
        "instruction": "핵심 뜻: 지도 / 지시",
        "analogy": "핵심 뜻: 유추 / 비유",
        "organization": "핵심 뜻: 구성 / 조직",
        "participation": "핵심 뜻: 참여 / 관여",
        "situated": "핵심 뜻: 맥락에 놓인 / 상황적인",
        "quantitative": "핵심 뜻: 양적인 / 수치 기반의\n구분: quantitative=숫자와 수치 중심의 / qualitative=질적 특징 중심의",
        "sample": "핵심 뜻: 표본\n구분: sample=전체를 대표하도록 뽑은 일부 / population=전체 모집단",
        "variable": "핵심 뜻: 변수 / 변인\n구분: variable=값이 달라지는 요소 / constant=고정된 값",
        "disposition": "핵심 뜻: 성향 / 경향",
        "exemplar": "핵심 뜻: 전형적 사례 / 모범 사례",
        "representation": "핵심 뜻: 표상 / 표현",
        "accelerate": "핵심 뜻: 가속하다 / 앞당기다",
        "revision": "핵심 뜻: 수정 / 재검토",
        "recall": "핵심 뜻: 기억해 내다 / 회상하다",
        "prototype": "핵심 뜻: 원형 / 전형적 예",
        "authentic": "핵심 뜻: 진정성 있는 / 실제적인",
        "reinforce": "핵심 뜻: 강화하다 / 다지다",
    },
}


def main() -> int:
    changed_files = 0
    changed_rows = 0
    for rel in [
        "toefl_ets_2026_set_05.tsv",
        "toefl_ets_2026_set_06.tsv",
        "toefl_ets_2026_set_07.tsv",
        "toefl_ets_2026_set_08.tsv",
    ]:
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
