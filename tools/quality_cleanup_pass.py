from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ETS_PATTERN = "toefl_ets_2026_set_*.tsv"
AWL_PATTERN = "toefl_awl_set_*.tsv"

SPECIALIZED_ETS_DROP = {
    "ecology": "too field-specific as a subject label for the broad ETS core",
    "sediment": "earth-science-specific and too narrow for the broad ETS core",
    "fossil": "narrow paleontology term for the broad ETS core",
    "molecular": "too specialized toward molecular science for the broad ETS core",
    "geotagged": "too product/metadata-specific for the broad ETS core",
    "morphological": "too morphology-specific for the broad ETS core",
}

AWL_OVERRIDES = {
    "analyse": (
        "분석하다 / 구조와 원인을 따져보다",
        "자료나 현상을 쪼개서 구성·패턴·의미를 밝히다",
        "겉만 보지 않고 안쪽 구조를 분해해서 읽는 느낌",
        "analyse=구조·원인을 분석하다 / examine=면밀히 살피다 / assess=가치·수준을 평가하다",
    ),
    "approach": (
        "접근법 / 문제를 다루는 방식",
        "연구, 설명, 해결을 어떤 관점과 절차로 밀고 갈지의 방법",
        "문제 앞에서 어느 방향으로 들어갈지 잡는 길",
        "approach=문제를 다루는 방식 / method=구체적 절차 / perspective=보는 관점",
    ),
    "area": (
        "영역 / 분야 / 지역",
        "공간적 지역뿐 아니라 연구나 활동의 특정 범위",
        "넓은 전체 안에서 특정 부분을 둘러 잡은 구역",
        "area=범위·영역 일반 / field=전문 분야 / region=지리적 지역",
    ),
    "assess": (
        "평가하다 / 수준·영향·가치를 판단하다",
        "근거를 보고 상태, 크기, 중요성, 품질을 따져 보다",
        "대상을 그냥 보지 않고 기준을 대고 값을 매기는 느낌",
        "assess=기준을 두고 평가하다 / measure=수치로 재다 / analyze=구조를 분석하다",
    ),
    "assume": (
        "가정하다 / 사실이라고 일단 받아들이다",
        "증명이 끝나기 전이라도 논의나 계산을 위해 어떤 전제를 놓다",
        "확정 도장 전에 일단 이렇다고 바닥 가정을 깔아두는 느낌",
        "assume=일단 전제로 놓다 / presume=그럴 가능성이 높다고 보다 / verify=확인하다",
    ),
    "benefit": (
        "이익 / 도움이 되는 효과",
        "정책, 선택, 변화가 가져오는 유리한 결과나 긍정적 효용",
        "들인 노력 뒤에 실제로 남는 좋은 쪽 몫",
        "benefit=긍정적 이익과 효용 / profit=금전적 이익 / advantage=유리한 점",
    ),
    "consist": (
        "~으로 이루어지다 / 핵심이 ~에 있다",
        "어떤 전체가 몇 개 요소로 구성되거나 본질이 특정 성격에 놓여 있다",
        "겉덩어리를 보면 안쪽이 무엇으로 채워졌는지 드러나는 느낌",
        "consist=구성되다·본질이 ~에 있다 / comprise=전체가 부분을 포함하다 / include=포함하다",
    ),
    "contract": (
        "계약 / 법적 구속력이 있는 합의",
        "당사자 사이 권리와 의무를 정해 공식적으로 묶는 약속",
        "말로만 한 약속보다 법과 문서로 매듭을 묶은 느낌",
        "contract=법적 구속력이 있는 계약 / agreement=합의 일반 / treaty=국가 간 조약",
    ),
    "derive": (
        "이끌어내다 / ~에서 얻다·유래하다",
        "자료, 원리, 출처에서 결론·공식·이익·기원을 뽑아내다",
        "결과가 허공에서 나온 게 아니라 앞의 출처 줄에서 당겨져 나오는 느낌",
        "derive=근거나 출처에서 얻어내다 / infer=증거로 추론하다 / originate=기원하다",
    ),
    "format": (
        "형식 / 자료를 배열하고 제시하는 틀",
        "문서, 데이터, 발표, 파일이 어떤 구조와 규칙으로 정리되어 있는지의 형태",
        "내용을 아무렇게나 두지 않고 담는 칸과 순서를 정한 틀",
        "format=자료를 담는 형식과 구조 / layout=눈에 보이는 배치 / protocol=진행 규칙",
    ),
    "distribute": (
        "분배하다 / 퍼뜨려 나누다",
        "자원, 정보, 물건, 부담을 여러 대상이나 구역에 나눠 보내다",
        "한 덩어리를 여러 손과 위치로 갈라 흘려보내는 느낌",
        "distribute=여러 곳에 나눠 보내다 / allocate=몫을 정해 배분하다 / spread=퍼지다",
    ),
    "found": (
        "설립하다 / 기초를 세우다",
        "조직, 기관, 도시, 제도를 처음 세워 공식적으로 출발시키다",
        "없던 조직의 첫 기둥을 땅에 박는 느낌",
        "found=조직·기관을 설립하다 / establish=제도나 기반을 확립하다 / discover=발견하다",
    ),
    "integral": (
        "필수적인 / 전체에 빠질 수 없이 들어간",
        "부가 장식이 아니라 구조나 기능의 핵심 일부로 안에 붙어 있는",
        "겉에 잠깐 얹힌 게 아니라 본체 안에 박힌 필수 조각",
        "integral=전체에 필수로 들어간 / inherent=본래부터 내재한 / optional=선택적인",
    ),
    "intermediate": (
        "중간 단계의 / 두 끝 사이에 놓인",
        "초기와 최종 사이의 수준, 위치, 단계, 결과물을 가리키는",
        "출발점도 끝점도 아닌 가운데 징검다리 칸",
        "intermediate=중간 단계의 / preliminary=본격 이전의 예비 단계 / advanced=고급 단계의",
    ),
    "manual": (
        "설명서 / 손으로 하는",
        "사용법을 적은 안내서이거나 자동이 아니라 사람이 직접 조작하는 방식의",
        "자동으로 굴러가는 게 아니라 손과 절차를 직접 얹는 느낌",
        "manual=설명서 또는 수동의 / handbook=안내서 / automatic=자동의",
    ),
    "mature": (
        "성숙한 / 충분히 발달하다",
        "사람, 제도, 생각, 시장, 기술이 시간이 지나 더 안정되고 완성도 있게 자라다",
        "덜 익은 상태를 지나 속이 찬 단계로 넘어가는 느낌",
        "mature=충분히 발달하고 성숙한 / develop=발달하다 / premature=너무 이른",
    ),
    "mediate": (
        "중재하다 / 사이에서 조정하다",
        "대립, 관계, 영향이 직접 충돌하지 않도록 중간에서 연결하거나 완화하다",
        "둘 사이에 들어가 말과 힘의 충돌을 정리하는 느낌",
        "mediate=사이에서 중재·매개하다 / negotiate=직접 협상하다 / intervene=개입하다",
    ),
    "medium": (
        "매체 / 중간 수단",
        "정보, 예술, 신호, 물질이 전달되거나 담기는 경로나 재료",
        "내용 자체보다 그 내용을 실어 나르는 그릇과 통로",
        "medium=전달 매체나 수단 / method=방법 / environment=주변 환경",
    ),
    "minimal": (
        "최소한의 / 아주 적은",
        "필요한 수준만 남기고 양, 정도, 장식을 최대한 줄인",
        "딱 필요한 선만 남기고 나머지는 덜어낸 느낌",
        "minimal=최소한의 / minimum=허용 가능한 최저선 / limited=제한된",
    ),
    "mutual": (
        "상호의 / 서로 공유하는",
        "한쪽만이 아니라 둘 이상이 함께 느끼거나 주고받는 관계의",
        "화살표가 한 방향이 아니라 양쪽으로 이어진 느낌",
        "mutual=서로 공유하고 주고받는 / reciprocal=서로 맞교환하는 / common=공통의",
    ),
    "norm": (
        "규범 / 일반적으로 받아들여지는 기준",
        "특정 집단이나 상황에서 보통 정상적이고 기대된다고 여겨지는 기준",
        "문서에 다 적히지 않아도 다들 맞춰 보는 기준선",
        "norm=사회적·일반적 기준 / rule=명시적 규칙 / average=평균값",
    ),
    "overlap": (
        "겹치다 / 공통 부분이 생기다",
        "범위, 시기, 기능, 내용이 완전히 분리되지 않고 일부를 함께 공유하다",
        "두 원이 따로 있다가 가운데가 겹쳐 같은 구역을 갖는 느낌",
        "overlap=일부 범위가 겹치다 / intersect=교차하다 / coincide=동시에 일치하다",
    ),
    "passive": (
        "수동적인 / 직접 나서지 않는",
        "행동이나 반응이 스스로 주도하기보다 외부를 받는 쪽으로 머무는",
        "앞에서 밀고 나가기보다 뒤에서 받아만 두는 느낌",
        "passive=수동적인 / inactive=활동이 없는 / receptive=받아들이는",
    ),
    "portion": (
        "부분 / 몫",
        "전체에서 떼어 낸 한 조각이거나 나눠 받은 일정한 비율의 몫",
        "큰 덩어리에서 잘려 나온 자기 몫의 한 조각",
        "portion=전체 중 한 부분이나 몫 / part=부분 일반 / share=나눠 가진 몫",
    ),
    "preliminary": (
        "예비의 / 본격 단계 전에 먼저 하는",
        "최종 결론이나 본실행 전에 방향과 가능성을 먼저 확인하는 초기 단계의",
        "정식 출발 전에 먼저 길과 상태를 가볍게 찍어보는 단계",
        "preliminary=본격 전에 하는 예비의 / initial=초기의 / final=최종의",
    ),
    "protocol": (
        "절차 규약 / 정해진 실행 규칙",
        "실험, 통신, 회의, 외교에서 어떤 순서와 형식으로 진행할지 정한 규칙",
        "아무렇게나 하지 않게 순서와 형식을 묶어 둔 진행 매뉴얼",
        "protocol=정해진 절차·규약 / procedure=절차 / etiquette=예절 규범",
    ),
    "qualitative": (
        "질적인 / 수치보다 성격과 특성을 보는",
        "양의 크기보다 종류, 의미, 경험, 특성 차이를 중심으로 다루는",
        "숫자 눈금보다 어떤 결을 가졌는지 먼저 보는 느낌",
        "qualitative=성격과 의미를 보는 질적 접근의 / quantitative=수량을 재는 / descriptive=묘사적인",
    ),
    "refine": (
        "정교하게 다듬다 / 개선하다",
        "거친 초안이나 방법을 세부 조정과 수정으로 더 정확하고 매끄럽게 만들다",
        "큰 틀을 부수기보다 표면과 결을 곱게 갈아 맞추는 느낌",
        "refine=더 정교하게 다듬다 / revise=내용을 고치다 / simplify=단순화하다",
    ),
    "relax": (
        "완화하다 / 느슨하게 하다",
        "긴장, 규제, 제약, 기준의 강도를 낮추거나 몸과 상태를 풀다",
        "꽉 조여 있던 줄을 조금 풀어 숨통을 여는 느낌",
        "relax=긴장이나 제약을 완화하다 / ease=부담을 덜다 / tighten=조이다",
    ),
    "restrain": (
        "억제하다 / 제한하다",
        "행동, 감정, 힘, 범위를 마음대로 커지지 못하게 붙잡아 두다",
        "앞으로 튀어나가려는 것을 손으로 다시 잡아당기는 느낌",
        "restrain=움직임이나 확대를 억제하다 / restrict=범위나 접근을 제한하다 / suppress=눌러 드러나지 않게 하다",
    ),
    "rigid": (
        "경직된 / 쉽게 휘거나 바뀌지 않는",
        "물리적으로 단단히 굳었거나 규칙·태도가 유연하게 조정되지 않는",
        "조금만 바꿔도 되는 게 아니라 딱딱하게 굳어 잘 안 휘는 느낌",
        "rigid=잘 휘지 않고 경직된 / strict=규칙이 엄격한 / flexible=유연한",
    ),
    "route": (
        "경로 / 어떤 지점으로 가는 길이나 절차",
        "물리적 이동 경로뿐 아니라 목표에 도달하는 진행 방향이나 통로",
        "출발점에서 목적지까지 이어지는 지나가는 선",
        "route=가는 경로나 진행 통로 / path=길 일반 / procedure=절차",
    ),
    "scenario": (
        "시나리오 / 가능한 전개 가정",
        "어떤 조건이 이어질 때 사건, 정책, 결과가 어떻게 펼쳐질지 그려본 가능 경로",
        "아직 현실은 아니지만 이렇다면 이렇게 간다는 가정의 줄거리",
        "scenario=가능한 상황 전개 가정 / forecast=미래 예측 / narrative=이야기 서술",
    ),
    "sphere": (
        "영역 / 활동·영향·관심이 미치는 범위",
        "특정한 삶, 제도, 역할, 담론이 작동하는 사회적·개념적 범위",
        "이 안에서는 이 규칙과 영향이 도는 하나의 둥근 구역",
        "sphere=영향이나 활동의 영역 / domain=전문적·개념적 영역 / area=범위 일반",
    ),
    "supplement": (
        "보충하다 / 추가 보완 자료나 양",
        "기존 내용을 대체하기보다 부족한 부분을 채우려고 덧붙이는 것",
        "본체를 갈아엎는 게 아니라 빈칸 옆에 한 장 더 끼워 넣는 느낌",
        "supplement=부족한 부분을 보충하다·보충물 / complement=서로 맞물려 보완하다 / appendix=부록",
    ),
    "team": (
        "팀 / 공동 목표를 위해 함께 일하는 집단",
        "개인이 따로 움직이는 것이 아니라 역할을 나눠 협력하는 작업 단위",
        "각자 한 방향으로 흩어지지 않고 같은 목표를 향해 묶인 사람들",
        "team=공동 목표를 위한 협업 집단 / group=집단 일반 / squad=작은 팀·분대",
    ),
    "temporary": (
        "일시적인 / 오래 지속되지 않는",
        "영구적으로 고정되는 것이 아니라 일정 기간만 유지되거나 임시로 쓰이는",
        "지금 잠깐 세워 둔 구조이고 오래 박아두는 기둥은 아닌 느낌",
        "temporary=잠시만 지속되는 / provisional=임시로 정한 / permanent=영구적인",
    ),
    "trigger": (
        "촉발하다 / 계기·방아쇠",
        "어떤 반응, 사건, 변화가 시작되도록 직접 또는 간접적으로 불을 붙이는 원인이나 장치",
        "잠자던 반응이 이 한 점을 건드리자 바로 시작되는 느낌",
        "trigger=반응·사건을 촉발하다 / cause=원인이 되다 / activate=작동시키다",
    ),
    "unify": (
        "통합하다 / 하나로 묶다",
        "따로 나뉜 요소나 집단을 공통 구조나 목표 아래 연결해 하나의 전체로 만들다",
        "갈라진 조각들 사이 선을 당겨 한 덩어리로 묶는 느낌",
        "unify=나뉜 것을 하나로 통합하다 / merge=합쳐지다 / coordinate=맞춰 움직이게 하다",
    ),
    "violate": (
        "위반하다 / 규칙이나 원칙을 어기다",
        "법, 기준, 합의, 기대된 선을 지키지 않고 넘어서는 행동을 하다",
        "정해진 경계선을 알고도 발이 그 밖으로 넘어가는 느낌",
        "violate=규칙·원칙을 위반하다 / breach=계약·규정을 어기다 / ignore=무시하다",
    ),
    "vision": (
        "비전 / 미래상 / 시각",
        "앞으로 어떤 방향과 모습으로 가야 하는지 그리는 큰 구상이거나 보는 능력",
        "눈앞 장면만이 아니라 머릿속에 먼저 세운 앞으로의 그림",
        "vision=미래 방향을 그린 구상 또는 시각 / goal=도달 목표 / eyesight=시력",
    ),
    "colleague": (
        "동료 / 같은 조직이나 직업에서 함께 일하는 사람",
        "친구 일반보다 업무나 전문 활동을 같은 장 안에서 수행하는 사람",
        "개인적 친분보다 같은 일터 테이블에 앉은 사람",
        "colleague=같은 직장·전문 분야의 동료 / friend=친구 / coworker=같은 일터의 동료",
    ),
    "convince": (
        "납득시키다 / 사실·타당성을 믿게 하다",
        "상대가 어떤 주장이나 설명을 그렇다고 받아들이도록 근거와 설명으로 마음을 돌리다",
        "내 말이 상대 머릿속에서 말이 된다고 고개가 꺾이게 만드는 느낌",
        "convince=근거로 믿고 납득하게 하다 / persuade=행동·태도를 바꾸게 설득하다 / inform=정보를 주다",
    ),
    "depress": (
        "낮추다 / 떨어뜨리다 / 우울하게 하다",
        "가격, 수준, 활동, 기분이 위로 오르지 못하게 아래쪽으로 누르다",
        "위로 뜨려는 것을 무게로 눌러 아래로 가라앉히는 느낌",
        "depress=수준이나 기분을 낮추다 / reduce=양을 줄이다 / discourage=의욕을 꺾다",
    ),
    "encounter": (
        "마주치다 / 예상치 못한 문제나 대상을 만나다",
        "사람, 현상, 어려움, 반응을 계획 밖에서 직접 접하거나 경험하다",
        "길을 가다 앞에서 무언가가 불쑥 나타나 맞닥뜨리는 느낌",
        "encounter=직접 마주치거나 맞닥뜨리다 / face=직면하다 / experience=겪다",
    ),
    "enormous": (
        "막대한 / 매우 큰",
        "크기, 양, 영향, 비용, 차이가 보통 수준을 훨씬 넘을 만큼 큰",
        "보통 크기 상자를 넘어 옆 공간까지 크게 밀고 나오는 느낌",
        "enormous=규모나 정도가 매우 큰 / substantial=상당히 큰 / gigantic=물리적으로 거대한",
    ),
    "forthcoming": (
        "곧 있을 / 기꺼이 정보를 내놓는",
        "가까운 미래에 예정되어 있거나, 질문에 대해 숨기지 않고 비교적 솔직하게 답하는",
        "아직 안 왔지만 곧 앞으로 나오거나, 말을 닫지 않고 앞으로 내미는 느낌",
        "forthcoming=곧 있을 또는 정보를 잘 내놓는 / upcoming=다가오는 / candid=솔직한",
    ),
    "incline": (
        "기울이다 / 마음이 ~쪽으로 기울다 / 경사",
        "물리적으로 한쪽으로 비스듬히 기울거나, 판단과 선호가 특정 방향으로 조금 쏠리다",
        "평평한 바닥이 아니라 한쪽으로 살짝 내려가는 선을 타는 느낌",
        "incline=기울다·~쪽으로 마음이 가다 / slope=경사면 / tend=~하는 경향이 있다",
    ),
    "identify": (
        "식별하다 / 누구·무엇인지 알아내다",
        "특징, 이름, 증거를 근거로 대상을 구별하거나 특정 원인·패턴을 찾아내다",
        "흐릿한 덩어리에서 이게 무엇인지 이름표와 윤곽을 붙이는 느낌",
        "identify=대상·원인·패턴을 식별하다 / recognize=보고 알아보다 / define=의미를 규정하다",
    ),
    "major": (
        "주요한 / 더 큰 비중을 차지하는",
        "여러 요소 중 영향, 규모, 중요도에서 상대적으로 중심적이고 큰 쪽의",
        "주변 조각보다 화면 가운데를 크게 차지하는 핵심 덩어리",
        "major=중요도·규모가 큰 주요한 / main=중심이 되는 / minor=작은·덜 중요한",
    ),
    "structure": (
        "구조 / 부분들이 짜여 있는 방식",
        "개별 요소 자체보다 그것들이 어떤 관계와 배열로 연결되어 전체를 이루는가",
        "흩어진 조각 뒤에 그 조각들을 세우는 뼈대와 배치",
        "structure=전체를 이루는 짜임과 구조 / organization=조직화 방식 / component=개별 부분",
    ),
    "chapter": (
        "장 / 책이나 긴 글을 나눈 한 단위",
        "하나의 긴 텍스트나 역사적 흐름을 주제나 시점에 따라 구분한 구획",
        "긴 이야기를 한 번에 다 보지 않게 중간 문패로 나눠 놓은 칸",
        "chapter=책·역사 흐름의 한 구획 / section=일반적인 구분 단위 / episode=사건 중심의 한 부분",
    ),
    "criteria": (
        "기준들 / 판단·평가에 쓰는 복수의 잣대",
        "어떤 선택이나 평가가 타당한지 보기 위해 적용하는 여러 조건과 판단 항목",
        "마음대로 고르지 않고 여러 눈금을 나란히 놓고 재는 느낌",
        "criteria=판단에 쓰는 복수 기준 / criterion=단일 기준 / standard=표준·기준",
    ),
    "deduce": (
        "추론해내다 / 주어진 사실에서 결론을 이끌다",
        "직접 보지 않은 결론을 이미 있는 정보와 논리 관계를 따라 도출하다",
        "조각 증거들을 따라가다 보니 마지막 답이 논리적으로 끌려 나오는 느낌",
        "deduce=주어진 전제로 논리적 결론을 이끌다 / infer=근거로 추론하다 / guess=짐작하다",
    ),
    "licence": (
        "면허 / 허가",
        "특정 행위나 영업, 사용을 공식적으로 할 수 있도록 부여된 승인이나 자격",
        "하고 싶다고 바로 되는 게 아니라 공식 문이 열렸다는 허가증 느낌",
        "licence=공식 허가·면허 / permit=허가증 / freedom=자유",
    ),
    "motive": (
        "동기 / 그렇게 행동하게 만든 이유",
        "겉으로 보이는 행동 뒤에서 왜 그 선택을 했는지 설명하는 내적·사회적 이유",
        "행동의 겉모양보다 뒤에서 밀고 있는 이유의 엔진",
        "motive=행동을 일으킨 이유·동기 / motivation=동기부여 상태나 힘 / cause=원인 일반",
    ),
    "utilise": (
        "활용하다 / 실제 목적에 맞게 써먹다",
        "자원, 자료, 방법, 기회를 그냥 보유하는 데서 끝내지 않고 일에 투입해 효과를 내다",
        "갖고만 있는 도구를 작업대 위에 올려 실제로 돌리는 느낌",
        "utilise=자원·방법을 활용하다 / use=쓰다 일반 / apply=특정 목적에 적용하다",
    ),
    "globe": (
        "지구 / 세계 / 구형체",
        "물리적 구 모양이거나, 넓게는 전 세계 범위를 가리키는 표현",
        "한 지역이 아니라 둥근 지구 전체를 한 덩어리로 잡는 느낌",
        "globe=지구 또는 전 세계 / earth=지구 / sphere=구형체·영역",
    ),
    "identical": (
        "동일한 / 구분할 차이가 없는",
        "둘 이상의 대상이 형태, 값, 내용, 특성이 사실상 똑같아 차이를 가르기 어려운",
        "옆에 나란히 놔도 다른 선이 거의 안 보이는 느낌",
        "identical=사실상 완전히 같은 / similar=비슷한 / equivalent=기능·값이 동등한",
    ),
    "ultimate": (
        "궁극적인 / 최종의 / 가장 근본적인",
        "순서상 마지막이거나, 여러 층을 거슬러 올라가 가장 깊은 목표·원인·결론에 해당하는",
        "중간 단계를 다 지나 마지막 바닥이나 꼭대기에 닿는 느낌",
        "ultimate=최종적이거나 가장 근본적인 / final=마지막의 / fundamental=근본적인",
    ),
    "abandon": (
        "버리다 / 포기하다 / 중단하다",
        "계획, 소유, 시도, 책임을 더 이상 붙잡지 않고 손에서 놓아버리다",
        "끝까지 끌고 가지 않고 잡고 있던 줄을 손에서 툭 놓는 느낌",
        "abandon=완전히 포기하거나 버리다 / quit=그만두다 / neglect=돌보지 않고 방치하다",
    ),
    "crucial": (
        "결정적으로 중요한",
        "결과나 판단이 갈리는 데 핵심 역할을 해서 빠지면 전체 의미가 크게 흔들리는",
        "있으면 좋은 정도가 아니라 이 조각이 없으면 판이 안 서는 느낌",
        "crucial=결정적으로 중요한 / important=중요한 / relevant=관련 있는",
    ),
}


