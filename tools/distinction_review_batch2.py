#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REMOVE = {
    "toefl_ets_2026_set_13.tsv": {
        "resilient", "restructure", "secular", "sovereign", "streamline", "transparent",
        "annotation", "eclectic", "envision", "notable", "residual", "tangible",
        "deliverable", "design", "facilitation", "variety", "recoverable", "coverage",
        "planning", "circularity", "presentation", "byproduct", "interconnection",
        "progress", "proposal", "roadmap", "impermeable", "buffer-zone", "teamwork",
        "lowland", "climate-related", "timeline", "training"
    },
    "toefl_ets_2026_set_14.tsv": {
        "nutrient", "overuse", "pasture", "summary", "countermeasure", "reclamation",
        "revitalization", "storage", "spillover", "initiative", "completion", "visibility",
        "sustainable", "vegetation", "transitional", "participatory", "preparatory",
        "desalination", "workflow", "junction", "floodplain", "strategic",
        "accommodating", "analysis", "coordinated", "agent", "roadmapping",
        "evaluative", "instructional", "manageable", "negotiable", "persuasive",
        "vapor", "renewable", "finite", "productive", "structured", "transferable",
        "disruption", "awareness", "attachment", "concentration"
    },
    "toefl_ets_2026_set_15.tsv": {
        "identity", "memory", "mindfulness", "preference", "tendency", "workload",
        "pattern", "drive"
    },
    "toefl_ets_2026_set_16.tsv": {
        "alumni", "attendee", "brainstorm", "bulletin", "coauthor", "correspondence",
        "credential", "excerpt", "faculty", "keynote", "liaison", "logistics",
        "manuscript", "memorandum", "panel", "peer", "poster", "publicize", "floor",
        "recipient", "receptiveness", "reminder", "reservation", "roster",
        "spokesperson", "venue"
    },
    "toefl_ets_2026_set_17.tsv": {
        "acknowledgment", "archiving", "caption", "conferral", "handshake", "readout",
        "recap", "sponsorship", "whiteboard", "continuum", "trace", "chronicle",
        "chronological", "citizenship", "civilization", "community", "craftsmanship",
        "declaration", "descendant", "empire", "enduring", "uncover", "storytelling",
        "pedigree", "chronicler", "kingdom", "legacy", "estate", "merchant", "marker",
        "multicultural", "symbolism", "mobile", "laborer", "journey", "prosperity",
        "vestige", "renaissance"
    },
    "toefl_ets_2026_set_18.tsv": {
        "recorder", "textile", "memorial", "group-based", "vessel", "waterway",
        "artisan", "heirloom", "family-based", "archival", "senior-led",
        "inheritance-based", "workforce", "outlying", "stranded", "algorithmic",
        "cloud-based", "connectivity", "crowdsourced", "curate", "debug", "download",
        "e-commerce", "editable", "formatting", "hyperlink", "infographic", "input",
        "interactive", "livestream", "multimedia", "navigate", "newsletter"
    },
    "toefl_ets_2026_set_19.tsv": {
        "notification", "open-source", "password-protected", "platform", "plugin",
        "podcast", "pop-up", "public-facing", "real-time", "searchable", "shareability",
        "software", "spam", "streaming", "subscribe", "tag", "template", "thumbnail",
        "user-generated", "virtual", "web-based", "wireless", "zoomable",
        "file-sharing", "link-sharing", "scrolling", "webinar", "auto-save",
        "activation", "amplifier", "anatomical", "biosphere", "camouflage", "cellular",
        "compartment", "convergent", "cyclic", "dormancy", "encapsulate", "frictionless",
        "gradational", "hybridize", "inflow", "microstructure", "nutrient-rich",
        "organismal", "overflow", "photosensitive"
    },
    "toefl_ets_2026_set_20.tsv": {
        "reassembly", "recombination", "regenerative", "stabilizer", "survivorship",
        "transboundary", "oxygenation", "self-renewal", "energy-efficient",
        "microhabitat", "moisture-retaining", "multiphase", "budgetary", "federated",
        "incentivize", "inclusionary", "interagency", "jurisdictional", "localize",
        "multi-stakeholder", "redistributive", "subsidize", "unfunded",
        "cross-jurisdictional", "cost-sharing", "defunding", "disbursement",
        "beneficiary", "appropriation", "citizen-facing", "co-funding", "assertive",
        "coherently", "debatable", "disputable", "emphatic", "foreground"
    },
    "toefl_ets_2026_set_21.tsv": {
        "illustrative", "plausibility", "scholarly", "thematic", "perspectival", "voice",
        "attributional", "contrastive", "definitional", "discursive",
        "evidence-backed", "paraphrastic", "persuasively", "recontextualize",
        "rhetorically", "source-critical", "viewpoint-dependent", "bottlenecked",
        "cost-effective", "downtime", "durability", "fit-for-purpose", "future-proof",
        "human-centered", "interchangeable", "load-bearing", "modular", "overhaul",
        "reconfigurable", "retrofit", "robustness", "calculated", "customizable",
        "deployment", "downgrade", "end-user", "error-prone"
    },
    "toefl_ets_2026_set_22.tsv": {
        "fine-grained", "high-throughput", "iterative", "plug-and-play", "post-launch",
        "process-oriented", "quality-assurance", "resource-intensive", "serviceability",
        "streamlined", "underutilized", "upgradable", "design-driven", "go-live",
        "high-availability", "off-the-shelf", "solution-oriented", "co-design",
        "maintainability", "open-ended", "allegorical", "ambience", "choreograph",
        "cinematic", "expressive", "immersive", "improvise", "lyrical", "minimalist",
        "pictorial", "rhythmic", "scene-setting", "silhouette", "spectator", "staging",
        "stylized", "textured", "tonal", "understated", "visualize", "authorial",
        "characterization", "emotive", "impressionistic", "medium-specific", "montage",
        "ornamental", "performer", "poetics", "rehearsed", "scripted", "world-building"
    },
    "toefl_ets_2026_set_23.tsv": {
        "abstract", "audience-centered", "documentary-style", "gestural", "handcrafted",
        "high-contrast", "presentational", "repertoire", "asymmetry", "civic-minded",
        "coalition-building", "consensus-building", "dissenting", "etiquette",
        "interpersonal", "consultative", "identity-based", "subgroup", "turn-taking",
        "cross-sector", "diplomatic", "institutionalized", "value-laden",
        "climate-sensitive", "future-oriented", "low-emission", "resource-efficient",
        "water-stressed", "low-impact", "low-waste", "low-carbon",
        "pollution-intensive", "resource-sharing", "ecosystem-based",
        "low-vulnerability", "rechargeable", "resend", "rebook", "recheck",
        "reapply", "preregister", "dropoff"
    },
    "toefl_ets_2026_set_24.tsv": {
        "pickup", "handoff", "inbox", "outbox", "sender", "salutation", "timeslot",
        "callback", "voicemail", "overrun", "frontdesk", "helpdesk", "workstation",
        "workspace", "markup", "sync", "login", "logout", "timesheet", "queue",
        "waittime", "locker", "shuttle", "doublecheck", "slot", "headcount", "turnout",
        "reopen", "overwrite", "walkthrough", "setup", "spellcheck", "handout",
        "printout", "slides", "projector", "timeframe", "sincerely", "courteous",
        "respectfully", "request"
    },
    "toefl_ets_2026_set_25.tsv": {
        "slope", "uptrend", "downtrend", "spike", "dip", "surge", "increment",
        "decrement", "subset", "metric", "rounding", "weighting", "benchmarking",
        "tabulate", "calibrate", "compare", "rank", "filtering", "ranking", "linear",
        "seasonality", "cyclicality", "deterioration", "stagnation", "acceleration",
        "deceleration", "data-based", "measurability", "traceability", "statistically",
        "numerically", "simultaneously", "cautiously", "substantially", "uniformly",
        "steadily"
    },
}


def main() -> int:
    changed_files = 0
    changed_rows = 0
    for rel, words in REMOVE.items():
        path = ROOT / rel
        rows = []
        changed = False
        with path.open(encoding="utf-8", newline="") as f:
            for front, back in csv.reader(f, delimiter="\t"):
                new_back = back
                if front in words and "\n구분:" in back:
                    new_back = back.split("\n구분:", 1)[0]
                if new_back != back:
                    changed = True
                    changed_rows += 1
                rows.append([front, new_back])
        if changed:
            changed_files += 1
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter="\t", lineterminator="\n")
                writer.writerows(rows)
    print(f"changed_files={changed_files} changed_rows={changed_rows}")


if __name__ == "__main__":
    main()
