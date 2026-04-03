from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "toefl_ets_2026_set_08.tsv": {
        "scaffold": ("backbone", "뼈대 / 핵심 지지 구조", "전체를 무너지지 않게 받쳐 주는 중심 구조", "겉의 세부보다 안에서 형태를 버티게 하는 중심줄기", "backbone=중심 지지 구조 / structure=짜임 / framework=전체 틀"),
        "syllabus": ("synopsis", "개요 / 압축 요약", "전체 내용을 짧게 압축해 핵심 흐름을 보여주는 설명", "세부로 길게 들어가기 전에 줄거리만 먼저 접어 보여주는 느낌", "synopsis=압축된 개요 / summary=핵심 요약 / outline=큰 구조"),
        "rubric": ("yardstick", "판단 기준 / 비교 잣대", "얼마나 적절한지 재거나 비교할 때 쓰는 기준", "대상을 옆에 대고 가늠해보는 눈금자 같은 느낌", "yardstick=비교·판단의 잣대 / standard=기준 일반 / criterion=판단 항목"),
        "remediation": ("improvement", "개선 / 더 나아지게 함", "부족하거나 약한 부분을 더 나은 상태로 고치는 과정", "문제점을 놔두지 않고 한 단계 끌어올리는 느낌", "improvement=상태를 더 낫게 함 / correction=오류를 바로잡음 / refinement=더 정교하게 다듬음"),
        "apprenticeship": ("mentorship", "멘토링 / 지도 관계", "경험 있는 사람이 덜 익숙한 사람의 성장과 판단을 도와주는 관계", "혼자 헤매지 않게 옆에서 방향을 잡아주는 연결", "mentorship=경험자가 성장을 돕는 관계 / supervision=진행을 감독함 / training=기술을 익히는 훈련"),
        "taxonomy": ("classification", "분류 / 유형 나누기", "공통점과 차이에 따라 대상을 범주로 나누는 일", "섞여 있는 것을 기준에 따라 칸칸이 나누는 느낌", "classification=기준에 따라 범주로 나눔 / category=나뉜 범주 / ranking=순위를 매김"),
        "automaticity": ("fluency", "유창성 / 막힘없는 처리", "많이 힘들이지 않고 자연스럽고 빠르게 수행하는 능력", "중간에 끊기지 않고 부드럽게 흘러가는 느낌", "fluency=막힘없이 자연스럽게 처리함 / automaticity=거의 자동처럼 수행됨 / accuracy=정확성"),
    },
    "toefl_ets_2026_set_11.tsv": {
        "freshwater": ("supply", "공급 / 제공되는 양", "필요한 자원이나 물품이 들어오거나 제공되는 흐름과 양", "필요한 쪽으로 계속 채워 넣는 흐름", "supply=필요한 것을 공급함·공급량 / reserve=비축분 / demand=수요"),
        "groundwater": ("reserve", "비축분 / 저장된 자원", "바로 쓰지 않고 남겨두거나 쌓아둔 자원", "겉에 바로 안 보여도 뒤에 남겨둔 여분", "reserve=저장해 둔 자원·비축분 / supply=공급량 / stock=보유 재고"),
        "lagoon": ("buffer-zone", "완충 구역 / 경계 완화 지대", "두 영역 사이에서 충격이나 직접 영향을 줄이는 중간 구역", "바로 맞닿지 않게 사이에 둔 쿠션 같은 공간", "buffer-zone=직접 충돌을 줄이는 중간 구역 / boundary=경계선 / interface=접점"),
        "marsh": ("lowland", "저지대 / 낮은 땅", "주변보다 고도가 낮아 흐름이나 축적이 모이기 쉬운 지역", "높은 곳에서 내려온 것이 모이기 쉬운 아래쪽 땅", "lowland=주변보다 낮은 지역 / plain=넓고 평평한 땅 / basin=움푹 들어간 분지"),
        "meteorological": ("climate-related", "기후와 관련된 / 날씨 조건의", "날씨나 장기 기후 조건과 연결된", "현상을 볼 때 대기와 계절 조건 쪽을 같이 보는 느낌", "climate-related=기후 조건과 관련된 / environmental=환경의 / atmospheric=대기의"),
        "reforestation": ("revitalization", "활성화 / 다시 활력을 살림", "약해졌거나 정체된 상태에 다시 힘과 기능을 불어넣음", "꺼져가던 흐름에 다시 생기를 넣어 움직이게 하는 느낌", "revitalization=다시 활력을 살림 / restoration=원래 상태에 가깝게 되돌림 / improvement=개선"),
        "reservoir": ("storage", "저장 / 보관", "나중에 쓰기 위해 자원이나 정보를 모아두는 일 또는 그 공간", "들어온 것을 흘려보내지 않고 한곳에 담아두는 느낌", "storage=모아 두고 보관함 / reserve=비축분 / archive=기록 보관"),
        "watershed": ("turning point", "전환점 / 흐름이 바뀌는 계기", "이후 방향이나 결과가 눈에 띄게 달라지는 중요한 지점", "여기서부터 길이 다른 쪽으로 갈라지는 느낌", "turning point=흐름이 바뀌는 전환점 / milestone=중간 이정표 / threshold=변화가 시작되는 경계"),
        "wetland": ("transitional", "전환기의 / 경계적 성격의", "한 상태에서 다른 상태로 넘어가는 중간 단계나 혼합적 성격의", "완전히 한쪽이 아니라 두 상태 사이에 걸쳐 있는 느낌", "transitional=전환 과정의·중간적 / intermediate=중간 단계의 / temporary=일시적인"),
        "estuary": ("junction", "접합 지점 / 합류점", "두 흐름이나 체계가 만나 이어지는 지점", "따로 오던 선들이 한 곳에서 만나는 마디", "junction=흐름·경로가 만나는 지점 / intersection=교차점 / boundary=경계"),
    },
    "toefl_ets_2026_set_13.tsv": {
        "handout": ("reference sheet", "참고용 요약지 / 한눈에 보는 자료", "필요한 내용을 빠르게 다시 볼 수 있게 압축해 적은 자료", "전체 책 대신 옆에 두고 바로 확인하는 짧은 정리본", "reference sheet=빠르게 참고하는 요약 자료 / handout=나눠주는 자료 / summary=핵심 요약"),
        "fellowship": ("support grant", "지원금 / 후원성 보조금", "학업·연구·활동을 이어가도록 재정적으로 돕는 지원", "혼자 버티게 두지 않고 뒤에서 비용을 받쳐주는 느낌", "support grant=활동을 뒷받침하는 지원금 / scholarship=학업 장학금 / sponsorship=공식 후원"),
        "proceedings": ("meeting record", "회의 기록 / 논의 결과 기록", "회의나 발표에서 나온 핵심 내용과 결정을 남긴 문서", "지나간 말을 흘리지 않고 문서로 고정해 두는 느낌", "meeting record=논의 내용을 남긴 기록 / transcript=발언을 적은 기록문 / summary=핵심 요약"),
        "accreditation": ("validation", "타당성 인정 / 검증 승인", "기준에 맞고 믿을 만하다고 확인해 주는 인정", "그냥 주장하는 게 아니라 확인 절차를 거쳐 맞다고 찍히는 느낌", "validation=타당하다고 확인·인정함 / approval=승인 / certification=자격 인증"),
        "invitation": ("outreach", "참여를 끌어내는 연락 / 외부 연결", "사람이나 집단이 관심을 가지고 들어오도록 먼저 다가가는 소통", "안에서 기다리지 않고 바깥으로 손을 뻗는 느낌", "outreach=외부와 연결하려고 다가감 / invitation=참여를 요청하는 초대 / announcement=공식 알림"),
    },
}


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join(
        [
            f"핵심 뜻: {core}",
            f"부가 뜻: {extra}",
            f"핵심 느낌: {feeling}",
            f"구분: {distinction}",
        ]
    )


