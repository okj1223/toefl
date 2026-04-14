#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REMOVE = {
    "toefl_awl_set_01.tsv": {
        "available", "concept", "context", "create", "define", "factor", "identify",
        "major", "occur", "period", "role", "section", "similar", "source", "specific",
        "achieve", "appropriate", "aspect", "chapter", "complex", "culture", "item",
        "journal", "reside", "administrate", "feature", "focus", "positive", "purchase"
    },
    "toefl_awl_set_02.tsv": {
        "site", "text", "circumstance", "comment", "corporate", "criteria", "dominate",
        "ensure", "minor", "partner", "philosophy", "physical", "remove", "task",
        "technical", "technique", "adequate", "attitude", "communicate", "concentrate",
        "job", "obvious", "series", "status", "sum", "aware", "conflict", "enable",
        "expand", "generation", "psychology"
    },
    "toefl_awl_set_03.tsv": {
        "style", "target", "trend", "accurate", "author", "federal", "furthermore",
        "intelligent", "neutral", "overseas", "classic", "comprise", "confirm",
        "differentiate", "foundation", "globe", "grade", "identical", "insert",
        "media", "mode", "publication", "sole", "somewhat", "ultimate", "visible",
        "ambiguous", "bias", "chart"
    },
    "toefl_awl_set_04.tsv": {
        "eventual", "intense", "paragraph", "plus", "theme", "thereby", "via",
        "visual", "behalf", "bulk", "ethic", "minimal", "mutual", "route",
        "scenario", "sphere", "team", "temporary", "albeit", "ongoing", "whereby"
    },
    "toefl_ets_2026_set_01.tsv": {
        "abnormal", "administrative", "alteration", "barrier", "beneficial", "bolster",
        "caution", "clarity", "complexity", "conclusive", "confront", "contaminate",
        "controversy", "convincing", "dimension", "emphasis", "formulate", "innovate",
        "intermediate", "mechanism", "participate", "preliminary", "prominent"
    },
    "toefl_ets_2026_set_04.tsv": {
        "external", "framework", "global", "hence", "hierarchy", "incidence", "income",
        "inevitable", "initial", "instance", "interval", "lecture", "minimum", "network",
        "phenomenon", "phase", "policy", "portion", "potential", "project", "region",
        "resident", "sequence", "stable", "adult", "annual"
    },
    "toefl_ets_2026_set_05.tsv": {
        "benefit", "brief", "category", "chemical", "civil", "commodity", "consideration",
        "contact", "currency", "cycle", "data", "energy", "entity", "environment",
        "era", "error", "expert", "final", "goal", "image", "layer", "legal", "logic",
        "margin", "medical", "mental", "military", "normal", "perspective", "topic",
        "tradition"
    },
}