AWKWARD_REPLACEMENTS = [
    ("쪽으로 처리하는 느낌", "방향으로 읽는 느낌"),
    ("이라는 핵심 개념을 잡는 느낌", "이라는 중심 뜻을 잡는 느낌"),
    ("하십시오", "하다"),
    ("됩니다", "된다"),
    ("됩니다.", "된다."),
    ("습니다", "다"),
    ("입니다", "이다"),
    ("브릿지", "브리지"),
]

LEGACY_ETS_DISTINCTION_RE = re.compile(
    r"^(명사|동사|형용사|부사|명사/동사|동사/형용사|명사/형용사)\s*\(.+\)$"
)


def parse_back(back: str) -> tuple[str, str, str, str]:
    lines = back.split("\n")
    if len(lines) != 4:
        raise ValueError(f"expected 4 back lines, got {len(lines)}")
    values = []
    for line, label in zip(lines, ["핵심 뜻: ", "부가 뜻: ", "핵심 느낌: ", "구분: "]):
        if not line.startswith(label):
            raise ValueError(f"invalid label order: {line!r}")
        values.append(line.removeprefix(label))
    return tuple(values)  # type: ignore[return-value]


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join(
        [
            f"핵심 뜻: {core}",
            f"부가 뜻: {extra}",
            f"핵심 느낌: {feeling}",
            f"구분: {distinction}",
        ]
    )


