#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DELETIONS = {
    "toefl_ets_2026_set_17.tsv": {
        "administrability",
        "adjudicator",
        "caseworker",
        "deliverable-based",
        "whole-of-government",
    },
    "toefl_ets_2026_set_18.tsv": {
        "line-by-line",
        "premise-checking",
        "quote-heavy",
        "reason-giving",
        "rebuttal-ready",
        "statement-level",
        "text-to-context",
    },
    "toefl_ets_2026_set_19.tsv": {
        "backward-compatible",
        "buildout",
        "constraint-aware",
        "make-or-buy",
        "milestone-driven",
        "outage-prone",
        "proof-of-concept",
        "trialable",
        "upgrade-ready",
        "zero-defect",
    },
    "toefl_ets_2026_set_20.tsv": {
        "captioned",
        "chiaroscuro",
        "dramaturgical",
        "genre-bending",
        "mise-en-scene",
        "motivic",
        "offscreen",
        "scenic",
        "soundscape",
        "voiceover",
    },
}


REPLACEMENTS = {
    "toefl_ets_2026_set_17.tsv": {
        "eligibility": "핵심 뜻: 지원 자격 / 수급 자격\n구분: eligibility=지원·혜택 대상 자격 / qualification=요건을 갖춤",
        "implementer": "핵심 뜻: 실행 주체 / 실행 담당자\n구분: implementer=정책·계획을 실제로 집행하는 주체 / planner=계획을 짜는 사람",
        "mandated": "핵심 뜻: 의무화된 / 공식 지정된\n구분: mandated=공식적으로 의무화된 / required=필수의 / optional=선택의",
        "rollout": "핵심 뜻: 단계적 도입 / 현장 배포\n구분: rollout=실제 현장 도입·배포 / implementation=실행 / launch=시작 공개",
        "citizen-facing": "핵심 뜻: 시민 접점의 / 시민 대상의\n구분: citizen-facing=시민이 직접 마주하는 / public-facing=외부 공개용의",
        "co-funding": "핵심 뜻: 공동 재원 지원 / 공동 부담\n구분: co-funding=여러 주체가 함께 재원을 지원함 / cost-sharing=비용을 나눠 부담함",
        "devolution": "핵심 뜻: 권한 이양 / 기능 이관\n구분: devolution=권한을 하위 단위로 이양함 / decentralization=권한 분산",
    },
    "toefl_ets_2026_set_18.tsv": {
        "assertive": "핵심 뜻: 단호한 / 자기 입장을 분명히 밝히는\n구분: assertive=자기 입장을 분명히 말하는 / tentative=조심스럽고 잠정적인",
        "backing": "핵심 뜻: 뒷받침 근거\n구분: backing=주장을 뒷받침하는 근거 / evidence=실제 근거 자료",
        "foreground": "핵심 뜻: 전면에 내세우다\n구분: foreground=특정 요소를 전면에 강조하다 / emphasize=강조하다",
        "salience": "핵심 뜻: 두드러짐 / 현저성\n구분: salience=특히 눈에 띄고 중요하게 보임 / prominence=두드러진 위치",
        "voice": "핵심 뜻: 서술 목소리 / 어조\n구분: voice=글이나 발화에 드러난 어조와 태도 / tone=정서적 말투 / stance=입장",
        "warranted": "핵심 뜻: 정당화되는 / 타당한\n구분: warranted=근거상 정당화되는 / justified=타당한 이유가 있는 / arbitrary=임의적인",
        "counterclaim": "핵심 뜻: 맞대응 주장 / 맞주장\n구분: counterclaim=기존 주장에 맞서는 주장 / counterargument=반대 논거",
    },
    "toefl_ets_2026_set_19.tsv": {
        "fallback": "핵심 뜻: 대체 수단 / 예비안\n구분: fallback=문제 시 쓰는 예비 대안 / contingency=비상 대비책 / default=기본값",
        "future-proof": "핵심 뜻: 미래 변화에도 버티게 설계하다\n구분: future-proof=미래 변화에도 덜 흔들리게 설계하다 / scalable=규모 확장이 가능한",
        "human-centered": "핵심 뜻: 사람 중심의 / 사용자 중심의\n구분: human-centered=사용자 필요를 중심에 둔 / user-friendly=사용하기 쉬운",
        "maintainability": "핵심 뜻: 유지보수성 / 관리 용이성\n구분: maintainability=유지보수하기 쉬운 정도 / serviceability=정비 용이성",
        "usability": "핵심 뜻: 사용성 / 사용 편의성\n구분: usability=실제 사용하기 쉬운 정도 / accessibility=접근하기 쉬운 정도",
    },
    "toefl_ets_2026_set_20.tsv": {
        "backdrop": "핵심 뜻: 배경 / 배경막\n구분: backdrop=앞 장면을 받치는 배경 / foreground=앞쪽에 두드러진 부분",
        "composition": "핵심 뜻: 구도 / 구성\n구분: composition=요소의 전체 배열과 구도 / layout=배치 / component=개별 구성 요소",
        "iconic": "핵심 뜻: 상징적으로 유명한 / 대표적인\n구분: iconic=대표 이미지처럼 널리 각인된 / famous=유명한 / symbolic=상징적 의미를 띤",
        "resonance": "핵심 뜻: 울림 / 공명\n구분: resonance=마음이나 문화 속에 오래 남는 울림 / impact=즉각적 영향",
        "embody": "핵심 뜻: 구현하다 / 체현하다\n구분: embody=의미·가치를 구체적 형태로 드러내다 / symbolize=상징하다",
        "rendering": "핵심 뜻: 표현 방식 / 구현 결과\n구분: rendering=어떤 방식으로 구현해 나타낸 결과 / depiction=묘사",
        "readability": "핵심 뜻: 가독성\n구분: readability=읽기 쉬운 정도 / legibility=글자 형태를 알아보기 쉬운 정도",
    },
}


