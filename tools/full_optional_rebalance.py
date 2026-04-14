#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LABELS = ["핵심 뜻:", "부가 뜻:", "핵심 느낌:", "구분:"]


def parse_back(back: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in back.split("\n"):
        for label in LABELS:
            if line.startswith(label):
                parsed[label] = line
                break
        else:
            raise ValueError(f"Unknown line in back: {line!r}")
    return parsed


def build_back(lines: dict[str, str]) -> str:
    return "\n".join(lines[label] for label in LABELS if label in lines)


ADDITIONS: dict[str, dict[str, dict[str, str]]] = {
    "toefl_awl_set_01.tsv": {
        "assist": {
            "구분:": "구분: assist=옆에서 보조하다 / support=넓게 지원하다",
        },
        "scheme": {
            "구분:": "구분: scheme=조직적 계획·제도 / plan=계획 일반 / plot=음모",
        },
    },
    "toefl_ets_2026_set_02.tsv": {
        "assess": {
            "구분:": "구분: assess=근거를 보고 평가하다 / measure=수치로 재다",
        },
        "clarify": {
            "구분:": "구분: clarify=헷갈림을 풀어 또렷하게 하다 / explain=설명하다",
        },
        "correlate": {
            "구분:": "구분: correlate=함께 움직이는 관련성을 보이다 / cause=원인으로 일으키다",
        },
        "estimate": {
            "구분:": "구분: estimate=대략 추정하다 / calculate=정확히 계산하다",
        },
        "facilitate": {
            "구분:": "구분: facilitate=과정을 쉽게 만들다 / accelerate=속도를 높이다",
        },
        "foster": {
            "구분:": "구분: foster=성장하도록 북돋우다 / facilitate=진행을 쉽게 하다",
        },
        "integrate": {
            "구분:": "구분: integrate=부분을 하나로 통합하다 / combine=여럿을 합치다",
        },
        "interpret": {
            "구분:": "구분: interpret=뜻을 해석하다 / translate=다른 언어로 옮기다",
        },
        "mitigate": {
            "구분:": "구분: mitigate=심각성을 줄이다 / eliminate=없애다",
        },
        "regulate": {
            "구분:": "구분: regulate=규칙이나 기준으로 조절하다 / monitor=지켜보다",
        },
        "threshold": {
            "구분:": "구분: threshold=판정이 바뀌는 기준선 / limit=허용 한계",
        },
        "apparent": {
            "구분:": "구분: apparent=겉으로 분명해 보이는 / actual=실제의",
        },
        "viable": {
            "구분:": "구분: viable=실행 가능하고 지속될 수 있는 / feasible=당장 해볼 수 있는",
        },
    },
    "toefl_ets_2026_set_05.tsv": {
        "deficit": {
            "구분:": "구분: deficit=부족분·적자 / surplus=남는 몫·흑자",
        },
        "surplus": {
            "구분:": "구분: surplus=남는 몫·흑자 / deficit=부족분·적자",
        },
        "fiscal": {
            "구분:": "구분: fiscal=정부 재정과 예산의 / monetary=통화와 화폐의",
        },
        "monetary": {
            "구분:": "구분: monetary=통화와 화폐의 / fiscal=정부 재정과 예산의",
        },
        "liability": {
            "구분:": "구분: liability=부채·법적 책임 / asset=자산",
        },
        "equity": {
            "구분:": "구분: equity=자기자본 또는 공정성 / asset=자산 / equality=평등",
        },
        "monopoly": {
            "구분:": "구분: monopoly=한 기업의 독점 / oligopoly=소수 기업의 지배",
        },
        "jurisdiction": {
            "구분:": "구분: jurisdiction=법적 관할권 / authority=권한 일반",
        },
        "statute": {
            "구분:": "구분: statute=성문 법령 / regulation=세부 규정",
        },
        "treaty": {
            "구분:": "구분: treaty=국가 간 조약 / agreement=합의 일반",
        },
        "mediate": {
            "구분:": "구분: mediate=양측을 중재하다 / arbitrate=판단을 내려 재정하다",
        },
        "arbitrate": {
            "구분:": "구분: arbitrate=판단을 내려 재정하다 / mediate=합의를 돕다",
        },
        "accountability": {
            "구분:": "구분: accountability=결과를 설명하고 책임지는 의무 / responsibility=책임 일반",
        },
        "compliance": {
            "구분:": "구분: compliance=규정 준수 / obedience=복종",
        },
    },
    "toefl_ets_2026_set_12.tsv": {
        "awareness": {
            "구분:": "구분: awareness=알아차리고 의식하는 상태 / attention=한 대상에 주의를 모음",
        },
        "attachment": {
            "부가 뜻:": "부가 뜻: 정서적 유대",
            "구분:": "구분: attachment=정서적으로 붙는 유대 / dependency=상대에게 기대는 의존",
        },
        "belief": {
            "구분:": "구분: belief=사실처럼 받아들이는 믿음 / assumption=검증 전 가정",
        },
        "concentration": {
            "구분:": "구분: concentration=한 대상에 집중한 상태 / distraction=주의가 흩어짐",
        },
        "empathy": {
            "구분:": "구분: empathy=남의 감정을 함께 느끼는 공감 / sympathy=안타깝게 여기는 동정",
        },
        "expectation": {
            "구분:": "구분: expectation=앞으로 그렇게 될 거라는 예상 / hope=바라는 마음",
        },
        "identity": {
            "부가 뜻:": "부가 뜻: 자기 정체감",
            "구분:": "구분: identity=나는 누구인가에 대한 자아 틀 / role=상황 속 맡은 역할",
        },
        "intention": {
            "구분:": "구분: intention=하려는 마음과 의도 / impulse=즉각 튀는 충동",
        },
        "judgment": {
            "구분:": "구분: judgment=따져 본 뒤 내린 판단 / opinion=의견",
        },
        "memory": {
            "구분:": "구분: memory=저장된 기억 전체 / recall=기억을 꺼내기",
        },
        "mindfulness": {
            "구분:": "구분: mindfulness=현재를 의식적으로 알아차림 / concentration=한 대상에 집중함",
        },
        "misconception": {
            "구분:": "구분: misconception=잘못 굳어진 오해 / error=개별 실수",
        },
        "preference": {
            "구분:": "구분: preference=상대적으로 더 좋아하는 경향 / bias=한쪽으로 기운 편향",
        },
        "reasoning": {
            "구분:": "구분: reasoning=근거를 따라 따지는 사고 / intuition=설명 전 먼저 오는 감",
        },
        "recognition": {
            "구분:": "구분: recognition=보고 알아봄 / recall=단서 없이 떠올림",
        },
        "self-control": {
            "구분:": "구분: self-control=충동을 눌러 버티는 힘 / self-regulation=행동과 감정을 스스로 조절하는 과정",
        },
        "self-regulation": {
            "구분:": "구분: self-regulation=상태를 스스로 조절하는 과정 / self-control=충동을 참는 힘",
        },
        "strain": {
            "구분:": "구분: strain=지속 압박에서 오는 긴장 / stress=스트레스 일반",
        },
        "temperament": {
            "구분:": "구분: temperament=타고난 기질 / personality=전반적 성격",
        },
        "tendency": {
            "구분:": "구분: tendency=반복적으로 기우는 경향 / trend=집단이나 수치의 흐름",
        },
        "uncertainty": {
            "구분:": "구분: uncertainty=확신할 수 없음 / risk=손실 가능성을 안고 있음",
        },
        "confidence": {
            "구분:": "구분: confidence=해낼 수 있다는 자신감 / certainty=사실이라고 보는 확실성",
        },
        "expectancy": {
            "부가 뜻:": "부가 뜻: 행동이 결과로 이어질 거라는 기대",
            "구분:": "구분: expectancy=행동과 결과의 연결 기대 / expectation=앞으로 일어날 예상",
        },
        "frustration": {
            "구분:": "구분: frustration=막혀서 생기는 좌절감 / disappointment=기대가 깨진 실망",
        },
        "inhibition": {
            "구분:": "구분: inhibition=반응에 브레이크를 거는 억제 / restraint=행동을 스스로 절제함",
        },
        "intuition": {
            "구분:": "구분: intuition=설명 전 먼저 오는 직감 / reasoning=근거를 따라 따지는 사고",
        },
        "persuasion": {
            "구분:": "구분: persuasion=상대 생각을 설득으로 바꿈 / coercion=강제로 따르게 함",
        },
        "reinforcement": {
            "부가 뜻:": "부가 뜻: 행동을 더 자주 나오게 만드는 자극",
            "구분:": "구분: reinforcement=행동을 강화하는 결과 / reward=그 결과로 주어지는 보상",
        },
        "reward": {
            "구분:": "구분: reward=행동 뒤에 주어지는 보상 / reinforcement=행동을 굳히는 강화 효과",
        },
        "vigilance": {
            "구분:": "구분: vigilance=계속 깨어 살피는 경계 / awareness=알아차림 상태",
        },
        "workload": {
            "부가 뜻:": "부가 뜻: 처리해야 할 과제 부담",
            "구분:": "구분: workload=맡은 일의 양 / difficulty=일의 난이도",
        },
        "impulse": {
            "구분:": "구분: impulse=생각 전에 튀는 충동 / intention=하려고 정한 의도",
        },
        "pattern": {
            "구분:": "구분: pattern=반복되는 결이나 규칙 / trend=시간 따라 움직이는 방향",
        },
        "risk": {
            "구분:": "구분: risk=손실 가능성을 안은 위험 / uncertainty=결과를 확신할 수 없음",
        },
        "drive": {
            "구분:": "구분: drive=행동을 밀어붙이는 추진력 / impulse=순간 충동 / motivation=동기",
        },
        "engagement": {
            "구분:": "구분: engagement=활동에 실제로 붙어 있는 참여와 몰입 / commitment=계속 책임지려는 헌신",
        },
        "exposure": {
            "부가 뜻:": "부가 뜻: 자극이나 환경에 접하는 경험",
            "구분:": "구분: exposure=무언가에 접하는 상태 / experience=겪어 얻은 경험",
        },
        "flexibility": {
            "구분:": "구분: flexibility=상황에 따라 바꿀 수 있는 유연성 / stability=쉽게 안 흔들리는 안정성",
        },
        "independence": {
            "구분:": "구분: independence=남에게 덜 기대는 독립성 / autonomy=스스로 결정하는 자율성",
        },
        "mood": {
            "구분:": "구분: mood=한동안 이어지는 기분 상태 / emotion=순간적으로 올라오는 감정",
        },
        "restraint": {
            "구분:": "구분: restraint=행동을 눌러 절제함 / inhibition=반응이 막히는 억제",
        },
    },
    "toefl_ets_2026_set_21.tsv": {
        "civic-minded": {
            "구분:": "구분: civic-minded=공동체 이익까지 생각하는 / self-interested=자기 이익 중심의",
        },
        "cross-cultural": {
            "구분:": "구분: cross-cultural=서로 다른 문화권 사이의 / intracultural=한 문화권 내부의",
        },
        "cross-sector": {
            "구분:": "구분: cross-sector=공공·민간 등 다른 부문을 가로지르는 / within-sector=한 부문 내부의",
        },
    },
    "toefl_ets_2026_set_22.tsv": {
        "conservation-oriented": {
            "구분:": "구분: conservation-oriented=자원을 보전하는 쪽 / extraction-focused=자원 채취를 앞세우는 쪽",
        },
        "restoration-oriented": {
            "구분:": "구분: restoration-oriented=훼손된 것을 되살리는 쪽 / conservation-oriented=있는 것을 지키는 쪽",
        },
        "climate-proof": {
            "구분:": "구분: climate-proof=미래 기후 위험까지 반영해 버티게 한 / weather-resilient=기상 충격을 견디는",
        },
        "sustainability-oriented": {
            "구분:": "구분: sustainability-oriented=오래 유지될 균형을 우선하는 / short-term=단기 성과 중심의",
        },
        "future-proofing": {
            "구분:": "구분: future-proofing=앞으로의 변화에도 버티게 미리 설계함 / maintenance=현재 상태를 유지함",
        },
    },
}


REPLACEMENTS: dict[str, dict[str, str]] = {
    "toefl_ets_2026_set_05.tsv": {
        "sanction": (
            "핵심 뜻: 제재 / 승인\n"
            "부가 뜻: 공식 허가를 내리다\n"
            "핵심 느낌: 공적 권한이 허용하거나 벌을 주는 식으로 힘을 행사하는 느낌\n"
            "구분: sanction=제재 또는 공식 승인 / penalty=벌 / approve=승인하다"
        ),
    },
    "toefl_ets_2026_set_24.tsv": {
        "cluster": (
            "핵심 뜻: 군집\n"
            "핵심 느낌: 비슷한 점들이 한 덩어리로 모이는 느낌\n"
            "구분: cluster=가까이 모인 군집 / category=개념상 묶은 범주"
        ),
        "dispersion": (
            "핵심 뜻: 산포\n"
            "핵심 느낌: 데이터가 넓게 퍼졌는지 좁게 모였는지 보는 느낌\n"
            "구분: dispersion=퍼짐 정도 / concentration=한곳에 모임"
        ),
        "sensitivity": (
            "핵심 뜻: 민감도\n"
            "부가 뜻: 실제 양성을 놓치지 않고 잘 잡아내는 정도\n"
            "핵심 느낌: 작은 신호도 놓치지 않고 반응하는 힘\n"
            "구분: sensitivity=양성을 잘 잡아내는 능력 / specificity=음성을 잘 가려 내는 능력"
        ),
        "specificity": (
            "핵심 뜻: 특이성\n"
            "부가 뜻: 실제 음성을 양성으로 잘못 잡지 않는 정도\n"
            "핵심 느낌: 아무거나 잡지 않고 목표가 아닌 것은 걸러 내는 힘\n"
            "구분: specificity=음성을 제대로 가려 내는 능력 / sensitivity=양성을 잘 잡아내는 능력"
        ),
        "slope": (
            "핵심 뜻: 기울기\n"
            "부가 뜻: 변화선이 얼마나 가파르게 움직이는지\n"
            "핵심 느낌: 선이 위아래로 얼마나 비스듬한지 보는 느낌\n"
            "구분: slope=선의 기울기 / trend=전체 방향"
        ),
        "plateau": (
            "핵심 뜻: 정체 구간\n"
            "핵심 느낌: 오르던 선이 꼭대기에서 납작해지는 느낌\n"
            "구분: plateau=상승이 멈춘 평평한 구간 / peak=가장 높은 한 점"
        ),
        "uptrend": (
            "핵심 뜻: 상승 추세\n"
            "부가 뜻: 시간이 갈수록 전반적으로 올라가는 흐름\n"
            "핵심 느낌: 그래프가 대체로 위로 방향을 잡는 느낌\n"
            "구분: uptrend=전반적 상승 흐름 / spike=짧은 급등"
        ),
        "downtrend": (
            "핵심 뜻: 하락 추세\n"
            "부가 뜻: 시간이 갈수록 전반적으로 내려가는 흐름\n"
            "핵심 느낌: 그래프가 대체로 아래로 향하는 느낌\n"
            "구분: downtrend=전반적 하락 흐름 / dip=일시적 하락"
        ),
        "trendline": (
            "핵심 뜻: 추세선\n"
            "부가 뜻: 여러 점의 전체 방향을 요약해 그은 선\n"
            "핵심 느낌: 흩어진 점들 위에 큰 방향선을 얹는 느낌\n"
            "구분: trendline=전체 방향을 잇는 선 / baseline=비교 기준선"
        ),
        "timepoint": (
            "핵심 뜻: 측정 시점\n"
            "부가 뜻: 데이터를 기록한 특정 시간 지점\n"
            "핵심 느낌: 긴 시간축 위에 콕 찍은 관찰 시점"
        ),
        "increment": (
            "핵심 뜻: 증가분\n"
            "부가 뜻: 단계적으로 늘어난 작은 변화량\n"
            "핵심 느낌: 한 칸씩 더해지는 작은 상승 단위\n"
            "구분: increment=작게 늘어난 한 단계 / increase=증가 일반"
        ),
        "decrement": (
            "핵심 뜻: 감소분\n"
            "부가 뜻: 단계적으로 줄어든 작은 변화량\n"
            "핵심 느낌: 한 칸씩 덜어지는 작은 감소 단위\n"
            "구분: decrement=작게 줄어든 한 단계 / decrease=감소 일반"
        ),
        "subset": (
            "핵심 뜻: 부분집합\n"
            "부가 뜻: 전체 데이터에서 특정 기준으로 떼어 낸 일부\n"
            "핵심 느낌: 큰 집합 안에서 조건 맞는 조각만 따로 꺼내는 느낌\n"
            "구분: subset=전체에서 떼어 낸 일부 / sample=관측을 위해 뽑은 표본"
        ),
        "datapoint": (
            "핵심 뜻: 데이터 점\n"
            "부가 뜻: 각 관측값 하나하나를 이루는 개별 값\n"
            "핵심 느낌: 그래프 위에 찍히는 한 점짜리 관측치\n"
            "구분: datapoint=개별 관측값 / metric=무엇을 재는 지표"
        ),
        "stratification": (
            "핵심 뜻: 층화\n"
            "핵심 느낌: 전체를 한 번에 보지 않고 층층이 갈라 보는 느낌\n"
            "구분: stratification=층별로 나눠 보는 구조 / segmentation=기준에 따라 잘게 나눈 구획"
        ),
        "confounding": (
            "핵심 뜻: 교란\n"
            "핵심 느낌: 겉으로 보이는 연결 사이에 다른 원인이 끼어드는 느낌\n"
            "구분: confounding=제3변수가 관계를 흐리는 교란 / bias=한쪽으로 기운 왜곡"
        ),
        "thresholding": (
            "핵심 뜻: 임계값 적용\n"
            "부가 뜻: 특정 기준선 이상·이하를 나누어 판정하다\n"
            "핵심 느낌: 선 하나를 그어 넘었는지 안 넘었는지 가르는 느낌\n"
            "구분: thresholding=기준선으로 갈라내기 / filtering=조건에 맞는 것만 걸러내기"
        ),
        "ranking": (
            "핵심 뜻: 순위화\n"
            "부가 뜻: 값이나 대상의 상대적 위치를 순서로 정하다\n"
            "핵심 느낌: 크고 작은 순으로 줄을 세워 위치를 매기는 느낌\n"
            "구분: ranking=순서를 매김 / rating=점수를 매김"
        ),
        "comparability": (
            "핵심 뜻: 비교 가능성\n"
            "핵심 느낌: 같은 눈금 위에 올려 비교해도 되는 상태\n"
            "구분: comparability=같은 기준으로 견줄 수 있음 / similarity=서로 닮아 있음"
        ),
        "acceleration": (
            "핵심 뜻: 가속\n"
            "부가 뜻: 증가나 변화 속도가 더 빨라지는 것\n"
            "핵심 느낌: 같은 방향 변화가 점점 더 빠르게 붙는 느낌\n"
            "구분: acceleration=변화 속도가 빨라짐 / increase=수준 자체가 늘어남"
        ),
        "breakdown": (
            "핵심 뜻: 세부 내역\n"
            "부가 뜻: 전체 수치를 항목별로 나누어 보여 준 정리\n"
            "핵심 느낌: 한 숫자 덩어리를 항목별 조각으로 풀어 놓은 표\n"
            "구분: breakdown=항목별로 쪼갠 내역 / total=전체 합계"
        ),
        "data-based": (
            "핵심 뜻: 자료 기반의\n"
            "부가 뜻: 주관보다 수집된 자료를 근거로 한\n"
            "핵심 느낌: 느낌보다 데이터 바닥 위에 올려 말하는 느낌\n"
            "구분: data-based=자료 근거의 / subjective=주관적"
        ),
    },
}


RENAMES: dict[str, dict[str, str]] = {
    "toefl_ets_2026_set_24.tsv": {
        "databased": "data-based",
    }
}


DELETIONS: dict[str, set[str]] = {
    "toefl_ets_2026_set_24.tsv": {"trendwise"},
}

REMOVE_LABELS: dict[str, dict[str, set[str]]] = {
    "toefl_ets_2026_set_24.tsv": {
        "upward": {"구분:"},
        "downward": {"구분:"},
        "comparability": {"구분:"},
        "uncorrelated": {"구분:"},
        "proportional": {"구분:"},
        "inverse": {"구분:"},
        "annualized": {"구분:"},
        "stabilization": {"구분:"},
        "attainment": {"구분:"},
        "observability": {"구분:"},
        "approximately": {"구분:"},
        "roughly": {"구분:"},
        "consistently": {"구분:"},
        "systematically": {"구분:"},
        "sequentially": {"구분:"},
        "tentatively": {"구분:"},
        "marginally": {"구분:"},
        "unevenly": {"구분:"},
        "erratically": {"구분:"},
        "intermittently": {"구분:"},
    }
}


def apply_changes(path: Path) -> bool:
    changed = False
    rows = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row in reader:
            if len(row) != 2:
                rows.append(row)
                continue

            headword, back = row
            if headword in DELETIONS.get(path.name, set()):
                changed = True
                continue

            headword = RENAMES.get(path.name, {}).get(headword, headword)

            if headword in REPLACEMENTS.get(path.name, {}):
                back = REPLACEMENTS[path.name][headword]
                changed = True
            else:
                lines = parse_back(back)
                if headword in REMOVE_LABELS.get(path.name, {}):
                    for label in REMOVE_LABELS[path.name][headword]:
                        if label in lines:
                            del lines[label]
                            changed = True
                if headword in ADDITIONS.get(path.name, {}):
                    for label, content in ADDITIONS[path.name][headword].items():
                        lines[label] = content
                    changed = True
                back = build_back(lines)

            rows.append([headword, back])

    if changed:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerows(rows)
    return changed


def main() -> int:
    changed_files = []
    for name in sorted(
        set(ADDITIONS) | set(REPLACEMENTS) | set(RENAMES) | set(DELETIONS) | set(REMOVE_LABELS)
    ):
        path = ROOT / name
        if apply_changes(path):
            changed_files.append(name)
    print(f"changed_files={len(changed_files)}")
    for name in changed_files:
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
