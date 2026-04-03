from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REPLACEMENTS: dict[str, dict[str, tuple[str, str, str, str, str]]] = {
    "toefl_ets_2026_set_07.tsv": {
        "diagnosis": ("baseline", "기준선 / 초기 기준", "변화나 효과를 비교하기 위해 먼저 잡는 출발 기준", "나중 상태를 재기 전에 바닥 기준선을 하나 그어두는 느낌", "baseline=비교의 출발 기준선 / benchmark=성능 비교 기준 / standard=일반 기준"),
        "symptom": ("bottleneck", "병목 / 진행을 막는 좁은 지점", "전체 흐름에서 처리나 이동을 느리게 만드는 제한 지점", "넓던 흐름이 한 지점에서 좁아져 막히는 느낌", "bottleneck=흐름을 느리게 하는 병목 지점 / constraint=제약 조건 / obstacle=진행을 막는 장애물"),
        "inflammation": ("regularity", "규칙성 / 일정하게 반복됨", "상황이나 값이 비교적 예측 가능한 패턴을 보임", "들쭉날쭉하지 않고 일정한 결이 반복되는 느낌", "regularity=규칙적인 반복성 / consistency=일관성 / stability=흔들림이 적음"),
        "prognosis": ("projection", "예측 / 전망", "현재 추세를 바탕으로 앞으로를 추정한 결과", "지금 선을 앞으로 쭉 밀어 미래를 그려보는 느낌", "projection=추세 기반 전망 / prediction=예측 일반 / estimate=대략적 추산"),
        "remission": ("attenuation", "약화 / 강도 감소", "영향이나 강도가 줄어듦", "세게 들어오던 힘이 점점 옅어지는 느낌", "attenuation=강도가 약해짐 / decline=점점 떨어짐 / mitigation=나쁜 영향을 완화함"),
        "relapse": ("setback", "차질 / 후퇴", "잘 가던 진행이 일시적으로 뒤로 밀리거나 악화됨", "앞으로 가다 발이 걸려 한 번 뒤로 꺾이는 느낌", "setback=진행상의 후퇴·차질 / failure=완전한 실패 / delay=시간이 늦어짐"),
        "transplant": ("transferability", "전이 가능성 / 다른 상황에 적용 가능함", "한 맥락에서 얻은 방식이나 결과가 다른 맥락에서도 쓰일 수 있음", "여기서 배운 걸 저기로 옮겨도 통하는지 보는 느낌", "transferability=다른 맥락으로 옮겨 적용 가능함 / adaptability=상황에 맞게 조정 가능함 / applicability=그 경우에 적용됨"),
        "therapeutic": ("advantageous", "유리한 / 이점이 있는", "결과를 더 나은 쪽으로 밀어주는 조건이나 성질의", "같은 조건이면 이쪽이 더 득이 되는 방향으로 기우는 느낌", "advantageous=유리하게 작용하는 / beneficial=도움이 되는 / favorable=좋은 결과에 유리한"),
        "placebo": ("counterpart", "대응되는 것 / 짝이 되는 대상", "비교나 대응 관계에서 한쪽에 맞서는 짝", "혼자 보는 게 아니라 맞은편 짝과 나란히 놓이는 느낌", "counterpart=역할이나 위치가 대응되는 짝 / equivalent=가치·기능이 같은 것 / contrast=대조되는 차이"),
        "dosage": ("apportionment", "분배 / 몫을 나눔", "한정된 자원이나 부담을 여러 쪽에 나누어 배정함", "전체를 여러 몫으로 잘라 각자에게 나눠 주는 느낌", "apportionment=몫을 나눠 배정함 / allocation=자원·시간을 배분함 / distribution=퍼져 나뉜 양상"),
        "antibiotic": ("preventive", "예방적인 / 미리 막는", "문제가 커지기 전에 막으려는", "터진 뒤 수습보다 미리 앞에서 막는 느낌", "preventive=사전에 막는 / protective=피해를 막아 보호하는 / corrective=이미 생긴 문제를 고치는"),
        "toxin": ("hazard", "위해 요인 / 위험 요소", "해를 일으킬 가능성이 있는 요소", "가만히 두면 문제를 낼 수 있는 위험 씨앗", "hazard=잠재적 위험 요인 / risk=나쁜 결과가 날 가능성 / threat=구체적으로 위협하는 대상"),
        "virulent": ("intensified", "강화된 / 더 강해진", "정도나 영향력이 더 세진", "힘의 눈금이 한 단계 올라간 느낌", "intensified=강도가 세진 / severe=상태가 심각한 / amplified=크기나 영향이 증폭된"),
        "endemic": ("recurring", "반복해서 나타나는", "한 번으로 끝나지 않고 다시 생기는", "사라진 듯해도 주기적으로 다시 올라오는 느낌", "recurring=되풀이해 나타나는 / persistent=계속 남는 / occasional=가끔 나타나는"),
        "mutation": ("modification", "수정 / 일부 변경", "원래 형태를 유지하면서 필요한 부분을 바꿈", "뼈대는 두고 일부만 손보는 느낌", "modification=부분 변경 / alteration=변형·변경 / revision=내용을 다시 고쳐 씀"),
        "hereditary": ("inherited", "물려받은 / 이전부터 이어진", "앞선 세대나 이전 상태에서 넘어온", "새로 생긴 게 아니라 전부터 내려온 것을 안고 있는 느낌", "inherited=이전으로부터 물려받은 / innate=타고난 / acquired=나중에 얻은"),
        "protein": ("component", "구성 요소 / 부분", "전체를 이루는 한 단위", "큰 구조 안에 끼워진 한 조각", "component=전체를 이루는 요소 / element=요소 일반 / ingredient=재료 성분"),
        "enzyme": ("driver", "추진 요인 / 변화를 밀어주는 것", "어떤 과정이 실제로 움직이게 만드는 핵심 요인", "뒤에서 가만히 있지 않고 변화를 앞으로 미는 힘", "driver=변화를 움직이는 핵심 요인 / factor=영향 요인 / catalyst=변화를 촉진하는 계기"),
        "homeostasis": ("constancy", "불변성 / 비교적 일정함", "시간이 지나도 값이나 상태가 크게 달라지지 않는 성질", "흔들리기보다 일정한 선을 계속 지키는 느낌", "constancy=비교적 변하지 않는 성질 / stability=안정성 / uniformity=고르게 같음"),
        "syndrome": ("profile", "특성 묶음 / 윤곽", "대상이나 집단을 설명하는 대표적 특징들의 조합", "하나의 점이 아니라 여러 특징이 모여 만든 얼굴 윤곽", "profile=특징을 묶어 보여주는 윤곽 / pattern=반복 양상 / description=설명"),
        "pathway": ("progression", "진행 / 단계적 전개", "앞 단계에서 다음 단계로 이어지며 나아감", "처음 상태가 다음 단계로 차례차례 넘어가는 느낌", "progression=단계적으로 진행됨 / sequence=정해진 순서 / process=과정 전체"),
        "eradicate": ("eliminate", "없애다 / 제거하다", "불필요하거나 해로운 것을 남기지 않고 치우다", "문제 요소를 목록에서 완전히 빼내는 느낌", "eliminate=없애다·배제하다 / reduce=줄이다 / remove=물리적으로 치우다"),
    },
    "toefl_ets_2026_set_08.tsv": {
        "pedagogy": ("procedure", "절차 / 정해진 진행 방식", "일을 어떤 순서와 방식으로 처리하는지의 단계적 틀", "마음대로가 아니라 순서를 밟아 따라가는 길", "procedure=정해진 절차 / method=방법 하나 / protocol=공식 절차 규약"),
        "formative": ("stepwise", "단계적인 / 한 단계씩 진행되는", "한 번에 확 바뀌지 않고 순서대로 나아가는", "계단을 한 칸씩 밟듯 진행되는 느낌", "stepwise=단계별로 진행되는 / gradual=서서히 진행되는 / abrupt=갑작스러운"),
        "summative": ("holistic", "전체론적인 / 종합적으로 보는", "부분 하나보다 전체 맥락과 연결을 함께 보는", "조각만 떼지 않고 큰 그림을 한꺼번에 보는 느낌", "holistic=전체를 함께 보는 / comprehensive=폭넓게 아우르는 / partial=부분적인"),
        "self-efficacy": ("self-assurance", "자신감 / 스스로에 대한 확신", "자신이 해낼 수 있다고 느끼는 안정된 확신", "내가 할 수 있다는 쪽으로 중심이 단단히 서는 느낌", "self-assurance=스스로에 대한 확신 / confidence=자신감 일반 / self-esteem=자기 가치감"),
        "spacing": ("lag", "지연 간격 / 시간차", "한 사건이나 반응이 바로 이어지지 않고 생기는 시간 차이", "앞선 일 뒤에 바로 안 오고 살짝 늦게 따라오는 틈", "lag=뒤따르는 시간차·지연 / delay=늦어짐 / interval=사이 간격"),
    },
    "toefl_ets_2026_set_09.tsv": {
        "solar": ("systematic", "체계적인", "규칙과 구조를 따라 조직적으로 이루어지는", "마구잡이가 아니라 정해진 틀 안에서 움직이는 느낌", "systematic=절차와 구조를 갖춘 / organized=잘 정돈된 / random=무작위의"),
        "inertia": ("carryover", "이월 효과 / 다음까지 이어지는 영향", "앞 단계의 상태나 효과가 다음 단계에도 남아 이어짐", "앞에서 생긴 영향이 뒤까지 같이 묻어 넘어가는 느낌", "carryover=다음 단계로 이어진 잔여 영향 / continuity=끊기지 않고 이어짐 / residue=남은 잔여물"),
        "velocity": ("pace", "속도 / 진행 페이스", "어떤 일이 진행되는 빠르기", "너무 느리거나 빠르지 않게 흘러가는 리듬의 빠르기", "pace=진행 속도 / rate=비율화된 변화 속도 / speed=빠르기 일반"),
        "wavelength": ("timescale", "시간 척도 / 진행되는 시간 범위", "현상이나 변화가 어느 정도 시간 폭에서 일어나는지 보는 기준", "짧은 순간인지 긴 기간인지 시간자를 대 보는 느낌", "timescale=현상을 보는 시간 범위 / duration=지속 시간 / timeline=일정의 시간 배열"),
        "radiation": ("distribution", "분포 / 퍼져 있는 양상", "값이나 대상이 여러 위치·집단에 나뉘어 퍼진 모습", "한 점에 몰리지 않고 어디에 얼마나 놓였는지 펼쳐 보는 느낌", "distribution=퍼져 있는 배치 양상 / spread=퍼짐 / allocation=몫을 나누어 배정함"),
        "glacier": ("breakpoint", "분기점 / 변화가 갈리는 지점", "이 지점을 기준으로 상태나 경향이 달라지는 경계", "여기서부터 흐름이 다른 쪽으로 꺾이는 갈림점", "breakpoint=상태가 갈리는 기준 지점 / threshold=변화가 시작되는 문턱 / turning point=흐름의 전환점"),
        "salinity": ("variability", "변동성 / 달라지는 정도", "상황이나 값이 일정하지 않고 바뀌는 성질", "고정된 한 값이 아니라 계속 흔들리는 폭을 보는 느낌", "variability=값이 변하는 정도 / variance=통계적 분산 / instability=안정되지 않음"),
        "tectonic": ("structural", "구조적인 / 짜임과 관련된", "표면 현상보다 아래 틀과 배열 방식에 관련된", "겉모습보다 뼈대를 이루는 구조 쪽을 보는 느낌", "structural=구조와 관련된 / systemic=시스템 전체에 걸친 / superficial=겉면의"),
        "seismic": ("abrupt", "갑작스러운 / 급격한", "서서히가 아니라 짧은 순간에 확 바뀌는", "완만한 변화가 아니라 툭 끊기며 급히 튀는 느낌", "abrupt=갑작스럽고 툭 끊기는 / gradual=서서히 진행되는 / sudden=갑작스러운"),
        "crystalline": ("legible", "읽어낼 수 있는 / 알아보기 쉬운", "정보나 구조가 해석 가능할 만큼 분명히 드러나는", "복잡해도 눈으로 따라가며 뜻을 읽을 수 있는 느낌", "legible=읽고 파악하기 쉬운 / clear=명확한 / obscure=잘 안 드러나는"),
        "lava": ("outflow", "유출 / 밖으로 흘러나감", "안에 있던 자원·정보·사람이 바깥으로 빠져나가는 흐름", "안쪽에 머물던 것이 밖으로 흘러 나가는 느낌", "outflow=밖으로 나가는 흐름 / inflow=안으로 들어오는 흐름 / discharge=방출"),
        "volcanic": ("fluctuating", "변동하는 / 오르내리는", "값이나 상태가 고정되지 않고 계속 바뀌는", "가만히 한 줄로 가지 않고 위아래로 출렁이는 느낌", "fluctuating=계속 오르내리며 변하는 / volatile=급변하기 쉬운 / stable=안정적인"),
        "acidic": ("unfavorable", "불리한 / 좋지 않은", "원하는 결과가 나오기 어려운 방향으로 작용하는", "조건이 내 편이 아니라 반대쪽으로 기울어진 느낌", "unfavorable=좋은 결과에 불리한 / adverse=부정적 영향을 주는 / favorable=유리한"),
        "alkaline": ("favorable", "유리한 / 긍정적인", "원하는 결과가 나오기 좋은 쪽으로 작용하는", "조건이 내 쪽으로 살짝 밀어주는 느낌", "favorable=유리한 조건의 / beneficial=도움이 되는 / positive=긍정적인"),
        "oxidize": ("degrade", "저하되다 / 품질이 떨어지다", "시간이나 조건 때문에 성능·상태가 나빠지다", "처음보다 점점 닳고 떨어져 가는 느낌", "degrade=질이 떨어지다 / deteriorate=점점 나빠지다 / weaken=약해지다"),
        "radioactive": ("unstable", "불안정한 / 쉽게 바뀌는", "상태가 고정되지 않아 변화나 흔들림이 큰", "단단히 고정되지 않고 언제든 흔들리는 느낌", "unstable=상태가 불안정한 / volatile=급변하기 쉬운 / steady=안정적인"),
        "thermal": ("adjustable", "조정 가능한 / 바꿀 수 있는", "필요에 따라 수준이나 조건을 바꿀 수 있는", "고정값이 아니라 손잡이를 돌려 맞출 수 있는 느낌", "adjustable=조건이나 수준을 바꿀 수 있는 / flexible=상황에 맞게 조정 가능한 / fixed=고정된"),
    },
    "toefl_ets_2026_set_11.tsv": {
        "arable": ("tractable", "다루기 쉬운 / 해결 가능한", "문제가 너무 복잡하지 않아 분석이나 처리가 가능한", "손에 잡히지 않던 문제가 풀 수 있는 크기로 들어오는 느낌", "tractable=다룰 수 있을 만큼 해결 가능한 / manageable=감당 가능한 / intractable=다루기 어려운"),
        "biodiversity": ("variety", "다양성 / 여러 종류가 있음", "서로 다른 종류나 방식이 함께 존재함", "하나로만 채워지지 않고 여러 갈래가 섞인 느낌", "variety=종류가 다양함 / diversity=구성의 다양성 / uniformity=획일성"),
        "biodegradable": ("recoverable", "회복 가능한 / 다시 찾아올 수 있는", "손상이나 손실 후에도 다시 돌려놓을 여지가 있는", "완전히 끝난 게 아니라 다시 끌어올릴 수 있는 느낌", "recoverable=다시 회복·회수 가능한 / renewable=다시 보충 가능한 / irreversible=되돌릴 수 없는"),
        "canopy": ("coverage", "포괄 범위 / 적용 범위", "어디까지 포함하거나 덮고 있는지의 범위", "무엇을 얼마나 넓게 덮고 있는지 보는 느낌", "coverage=포함·적용 범위 / scope=다루는 범위 / extent=퍼진 정도"),
        "compost": ("byproduct", "부산물 / 부수적으로 생긴 결과", "주된 목적이 아닌데 과정에서 함께 생긴 산물", "원래 목표 옆에서 덤처럼 딸려 나온 결과물", "byproduct=과정에서 부수적으로 생긴 것 / outcome=나온 결과 / residue=남은 찌꺼기"),
        "drought": ("shortage", "부족 / 결핍", "필요한 양이 충분하지 않은 상태", "채워져야 할 몫이 모자라 비는 느낌", "shortage=필요한 양이 부족함 / deficit=수치상 부족분 / scarcity=자체가 희소함"),
        "ecosystem": ("interconnection", "상호 연결 / 서로 이어짐", "여러 요소가 따로가 아니라 영향을 주고받으며 연결된 상태", "각 점이 선으로 엮여 서로 당기고 미는 느낌", "interconnection=서로 이어진 연결 관계 / network=연결망 / interaction=서로 영향을 주고받음"),
        "encroachment": ("intrusion", "침범 / 끼어듦", "원래 구역이나 흐름 안으로 바깥 요소가 밀고 들어옴", "경계를 넘어 안쪽 공간을 슬금슬금 파고드는 느낌", "intrusion=원치 않는 침범·개입 / expansion=범위 확대 / interference=진행을 방해하는 간섭"),
        "evaporate": ("diminish", "줄어들다 / 약해지다", "양·영향·강도가 점점 작아지다", "눈에 띄던 힘이나 양이 서서히 빠지는 느낌", "diminish=점점 줄어들다 / disappear=사라지다 / decline=감소세를 보이다"),
        "pesticide": ("countermeasure", "대응책 / 대응 수단", "문제나 위험을 줄이기 위해 취하는 조치", "그냥 두지 않고 맞받아치는 조치 카드", "countermeasure=문제에 맞선 대응책 / solution=해결책 / prevention=사전 예방"),
        "photosynthetic": ("foundational", "기초가 되는 / 토대의", "다른 과정이나 논의가 올라설 바탕을 제공하는", "위 구조를 받치는 맨 아래 받침돌 같은 느낌", "foundational=바탕을 이루는 / basic=기초적인 / preliminary=예비 단계의"),
        "pollinator": ("stakeholder", "이해관계자 / 관련 당사자", "결정이나 변화의 영향을 받거나 관여하는 사람·집단", "밖에서 구경하는 쪽이 아니라 그 일에 직접 걸려 있는 쪽", "stakeholder=영향을 주고받는 관련 당사자 / participant=참가자 / observer=관찰자"),
        "runoff": ("spillover", "파급 효과 / 넘쳐 퍼진 영향", "원래 범위를 넘어 주변으로 번져 나가는 영향", "한 곳의 변화가 가장자리를 넘어 옆으로 흘러넘치는 느낌", "spillover=주변으로 퍼진 파급 효과 / outcome=결과 자체 / externality=제3자에게 미치는 부수 영향"),
        "smog": ("visibility", "가시성 / 눈에 잘 보임", "대상이 얼마나 잘 드러나고 알아볼 수 있는지의 정도", "흐려 숨는 게 아니라 시야 안으로 분명히 들어오는 정도", "visibility=겉으로 드러나 보이는 정도 / exposure=영향에 노출됨 / clarity=명확성"),
        "microbe": ("agent", "작용 주체 / 행위자", "변화나 결과를 일으키는 역할을 하는 사람·요소", "가만히 있는 배경이 아니라 뭔가를 실제로 움직이는 주체", "agent=작용을 일으키는 주체 / factor=영향 요인 / actor=행위자"),
        "percolate": ("propagate", "전파되다 / 퍼져 나가게 하다", "정보·변화·영향이 한 지점에서 다른 곳으로 퍼져 이어지다", "한 번 생긴 신호가 옆으로 계속 번져 가는 느낌", "propagate=신호·정보·영향이 퍼져 나가다 / diffuse=넓게 확산되다 / transmit=전달하다"),
        "stormwater": ("drainage", "배수 / 물을 빼내는 체계", "고인 물이나 과잉 유입을 밖으로 빼내는 흐름·시설", "넘친 것을 한쪽 길로 빼서 정리하는 느낌", "drainage=물을 빼내는 체계 / irrigation=물을 대는 체계 / channel=흐름을 보내는 통로"),
        "nonrenewable": ("finite", "유한한 / 한정된", "무한히 계속되지 않고 쓸 수 있는 양이나 기간에 끝이 있는", "계속 꺼내 쓸 수 없고 끝선이 정해진 느낌", "finite=양이나 범위에 끝이 있음 / limited=제한된 / renewable=다시 보충 가능한"),
        "wildfire": ("disruption", "교란 / 큰 혼란", "정상적 흐름이나 체계를 갑자기 흔들어 깨는 일", "잘 돌아가던 판을 확 흐트러뜨리는 충격", "disruption=흐름을 깨는 교란 / disturbance=방해·혼란 일반 / breakdown=작동이 무너짐"),
    },
    "toefl_ets_2026_set_13.tsv": {
        "colloquium": ("discussion-based", "토론 중심의", "일방향 전달보다 참여자 간 의견 교환이 중심이 되는", "혼자 설명하는 게 아니라 주고받으며 생각을 여는 느낌", "discussion-based=토론 참여가 중심인 / lecture-based=강의 전달 중심의 / interactive=상호작용이 있는"),
        "plenary": ("groupwide", "전체 집단 대상의", "일부 소그룹이 아니라 구성원 전체가 함께하는", "작은 분과가 아니라 모두를 한꺼번에 묶는 느낌", "groupwide=전체 집단에 걸친 / partial=일부만의 / collective=집단 전체의"),
        "quorum": ("floor", "하한선 / 최저 기준", "이 아래로 내려가면 조건을 충족하지 못하는 기준 수준", "더 내려가면 안 되는 바닥선을 하나 긋는 느낌", "floor=최저 기준선 / threshold=성립 경계선 / minimum=가장 작은 허용치"),
        "invigilation": ("monitoring", "모니터링 / 지속적 점검", "상황이나 진행을 계속 살펴 이상을 확인하는 일", "눈을 떼지 않고 흐름을 따라가며 확인하는 느낌", "monitoring=계속 지켜보며 점검함 / supervision=위에서 관리·감독함 / review=나중에 다시 검토함"),
        "proctor": ("overseer", "감독 담당자 / 총괄 감시자", "일이나 절차가 기준대로 진행되는지 살피는 사람", "세부를 놓치지 않게 위에서 전체 흐름을 지켜보는 역할", "overseer=진행을 위에서 감독하는 사람 / supervisor=지도·감독 책임자 / monitor=상황을 지켜보는 사람"),
    },
    "toefl_ets_2026_set_14.tsv": {
        "antiquity": ("continuum", "연속선 / 이어진 범위", "서로 분리된 조각이 아니라 한 흐름으로 이어진 범위", "뚝 끊긴 점들이 아니라 하나의 선으로 이어진 느낌", "continuum=연속적으로 이어진 범위 / sequence=순서 / spectrum=폭넓은 연속 분포"),
        "artifact": ("trace", "흔적 / 남은 자취", "직접 보이지 않는 과거나 원인을 짐작하게 해 주는 남은 표시", "사라진 것의 발자국만 남아 있는 느낌", "trace=남은 흔적 / evidence=근거 자료 / remnant=남은 일부"),
        "clan": ("community", "공동체 / 집단", "사람들이 관계와 소속감을 공유하며 함께 묶인 집단", "따로 흩어진 개인이 아니라 같이 속한 무리", "community=소속과 관계가 있는 집단 / population=전체 인구 집단 / network=연결망"),
        "conquest": ("dominance", "우위 / 지배적 영향력", "다른 대상보다 더 강하게 위에 서거나 영향을 행사함", "힘이나 존재감이 위쪽에서 눌러 앞서는 느낌", "dominance=지배적 우위 / control=직접 통제 / superiority=더 뛰어나거나 위에 있음"),
        "dynasty": ("regime", "체제 / 통치 방식", "권력과 규칙이 한 사회를 운영하는 방식이나 그 지배 질서", "누가 어떤 규칙으로 판을 움직이는지 정해진 권력 틀", "regime=권력이 작동하는 통치 체제 / government=정부 조직 / administration=행정 운영"),
        "mythology": ("symbolism", "상징성 / 상징 체계", "겉으로 보이는 것 너머에 담긴 의미와 표지 체계", "이미지나 이야기 뒤에 숨은 뜻을 읽는 느낌", "symbolism=상징을 통한 의미 표현 / imagery=이미지 표현 / interpretation=해석"),
        "nomadic": ("mobile", "이동성 있는 / 옮겨 다니는", "한곳에 고정되지 않고 위치나 상태를 바꿀 수 있는", "붙박이보다 필요에 따라 움직일 수 있는 느낌", "mobile=움직이며 옮길 수 있는 / flexible=조정 가능한 / sedentary=정착형의"),
        "peasant": ("laborer", "노동자 / 일하는 사람", "생산이나 현장 일을 맡아 수행하는 사람", "지위보다 실제로 몸과 시간을 들여 일하는 사람", "laborer=노동을 제공하는 사람 / worker=일하는 사람 일반 / artisan=숙련 제작자"),
        "pilgrimage": ("journey", "여정 / 긴 이동 과정", "한 목적지를 향해 이어지는 이동이나 진행 과정", "출발해서 여러 단계를 지나 목적지로 가는 길", "journey=목적지를 향한 이동·과정 / trip=짧은 여행 / process=진행 과정"),
        "relic": ("vestige", "자취 / 아주 조금 남은 흔적", "거의 사라진 과거나 상태에서 조금 남아 있는 잔재", "큰 것은 없어졌는데 끝에 희미한 흔적만 남은 느낌", "vestige=희미하게 남은 자취 / remnant=남은 일부 / trace=흔적"),
        "royalty": ("leadership", "지도층 / 이끄는 역할", "집단의 방향과 결정을 이끄는 위치나 사람들", "앞에서 방향을 잡고 다른 사람을 이끄는 자리", "leadership=이끄는 역할·지도력 / authority=공식 권한 / status=사회적 지위"),
        "scribe": ("recorder", "기록 담당자 / 기록자", "논의나 사건을 글로 남기는 사람", "흘러가는 내용을 빠뜨리지 않고 적어두는 역할", "recorder=내용을 기록하는 사람 / writer=글쓴이 일반 / clerk=사무 기록 담당자"),
        "numismatic": ("archival", "기록 보관의 / 아카이브 관련의", "문서와 자료를 보관·정리해 두는 일과 관련된", "나중에 다시 찾을 수 있게 남겨두는 기록 쪽 느낌", "archival=기록 보관과 관련된 / documentary=문서 기록의 / historical=역사와 관련된"),
        "manorial": ("institutional", "제도적 / 기관 차원의", "개인 선택보다 조직·제도의 틀 안에서 작동하는", "개인보다 큰 공식 구조가 움직이는 느낌", "institutional=제도·기관 차원의 / organizational=조직의 / individual=개인의"),
        "vassal": ("subordinate", "하위의 / 종속된 사람", "권한이나 지위가 위쪽에 비해 아래에 놓인 사람이나 위치", "중심에 서기보다 위 체계 아래에 딸려 있는 느낌", "subordinate=하위 지위의 사람·종속된 / dependent=의존적인 / assistant=보조자"),
        "citadel": ("stronghold", "거점 / 강한 기반", "영향력이나 방어가 단단히 유지되는 중심 근거지", "쉽게 밀리지 않는 단단한 중심 자리", "stronghold=힘이 집중된 거점 / base=기반 / center=중심지"),
        "hinterland": ("outlying", "외곽의 / 중심에서 떨어진", "중심 지역에서 벗어나 주변부에 놓인", "핵심 한복판이 아니라 가장자리 바깥쪽에 있는 느낌", "outlying=중심에서 떨어진 외곽의 / peripheral=주변부의 / remote=멀리 떨어진"),
        "marooned": ("stranded", "발이 묶인 / 오도 가도 못하는", "예상치 못한 이유로 이동하거나 빠져나가기 어려운", "어딘가에 남겨져 길이 막힌 느낌", "stranded=발이 묶인 / isolated=떨어져 고립된 / delayed=늦춰진"),
    },
}


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join(
        [
            f"핵심 뜻: {core}",
            f"부가 뜻: {extra}",
            f"핵심 느낌: {feeling}",
            f"구분: {distinction}",
        ]
    )


