from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_19.tsv"

CARDS = [
    ("adaptable", "적응 가능한 / 유연하게 바꿀 수 있는", "상황이나 조건이 달라져도 형태나 방식이 맞춰질 수 있는", "고정된 틀보다 조건 따라 몸을 틀 수 있는 느낌", "adaptable=상황에 맞춰 바뀔 수 있는 / flexible=유연한 / fixed=고정된"),
    ("bottlenecked", "병목이 걸린 / 한 지점에서 막힌", "전체 진행이 특정 제한 지점 때문에 느려지거나 막힌", "길은 있는데 한 좁은 목에서 줄이 걸린 느낌", "bottlenecked=한 제한 지점에서 흐름이 막힌 / constrained=제약을 받는 / delayed=늦어진"),
    ("buildout", "구축 확장 / 시설·기능을 실제로 늘려감", "계획된 구조나 기능을 단계적으로 실제 환경에 깔고 늘려가는 일", "설계도 위 선이 현장에 하나씩 설치되며 넓어지는 느낌", "buildout=실제 구축을 확장함 / rollout=서비스를 도입·배포함 / expansion=규모를 키움"),
    ("cost-effective", "비용 대비 효율적인", "투입 비용에 비해 얻는 효과나 성과가 좋은", "돈을 많이 태우지 않아도 결과가 잘 나오는 느낌", "cost-effective=비용 대비 효과가 좋은 / efficient=자원 대비 성과가 좋은 / expensive=비용이 큰"),
    ("design constraint", "설계 제약 조건", "원하는 대로 만들 때 반드시 고려해야 하는 비용·크기·시간·안전 등의 한계", "아무렇게나 못 만들게 테두리를 그어두는 조건", "design constraint=설계가 지켜야 하는 제한 조건 / requirement=충족해야 할 요건 / obstacle=진행을 막는 장애물"),
    ("design iteration", "설계 반복 개선 / 반복 수정 단계", "처음 안을 그대로 두지 않고 시험과 피드백을 거쳐 여러 차례 고쳐가는 과정", "한 번에 완성보다 만들고 다시 손보는 순환", "design iteration=설계를 반복적으로 고쳐 개선함 / revision=수정 / prototype=시험용 초안 모델"),
    ("downtime", "중단 시간 / 작동 멈춤 시간", "시스템이나 서비스가 정상적으로 돌아가지 않는 시간", "돌아가던 것이 멈춰 실제로 못 쓰는 빈 시간", "downtime=작동이 멈춘 시간 / outage=서비스 장애 / delay=늦어짐"),
    ("durability", "내구성 / 오래 버티는 성질", "시간이나 반복 사용에도 쉽게 망가지지 않고 버티는 정도", "한두 번 쓰고 끝나지 않고 계속 견디는 힘", "durability=오래 견디는 성질 / resilience=충격 후 회복력 / longevity=오래 지속됨"),
    ("fit-for-purpose", "목적에 맞는 / 용도에 적합한", "멋있거나 고급이라는 뜻보다 실제 목적과 요구에 잘 맞는", "보기에 그럴듯한 것보다 이 일에 딱 맞게 맞춰진 느낌", "fit-for-purpose=주어진 목적에 적합한 / suitable=알맞은 / overengineered=필요 이상으로 복잡한"),
    ("fallback", "대체 수단 / 예비안", "원래 방식이 안 될 때 대신 쓸 수 있게 준비한 두 번째 선택지", "첫 길이 막히면 바로 옆길로 갈 수 있게 남겨둔 카드", "fallback=문제 시 쓰는 예비 대안 / backup=예비 복사본·대체 수단 / default=기본값"),
    ("fault-tolerant", "고장에 강한 / 일부 오류를 견디는", "일부 구성요소가 실패해도 전체가 완전히 멈추지 않도록 버티는", "한 군데 삐끗해도 전체 시스템이 바로 무너지지 않는 느낌", "fault-tolerant=부분 고장을 견디는 / resilient=충격에도 버티고 회복하는 / fragile=쉽게 깨지는"),
    ("field-tested", "현장 검증된 / 실제 환경에서 시험된", "실험실이나 문서뿐 아니라 실제 사용 조건에서 검토된", "책상 위 아이디어가 아니라 현장 바람을 맞으며 한 번 버틴 느낌", "field-tested=실제 현장에서 시험된 / theoretical=이론적인 / preliminary=예비 단계의"),
    ("fine-tune", "미세 조정하다 / 더 정교하게 다듬다", "큰 틀은 유지하면서 성능이나 결과가 더 좋아지도록 세부 값을 조정하다", "큰 망치질보다 마지막 눈금을 살짝살짝 맞추는 느낌", "fine-tune=세부를 미세 조정하다 / revise=고쳐 쓰다 / calibrate=기준에 맞게 보정하다"),
    ("future-proof", "미래 변화에도 버티게 설계하다", "지금만 맞는 게 아니라 이후 변화와 확장에도 쉽게 낡지 않게 만들다", "당장 맞추고 끝이 아니라 다음 변화에도 버티게 여유를 넣는 느낌", "future-proof=미래 변화에도 덜 흔들리게 설계하다 / scalable=규모 확장이 가능한 / temporary=일시적인"),
    ("human-centered", "사람 중심의 / 사용자 경험을 우선한", "기술 자체보다 실제 사용자의 필요와 이해, 편의를 우선해 설계한", "기계 논리보다 사람이 쓸 때 편한지를 먼저 보는 느낌", "human-centered=사용자 필요를 중심에 둔 / user-friendly=사용하기 쉬운 / technology-driven=기술 자체가 이끄는"),
    ("incremental rollout", "점진적 도입 / 단계적 배포", "전체를 한꺼번에 바꾸지 않고 작은 범위부터 순서대로 넓히는 시행 방식", "작게 먼저 깔아보고 문제 없으면 다음 칸으로 넓혀가는 느낌", "incremental rollout=단계적으로 넓혀 도입함 / full launch=전면 공개·출시 / pilot program=시범 운영"),
    ("interchangeable", "서로 바꿔 쓸 수 있는 / 호환되는", "기능이나 역할이 비슷해 한쪽을 다른 것으로 대체해도 되는", "꼭 이 부품만이 아니라 비슷한 다른 것으로 끼워도 맞는 느낌", "interchangeable=서로 대체 가능함 / compatible=함께 맞게 쓸 수 있음 / unique=대체 불가한"),
    ("load-bearing", "하중을 지탱하는 / 핵심 부담을 받는", "장식보다 실제 무게나 책임을 떠받치는 역할을 하는", "겉모양보다 판을 실제로 받치고 있는 중심 기둥 느낌", "load-bearing=무게나 핵심 부담을 지탱하는 / supportive=도움을 주는 / decorative=장식적인"),
    ("maintenance cycle", "정비 주기 / 반복 유지관리 일정", "고장 난 뒤가 아니라 일정한 간격으로 점검·수리·교체를 반복하는 흐름", "한 번 만들고 끝이 아니라 주기적으로 다시 들여다보는 관리 고리", "maintenance cycle=반복적인 유지관리 주기 / life cycle=전체 생애주기 / repair=고장 수리"),
    ("modular", "모듈형의 / 조립식 구성의", "전체를 작은 기능 단위로 나눠 필요에 따라 붙이거나 바꿀 수 있는", "한 덩어리 통짜보다 블록처럼 나눠 조립하는 느낌", "modular=작은 기능 단위로 나뉜 / integrated=하나로 결합된 / flexible=유연한"),
    ("overhaul", "전면 개편하다 / 대대적으로 손보다", "작은 수정이 아니라 구조나 시스템을 큰 폭으로 고쳐 개선하다", "겉칠만 다시 하는 게 아니라 속 구조까지 크게 뜯어고치는 느낌", "overhaul=대대적으로 개편하다 / revise=부분적으로 수정하다 / optimize=성능을 더 좋게 맞추다"),
    ("pain point", "불편 지점 / 가장 거슬리는 문제", "사용자나 현장이 특히 불편하거나 막힌다고 느끼는 구체적 문제 지점", "전체가 다 나쁜 건 아니어도 여기서 계속 걸리는 아픈 지점", "pain point=특히 불편한 문제 지점 / bottleneck=흐름을 막는 병목 / complaint=불만 제기"),
    ("proof-of-concept", "개념 검증용 시제품 / 실현 가능성 확인", "아이디어가 실제로 작동할 수 있는지 작게 만들어 먼저 확인하는 단계", "큰 제품 전에 이 생각이 정말 되는지 작은 판으로 시험하는 느낌", "proof-of-concept=아이디어 작동 가능성을 먼저 보여주는 단계 / prototype=시험용 모델 / full implementation=전면 실행"),
    ("reconfigurable", "재구성 가능한 / 다시 배치할 수 있는", "한 번 정한 형태로 끝나지 않고 필요에 따라 구조나 조합을 바꿀 수 있는", "고정된 한 모양보다 다시 분해하고 새로 짤 수 있는 느낌", "reconfigurable=구조를 다시 바꿔 짤 수 있는 / adaptable=상황에 맞게 바꿀 수 있는 / permanent=영구 고정된"),
    ("redundancy", "여분의 중복 장치 / 예비 겹침", "한 부분이 실패해도 버틸 수 있게 같은 기능을 겹쳐 남겨 둔 여유", "낭비처럼 보여도 하나 터졌을 때 대신 버틸 여분 줄", "redundancy=고장 대비 여분 중복 / backup=대체 예비 수단 / duplication=단순 반복"),
    ("retrofit", "개조해 덧붙이다 / 기존 구조에 맞춰 보강하다", "완전히 새로 짓지 않고 기존 시스템에 새 기능이나 기준을 맞춰 넣다", "옛 틀을 버리지 않고 그 위에 새 부품을 맞춰 끼우는 느낌", "retrofit=기존 구조에 새 기능을 보강해 붙임 / upgrade=더 높은 버전으로 올림 / replace=바꿔 끼움"),
    ("robustness", "견고성 / 다양한 조건에도 잘 버팀", "작은 변화나 잡음, 오류가 있어도 성능이나 결론이 크게 무너지지 않는 정도", "조금 흔들어도 쉽게 흐트러지지 않는 단단한 버팀", "robustness=다양한 조건에도 잘 버티는 견고성 / resilience=충격 후 회복력 / sensitivity=작은 변화에 민감함"),
    ("scaling constraint", "확장 제약 / 규모를 키울 때 생기는 한계", "작게는 되던 것이 규모가 커질 때 비용·조직·성능 때문에 막히는 조건", "작은 판에서는 괜찮았는데 크게 키우자 벽이 나타나는 느낌", "scaling constraint=규모 확장에서 생기는 제약 / design constraint=설계 제한 조건 / capacity limit=수용 한계"),
    ("stress-test", "한계 시험을 하다 / 강한 조건에서 검증하다", "평소 조건이 아니라 일부러 부담을 크게 줘 시스템이 어디까지 버티는지 확인하다", "평온할 때가 아니라 세게 흔들어봐서 약한 지점을 찾는 느낌", "stress-test=강한 부담 조건에서 한계와 약점을 시험하다 / field-test=실제 환경에서 시험하다 / validate=타당성을 확인하다"),
    ("trade-off", "상충 관계 / 하나를 얻으면 다른 걸 내주는 선택", "한 장점을 키우면 비용·속도·안전 같은 다른 목표가 줄어드는 균형 문제", "모든 걸 다 못 가져서 한쪽을 올리면 다른 쪽이 내려가는 저울", "trade-off=서로 상충하는 목표 사이의 선택 / compromise=서로 양보한 절충 / balance=균형"),
    ("upgrade path", "업그레이드 경로 / 개선해 나갈 단계", "현재 시스템을 앞으로 더 나은 버전으로 어떤 순서로 바꿀지의 방향", "지금 버전에서 다음 버전으로 넘어갈 길을 미리 열어두는 느낌", "upgrade path=앞으로 개선해 갈 단계 경로 / roadmap=진행 방향표 / transition plan=전환 계획"),
    ("user testing", "사용자 테스트 / 실제 이용자 검증", "실제 쓰는 사람이 제품이나 절차를 해보며 문제와 반응을 확인하는 시험", "만든 사람 눈이 아니라 진짜 사용자 손으로 써보며 검증하는 느낌", "user testing=실제 사용자에게 써보게 하는 검증 / usability testing=사용성 평가 / feedback=반응과 의견"),
    ("workaround", "우회 해결책 / 임시로 돌아가는 방법", "근본 수정 전이라도 당장 막힌 문제를 피해서 진행하게 하는 대체 방법", "정문이 막혔을 때 일단 옆길로 돌아서라도 지나가는 느낌", "workaround=문제를 피해 가는 임시 우회책 / solution=근본 해결책 / fallback=예비 대안"),
    ("zero-defect", "무결함을 목표로 하는 / 오류 없는 상태의", "작은 결함도 허용하지 않으려는 품질 목표나 상태", "대충 괜찮다보다 오류를 끝까지 0에 가깝게 밀어붙이는 느낌", "zero-defect=오류가 없게 맞추려는 / high-quality=품질이 높은 / acceptable=허용 가능한"),
    ("assembly-line", "조립 라인식의 / 단계별 반복 생산의", "작업을 여러 단계로 나눠 순서대로 반복 처리하는 방식의", "한 사람이 통째로 하기보다 공정이 줄지어 이어지는 느낌", "assembly-line=단계별로 이어지는 반복 작업 방식의 / modular=모듈형의 / handcrafted=수작업 중심의"),
    ("capacity buffer", "용량 여유분 / 충격 흡수용 여지", "예상보다 수요나 부담이 늘 때 바로 넘치지 않게 남겨 둔 처리 여력", "꽉 채우지 않고 갑자기 몰려도 버틸 빈칸을 남기는 느낌", "capacity buffer=급증 부담을 견디는 여유 용량 / bandwidth=처리 여력 / reserve=비축분"),
    ("cross-functional", "여러 기능 부서가 함께하는 / 기능 간 협업형의", "한 전문 파트만이 아니라 서로 다른 역할의 팀이 함께 얽혀 일하는", "각자 칸막이를 넘어서 여러 기능이 한 프로젝트 위에 모이는 느낌", "cross-functional=여러 기능 부서가 함께하는 / interdisciplinary=여러 학문 분야가 섞인 / specialized=한 분야에 특화된"),
    ("design brief", "설계 요약서 / 요구사항 개요", "무엇을 왜 만들고 어떤 조건을 만족해야 하는지 압축해 적은 초기 설명", "본격 제작 전에 목표와 조건을 한 장에 잡아두는 설계 출발 문서", "design brief=설계 목표와 요구를 요약한 문서 / proposal=제안서 / specification=세부 명세"),
    ("failure mode", "고장 양상 / 실패가 나타나는 방식", "어떤 조건에서 시스템이나 절차가 어떤 식으로 망가지는지의 패턴", "그냥 안 된다가 아니라 어디가 어떤 모습으로 무너지는지 보는 틀", "failure mode=실패가 나타나는 양상 / malfunction=오작동 / breakdown=작동 붕괴"),
    ("friction point", "마찰 지점 / 진행이 거칠어지는 부분", "사용자 이동이나 업무 흐름에서 불필요한 저항과 지연이 생기는 구체적 지점", "흐름이 매끄럽다가 여기서 손이 걸리는 부분", "friction point=진행 저항이 생기는 지점 / pain point=사용자가 불편해하는 문제 지점 / bottleneck=흐름을 막는 좁은 지점"),
    ("implementation-ready", "실행 준비가 된 / 현장 적용 가능한", "아이디어 수준을 넘어 실제 적용에 필요한 조건과 자료가 어느 정도 갖춰진", "이제 말이 아니라 바로 움직일 만큼 준비가 차 있는 느낌", "implementation-ready=실제로 실행할 준비가 된 / feasible=실현 가능한 / preliminary=예비 단계의"),
    ("interface layer", "접점 층 / 사용자·시스템이 만나는 계층", "한 시스템의 내부 기능과 바깥 사용자나 다른 시스템이 맞닿는 층", "안쪽 복잡한 작동과 바깥 조작이 만나는 얇은 접점판", "interface layer=서로 다른 쪽이 만나는 접점 계층 / boundary layer=경계 근처 층 / interface=접점"),
    ("make-or-buy", "직접 만들지 외부에서 살지의 선택", "기능이나 제품을 내부에서 개발할지 바깥에서 조달할지 따지는 결정", "내부 제작과 외부 구매 사이에서 자원과 시간 저울을 재는 선택", "make-or-buy=내부 제작과 외부 구매 사이의 결정 / outsourcing=외부에 맡김 / in-house=내부에서 수행하는"),
    ("reusability", "재사용성", "한 번 만든 구성이나 방법을 다른 상황이나 프로젝트에도 다시 쓸 수 있는 정도", "한 번 쓰고 버리는 게 아니라 다른 곳에도 다시 끼워 쓸 수 있는 느낌", "reusability=다른 맥락에서도 다시 쓸 수 있음 / transferability=다른 상황에 적용 가능함 / disposability=한 번 쓰고 버림"),
    ("testbed", "시험 플랫폼 / 실험용 환경", "새 아이디어나 시스템을 실제 전면 도입 전에 안전하게 시험해볼 수 있는 환경", "현장 전체를 건드리기 전에 작게 올려 실험하는 판", "testbed=시험용 환경·플랫폼 / prototype=시험용 모델 / field site=현장 위치"),
    ("actionable", "실행 가능한 / 바로 조치로 옮길 수 있는", "아이디어나 피드백이 너무 막연하지 않고 실제 다음 행동으로 연결될 수 있는", "듣고 끝나는 말이 아니라 손이 바로 움직일 수 있게 구체적인 느낌", "actionable=실제 조치로 이어질 수 있는 / practical=실용적인 / vague=모호한"),
    ("buildup", "점진적 축적 / 단계적으로 쌓아 올림", "한 번에 크게 늘리는 게 아니라 요소나 역량을 순서대로 더해 가며 키우는 일", "작은 층을 계속 얹어 전체 구조가 서서히 높아지는 느낌", "buildup=단계적으로 쌓아 감 / expansion=규모를 넓힘 / accumulation=쌓임"),
    ("calculated", "신중히 계산된 / 의도적으로 판단한", "즉흥적이 아니라 비용과 위험, 효과를 따져 보고 의도적으로 선택한", "감으로 던진 게 아니라 수를 재고 놓은 돌 같은 느낌", "calculated=의도와 판단을 거친 / deliberate=신중히 의도적인 / accidental=우연한"),
    ("contingency", "비상 대책 / 상황 변화 대비책", "계획대로 안 될 경우를 대비해 미리 세워 둔 대안이나 조치", "원래 길이 흔들릴 때 바로 펼칠 수 있게 접어 둔 플랜", "contingency=만일의 경우 대비책 / fallback=예비 대안 / emergency=비상 사태"),
    ("customizable", "맞춤 조정 가능한", "사용 목적이나 조건에 따라 설정이나 구성을 바꿀 수 있는", "똑같이 찍힌 한 벌이 아니라 필요한 칸을 내게 맞게 바꾸는 느낌", "customizable=필요에 맞게 조정 가능한 / standardized=표준화된 / adaptable=상황에 맞게 변할 수 있는"),
    ("deliverable", "산출물 / 제출 가능한 결과물", "일이나 프로젝트가 끝날 때 실제로 내놓아야 하는 문서, 결과, 구현물", "열심히 했다는 말보다 손에 잡히게 제출되는 결과물", "deliverable=프로젝트가 내놓는 구체적 산출물 / outcome=결과 / draft=초안"),
    ("dependency", "의존 관계 / 선행 조건", "어떤 작업이나 기능이 다른 요소가 먼저 있어야 제대로 진행되는 관계", "혼자 못 움직이고 앞의 한 조각이 있어야 다음 칸이 열리는 느낌", "dependency=다른 요소에 기대는 선행 관계 / prerequisite=먼저 필요한 조건 / linkage=연결 관계"),
    ("deployment", "배치·도입 / 현장에 실제 적용함", "설계나 개발이 끝난 것을 실제 운영 환경이나 사용자 쪽에 내보내는 일", "만든 걸 내부에 두지 않고 실제 판 위에 올리는 순간", "deployment=실제 환경에 도입·배치함 / development=개발 과정 / implementation=실행에 옮김"),
    ("downgrade", "성능·등급을 낮추다 / 하향 조정하다", "사양, 우선순위, 평가 수준 등을 이전보다 낮은 단계로 내리다", "더 높은 칸에서 한 단계 아래로 내려놓는 느낌", "downgrade=등급·수준을 낮춤 / upgrade=상향 개선 / reduce=양이나 정도를 줄임"),
    ("end-user", "최종 사용자", "중간 관리자나 개발자가 아니라 실제 제품이나 서비스를 직접 쓰는 사람", "만드는 쪽이 아니라 마지막에 손으로 직접 쓰는 사람", "end-user=최종적으로 직접 사용하는 사람 / stakeholder=이해관계자 / developer=개발자"),
    ("error-prone", "오류가 나기 쉬운", "구조나 절차가 복잡하거나 불안정해서 실수나 실패가 자주 생기기 쉬운", "조금만 삐끗해도 잘못되기 쉬운 위태로운 느낌", "error-prone=오류가 잘 나는 / unreliable=믿기 어려운 / robust=잘 버티는"),
    ("evaluation metric", "평가 지표 / 성과를 재는 기준", "개선이나 성공 여부를 판단하기 위해 수치나 기준으로 잡는 측정 항목", "좋아졌다는 말을 숫자나 기준선으로 재는 자", "evaluation metric=성과를 판단하는 측정 기준 / criterion=판단 기준 / benchmark=비교 기준점"),
    ("execution gap", "실행 격차 / 계획과 실제 사이의 벌어짐", "좋은 계획이나 설계가 있어도 현장에서 제대로 구현되지 않아 생기는 차이", "종이 위 계획과 실제 움직임 사이에 벌어진 빈틈", "execution gap=계획과 실행 사이의 차이 / mismatch=서로 안 맞음 / shortfall=부족분"),
    ("fine-grained", "세밀한 / 작은 단위까지 나눈", "큰 덩어리로 뭉뚱그리지 않고 더 작은 구분과 조정 단위까지 나눈", "거친 덩어리 대신 촘촘한 눈금으로 쪼개 보는 느낌", "fine-grained=작은 단위까지 세분화된 / detailed=상세한 / broad=폭넓은"),
    ("high-throughput", "대량 처리형의 / 처리량이 큰", "짧은 시간에 많은 작업이나 입력을 감당하도록 설계된", "하나씩 느리게가 아니라 많이 밀려와도 빠르게 흘려보내는 느낌", "high-throughput=처리량이 큰 / efficient=효율적인 / low-volume=물량이 적은"),
    ("interoperability", "상호 운용성 / 서로 다른 시스템이 함께 작동하는 성질", "서로 다른 도구나 조직, 데이터 체계가 막히지 않고 연결되어 함께 쓰일 수 있는 정도", "각자 따로 놀지 않고 서로 꽂히고 읽히는 연결성", "interoperability=서로 다른 체계가 함께 작동함 / compatibility=서로 맞게 쓸 수 있음 / isolation=분리됨"),
    ("iterative", "반복 개선형의 / 여러 번 수정하며 나아가는", "처음부터 완성본을 고정하지 않고 시험과 수정 단계를 여러 차례 거치는", "한 바퀴 돌고 다시 고쳐 또 돌리는 개선 루프", "iterative=반복하며 개선하는 / linear=한 방향으로 순차적인 / final=최종의"),
    ("maintainable", "유지보수하기 쉬운", "처음 만드는 것보다 이후 수정, 점검, 확장이 지나치게 어렵지 않은", "한 번 세워두고 끝이 아니라 나중에 다시 열어 손보기 편한 느낌", "maintainable=이후 관리와 수정이 쉬운 / durable=오래 버티는 / complex=복잡한"),
    ("milestone-driven", "단계 목표 중심의 / 마일스톤을 따라 가는", "막연히 진행하지 않고 중간 목표와 일정 지점을 기준으로 움직이는", "긴 길을 그냥 걷는 게 아니라 중간 표지판을 찍으며 가는 느낌", "milestone-driven=중간 목표를 기준으로 진행하는 / deadline-driven=마감에 강하게 맞춘 / open-ended=끝이나 기준이 열려 있는"),
    ("operationalize", "실행 가능한 절차로 구체화하다", "추상적 아이디어나 원칙을 실제 운영 규칙, 절차, 측정 방식으로 바꾸다", "말로만 있던 개념을 현장에서 돌릴 수 있는 작업 절차로 내리는 느낌", "operationalize=추상 개념을 실행 절차로 바꿈 / implement=실제로 실행함 / define=의미를 규정함"),
    ("outage-prone", "장애가 잦은 / 중단이 잘 생기는", "서비스나 시스템이 안정적으로 오래 못 버티고 작동 중단이 자주 발생하기 쉬운", "한 번 켜두면 쭉 가는 게 아니라 자주 픽 꺼지는 느낌", "outage-prone=장애나 중단이 자주 생기기 쉬운 / unstable=불안정한 / reliable=신뢰할 수 있는"),
    ("plug-and-play", "바로 연결해 쓸 수 있는", "복잡한 추가 설정 없이 꽂거나 붙이면 비교적 바로 사용할 수 있게 만든", "길게 세팅하지 않고 끼우면 곧장 돌아가는 느낌", "plug-and-play=간단히 연결해 바로 쓰는 / configurable=설정을 바꿀 수 있는 / bespoke=맞춤 제작된"),
    ("post-launch", "출시 이후의 / 도입 후 단계의", "제품이나 제도를 공개하거나 시행한 다음 실제 운영과 반응을 다루는", "문을 연 뒤에야 보이는 문제와 수정이 이어지는 단계", "post-launch=출시·도입 이후의 / pre-launch=출시 전의 / initial=초기의"),
    ("process-oriented", "과정 중심의 / 절차와 흐름을 중시하는", "결과만 보지 않고 일이 어떻게 진행되는지와 단계별 관리에 초점을 두는", "마지막 점수보다 중간 흐름과 절차를 따라가며 보는 느낌", "process-oriented=과정과 절차를 중시하는 / outcome-oriented=결과 중심의 / procedural=절차상의"),
    ("quality-assurance", "품질 보증 / 기준을 맞추는 점검 체계", "완성 전에 오류와 편차를 잡고 일정 수준을 유지하도록 확인하는 과정이나 체계", "그냥 만들고 끝이 아니라 기준선 아래로 떨어지지 않게 거르는 점검망", "quality-assurance=품질 기준을 확인·보증하는 체계 / inspection=검사 / optimization=성능 개선"),
    ("resource-intensive", "자원을 많이 쓰는 / 비용·인력·시간이 많이 드는", "원하는 결과를 내는 데 필요한 돈, 사람, 시간, 계산량이 큰", "성과는 나올 수 있지만 그만큼 연료를 많이 먹는 느낌", "resource-intensive=자원을 많이 소모하는 / costly=비용이 많이 드는 / efficient=자원 대비 효율적인"),
    ("roadmap", "추진 로드맵 / 단계별 방향 계획", "목표까지 어떤 순서와 우선순위로 진행할지 큰 흐름을 잡은 계획", "최종 목적지까지 어디를 어떤 차례로 지날지 그린 길 지도", "roadmap=단계별 추진 방향을 잡은 계획 / timeline=시간 순서표 / strategy=큰 전략"),
    ("serviceability", "정비 용이성 / 고치고 관리하기 쉬운 정도", "문제가 생겼을 때 분해, 점검, 교체, 복구를 얼마나 쉽게 할 수 있는지", "고장 났을 때 닫힌 상자보다 열고 손보기 쉬운 구조", "serviceability=정비와 수리가 쉬운 정도 / maintainability=유지관리 용이성 / durability=오래 버티는 성질"),
    ("streamlined", "간소화된 / 불필요한 단계가 줄어든", "절차나 구조에서 군더더기를 줄여 더 빠르고 매끄럽게 만든", "복잡한 가지를 쳐내고 한결 매끈한 흐름으로 다듬은 느낌", "streamlined=불필요한 단계를 줄여 매끄럽게 만든 / simplified=단순화된 / elaborate=복잡하고 자세한"),
    ("suboptimal", "최적에는 못 미치는 / 다소 비효율적인", "완전히 실패는 아니지만 가능한 가장 좋은 선택이나 성능에는 못 미치는", "돌아가긴 하지만 더 나은 해법에 비해 살짝 덜 맞는 느낌", "suboptimal=최선보다 못한 / inefficient=비효율적인 / adequate=기본은 충족하는"),
    ("throughput", "처리량 / 일정 시간 동안 감당하는 작업 규모", "정해진 시간 안에 시스템이나 절차가 처리할 수 있는 양", "통로를 지나는 개별 속도보다 전체가 얼마나 많이 지나가느냐", "throughput=일정 시간 내 처리량 / capacity=최대 수용 능력 / output=산출량"),
    ("underutilized", "충분히 활용되지 않는", "가지고 있는 자원이나 기능, 공간이 가능성에 비해 덜 쓰이는", "쓸 수 있는 여력이 남아 있는데 반쯤 비어 있는 느낌", "underutilized=잠재력보다 덜 활용되는 / idle=놀고 있는 / overused=과도하게 쓰인"),
    ("upgradable", "업그레이드 가능한 / 나중에 개선해 올릴 수 있는", "처음 상태에서 끝나지 않고 이후 성능이나 기능을 더 높은 수준으로 바꿀 수 있는", "닫힌 완제품보다 다음 버전으로 올릴 길이 열려 있는 느낌", "upgradable=나중에 개선·확장해 올릴 수 있는 / extensible=기능을 덧붙이기 쉬운 / fixed=고정된"),
    ("usability", "사용성 / 실제로 쓰기 쉬운 정도", "사용자가 기능을 배우고 조작하며 원하는 일을 얼마나 어렵지 않게 할 수 있는지", "기능이 많다는 말보다 손에 잡았을 때 막히지 않고 쓰기 쉬운지", "usability=실제 사용하기 쉬운 정도 / accessibility=접근하기 쉬운 정도 / functionality=기능 자체"),
    ("versioning", "버전 관리 / 변경판을 구분해 다루는 일", "수정된 상태들을 섞지 않고 어떤 판이 어떤 변경을 담는지 나눠 관리하는 것", "계속 고치더라도 어느 판이 어떤 상태인지 꼬리표를 붙여 두는 느낌", "versioning=서로 다른 수정판을 구분해 관리함 / tracking=변화를 추적함 / documentation=기록 문서화"),
    ("viable", "실현 가능한 / 실제로 굴러갈 수 있는", "이론상 가능하다는 수준을 넘어 조건과 비용 안에서 실제 지속될 수 있는", "그럴듯한 생각이 아니라 현실 바닥에 발을 붙이고 버틸 수 있는 느낌", "viable=현실적으로 실행·지속 가능한 / feasible=실행 가능성이 있는 / ideal=이상적인"),
    ("workflow", "업무 흐름 / 작업이 이어지는 절차", "한 사람이든 여러 사람이든 일이 어떤 순서와 연결로 진행되는지의 흐름", "개별 과제가 흩어진 점이 아니라 다음 단계로 이어지는 일의 길", "workflow=작업이 이어지는 절차 흐름 / procedure=정해진 절차 / schedule=일정"),
    ("workload", "업무량 / 처리해야 할 부담", "한 사람, 팀, 시스템이 감당해야 하는 일의 총량이나 부담 정도", "할 일이 책상 위에 얼마나 무겁게 쌓여 있는지", "workload=감당해야 할 일의 양과 부담 / capacity=감당 가능 한계 / assignment=맡겨진 과제"),
    ("backward-compatible", "하위 호환되는 / 이전 버전과도 맞는", "새 버전이 나와도 예전 자료나 방식과 어느 정도 함께 작동할 수 있는", "앞으로 바꾸되 옛것과 연결선이 끊기지 않게 남겨두는 느낌", "backward-compatible=이전 버전과도 호환되는 / interoperable=서로 다른 체계가 함께 작동하는 / incompatible=서로 안 맞는"),
    ("constraint-aware", "제약을 의식한 / 한계를 반영해 판단하는", "이상적 목표만 보지 않고 시간, 예산, 규정, 성능 한계를 함께 고려하는", "하고 싶은 것보다 실제 테두리를 같이 보며 움직이는 느낌", "constraint-aware=제약 조건을 반영하는 / idealistic=현실 제약보다 이상을 앞세우는 / pragmatic=현실적으로 판단하는"),
    ("design-driven", "설계 중심의 / 구조적 구상을 바탕으로 한", "즉흥적 추가보다 목표와 구조를 먼저 잡고 그 설계에 따라 전개되는", "되는 대로 붙이는 게 아니라 설계 틀이 방향을 끌고 가는 느낌", "design-driven=설계 구상이 중심이 되는 / ad hoc=즉석 대응식의 / systematic=체계적인"),
    ("feasibility study", "실현 가능성 검토", "아이디어를 본격 추진하기 전에 비용, 조건, 위험, 자원을 따져 실제 가능한지 보는 조사", "바로 뛰어들기 전에 이 길이 정말 열리는지 먼저 땅을 두드려 보는 단계", "feasibility study=추진 전 실행 가능성을 따지는 검토 / pilot study=작게 먼저 해보는 시범 조사 / evaluation=평가"),
    ("fit gap", "적합성 차이 / 요구와 현재 상태의 어긋남", "필요한 조건과 현재 도구나 설계가 얼마나 맞지 않는지에서 생기는 차이", "맞춰 끼우려는데 모서리가 조금 안 맞아 생기는 틈", "fit gap=요구와 현재 상태 사이의 부적합 차이 / mismatch=서로 안 맞음 / deficiency=부족함"),
    ("go-live", "정식 가동 / 실제 운영 시작", "시험이나 준비 단계를 지나 사용자가 실제로 쓰는 운영 상태로 전환하는 시점", "리허설이 아니라 이제 실제 무대 조명이 켜지는 순간", "go-live=실제 운영을 시작함 / rollout=단계적으로 도입함 / trial=시험 운영"),
    ("high-availability", "고가용성의 / 오래 끊김 없이 쓸 수 있는", "장애와 중단을 최소화해 사용자가 가능한 오래 계속 접근할 수 있게 설계된", "잠깐씩 자주 멈추는 게 아니라 거의 늘 열려 있도록 버티는 느낌", "high-availability=끊김을 줄여 오래 쓸 수 있는 / reliable=믿고 쓸 수 있는 / intermittent=간헐적인"),
    ("integration point", "통합 접점 / 서로 연결되는 지점", "서로 다른 기능이나 시스템이 데이터를 넘기거나 함께 작동하도록 맞닿는 부분", "따로 만든 조각들이 여기서 서로 손을 잡는 연결 마디", "integration point=서로 다른 요소가 연결되는 접점 / interface=접점 / boundary=경계"),
    ("minimum viable", "최소한으로 실행 가능한", "필수 기능만 갖춰 작게라도 실제 작동과 검증이 가능하도록 만든 수준의", "완벽한 풀세트보다 일단 핵심만 넣어 움직이게 만든 출발선", "minimum viable=최소 기능으로도 실제 검증이 가능한 / complete=완비된 / provisional=임시의"),
    ("off-the-shelf", "기성품형의 / 바로 가져다 쓸 수 있는", "새로 맞춤 제작하지 않고 이미 만들어진 제품이나 해결책을 그대로 활용하는", "처음부터 깎아 만들지 않고 진열대에서 바로 집어 오는 느낌", "off-the-shelf=이미 있는 기성 솔루션을 쓰는 / custom-built=맞춤 제작한 / in-house=내부에서 만든"),
    ("onboarding", "적응·도입 지원 / 새 사용자를 안착시키는 과정", "새 사람이나 사용자가 시스템, 절차, 역할을 익혀 실제로 쓰기 시작하게 돕는 과정", "문 앞에 세워두지 않고 안으로 데려와 손에 익게 만드는 느낌", "onboarding=새 사용자가 익숙해지도록 안착시키는 과정 / training=훈련·교육 / orientation=초기 안내"),
    ("performance baseline", "성능 기준선 / 비교 출발점", "개선 전 현재 상태나 표준 상태를 측정해 이후 변화와 비교하는 기준", "좋아졌는지 보려면 먼저 바닥에 그어두는 시작선", "performance baseline=성능 비교용 기준선 / benchmark=비교 기준점 / target=도달 목표"),
    ("process bottleneck", "절차상 병목 / 흐름을 막는 단계", "전체 작업 중 특정 단계가 유독 느리거나 막혀 뒤의 흐름까지 지연시키는 지점", "일이 줄줄 흐르다가 한 칸에서 꽉 막혀 뒤가 밀리는 느낌", "process bottleneck=절차 흐름을 막는 병목 단계 / delay point=지연 지점 / constraint=제약"),
    ("readiness check", "준비 상태 점검", "실행이나 전환 전에 필요한 조건, 자료, 인력, 위험 대응이 갖춰졌는지 확인하는 절차", "출발 버튼을 누르기 전에 빠진 나사가 없는지 한 번 훑는 느낌", "readiness check=실행 전 준비 상태를 확인함 / inspection=검사 / approval=승인"),
    ("requirements drift", "요구사항 변동 / 처음 조건이 점점 달라짐", "프로젝트가 진행되는 동안 처음 정한 요구나 범위가 조금씩 바뀌며 흔들리는 현상", "처음 그은 목표선이 가만히 있지 않고 옆으로 조금씩 이동하는 느낌", "requirements drift=진행 중 요구사항이 점점 변함 / scope creep=범위가 조금씩 커짐 / revision=수정"),
    ("scalable architecture", "확장 가능한 구조 설계", "사용량이나 기능이 커져도 완전히 갈아엎지 않고 키울 수 있게 짠 구조", "작은 집으로 끝나지 않고 층을 더 올릴 여지를 남긴 골조", "scalable architecture=규모 확장에 대응 가능한 구조 / modular design=모듈형 설계 / fixed layout=고정된 배치"),
    ("service continuity", "서비스 연속성 / 중단 없이 이어지는 운영성", "문제나 전환이 있어도 사용자에게 제공되는 핵심 기능이 끊기지 않고 이어지는 상태", "중간에 덜컥 끊기지 않게 흐름의 불을 계속 켜두는 느낌", "service continuity=서비스가 끊기지 않고 이어지는 상태 / availability=이용 가능성 / interruption=중단"),
    ("side-by-side rollout", "병행 도입 / 새 방식과 기존 방식을 함께 운영하며 전환함", "새 시스템을 바로 단독으로 바꾸지 않고 기존 방식과 나란히 돌려 비교와 안전성을 확보하는 전환 방식", "한쪽 다리를 바로 치우지 않고 새 다리와 옛 다리를 잠시 같이 놓는 느낌", "side-by-side rollout=기존·새 방식을 병행하며 전환함 / phased rollout=단계적 도입 / full cutover=한 번에 전면 전환"),
    ("single-point failure", "단일 장애 지점 / 하나가 무너지면 전체가 흔들리는 약점", "특정 한 요소에 너무 의존해 그 부분이 실패하면 전체 서비스나 과정이 크게 멈추는 구조적 약점", "기둥 하나에만 너무 기대서 그 하나가 빠지면 전체가 휘청이는 느낌", "single-point failure=하나의 실패가 전체 장애로 번지는 지점 / redundancy=고장 대비 여분 중복 / bottleneck=흐름을 막는 병목"),
    ("solution-oriented", "해결 중심의 / 문제를 풀 수단에 초점을 둔", "비판이나 원인 설명에서 멈추지 않고 실제 무엇을 바꿀지와 대안을 중심으로 보는", "문제만 붙잡고 있기보다 다음 조치 쪽으로 시선을 밀어주는 느낌", "solution-oriented=해결책과 실행에 초점을 둔 / problem-focused=문제 자체에 초점을 둔 / constructive=건설적인"),
    ("stress condition", "부하 조건 / 일부러 강한 압력을 준 상황", "정상보다 더 높은 수요, 제한, 속도, 압력을 걸어 성능과 약점을 보는 조건", "평소보다 세게 눌러서 어디서 삐걱이는지 드러내는 환경", "stress condition=부하가 큰 시험 조건 / normal condition=일반 조건 / edge case=예외적 극단 상황"),
    ("technical debt", "기술 부채 / 빠른 임시 해법 때문에 나중에 치를 관리 비용", "당장 빨리 넘기려고 구조를 깔끔히 못 만든 탓에 이후 수정과 유지보수가 더 무거워지는 누적 부담", "지금은 넘어갔지만 나중에 이자처럼 돌아오는 구조의 빚", "technical debt=임시 설계가 남긴 미래 관리 부담 / shortcut=지름길식 처리 / maintenance cost=유지보수 비용"),
    ("trialable", "시범적으로 써볼 수 있는", "전면 채택 전에 작은 범위에서 부담 적게 테스트해볼 수 있는", "큰 약속 전에 먼저 한 번 손에 얹어 시험해볼 수 있는 느낌", "trialable=작게 먼저 써보며 시험 가능한 / testable=검증 가능한 / irreversible=되돌리기 어려운"),
    ("upgrade-ready", "업그레이드 준비가 된 / 개선 전환을 염두에 둔", "나중에 새 기능이나 성능 개선을 넣기 쉽게 필요한 구조나 호환성을 미리 갖춘", "닫아 걸어 잠근 구조가 아니라 다음 확장을 받아들일 문을 열어둔 느낌", "upgrade-ready=향후 업그레이드를 넣기 쉽게 준비된 / upgradable=업그레이드 가능한 / locked-in=한 방식에 묶인"),
    ("validation step", "검증 단계 / 맞는지 확인하는 절차", "결과나 설계가 기준을 충족하는지 다음 단계로 넘어가기 전에 확인하는 과정", "바로 지나가지 않고 한 번 멈춰 맞는지 찍고 넘어가는 체크포인트", "validation step=기준 충족 여부를 확인하는 단계 / testing=시험 / approval=승인"),
    ("workable", "실행 가능한 / 현실적으로 돌아가는", "이론상 완벽하지는 않아도 실제 조건 안에서 작동하고 유지될 수 있는", "이상적이지 않아도 손에 쥐고 굴릴 수는 있는 현실적 해법", "workable=현실적으로 실행 가능한 / ideal=이상적인 / impractical=비현실적인"),
    ("co-design", "공동 설계 / 사용자나 이해관계자와 함께 설계함", "전문가가 혼자 정하지 않고 실제 사용자나 관련자와 같이 요구와 구조를 만들어 가는 방식", "설계자가 위에서 내려주는 게 아니라 쓰는 사람과 한 책상에서 같이 그리는 느낌", "co-design=이해관계자와 함께 설계함 / consultation=의견을 구함 / top-down=위에서 아래로 정함"),
    ("decision gate", "결정 관문 / 다음 단계로 넘길지 판단하는 지점", "각 단계 사이에서 기준을 보고 계속 진행, 수정, 중단을 판단하는 공식 점검 지점", "아무 때나 흘러가는 게 아니라 문 앞에서 조건을 보고 열지 말지 정하는 느낌", "decision gate=다음 단계 진행 여부를 판단하는 지점 / checkpoint=중간 확인 지점 / deadline=마감 시점"),
    ("fit check", "적합성 점검 / 요구와 맞는지 확인", "해결책이나 설계가 실제 목적, 사용자, 제약 조건에 맞는지 다시 확인하는 것", "만든 조각이 원래 빈칸에 진짜 잘 들어맞는지 대보는 느낌", "fit check=요구와 목적에 맞는지 점검함 / inspection=상태를 검사함 / validation=기준 충족을 확인함"),
    ("implementation lag", "실행 지연 / 결정 후 실제 반영까지의 시간차", "정책이나 설계가 정해진 뒤 현장에서 실제 바뀌기까지 시간이 벌어지는 현상", "머리로는 정해졌는데 손과 시스템이 따라오는 데 시간이 남는 느낌", "implementation lag=결정과 실제 실행 사이의 지연 / delay=늦어짐 / transition period=전환 기간"),
    ("maintainability", "유지보수성 / 나중에 관리하고 고치기 쉬운 정도", "초기 완성보다 이후 수정, 점검, 확장을 얼마나 부담 적게 할 수 있는지", "한 번 세운 뒤 다시 열어 손보는 일이 너무 고역이 아닌 구조", "maintainability=유지보수하기 쉬운 정도 / serviceability=정비 용이성 / robustness=잘 버티는 견고성"),
    ("open-ended", "열린 형태의 / 답이나 끝이 하나로 닫히지 않은", "문제 해결이나 설계 방향이 한 가지로 고정되지 않고 여러 방식으로 이어질 수 있는", "정해진 한 칸으로 닫히지 않고 아직 선택지가 벌어져 있는 느낌", "open-ended=끝이나 답이 하나로 고정되지 않은 / fixed=고정된 / flexible=유연한"),
    ("prerelease", "정식 출시 전의 / 사전 공개 단계의", "완전한 정식 버전 이전에 제한적으로 먼저 내놓아 반응과 문제를 보는", "정식 개장 전 문을 살짝 열어 먼저 시험해보는 느낌", "prerelease=정식 출시 전의 / beta=시험판의 / post-launch=출시 후의"),
    ("rework", "재작업하다 / 다시 손봐 고치다", "처음 만든 결과가 기준이나 요구에 충분히 맞지 않아 다시 수정하거나 다시 처리하다", "완료 도장을 찍지 못해 다시 작업대 위로 올라오는 느낌", "rework=기준에 맞추려 다시 작업함 / revise=내용을 수정함 / discard=버림"),
    ("scalability", "확장성 / 규모가 커져도 대응하는 능력", "사용량, 데이터, 범위가 커질 때 구조를 완전히 무너뜨리지 않고 키울 수 있는 정도", "작게만 되는 구조가 아니라 더 커져도 판을 넓혀 받칠 수 있는 힘", "scalability=규모 확대에 대응하는 능력 / flexibility=상황에 맞게 바뀌는 유연성 / capacity=수용 능력"),
    ("service bottleneck", "서비스 병목 / 제공 흐름을 막는 지점", "사용자 요청이나 지원 흐름에서 특정 구간이 느려 전체 서비스 속도와 품질을 떨어뜨리는 부분", "전체 서비스가 순조롭다가 이 한 지점에서 줄이 길게 막히는 느낌", "service bottleneck=서비스 흐름을 막는 병목 / pain point=사용자가 불편해하는 지점 / outage=서비스 중단"),
    ("task sequencing", "작업 순서 배치 / 어떤 일을 먼저 할지 정함", "서로 얽힌 작업들을 어떤 차례로 진행해야 지연과 충돌이 줄어드는지 배열하는 것", "무작정 동시에 던지지 않고 앞뒤 순서를 짜서 길을 정리하는 느낌", "task sequencing=작업 진행 순서를 배치함 / prioritization=우선순위를 정함 / scheduling=시간표를 잡음"),
    ("usability gap", "사용성 격차 / 기능은 있어도 실제 쓰기 어려운 차이", "기능적으로는 가능하지만 사용자가 이해하거나 조작하기엔 불편해서 생기는 간극", "기계는 되는데 사람이 손대면 자꾸 헷갈리는 틈", "usability gap=기능과 실제 사용 편의 사이의 차이 / learning curve=익숙해지는 데 드는 어려움 / accessibility gap=접근성 차이"),
    ("value-for-money", "가격 대비 가치가 있는", "들인 비용에 비해 실제 효용, 품질, 만족이 충분히 크다고 볼 수 있는", "싸다는 말보다 낸 돈만큼 혹은 그 이상으로 값어치를 하는 느낌", "value-for-money=비용 대비 가치가 좋음 / cost-effective=비용 대비 효과가 좋음 / overpriced=값에 비해 비싼"),
    ("workflow redesign", "업무 흐름 재설계", "기존 절차를 그대로 두지 않고 단계, 역할, 연결 방식을 다시 짜서 더 낫게 만드는 일", "길 위 장애물을 조금 손보는 수준이 아니라 흐름의 동선을 다시 그리는 느낌", "workflow redesign=작업 절차 흐름을 다시 설계함 / process improvement=절차 개선 / reorganization=조직이나 구조를 다시 짬"),
]


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join([f"핵심 뜻: {core}", f"부가 뜻: {extra}", f"핵심 느낌: {feeling}", f"구분: {distinction}"])