REPLACE = {
    "toefl_awl_set_01.tsv": {
        "assume": "핵심 뜻: 가정하다\n구분: assume=일단 전제로 놓다 / presume=그럴 가능성이 높다고 보다",
        "contract": "핵심 뜻: 계약\n구분: contract=법적 구속력이 있는 계약 / agreement=합의 일반",
        "finance": "핵심 뜻: 재정 / 자금을 조달하다\n구분: finance=자금 조달·재정 관리 / funding=지원 자금 / budget=예산",
        "involve": "핵심 뜻: 포함하다 / 수반하다 / 관련되다\n구분: involve=요소를 포함하거나 수반하다 / entail=필연적으로 수반하다",
        "principle": "핵심 뜻: 원칙\n구분: principle=원칙·기본 원리 / principal=주요한·교장·원금",
        "process": "핵심 뜻: 과정\n구분: process=단계가 이어지는 과정 / procedure=정해진 수행 절차",
        "research": "핵심 뜻: 연구 / 체계적으로 조사하다\n구분: research=체계적 연구·조사 / survey=설문·조사",
        "respond": "핵심 뜻: 응답하다 / 반응하다\n구분: respond=응답하거나 반응하다 / react=자극에 반응하다",
        "conduct": "핵심 뜻: 수행하다 / 행동\n구분: conduct=조사·실험을 수행하다 또는 행동 / behavior=행동",
        "credit": "핵심 뜻: 공로 / 학점 / 인정하다\n구분: credit=공로·학점·신용 또는 인정하다 / recognition=인정",
        "maintain": "핵심 뜻: 유지하다 / 주장하다\n구분: maintain=상태를 유지하거나 입장을 주장하다 / claim=주장하다",
    },
    "toefl_awl_set_02.tsv": {
        "survey": "핵심 뜻: 조사하다 / 설문 조사\n구분: survey=설문·실태 조사하다 / questionnaire=설문지",
        "compensate": "핵심 뜻: 보상하다 / 상쇄하다\n구분: compensate=보상하거나 상쇄하다 / offset=상쇄하다",
        "correspond": "핵심 뜻: 일치하다 / 대응하다 / 서신을 주고받다\n구분: correspond=서로 대응하거나 서신 교환하다 / match=일치하다",
        "demonstrate": "핵심 뜻: 입증하다 / 보여주다\n구분: demonstrate=증거로 보여주거나 입증하다 / prove=증명하다",
        "imply": "핵심 뜻: 함축하다 / 암시하다\n구분: imply=간접적으로 함축·암시하다 / state=직접 말하다",
        "stress": "핵심 뜻: 스트레스 / 강조하다\n구분: stress=압박·스트레스 또는 강조하다 / emphasize=강조하다",
        "challenge": "핵심 뜻: 도전 과제 / 이의를 제기하다\n구분: challenge=도전 과제이거나 이의를 제기하다 / dispute=반박하다",
        "decline": "핵심 뜻: 감소하다 / 하락 / 거절하다\n구분: decline=감소·하락하다 또는 거절하다 / refuse=거절하다",
        "generate": "핵심 뜻: 생성하다 / 만들어내다\n구분: generate=새 결과를 생성하다 / produce=생산하다",
        "prime": "핵심 뜻: 주요한 / 준비시키다\n구분: prime=주요하거나 미리 준비시키다 / primary=주요한",
    },
    "toefl_awl_set_03.tsv": {
        "reject": "핵심 뜻: 거부하다\n구분: reject=기준에 따라 거부하다 / refuse=요청을 거절하다",
        "transit": "핵심 뜻: 운송 / 이동 / 통과\n구분: transit=이동·운송·통과 / transport=운송하다",
        "cite": "핵심 뜻: 인용하다\n구분: cite=출처나 근거로 인용하다 / quote=문장을 직접 인용하다",
        "index": "핵심 뜻: 지수 / 색인\n구분: index=지수 또는 색인 / indicator=상태 지표",
        "motive": "핵심 뜻: 동기\n구분: motive=행동을 일으킨 이유·동기 / motivation=동기부여 상태나 힘",
        "presume": "핵심 뜻: 추정하다\n구분: presume=그럴듯한 전제로 추정하다 / assume=가정하다",
        "submit": "핵심 뜻: 제출하다 / 따르다\n구분: submit=공식 제출하다 또는 따르다 / comply=따르다",
        "abandon": "핵심 뜻: 버리다 / 포기하다 / 중단하다\n구분: abandon=완전히 포기하거나 버리다 / neglect=돌보지 않고 방치하다",
        "arbitrary": "핵심 뜻: 임의의 / 자의적인\n구분: arbitrary=자의적·임의적인 / random=무작위의",
        "denote": "핵심 뜻: 나타내다 / 뜻하다\n구분: denote=직접적으로 나타내다 / connote=함축하다",
    },
    "toefl_awl_set_04.tsv": {
        "deviate": "핵심 뜻: 벗어나다\n구분: deviate=기준·경로에서 벗어나다 / diverge=갈라져 멀어지다",
        "exhibit": "핵심 뜻: 보여주다 / 전시하다\n구분: exhibit=특징을 드러내거나 전시하다 / demonstrate=증명해 보이다",
        "offset": "핵심 뜻: 상쇄하다\n구분: offset=반대 효과로 상쇄하다 / counteract=맞받아 줄이다",
        "prospect": "핵심 뜻: 전망 / 가능성\n구분: prospect=미래 전망·가능성 / outlook=전망",
        "terminate": "핵심 뜻: 끝내다 / 종료되다\n구분: terminate=공식적으로 끝내다 / end=끝나다·끝내다",
        "coincide": "핵심 뜻: 동시에 일어나다 / 일치하다\n구분: coincide=동시에 겹치거나 일치하다 / overlap=일부가 겹치다",
        "manual": "핵심 뜻: 설명서 / 수동의\n구분: manual=설명서이거나 수동의 / automatic=자동의",
        "supplement": "핵심 뜻: 보충하다\n구분: supplement=부족한 부분을 보충하다·보충물 / complement=서로 맞물려 보완하다",
        "trigger": "핵심 뜻: 촉발하다 / 계기·방아쇠\n구분: trigger=반응·사건을 촉발하다 / cause=원인이 되다",
        "convince": "핵심 뜻: 납득시키다\n구분: convince=근거로 믿고 납득하게 하다 / persuade=행동·태도를 바꾸게 설득하다",
    },
    "toefl_ets_2026_set_01.tsv": {
        "accessible": "핵심 뜻: 접근 가능한\n구분: accessible=쉽게 접근 가능 / available=이용 가능",
        "amend": "핵심 뜻: 수정하다 / 개정하다\n구분: amend=공식 수정 / revise=전반적으로 고치다",
        "argument": "핵심 뜻: 주장 / 논거\n구분: argument=근거 있는 주장 / claim=주장 / debate=논쟁",
        "assumption": "핵심 뜻: 가정 / 전제\n구분: assumption=전제된 믿음 / premise=논리적 전제 / speculation=추측",
        "authoritative": "핵심 뜻: 권위 있는\n구분: authoritative=권위와 근거로 신뢰됨 / official=공식 절차상 인정된",
        "causal": "핵심 뜻: 인과의\n구분: causal=원인과 결과의 / correlational=상관의",
        "cohesive": "핵심 뜻: 응집력 있는 / 결속된\n구분: cohesive=부분들이 잘 결속됨 / coherent=논리적으로 일관됨",
        "constraint": "핵심 뜻: 제약\n구분: constraint=행동 제약 / limitation=한계 / restriction=규정상 제한",
        "conserve": "핵심 뜻: 보존하다 / 절약하다\n구분: conserve=보존·절약하다 / preserve=손상 없이 보존하다",
        "contend": "핵심 뜻: 주장하다 / 다투다\n구분: contend=강하게 주장 / compete=경쟁하다",
        "discrete": "핵심 뜻: 별개의 / 분리된\n구분: discrete=서로 분리된 / distinct=차이가 뚜렷한",
        "distinct": "핵심 뜻: 뚜렷이 다른 / 분명한\n구분: distinct=차이가 선명함 / discrete=분리된",
        "efficient": "핵심 뜻: 효율적인\n구분: efficient=낭비 적음 / effective=효과 있음",
        "evoke": "핵심 뜻: 불러일으키다 / 환기하다\n구분: evoke=감정·기억을 자아냄 / provoke=반응을 유발",
        "exploit": "핵심 뜻: 활용하다 / 착취하다\n구분: exploit=이용하거나 착취 / abuse=남용하다",
        "inherent": "핵심 뜻: 내재된 / 본질적인\n구분: inherent=본질적으로 내재 / acquired=후천적",
        "intervene": "핵심 뜻: 개입하다 / 중재하다\n구분: intervene=중간에 개입 / mediate=중재하다 / interfere=간섭하다",
        "likelihood": "핵심 뜻: 가능성 / 개연성\n구분: likelihood=일어날 가능성 / probability=수학적 확률",
        "plausible": "핵심 뜻: 그럴듯한\n구분: plausible=겉으로 타당해 보임 / convincing=더 설득력 있음",
        "proportion": "핵심 뜻: 비율 / 부분\n구분: proportion=전체 대비 비율 / ratio=두 수의 비 / percentage=백분율",
        "ratio": "핵심 뜻: 비율 / 비\n구분: ratio=두 수의 비 / proportion=전체 대비 비율",
    },
    "toefl_ets_2026_set_04.tsv": {
        "exclude": "핵심 뜻: 제외하다\n구분: exclude=제외하다 / omit=빠뜨리다",
        "explicit": "핵심 뜻: 명시적인\n구분: explicit=분명히 드러난 / implicit=암묵적인",
        "export": "핵심 뜻: 수출하다 / 수출품\n구분: export=밖으로 보내다 / import=안으로 들이다",
        "grant": "핵심 뜻: 보조금 / 승인하다\n구분: grant=공식 지원금 / scholarship=장학금",
        "ignore": "핵심 뜻: 무시하다\n구분: ignore=의도적으로 무시 / overlook=못 보고 지나침",
        "implement": "핵심 뜻: 실행하다 / 시행하다\n구분: implement=실행에 옮기다 / apply=적용하다 / enforce=강제로 시행하다",
        "impose": "핵심 뜻: 부과하다 / 강요하다\n구분: impose=강제로 부과 / enforce=집행하다",
        "infer": "핵심 뜻: 추론하다\n구분: infer=증거로 추론 / assume=가정하다",
        "migrate": "핵심 뜻: 이동하다 / 이주하다\n구분: migrate=이동·이주 / immigrate=이민 오다",
        "modify": "핵심 뜻: 수정하다 / 변경하다\n구분: modify=부분 수정 / adapt=상황에 맞게 바꾸다",
        "notion": "핵심 뜻: 개념 / 생각\n구분: notion=막연한 개념 / concept=정교한 개념",
        "objective": "핵심 뜻: 객관적인 / 목표\n구분: objective=객관적 / unbiased=편향 없는",
        "option": "핵심 뜻: 선택지 / 선택권\n구분: option=선택 가능한 것 / alternative=대안",
        "parameter": "핵심 뜻: 매개변수\n구분: parameter=설정 값 / variable=변수",
        "precise": "핵심 뜻: 정확한 / 정밀한\n구분: precise=세밀하게 정확 / accurate=오차 없이 정확",
        "predict": "핵심 뜻: 예측하다\n구분: predict=미래 예측 / forecast=전망하다",
        "prior": "핵심 뜻: 이전의 / 사전의\n구분: prior=시간상 앞선 / previous=이전의",
        "prohibit": "핵심 뜻: 금지하다\n구분: prohibit=공식 금지 / ban=금지하다",
        "relevant": "핵심 뜻: 관련 있는 / 적절한\n구분: relevant=주제와 관련 / appropriate=적절한",
        "resource": "핵심 뜻: 자원 / 자료\n구분: resource=활용 자원 / source=출처",
        "access": "핵심 뜻: 접근 / 이용할 수 있음\n구분: access=접근하거나 이용할 수 있음 / permission=허가",
        "aid": "핵심 뜻: 돕다 / 도움\n구분: aid=도움을 주거나 도움 / assist=돕다 / relief=구호",
        "assign": "핵심 뜻: 할당하다\n구분: assign=할당하다 / allocate=배분하다",
    },
    "toefl_ets_2026_set_05.tsv": {
        "compatible": "핵심 뜻: 양립 가능한\n구분: compatible=서로 맞는 / suitable=적합한",
        "complement": "핵심 뜻: 보완하다\n구분: complement=보완하다 / supplement=추가 보충 / replace=대체하다",
        "compound": "핵심 뜻: 혼합물 / 복합의\n구분: compound=복합되다 / intensify=강화하다",
        "consent": "핵심 뜻: 동의\n구분: consent=동의 / permission=허가",
        "convert": "핵심 뜻: 전환하다\n구분: convert=형태 전환 / transform=크게 바꾸다",
        "credible": "핵심 뜻: 신뢰할 수 있는\n구분: credible=믿을 만한 / plausible=그럴듯한",
        "despite": "핵심 뜻: ~에도 불구하고\n구분: despite=~에도 불구하고 / regardless of=상관없이",
        "displace": "핵심 뜻: 대체하다 / 이동시키다\n구분: displace=자리에서 밀어내다 / replace=대체하다",
        "display": "핵심 뜻: 보여 주다 / 전시하다\n구분: display=보여 주거나 전시하다 / exhibit=전시하다",
        "enforce": "핵심 뜻: 시행하다\n구분: enforce=강제 시행 / implement=실행하다",
        "equilibrium": "핵심 뜻: 균형 상태\n구분: equilibrium=평형 / stability=안정성",
        "fund": "핵심 뜻: 기금 / 자금을 대다\n구분: fund=기금이거나 자금 지원하다 / sponsor=후원하다",
        "guarantee": "핵심 뜻: 보장하다\n구분: guarantee=확실히 보장 / ensure=확실히 하다",
        "permit": "핵심 뜻: 허용하다 / 허가증\n구분: permit=허용하거나 허가증 / authorize=공식 허가하다",
        "preserve": "핵심 뜻: 보존하다\n구분: preserve=보존하다 / conserve=보호·보존하다",
        "qualitative": "핵심 뜻: 질적인\n구분: qualitative=질적인 / quantitative=양적인",
        "recover": "핵심 뜻: 회복하다\n구분: recover=회복하다 / restore=복구하다",
        "scope": "핵심 뜻: 범위\n구분: scope=범위 / extent=정도·범위",
        "sustain": "핵심 뜻: 유지하다 / 지탱하다\n구분: sustain=지속시키거나 지탱하다 / maintain=유지하다 / support=떠받치다",
        "transfer": "핵심 뜻: 옮기다 / 이전하다\n구분: transfer=옮기다 / transmit=전달하다",
    },
}


def main() -> int:
    changed_files = 0
    changed_rows = 0
    for rel in sorted(set(REMOVE) | set(REPLACE)):
        path = ROOT / rel
        rows = []
        changed = False
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            for front, back in reader:
                new_back = back
                if front in REMOVE.get(rel, set()):
                    new_back = back.split("\n구분:", 1)[0]
                if front in REPLACE.get(rel, {}):
                    new_back = REPLACE[rel][front]
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


if __name__ == "__main__":
    main()