REJECTED_APPEND = [
    "administrability\trare bureaucratic noun with weak broad TOEFL transferability\t\thigh",
    "caseworker\tsocial-services-specific occupational term with low cross-topic reuse\t\thigh",
    "deliverable-based\tjargon-heavy compound with low standalone vocabulary value\t\thigh",
    "whole-of-government\tpolicy-jargon compound with low standalone TOEFL transferability\t\thigh",
    "adjudicator\tnarrow formal decision-maker term with lower utility than broader judging vocabulary\t\thigh",
    "text-to-context\tstudy-label compound rather than a strong standalone academic headword\t\thigh",
    "premise-checking\tmeta-analytic compound with low standalone vocabulary value\t\thigh",
    "quote-heavy\tlow-transfer descriptive compound with limited standalone payoff\t\thigh",
    "reason-giving\tmeta-analytic compound with low standalone vocabulary value\t\thigh",
    "rebuttal-ready\tcoined study-prep compound with weak standalone TOEFL value\t\thigh",
    "statement-level\tmeta-analytic compound with limited standalone transferability\t\thigh",
    "line-by-line\tcommon phrase but weak as a dedicated Band-5 headword\t\tmedium",
    "buildout\tproduct-development noun with low broad TOEFL reuse\t\thigh",
    "proof-of-concept\tstartup/product jargon compound with limited broad TOEFL transferability\t\thigh",
    "make-or-buy\tbusiness decision compound with low standalone TOEFL value\t\thigh",
    "milestone-driven\tproject-management compound with lower broad transferability\t\thigh",
    "outage-prone\ttechnical-service compound with low broad TOEFL reuse\t\thigh",
    "zero-defect\tquality-control slogan-like compound with low broad academic payoff\t\thigh",
    "backward-compatible\tsoftware-specific compound with low cross-topic TOEFL reuse\t\thigh",
    "constraint-aware\tengineering/design jargon compound with low standalone payoff\t\thigh",
    "trialable\tawkward low-frequency product-adoption adjective\t\thigh",
    "upgrade-ready\tproduct-lifecycle compound with low standalone TOEFL value\t\thigh",
    "captioned\tmedia-format descriptor with limited broad academic transferability\t\thigh",
    "genre-bending\tarts-review compound with low broad TOEFL reuse\t\thigh",
    "voiceover\tmedia-production term with low cross-topic transferability\t\thigh",
    "chiaroscuro\tart-history-specific term likely to be glossed if needed\t\thigh",
    "mise-en-scene\tfilm/theater-specific term likely to be glossed if needed\t\thigh",
    "dramaturgical\ttheater-structure term with low broad TOEFL reuse\t\thigh",
    "motivic\tnarrow arts-analysis adjective with low broad transferability\t\thigh",
    "soundscape\tmedium-specific arts term with limited broad academic reuse\t\thigh",
    "offscreen\tfilm/video-specific adjective with low cross-topic transferability\t\thigh",
    "scenic\tarts/landscape descriptor with lower utility than broader interpretive vocabulary\t\tmedium",
]


def append_unique_lines(path: Path, lines: list[str]) -> None:
    if not lines:
        return
    existing = path.read_text(encoding="utf-8").splitlines()
    additions = [line for line in lines if line not in existing]
    if not additions:
        return
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    text += "\n".join(additions) + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> int:
    targets = [
        "toefl_ets_2026_set_17.tsv",
        "toefl_ets_2026_set_18.tsv",
        "toefl_ets_2026_set_19.tsv",
        "toefl_ets_2026_set_20.tsv",
    ]
    changed_files = 0
    changed_rows = 0
    removed_rows = 0
    for rel in targets:
        path = ROOT / rel
        rows = []
        changed = False
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if len(row) != 2:
                    rows.append(row)
                    continue
                front, back = row
                if front in DELETIONS.get(rel, set()):
                    changed = True
                    removed_rows += 1
                    continue
                new_back = REPLACEMENTS.get(rel, {}).get(front, back)
                if new_back != back:
                    changed = True
                    changed_rows += 1
                rows.append([front, new_back])
        if changed:
            changed_files += 1
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter="\t", lineterminator="\n")
                writer.writerows(rows)

    append_unique_lines(ROOT / "rejected_candidates.tsv", REJECTED_APPEND)
    print(f"changed_files={changed_files} changed_rows={changed_rows} removed_rows={removed_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