def main() -> None:
    cards_by_file = {}
    owner = {}
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            rows = [row for row in csv.reader(f, delimiter="\t") if row]
        cards_by_file[path.name] = rows
        for word, _back in rows:
            if word in owner:
                raise RuntimeError(f"duplicate before rewrite: {word}")
            owner[word] = path.name

    for filename, mapping in REPLACEMENTS.items():
        file_words = {row[0] for row in cards_by_file[filename]}
        for old_word, (new_word, *_rest) in mapping.items():
            if old_word not in file_words:
                raise RuntimeError(f"{old_word} missing in {filename}")
            if new_word in owner and owner[new_word] != filename:
                raise RuntimeError(f"{new_word} already exists in {owner[new_word]}")

    for filename, mapping in REPLACEMENTS.items():
        new_rows = []
        count = 0
        for word, back in cards_by_file[filename]:
            if word in mapping:
                new_word, core, extra, feeling, distinction = mapping[word]
                new_rows.append([new_word, build_back(core, extra, feeling, distinction)])
                count += 1
            else:
                new_rows.append([word, back])
        with (ROOT / filename).open("w", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter="\t", lineterminator="\n").writerows(new_rows)
        print(f"{filename}: {count} replaced")

    ets_words = []
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            ets_words.extend(row[0] for row in csv.reader(f, delimiter="\t") if row)
    (ROOT / ".existing_words.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_ets_headwords.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")

    awl_words = []
    for path in sorted(ROOT.glob("toefl_awl_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            awl_words.extend(row[0] for row in csv.reader(f, delimiter="\t") if row)
    (ROOT / "all_awl_headwords.txt").write_text("\n".join(awl_words) + "\n", encoding="utf-8")
    (ROOT / "all_headwords.txt").write_text("\n".join(sorted(set(ets_words + awl_words))) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