def clean_text(text: str) -> str:
    cleaned = text.strip().replace("\u00a0", " ")
    for old, new in AWKWARD_REPLACEMENTS:
        cleaned = cleaned.replace(old, new)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.rstrip(";")
    cleaned = cleaned.replace("다다", "다")
    return cleaned


def polish_awl_row(headword: str, back: str) -> str:
    if headword in AWL_OVERRIDES:
        return build_back(*AWL_OVERRIDES[headword])

    core, extra, feeling, distinction = parse_back(back)
    core = clean_text(core)
    extra = clean_text(extra)
    feeling = clean_text(feeling)
    feeling = feeling.replace("학술 문맥에서 ", "")
    feeling = feeling.replace(f"{core}이라는 중심 뜻을 잡는 느낌", f"{core} 쪽으로 빠르게 잡는 느낌")
    feeling = feeling.replace(f"{core} 방향으로 읽는 느낌", f"{core} 쪽으로 빠르게 잡는 느낌")

    distinction = clean_text(distinction)
    if "=유사어" in distinction:
        parts = [part.strip() for part in distinction.split("/") if part.strip()]
        rewritten = []
        for idx, part in enumerate(parts):
            if "=" not in part:
                continue
            label, value = [piece.strip() for piece in part.split("=", 1)]
            if idx == 0:
                rewritten.append(f"{label}={core}")
            elif value == "유사어":
                rewritten.append(f"{label}=뜻이 가까우므로 문맥으로 구분")
            else:
                rewritten.append(f"{label}={value}")
        if rewritten:
            distinction = " / ".join(rewritten)

    return build_back(core, extra, feeling, distinction)


