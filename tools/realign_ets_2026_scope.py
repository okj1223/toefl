#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlencode


TARGETS = {
    "toefl_ets_2026_set_06.tsv": [
        "acculturation",
        "clan",
        "ethnography",
        "folklore",
        "hinterland",
        "kinship",
        "patriarchal",
        "tribal",
        "xenophobia",
        "hegemony",
        "nomadic",
        "pilgrimage",
    ],
    "toefl_ets_2026_set_07.tsv": [
        "morbidity",
        "etiology",
        "biopsy",
        "anesthesia",
        "sedation",
        "lesion",
        "tumor",
        "malignant",
        "benign",
        "pathogen",
        "antigen",
        "autoimmune",
        "carcinogen",
        "genome",
        "chromosome",
        "allele",
        "phenotype",
        "genotype",
        "apoptosis",
        "fibrosis",
        "synapse",
        "cortex",
        "autonomic",
        "hippocampus",
        "epidemiology",
    ],
    "toefl_ets_2026_set_08.tsv": [
        "didactic",
        "heuristic",
        "metacognition",
        "interleave",
        "declarative",
        "episodic",
        "andragogy",
        "constructivism",
        "behaviorism",
        "cognitivism",
        "rote",
        "proximal",
        "psychomotor",
        "praxis",
        "chunking",
        "mnemonic",
    ],
    "toefl_ets_2026_set_09.tsv": [
        "celestial",
        "orbital",
        "asteroid",
        "comet",
        "galaxy",
        "galactic",
        "stellar",
        "lunar",
        "eclipse",
        "gravitational",
        "quantum",
        "luminosity",
        "interstellar",
        "stratosphere",
        "troposphere",
        "geothermal",
        "glacial",
        "sedimentary",
        "tectonics",
        "magma",
        "basalt",
        "granite",
        "aquifer",
        "isotope",
        "viscosity",
        "reactant",
        "reagent",
        "ionize",
    ],
    "toefl_ets_2026_set_11.tsv": [
        "afforestation",
        "agroforestry",
        "aridity",
        "biofuel",
        "biomass",
        "biosphere",
        "catchment",
        "climatology",
        "effluent",
        "eutrophication",
        "geomorphology",
        "hydrology",
        "leachate",
        "microclimate",
        "mineralization",
        "monoculture",
        "overharvest",
        "overirrigation",
        "peatland",
        "phytoplankton",
        "rangeland",
        "riparian",
        "salinization",
        "scrubland",
        "sequestration",
        "topsoil",
        "tributary",
        "windborne",
        "albedo",
        "ecotone",
        "geochemical",
        "geospatial",
        "hydroelectric",
        "mangrove",
        "phytoremediation",
        "sedimentation",
        "snowpack",
        "subsidence",
        "thermodynamic",
        "turbidity",
        "upwelling",
        "anthropocene",
        "methane",
        "nitrogen",
    ],
}


REPLACEMENT_POOL = [
    "adapt",
    "adjust",
    "advocate",
    "agenda",
    "alternative",
    "construct",
    "contribute",
    "discuss",
    "document",
    "draft",
    "dynamic",
    "empirical",
    "evaluate",
    "illustrate",
    "instruct",
    "method",
    "moderate",
    "organize",
    "practical",
    "priority",
    "revise",
    "schedule",
    "selective",
    "strengthen",
    "summarize",
    "update",
    "valid",
    "advancement",
    "alignment",
    "applicability",
    "assignment",
    "clarification",
    "collaboration",
    "communication",
    "consistency",
    "continuity",
    "contribution",
    "coordination",
    "discussion",
    "documentation",
    "effectiveness",
    "enhancement",
    "explanation",
    "feasibility",
    "implementation",
    "instruction",
    "interaction",
    "interpretation",
    "organization",
    "participation",
    "preparation",
    "prioritization",
    "revision",
    "utilization",
    "actionable",
    "adaptable",
    "balanced",
    "communicative",
    "contextual",
    "decision",
    "descriptive",
    "editorial",
    "educational",
    "explanatory",
    "generalizable",
    "guided",
    "informative",
    "managerial",
    "operational",
    "organizational",
    "purposeful",
    "readiness",
    "responsive",
    "scalable",
    "supportive",
    "targeted",
    "workable",
    "blueprint",
    "briefing",
    "checkpoint",
    "coursework",
    "deliverable",
    "design",
    "facilitation",
    "guideline",
    "milestone",
    "overview",
    "planning",
    "presentation",
    "progress",
    "proposal",
    "review",
    "roadmap",
    "teamwork",
    "timeline",
    "training",
    "usable",
    "variance",
]


