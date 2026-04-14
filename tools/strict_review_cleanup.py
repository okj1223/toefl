#!/usr/bin/env python3
from __future__ import annotations

import csv
import glob
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ETS_PATTERN = "toefl_ets_2026_set_[0-9][0-9].tsv"
REJECTED_PATH = ROOT / "rejected_candidates.tsv"

REMOVE_HEADWORDS = {
    "bioindicator": (
        "too biology/environment-specific for the broad band-5 TOEFL core",
        "",
        "high",
    ),
    "biomechanical": (
        "too specialized toward movement science and physiology",
        "",
        "high",
    ),
    "carbohydrate": (
        "domain-specific nutrition term with lower cross-topic academic reuse",
        "",
        "high",
    ),
    "circulatory": (
        "biology-system term with lower transferability outside science passages",
        "",
        "high",
    ),
    "cross-signaling": (
        "niche scientific mechanism term with low broad TOEFL transferability",
        "",
        "high",
    ),
    "brushstroke": (
        "art-production-specific term with low cross-disciplinary reuse",
        "",
        "high",
    ),
    "collage": (
        "art-technique term with lower broad academic utility",
        "",
        "medium",
    ),
    "curatorial": (
        "museum/exhibition-specific adjective with low broad TOEFL reuse",
        "",
        "high",
    ),
    "photorealistic": (
        "visual-rendering term that is too medium-specific for the core set",
        "",
        "high",
    ),
    "weather-proofing": (
        "practical building-maintenance compound with low academic transferability",
        "",
        "high",
    ),
}

OVERRIDES = {
    "recession": "\n".join(
        [
            "핵심 뜻: 경기 침체",
            "부가 뜻: 경기 후퇴 / 불경기",
            "핵심 느낌: 경제 전체의 움직임이 눈에 띄게 꺾인 상태",
        ]
    ),
    "oversight": "\n".join(
        [
            "핵심 뜻: 감독 / 감시",
            "부가 뜻: 문맥에 따라 실수로 빠뜨림이란 뜻도 있음",
            "핵심 느낌: 위에서 계속 살피며 놓치는 게 없게 관리하는 일",
        ]
    ),
    "executive": "\n".join(
        [
            "핵심 뜻: 집행의 / 운영을 맡는",
            "부가 뜻: 인지에서는 계획·조절을 맡는 실행 기능의",
            "핵심 느낌: 전체가 굴러가게 조정하고 실행을 챙기는 쪽",
        ]
    ),
    "mindset": "\n".join(
        [
            "핵심 뜻: 사고방식 / 마음가짐",
            "부가 뜻: 상황과 능력을 해석하는 기본 태도",
            "핵심 느낌: 같은 일을 봐도 반응 방향을 미리 정해 두는 마음의 틀",
        ]
    ),
    "sociocultural": "\n".join(
        [
            "핵심 뜻: 사회문화적인",
            "부가 뜻: 사회적 관계와 문화적 배경이 함께 작용하는",
            "핵심 느낌: 개인 안보다 사회와 문화의 영향 속에서 형성되는 쪽",
        ]
    ),
    "evaluation": "\n".join(
        [
            "핵심 뜻: 평가 / 판단",
            "부가 뜻: 기준을 세워 좋고 나쁨이나 타당성을 가리는 일",
            "핵심 느낌: 그냥 설명하는 게 아니라 값을 매기고 판정하는 단계",
        ]
    ),
    "username": "\n".join(
        [
            "핵심 뜻: 사용자 이름",
            "부가 뜻: 계정을 식별하는 로그인 이름",
            "핵심 느낌: 시스템이 나를 알아보는 계정 이름표",
        ]
    ),
    "passcode": "\n".join(
        [
            "핵심 뜻: 인증 코드 / 비밀번호 코드",
            "부가 뜻: 접속이나 본인 확인에 쓰는 짧은 코드",
            "핵심 느낌: 잠긴 문을 여는 짧은 인증 열쇠",
        ]
    ),
    "barcode": "\n".join(
        [
            "핵심 뜻: 바코드 / 막대형 식별 코드",
            "부가 뜻: 스캔으로 상품이나 자료 정보를 읽는 코드",
            "핵심 느낌: 찍으면 숨은 식별 정보가 열리는 줄무늬 표식",
        ]
    ),
    "keycard": "\n".join(
        [
            "핵심 뜻: 출입 카드",
            "부가 뜻: 문을 열거나 출입 권한을 확인하는 카드",
            "핵심 느낌: 찍으면 접근 권한이 열리는 카드 열쇠",
        ]
    ),
}


def update_ets_files() -> list[str]:
    removed = []
    for rel_path in sorted(glob.glob(ETS_PATTERN)):
        path = ROOT / rel_path
        updated_rows = []
        changed = False
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            for headword, back in reader:
                if headword in REMOVE_HEADWORDS:
                    removed.append(headword)
                    changed = True
                    continue
                if headword in OVERRIDES and back != OVERRIDES[headword]:
                    back = OVERRIDES[headword]
                    changed = True
                updated_rows.append([headword, back])

        if changed:
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                writer.writerows(updated_rows)
    return removed


def update_rejected(removed: list[str]) -> None:
    existing = set()
    rows = []
    with REJECTED_PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        rows = list(reader)
        for row in rows[1:]:
            if row:
                existing.add(row[0])

    for headword in removed:
        if headword in existing:
            continue
        reason, near_duplicate_of, confidence = REMOVE_HEADWORDS[headword]
        rows.append([headword, reason, near_duplicate_of, confidence])

    with REJECTED_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)


def main() -> int:
    removed = update_ets_files()
    update_rejected(removed)
    print(f"removed={len(removed)}")
    print("removed_headwords=" + ",".join(sorted(removed)))
    print(f"overrides={len(OVERRIDES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
