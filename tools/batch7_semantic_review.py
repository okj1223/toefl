#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DELETIONS = {
    "toefl_ets_2026_set_21.tsv": {
        "bridge-building",
        "consent-based",
        "status-seeking",
        "trust-building",
        "volunteer-based",
    },
    "toefl_ets_2026_set_22.tsv": {
        "climate-informed",
        "climate-proof",
        "climate-ready",
        "conservation-oriented",
        "flood-mitigation",
        "long-horizon",
        "low-consumption",
        "low-footprint",
        "low-maintenance",
        "low-regret",
        "resilience-oriented",
        "restoration-oriented",
        "reuse-oriented",
        "sustainability-oriented",
        "weather-resilient",
    },
    "toefl_ets_2026_set_23.tsv": {
        "autosave",
        "barcode",
        "buspass",
        "campus",
        "checkin",
        "checkout",
        "classmate",
        "filename",
        "folder",
        "followup",
        "grammarcheck",
        "headsup",
        "quickstart",
        "roommate",
        "scanner",
        "service",
        "signoff",
        "signup",
        "soundcheck",
        "teammate",
        "walkin",
        "wordcount",
    },
    "toefl_ets_2026_set_24.tsv": {
        "annualized",
        "datapoint",
        "denominator",
        "downward",
        "monotonically",
        "normalization",
        "numerator",
        "observability",
        "sensitivity",
        "specificity",
        "thresholding",
        "timepoint",
        "upward",
    },
}