EXTRA_POOL = [
    "reflection",
    "summary",
    "recommendation",
    "comparison",
    "guidance",
    "initiative",
    "coordination",
    "completion",
    "orientation",
    "adjustment",
    "collaborative",
    "observational",
    "participatory",
    "preparatory",
    "organizationally",
    "strategically",
    "accommodative",
    "analytical",
    "appraisive",
    "coordinated",
    "descriptively",
    "developmental",
    "diagnostic",
    "evaluative",
    "instructional",
    "interpretive",
    "manageable",
    "negotiable",
    "organizational",
    "persuasive",
    "procedural",
    "productive",
    "reflective",
    "responsive",
    "structured",
    "supportive",
    "transferable",
    "action-oriented",
    "goal-oriented",
    "evidence-based",
    "peer-reviewed",
    "well-defined",
    "broad-based",
    "context-aware",
    "result-oriented",
    "student-centered",
    "team-based",
    "task-oriented",
    "time-sensitive",
    "user-friendly",
]


def translate_word(word: str) -> str:
    query = urlencode({"client": "gtx", "sl": "en", "tl": "ko", "dt": "t", "q": word})
    try:
        result = subprocess.run(
            [
                "curl",
                "-L",
                "--silent",
                "--show-error",
                "--connect-timeout",
                "4",
                "--max-time",
                "8",
                f"https://translate.googleapis.com/translate_a/single?{query}",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        value = json.loads(result.stdout)[0][0][0]
        return re.sub(r"\s+", " ", value).strip().rstrip(".。")
    except Exception:
        return word


def build_back(word: str) -> str:
    ko = translate_word(word)
    return "\n".join(
        [
            f"핵심 뜻: {ko}",
            f"부가 뜻: {ko}와 관련된 의미 / 문맥에 따라 세부 해석",
            f"핵심 느낌: 학술 문맥에서 {ko}의 방향을 잡는 느낌",
            f"구분: {word}=핵심 의미 중심 / related=연관된 의미 / context=문맥상 구분",
        ]
    )


def read_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.reader(handle, delimiter="\t"))


def write_rows(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)


def main() -> int:
    all_paths = sorted(Path(".").glob("toefl_ets_2026_set_*.tsv"))
    all_rows = {path.name: read_rows(path) for path in all_paths}

    target_words = {word for words in TARGETS.values() for word in words}
    used = {
        row[0]
        for name, rows in all_rows.items()
        for row in rows
        if row and row[0] not in target_words
    }

    pool = [word for word in REPLACEMENT_POOL + EXTRA_POOL if word not in used]
    pool_index = 0
    changes = []

    for filename, words_to_replace in TARGETS.items():
        rows = all_rows[filename]
        replace_set = set(words_to_replace)
        for row in rows:
            if row[0] not in replace_set:
                continue
            while pool_index < len(pool) and pool[pool_index] in used:
                pool_index += 1
            if pool_index >= len(pool):
                raise RuntimeError("replacement pool exhausted")
            new_word = pool[pool_index]
            pool_index += 1
            old_word = row[0]
            row[0] = new_word
            row[1] = build_back(new_word)
            used.add(new_word)
            changes.append((filename, old_word, new_word))
        write_rows(Path(filename), rows)

    for filename, old_word, new_word in changes:
        print(f"{filename}\t{old_word}\t->\t{new_word}")
    print(f"changed={len(changes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