def polish_ets_row(headword: str, back: str) -> str:
    core, extra, feeling, distinction = parse_back(back)
    if LEGACY_ETS_DISTINCTION_RE.match(distinction.strip()):
        core_short = core.split("/")[0].strip()
        distinction = (
            f"{headword}={core_short} / 관련 어휘와는 의미 범위·강조점·쓰임으로 구분"
        )
    return build_back(core, extra, feeling, distinction)


def read_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return [row for row in csv.reader(f, delimiter="\t") if row]


def write_rows(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)


def append_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    if not rows:
        return
    existing = path.exists() and path.read_text(encoding="utf-8").strip()
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        if not existing:
            writer.writerow(header)
        writer.writerows(rows)


def refresh_inventory() -> tuple[int, int]:
    ets_words = []
    awl_words = []
    for path in sorted(ROOT.glob(ETS_PATTERN)):
        for row in read_rows(path):
            ets_words.append(row[0].strip())
    for path in sorted(ROOT.glob(AWL_PATTERN)):
        for row in read_rows(path):
            awl_words.append(row[0].strip())

    (ROOT / ".existing_words.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_ets_headwords.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_awl_headwords.txt").write_text("\n".join(awl_words) + "\n", encoding="utf-8")
    (ROOT / "all_headwords.txt").write_text(
        "\n".join(sorted(set(ets_words + awl_words))) + "\n",
        encoding="utf-8",
    )
    return len(ets_words), len(awl_words)


