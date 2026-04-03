#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


VERBS = {
    "adapt",
    "adjust",
    "advocate",
    "construct",
    "contribute",
    "discuss",
    "document",
    "draft",
    "evaluate",
    "illustrate",
    "instruct",
    "moderate",
    "organize",
    "revise",
    "schedule",
    "strengthen",
    "summarize",
    "update",
}

ADJECTIVES = {
    "alternative",
    "dynamic",
    "empirical",
    "practical",
    "selective",
    "valid",
    "actionable",
    "adaptable",
    "balanced",
    "communicative",
    "contextual",
    "descriptive",
    "editorial",
    "educational",
    "explanatory",
    "generalizable",
    "guided",
    "informative",
    "managerial",
    "operational",
    "organizational",
    "purposeful",
    "responsive",
    "scalable",
    "supportive",
    "targeted",
    "workable",
    "usable",
    "observational",
    "participatory",
    "preparatory",
    "coordinated",
    "evaluative",
    "instructional",
    "interpretive",
    "manageable",
    "negotiable",
    "persuasive",
    "productive",
    "structured",
    "transferable",
}

CUSTOM_BACKS = {
    "adapt": "핵심 뜻: 적응하다 / 맞게 바꾸다\n부가 뜻: 새로운 조건에 맞추다 / 적용 가능하게 수정하다\n핵심 느낌: 환경이 바뀌면 그에 맞춰 형태를 조정하는 느낌\n구분: adapt=상황에 맞춰 바꾸다 / adjust=세부를 조정하다 / adopt=받아들여 채택하다",
    "adjust": "핵심 뜻: 조정하다 / 맞추다\n부가 뜻: 조금 고치다 / 균형을 맞추다\n핵심 느낌: 기준에 맞게 미세하게 손보는 느낌\n구분: adjust=세부를 맞게 조정 / revise=내용을 고쳐 다듬음 / adapt=상황에 맞게 바꿈",
    "advocate": "핵심 뜻: 옹호하다 / 지지하다\n부가 뜻: 공개적으로 주장하다 / 지지자\n핵심 느낌: 어떤 입장이나 정책을 앞에서 밀어주는 느낌\n구분: advocate=공개적으로 지지·주장 / support=돕거나 지지 / endorse=공식적으로 승인·지지",
    "agenda": "핵심 뜻: 의제 / 안건\n부가 뜻: 논의할 목록 / 추진하려는 우선 과제\n핵심 느낌: 회의나 정책에서 무엇을 먼저 다룰지 적어 둔 목록\n구분: agenda=논의·추진 안건 / schedule=시간표 / priority=우선순위",
    "alternative": "핵심 뜻: 대안의 / 대안\n부가 뜻: 다른 선택지 / 기존 방식 대신 가능한\n핵심 느낌: 하나가 안 맞을 때 옆에 놓는 다른 선택지\n구분: alternative=대신 가능한 선택지 / substitute=대체물 / optional=선택 사항의",
    "construct": "핵심 뜻: 구성하다 / 만들어 세우다\n부가 뜻: 개념을 세우다 / 구조를 짜다\n핵심 느낌: 여러 요소를 엮어 하나의 틀을 만드는 느낌\n구분: construct=틀을 만들어 구성 / build=물리적으로 만들다 / formulate=생각을 체계화하다",
    "contribute": "핵심 뜻: 기여하다 / 보태다\n부가 뜻: 원인으로 작용하다 / 의견이나 자원을 더하다\n핵심 느낌: 전체 결과에 자기 몫을 얹는 느낌\n구분: contribute=결과나 공동 작업에 보태다 / provide=제공하다 / cause=직접 원인이 되다",
    "discuss": "핵심 뜻: 논의하다 / 토론하다\n부가 뜻: 자세히 다루다 / 의견을 나누다\n핵심 느낌: 여러 관점을 놓고 차분히 이야기하며 따져보는 느낌\n구분: discuss=내용을 놓고 논의 / debate=찬반을 두고 논쟁 / mention=짧게 언급하다",
    "document": "핵심 뜻: 문서로 기록하다 / 입증 자료를 남기다\n부가 뜻: 기록하다 / 증거를 첨부하다\n핵심 느낌: 나중에 확인할 수 있게 자료로 남겨 두는 느낌\n구분: document=자료로 기록·입증 / record=기록하다 / verify=사실을 확인하다",
    "draft": "핵심 뜻: 초안을 작성하다 / 초안\n부가 뜻: 예비안을 쓰다 / 아직 확정 전인 글\n핵심 느낌: 최종본 전에 먼저 뼈대를 써보는 느낌\n구분: draft=초안 작성·초안 / revise=쓴 것을 고치다 / outline=개요를 잡다",
    "dynamic": "핵심 뜻: 역동적인 / 변화하는\n부가 뜻: 상호작용하며 움직이는 / 활발한\n핵심 느낌: 고정돼 있지 않고 계속 움직이며 바뀌는 느낌\n구분: dynamic=변화와 움직임이 큼 / stable=안정적인 / active=활동적인",
    "empirical": "핵심 뜻: 경험적 / 실증적인\n부가 뜻: 관찰이나 데이터에 근거한 / 실험으로 확인된\n핵심 느낌: 이론만이 아니라 실제 자료로 확인하는 느낌\n구분: empirical=자료·관찰에 근거 / theoretical=이론 중심 / anecdotal=개별 경험담 수준",
    "evaluate": "핵심 뜻: 평가하다 / 가치를 판단하다\n부가 뜻: 기준에 따라 검토하다 / 효과를 따져보다\n핵심 느낌: 일정한 기준표를 놓고 얼마나 좋은지 재는 느낌\n구분: evaluate=가치·효과를 판단 / assess=수준·상태를 평가 / review=검토하다",
    "illustrate": "핵심 뜻: 설명해 보여주다 / 예시로 분명히 하다\n부가 뜻: 삽화로 나타내다 / 구체적으로 보여주다\n핵심 느낌: 추상적인 말을 예나 그림으로 눈앞에 보이게 하는 느낌\n구분: illustrate=예시·그림으로 설명 / explain=말로 풀어 설명 / demonstrate=보여주며 입증",
    "instruct": "핵심 뜻: 지시하다 / 가르치다\n부가 뜻: 방법을 알려주다 / 공식적으로 명령하다\n핵심 느낌: 무엇을 어떻게 해야 하는지 순서를 알려주는 느낌\n구분: instruct=절차나 방법을 알려주다 / teach=가르치다 / direct=지시하다",
    "method": "핵심 뜻: 방법 / 절차\n부가 뜻: 체계적인 방식 / 연구 기법\n핵심 느낌: 목표를 얻기 위해 정해 둔 실행 방식\n구분: method=체계적 방법 / approach=접근법 / technique=구체적 기법",
    "moderate": "핵심 뜻: 적당한 / 완만한\n부가 뜻: 지나치지 않은 / 조정하다\n핵심 느낌: 한쪽 극단으로 치우치지 않고 중간 수준을 지키는 느낌\n구분: moderate=중간 정도·완만한 / mild=강도가 약한 / extreme=극단적인",
    "organize": "핵심 뜻: 조직하다 / 정리하다\n부가 뜻: 체계적으로 배열하다 / 행사를 준비하다\n핵심 느낌: 흩어진 요소를 보기 좋게 순서와 구조로 묶는 느낌\n구분: organize=체계 있게 묶어 정리 / arrange=배열하다 / classify=분류하다",
    "practical": "핵심 뜻: 실용적인 / 현실적인\n부가 뜻: 실제 적용 가능한 / 실행에 초점을 둔\n핵심 느낌: 이론보다 실제로 쓸 수 있는지 보는 느낌\n구분: practical=현실 적용 가능 / theoretical=이론 중심 / feasible=실행 가능",
    "priority": "핵심 뜻: 우선순위 / 우선 사항\n부가 뜻: 먼저 처리해야 할 것 / 더 중요한 순위\n핵심 느낌: 여러 일 중 먼저 놓아야 하는 자리\n구분: priority=우선으로 둘 항목 / preference=선호 / urgency=시급성",
    "revise": "핵심 뜻: 수정하다 / 개정하다\n부가 뜻: 다시 검토해 고치다 / 내용을 다듬다\n핵심 느낌: 처음 쓴 것을 보고 더 낫게 다시 손보는 느낌\n구분: revise=검토 후 고쳐 다듬다 / edit=문장을 편집하다 / update=최신 상태로 바꾸다",
    "schedule": "핵심 뜻: 일정 / 일정표를 잡다\n부가 뜻: 예정하다 / 시간표\n핵심 느낌: 언제 무엇을 할지 시간 칸에 배치하는 느낌\n구분: schedule=시간 계획 / timeline=순서 있는 일정 흐름 / agenda=논의 안건 목록",
    "selective": "핵심 뜻: 선택적인 / 선별적인\n부가 뜻: 일부만 고르는 / 기준을 두고 가리는\n핵심 느낌: 전부가 아니라 필요한 것만 골라 집는 느낌\n구분: selective=기준을 두고 선별 / specific=특정한 / exclusive=배타적인",
    "strengthen": "핵심 뜻: 강화하다 / 더 튼튼하게 하다\n부가 뜻: 힘을 키우다 / 근거를 보강하다\n핵심 느낌: 약한 부분을 덧대어 더 단단하게 만드는 느낌\n구분: strengthen=힘·근거를 강화 / reinforce=추가로 보강 / intensify=강도를 높이다",
    "summarize": "핵심 뜻: 요약하다\n부가 뜻: 핵심만 간추리다 / 간단히 정리하다\n핵심 느낌: 많은 내용을 줄여 중요한 뼈대만 남기는 느낌\n구분: summarize=핵심을 간추림 / outline=개요를 잡음 / paraphrase=다른 말로 바꿔 씀",
    "update": "핵심 뜻: 갱신하다 / 최신 정보로 바꾸다\n부가 뜻: 새 정보를 반영하다 / 최신판\n핵심 느낌: 예전 상태를 현재 기준에 맞게 새로 고치는 느낌\n구분: update=최신 상태로 바꾸다 / revise=내용을 다시 고침 / renew=기간·상태를 새롭게 함",
    "valid": "핵심 뜻: 타당한 / 유효한\n부가 뜻: 정당한 / 조건상 인정되는\n핵심 느낌: 기준에 맞아 받아들일 수 있는 상태\n구분: valid=논리·기준상 타당 / legitimate=정당하고 인정됨 / reliable=일관되게 믿을 만함",
}


