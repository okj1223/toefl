from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_16.tsv"

CARDS = [
    ("acclimate", "적응하다 / 환경에 익숙해지다", "새 조건에 맞게 몸이나 방식이 서서히 맞춰지다", "낯선 조건을 버티며 점점 그 온도에 몸이 맞는 느낌", "acclimate=새 환경에 익숙해지다 / adapt=변화에 맞춰 조정하다 / adjust=세부를 맞춰 바꾸다"),
    ("activation", "활성화 / 작동 시작", "멈춰 있던 기능이나 반응이 실제로 켜져 움직이기 시작함", "꺼져 있던 스위치가 켜지며 과정이 살아나는 느낌", "activation=작동을 시작시킴 / stimulation=반응을 자극함 / initiation=시작 단계"),
    ("amplifier", "증폭 요인 / 강화 장치", "신호나 효과를 더 크게 키우는 것", "작게 들어온 신호를 더 크게 밀어 올리는 느낌", "amplifier=신호·효과를 키우는 것 / catalyst=변화를 촉진하는 요인 / enhancer=효과를 높이는 것"),
    ("anatomical", "구조상의 / 해부학적", "겉모습보다 내부 형태와 구성 구조에 관련된", "무엇이 어떻게 생겼고 어디에 놓였는지 구조를 보는 느낌", "anatomical=몸·내부 구조와 관련된 / structural=구조적인 / functional=작동 방식의"),
    ("bioindicator", "생물 지표 / 생태 상태를 보여주는 지표", "환경이나 시스템 상태를 간접적으로 보여주는 생물학적 단서", "겉으로 안 보이는 변화를 대신 알려주는 살아있는 신호등", "bioindicator=생물을 통해 상태를 보여주는 지표 / indicator=상태를 보여주는 신호 / biomarker=생체 상태를 나타내는 표지"),
    ("biomechanical", "생체역학적 / 구조와 힘의 작용에 관한", "살아 있는 구조가 힘과 움직임을 어떻게 견디고 전달하는지와 관련된", "몸이나 구조를 힘이 지나가는 장치처럼 보는 느낌", "biomechanical=생체 구조와 힘의 작용 관련 / mechanical=힘과 움직임의 / physiological=몸의 기능 작동과 관련된"),
    ("biosphere", "생물권 / 생명이 존재하는 전체 영역", "지구에서 생명체와 환경이 함께 맞물려 존재하는 큰 범위", "개별 생물보다 생명이 깔린 전체 층을 보는 느낌", "biosphere=생명체가 존재하는 전체 영역 / ecosystem=상호작용하는 생태 체계 / habitat=특정 서식지"),
    ("calibration", "보정 / 기준 맞춤", "측정이나 반응이 기준에 맞게 나오도록 눈금을 다시 맞춤", "어긋난 계기를 기준선에 맞춰 다시 조이는 느낌", "calibration=측정 기준을 다시 맞춤 / adjustment=세부를 조정함 / standardization=기준을 통일함"),
    ("camouflage", "위장 / 주변에 섞여 숨음", "눈에 띄지 않도록 주변 색·형태와 비슷하게 보이는 성질이나 전략", "배경 속에 묻혀 쉽게 구별되지 않게 숨는 느낌", "camouflage=주변에 섞여 숨는 위장 / concealment=감춤 / adaptation=환경에 맞춘 변화"),
    ("carbohydrate", "탄수화물", "에너지 공급이나 구조 형성에 쓰이는 주요 유기 영양 성분", "몸이나 시스템이 연료처럼 꺼내 쓰는 기본 재료", "carbohydrate=주요 에너지 영양 성분 / nutrient=영양분 일반 / glucose=당의 한 종류"),
    ("cellular", "세포 수준의 / 작은 단위 구조의", "큰 전체보다 아주 작은 기본 단위에서 일어나는 것과 관련된", "큰 덩어리를 쪼개 가장 작은 작동 단위에서 보는 느낌", "cellular=세포·작은 단위 수준의 / microscopic=현미경적 규모의 / systemic=전체 시스템 수준의"),
    ("circulatory", "순환의 / 흐름을 돌리는", "물질이나 정보가 닫힌 경로나 체계 안에서 돌아 움직이는 것과 관련된", "한 번 쓰고 끝이 아니라 길을 따라 계속 도는 느낌", "circulatory=흐름을 순환시키는 / distributive=여러 곳에 나눠 퍼뜨리는 / linear=한 방향으로만 이어지는"),
    ("coexist", "공존하다", "서로 다른 요소나 집단이 같은 공간이나 체계 안에 함께 존재하다", "하나가 다른 하나를 완전히 밀어내지 않고 같이 자리 잡는 느낌", "coexist=함께 존재하다 / interact=서로 영향을 주고받다 / compete=자리를 두고 겨루다"),
    ("compartment", "구획 / 분리된 칸", "전체 안에서 특정 기능이나 내용을 따로 담는 분리된 부분", "한 덩어리 속을 칸막이로 나눠 역할을 가르는 느낌", "compartment=분리된 구획 / section=부분 구역 / chamber=닫힌 공간"),
    ("conductive", "전달성이 있는 / 잘 통하는", "열·전기·신호 같은 것이 지나가기 쉬운 성질의", "막히지 않고 안을 통해 신호가 잘 흐르는 느낌", "conductive=열·신호를 잘 전달하는 / permeable=물질이 통과하기 쉬운 / insulating=흐름을 막는"),
    ("convergent", "수렴하는 / 한쪽으로 모이는", "서로 다른 흐름이나 특징이 점점 비슷한 방향으로 모이는", "따로 출발했지만 끝에서 점점 한 점으로 좁혀지는 느낌", "convergent=한 방향으로 수렴하는 / divergent=서로 갈라지는 / similar=비슷한"),
    ("cyclic", "주기적인 / 순환하는", "한 번으로 끝나지 않고 일정한 패턴으로 되풀이되는", "직선으로만 가지 않고 다시 처음 쪽으로 돌아오는 느낌", "cyclic=되풀이되는 순환형의 / periodic=일정 주기로 반복되는 / linear=직선적으로 진행되는"),
    ("decay", "쇠퇴 / 분해되다", "시간이 지나며 구조나 강도, 질서가 약해지거나 쪼개지다", "단단하던 것이 서서히 풀리고 무너지는 느낌", "decay=서서히 약해지거나 분해됨 / erosion=표면이 깎여 닳음 / deterioration=상태가 나빠짐"),
    ("decomposition", "분해 / 구성 요소로 쪼개짐", "복잡한 것이 더 단순한 부분으로 나뉘거나 해체됨", "큰 덩어리가 작은 조각과 성분으로 풀리는 느낌", "decomposition=구성 요소로 분해됨 / breakdown=작동·구조가 무너짐 / analysis=개념적으로 나누어 살펴봄"),
    ("differentiation", "분화 / 차별화", "처음 비슷하던 것이 서로 다른 기능이나 특징을 갖도록 갈라짐", "같은 출발점에서 각자 다른 역할로 갈라져 가는 느낌", "differentiation=다르게 분화·구별됨 / specialization=특정 역할에 맞게 특화됨 / distinction=차이를 구분함"),
    ("dispersal", "확산 / 흩어져 퍼짐", "한 곳에 모여 있던 것이 여러 방향으로 퍼져 나감", "뭉쳐 있던 점들이 바깥으로 흩어져 번지는 느낌", "dispersal=여러 방향으로 퍼져 흩어짐 / distribution=어디에 얼마나 퍼져 있는지의 배치 / diffusion=서서히 퍼지는 과정"),
    ("dormancy", "휴면 상태 / 잠잠히 멈춰 있음", "겉으로 활동이 거의 멈췄지만 완전히 사라진 것은 아닌 상태", "꺼진 듯 조용하지만 조건이 맞으면 다시 깨어날 수 있는 느낌", "dormancy=활동이 잠시 멈춘 휴면 상태 / inactivity=비활동 상태 일반 / extinction=완전히 사라짐"),
    ("downregulate", "하향 조절하다 / 작동을 낮추다", "반응이나 기능의 강도나 발현 수준을 줄이다", "너무 센 출력을 한 단계 낮춰 누르는 느낌", "downregulate=작동 수준을 낮추다 / suppress=억제하다 / attenuate=강도를 약화시키다"),
    ("ecological", "생태적 / 상호 환경 관계의", "개별 대상보다 주변 환경과 상호작용 속 관계를 보는", "혼자 떼어 보지 않고 둘러싼 관계망 안에서 보는 느낌", "ecological=환경과 상호관계 중심의 / environmental=주변 환경의 / biological=생물의"),
    ("efficiency ratio", "효율 비율 / 투입 대비 산출 비", "넣은 자원에 비해 얼마나 많은 결과가 나오는지 보여주는 비율", "쏟아 넣은 만큼 얼마나 잘 뽑아내는지 따지는 눈금", "efficiency ratio=투입 대비 산출의 효율 비 / yield=얻어낸 산출량 / productivity=생산성"),
    ("emergent", "새롭게 나타나는 / 상호작용에서 생겨나는", "부분만 따로 볼 때는 없던 특성이 전체 상호작용 속에서 드러나는", "조각을 합쳐 돌렸을 때 비로소 새 성질이 솟아오르는 느낌", "emergent=상호작용 속에서 새로 나타나는 / novel=새로운 / inherent=원래 안에 들어 있는"),
    ("encapsulate", "감싸 담다 / 핵심을 압축해 담다", "내용이나 기능을 한 경계 안에 넣어 보호하거나 요약해 담다", "중요한 것을 한 껍질 안에 모아 싸두는 느낌", "encapsulate=경계 안에 담거나 요약해 담다 / enclose=둘러싸 넣다 / summarize=핵심만 줄여 말하다"),
    ("equilibrate", "평형을 이루다 / 균형을 맞추다", "차이나 불균형이 줄어들며 비교적 안정된 상태로 맞춰지다", "한쪽으로 기운 상태가 서서히 가운데로 돌아오는 느낌", "equilibrate=평형 상태로 맞춰지다 / balance=균형을 맞추다 / stabilize=안정되게 하다"),
    ("exogenous", "외부에서 온 / 외생적인", "시스템 안에서 생긴 것이 아니라 바깥 원인에서 들어온", "안쪽 자체보다 밖에서 밀고 들어온 요인을 보는 느낌", "exogenous=외부 원인에서 온 / external=바깥의 / endogenous=내부에서 생긴"),
    ("feedback-driven", "피드백에 따라 조정되는", "한 번 정한 대로 고정되지 않고 돌아오는 반응을 바탕으로 바뀌는", "결과가 다시 돌아와 다음 작동의 손잡이를 돌리는 느낌", "feedback-driven=반응을 받아가며 조정되는 / adaptive=상황에 맞게 조정되는 / fixed=고정된"),
    ("flow-through", "흘러 통과하는 / 관통 흐름의", "자원이나 정보가 한 곳에 머물지 않고 들어와 지나가며 이어지는", "고여 쌓이기보다 안을 통과해 계속 흘러가는 느낌", "flow-through=안으로 들어와 지나가는 흐름의 / retained=안에 남겨진 / blocked=막힌"),
    ("frictionless", "마찰이 적은 / 막힘없이 진행되는", "절차나 이동이 불필요한 저항 없이 쉽게 이어지는", "중간 걸림돌 없이 매끄럽게 미끄러져 가는 느낌", "frictionless=저항이 적고 매끄러운 / smooth=부드럽게 이어지는 / cumbersome=절차가 번거로운"),
    ("gradational", "단계적으로 이어지는 / 점층적인", "뚝 끊긴 범주보다 연속적인 정도 차이로 변하는", "검은색과 흰색 사이가 서서히 여러 층으로 이어지는 느낌", "gradational=정도가 연속적으로 변하는 / discrete=뚝 나뉜 / gradual=서서히 진행되는"),
    ("growth curve", "성장 곡선 / 증가 양상", "시간에 따라 크기나 수준이 어떻게 늘어나는지 보여주는 변화선", "조금씩 오르거나 꺾이는 증가 흐름을 선으로 그린 느낌", "growth curve=시간에 따른 성장 변화선 / trend line=경향선 / trajectory=진행 경로"),
    ("homeostatic", "항상성을 유지하는 / 균형 조절의", "외부 변화가 있어도 내부 상태를 일정 범위 안에 맞추려는", "흔들려도 중심값 근처로 다시 끌어오는 조절 느낌", "homeostatic=내부 균형을 유지하려는 / self-regulating=스스로 조절하는 / stable=안정된"),
    ("hybridize", "혼합하다 / 서로 다른 것을 결합하다", "서로 다른 유형이나 방식의 요소를 섞어 새 조합을 만들다", "한 갈래만 쓰지 않고 두 계열을 섞어 새 형태를 내는 느낌", "hybridize=다른 유형을 섞어 결합하다 / integrate=하나의 체계로 묶다 / blend=섞다"),
    ("indicator species", "지표종 / 환경 상태를 보여주는 종", "특정 환경 조건이나 변화 상태를 알려주는 대표 생물종", "그 생물이 보이느냐로 주변 상태를 짐작하는 신호 역할", "indicator species=환경 상태를 알려주는 대표 종 / bioindicator=생물 지표 / sample=표본"),
    ("inflow", "유입 / 안으로 들어오는 흐름", "자원·정보·물질이 시스템 안으로 들어오는 양이나 움직임", "밖에서 안쪽으로 계속 흘러 들어오는 물줄기", "inflow=안으로 들어오는 흐름 / outflow=밖으로 나가는 흐름 / intake=받아들이는 양"),
    ("interdependent", "상호의존적인", "각 요소가 따로 독립해 있지 않고 서로 기대며 영향을 주고받는", "하나만 바뀌어도 다른 쪽이 같이 흔들릴 만큼 얽힌 느낌", "interdependent=서로 의존하며 연결된 / independent=독립적인 / interconnected=서로 이어진"),
    ("life cycle", "생애주기 / 순환 단계", "시작부터 성장, 변화, 끝 또는 반복까지 이어지는 전체 단계", "한 시점만이 아니라 처음부터 다음 단계까지 한 바퀴 도는 흐름", "life cycle=전체 순환 단계 / sequence=정해진 순서 / lifespan=지속 기간"),
    ("microstructure", "미세 구조 / 작은 수준의 내부 짜임", "겉에서 바로 보이지 않는 작은 단위 수준의 배열과 구조", "전체 표면 아래 확대했을 때 드러나는 안쪽 세부 짜임", "microstructure=미세한 내부 구조 / structure=짜임 일반 / texture=표면이나 조직감"),
    ("modulator", "조절 요인 / 강도를 바꾸는 요소", "반응이나 신호 자체를 새로 만들기보다 그 세기를 바꾸는 요소", "음량 손잡이처럼 작동 강도를 올리거나 내리는 역할", "modulator=반응 강도를 조절하는 요인 / regulator=작동 수준을 조정하는 요소 / trigger=시작을 일으키는 계기"),
    ("morphological", "형태상의 / 모양 구조와 관련된", "기능보다 겉과 내부 형태, 구성 모양의 차이에 관련된", "무엇이 어떤 모양과 배열을 가졌는지 보는 느낌", "morphological=형태와 구조 차이에 관한 / anatomical=내부 구조상의 / functional=기능상의"),
    ("niche", "틈새 역할 / 특정 자리", "전체 체계 안에서 어떤 대상이 맡는 특정 위치나 역할", "큰 판 안에서 내가 딱 들어맞는 좁지만 분명한 자리", "niche=특정 환경·시장 안의 자리나 역할 / role=맡은 역할 일반 / habitat=사는 장소"),
    ("nutrient-rich", "영양분이 풍부한 / 자원이 많은", "성장이나 생산에 필요한 성분이 충분히 들어 있는", "자라거나 돌아가기에 필요한 재료가 넉넉히 채워진 느낌", "nutrient-rich=필요한 영양·자원이 많은 / fertile=생산성이 높은 / resource-poor=자원이 부족한"),
    ("organismal", "개체 수준의 / 생물 개체와 관련된", "세포 하나가 아니라 한 생물 개체 전체를 단위로 보는", "조각보다 한 생명체 전체를 하나의 단위로 잡는 느낌", "organismal=생물 개체 수준의 / cellular=세포 수준의 / ecological=환경 관계 수준의"),
    ("oscillation", "진동 / 오르내림의 반복", "값이나 상태가 한 방향으로만 가지 않고 반복해서 왔다 갔다 함", "중심 주변을 두고 위아래로 흔들리며 되풀이되는 느낌", "oscillation=반복적으로 흔들리는 변동 / fluctuation=불규칙한 오르내림 / cycle=되풀이되는 주기"),
    ("outcompete", "경쟁에서 이기다 / 더 잘 버티다", "같은 자원이나 자리에서 다른 대상보다 더 우세해지다", "같은 판에서 더 잘 가져가며 상대를 밀어내는 느낌", "outcompete=경쟁에서 더 우세해지다 / dominate=위에서 강하게 앞서다 / coexist=함께 존재하다"),
    ("overflow", "넘침 / 한계를 넘어 흘러나옴", "용량이나 경계를 넘어서 밖으로 흘러나가거나 넘쳐 확산됨", "담아둔 선을 넘어 밖으로 흘러넘치는 느낌", "overflow=한계를 넘어 밖으로 넘침 / spillover=주변으로 퍼진 파급 효과 / excess=남아도는 초과분"),
    ("parameterize", "매개변수로 규정하다 / 조건값을 설정하다", "모형이나 과정이 어떤 값과 조건에 따라 움직이는지 변수로 정해 넣다", "막연한 설명 대신 조절 손잡이 값을 정해 작동 방식을 박아두는 느낌", "parameterize=조건값으로 모형을 규정하다 / specify=구체적으로 지정하다 / calibrate=기준에 맞게 보정하다"),
    ("partition", "분할하다 / 구획으로 나누다", "전체를 기능이나 기준에 따라 여러 부분으로 나눠 배치하다", "한 덩어리를 칸막이로 잘라 각 구역을 나누는 느낌", "partition=기준에 따라 나누어 구획함 / divide=나누다 일반 / allocate=몫을 배정하다"),
    ("permeability", "투과성 / 통과하기 쉬움", "물질이나 신호가 경계나 막을 얼마나 잘 지나갈 수 있는지의 성질", "벽이 완전히 막힌 게 아니라 어느 정도 지나갈 틈이 있는 느낌", "permeability=경계를 통과하기 쉬운 성질 / porosity=구멍이 많은 정도 / conductivity=열·신호를 잘 전달함"),
    ("phenotypic", "겉으로 드러난 특성의", "안쪽 원인보다 관찰 가능한 형태와 성질로 나타난 것과 관련된", "속의 설계보다 바깥에서 실제로 보이는 모습 쪽을 보는 느낌", "phenotypic=관찰되는 겉특성의 / genetic=유전 정보의 / morphological=형태상의"),
    ("photosensitive", "빛에 민감한 / 광반응성의", "빛 자극이나 밝기 변화에 반응하기 쉬운", "빛이 닿으면 그냥 지나가지 않고 반응이 열리는 느낌", "photosensitive=빛 자극에 민감한 / responsive=반응을 잘 보이는 / inert=반응성이 낮은"),
    ("plasticity", "가소성 / 유연하게 바뀌는 성질", "경험이나 조건에 따라 구조나 기능이 고정되지 않고 달라질 수 있음", "딱 굳지 않고 상황에 맞게 다시 모양이 바뀌는 느낌", "plasticity=조건에 따라 바뀔 수 있는 성질 / flexibility=유연성 / rigidity=고정되어 잘 안 바뀜"),
    ("porosity", "다공성 / 빈틈이 많은 정도", "작은 구멍이나 빈틈이 많아 물질이 스며들거나 통과할 여지가 있는 성질", "겉은 막혀 보여도 안에 작은 틈길이 많은 느낌", "porosity=빈틈과 구멍이 많은 성질 / permeability=실제로 통과하기 쉬운 성질 / density=빽빽한 정도"),
    ("predation", "포식 / 잡아먹음", "한 생물이나 주체가 다른 대상을 사냥하거나 소비하며 우위에 서는 관계", "관계망 안에서 한쪽이 다른 쪽을 먹이처럼 끌어가는 느낌", "predation=먹이로 삼아 잡아먹는 관계 / competition=자원을 두고 겨룸 / parasitism=붙어서 이득을 얻음"),
    ("pressure gradient", "압력 구배 / 압력 차에 따른 변화 경사", "한쪽과 다른 쪽의 압력 차이가 흐름이나 이동을 만들어내는 정도 차이", "높은 곳에서 낮은 곳으로 밀어내는 차이의 기울기", "pressure gradient=압력 차가 만든 변화 경사 / gradient=정도 차의 기울기 / differential=둘 사이의 차이"),
    ("reassembly", "재조립 / 다시 짜 맞춤", "흩어진 부분들을 다시 모아 하나의 구조나 작동 체계로 맞춤", "분해된 조각을 다시 제자리에 끼워 전체를 세우는 느낌", "reassembly=부분을 다시 조립함 / reconstruction=다시 세우거나 재구성함 / repair=고장난 것을 고침"),
    ("recombination", "재조합 / 새 조합으로 섞임", "기존 요소들이 다시 섞이며 이전과 다른 조합을 만듦", "있던 조각들을 다시 섞어 새 배열을 만드는 느낌", "recombination=기존 요소의 새 조합 형성 / combination=함께 묶임 일반 / hybridization=서로 다른 유형을 섞음"),
    ("regenerative", "재생의 / 다시 회복시키는", "손상이나 소모 후 다시 자라거나 기능을 되살리는 성질의", "잃은 것을 끝으로 두지 않고 다시 채워 살아나는 느낌", "regenerative=다시 자라거나 회복시키는 / restorative=원래 상태로 되돌리는 / renewable=다시 보충 가능한"),
    ("replicable", "재현 가능한 / 반복 검증 가능한", "같은 방법을 다시 적용했을 때 비슷한 결과를 얻을 수 있는", "한 번만 우연히가 아니라 다시 해도 따라 나오는 느낌", "replicable=같은 결과를 다시 재현할 수 있는 / reproducible=다시 만들어 확인 가능한 / unique=한 번뿐인"),
    ("resource uptake", "자원 흡수 / 자원 받아들임", "외부의 영양·물질·정보를 안으로 들여와 활용하는 과정", "밖에 있는 걸 그냥 두지 않고 안으로 끌어들여 쓰는 느낌", "resource uptake=자원을 안으로 받아들이는 과정 / intake=들어오는 양 / absorption=안으로 흡수됨"),
    ("retentive", "보유력이 있는 / 잘 유지하는", "들어온 정보나 물질, 상태를 쉽게 잃지 않고 붙잡아 두는", "한 번 들어온 것을 흘려보내지 않고 오래 잡고 있는 느낌", "retentive=잘 보유하고 유지하는 / absorptive=잘 흡수하는 / porous=빈틈이 많은"),
    ("self-regulating", "자기 조절적인 / 스스로 균형을 맞추는", "외부가 매번 조정하지 않아도 내부 기준에 따라 스스로 상태를 맞추는", "흔들리면 안에서 알아서 손잡이를 돌려 균형을 찾는 느낌", "self-regulating=스스로 상태를 조절함 / homeostatic=내부 균형을 유지함 / externally controlled=밖에서 통제됨"),
    ("sensitivity range", "민감도 범위 / 반응 가능한 구간", "자극이나 변화에 의미 있게 반응할 수 있는 값의 범위", "너무 약하거나 강한 구간 밖이 아니라 반응이 살아나는 눈금대", "sensitivity range=반응이 가능한 민감도 구간 / threshold=반응이 시작되는 경계 / tolerance=견딜 수 있는 범위"),
    ("signal cascade", "신호 연쇄 / 단계적 전달 반응", "한 신호가 다음 반응들을 차례로 이어 일으키는 연쇄 과정", "첫 신호 하나가 아래 단계로 줄줄이 내려가며 반응을 여는 느낌", "signal cascade=신호가 연쇄적으로 이어지는 과정 / transmission=신호 전달 / pathway=경로"),
    ("sink-source", "흡수원-공급원 관계의", "어떤 곳은 자원을 받아들이고 어떤 곳은 내보내는 흐름 관계를 나타내는", "한쪽은 끌어들이고 다른 쪽은 밀어내며 균형을 만드는 느낌", "sink-source=흡수원과 공급원의 대응 관계 / inflow-outflow=들어오고 나가는 흐름 / distribution=분포"),
    ("size-selective", "크기에 따라 선별되는", "대상의 크기 차이에 따라 통과·생존·선택 여부가 달라지는", "큰 것과 작은 것이 같은 문을 통과하지 못하고 따로 걸러지는 느낌", "size-selective=크기에 따라 선택되는 / selective=기준에 따라 골라지는 / random=무작위의"),
    ("spatially patterned", "공간적으로 패턴이 있는", "위치에 따라 무작위가 아니라 일정한 배열이나 반복 구조가 나타나는", "어디에 놓였는지가 우연이 아니라 눈에 보이는 무늬를 이루는 느낌", "spatially patterned=공간상 배열에 패턴이 있는 / scattered=흩어진 / clustered=무리지어 모인"),
    ("stabilizer", "안정화 요인 / 흔들림을 줄이는 것", "변동이나 과잉 반응을 줄여 상태를 더 안정되게 만드는 요소", "출렁이는 것을 한가운데로 붙잡아 두는 중심추", "stabilizer=상태를 안정되게 하는 요인 / buffer=충격을 완충하는 것 / regulator=작동 수준을 조절하는 요소"),
    ("survivorship", "생존 유지 / 오래 남아 버팀", "시간이나 조건 변화 속에서 계속 살아남거나 유지되는 정도", "중간에 떨어져 나가지 않고 끝까지 남아 버티는 느낌", "survivorship=생존이 유지되는 정도 / resilience=충격 후 회복력 / persistence=계속 남아 있음"),
    ("symbiotic", "공생의 / 서로 기대어 사는", "서로 다른 주체가 함께 있으면서 일정한 이익이나 영향을 주고받는", "완전히 따로보다 가까이 붙어 서로 기대는 관계", "symbiotic=서로 기대어 사는 공생의 / cooperative=협력적인 / parasitic=한쪽만 이득을 보는"),
    ("threshold-sensitive", "문턱값에 민감한", "작은 변화에는 반응이 적다가 특정 경계를 넘으면 뚜렷이 달라지는", "한 선 전에는 잠잠하다가 선을 넘는 순간 확 바뀌는 느낌", "threshold-sensitive=경계값을 넘을 때 반응이 커지는 / gradual=서서히 변하는 / abrupt=갑작스러운"),
    ("transboundary", "경계를 넘나드는 / 경계 간의", "행정·생태·공간적 경계 하나 안에만 머물지 않고 여러 경계를 가로지르는", "선 하나로 딱 막히지 않고 이쪽과 저쪽을 함께 건너는 느낌", "transboundary=여러 경계를 가로지르는 / local=한 지역 안의 / cross-regional=여러 지역에 걸친"),
    ("turnover rate", "교체율 / 순환 속도", "구성 요소가 얼마나 빠르게 바뀌거나 새 것으로 대체되는지의 비율", "한 자리에 같은 것이 오래 있지 않고 얼마나 빨리 갈리는지 보는 눈금", "turnover rate=구성 요소가 바뀌는 속도 비율 / replacement=대체 / retention=유지"),
    ("upregulate", "상향 조절하다 / 작동을 높이다", "반응이나 기능의 발현 수준이나 강도를 높이다", "낮게 돌아가던 출력을 한 단계 끌어올리는 느낌", "upregulate=작동 수준을 높이다 / enhance=효과를 높이다 / activate=작동을 시작시키다"),
    ("viability threshold", "생존 가능 문턱 / 유지 가능한 기준선", "어떤 개체나 시스템이 계속 유지되려면 넘어야 하는 최소 조건", "이 선 아래로 떨어지면 버티기 어려운 생존 기준선", "viability threshold=유지·생존 가능한 최소 기준선 / threshold=변화가 시작되는 경계 / viability=실현·생존 가능성"),
    ("adaptive capacity", "적응 역량 / 변화 대응 능력", "환경이나 조건 변화에 맞춰 작동 방식이나 구조를 바꿔 버틸 수 있는 능력", "흔들릴 때 부러지지 않고 새 조건에 맞춰 다시 자세를 잡는 힘", "adaptive capacity=변화에 맞춰 대응할 수 있는 능력 / resilience=충격 후 회복력 / flexibility=유연성"),
    ("boundary layer", "경계층 / 가장자리 접촉 층", "서로 다른 영역이 맞닿는 가장자리에서 상호작용이 두드러지는 얇은 층", "안쪽 본체보다 두 영역이 만나는 표면 가까운 얇은 띠", "boundary layer=맞닿은 경계 근처의 층 / interface=서로 만나는 접점 / edge=가장자리"),
    ("carrying capacity", "수용 한계 / 감당 가능한 최대치", "한 환경이나 시스템이 무리 없이 지탱할 수 있는 최대 규모나 양", "더 넣으면 버티기 어려워지는 감당 가능한 천장선", "carrying capacity=환경·시스템이 지탱 가능한 최대치 / capacity=수용 가능량 / limit=한계"),
    ("cross-adaptation", "교차 적응 / 한 변화가 다른 맥락에도 도움이 됨", "한 조건에서 생긴 적응이 다른 유사 조건에서도 이점을 주는 현상", "여기서 익힌 적응이 저기에서도 일부 통하는 느낌", "cross-adaptation=한 맥락의 적응이 다른 맥락에도 작용함 / transferability=다른 상황에 적용 가능함 / specialization=특정 조건에만 맞춘 특화"),
    ("density-dependent", "밀도 의존적인 / 붐빔 정도에 따라 달라지는", "개체나 요소가 얼마나 빽빽한지에 따라 효과나 성장률이 달라지는", "많이 몰릴수록 같은 조건도 다르게 작동하는 느낌", "density-dependent=밀도에 따라 결과가 달라지는 / crowding-sensitive=붐빔에 민감한 / independent=무관한"),
    ("disturbance-tolerant", "교란을 견디는 / 흔들림에 강한", "외부 충격이나 환경 변화가 있어도 비교적 버티고 유지되는", "판이 흔들려도 쉽게 무너지지 않고 남아 있는 느낌", "disturbance-tolerant=교란을 비교적 잘 견디는 / resilient=충격 후 회복력이 있는 / fragile=쉽게 깨지는"),
    ("energy budget", "에너지 배분 / 에너지 사용 균형", "사용 가능한 에너지가 성장·유지·활동 사이에 어떻게 나뉘는지 보는 틀", "한정된 연료를 어디에 얼마나 쓸지 몫을 나누는 느낌", "energy budget=에너지를 목적별로 나누어 보는 틀 / allocation=자원 배분 / expenditure=지출·소모"),
    ("flow dynamics", "흐름 동역학 / 움직임의 변화 양상", "물질·정보·에너지 흐름이 시간과 조건에 따라 어떻게 바뀌는지의 작동 양상", "고정된 상태보다 어디로 얼마나 빨리 흐르며 바뀌는지 보는 느낌", "flow dynamics=흐름이 어떻게 변하며 작동하는지 / circulation=순환 흐름 / trajectory=이동·변화 경로"),
    ("growth constraint", "성장 제약 / 커지는 것을 막는 조건", "자원·공간·시간 부족 때문에 증가나 확장이 제한되는 요인", "더 자라려 해도 어느 조건이 천장처럼 막는 느낌", "growth constraint=성장이나 증가를 막는 제한 요인 / bottleneck=흐름을 느리게 하는 병목 / limitation=한계"),
    ("habitat corridor", "서식지 연결 통로", "떨어진 공간 사이에서 이동이나 교류가 가능하도록 이어주는 경로", "끊긴 섬처럼 보이던 공간 사이를 이어주는 생명 이동길", "habitat corridor=서식지 사이 연결 통로 / pathway=지나가는 경로 / linkage=연결"),
    ("interaction zone", "상호작용 구역 / 접촉 영역", "서로 다른 요소나 집단이 만나 영향을 주고받는 공간이나 범위", "따로 있던 것들이 실제로 맞닿아 반응이 생기는 자리", "interaction zone=서로 영향을 주고받는 접촉 영역 / interface=접점 / boundary=경계"),
    ("metabolic rate", "대사 속도 / 에너지 처리 속도", "에너지나 물질이 내부 과정에서 얼마나 빠르게 사용·전환되는지의 비율", "안으로 들어온 연료가 얼마나 빠르게 돌며 쓰이는지 보는 눈금", "metabolic rate=내부 에너지·물질 처리 속도 / throughput=처리 흐름 / rate=변화 속도"),
    ("nutrient cycle", "영양분 순환 / 자원 순환 과정", "필요한 물질이 소비·분해·재사용을 거치며 시스템 안에서 다시 돌아가는 흐름", "한 번 쓰고 끝이 아니라 분해되어 다시 돌고 도는 자원 고리", "nutrient cycle=영양분이 다시 돌며 이어지는 과정 / cycle=반복 순환 / recycling=다시 회수해 재사용함"),
    ("oxygenation", "산소 공급 / 산소가 스며듦", "산소가 어떤 환경이나 물질 안으로 들어가거나 충분히 공급되는 과정", "막힌 곳에 공기가 돌며 다시 숨이 트이는 느낌", "oxygenation=산소를 공급하거나 스며들게 함 / ventilation=공기를 통하게 함 / aeration=공기를 섞어 넣음"),
    ("resource partitioning", "자원 분할 이용 / 자원 나눠쓰기", "서로 같은 자원을 완전히 겹치지 않게 나눠 써서 충돌을 줄이는 방식", "한 그릇을 똑같이 싸우지 않고 영역을 조금씩 갈라 쓰는 느낌", "resource partitioning=자원을 나눠 써서 겹침을 줄임 / allocation=자원 배분 / competition=같은 자원을 두고 겨룸"),
    ("self-renewal", "자기 갱신 / 스스로 다시 채움", "외부에서 전부 새로 넣지 않아도 내부적으로 다시 보충되거나 유지되는 성질", "소모되기만 하지 않고 안에서 다시 새것을 만들어 메우는 느낌", "self-renewal=스스로를 다시 보충·갱신함 / regeneration=손상 후 다시 자라남 / replacement=다른 것으로 대체됨"),
    ("stress response", "스트레스 반응 / 압박에 대한 대응", "외부 부담이나 충격이 들어왔을 때 상태를 조정하며 대응하는 과정", "압력이 들어오면 그대로 깨지지 않고 몸이나 체계가 대응 모드로 바뀌는 느낌", "stress response=부담에 대응하는 반응 과정 / adaptation=조건에 맞춰 조정됨 / resistance=버티는 힘"),
    ("bioenergetic", "에너지 흐름과 관련된 / 생체 에너지의", "살아 있는 체계나 과정에서 에너지가 어떻게 들어가고 쓰이는지와 관련된", "모양보다 에너지가 어디서 와서 어디에 쓰이는지 보는 느낌", "bioenergetic=에너지 사용·흐름과 관련된 / metabolic=내부 물질·에너지 전환의 / energetic=에너지와 관련된"),
    ("chemosensory", "화학 자극을 감지하는 / 화학 신호에 반응하는", "냄새나 농도 같은 화학적 단서를 받아들여 반응하는 성질의", "눈보다 화학 신호를 맡아 방향을 잡는 느낌", "chemosensory=화학 신호를 감지하는 / sensory=자극을 받아들이는 / responsive=반응하는"),
    ("co-regulation", "공동 조절 / 함께 균형을 맞춤", "한 요소만이 아니라 여러 요소가 서로 맞물려 작동 수준을 조정함", "손잡이 하나가 아니라 여러 조절축이 같이 눈금을 맞추는 느낌", "co-regulation=여러 요소가 함께 조절함 / self-regulation=스스로 조절함 / coordination=서로 맞춰 움직임"),
    ("cross-signaling", "교차 신호 전달 / 서로 다른 경로 간 신호 교환", "서로 다른 경로나 요소가 따로 움직이지 않고 신호를 주고받으며 연결됨", "옆 라인이 서로 무관하지 않고 중간중간 신호를 건네는 느낌", "cross-signaling=다른 경로 사이 신호 교환 / transmission=한 경로를 따라 전달 / interaction=서로 영향을 주고받음"),
    ("energy-efficient", "에너지 효율적인", "같은 결과를 내는 데 필요한 에너지 소모가 비교적 적은", "덜 태우고도 비슷한 일을 해내는 절약형 작동 느낌", "energy-efficient=에너지 소모가 적은 / efficient=자원 대비 결과가 좋은 / wasteful=낭비가 큰"),
    ("microhabitat", "미세 서식처 / 작은 규모의 환경 자리", "큰 환경 안에서도 조건이 조금 달라 특정 생물이나 과정이 자리 잡는 작은 공간", "넓은 환경 속에 숨어 있는 더 작은 조건의 자리", "microhabitat=작은 규모의 서식 환경 / habitat=서식지 일반 / niche=체계 안의 특정 자리·역할"),
    ("moisture-retaining", "수분을 붙잡아 두는 / 보습성 있는", "물이 쉽게 빠져나가지 않고 안에 어느 정도 유지되게 하는", "들어온 물을 흘려보내지 않고 머금고 붙잡는 느낌", "moisture-retaining=수분을 잘 유지하는 / retentive=들어온 것을 잘 붙잡는 / permeable=통과시키기 쉬운"),
    ("multiphase", "다단계의 / 여러 상태가 함께 있는", "하나의 단일 단계가 아니라 서로 다른 단계나 상태가 함께 얽힌", "한 층만 보는 게 아니라 여러 상태가 동시에 포개진 느낌", "multiphase=여러 단계·상태가 함께 있는 / stepwise=단계적인 / homogeneous=하나로 균일한"),
    ("photoperiodic", "일조 주기에 반응하는 / 빛 주기 기반의", "하루나 계절의 빛 길이 변화에 따라 반응이 달라지는", "빛이 얼마나 오래 들어오는지가 작동 타이밍을 잡는 느낌", "photoperiodic=빛의 주기 변화에 반응하는 / photosensitive=빛 자극에 민감한 / cyclic=주기적인"),
    ("re-oxygenate", "다시 산소를 공급하다", "산소가 부족해진 상태에 다시 산소를 들어가게 하다", "답답하게 막힌 상태에 공기를 다시 밀어 넣는 느낌", "re-oxygenate=다시 산소를 공급하다 / oxygenation=산소가 들어감·공급됨 / ventilate=공기를 통하게 하다"),
    ("resupply", "재공급하다 / 다시 채우다", "줄어든 자원이나 재료를 다시 넣어 부족분을 메우다", "비어 가는 쪽에 새 자원을 다시 밀어 넣는 느낌", "resupply=부족해진 것을 다시 공급하다 / replenish=다시 채워 넣다 / restore=원래 상태로 되돌리다"),
    ("self-sustaining", "자기 유지적인 / 스스로 지속 가능한", "외부 지원이 계속 많이 들어오지 않아도 내부 구조로 어느 정도 유지되는", "바깥에서 계속 밀지 않아도 안에서 버티며 돌아가는 느낌", "self-sustaining=스스로 유지되는 / autonomous=자율적으로 운영되는 / dependent=외부에 의존하는"),
    ("size-dependent", "크기에 따라 달라지는", "대상의 크기가 변하면 효과나 속도, 가능성도 함께 달라지는", "작고 크다는 차이가 결과를 그냥 바꾸는 핵심 조건이 되는 느낌", "size-dependent=크기에 따라 결과가 달라지는 / density-dependent=밀도에 따라 달라지는 / size-selective=크기에 따라 선별되는"),
    ("thermoregulatory", "체온·열 조절의 / 온도 균형 조절과 관련된", "내부 온도나 열 균형이 일정 범위에 머물도록 조절하는 작동과 관련된", "너무 뜨겁거나 차갑지 않게 온도 눈금을 맞추는 느낌", "thermoregulatory=온도 균형을 조절하는 / homeostatic=내부 균형을 유지하는 / thermal=열과 관련된"),
    ("water-retentive", "물을 잘 머금는 / 수분 보유력이 있는", "물이 쉽게 빠져나가지 않고 내부에 어느 정도 남아 있게 하는", "스펀지처럼 들어온 물을 붙잡아 오래 머금는 느낌", "water-retentive=물을 잘 보유하는 / moisture-retaining=수분을 유지하는 / porous=빈틈이 많은"),
]


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join([f"핵심 뜻: {core}", f"부가 뜻: {extra}", f"핵심 느낌: {feeling}", f"구분: {distinction}"])


