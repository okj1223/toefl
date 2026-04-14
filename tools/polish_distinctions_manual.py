#!/usr/bin/env python3
from __future__ import annotations

import csv
import glob
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    "toefl_ets_2026_set_[0-9][0-9].tsv",
    "toefl_awl_set_[0-9][0-9].tsv",
]

DIST_OVERRIDES = {
    "significant": "significant=해석상 의미 있거나 영향이 큼 / important=일반적으로 중요한",
    "assist": None,
    "scheme": None,
    "individual": "individual=개별 단위의 / collective=집단 전체의",
    "specific": "specific=대상·조건을 딱 집어 좁힘 / general=넓게 말하는 일반적",
    "positive": "positive=좋은 방향이거나 양의 값 / favorable=상황이 유리한 / negative=반대 방향·음의",
    "crucial": "crucial=빠지면 결과가 흔들릴 만큼 핵심 / relevant=관련 있는",
    "nonetheless": None,
    "notwithstanding": None,
    "authoritative": "authoritative=권위와 근거로 신뢰됨 / official=공식 절차상 인정된",
    "network": "network=여러 지점의 연결망 / connection=개별 연결",
    "overall": None,
    "brief": "brief=짧고 핵심만 있음 / concise=군더더기 없이 간결함",
    "actionable": None,
    "legible": None,
    "transparent": "transparent=과정·기준이 숨김없이 보임 / open=태도·구조가 개방적인",
    "overview": None,
    "usable": None,
    "favorable": "favorable=조건이 결과에 유리함 / beneficial=실질적 도움을 줌 / positive=좋은 쪽 평가·부호",
    "group-based": "group-based=집단 단위로 작동하는 / individual=개인 단위로 작동하는",
    "cloud-based": "cloud-based=서버·클라우드에서 저장·처리 / local=기기 내부에서 처리하는",
    "systemwide": "systemwide=전체 시스템 전반에 걸친 / local=일부 지점에 한정된",
    "contextual": "contextual=맥락에 따라 달라짐 / general=맥락을 덜 타는 일반적",
    "transboundary": "transboundary=국경·행정 경계를 넘는 / local=한 지역 안에 머무는",
    "cross-jurisdictional": "cross-jurisdictional=여러 관할권에 걸친 / local=한 관할 안에 머무는",
    "grassroots": "grassroots=아래로부터 시민 참여 기반의 / top-down=위에서 내려오는",
    "identity-based": "identity-based=사회적 정체성을 기준으로 한 / individual=개인 특성만 보는",
    "user-generated": "user-generated=사용자가 직접 만든 / curated=선별 편집된 / official=기관이 만든",
    "granularity": "granularity=얼마나 잘게 나눠 보는지 / resolution=구분의 세밀함",
}


def process_back(headword: str, back: str) -> tuple[str, bool]:
    override = DIST_OVERRIDES.get(headword)
    if headword not in DIST_OVERRIDES:
        return back, False

    lines = back.split("\n")
    rebuilt = []
    changed = False

    for line in lines:
        if line.startswith("구분:"):
            changed = True
            if override is None:
                continue
            rebuilt.append(f"구분: {override}")
        else:
            rebuilt.append(line)

    if override is not None and not any(line.startswith("구분:") for line in lines):
        rebuilt.append(f"구분: {override}")
        changed = True

    new_back = "\n".join(rebuilt)
    return new_back, changed and new_back != back


def main() -> int:
    files_changed = 0
    rows_changed = 0

    for pattern in PATTERNS:
        for rel_path in sorted(glob.glob(pattern)):
            path = ROOT / rel_path
            updated_rows = []
            local_changed = False

            with path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle, delimiter="\t", quotechar='"')
                for row in reader:
                    if len(row) != 2:
                        updated_rows.append(row)
                        continue
                    headword, back = row
                    new_back, changed = process_back(headword, back)
                    updated_rows.append([headword, new_back])
                    if changed:
                        local_changed = True
                        rows_changed += 1

            if local_changed:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                    writer.writerows(updated_rows)
                files_changed += 1

    print(f"files_changed={files_changed}")
    print(f"rows_changed={rows_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