def update_metadata(ets_count: int, awl_count: int) -> None:
    manifest_path = ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["total_ets_cards"] = ets_count
    manifest["total_awl_cards"] = awl_count
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    notes_path = ROOT / "generation_notes.md"
    notes_text = notes_path.read_text(encoding="utf-8")
    notes_text = re.sub(
        r"- ETS sets `01` to `22` exist, bringing the ETS-based total to \d+ cards\n",
        f"- ETS sets `01` to `22` exist, bringing the ETS-based total to {ets_count} cards after specialist-term pruning\n",
        notes_text,
    )
    notes_text = re.sub(
        r"- AWL sets `01` to `06` exist, covering \d+ AWL headwords\n",
        f"- AWL sets `01` to `06` exist, covering {awl_count} AWL headwords after ETS-overlap removal\n",
        notes_text,
    )
    notes_text = notes_text.replace(
        "- AWL generation is structurally complete but semantic polishing remains necessary for machine-translated glosses\n",
        "- AWL generation is structurally complete and a first-pass Korean meaning polish has been applied, but manual spot review is still recommended\n",
    )
    notes_path.write_text(notes_text, encoding="utf-8")

    plan_path = ROOT / "WORK_PLAN.md"
    plan_text = plan_path.read_text(encoding="utf-8")
    plan_text = re.sub(
        r"- Current ETS row count after the latest expansion pass: \d+\n",
        f"- Current ETS row count after pruning and dedupe cleanup: {ets_count}\n",
        plan_text,
    )
    plan_text = re.sub(
        r"- AWL files generated: .*?\n",
        f"- AWL files generated: `toefl_awl_set_01.tsv` to `toefl_awl_set_06.tsv` ({awl_count} cards after ETS-overlap removal)\n",
        plan_text,
    )
    plan_path.write_text(plan_text, encoding="utf-8")


