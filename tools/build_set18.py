from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_18.tsv"

CARDS = [
    ("argumentative", "논증적인 / 주장을 세워 전개하는", "입장과 근거를 연결해 설득하려는 성격의", "그냥 묘사보다 왜 그런지 밀고 나가는 말투", "argumentative=주장을 근거로 전개하는 / descriptive=상태를 묘사하는 / persuasive=상대를 설득하려는"),
    ("assertive", "단정적인 / 분명히 주장하는", "주저하지 않고 자기 입장을 선명하게 내세우는", "말끝을 흐리지 않고 앞으로 밀어붙이는 느낌", "assertive=자기 입장을 분명히 말하는 / tentative=조심스럽고 잠정적인 / aggressive=공격적으로 몰아붙이는"),
    ("backing", "뒷받침 / 지지 근거", "주장이나 해석이 버틸 수 있게 뒤에서 받쳐 주는 근거", "앞에 세운 말을 뒤에서 받쳐주는 받침대", "backing=주장을 뒷받침하는 근거 / support=지지 일반 / evidence=실제 근거 자료"),
    ("caveat", "단서 / 주의 조건", "주장이나 해석을 그대로 밀기 전에 붙이는 제한 조건이나 유보", "맞는 말이라도 이 조건은 조심하라고 옆에 다는 브레이크", "caveat=제한이나 주의 단서 / qualification=주장을 한정하는 보완 조건 / warning=위험을 알리는 경고"),
    ("coherently", "일관성 있게 / 앞뒤가 맞게", "생각이나 설명이 흩어지지 않고 논리적으로 이어지게", "문장들이 따로 놀지 않고 한 줄로 물려 가는 느낌", "coherently=논리적으로 이어지게 / consistently=기준이 흔들리지 않게 / randomly=무작위로"),
    ("counterargument", "반론 / 반대 논거", "기존 주장에 맞서 다른 결론이나 해석을 미는 논점", "한쪽 주장만 두지 않고 반대편에서 치고 들어오는 논리", "counterargument=기존 주장에 맞서는 반론 / objection=동의하지 않는 반대 제기 / rebuttal=반론을 다시 반박함"),
    ("counterevidence", "반대 증거 / 상충하는 근거", "현재 주장과 잘 맞지 않거나 그 주장을 약하게 만드는 자료", "내 말과 반대 방향으로 무게를 싣는 근거", "counterevidence=주장과 충돌하는 근거 / evidence=근거 일반 / anomaly=예상과 다른 이상 사례"),
    ("critique", "비판적 검토 / 논평하다", "대상을 무조건 깎는 게 아니라 강점과 약점을 따져 평가하는 분석", "겉만 칭찬하지 않고 어디가 약한지 구조를 뜯어보는 느낌", "critique=근거를 들어 비판적으로 검토하다 / criticize=비판하다 / review=전반적으로 검토하다"),
    ("debatable", "논쟁의 여지가 있는", "하나의 결론으로 쉽게 닫히지 않고 다른 해석이나 반론이 가능한", "딱 끝난 답이 아니라 더 따져볼 구멍이 남은 느낌", "debatable=논쟁 가능성이 있는 / controversial=입장이 크게 갈리는 / uncertain=확실하지 않은"),
    ("defensible", "옹호 가능한 / 근거로 방어 가능한", "비판이 들어와도 논리와 근거로 어느 정도 버틸 수 있는", "공격받아도 쉽게 무너지지 않게 이유를 세울 수 있는 느낌", "defensible=근거로 옹호 가능한 / justified=타당한 이유가 있는 / vulnerable=비판에 취약한"),
    ("disputable", "이의를 제기할 수 있는 / 반박 가능한", "사실이나 해석이 확정적이지 않아 반대 주장이 들어올 수 있는", "그냥 받아들이기엔 아직 다툴 여지가 열린 느낌", "disputable=반박·이의 제기가 가능한 / questionable=의심스러운 / conclusive=결론이 확실한"),
    ("emphatic", "강조하는 / 단호한", "어떤 점을 특별히 강하게 드러내며 말하는", "여기는 그냥 지나치지 말라고 말의 힘을 세게 싣는 느낌", "emphatic=강하게 강조하는 / neutral=중립적인 / restrained=절제된"),
    ("evidentiary", "증거상의 / 근거 자료와 관련된", "주장 자체보다 그 주장을 받치는 자료와 증명력에 관한", "말의 느낌보다 증거가 얼마나 받치느냐를 보는 쪽", "evidentiary=증거와 증명력에 관한 / interpretive=해석과 관련된 / rhetorical=표현과 설득 방식의"),
    ("explanatory power", "설명력 / 현상을 잘 풀어내는 힘", "한 이론이나 해석이 얼마나 많은 사실을 설득력 있게 설명하는지의 힘", "여러 퍼즐 조각을 하나의 이유로 잘 묶어내는 힘", "explanatory power=현상을 넓고 설득력 있게 설명하는 힘 / accuracy=정확성 / coverage=포괄 범위"),
    ("foreground", "앞세우다 / 두드러지게 놓다", "많은 요소 중 특정 쟁점이나 해석을 전면에 놓아 강조하다", "배경에 묻히지 않게 화면 맨 앞으로 끌어내는 느낌", "foreground=특정 요소를 전면에 강조하다 / emphasize=강조하다 / background=뒤쪽 맥락으로 물리다"),
    ("generalization", "일반화 / 넓은 결론으로 확장", "몇몇 사례에서 더 넓은 범위의 규칙이나 결론을 끌어내는 일", "작은 사례들을 모아 더 큰 규칙처럼 넓혀 말하는 느낌", "generalization=사례를 넓은 결론으로 확장함 / inference=근거에서 결론을 끌어냄 / oversimplification=너무 단순하게 일반화함"),
    ("hedge", "단정 수위를 낮추다 / 유보 표현을 쓰다", "너무 강하게 확정하지 않고 가능성이나 조건을 남겨 말하다", "말을 끝까지 못 박지 않고 살짝 여지를 남기는 느낌", "hedge=단정을 완화해 말하다 / qualify=조건을 붙여 한정하다 / assert=분명히 주장하다"),
    ("illustrative", "예시가 되는 / 설명을 돕는", "추상적 논점을 구체적으로 보여주는 사례 역할을 하는", "말만으로 흐린 부분을 한 장면으로 보여주는 느낌", "illustrative=논점을 보여주는 예시적 / representative=전체를 어느 정도 대표하는 / decorative=장식적인"),
    ("implausible", "그럴듯하지 않은 / 믿기 어려운", "근거나 상식, 맥락에 비춰 볼 때 설득력이 약한", "말은 되는데 곰곰이 보면 쉽게 믿기 어려운 느낌", "implausible=설득력 있게 믿기 어려운 / unlikely=가능성이 낮은 / invalid=타당하지 않은"),
    ("inconsistency", "불일치 / 앞뒤가 안 맞음", "같은 주장이나 자료 안에서 기준·내용·결론이 서로 어긋남", "한쪽 말과 다른 쪽 말이 서로 물리지 않고 삐걱대는 느낌", "inconsistency=내용이나 기준이 서로 어긋남 / contradiction=정면으로 충돌하는 모순 / discrepancy=수치나 진술의 차이"),
    ("infer", "추론하다 / 근거로 짐작하다", "직접 말하지 않은 결론을 자료와 맥락에서 끌어내다", "겉에 안 적힌 답을 남은 단서로 이어서 뽑아내는 느낌", "infer=근거로 결론을 끌어내다 / assume=충분히 확인 없이 가정하다 / deduce=원리에서 논리적으로 도출하다"),
    ("interpretive lens", "해석의 틀 / 바라보는 관점", "같은 자료를 어떤 기준과 관점으로 읽을지 정하는 해석 프레임", "있는 그대로 하나만 보는 게 아니라 어떤 안경을 끼고 읽는지의 문제", "interpretive lens=자료를 읽는 관점의 틀 / framework=구조적 틀 / bias=한쪽으로 기울어진 편향"),
    ("line of reasoning", "논리 전개 / 이유를 잇는 흐름", "주장에서 결론까지 근거와 판단이 어떻게 이어지는지의 연결선", "한 문장씩 따로가 아니라 이유가 줄줄이 이어지는 길", "line of reasoning=근거가 이어지는 논리 흐름 / argument=주장과 논거 묶음 / narrative=이야기식 서술"),
    ("misinterpret", "잘못 해석하다", "자료나 발언의 의미를 맥락과 다르게 읽어 잘못 이해하다", "같은 문장을 보고 방향을 엉뚱하게 잡는 느낌", "misinterpret=의미를 잘못 해석하다 / misunderstand=잘못 이해하다 일반 / distort=의미를 비틀다"),
    ("nuanced", "미묘한 차이를 살린 / 정교한", "단순한 찬반보다 여러 층의 차이와 조건을 세밀하게 반영한", "흑백으로 자르지 않고 중간의 결을 읽는 느낌", "nuanced=미묘한 차이까지 반영한 / subtle=차이가 섬세한 / simplistic=지나치게 단순한"),
    ("objectivity claim", "객관성 주장 / 중립적 근거를 내세움", "자기 입장이 아니라 자료와 기준이 중립적이라고 내세우는 주장", "내 생각이 아니라 사실대로 본다고 앞에 방패를 세우는 느낌", "objectivity claim=객관적이라고 내세우는 주장 / evidence claim=근거에 기대는 주장 / opinion=개인 의견"),
    ("overgeneralize", "과도하게 일반화하다", "일부 사례나 제한된 근거를 너무 넓은 결론으로 확장하다", "작은 표본 하나로 세상 전체를 다 말해버리는 느낌", "overgeneralize=근거보다 너무 넓게 일반화하다 / generalize=일반화하다 / exaggerate=과장하다"),
    ("overstate", "과장해 말하다 / 실제보다 강하게 주장하다", "근거나 실제 범위보다 결론이나 효과를 더 크게 말하다", "있던 사실보다 말의 볼륨을 한 단계 키우는 느낌", "overstate=실제보다 강하게 말하다 / exaggerate=과장하다 / emphasize=중요성을 강조하다"),
    ("paraphrase", "바꿔 말하다 / 의역하다", "원래 의미는 유지하면서 다른 표현으로 다시 말하다", "같은 뜻을 복붙하지 않고 내 문장으로 다시 옮기는 느낌", "paraphrase=뜻을 살려 다른 말로 바꾸다 / quote=원문 그대로 인용하다 / summarize=핵심만 줄여 말하다"),
    ("plausibility", "그럴듯함 / 개연성", "근거와 맥락에 비춰 설명이나 주장이 얼마나 말이 되는지의 정도", "완벽 증명은 아니어도 그럴 법하다고 고개가 끄덕여지는 느낌", "plausibility=설명이 그럴듯한 정도 / probability=확률 / credibility=믿을 만함"),
    ("positioning", "입장 설정 / 어떤 관점에 놓기", "대상이나 주장을 어떤 역할과 관점 안에 배치해 보이게 하는 방식", "같은 내용도 어디에 세워두느냐로 다르게 읽히는 느낌", "positioning=어떤 입장·자리로 배치해 보이게 함 / framing=해석 틀을 씌움 / classification=범주로 나눔"),
    ("premise", "전제 / 논의의 출발점", "주장이나 결론이 기대고 있는 기본 가정이나 조건", "뒤 결론을 세우기 전에 바닥에 먼저 깔아두는 문장", "premise=논증이 출발하는 전제 / assumption=가정 / conclusion=최종 결론"),
    ("presuppose", "전제로 깔다 / 미리 가정하다", "명시적으로 따지기 전에 어떤 사실이나 조건이 이미 맞다고 깔고 들어가다", "말을 시작하기 전에 이건 이미 맞다고 바닥에 깔아두는 느낌", "presuppose=이미 사실로 전제하다 / assume=가정하다 / imply=간접적으로 시사하다"),
    ("rebut", "반박하다 / 논리로 되받다", "상대 주장이나 비판이 틀렸다고 근거를 들어 맞받아치다", "그 말을 그대로 두지 않고 증거를 들고 되치기하는 느낌", "rebut=근거를 들어 반박하다 / refute=틀렸음을 입증하며 논파하다 / disagree=동의하지 않다"),
    ("reframe", "틀을 다시 짜다 / 다른 관점으로 다시 제시하다", "같은 사안을 다른 해석 틀이나 문제 설정으로 다시 보여주다", "내용 자체보다 보는 프레임을 바꿔 다른 의미로 보이게 하는 느낌", "reframe=해석의 틀을 다시 설정하다 / reinterpret=다시 해석하다 / revise=내용을 고쳐 쓰다"),
    ("rhetorical", "수사적인 / 표현 방식으로 설득하는", "내용 자체뿐 아니라 말의 구성과 어조로 효과를 내는", "무엇을 말하느냐 못지않게 어떻게 말하느냐를 쓰는 느낌", "rhetorical=표현 방식과 설득 효과의 / argumentative=논증적인 / stylistic=문체와 관련된"),
    ("salience", "두드러짐 / 눈에 띄는 중요성", "여러 정보 중 특히 강하게 주목되고 중요하게 보이는 정도", "많은 점들 중 유난히 앞으로 튀어나와 보이는 느낌", "salience=특히 눈에 띄고 중요하게 보임 / prominence=두드러진 위치 / relevance=관련성"),
    ("scholarly", "학술적인 / 연구자답게 근거를 갖춘", "일상적 인상보다 자료, 논의, 인용, 분석을 갖춘 학문적 성격의", "가볍게 말하기보다 근거와 출처를 챙겨 조심스럽게 다듬은 느낌", "scholarly=학술적이고 연구 기반의 / academic=학문적인 / casual=가벼운 일상적"),
    ("source-based", "출처 기반의 / 자료에 근거한", "개인 인상보다 문서·자료·근거 출처를 바탕으로 한", "내 말보다 어디서 가져왔는지 근거 줄을 붙여 세우는 느낌", "source-based=출처와 자료에 근거한 / evidence-based=검증된 근거에 기반한 / opinion-based=개인 의견 중심의"),
    ("stance", "입장 / 관점의 위치", "어떤 쟁점에 대해 어느 방향으로 보고 판단하는지의 태도", "논쟁판에서 내가 어느 쪽 발판 위에 서 있는지", "stance=쟁점에 대한 입장과 관점 / position=놓인 자리나 입장 / attitude=태도"),
    ("substantiated", "근거로 뒷받침된 / 입증된", "주장이나 설명이 자료와 논거로 어느 정도 받쳐진", "말만 세게 한 게 아니라 아래에 근거 기둥이 박힌 느낌", "substantiated=근거로 뒷받침된 / supported=지지받는 / speculative=추측성의"),
    ("textual evidence", "본문 근거 / 텍스트 속 증거", "글 안의 구체적 표현이나 정보에서 끌어온 근거", "밖에서 감으로 말하지 않고 문장 안에서 집어 올린 증거", "textual evidence=본문에서 찾은 구체적 근거 / citation=출처 표기 / interpretation=의미 해석"),
    ("thematic", "주제 중심의 / 반복되는 의미축과 관련된", "개별 사실보다 여러 부분을 관통하는 큰 주제나 의미 흐름과 관련된", "자잘한 조각 아래를 관통하는 중심 주제선을 보는 느낌", "thematic=반복되는 주제와 의미축의 / topical=주제와 관련된 / structural=구조적인"),
    ("thesis", "핵심 주장 / 논지", "글이나 발표 전체를 밀고 가는 중심 주장", "여러 근거와 단락이 결국 받치고 있는 큰 주장 기둥", "thesis=글의 중심 논지 / claim=개별 주장 / topic=다루는 주제"),
    ("traceable claim", "추적 가능한 주장 / 근거를 따라갈 수 있는 주장", "결론이 어디서 나왔는지 자료와 논리 경로를 따라 확인할 수 있는 주장", "주장 뒤를 따라가면 근거 발자국이 남아 있는 느낌", "traceable claim=근거 출처와 논리 경로를 따라갈 수 있는 주장 / assertion=단정적 주장 / speculation=추측"),
    ("understate", "축소해 말하다 / 실제보다 약하게 표현하다", "의미나 규모, 중요성을 실제보다 덜한 것처럼 말하다", "있는 무게보다 말의 볼륨을 일부러 낮추는 느낌", "understate=실제보다 약하게 말하다 / downplay=중요성을 낮춰 보이게 하다 / overstate=과하게 말하다"),
    ("warranted", "정당화되는 / 근거상 타당한", "주어진 근거와 조건에 비춰 그 결론이나 판단이 무리 없이 받아들여지는", "그렇게 말해도 될 만큼 이유가 충분히 받쳐주는 느낌", "warranted=근거상 정당화되는 / justified=타당한 이유가 있는 / arbitrary=임의적인"),
    ("analytical stance", "분석적 입장 / 따져보는 관점", "현상을 그냥 받아들이기보다 구조와 근거를 나눠 보려는 관점", "감상보다 무엇이 어떻게 작동하는지 뜯어보는 쪽에 선 자세", "analytical stance=분석 중심으로 보는 입장 / evaluative stance=가치를 판단하는 입장 / neutral stance=중립적 입장"),
    ("claim-evidence link", "주장-근거 연결 / 논거 연결선", "제시한 결론이 어떤 자료와 이유를 통해 이어지는지의 논리 연결", "주장만 따로 떠 있지 않게 아래 근거와 선을 이어주는 고리", "claim-evidence link=주장과 근거를 잇는 논리 연결 / line of reasoning=이유 전개 흐름 / citation=출처 표기"),
    ("conceptual framing", "개념적 틀짓기 / 문제를 어떤 개념으로 잡는가", "현상을 어떤 개념과 범주로 놓고 해석할지 정하는 방식", "같은 현실도 어떤 개념 그릇에 담느냐에 따라 다르게 보이는 느낌", "conceptual framing=개념 틀로 문제를 잡는 방식 / positioning=어떤 자리와 관점에 놓기 / labeling=이름 붙이기"),
    ("evidence hierarchy", "증거 위계 / 근거의 강도 순서", "근거 자료를 얼마나 직접적이고 믿을 만한지에 따라 층위로 나누는 기준", "모든 자료를 똑같이 보지 않고 더 센 근거와 약한 근거를 줄 세우는 느낌", "evidence hierarchy=증거의 강도와 신뢰도를 층위화함 / credibility=믿을 만함 / ranking=순위 매김"),
    ("explanatory gap", "설명 공백 / 이유가 비는 부분", "주장이나 이론이 어떤 현상이나 단계는 충분히 설명하지 못하고 남긴 빈틈", "말은 이어지는데 왜 그런지 한 구간이 툭 비어 있는 느낌", "explanatory gap=설명이 충분히 닿지 않는 빈틈 / ambiguity=모호함 / contradiction=모순"),
    ("framing effect", "프레이밍 효과 / 제시 방식에 따라 판단이 달라짐", "같은 정보라도 어떤 틀과 표현으로 보여주느냐에 따라 해석과 선택이 달라지는 현상", "내용 하나가 아니라 포장과 틀이 판단의 방향을 살짝 바꾸는 느낌", "framing effect=제시 틀이 판단을 바꾸는 효과 / bias=한쪽으로 기울어짐 / interpretation=의미 해석"),
    ("line-by-line", "한 줄씩 / 세부를 따라가며", "글이나 논리를 전체 인상만이 아니라 순서대로 세밀하게 따라가며 보는", "덩어리로 뭉뚱그리지 않고 문장을 하나씩 짚어가는 느낌", "line-by-line=한 줄씩 차례로 세밀하게 / holistic=전체를 함께 보는 / skimmed=대충 훑은"),
    ("perspectival", "관점에 따른 / 보는 위치에 좌우되는", "무엇을 어디서 보느냐에 따라 해석과 강조점이 달라지는", "같은 대상을 봐도 서 있는 자리와 렌즈에 따라 다르게 보이는 느낌", "perspectival=관점에 따라 달라지는 / objective=객관적인 / interpretive=해석과 관련된"),
    ("reading cue", "독해 단서 / 읽는 방향을 알려주는 신호", "다음 내용의 전환, 강조, 예시, 반론 등을 알아차리게 해주는 표현이나 구조", "문장 속에서 여기서 방향이 바뀐다고 알려주는 작은 표지판", "reading cue=독해 방향을 알려주는 단서 / signal word=논리 관계를 알리는 표현 / hint=힌트"),
    ("text-to-context", "본문을 맥락과 연결하는 / 텍스트-맥락 연결의", "문장 자체만 보지 않고 시대·상황·목적과 이어서 해석하는", "글 안 문장과 글 밖 배경을 선으로 이어 읽는 느낌", "text-to-context=본문 내용을 넓은 맥락과 연결함 / textual=텍스트 자체의 / contextual=맥락에 의존하는"),
    ("unsubstantiated", "근거가 부족한 / 입증되지 않은", "주장이 있는데 그 아래를 받치는 자료나 논거가 충분하지 않은", "말은 세워졌지만 밑받침이 비어 흔들리는 느낌", "unsubstantiated=근거가 충분히 뒷받침되지 않은 / unsupported=지지 근거가 없는 / substantiated=근거로 뒷받침된"),
    ("viewpoint shift", "관점 전환 / 보는 방향의 변화", "같은 문제를 다른 기준이나 입장으로 다시 보며 해석이 바뀌는 것", "서 있던 자리에서 한 걸음 옮기자 대상의 의미가 달리 보이는 느낌", "viewpoint shift=관점이 바뀌는 전환 / reframe=틀을 다시 짜다 / revision=고쳐 쓰기"),
    ("voice", "서술 목소리 / 글의 태도와 어조", "글쓴이나 화자가 어떤 거리감과 태도로 말하는지 드러나는 표현 성격", "내용 뒤에서 누가 어떤 톤으로 말하는지가 들리는 느낌", "voice=글이나 발화에 드러난 어조와 태도 / tone=정서적 말투 / stance=입장"),
    ("argument map", "논증 지도 / 주장과 근거의 구조도", "주장, 근거, 반론, 결론이 어떻게 연결되는지 한눈에 정리한 구조", "흩어진 문장을 선으로 엮어 논리 뼈대를 보이게 한 지도", "argument map=주장과 근거의 연결 구조도 / outline=큰 틀의 개요 / line of reasoning=논리 전개 흐름"),
    ("attributional", "귀인과 관련된 / 원인을 어디에 두는가의", "사건이나 결과의 원인을 어떤 주체나 조건에 돌리는 방식과 관련된", "무슨 일이 왜 생겼는지 화살표를 어디에 꽂는지 보는 느낌", "attributional=원인을 어디에 귀속하는지와 관련된 / causal=원인 관계의 / interpretive=해석과 관련된"),
    ("claim strength", "주장 강도 / 단정의 세기", "글쓴이가 결론을 얼마나 강하게 확신하며 밀고 있는지의 정도", "아마 그럴지도와 분명히 그렇다 사이에서 말의 힘이 어디쯤인지 보는 눈금", "claim strength=주장의 단정 수준 / certainty=확신 정도 / hedging=단정 완화"),
    ("contrastive", "대조적인 / 차이를 드러내는", "비슷하게 보이는 것들 사이의 차이를 분명히 보이게 하는", "나란히 놓고 어디가 다른지 선을 진하게 긋는 느낌", "contrastive=차이를 드러내는 / comparative=서로 견주어 보는 / analogous=비슷한 구조를 가진"),
    ("definitional", "정의와 관련된 / 개념 경계를 정하는", "어떤 용어나 개념이 정확히 무엇을 포함하고 제외하는지 정하는", "이 말이 어디까지를 뜻하는지 테두리를 긋는 느낌", "definitional=개념 정의와 경계 설정의 / descriptive=특성을 묘사하는 / conceptual=개념적"),
    ("evidence threshold", "증거 기준선 / 인정할 만한 근거 최소선", "어느 정도 근거가 있어야 결론이나 판단을 받아들일 수 있는지의 문턱", "이만큼 아래면 아직 부족하고 이 선을 넘어야 납득되는 느낌", "evidence threshold=결론을 받아들일 최소 근거선 / standard of proof=입증 기준 / threshold=문턱값"),
    ("exemplify", "예시로 보여주다 / 전형적으로 나타내다", "추상적 주장이나 범주를 구체적 사례로 잘 드러내다", "이 예 하나를 보면 그 말이 어떤 뜻인지 바로 보이게 하는 느낌", "exemplify=예로써 잘 보여주다 / illustrate=설명해 보여주다 / represent=대표하다"),
    ("interpretive bias", "해석 편향 / 한쪽으로 기운 읽기", "자료 자체보다 특정 관점이나 기대가 해석을 한 방향으로 밀어놓는 경향", "있는 그대로 읽는 줄 알지만 안경 색이 한쪽으로 물든 느낌", "interpretive bias=해석이 한 관점으로 기우는 경향 / bias=편향 일반 / viewpoint=관점"),
    ("persuasive force", "설득력 / 밀어붙이는 논리 힘", "주장이나 표현이 독자를 납득시키는 힘의 정도", "말이 그냥 떠 있지 않고 상대를 고개 끄덕이게 밀어주는 힘", "persuasive force=상대를 납득시키는 힘 / credibility=믿을 만함 / emphasis=강조"),
    ("premise-checking", "전제 점검 / 깔린 가정 검토", "결론을 보기 전에 그 아래 전제가 맞는지 따져보는 일", "위에 올라간 주장보다 먼저 바닥 가정이 튼튼한지 눌러보는 느낌", "premise-checking=전제가 맞는지 검토함 / critique=비판적 검토 / verification=맞는지 확인"),
    ("quote-heavy", "인용이 많은 / 직접 인용 중심의", "자기 설명보다 다른 출처의 문장을 많이 끌어와 세우는", "내 문장보다 남의 말 조각이 많이 박힌 글의 느낌", "quote-heavy=직접 인용이 많은 / source-based=출처 기반의 / paraphrased=바꿔 말한"),
    ("reason-giving", "이유를 제시하는 / 근거를 붙이는", "결론만 던지지 않고 왜 그런지 설명과 근거를 함께 내는", "말 뒤에 바로 왜냐하면의 다리를 붙이는 느낌", "reason-giving=이유와 근거를 제시하는 / assertive=분명히 주장하는 / descriptive=묘사하는"),
    ("rebuttal-ready", "반박에 대비된 / 되받을 근거가 있는", "비판이나 질문이 들어와도 다시 대응할 논리와 근거를 갖춘", "반대편 질문이 들어와도 바로 받쳐낼 방어선을 세워둔 느낌", "rebuttal-ready=반박에 대응할 준비가 된 / defensible=옹호 가능한 / vulnerable=비판에 취약한"),
    ("statement-level", "문장 단위의 / 진술 수준의", "글 전체 구조보다 개별 문장이나 진술 하나하나의 의미와 기능에 초점을 둔", "큰 단락보다 한 문장씩 떼어 그 말이 무슨 일을 하는지 보는 느낌", "statement-level=개별 진술 단위에 초점을 둔 / paragraph-level=단락 단위의 / holistic=전체적으로 보는"),
    ("text-centered", "본문 중심의 / 텍스트에 밀착한", "바깥 추측보다 글 안의 표현과 구조를 우선해서 해석하는", "상상으로 넓히기 전에 일단 문장 속 증거에 붙어 읽는 느낌", "text-centered=본문 표현과 구조에 밀착한 / context-driven=주변 맥락에 크게 기대는 / speculative=추측성의"),
    ("topic sentence", "주제문 / 단락의 중심 문장", "단락이 무엇을 말하려는지 핵심 방향을 먼저 잡아주는 문장", "뒤 문장들을 어디로 데려갈지 먼저 기둥을 세우는 문장", "topic sentence=단락 중심 주제를 잡는 문장 / thesis=글 전체 중심 논지 / supporting detail=뒷받침 세부 내용"),
    ("well-grounded", "근거가 탄탄한 / 바탕이 잘 선", "주장이나 해석이 충분한 자료와 논리 위에 놓여 쉽게 흔들리지 않는", "허공에 뜬 말이 아니라 바닥에 기초를 단단히 박은 느낌", "well-grounded=근거와 바탕이 탄탄한 / substantiated=근거로 뒷받침된 / speculative=추측성의"),
    ("argument chain", "논증 사슬 / 이유가 이어진 구조", "여러 근거와 판단이 순서대로 연결되어 결론을 받치는 구조", "한 고리씩 이어져 마지막 주장까지 당겨가는 느낌", "argument chain=근거들이 이어져 결론을 받치는 구조 / line of reasoning=논리 전개 흐름 / claim-evidence link=주장과 근거 연결"),
    ("claim qualifier", "주장 한정어 / 단정 수위를 조절하는 표현", "주장이 언제, 어느 정도, 어떤 조건에서만 맞는지 좁혀주는 표현", "말을 무조건 크게 두지 않고 적용 범위를 조이는 느낌", "claim qualifier=주장의 적용 범위를 한정하는 표현 / hedge=단정을 낮추는 표현 / caveat=주의 단서"),
    ("close reading", "정밀 독해 / 문장과 표현을 세밀히 읽기", "전체 인상보다 텍스트의 단어 선택과 구조를 자세히 따라가며 해석하는 읽기", "대충 줄거리보다 문장 결을 가까이 붙어 읽는 느낌", "close reading=표현과 구조를 세밀히 읽는 독해 / skim reading=대략 훑어보기 / text-centered=본문에 밀착한"),
    ("contextual cue", "맥락 단서 / 주변 문맥이 주는 힌트", "앞뒤 상황이나 표현에서 의미와 방향을 짐작하게 해주는 신호", "모르는 말을 홀로 보지 않고 주변 문장으로 방향을 잡는 느낌", "contextual cue=문맥에서 얻는 단서 / reading cue=독해 방향 신호 / clue=실마리"),
    ("counterclaim", "맞주장 / 반대 주장", "기존 주장과 다른 결론이나 해석을 세우는 반대편 주장", "한쪽 주장에 정면으로 다른 깃발을 세우는 느낌", "counterclaim=기존 주장에 맞서는 주장 / counterargument=반대 논거 / rebuttal=그 반대를 다시 반박함"),
    ("critical lens", "비판적 시각 / 따져보는 해석 틀", "대상을 그대로 받아들이지 않고 어떤 기준으로 문제점과 의미를 살피는 관점", "그럴듯한 말도 한 번 걸러 보게 하는 분석 안경", "critical lens=비판적으로 읽는 관점 / interpretive lens=해석의 틀 / bias=한쪽으로 기운 편향"),
    ("discursive", "담화적인 / 논의 흐름 속의", "개별 단어보다 발화와 논의의 전개 방식, 의미 구성과 관련된", "한 문장 조각보다 말들이 이어지며 논의를 만드는 흐름을 보는 느낌", "discursive=담화 전개와 의미 구성의 / textual=텍스트 자체의 / rhetorical=표현과 설득 방식의"),
    ("evidence-backed", "근거로 뒷받침된", "주장이나 설명이 자료와 사례에 의해 받쳐지는", "말만 띄운 게 아니라 아래에 증거를 깔고 선 느낌", "evidence-backed=근거가 붙어 있는 / substantiated=근거로 입증된 / unsupported=근거 없는"),
    ("explanatory frame", "설명 틀 / 원인을 묶는 프레임", "현상을 어떤 원리와 관계로 설명할지 잡아주는 개념적 구조", "여러 사실을 어느 이유틀에 넣어 읽을지 정하는 프레임", "explanatory frame=현상을 설명하는 개념 틀 / conceptual framing=개념적 틀짓기 / interpretation=해석"),
    ("fallacious", "오류를 담은 / 논리적으로 잘못된", "겉보기엔 그럴듯하지만 추론이나 근거 연결에 결함이 있는", "말은 이어지는 듯해도 중간 논리 고리가 잘못 끼워진 느낌", "fallacious=논리 오류가 있는 / invalid=타당하지 않은 / misleading=오해를 부르는"),
    ("interpretive range", "해석 범위 / 가능한 읽기의 폭", "한 텍스트나 자료를 타당하게 읽을 수 있는 여러 의미의 폭", "하나만 고정된 게 아니라 어디까지 다른 읽기가 가능한지 열린 폭", "interpretive range=가능한 해석의 범위 / ambiguity=여러 뜻으로 읽힐 여지 / scope=범위"),
    ("misleadingly", "오해를 부르게 / 잘못된 인상을 주며", "표현이나 제시 방식이 실제보다 다른 방향으로 이해를 끌고 가도록", "겉말이 독자를 엉뚱한 길로 슬쩍 몰고 가는 느낌", "misleadingly=잘못된 인상을 주며 / inaccurately=부정확하게 / deceptively=속이는 듯하게"),
    ("non sequitur", "앞뒤가 안 맞는 결론 / 논리 비약", "앞의 근거에서 자연스럽게 따라나오지 않는 결론이나 발언", "앞 고리와 안 물리는데 갑자기 다른 결론이 튀어나온 느낌", "non sequitur=근거에서 이어지지 않는 논리 비약 / contradiction=정면 모순 / irrelevance=관련 없음"),
    ("paraphrastic", "바꿔 말한 / 의역적인", "원래 뜻은 유지하되 다른 표현으로 다시 풀어 쓴", "복붙이 아니라 같은 뜻을 새 문장 껍질로 갈아입힌 느낌", "paraphrastic=같은 뜻을 다른 표현으로 옮긴 / quoted=원문 그대로 인용한 / summarized=핵심만 요약한"),
    ("persuasively", "설득력 있게 / 납득되게", "주장과 근거, 표현이 상대를 고개 끄덕이게 만들 만큼 잘 맞물리게", "말이 허공에 뜨지 않고 듣는 사람 쪽으로 힘 있게 들어가는 느낌", "persuasively=상대를 납득시키게 / convincingly=믿고 받아들일 만큼 / vaguely=흐릿하게"),
    ("reasoned", "숙고된 / 근거를 갖춘", "즉흥적 감정이 아니라 이유와 판단을 거쳐 정리된", "툭 던진 말이 아니라 이유를 밟아 다듬은 느낌", "reasoned=이유를 갖춘 숙고된 / impulsive=충동적인 / arbitrary=임의적인"),
    ("recontextualize", "새 맥락에 다시 놓다 / 맥락을 바꿔 재해석하다", "같은 자료나 발언을 다른 상황과 배경 안에 놓아 의미를 새로 읽다", "문장을 다른 배경 조명 아래 옮겨 다시 보게 하는 느낌", "recontextualize=새 맥락에 놓아 다시 해석하다 / reframe=틀을 다시 짜다 / reinterpret=다시 해석하다"),
    ("rhetorically", "수사적으로 / 설득 효과를 노리며", "정보 자체만이 아니라 표현과 구성의 효과를 활용해", "내용 전달을 넘어서 말의 배치로 상대 반응을 겨냥하는 느낌", "rhetorically=수사적 효과를 살려 / stylistically=문체상으로 / neutrally=중립적으로"),
    ("source-critical", "출처를 비판적으로 검토하는", "자료를 그대로 믿지 않고 출처의 신뢰도와 편향, 목적을 따져보는", "누가 왜 말했는지까지 같이 보고 근거를 걸러 읽는 느낌", "source-critical=출처 신뢰도와 편향을 비판적으로 검토하는 / source-based=출처에 근거한 / uncritical=그대로 받아들이는"),
    ("stance marker", "입장 표지 / 태도를 드러내는 표현", "글쓴이가 확신, 유보, 평가, 거리감을 어떻게 두는지 보여주는 표현", "문장 내용보다 말하는 사람이 어디 서 있는지 드러내는 작은 깃발", "stance marker=입장과 태도를 드러내는 표현 / signal word=논리 관계를 알리는 표현 / tone=어조"),
    ("supporting detail", "뒷받침 세부 내용 / 근거가 되는 구체 정보", "중심 주장이나 주제문을 더 구체적으로 받쳐주는 사례·설명·자료", "큰 기둥 옆에 실제 살을 붙여주는 세부 조각", "supporting detail=주장을 받치는 구체 세부 내용 / topic sentence=단락 중심 문장 / evidence=근거 자료"),
    ("textual nuance", "텍스트의 미묘한 결 / 표현상 섬세한 차이", "단어 선택이나 어조, 문장 구조에서 생기는 작은 의미 차이", "큰 뜻은 비슷해도 말의 질감이 살짝 달라지는 결", "textual nuance=글 표현 속 미묘한 의미 차이 / nuance=미묘한 차이 / wording=말 선택"),
    ("unexamined", "검토되지 않은 / 따져보지 않은", "당연한 듯 깔려 있지만 실제로는 충분히 점검되지 않은", "바닥에 놓인 가정을 그냥 지나치고 아직 눌러보지 않은 느낌", "unexamined=충분히 검토되지 않은 / unquestioned=의심 없이 받아들인 / verified=확인된"),
    ("viewpoint-dependent", "관점에 따라 달라지는", "어느 입장과 위치에서 보느냐에 따라 해석이나 평가가 달라지는", "하나의 고정답보다 서 있는 자리의 각도에 따라 보이는 얼굴이 바뀌는 느낌", "viewpoint-dependent=보는 관점에 따라 달라지는 / perspectival=관점에 따른 / objective=객관적인"),
    ("word choice", "단어 선택 / 표현 선택", "같은 뜻이라도 어떤 단어를 골라 쓰느냐가 어조와 인상을 바꾸는 문제", "내용은 비슷해도 어떤 말을 집느냐가 글의 색을 바꾸는 느낌", "word choice=어떤 단어를 택해 표현하느냐 / diction=어휘 선택과 문체 / phrasing=말을 구성하는 방식"),
    ("argument sketch", "논증 개요 / 주장 구조의 초안", "주장, 이유, 근거, 반론을 간단히 뼈대로 적어둔 틀", "완성 문장 전에 논리 줄기만 먼저 그려보는 밑그림", "argument sketch=논증 구조의 간단한 초안 / outline=큰 틀의 개요 / thesis=중심 논지"),
    ("citation-backed", "출처로 뒷받침된 / 인용 근거가 붙은", "주장이나 설명 아래에 참고 출처와 문헌 근거가 붙어 있는", "혼자 한 말이 아니라 뒤에 어디서 가져왔는지 줄이 달린 느낌", "citation-backed=출처 인용으로 뒷받침된 / source-based=출처 기반의 / unsupported=근거 없는"),
    ("counterexample", "반례 / 일반화를 깨는 사례", "넓은 주장이나 규칙이 항상 맞지는 않음을 보여주는 예외 사례", "다 그렇다고 말한 순간 옆에서 아닌 경우 하나가 튀어나오는 느낌", "counterexample=일반화를 반박하는 반례 / example=예시 일반 / anomaly=예상과 다른 특이 사례"),
    ("evidence pooling", "근거 통합 / 자료를 모아 함께 보기", "여러 출처나 사례의 자료를 한데 모아 더 넓게 판단하는 방식", "흩어진 근거를 한 그릇에 모아 전체 무게를 다시 재는 느낌", "evidence pooling=여러 근거를 합쳐 판단함 / synthesis=종합 / aggregation=모아 합침"),
    ("interpretively", "해석적으로 / 의미를 읽어내는 방식으로", "표면 사실만 나열하기보다 그 의미와 함의를 읽는 방향으로", "겉내용 아래에 무엇을 뜻하는지 한 층 더 읽어내는 느낌", "interpretively=의미를 해석하는 방식으로 / descriptively=상태를 묘사하는 방식으로 / analytically=구조를 분석하며"),
    ("mischaracterize", "잘못 특징짓다 / 성격을 왜곡해 말하다", "대상이나 입장을 실제와 다르게 규정하거나 표현하다", "이 사람이나 주장을 다른 얼굴로 잘못 그려버리는 느낌", "mischaracterize=대상을 잘못 규정해 말하다 / misinterpret=의미를 잘못 해석하다 / distort=왜곡하다"),
    ("premise-based", "전제 기반의 / 깔린 가정에서 출발하는", "논의나 판단이 특정 전제를 바닥에 두고 그 위에서 전개되는", "결론보다 아래에 깐 출발 가정이 논리의 방향을 먼저 정하는 느낌", "premise-based=전제에 기대어 전개되는 / evidence-based=근거에 기반한 / assumption-driven=가정이 강하게 이끄는"),
    ("qualified claim", "조건부 주장 / 한정된 주장", "항상 그렇다고 세게 밀지 않고 범위나 조건을 붙여 조정한 주장", "결론을 세우되 어디까지 맞는지 괄호를 같이 붙이는 느낌", "qualified claim=조건과 범위를 붙여 조정한 주장 / claim qualifier=주장 한정어 / overstatement=과한 단정"),
    ("reading position", "독해 관점 / 읽는 자리", "글을 어떤 입장과 기준에서 받아들이고 해석하는지의 위치", "문장을 어느 발판 위에서 읽느냐에 따라 의미가 달라지는 자리", "reading position=글을 읽는 관점과 입장 / stance=입장 / interpretive lens=해석의 틀"),
    ("source note", "출처 주 / 자료 출처를 적은 짧은 표기", "본문이나 자료 옆에 어디서 왔는지 짧게 달아둔 출처 설명", "이 정보가 나온 곳을 옆에 작은 이름표로 붙여두는 느낌", "source note=자료 출처를 짧게 적은 주 / citation=참고문헌 표기 / annotation=설명 주석"),
    ("textual ambiguity", "본문의 모호성 / 여러 해석 가능성", "글의 표현이나 구조가 하나로 딱 닫히지 않아 여러 의미로 읽힐 수 있는 상태", "문장은 하나인데 어느 뜻으로 읽을지 문이 둘 이상 열린 느낌", "textual ambiguity=텍스트 표현이 여러 해석을 허용함 / ambiguity=모호성 일반 / interpretive range=가능한 해석 폭"),
    ("tone shift", "어조 변화 / 말투의 방향이 바뀜", "중립적이다가 비판적으로, 확신하다가 조심스럽게 등 말의 태도가 바뀌는 것", "같은 목소리가 한 지점에서 다른 색으로 살짝 꺾이는 느낌", "tone shift=어조나 태도가 바뀌는 지점 / viewpoint shift=관점이 바뀌는 전환 / contrast=대조"),
    ("unsupported claim", "근거 없는 주장 / 뒷받침이 약한 주장", "결론은 있지만 아래에 충분한 자료나 논거가 붙지 않은 주장", "말만 앞으로 나와 있고 밑받침 기둥이 비어 있는 느낌", "unsupported claim=근거가 부족한 주장 / unsubstantiated=입증되지 않은 / assertion=단정적 주장"),
    ("writerly", "글쓰기 방식의 / 문체·서술 선택과 관련된", "무슨 내용을 말하느냐보다 어떻게 글로 구성하고 표현하느냐와 관련된", "아이디어 자체보다 문장을 만드는 손길과 스타일을 보는 느낌", "writerly=글쓰기 방식과 문체에 관련된 / stylistic=문체상의 / thematic=주제 중심의"),
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
        manifest["files_created"].insert(17, TARGET.name)
    manifest["total_ets_cards"] = len(ets_words)
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (ROOT / "generation_notes.md").write_text(
        (ROOT / "generation_notes.md").read_text(encoding="utf-8").replace(
            "- ETS sets `01` to `17` exist, bringing the ETS-based total to 1700 cards\n",
            "- ETS sets `01` to `18` exist, bringing the ETS-based total to 1800 cards\n",
        ),
        encoding="utf-8",
    )

    plan = ROOT / "WORK_PLAN.md"
    plan.write_text(
        plan.read_text(encoding="utf-8")
        .replace(
            "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_17.tsv`\n",
            "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_18.tsv`\n",
        )
        .replace(
            "- Current ETS row count after the latest expansion pass: 1700\n",
            "- Current ETS row count after the latest expansion pass: 1800\n",
        ),
        encoding="utf-8",
    )

    task_next = ROOT / ".task_next.md"
    task_next.write_text(
        task_next.read_text(encoding="utf-8")
        .replace("`toefl_ets_2026_set_18.tsv`", "`toefl_ets_2026_set_19.tsv`")
        .replace(
            "argumentation, critique, interpretation, evidence framing, rhetorical stance, and scholarly communication across reading, speaking, and writing tasks.",
            "design, constraints, feasibility, implementation, systems, and innovation in practical problem-solving, while avoiding narrow engineering/materials jargon.",
        ),
        encoding="utf-8",
    )

    print(f"{TARGET.name}: {len(rows)} cards")


if __name__ == "__main__":
    main()
