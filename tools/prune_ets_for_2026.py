#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ETS_FILES = sorted(ROOT.glob("toefl_ets_2026_set_[0-9][0-9].tsv"))
REJECTED_PATH = ROOT / "rejected_candidates.tsv"


DROP_WORDS: dict[str, tuple[str, str]] = {
    # 구버전 TOEFL에서 더 흔한 좁은 인문/역사 소재성 어휘
    "acculturation": (
        "older-style narrow anthropology vocabulary; post-2026 TOEFL favors broader modern academic-life language",
        "medium",
    ),
    "assimilation": (
        "too tied to older narrow social-science framing relative to newer practical academic-life language",
        "medium",
    ),
    "clan": (
        "narrow anthropology term with lower post-2026 TOEFL transferability",
        "high",
    ),
    "colonize": (
        "narrow historical-process term; lower utility than broader academic verbs in the post-2026 format",
        "medium",
    ),
    "folklore": (
        "older-style culture-specific topic vocabulary; less aligned with modern practical TOEFL contexts",
        "high",
    ),
    "hegemony": (
        "specialized political-theory term with lower broad TOEFL transferability",
        "high",
    ),
    "hinterland": (
        "niche geography/history term with low broad post-2026 TOEFL reuse",
        "high",
    ),
    "kinship": (
        "niche anthropology term with lower broad post-2026 TOEFL transferability",
        "high",
    ),
    "nomadic": (
        "older-style passage-specific anthropology/geography vocabulary; lower practical reuse",
        "medium",
    ),
    "patriarchal": (
        "narrow theory-loaded social term; kept out to prioritize broadly reusable Band-5 vocabulary",
        "medium",
    ),
    "pilgrimage": (
        "older-style culturally specific passage vocabulary; lower fit for modern practical TOEFL contexts",
        "high",
    ),
    "tribal": (
        "culture-specific and older-style topic vocabulary; lower broad post-2026 TOEFL utility",
        "high",
    ),
    "xenophobia": (
        "topic-specific sociopolitical term with lower broad transferability for the current core set",
        "medium",
    ),
    # 과도하게 세부적인 의생명/인지과학/자연과학 단어
    "allele": ("hyper-specialized genetics term likely to be glossed in passage", "high"),
    "anesthesia": ("specialized medical term beyond broad post-2026 TOEFL core", "high"),
    "andragogy": ("specialized pedagogy term with low broad TOEFL reuse", "high"),
    "antigen": ("specialized immunology term likely to be glossed in passage", "high"),
    "apoptosis": ("hyper-specialized cell-biology term likely to be glossed in passage", "high"),
    "asteroid": ("narrow astronomy object term; lower broad transferability", "medium"),
    "autonomic": ("specialized physiology/neuroscience term", "high"),
    "basalt": ("narrow geology rock term likely to be glossed in passage", "high"),
    "behaviorism": ("specialized school-of-thought term with low broad practical transfer", "high"),
    "benign": ("medical diagnostic adjective; narrower than broad post-2026 TOEFL core", "medium"),
    "biopsy": ("specialized clinical procedure term likely to be glossed in passage", "high"),
    "carcinogen": ("specialized toxicology term likely to be glossed in passage", "high"),
    "celestial": ("older-style astronomy passage vocabulary with lower practical academic-life reuse", "medium"),
    "chromosome": ("specialized genetics term likely to be glossed in passage", "high"),
    "chunking": ("specialized learning-science term; lower broad utility", "high"),
    "cognitivism": ("specialized theory-label term; lower broad TOEFL transferability", "high"),
    "comet": ("narrow astronomy object term; lower broad transferability", "medium"),
    "cortex": ("specialized neuroanatomy term likely to be glossed in passage", "high"),
    "declarative": ("specialized memory-taxonomy adjective in this dataset; lower broad utility", "medium"),
    "didactic": ("narrow pedagogy label with lower post-2026 practical transfer", "high"),
    "eclipse": ("narrow astronomy event term; lower broad transferability", "medium"),
    "episodic": ("specialized memory-taxonomy adjective in this dataset", "medium"),
    "epidemiology": ("specialized medical discipline term", "high"),
    "etiology": ("specialized clinical causation term", "high"),
    "fibrosis": ("hyper-specialized pathology term likely to be glossed in passage", "high"),
    "galactic": ("narrow astronomy adjective; lower practical TOEFL transfer", "medium"),
    "galaxy": ("narrow astronomy noun; lower broad utility than cross-disciplinary academic vocabulary", "medium"),
    "genome": ("specialized genetics term likely to be glossed in passage", "high"),
    "genotype": ("specialized genetics term likely to be glossed in passage", "high"),
    "geothermal": ("niche earth-science term with lower broad post-2026 TOEFL reuse", "medium"),
    "glacial": ("niche earth-science adjective with lower broad transferability", "medium"),
    "granite": ("narrow rock term likely to be glossed in passage", "high"),
    "gravitational": ("physics-specific adjective; lower broad post-2026 TOEFL utility", "medium"),
    "heuristic": ("specialized cognitive-science term; lower broad practical transfer", "medium"),
    "hippocampus": ("specialized neuroanatomy term likely to be glossed in passage", "high"),
    "interleave": ("specialized learning-strategy term; lower broad transferability", "high"),
    "interstellar": ("niche astronomy adjective with low practical academic-life reuse", "high"),
    "ionize": ("specialized chemistry verb likely to be glossed in passage", "high"),
    "isotope": ("specialized chemistry term likely to be glossed in passage", "high"),
    "lesion": ("specialized medical pathology term likely to be glossed in passage", "high"),
    "luminosity": ("niche astronomy/physics term; lower broad transferability", "medium"),
    "lunar": ("narrow astronomy adjective; lower practical TOEFL utility", "medium"),
    "magma": ("narrow geology term likely to be glossed in passage", "high"),
    "malignant": ("specialized clinical adjective; narrower than broad post-2026 TOEFL core", "high"),
    "metacognition": ("specialized education-psychology term; lower broad practical transfer", "medium"),
    "mnemonic": ("specialized memory technique term; lower broad TOEFL transferability", "medium"),
    "morbidity": ("specialized epidemiology term", "high"),
    "orbital": ("narrow astronomy/physics adjective; lower broad practical reuse", "medium"),
    "pathogen": ("specialized microbiology term likely to be glossed in passage", "high"),
    "phenotype": ("specialized genetics term likely to be glossed in passage", "high"),
    "praxis": ("specialized theory term with low broad practical TOEFL transfer", "high"),
    "proximal": ("specialized technical adjective in this dataset; lower broad transferability", "medium"),
    "psychomotor": ("specialized education/psychology term", "high"),
    "quantum": ("physics-specific technical term likely to be topic-glossed", "medium"),
    "reagent": ("specialized chemistry reagent term likely to be glossed in passage", "high"),
    "reactant": ("specialized chemistry term likely to be glossed in passage", "high"),
    "rote": ("specialized pedagogy contrast term with low broad practical utility", "medium"),
    "sedation": ("specialized medical treatment term", "high"),
    "sedimentary": ("narrow geology rock/process adjective", "high"),
    "stratosphere": ("narrow atmospheric-layer term", "high"),
    "stellar": ("niche astronomy adjective with lower practical TOEFL transfer", "medium"),
    "synapse": ("specialized neuroscience term likely to be glossed in passage", "high"),
    "tectonics": ("narrow geology topic term likely to be glossed in passage", "high"),
    "troposphere": ("narrow atmospheric-layer term", "high"),
    "tumor": ("specialized medical noun; narrower than the broad ETS core", "medium"),
    "viscosity": ("specialized physical-property term likely to be glossed in passage", "medium"),
    # 현대적이긴 하지만 지나치게 제품/플랫폼/분석 KPI 쪽으로 좁은 용어
    "browser": ("product/UI-specific term; not a strong standalone Band-5 academic headword", "medium"),
    "cache": ("implementation-specific computing term; lower broad TOEFL transferability", "medium"),
    "clickthrough": ("digital advertising KPI term; too product-specific for the core set", "high"),
    "dashboard": ("software UI noun; lower broad academic transferability as a standalone headword", "medium"),
}


