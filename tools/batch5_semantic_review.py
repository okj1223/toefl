#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


RENAMES = {
    "toefl_ets_2026_set_13.tsv": {
        "groupwide": "group-wide",
    },
    "toefl_ets_2026_set_15.tsv": {
        "plug-in": "plugin",
    },
}


DELETIONS = {
    "toefl_ets_2026_set_15.tsv": {
        "log-in",
        "infostream",
        "two-factor",
    },
    "toefl_ets_2026_set_16.tsv": {
        "bioenergetic",
        "chemosensory",
        "cross-adaptation",
        "density-dependent",
        "disturbance-tolerant",
        "photoperiodic",
        "sink-source",
        "threshold-sensitive",
    },
}


REPLACEMENTS = {
    "toefl_ets_2026_set_13.tsv": {
        "citation": "핵심 뜻: 출처 표기 / 인용\n구분: citation=출처를 밝히는 인용 표기 / reference=참고문헌·참조 대상 / quotation=직접 인용문",
        "floor": "핵심 뜻: 발언권 / 토론 기회\n구분: floor=발언할 차례나 기회 / agenda=논의 안건 목록 / stage=발표 무대",
        "recipient": "핵심 뜻: 수신자 / 수령인\n구분: recipient=공식적으로 받는 사람 / receiver=받는 사람 일반",
        "validation": "핵심 뜻: 검증 / 타당성 확인\n구분: validation=타당한지 확인함 / approval=승인 / certification=자격 인증",
        "acknowledgment": "핵심 뜻: 감사의 말 / 기여 인정\n구분: acknowledgment=도움·기여를 인정함 / appreciation=감사하는 마음",
        "outreach": "핵심 뜻: 대외 연계 / 홍보 활동\n구분: outreach=외부 대상 연결·홍보 활동 / publicity=널리 알리는 홍보",
        "advisory": "핵심 뜻: 권고의 / 자문용의\n구분: advisory=권고·자문 성격의 / mandatory=의무적인",
        "monitoring": "핵심 뜻: 지속 점검 / 모니터링\n구분: monitoring=계속 지켜보며 점검함 / supervision=위에서 관리·감독함",
        "readout": "핵심 뜻: 요약 보고 / 결과 요약\n구분: readout=회의·결과를 짧게 정리한 보고 / transcript=발언 기록문",
        "keynote": "핵심 뜻: 기조연설 / 기조발표\n구분: keynote=행사의 중심 기조발표 / lecture=일반 강의",
        "group-wide": "핵심 뜻: 집단 전체 대상의\n구분: group-wide=집단 전체에 걸친 / partial=일부만의 / individual=개별의",
    },
    "toefl_ets_2026_set_14.tsv": {
        "trace": "핵심 뜻: 흔적 / 자취\n구분: trace=희미하게 남은 흔적 / evidence=판단 근거 / remnant=남은 일부",
        "convention": "핵심 뜻: 관례 / 관습\n구분: convention=사회적으로 굳어진 관례 / custom=생활 관습 / conference=발표·논의 중심 회의",
        "regime": "핵심 뜻: 정권 / 체제\n구분: regime=정권 또는 지배 체제 / government=정부 조직",
        "customary": "핵심 뜻: 관습적인 / 관례적인\n구분: customary=관습적으로 으레 하는 / conventional=통상적·관례적인",
        "recovery": "핵심 뜻: 회복 / 되찾기\n구분: recovery=잃은 상태를 되찾거나 회복함 / restoration=원래 모습에 가깝게 복원함 / retrieval=찾아 꺼냄",
        "storytelling": "핵심 뜻: 이야기 전달 방식 / 서사화\n구분: storytelling=이야기 구조로 전달하는 방식 / narration=사건을 서술함",
        "landmark": "핵심 뜻: 중요한 전환점 / 기준점\n구분: landmark=중요한 전환점·기준점 / milestone=진행 중 주요 단계 / monument=기념 구조물",
        "leadership": "핵심 뜻: 지도력 / 지도부\n구분: leadership=이끄는 힘이나 집단 / authority=공식 권한 / elite=상층 집단",
        "memorial": "핵심 뜻: 추모물 / 기념물\n구분: memorial=추모·기념 대상 / monument=기념 구조물 / reminder=떠올리게 하는 것",
        "subordinate": "핵심 뜻: 하위의 / 종속된\n구분: subordinate=상위 체계 아래 놓인 / dependent=의존적인 / assistant=보조 역할의",
        "urbanism": "핵심 뜻: 도시 생활 양식 / 도시주의\n구분: urbanism=도시 중심 생활·사고 방식 / urbanization=도시로 집중되는 과정",
        "caravan": "핵심 뜻: 상단 / 이동 행렬\n구분: caravan=사람과 짐이 함께 이동하는 행렬 / convoy=호위 속 이동 대열",
        "figurehead": "핵심 뜻: 명목상 지도자 / 상징적 대표\n구분: figurehead=상징적 대표 인물 / leader=실질적 지도자",
        "outlying": "핵심 뜻: 외곽의 / 주변부의\n구분: outlying=중심에서 떨어진 외곽의 / peripheral=주변부의 / remote=멀리 떨어진",
    },
    "toefl_ets_2026_set_15.tsv": {
        "query": "핵심 뜻: 검색 질의 / 질의\n구분: query=정보를 얻기 위한 질의 / question=질문 일반 / request=요청",
        "auto-save": "핵심 뜻: 자동 저장\n구분: auto-save=변경 내용을 자동으로 저장함 / backup=예비 저장본을 따로 남김",
        "plugin": "핵심 뜻: 플러그인\n구분: plugin=기존 시스템에 붙는 추가 기능 / module=기능 단위 / extension=기능을 덧붙이는 요소",
        "shareability": "핵심 뜻: 공유 용이성 / 퍼뜨리기 쉬움\n구분: shareability=공유하고 퍼뜨리기 쉬움 / accessibility=접근하기 쉬움",
        "platform": "핵심 뜻: 플랫폼 / 기반 서비스\n구분: platform=서비스와 상호작용이 올라서는 기반 / interface=사용자가 만나는 접점",
    },
    "toefl_ets_2026_set_16.tsv": {
        "conductive": "핵심 뜻: 전도성의 / 전달성이 있는\n구분: conductive=열·신호를 잘 전달하는 / permeable=물질이 통과하기 쉬운",
        "modulator": "핵심 뜻: 조절 요인 / 조절 장치\n구분: modulator=반응 강도를 조절하는 요인 / regulator=작동 수준을 조정하는 요소",
        "niche": "핵심 뜻: 특정 자리 / 틈새 역할\n구분: niche=특정 환경 안에서 차지하는 자리 / habitat=사는 장소 / role=역할 일반",
        "plasticity": "핵심 뜻: 가소성 / 변화 가능성\n구분: plasticity=조건에 따라 바뀔 수 있는 성질 / flexibility=유연성",
        "retentive": "핵심 뜻: 잘 보유하는 / 유지력이 있는\n구분: retentive=잘 보유하고 유지하는 / absorptive=잘 흡수하는 / porous=빈틈이 많은",
        "survivorship": "핵심 뜻: 생존률 / 생존 유지\n구분: survivorship=생존이 유지되는 정도 / resilience=충격 후 회복력",
    },
}


