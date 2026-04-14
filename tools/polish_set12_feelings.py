#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "toefl_ets_2026_set_12.tsv"

FEELINGS = {
    "awareness": "이미 있던 걸 의식 위로 올려 알아차리는 상태",
    "arousal": "몸과 마음이 확 깨어 긴장이 올라간 상태",
    "attachment": "대상과 정서적으로 단단히 붙어 있는 상태",
    "aversion": "싫어서 본능적으로 멀리하고 싶은 마음",
    "behavioral": "생각보다 실제 행동에서 드러나는 쪽",
    "belief": "사실처럼 굳게 받아들이는 마음속 전제",
    "burnout": "오래 버티다 에너지가 다 타버린 상태",
    "concentration": "흩어진 주의를 한 점에 모으는 상태",
    "conformity": "튀지 않으려 다수 기준에 맞추는 쪽",
    "curiosity": "모르는 걸 그냥 못 지나가게 하는 마음",
    "deliberation": "바로 반응하지 않고 한 번 더 따져보는 상태",
    "dependency": "혼자보다 바깥 대상에 기대는 상태",
    "distraction": "해야 할 일에서 주의가 새는 상태",
    "emotion": "생각보다 먼저 올라오는 마음의 반응",
    "empathy": "남의 감정을 내 쪽에서 같이 느끼는 상태",
    "expectation": "아직 오지 않은 결과를 미리 그려두는 상태",
    "framing": "같은 내용도 어떤 틀로 보여주느냐의 문제",
    "gratification": "원하던 것이 채워져 바로 오는 만족",
    "habit": "반복 끝에 거의 자동으로 나오는 패턴",
    "identity": "나는 어떤 사람인가를 묶는 중심감",
    "impulsive": "생각보다 반응이 먼저 튀어나오는 쪽",
    "intention": "그냥 생각이 아니라 하려는 방향이 선 마음",
    "judgment": "이것이 맞는지 가르는 머릿속 판정",
    "learning": "경험이 남아서 다음 행동이 달라지는 상태",
    "memory": "지나간 정보가 머릿속에 남아 있는 상태",
    "mindfulness": "딴생각보다 지금 이 순간에 주의를 두는 상태",
    "misconception": "맞다고 믿지만 실제로는 빗나간 생각",
    "aspiration": "지금보다 더 높은 곳을 향해 끌리는 마음",
    "personality": "사람마다 비교적 오래 가는 반응의 결",
    "preference": "여러 선택지 중 이쪽이 더 끌리는 쪽",
    "priming": "먼저 받은 자극이 뒤 판단에 몰래 영향 주는 상태",
    "reasoning": "근거를 이어 결론까지 밀고 가는 생각",
    "recognition": "본 것 가운데 익숙한 대상을 알아보는 순간",
    "self-control": "하고 싶은 걸 눌러 방향을 지키는 힘",
    "self-regulation": "감정과 행동의 세기를 스스로 조절하는 힘",
    "self-esteem": "스스로를 어느 정도 괜찮게 보는 감각",
    "strain": "계속 버티느라 안쪽에 힘이 과하게 걸린 상태",
    "temperament": "타고난 반응 속도와 감정 결",
    "tendency": "자꾸 같은 쪽으로 기우는 버릇",
    "uncertainty": "어느 쪽이 맞는지 딱 못 박기 어려운 상태",
    "willpower": "힘들어도 선택을 끝까지 붙드는 힘",
    "withdrawal": "관계나 활동에서 한발 물러나는 움직임",
    "attribution": "결과 원인을 어디에 돌릴지 정하는 해석",
    "avoidance": "마주치기 싫어 미리 비켜 가는 행동",
    "commitment": "쉽게 안 놓고 계속 책임지려는 묶임",
    "conditioning": "반복된 연결로 반응이 길들여지는 과정",
    "confidence": "해낼 수 있다는 쪽으로 마음이 선 상태",
    "coping": "스트레스가 와도 무너지지 않게 다루는 방식",
    "disengagement": "하던 일과 마음의 연결을 끊는 상태",
    "expectancy": "노력하면 이런 결과가 올 거라는 예상치",
    "fixation": "한 생각이나 대상에 지나치게 묶인 상태",
    "attentiveness": "작은 신호도 놓치지 않게 주의를 세운 상태",
    "frustration": "막혀서 힘은 드는데 풀리지 않는 답답함",
    "habituation": "같은 자극에 점점 덜 반응하게 되는 상태",
    "imitation": "남의 방식과 행동을 그대로 따라 하는 것",
    "inferential": "드러난 사실보다 단서에서 뜻을 끌어내는 쪽",
    "inhibition": "나오려는 반응에 브레이크를 거는 힘",
    "introspection": "시선을 밖보다 내 마음 안으로 돌리는 상태",
    "intuition": "설명 전에도 먼저 답 감이 오는 느낌",
    "optimism": "앞으로 잘 풀릴 쪽으로 기본값이 기우는 상태",
    "pessimism": "잘 안 될 쪽을 먼저 예상하는 상태",
    "persuasion": "남의 생각 방향을 슬쩍 돌려 놓는 힘",
    "rationalization": "진짜 이유보다 그럴듯한 이유를 붙이는 것",
    "reinforcement": "보상이나 결과로 행동을 더 굳히는 힘",
    "reward": "어떤 행동을 다시 하게 만드는 달콤한 대가",
    "rumination": "같은 생각을 빠져나오지 못하고 되씹는 상태",
    "situational": "사람 자체보다 놓인 상황 영향을 더 받는 쪽",
    "socialization": "사회 규칙을 몸에 익혀 가는 과정",
    "threat": "위험이 가까이 왔다고 느끼게 하는 신호",
    "vigilance": "방심하지 않고 계속 살피는 상태",
    "workload": "해야 할 일이 어깨 위에 쌓인 무게",
    "choice": "여러 길 중 하나를 집어 드는 순간",
    "impulse": "생각 전에 먼저 튀는 욕구",
    "meaning": "겉정보를 넘어 왜 중요한지 붙는 뜻",
    "pattern": "흩어진 것들 사이에서 반복되는 결",
    "risk": "잘못될 가능성을 안고 가는 상태",
    "self-directed": "남이 끌기보다 스스로 방향을 잡는 쪽",
    "goal-oriented": "과정보다 도착점에 더 눈이 가는 쪽",
    "task-focused": "사람보다 지금 해야 할 일에 시선이 모이는 쪽",
    "value-based": "편의보다 원칙과 가치 기준을 따르는 쪽",
    "uncertainty-reduction": "모르는 상태를 견디기보다 빨리 줄이려는 움직임",
    "agency": "내 선택으로 상황을 움직일 수 있다는 감각",
    "ambition": "현재선에 안주하지 않고 더 크게 노리는 마음",
    "appetite": "무언가를 더 원하고 끌리는 힘",
    "assertion": "주저하지 않고 내 입장을 앞으로 내미는 말",
    "association": "하나를 보면 다른 하나가 같이 떠오르는 연결",
    "calm": "흔들림이 줄고 안쪽이 가라앉은 상태",
    "delay": "바로 하지 않고 시간을 뒤로 미루는 움직임",
    "desire": "갖고 싶고 이루고 싶은 쪽으로 당기는 힘",
    "discipline": "충동보다 기준을 따라 움직이게 하는 힘",
    "drive": "안에서 계속 앞으로 밀어붙이는 추진력",
    "engagement": "거리 두지 않고 적극적으로 안으로 들어가는 상태",
    "exposure": "자극이나 환경에 반복해서 닿는 상태",
    "fatigue": "에너지가 빠져 반응이 무거워진 상태",
    "flexibility": "한 방식에 고정되지 않고 바꿔 맞출 수 있는 힘",
    "independence": "남 기대지 않고 스스로 결정하는 상태",
    "instinct": "배우기 전에 거의 자동으로 나오는 반응",
    "mood": "한동안 바탕에 깔리는 감정 톤",
    "patience": "답답해도 서두르지 않고 버티는 힘",
    "restraint": "하고 싶어도 선을 넘지 않게 붙드는 힘",
}


def main() -> int:
    rows = []
    changed = 0
    with PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for headword, back in reader:
            lines = back.split("\n")
            updated = []
            for line in lines:
                if line.startswith("핵심 느낌:") and headword in FEELINGS:
                    updated.append(f"핵심 느낌: {FEELINGS[headword]}")
                    if line != updated[-1]:
                        changed += 1
                else:
                    updated.append(line)
            rows.append([headword, "\n".join(updated)])

    with PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    print(f"changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