REPLACEMENTS = {
    "toefl_ets_2026_set_21.tsv": {
        "agenda-setting": "핵심 뜻: 의제 설정 / 논의 방향 정하기\n구분: agenda-setting=공론장의 논의 우선순위를 정함 / prioritization=우선순위 정하기",
        "allyship": "핵심 뜻: 연대적 지지 / 연대 행동\n구분: allyship=당사자와 함께하는 지지와 연대 / sympathy=공감 / sponsorship=공식 후원",
        "bystander": "핵심 뜻: 방관자 / 곁에 있던 사람\n구분: bystander=현장에 있으나 개입하지 않는 사람 / witness=목격자",
        "unanimity": "핵심 뜻: 만장일치 / 전원 합의\n구분: unanimity=전원이 같은 결론에 동의함 / consensus=대체로 함께 받아들일 수 있는 합의",
        "facilitative": "핵심 뜻: 촉진적인 / 참여를 돕는\n구분: facilitative=과정과 참여를 촉진하는 / directive=지시적인",
    },
    "toefl_ets_2026_set_22.tsv": {
        "carbon-neutral": "핵심 뜻: 탄소중립의\n구분: carbon-neutral=순탄소배출을 상쇄해 균형을 맞춘 / low-emission=배출이 적은",
        "preparedness": "핵심 뜻: 대비 태세 / 사전 대비 수준\n구분: preparedness=사전 대비 수준 / readiness=실행 준비 상태",
        "resource-efficient": "핵심 뜻: 자원 효율적인\n구분: resource-efficient=자원 투입 대비 효율이 높은 / cost-effective=비용 대비 효과가 좋은",
        "greenwashing": "핵심 뜻: 위장 친환경 홍보 / 그린워싱\n구분: greenwashing=실제보다 친환경적으로 과장 포장함 / branding=이미지 구축",
        "future-proofing": "핵심 뜻: 미래 대비 보강 / 선제 설계\n구분: future-proofing=앞으로의 변화에도 버티게 미리 설계함 / maintenance=현재 상태를 유지함",
        "scarcity": "핵심 뜻: 희소성 / 부족 상태\n구분: scarcity=수요에 비해 자원이 부족한 상태 / shortage=당장의 부족",
        "low-impact": "핵심 뜻: 환경 부담이 적은\n구분: low-impact=주변 환경 부담이 작은 / low-emission=배출이 적은",
    },
    "toefl_ets_2026_set_23.tsv": {
        "reschedule": "핵심 뜻: 일정을 다시 잡다\n구분: reschedule=일정을 다시 잡다 / postpone=뒤로 미루다 / cancel=취소하다",
        "shortlist": "핵심 뜻: 최종 후보로 추리다 / 압축해 추리다\n구분: shortlist=최종 후보로 추리다 / select=선정하다 / exclude=제외하다",
        "proofread": "핵심 뜻: 교정하다 / 오탈자를 점검하다\n구분: proofread=오탈자 교정 / revise=내용 수정 / edit=편집하다",
        "waiver": "핵심 뜻: 면제서 / 면제 승인\n구분: waiver=면제서 또는 면제 승인 / exemption=면제 / permit=허가",
        "stipend": "핵심 뜻: 정액 지원금 / 생활 지원금\n구분: stipend=정액 지원금 / salary=급여 / grant=지원금",
        "availability": "핵심 뜻: 가능 시간 / 이용 가능성\n구분: availability=가능 여부·가능 시간 / accessibility=접근 가능성",
        "registrar": "핵심 뜻: 학사 등록 담당 부서\n구분: registrar=학사 등록·기록을 맡는 부서 / advisor=지도교수·상담자 / office=사무실",
        "turnaround": "핵심 뜻: 처리 소요 시간 / 회신 속도\n구분: turnaround=처리 소요 시간 / deadline=마감 시한 / duration=지속 시간",
        "leadtime": "핵심 뜻: 사전 준비 기간\n구분: leadtime=사전 소요 기간 / timeframe=기간 틀 / delay=지연",
        "troubleshooting": "핵심 뜻: 문제 해결 점검 / 오류 해결\n구분: troubleshooting=오류 원인 해결 / repair=수리 / diagnosis=진단",
    },
    "toefl_ets_2026_set_24.tsv": {
        "approximation": "핵심 뜻: 근사치 / 어림값\n구분: approximation=근사치 / estimate=추정치 / exact value=정확한 값",
        "outlier": "핵심 뜻: 이상치 / 유난한 값\n구분: outlier=이상치 / anomaly=이례 현상 / exception=예외",
        "forecast": "핵심 뜻: 예측하다 / 전망하다\n구분: forecast=미래를 예측하다 / predict=예측하다 / estimate=어림하다",
        "dispersion": "핵심 뜻: 산포 / 퍼짐 정도\n구분: dispersion=퍼짐 정도 / concentration=한곳에 모임",
        "plateau": "핵심 뜻: 정체 구간 / 고원 상태\n구분: plateau=상승이 멈춘 평평한 구간 / peak=가장 높은 한 점",
        "shortfall": "핵심 뜻: 부족분 / 목표 미달분\n구분: shortfall=부족분 / deficit=적자·결손 / gap=차이",
        "breakdown": "핵심 뜻: 세부 내역 / 항목별 구분\n구분: breakdown=항목별로 쪼갠 내역 / total=전체 합계",
        "volatility": "핵심 뜻: 변동성\n구분: volatility=변동성 / variability=퍼짐 정도 / instability=불안정성",
        "deterioration": "핵심 뜻: 악화 / 저하\n구분: deterioration=악화 / decline=감소 / degradation=저하",
        "traceability": "핵심 뜻: 추적 가능성\n구분: traceability=추적 가능성 / accountability=책임성 / transparency=투명성",
    },
}