def load_all_cards() -> dict[str, list[list[str]]]:
    result: dict[str, list[list[str]]] = {}
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            result[path.name] = [row for row in csv.reader(f, delimiter="\t") if row]
    return result


def write_all_cards(cards_by_file: dict[str, list[list[str]]]) -> None:
    for filename, rows in cards_by_file.items():
        with (ROOT / filename).open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t", lineterminator="\n")
            writer.writerows(rows)


def refresh_wordlists(cards_by_file: dict[str, list[list[str]]]) -> None:
    ets_words: list[str] = []
    for filename in sorted(cards_by_file):
        ets_words.extend(row[0].strip() for row in cards_by_file[filename])

    awl_words: list[str] = []
    for path in sorted(ROOT.glob("toefl_awl_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            awl_words.extend(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)

    (ROOT / ".existing_words.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_ets_headwords.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_awl_headwords.txt").write_text("\n".join(awl_words) + "\n", encoding="utf-8")
    (ROOT / "all_headwords.txt").write_text("\n".join(sorted(set(ets_words + awl_words))) + "\n", encoding="utf-8")


def validate_no_duplicate_plan(cards_by_file: dict[str, list[list[str]]]) -> None:
    current_owner: dict[str, str] = {}
    for filename, rows in cards_by_file.items():
        for row in rows:
            word = row[0].strip()
            if word in current_owner:
                raise RuntimeError(f"Existing duplicate headword before rewrite: {word} in {filename} and {current_owner[word]}")
            current_owner[word] = filename

    for filename, mapping in REPLACEMENTS.items():
        for old_word, (new_word, *_rest) in mapping.items():
            if old_word not in current_owner:
                raise RuntimeError(f"{old_word} not found in {filename}")
            owner = current_owner.get(new_word)
            if owner is not None and not (owner == filename and new_word == old_word):
                raise RuntimeError(f"Replacement word {new_word} already exists in {owner}, cannot use in {filename}")


def apply_replacements(cards_by_file: dict[str, list[list[str]]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for filename, mapping in REPLACEMENTS.items():
        rows = cards_by_file[filename]
        rewritten = []
        for word, _back in rows:
            if word in mapping:
                new_word, core, extra, feeling, distinction = mapping[word]
                rewritten.append([new_word, build_back(core, extra, feeling, distinction)])
                counts[filename] += 1
            else:
                rewritten.append([word, _back])
        cards_by_file[filename] = rewritten
    return counts


def main() -> None:
    cards_by_file = load_all_cards()
    validate_no_duplicate_plan(cards_by_file)
    counts = apply_replacements(cards_by_file)
    write_all_cards(cards_by_file)
    refresh_wordlists(cards_by_file)

    print("rebalanced sets:")
    for filename in sorted(counts):
        print(f"{filename}: {counts[filename]} cards replaced")


if __name__ == "__main__":
    main()