REJECTED_APPEND = [
    "infostream\tlow-transfer coined digital term with weak standalone TOEFL value\t\thigh",
    "two-factor\tfragmentary headword; the full expression is better omitted than forced into a single-word front\t\thigh",
    "cross-adaptation\thyper-specialized biology term with low cross-topic TOEFL transferability\t\thigh",
    "sink-source\tnarrow ecology compound with low standalone transferability\t\thigh",
    "threshold-sensitive\tnarrow technical compound likely to be glossed in passage if needed\t\thigh",
    "density-dependent\tnarrow ecology/statistics compound with limited broad TOEFL reuse\t\thigh",
    "disturbance-tolerant\tniche ecology descriptor with low broad TOEFL transferability\t\thigh",
    "chemosensory\thyper-specialized sensory-science term\t\thigh",
    "photoperiodic\thyper-specialized biology term\t\thigh",
    "bioenergetic\tnarrow biological-process descriptor with low broad TOEFL reuse\t\thigh",
]


DUPLICATES_APPEND = [
    "toefl_ets_2026_set_15.tsv:51\tlogin\tremoved semantic duplicate already covered in ETS supplement (toefl_ets_2026_set_23.tsv:93)",
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
        "toefl_ets_2026_set_13.tsv",
        "toefl_ets_2026_set_14.tsv",
        "toefl_ets_2026_set_15.tsv",
        "toefl_ets_2026_set_16.tsv",
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
                new_front = RENAMES.get(rel, {}).get(front, front)
                new_back = REPLACEMENTS.get(rel, {}).get(new_front, REPLACEMENTS.get(rel, {}).get(front, back))
                if new_front != front or new_back != back:
                    changed = True
                    changed_rows += 1
                rows.append([new_front, new_back])
        if changed:
            changed_files += 1
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter="\t", lineterminator="\n")
                writer.writerows(rows)

    append_unique_lines(ROOT / "rejected_candidates.tsv", REJECTED_APPEND)
    append_unique_lines(ROOT / "duplicates_removed.tsv", DUPLICATES_APPEND)
    print(f"changed_files={changed_files} changed_rows={changed_rows} removed_rows={removed_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