def main() -> None:
    existing = set()
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            existing.update(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)

    rows = []
    for word, core, extra, feeling, distinction in CARDS:
        if word in existing:
            continue
        rows.append([word, build_back(core, extra, feeling, distinction)])
        if len(rows) == 100:
            break
    if len(rows) < 100:
        raise RuntimeError(f"only {len(rows)} cards")

    with TARGET.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)

    ets_words = []
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            ets_words.extend(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)
    (ROOT / ".existing_words.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_ets_headwords.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")

    awl_words = []
    for path in sorted(ROOT.glob("toefl_awl_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            awl_words.extend(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)
    (ROOT / "all_awl_headwords.txt").write_text("\n".join(awl_words) + "\n", encoding="utf-8")
    (ROOT / "all_headwords.txt").write_text("\n".join(sorted(set(ets_words + awl_words))) + "\n", encoding="utf-8")

    manifest_path = ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if TARGET.name not in manifest["files_created"]:
        manifest["files_created"].insert(18, TARGET.name)
    manifest["total_ets_cards"] = len(ets_words)
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (ROOT / "generation_notes.md").write_text(
        (ROOT / "generation_notes.md").read_text(encoding="utf-8").replace(
            "- ETS sets `01` to `18` exist, bringing the ETS-based total to 1800 cards\n",
            "- ETS sets `01` to `19` exist, bringing the ETS-based total to 1900 cards\n",
        ),
        encoding="utf-8",
    )

    plan = ROOT / "WORK_PLAN.md"
    plan.write_text(
        plan.read_text(encoding="utf-8")
        .replace(
            "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_18.tsv`\n",
            "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_19.tsv`\n",
        )
        .replace(
            "- Current ETS row count after the latest expansion pass: 1800\n",
            "- Current ETS row count after the latest expansion pass: 1900\n",
        ),
        encoding="utf-8",
    )

    task_next = ROOT / ".task_next.md"
    task_next.write_text(
        task_next.read_text(encoding="utf-8")
        .replace("`toefl_ets_2026_set_19.tsv`", "`toefl_ets_2026_set_20.tsv`")
        .replace(
            "design, constraints, feasibility, implementation, systems, and innovation in practical problem-solving, while avoiding narrow engineering/materials jargon.",
            "creative works, visual/auditory representation, aesthetics, interpretation, and performance, with transferable culture-and-analysis vocabulary.",
        ),
        encoding="utf-8",
    )

    print(f"{TARGET.name}: {len(rows)} cards")


if __name__ == "__main__":
    main()