def rejection_reason(headword: str) -> tuple[str, str] | None:
    if " " in headword:
        return (
            "multi-word front violates the one-headword/lemma rule and is better omitted than force-normalized",
            "high",
        )
    if not re.fullmatch(r"[A-Za-z][A-Za-z-]*", headword):
        return (
            "front form is not a clean single English lemma/headword",
            "medium",
        )
    return DROP_WORDS.get(headword)


def read_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [row for row in csv.reader(handle, delimiter="\t") if row]


def write_rows(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)


def append_rejections(records: list[tuple[str, str, str]]) -> None:
    existing: set[tuple[str, str]] = set()
    if REJECTED_PATH.exists():
        with REJECTED_PATH.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    existing.add((row[0], row[1]))

    with REJECTED_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        if REJECTED_PATH.stat().st_size == 0:
            writer.writerow(
                ["candidate", "reason_for_rejection", "near_duplicate_of", "confidence"]
            )
        for candidate, reason, confidence in records:
            if (candidate, reason) in existing:
                continue
            writer.writerow([candidate, reason, "", confidence])
            existing.add((candidate, reason))


def main() -> int:
    total_removed = 0
    rejected_records: list[tuple[str, str, str]] = []

    for path in ETS_FILES:
        rows = read_rows(path)
        kept: list[list[str]] = []
        removed_here: list[str] = []
        for row in rows:
            if len(row) != 2:
                kept.append(row)
                continue
            headword = row[0].strip()
            reason = rejection_reason(headword)
            if reason is None:
                kept.append(row)
                continue
            reason_text, confidence = reason
            removed_here.append(headword)
            rejected_records.append((headword, reason_text, confidence))

        if removed_here:
            write_rows(path, kept)
            total_removed += len(removed_here)
            print(f"{path.name}: removed {len(removed_here)}")
            print("  " + ", ".join(removed_here[:40]))

    append_rejections(rejected_records)
    print(f"total_removed={total_removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