REJECTED_APPEND = [
    "bridge-building\tmetaphoric social-process compound with lower standalone vocabulary value\t\thigh",
    "trust-building\tprocess-label compound better handled through broader trust vocabulary\t\thigh",
    "status-seeking\tsocial-behavior compound with lower broad TOEFL transferability\t\thigh",
    "volunteer-based\tcompound descriptor with limited standalone payoff\t\thigh",
    "consent-based\tprocess descriptor better handled through broader consent vocabulary\t\thigh",
    "conservation-oriented\tjargon-heavy climate descriptor with limited standalone payoff\t\thigh",
    "flood-mitigation\tnarrow hazard-management compound with low cross-topic transferability\t\thigh",
    "restoration-oriented\tjargon-heavy environmental descriptor with limited standalone payoff\t\thigh",
    "weather-resilient\tcompound descriptor with narrower payoff than broader resilience vocabulary\t\thigh",
    "climate-informed\tpolicy-planning compound with lower standalone vocabulary value\t\thigh",
    "climate-proof\tpolicy/engineering compound with low standalone transferability\t\thigh",
    "climate-ready\tpolicy-planning compound with low standalone transferability\t\thigh",
    "low-maintenance\tconsumer/product-style descriptor with weak academic payoff\t\tmedium",
    "low-footprint\tenvironmental slogan-like compound with low standalone value\t\thigh",
    "low-regret\tpolicy-jargon compound with low standalone TOEFL payoff\t\thigh",
    "long-horizon\tcompound descriptor better handled through broader long-term vocabulary\t\tmedium",
    "reuse-oriented\tjargon-heavy sustainability descriptor with limited standalone payoff\t\thigh",
    "low-consumption\tcompound descriptor with lower payoff than broader efficiency vocabulary\t\tmedium",
    "resilience-oriented\tjargon-heavy planning descriptor with limited standalone payoff\t\thigh",
    "sustainability-oriented\tjargon-heavy planning descriptor with limited standalone payoff\t\thigh",
    "signup\tUI/process label with low standalone Band-5 vocabulary value\t\thigh",
    "signoff\tworkflow label with low broad TOEFL transferability\t\thigh",
    "checkin\tUI/process label with low standalone vocabulary value\t\thigh",
    "checkout\tUI/process label with low standalone vocabulary value\t\thigh",
    "walkin\tservice-desk label with low broad TOEFL transferability\t\thigh",
    "headsup\tinformal colloquial label with low academic usefulness\t\thigh",
    "filename\tsoftware UI label with low standalone TOEFL value\t\thigh",
    "folder\ttoo basic as a standalone Band-5 target in this set\t\thigh",
    "barcode\tproduct/labeling term with low broad academic transferability\t\thigh",
    "buspass\tcampus-life specific noun with low broad TOEFL reuse\t\thigh",
    "classmate\ttoo basic for target band\t\thigh",
    "teammate\ttoo basic for target band\t\thigh",
    "roommate\ttoo basic for target band\t\thigh",
    "campus\ttoo basic for target band\t\thigh",
    "service\ttoo broad/basic for standalone focus in this supplement\t\thigh",
    "wordcount\tUI/task label with low standalone vocabulary payoff\t\thigh",
    "grammarcheck\tawkward tool label with low standalone academic value\t\thigh",
    "scanner\ttoo basic/product-specific for target band\t\tmedium",
    "quickstart\tsoftware/help label with low standalone TOEFL value\t\thigh",
    "soundcheck\tevent-tech label with low broad academic transferability\t\thigh",
    "timepoint\tnarrow stats/research noun with lower broad payoff than broader time vocabulary\t\thigh",
    "datapoint\tnarrow analytics noun with lower broad payoff than broader data vocabulary\t\thigh",
    "denominator\tmath-specific term with low broad TOEFL transferability\t\thigh",
    "numerator\tmath-specific term with low broad TOEFL transferability\t\thigh",
    "sensitivity\ttechnical diagnostic-statistics term with limited broad reuse\t\thigh",
    "specificity\ttechnical diagnostic-statistics term with limited broad reuse\t\thigh",
    "normalization\ttechnical data-processing term with lower broad transferability\t\thigh",
    "thresholding\ttechnical processing term likely to be glossed if needed\t\thigh",
    "observability\tnarrow measurement concept with lower payoff than broader measurable/observable vocabulary\t\thigh",
    "annualized\tfinance/reporting-specific adjective with limited cross-topic reuse\t\thigh",
    "upward\ttoo basic as a standalone Band-5 target\t\thigh",
    "downward\ttoo basic as a standalone Band-5 target\t\thigh",
    "monotonically\tnarrow mathematical adverb with low broad TOEFL transferability\t\thigh",
]


DUPLICATES_APPEND = [
    "toefl_ets_2026_set_23.tsv:15\tfollow-up\tremoved semantic duplicate already covered in ETS campus set (toefl_ets_2026_set_13.tsv:25)",
    "toefl_ets_2026_set_23.tsv:96\tauto-save\tremoved semantic duplicate already covered in ETS digital set (toefl_ets_2026_set_15.tsv:95)",
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
        "toefl_ets_2026_set_21.tsv",
        "toefl_ets_2026_set_22.tsv",
        "toefl_ets_2026_set_23.tsv",
        "toefl_ets_2026_set_24.tsv",
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
    append_unique_lines(ROOT / "duplicates_removed.tsv", DUPLICATES_APPEND)
    print(f"changed_files={changed_files} changed_rows={changed_rows} removed_rows={removed_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
