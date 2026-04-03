from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FOCUS_MAP = {
    4: "interpretation, meaning, representation, language, and culture, with vocabulary reusable across multiple academic topics rather than one humanities subfield.",
    5: "claims, evidence, institutions, rules, negotiation, and public decisions across civic/economic contexts, while avoiding one-field legal or finance jargon clusters.",
    6: "population change, social patterns, community, mobility, and place-based comparison, with broad social-science language mixed across contexts.",
    7: "health, risk, outcomes, intervention, and evidence in general academic passages, while avoiding dense medical or genetics terminology clusters.",
    8: "learning, explanation, participation, assessment, and skill development in academic settings, with broad classroom language rather than pedagogy jargon.",
    9: "processes, systems, physical change, measurement, and uncertainty across science passages, while avoiding narrow astronomy/geology/chemistry clusters.",
    10: "general cross-disciplinary academic verbs, adjectives, and adverbs used to explain change, degree, contrast, evidence, and relationships across all TOEFL sections.",
    11: "resources, environmental change, sustainability, tradeoffs, and management, framed with broad cause-effect and policy language rather than niche ecology terms.",
    12: "cognition, motivation, perception, judgment, and behavioral explanation, emphasizing reusable psychology language and avoiding specialist clinical terms.",
    13: "collaboration, seminars, project coordination, academic communication, feedback, and campus workflows, with reusable university-life vocabulary.",
    14: "historical change, continuity, institutions, migration, heritage, and interpretation, while avoiding archaeology-only or era-specific term clusters.",
    15: "digital information, online communication, media use, platforms, data handling, and technology impacts in academic/campus contexts, avoiding narrow computing jargon.",
    16: "systems, adaptation, interaction, mechanisms, and living-process descriptions across science passages, while avoiding biology-only technical clusters.",
    17: "policy, governance, institutions, implementation, social programs, and public outcomes, with broad analytical language and limited bureaucracy jargon.",
    18: "argumentation, critique, interpretation, evidence framing, rhetorical stance, and scholarly communication across reading, speaking, and writing tasks.",
    19: "design, constraints, feasibility, implementation, systems, and innovation in practical problem-solving, while avoiding narrow engineering/materials jargon.",
    20: "creative works, visual/auditory representation, aesthetics, interpretation, and performance, with transferable culture-and-analysis vocabulary.",
    21: "movement, globalization, identity, intercultural contact, belonging, and social integration, using broad social vocabulary rather than migration-only jargon.",
    22: "built environments, infrastructure, housing, transport, access, and public space, emphasizing practical urban language without planning-only jargon clusters.",
    23: "data patterns, comparison, estimation, magnitude, measurement, uncertainty, and trend interpretation across graphs, lectures, and explanations.",
    24: "cause-effect explanation, comparison, classification, synthesis, qualification, and conceptual framing across cross-disciplinary academic discourse.",
    25: "academic response language for stating positions, giving reasons, adding support, qualifying claims, organizing explanations, and revising ideas.",
    26: "seminar and lecture interaction, note-taking, asking/answering questions, peer exchange, clarification, and discussion management.",
    27: "cross-disciplinary academic nouns for processes, structures, relationships, constraints, evidence, and outcomes, mixed across topic areas.",
    28: "cross-disciplinary academic verbs for analyzing, changing, supporting, limiting, comparing, and interpreting, mixed across topic areas.",
    29: "cross-disciplinary academic adjectives and adverbs for degree, scope, certainty, frequency, relation, and evaluation, mixed across topic areas.",
    30: "final mixed high-utility modern academic-life vocabulary spanning reading, listening, speaking, and writing, with no dominant subject cluster.",
}

OLD_RULE_LINE = (
    "Rules: TOEFL 100+ academic vocab aligned with post-2026 TOEFL iBT broad academic language, "
    "not too basic/specialized, Korean quick-recall meanings, 핵심 느낌 short vivid hook, "
    "구분 should compare genuinely confusable words, American spelling, lemma form, EXACTLY 100 records.\n"
)

NEW_RULE_LINE = (
    "Rules: TOEFL 100+ academic vocab aligned with post-2026 TOEFL iBT broad academic language, "
    "not too basic/specialized, Korean quick-recall meanings, 핵심 느낌 short vivid hook, "
    "구분 should compare genuinely confusable words, American spelling, lemma form, EXACTLY 100 records. "
    "Anti-silo rule: do not let one narrow subject dominate the set; cap any single specialist subdomain to roughly 15 cards and prefer transferable academic wording.\n"
)


def rewrite_task_file(path: Path, set_num: int) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("Focus: ") and set_num in FOCUS_MAP:
            lines[i] = f"Focus: {FOCUS_MAP[set_num]}"
            break
    text = "\n".join(lines) + "\n"
    text = text.replace(OLD_RULE_LINE, NEW_RULE_LINE)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def rewrite_prompt_template() -> bool:
    path = ROOT / ".generation_prompt_template.md"
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        "- Cross-disciplinary academic words and modern academic-life language preferred\n",
        "- Cross-disciplinary academic words and modern academic-life language preferred\n"
        "- Anti-silo rule: do not let one narrow subject dominate a set; cap any single specialist subdomain to roughly 15 cards and mix transferable academic wording across contexts\n",
    )
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def rewrite_work_plan() -> bool:
    path = ROOT / "WORK_PLAN.md"
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        "## Immediate Next Actions\n\n"
        "1. Continue ETS expansion one set at a time with quality gates and no hard 3000-card quota.\n"
        "2. Re-run validation after each new set and repair malformed cards immediately.\n"
        "3. Do a semantic polishing pass on machine-generated AWL glosses before final study use.\n"
        "4. Periodically prune overly specialized or duplicate-prone ETS tail candidates.\n",
        "## Set Architecture Redesign\n\n"
        "- Avoid \"one set = one school subject\" design.\n"
        "- Use function-centered and discourse-centered set focuses: evidence, cause-effect, comparison, interpretation, project coordination, data explanation, policy reasoning, and academic response language.\n"
        "- Allow topic variety inside each set, but cap any one narrow specialist subdomain to roughly 15 cards so biology/history/engineering clusters do not take over.\n"
        "- Prefer transferable academic wording that can reappear in multiple TOEFL sections and passage types.\n"
        "- Existing `set_05` to `set_14` need a rebalancing pass under this anti-silo rule before expanding further.\n\n"
        "## Immediate Next Actions\n\n"
        "1. Rewrite `.task_set05.md` to `.task_set30.md` around function-centered, anti-silo focuses.\n"
        "2. Rebalance existing ETS sets `05` to `14` so no set is dominated by one narrow subject cluster.\n"
        "3. Re-run validation after each rewritten set and repair malformed cards immediately.\n"
        "4. Do a semantic polishing pass on machine-generated AWL glosses before final study use.\n",
    )
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = []
    for set_num in range(4, 31):
        path = ROOT / f".task_set{set_num:02d}.md"
        if path.exists() and rewrite_task_file(path, set_num):
            updated.append(path.name)
    if rewrite_prompt_template():
        updated.append(".generation_prompt_template.md")
    if rewrite_work_plan():
        updated.append("WORK_PLAN.md")

    print(f"updated {len(updated)} files")
    for name in updated:
        print(name)


if __name__ == "__main__":
    main()