def make_generic_back(word: str, core: str) -> str:
    if word in VERBS:
        return "\n".join(
            [
                f"핵심 뜻: {core}",
                f"부가 뜻: 목적이나 기준에 맞게 {core} / 절차나 내용을 그렇게 처리하다",
                f"핵심 느낌: 대상을 {core} 쪽으로 직접 움직이거나 다듬는 느낌",
                f"구분: {word}=해당 동작을 직접 수행 / revise=고쳐 다듬다 / adjust=세부를 맞추다",
            ]
        )
    if word in ADJECTIVES:
        return "\n".join(
            [
                f"핵심 뜻: {core}",
                f"부가 뜻: 그런 성격을 가진 / 해당 조건이나 목적에 맞는",
                f"핵심 느낌: 대상의 성질이 {core} 쪽으로 분명하게 드러나는 느낌",
                f"구분: {word}=그 성질을 강조 / practical=실용성 강조 / relevant=관련성 강조",
            ]
        )
    return "\n".join(
        [
            f"핵심 뜻: {core}",
            f"부가 뜻: 관련된 개념·절차·결과 / 문맥에 따라 구체적 대상이 달라짐",
            f"핵심 느낌: 학술·과제·협업 상황에서 {core}의 역할을 떠올리는 느낌",
            f"구분: {word}=해당 개념 자체 / process=진행 절차 / outcome=결과",
        ]
    )


def polish_file(path: Path) -> int:
    changed = 0
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    for row in rows:
        if len(row) != 2:
            continue
        word, back = row
        if word in CUSTOM_BACKS:
            row[1] = CUSTOM_BACKS[word]
            changed += 1
            continue
        if (
            "와 관련된 의미 / 문맥에 따라 세부 해석" in back
            or "학술 문맥에서" in back
            or "related=연관된 의미 / context=문맥상 구분" in back
        ):
            core = back.split("\n", 1)[0].replace("핵심 뜻:", "").strip()
            row[1] = make_generic_back(word, core)
            changed += 1

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)
    return changed


def main() -> int:
    total = 0
    for set_num in [6, 7, 8, 9, 11]:
        path = Path(f"toefl_ets_2026_set_{set_num:02d}.tsv")
        count = polish_file(path)
        total += count
        print(f"{path.name}: polished={count}")
    print(f"total={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