def update_notes() -> None:
    gen = ROOT / "generation_notes.md"
    text = gen.read_text(encoding="utf-8")
    text = text.replace(
        "- ETS sets `01` to `14` exist, bringing the ETS-based total to 1400 cards\n",
        "- ETS sets `01` to `16` exist, bringing the ETS-based total to 1600 cards\n",
    )
    text = text.replace(
        "- ETS sets `01` to `15` exist, bringing the ETS-based total to 1500 cards\n",
        "- ETS sets `01` to `16` exist, bringing the ETS-based total to 1600 cards\n",
    )
    gen.write_text(text, encoding="utf-8")

    plan = ROOT / "WORK_PLAN.md"
    text = plan.read_text(encoding="utf-8")
    text = text.replace(
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_14.tsv`\n",
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_16.tsv`\n",
    )
    text = text.replace(
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_15.tsv`\n",
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_16.tsv`\n",
    )
    text = text.replace(
        "- Current ETS row count after the latest expansion pass: 1400\n",
        "- Current ETS row count after the latest expansion pass: 1600\n",
    )
    text = text.replace(
        "- Current ETS row count after the latest expansion pass: 1500\n",
        "- Current ETS row count after the latest expansion pass: 1600\n",
    )
    plan.write_text(text, encoding="utf-8")


def main() -> None:
    existing = set()
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.reader(f, delimiter="\t"):
                if row:
                    existing.add(row[0].strip())

    rows = []
    seen = set()
    for word, core, extra, feeling, distinction in CARDS:
        if word in existing or word in seen:
            continue
        rows.append([word, build_back(core, extra, feeling, distinction)])
        seen.add(word)
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
        manifest["files_created"].insert(15, TARGET.name)
    manifest["total_ets_cards"] = len(ets_words)
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    update_notes()
    print(f"{TARGET.name}: {len(rows)} cards")


if __name__ == "__main__":
    main()
