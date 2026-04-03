#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


CARDS = {
    "utilization": "핵심 뜻: 활용 / 이용\n부가 뜻: 자원·정보·기술을 실제로 써먹는 것\n핵심 느낌: 가진 것을 실제 목적에 맞게 끌어 쓰는 느낌\n구분: utilization=실제 활용 / usage=사용 방식·빈도 / application=구체적 적용",
    "actionable": "핵심 뜻: 실행 가능한 / 조치로 옮길 수 있는\n부가 뜻: 바로 행동 계획으로 연결되는 / 실천 가능한\n핵심 느낌: 읽고 끝나는 게 아니라 바로 할 일로 바뀌는 느낌\n구분: actionable=바로 실행 가능 / practical=현실적으로 쓸 만함 / feasible=실행 가능성이 있음",
    "adaptable": "핵심 뜻: 적응 가능한 / 융통성 있는\n부가 뜻: 조건 변화에 맞게 바꿀 수 있는 / 유연한\n핵심 느낌: 환경이 바뀌어도 형태를 맞춰 따라가는 느낌\n구분: adaptable=변화에 맞게 조정 가능 / flexible=유연함 / versatile=여러 용도에 두루 쓸 수 있음",
    "balanced": "핵심 뜻: 균형 잡힌 / 치우치지 않은\n부가 뜻: 여러 요소를 고르게 반영한 / 안정적인\n핵심 느낌: 한쪽으로 쏠리지 않고 무게가 맞는 느낌\n구분: balanced=여러 요소가 고르게 맞음 / impartial=편파적이지 않음 / stable=흔들림이 적음",
    "communicative": "핵심 뜻: 의사소통 중심의 / 소통을 잘하는\n부가 뜻: 정보를 주고받기 쉬운 / 표현이 분명한\n핵심 느낌: 말과 메시지가 상대에게 잘 오가도록 열려 있는 느낌\n구분: communicative=소통 기능이 잘 살아 있음 / interactive=서로 주고받음 / expressive=감정·생각을 드러냄",
    "contextual": "핵심 뜻: 맥락상의 / 문맥에 따른\n부가 뜻: 상황·배경과 연결된 / 맥락을 반영한\n핵심 느낌: 단어 하나만 보지 않고 주변 상황과 함께 읽는 느낌\n구분: contextual=맥락과 연결됨 / situational=특정 상황에 따른 / general=일반적인",
    "decision": "핵심 뜻: 결정 / 판단\n부가 뜻: 여러 선택지 중 하나를 고른 결론 / 방침\n핵심 느낌: 고민 끝에 한 방향으로 확정하는 느낌\n구분: decision=선택 후 내린 결론 / choice=선택지 또는 선택 행위 / judgment=판단력·판정",
    "descriptive": "핵심 뜻: 서술적인 / 묘사하는\n부가 뜻: 있는 그대로 특징을 설명하는 / 기술적인\n핵심 느낌: 평가보다 모습과 특성을 차근차근 그려주는 느낌\n구분: descriptive=특징을 설명·묘사 / analytical=분석 중심 / evaluative=가치 판단 중심",
    "editorial": "핵심 뜻: 편집상의 / 사설의\n부가 뜻: 편집 과정과 관련된 / 편집자 의견을 담은\n핵심 느낌: 내용을 어떻게 싣고 다듬을지 편집 관점에서 보는 느낌\n구분: editorial=편집·사설 관련 / journalistic=보도·언론 관련 / administrative=행정 운영 관련",
    "educational": "핵심 뜻: 교육의 / 교육적인\n부가 뜻: 학습에 도움이 되는 / 교육 목적의\n핵심 느낌: 지식·기술을 배우게 하는 방향으로 설계된 느낌\n구분: educational=교육 목적·학습 효과 강조 / academic=학문·학교 맥락 / instructional=가르치는 절차 중심",
    "explanatory": "핵심 뜻: 설명용의 / 해설적인\n부가 뜻: 이유나 원리를 풀어 주는 / 이해를 돕는\n핵심 느낌: 왜 그런지 알기 쉽게 풀어서 밝혀주는 느낌\n구분: explanatory=이유·원리를 설명 / descriptive=모습을 서술 / interpretive=의미를 해석",
    "generalizable": "핵심 뜻: 일반화 가능한\n부가 뜻: 한 사례를 넘어 더 넓은 상황에 적용 가능한\n핵심 느낌: 특정 결과가 다른 맥락에도 퍼져 적용될 수 있는 느낌\n구분: generalizable=넓은 범위로 일반화 가능 / transferable=다른 상황으로 옮겨 적용 가능 / universal=보편적인",
    "guided": "핵심 뜻: 안내를 받는 / 지도된\n부가 뜻: 방향 제시가 포함된 / 교사의 지원 아래 진행되는\n핵심 느낌: 혼자 막 가는 게 아니라 옆에서 길을 잡아 주는 느낌\n구분: guided=지도·안내가 붙음 / independent=혼자 수행 / structured=정해진 틀을 따름",
    "informative": "핵심 뜻: 유익한 정보를 주는 / 정보성이 높은\n부가 뜻: 이해에 도움이 되는 사실을 많이 담은\n핵심 느낌: 읽고 나면 새로 알게 되는 내용이 늘어나는 느낌\n구분: informative=정보를 많이 제공 / explanatory=이유를 풀어 설명 / educational=학습 목적이 강함",
    "managerial": "핵심 뜻: 관리상의 / 경영의\n부가 뜻: 조직·자원·업무를 운영하는 데 관련된\n핵심 느낌: 사람과 일을 어떻게 배치하고 통제할지 보는 느낌\n구분: managerial=관리 책임·운영 관련 / administrative=행정 절차 관련 / organizational=조직 구조 관련",
    "operational": "핵심 뜻: 운영상의 / 작동의\n부가 뜻: 실제 실행 단계와 관련된 / 시스템이 돌아가는\n핵심 느낌: 계획이 아니라 실제로 굴러가는 방식에 초점이 있는 느낌\n구분: operational=실제 운영·작동 관련 / strategic=큰 방향·전략 관련 / practical=현실 적용성 중심",
    "organizational": "핵심 뜻: 조직의 / 조직 운영상의\n부가 뜻: 조직 구조·역할·협력 방식과 관련된\n핵심 느낌: 개인 하나가 아니라 팀이나 기관 전체의 짜임을 보는 느낌\n구분: organizational=조직 구조·운영 관련 / managerial=관리 책임 중심 / institutional=제도·기관 차원",
    "purposeful": "핵심 뜻: 목적이 분명한 / 의도적인\n부가 뜻: 뚜렷한 목표를 갖고 설계된 / 계획적인\n핵심 느낌: 그냥 하는 게 아니라 분명한 목표를 향해 움직이는 느낌\n구분: purposeful=의도·목표가 뚜렷함 / deliberate=신중하고 의도적 / intentional=일부러 한",
    "readiness": "핵심 뜻: 준비 상태 / 준비성\n부가 뜻: 바로 시작하거나 대응할 수 있는 정도\n핵심 느낌: 필요할 때 곧바로 움직일 수 있게 갖춰진 상태\n구분: readiness=행동 직전의 준비 상태 / preparation=준비 과정 / availability=사용 가능한 상태",
    "responsive": "핵심 뜻: 반응이 빠른 / 호응하는\n부가 뜻: 요구나 변화에 즉각 맞춰 대응하는 / 민감하게 반응하는\n핵심 느낌: 들어온 신호를 늦지 않게 받아 조정하는 느낌\n구분: responsive=요구·변화에 빠르게 반응 / reactive=사후적으로 반응 / adaptable=조건 변화에 맞춰 바뀜",
    "scalable": "핵심 뜻: 규모 확장이 가능한\n부가 뜻: 이용량·범위를 키워도 운영 가능한 / 확장성 있는\n핵심 느낌: 작은 규모에서 큰 규모로 키워도 구조가 버티는 느낌\n구분: scalable=규모를 키워도 작동 / expandable=물리·범위 확장 가능 / sustainable=장기 유지 가능",
    "supportive": "핵심 뜻: 지지하는 / 도움이 되는\n부가 뜻: 정서적·실무적으로 뒷받침하는 / 협조적인\n핵심 느낌: 혼자 버티게 두지 않고 옆에서 받쳐 주는 느낌\n구분: supportive=지지와 도움 제공 / cooperative=협조적으로 함께함 / encouraging=용기를 북돋움",
    "targeted": "핵심 뜻: 표적화된 / 특정 대상을 겨냥한\n부가 뜻: 특정 문제·집단에 맞춰 설계된 / 집중된\n핵심 느낌: 넓게 퍼붓지 않고 정확히 한 지점을 겨누는 느낌\n구분: targeted=특정 대상에 맞춘 / focused=집중된 / selective=일부만 골라 적용",
    "workable": "핵심 뜻: 실행 가능한 / 그럭저럭 돌아가는\n부가 뜻: 현실적으로 쓸 수 있는 / 해결책으로 성립하는\n핵심 느낌: 완벽하진 않아도 실제로 굴릴 수 있는 수준이라는 느낌\n구분: workable=현실적으로 운용 가능 / feasible=실현 가능성 있음 / practical=실용적",
    "blueprint": "핵심 뜻: 청사진 / 구체적 설계안\n부가 뜻: 실행 전 전체 구조를 보여주는 계획도 / 기본 설계\n핵심 느낌: 실제로 만들기 전에 전체 틀을 미리 그려 놓은 지도\n구분: blueprint=구조와 단계가 담긴 설계안 / outline=개요 / roadmap=추진 경로",
    "briefing": "핵심 뜻: 요약 보고 / 사전 설명\n부가 뜻: 핵심 정보를 짧게 정리해 전달하는 회의나 문서\n핵심 느낌: 본격 실행 전에 꼭 알아야 할 핵심만 빠르게 공유하는 느낌\n구분: briefing=짧은 핵심 보고 / presentation=발표 / report=더 긴 공식 보고",
    "checkpoint": "핵심 뜻: 점검 지점 / 중간 확인 단계\n부가 뜻: 진행 상황을 확인하는 기준점 / 검토 시점\n핵심 느낌: 계속 가기 전에 멈춰서 제대로 왔는지 확인하는 표시\n구분: checkpoint=중간 점검 지점 / milestone=주요 성취 단계 / benchmark=비교 기준",
    "coursework": "핵심 뜻: 수업 과제 / 교과 과정에서 하는 학업\n부가 뜻: 강의와 연계된 과제·보고서·학습 활동\n핵심 느낌: 시험만이 아니라 수업 중 쌓아 가는 학업 작업 전체\n구분: coursework=수업 중 수행 과제와 학업 / curriculum=교육과정 전체 / assignment=개별 과제",
    "deliverable": "핵심 뜻: 제출해야 할 산출물 / 결과물\n부가 뜻: 프로젝트 단계별로 완성해 내야 하는 구체적 결과\n핵심 느낌: 말로만 진행하는 게 아니라 손에 잡히게 내야 하는 완성물\n구분: deliverable=제출 가능한 산출물 / outcome=결과 일반 / output=생산된 결과물",
    "design": "핵심 뜻: 설계 / 설계하다\n부가 뜻: 목적에 맞게 구조나 방식을 짜다 / 계획안\n핵심 느낌: 기능과 목적을 생각하며 전체 모양과 구조를 짜는 느낌\n구분: design=구조·방식을 목적에 맞게 설계 / plan=실행 계획을 세움 / draft=초안을 씀",
    "facilitation": "핵심 뜻: 촉진 / 진행을 쉽게 돕기\n부가 뜻: 토론·학습·협업이 잘 흐르도록 지원하는 일\n핵심 느낌: 일이 막히지 않고 부드럽게 굴러가도록 옆에서 길을 터주는 느낌\n구분: facilitation=과정이 잘 흐르도록 도움 / mediation=갈등을 중재 / support=일반적 지원",
    "guideline": "핵심 뜻: 지침 / 가이드라인\n부가 뜻: 행동이나 판단의 기준으로 삼는 권고 규칙\n핵심 느낌: 무엇을 어떻게 해야 하는지 큰 선을 잡아 주는 기준선\n구분: guideline=권고형 기준·지침 / rule=의무 규칙 / instruction=구체적 지시",
    "milestone": "핵심 뜻: 중요한 단계 / 이정표\n부가 뜻: 프로젝트나 과정에서 의미 있는 중간 성취점\n핵심 느낌: 긴 진행 중 여기까지 왔다고 표시하는 핵심 지점\n구분: milestone=중요한 중간 성취점 / checkpoint=점검 지점 / deadline=마감 시점",
    "overview": "핵심 뜻: 개요 / 전체적인 훑어보기\n부가 뜻: 세부 전에 큰 구조를 간단히 정리한 설명\n핵심 느낌: 숲 전체를 먼저 보여 주고 세부는 나중에 보는 느낌\n구분: overview=큰 그림 요약 / summary=핵심 요약 / detail=세부 사항",
    "planning": "핵심 뜻: 계획 수립 / 기획\n부가 뜻: 목표·일정·자원을 미리 짜는 과정\n핵심 느낌: 실행 전에 어디로 어떻게 갈지 길을 먼저 짜는 느낌\n구분: planning=사전 계획 수립 과정 / schedule=시간 배치 / strategy=큰 방향 설계",
    "presentation": "핵심 뜻: 발표 / 제시\n부가 뜻: 자료나 생각을 청중에게 구조적으로 전달하는 일\n핵심 느낌: 준비한 내용을 남이 이해할 수 있게 앞에 펼쳐 보이는 느낌\n구분: presentation=청중 앞 제시·발표 / briefing=짧은 핵심 보고 / report=문서형 보고",
    "progress": "핵심 뜻: 진전 / 발전\n부가 뜻: 목표를 향해 앞으로 나아가는 정도 / 향상\n핵심 느낌: 제자리에서 멈춘 게 아니라 한 단계씩 앞으로 가는 느낌\n구분: progress=목표 방향의 진전 / improvement=질적 향상 / advancement=더 높은 단계로 나아감",
    "proposal": "핵심 뜻: 제안 / 제안서\n부가 뜻: 실행하거나 검토해 달라고 내놓는 계획안\n핵심 느낌: 이런 방향으로 해보자고 공식적으로 내미는 안\n구분: proposal=검토를 위한 제안안 / suggestion=가벼운 제안 / plan=실행 계획",
    "review": "핵심 뜻: 검토 / 재검토하다\n부가 뜻: 내용을 다시 살펴 평가하거나 고치는 과정 / 평론\n핵심 느낌: 한 번 끝났다고 두지 않고 다시 들여다보며 따지는 느낌\n구분: review=다시 검토·평가 / evaluate=기준에 따라 평가 / revise=검토 후 고침",
    "roadmap": "핵심 뜻: 로드맵 / 단계별 추진 계획\n부가 뜻: 목표까지의 경로와 순서를 보여주는 큰 계획\n핵심 느낌: 어디부터 어디까지 어떤 순서로 갈지 그린 길지도\n구분: roadmap=단계별 추진 경로 / blueprint=구조 설계안 / timeline=시간 순서표",
    "teamwork": "핵심 뜻: 팀워크 / 협업\n부가 뜻: 여러 사람이 역할을 나눠 함께 일하는 능력과 방식\n핵심 느낌: 각자 따로가 아니라 한 방향으로 맞춰 움직이는 느낌\n구분: teamwork=팀 단위 협업 / collaboration=공동 작업 / cooperation=협조",
    "timeline": "핵심 뜻: 시간표 / 진행 일정선\n부가 뜻: 사건이나 과제 단계를 시간 순서로 배열한 계획\n핵심 느낌: 언제 무엇이 일어나는지 한 줄로 펼쳐 보는 느낌\n구분: timeline=시간 순서 흐름 / schedule=구체적 일정 배치 / sequence=순서 자체",
    "training": "핵심 뜻: 훈련 / 교육 과정\n부가 뜻: 기술이나 절차를 익히도록 반복해서 배우는 과정\n핵심 느낌: 할 수 있게 될 때까지 연습하며 몸에 붙이는 느낌\n구분: training=실행 능력을 기르는 훈련 / education=넓은 의미의 교육 / practice=연습",
    "usable": "핵심 뜻: 사용 가능한 / 쓰기 좋은\n부가 뜻: 실제로 문제없이 활용할 수 있는 / 실용성이 있는\n핵심 느낌: 보기만 좋은 게 아니라 실제 작업에 바로 쓸 수 있는 느낌\n구분: usable=실제로 사용 가능 / practical=현실적으로 유용 / accessible=접근·사용이 쉬움",
    "variance": "핵심 뜻: 변동성 / 차이\n부가 뜻: 평균이나 기준에서 얼마나 퍼져 있는지 / 편차\n핵심 느낌: 값들이 한 점에 모이지 않고 얼마나 흩어지는지 보는 느낌\n구분: variance=값의 퍼짐·변동 / deviation=기준에서 벗어난 정도 / variability=변하기 쉬운 성질",
    "reflection": "핵심 뜻: 성찰 / 되돌아보기\n부가 뜻: 경험이나 생각을 다시 곱씹어 의미를 정리하는 과정 / 반영\n핵심 느낌: 지나간 일을 다시 비춰 보며 배울 점을 찾는 느낌\n구분: reflection=경험을 되짚는 성찰 / review=내용 재검토 / contemplation=깊은 숙고",
    "summary": "핵심 뜻: 요약 / 개괄\n부가 뜻: 긴 내용을 핵심만 간단히 정리한 것\n핵심 느낌: 많은 내용을 짧게 줄여 뼈대만 남기는 느낌\n구분: summary=핵심만 간추린 정리 / overview=전체 큰 그림 / abstract=논문 초록",
    "recommendation": "핵심 뜻: 권고 / 추천\n부가 뜻: 무엇을 하는 게 좋다고 제안하는 판단이나 조언\n핵심 느낌: 여러 선택지 중 이쪽이 낫다고 방향을 찍어 주는 느낌\n구분: recommendation=판단이 담긴 권고 / suggestion=가벼운 제안 / advice=조언",
    "comparison": "핵심 뜻: 비교 / 대조\n부가 뜻: 둘 이상을 나란히 놓고 공통점과 차이를 살피는 일\n핵심 느낌: 옆에 놓고 어느 점이 같고 다른지 선명하게 보는 느낌\n구분: comparison=공통점·차이를 함께 봄 / contrast=차이를 특히 부각 / analogy=구조적 유사성",
    "guidance": "핵심 뜻: 지도 / 안내\n부가 뜻: 방향을 잡아 주는 조언이나 지원 / 지침 제공\n핵심 느낌: 혼자 헤매지 않게 어디로 가면 되는지 길을 잡아 주는 느낌\n구분: guidance=방향을 잡아 주는 안내 / instruction=구체적 지시·교수 / support=도움 일반",
    "initiative": "핵심 뜻: 주도성 / 새로운 계획\n부가 뜻: 먼저 나서서 일을 시작하는 태도 / 추진 과제\n핵심 느낌: 누가 시키기 전에 먼저 움직여 일을 여는 느낌\n구분: initiative=먼저 시작하는 주도성·사업 / proposal=제안안 / leadership=이끄는 능력",
    "completion": "핵심 뜻: 완료 / 완성\n부가 뜻: 과제나 과정이 끝까지 마무리된 상태\n핵심 느낌: 시작한 일이 중간에 멈추지 않고 끝선까지 닿은 느낌\n구분: completion=끝까지 마무리됨 / conclusion=논의·글의 결말 / fulfillment=요구나 약속의 충족",
    "orientation": "핵심 뜻: 방향 설정 / 오리엔테이션\n부가 뜻: 새로운 환경·과제의 기본 방향을 잡아 주는 안내 / 관점\n핵심 느낌: 처음 들어갈 때 어디를 기준으로 봐야 하는지 방향을 맞추는 느낌\n구분: orientation=초기 방향 설정·안내 / guidance=지속적 안내 / perspective=바라보는 관점",
    "adjustment": "핵심 뜻: 조정 / 수정\n부가 뜻: 상황에 맞게 조금 바꾼 결과나 과정\n핵심 느낌: 딱 맞지 않는 부분을 손봐서 맞춰 넣는 느낌\n구분: adjustment=세부를 맞추는 조정 / revision=내용을 다시 고침 / adaptation=환경에 맞게 바뀜",
    "observational": "핵심 뜻: 관찰 기반의 / 관찰용의\n부가 뜻: 실험 조작보다 관찰 자료에 근거한 / 관찰과 관련된\n핵심 느낌: 개입하기보다 있는 현상을 지켜보며 자료를 모으는 느낌\n구분: observational=관찰 자료 중심 / experimental=실험 조작 중심 / descriptive=서술 중심",
    "participatory": "핵심 뜻: 참여형의 / 참여를 수반하는\n부가 뜻: 구성원이 직접 참여하도록 설계된 / 함께 관여하는\n핵심 느낌: 구경만 하지 않고 실제로 과정 안에 들어가 함께 하는 느낌\n구분: participatory=직접 참여를 강조 / collaborative=함께 작업함 / passive=수동적",
    "preparatory": "핵심 뜻: 준비 단계의 / 예비적인\n부가 뜻: 본격 작업 전에 준비를 위한 / 사전의\n핵심 느낌: 바로 본게임이 아니라 먼저 기반을 다지는 단계\n구분: preparatory=사전 준비용 / preliminary=초기 단계의 / introductory=도입용",
    "coordinated": "핵심 뜻: 조율된 / 체계적으로 맞춰진\n부가 뜻: 여러 요소가 서로 맞게 연결된 / 협력적으로 조직된\n핵심 느낌: 따로따로 움직이지 않고 타이밍과 역할이 맞게 돌아가는 느낌\n구분: coordinated=여러 부분이 맞춰 움직임 / organized=구조적으로 정리됨 / aligned=방향이 일치함",
    "evaluative": "핵심 뜻: 평가적인 / 가치 판단을 포함한\n부가 뜻: 기준에 따라 좋고 나쁨을 판단하는 / 평가 중심의\n핵심 느낌: 단순 설명이 아니라 어떤 기준으로 점검하고 판단하는 느낌\n구분: evaluative=가치 판단 포함 / descriptive=묘사 중심 / analytical=구조 분석 중심",
    "instructional": "핵심 뜻: 교육용의 / 교수의\n부가 뜻: 가르치기 위해 설계된 / 학습 절차를 안내하는\n핵심 느낌: 학생이 따라 배우도록 순서와 설명이 붙어 있는 느낌\n구분: instructional=가르치는 목적·절차 중심 / educational=교육 전반 관련 / informative=정보 제공 중심",
    "interpretive": "핵심 뜻: 해석의 / 해석적인\n부가 뜻: 자료나 텍스트의 의미를 풀어내는 / 해석 관점의\n핵심 느낌: 겉에 보이는 사실을 넘어서 무슨 뜻인지 읽어내는 느낌\n구분: interpretive=의미 해석 중심 / analytical=구조 분석 중심 / explanatory=이유 설명 중심",
    "manageable": "핵심 뜻: 감당할 수 있는 / 다루기 쉬운\n부가 뜻: 통제 가능한 규모나 난이도의 / 처리 가능한\n핵심 느낌: 너무 크거나 복잡하지 않아 실제로 손댈 수 있는 느낌\n구분: manageable=감당 가능한 수준 / feasible=실행 가능 / controllable=통제 가능",
    "negotiable": "핵심 뜻: 협상 가능한 / 조정 여지가 있는\n부가 뜻: 고정되지 않아 조건을 바꿀 수 있는 / 타협 가능한\n핵심 느낌: 이미 딱 굳은 게 아니라 대화로 조건을 움직일 수 있는 느낌\n구분: negotiable=협상·조정 여지 있음 / flexible=유연함 / fixed=고정됨",
    "persuasive": "핵심 뜻: 설득력 있는\n부가 뜻: 이유나 표현이 상대를 납득시키는 / 마음을 움직이는\n핵심 느낌: 듣는 사람이 그럴듯하다고 받아들이게 만드는 힘\n구분: persuasive=상대를 설득하는 힘 / convincing=납득이 감 / compelling=강하게 끌어당김",
    "productive": "핵심 뜻: 생산적인 / 성과를 내는\n부가 뜻: 좋은 결과를 만들어 내는 / 효율적으로 산출하는\n핵심 느낌: 시간과 노력을 넣었을 때 눈에 보이는 결과가 나오는 느낌\n구분: productive=성과·산출이 잘 나옴 / efficient=낭비가 적음 / effective=목표 달성 효과가 있음",
    "structured": "핵심 뜻: 구조화된 / 체계적으로 짜인\n부가 뜻: 일정한 틀과 순서를 갖춘 / 조직적으로 배열된\n핵심 느낌: 아무렇게나 흩어진 게 아니라 뼈대와 순서가 분명한 느낌\n구분: structured=정해진 틀과 순서가 있음 / organized=잘 정리됨 / systematic=체계적으로 진행",
    "transferable": "핵심 뜻: 전이 가능한 / 다른 상황에도 옮겨 쓸 수 있는\n부가 뜻: 한 맥락에서 배운 것을 다른 맥락에 적용 가능한 / 이전 가능한\n핵심 느낌: 여기서 익힌 것을 저기로 가져가도 통하는 느낌\n구분: transferable=다른 맥락으로 옮겨 적용 가능 / generalizable=더 넓게 일반화 가능 / portable=물리적·기술적으로 옮기기 쉬움",
}


def main() -> int:
    touched = 0
    for filename in ["toefl_ets_2026_set_09.tsv", "toefl_ets_2026_set_11.tsv"]:
        path = Path(filename)
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle, delimiter="\t"))
        for row in rows:
            if row[0] in CARDS:
                row[1] = CARDS[row[0]]
                touched += 1
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerows(rows)
    print(f"updated={touched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
