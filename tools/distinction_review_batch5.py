#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


TARGET_FILES = {
    "toefl_awl_set_01.tsv",
    "toefl_awl_set_03.tsv",
    "toefl_awl_set_04.tsv",
    "toefl_ets_2026_set_01.tsv",
    "toefl_ets_2026_set_02.tsv",
    "toefl_ets_2026_set_04.tsv",
    "toefl_ets_2026_set_09.tsv",
    "toefl_ets_2026_set_12.tsv",
    "toefl_ets_2026_set_16.tsv",
    "toefl_ets_2026_set_17.tsv",
    "toefl_ets_2026_set_25.tsv",
}


OVERRIDES: dict[str, dict[str, str | None]] = {
    "toefl_ets_2026_set_02.tsv": {
        "temporal": "temporal=시간과 관련된 / spatial=공간의",
        "rely": None,
    },
    "toefl_ets_2026_set_04.tsv": {
        "rely": "rely on=의존하다 / trust=믿고 맡기다",
    },
    "toefl_ets_2026_set_09.tsv": {
        "outbreak": "outbreak=갑작스러운 집단 발병 / epidemic=지역적 유행",
        "quarantine": "quarantine=예방적 격리 / isolation=확진자 격리",
    },
    "toefl_ets_2026_set_12.tsv": {
        "coursework": None,
    },
    "toefl_ets_2026_set_16.tsv": {
        "appointment": "appointment=예약된 만남 / reservation=자리·시설 예약",
        "questionnaire": "questionnaire=설문 질문지 / survey=조사 전체",
        "scholarship": "scholarship=장학금 / fellowship=연구 중심 지원",
        "transcript": "transcript=공식 성적·발언 기록문 / certificate=증명서",
        "undergraduate": "undergraduate=학부생·학부 과정의 / graduate=대학원생·졸업자의",
    },
    "toefl_ets_2026_set_17.tsv": {
        "waitlist": "waitlist=대기자 명단 / roster=확정된 명단",
        "itinerary": "itinerary=이동·방문 중심 일정표 / agenda=회의 안건",
        "convention": "convention=사회적으로 굳어진 관례 / conference=발표·논의 중심 회의",
        "resettlement": "resettlement=새 지역에 다시 정착함 / relocation=위치를 옮김",
    },
    "toefl_ets_2026_set_25.tsv": {
        "dispersion": "dispersion=퍼짐 정도 / concentration=한곳에 모임",
        "skew": "skew=한쪽으로 치우치다 / bias=편향",
        "plateau": "plateau=상승이 멈춘 평평한 구간 / peak=가장 높은 한 점",
        "trendline": "trendline=전체 방향을 잇는 선 / baseline=비교 기준선",
        "amplitude": "amplitude=진폭 / frequency=빈도",
        "underestimate": "underestimate=과소평가하다 / overestimate=과대평가하다",
        "disaggregate": "disaggregate=세분해 나누다 / classify=기준별로 분류하다",
        "quantify": "quantify=수량화하다 / measure=측정하다",
        "classify": "classify=분류하다 / categorize=범주화하다",
        "segmentation": "segmentation=세분화 / stratification=층화",
        "causation": "causation=인과관계 / correlation=상관관계",
        "randomization": "randomization=무작위 배정 / allocation=배분",
        "replicability": "replicability=재현 가능성 / reliability=신뢰성",
        "extrapolation": "extrapolation=외삽 추정 / interpolation=보간 추정",
        "volatility": "volatility=변동성 / instability=불안정성",
        "shortfall": "shortfall=부족분 / deficit=적자·결손",
        "divergence": "divergence=발산·차이 확대 / deviation=편차",
        "plateauing": "plateauing=정체 단계 진입 / declining=감소",
    },
}


def collapse_distinction(line: str) -> str:
    payload = line[len("구분: ") :]
    parts = [part.strip() for part in payload.split(" / ") if part.strip()]
    if len(parts) >= 3:
        return "구분: " + " / ".join(parts[:2])
    return line


def apply_file(path: Path) -> int:
    rows: list[tuple[str, str]] = []
    changed = 0
    overrides = OVERRIDES.get(path.name, {})

    with path.open(encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for headword, back in reader:
            lines = back.split("\n")
            new_lines: list[str] = []
            for line in lines:
                if not line.startswith("구분:"):
                    new_lines.append(line)
                    continue

                if headword in overrides:
                    target = overrides[headword]
                    if target is not None:
                        new_lines.append(f"구분: {target}")
                    continue

                new_lines.append(collapse_distinction(line))

            new_back = "\n".join(new_lines)
            if new_back != back:
                changed += 1
            rows.append((headword, new_back))

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    return changed


def main() -> int:
    total = 0
    changed_files = 0
    for name in sorted(TARGET_FILES):
        path = Path(name)
        modified = apply_file(path)
        if modified:
            print(f"{path.name}: {modified}")
            total += modified
            changed_files += 1
    print(f"changed_files={changed_files} changed_rows={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
