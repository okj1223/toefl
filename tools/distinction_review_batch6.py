#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


TARGET_FILES = {
    "toefl_ets_2026_set_06.tsv",
    "toefl_ets_2026_set_07.tsv",
    "toefl_ets_2026_set_10.tsv",
    "toefl_ets_2026_set_11.tsv",
    "toefl_ets_2026_set_13.tsv",
    "toefl_ets_2026_set_14.tsv",
    "toefl_ets_2026_set_18.tsv",
    "toefl_ets_2026_set_19.tsv",
    "toefl_ets_2026_set_20.tsv",
    "toefl_ets_2026_set_21.tsv",
    "toefl_ets_2026_set_22.tsv",
    "toefl_ets_2026_set_23.tsv",
}


OVERRIDES: dict[str, dict[str, str | None]] = {
    "toefl_ets_2026_set_07.tsv": {
        "agenda": "agenda=논의·추진 안건 / schedule=시간표",
    },
    "toefl_ets_2026_set_11.tsv": {
        "guided": "guided=지도·안내가 붙는 / independent=혼자 수행하는",
    },
    "toefl_ets_2026_set_18.tsv": {
        "firewall": "firewall=무단 접근을 막는 보안벽 / password=접속 암호",
        "metadata": "metadata=데이터를 설명하는 정보 / content=본문 내용",
    },
    "toefl_ets_2026_set_19.tsv": {
        "server": "server=요청을 처리해 주는 시스템 / platform=서비스 기반",
        "niche": "niche=특정 환경 안에서 차지하는 자리 / habitat=사는 장소",
    },
    "toefl_ets_2026_set_20.tsv": {
        "hedge": "hedge=단정을 완화해 말하다 / assert=분명히 주장하다",
    },
    "toefl_ets_2026_set_21.tsv": {
        "premise": "premise=논증이 출발하는 전제 / conclusion=최종 결론",
        "fallback": "fallback=문제 시 쓰는 예비 대안 / default=기본값",
    },
    "toefl_ets_2026_set_22.tsv": {
        "layered": "layered=의미나 구성이 여러 겹인 / simple=단순한",
        "pacing": "pacing=전개와 전달의 속도 조절 / timing=언제 맞춰 내는가",
    },
    "toefl_ets_2026_set_23.tsv": {
        "reschedule": "reschedule=일정을 다시 잡다 / postpone=뒤로 미루다",
        "shortlist": "shortlist=최종 후보로 추리다 / select=선정하다",
    },
}


def collapse(line: str) -> str:
    parts = [part.strip() for part in line[len("구분: ") :].split(" / ") if part.strip()]
    if len(parts) >= 3:
        return "구분: " + " / ".join(parts[:2])
    return line


def rewrite_file(path: Path) -> int:
    changed = 0
    rows: list[tuple[str, str]] = []
    overrides = OVERRIDES.get(path.name, {})

    with path.open(encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for headword, back in reader:
            lines = []
            for line in back.split("\n"):
                if not line.startswith("구분:"):
                    lines.append(line)
                    continue

                if headword in overrides:
                    target = overrides[headword]
                    if target is not None:
                        lines.append(f"구분: {target}")
                    continue

                lines.append(collapse(line))

            new_back = "\n".join(lines)
            if new_back != back:
                changed += 1
            rows.append((headword, new_back))

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    return changed


def main() -> int:
    changed_files = 0
    changed_rows = 0
    for name in sorted(TARGET_FILES):
        modified = rewrite_file(Path(name))
        if modified:
            print(f"{name}: {modified}")
            changed_files += 1
            changed_rows += modified
    print(f"changed_files={changed_files} changed_rows={changed_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