def main() -> None:
    ets_locations: dict[str, list[str]] = defaultdict(list)
    awl_locations: dict[str, list[str]] = defaultdict(list)
    awl_removed_log: list[list[str]] = []
    ets_rejected_log: list[list[str]] = []

    for path in sorted(ROOT.glob(ETS_PATTERN)):
        original_rows = read_rows(path)
        kept_rows = []
        for row_index, (headword, back) in enumerate(original_rows, 1):
            word = headword.strip()
            ets_locations[word].append(f"{path.name}:{row_index}")
            if word in SPECIALIZED_ETS_DROP:
                ets_rejected_log.append(
                    [word, SPECIALIZED_ETS_DROP[word], "", "high"]
                )
                continue
            kept_rows.append([word, polish_ets_row(word, back)])
        if kept_rows != original_rows:
            write_rows(path, kept_rows)

    for path in sorted(ROOT.glob(AWL_PATTERN)):
        original_rows = read_rows(path)
        kept_rows = []
        for row_index, (headword, back) in enumerate(original_rows, 1):
            word = headword.strip()
            awl_locations[word].append(f"{path.name}:{row_index}")
            if word in ets_locations:
                awl_removed_log.append(
                    [
                        f"{path.name}:{row_index}",
                        word,
                        f"removed AWL duplicate already covered in ETS ({', '.join(ets_locations[word])})",
                    ]
                )
                continue
            kept_rows.append([word, polish_awl_row(word, back)])
        if kept_rows != original_rows:
            write_rows(path, kept_rows)

    append_tsv(
        ROOT / "duplicates_removed.tsv",
        ["removed_from", "replaced_with", "reason"],
        awl_removed_log,
    )
    append_tsv(
        ROOT / "rejected_candidates.tsv",
        ["candidate", "reason_for_rejection", "near_duplicate_of", "confidence"],
        ets_rejected_log,
    )

    ets_count, awl_count = refresh_inventory()
    update_metadata(ets_count, awl_count)

    print(f"ETS cards: {ets_count}")
    print(f"AWL cards: {awl_count}")
    print(f"Removed AWL duplicates: {len(awl_removed_log)}")
    print(f"Removed ETS specialist terms: {len(ets_rejected_log)}")


if __name__ == "__main__":
    main()
