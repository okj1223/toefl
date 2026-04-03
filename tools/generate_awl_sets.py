#!/usr/bin/env python3
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import html
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote, urlencode


AWL_DICT_URL = "https://www.eapfoundation.com/vocab/academic/awllists/dic7.php?word="
TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


def strip_tags(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_awl_entries(source_html: Path) -> list[dict[str, object]]:
    text = source_html.read_text(encoding="utf-8")
    rows = re.findall(
        r"<tr><td><a[^>]*><b>([^<]+)</b></a></td><td>(\d+)</td><td>(.*?)</td></tr>",
        text,
        flags=re.S,
    )
    entries = []
    for headword, sublist, related_html in rows:
        related_forms = [form for form in re.findall(r">([^<]+)</a>", related_html) if form]
        entries.append(
            {
                "headword": html.unescape(headword).strip(),
                "sublist": int(sublist),
                "related_forms": related_forms,
            }
        )
    return entries


def fetch_url(url: str, timeout: int = 8) -> str:
    result = subprocess.run(
        [
            "curl",
            "-L",
            "--silent",
            "--show-error",
            "--connect-timeout",
            "4",
            "--max-time",
            str(timeout),
            url,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def translate_en_to_ko(text: str) -> str:
    query = urlencode({"client": "gtx", "sl": "en", "tl": "ko", "dt": "t", "q": text})
    try:
        payload = fetch_url(f"{TRANSLATE_URL}?{query}")
        translated = json.loads(payload)[0][0][0]
        return normalize_ko(translated)
    except Exception:
        return text


def normalize_ko(text: str) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    value = value.rstrip(".。 ")
    replacements = {
        "다.": "다",
        "합니다": "하다",
        "됩니다": "되다",
        "있습니다": "있다",
        "없습니다": "없다",
    }
    for src, dst in replacements.items():
        if value.endswith(src):
            value = value[: -len(src)] + dst
    return value


def parse_dictionary_entry(headword: str) -> dict[str, object]:
    try:
        raw_html = fetch_url(f"{AWL_DICT_URL}{quote(headword)}")
    except Exception:
        return {
            "pos": "",
            "definitions": [headword],
            "synonyms": [],
        }
    pos_match = re.search(r"<p><i>([^<]+)</i></p>", raw_html)
    pos = strip_tags(pos_match.group(1)) if pos_match else ""

    definition_blocks = re.findall(r"<p class='indentwn'>(.*?)</p>", raw_html, flags=re.S)
    definitions = []
    synonyms: list[str] = []
    for block in definition_blocks:
        clean = strip_tags(block)
        clean = re.sub(r"\s*E\.g\.:.*$", "", clean).strip()
        clean = re.sub(r"\s*\[Syn:.*$", "", clean).strip()
        clean = re.sub(r"^\d+\.\s*", "", clean).strip()
        if clean:
            definitions.append(clean)

        syn_block = re.search(r"\[Syn:(.*?)\]", block, flags=re.S)
        if syn_block:
            for syn in re.findall(r">([^<]+)</a>", syn_block.group(1)):
                syn = html.unescape(syn).strip().lower()
                if syn and syn != headword.lower() and syn not in synonyms:
                    synonyms.append(syn)

    return {
        "pos": pos,
        "definitions": definitions,
        "synonyms": synonyms[:3],
    }


def infer_core_feel(pos: str, core_ko: str) -> str:
    core = core_ko.strip()
    if pos.startswith("verb"):
        return f"대상이나 상황을 {core} 쪽으로 처리하는 느낌"
    if pos.startswith("adjective"):
        return f"대상이나 상태가 {core} 쪽으로 기울어 있는 느낌"
    if pos.startswith("adverb"):
        return f"행동이나 판단이 {core} 방식으로 이어지는 느낌"
    return f"학술 문맥에서 {core}이라는 핵심 개념을 잡는 느낌"


def build_card(
    entry: dict[str, object],
    cached_dict_entry: dict[str, object] | None = None,
) -> tuple[list[str], dict[str, object]]:
    headword = str(entry["headword"])
    dict_entry = cached_dict_entry or parse_dictionary_entry(headword)
    definitions = list(dict_entry.get("definitions", []))
    synonyms = list(dict_entry.get("synonyms", []))
    pos = str(dict_entry.get("pos", ""))

    if not definitions:
        definitions = [headword]

    core_ko = translate_en_to_ko(definitions[0])
    sub_ko = translate_en_to_ko(definitions[1]) if len(definitions) > 1 else translate_en_to_ko(headword)
    core_feel = infer_core_feel(pos, core_ko)

    if synonyms:
        syn_chunks = [f"{syn}=유사어" for syn in synonyms[:2]]
        distinction = f"{headword}={core_ko} / " + " / ".join(syn_chunks)
    else:
        related_forms = list(entry.get("related_forms", []))[:2]
        if related_forms:
            distinction = f"{headword}=기본형 / " + " / ".join(f"{form}=파생형" for form in related_forms)
        else:
            distinction = f"{headword}=문맥상 핵심 의미를 우선 확인"

    back = "\n".join(
        [
            f"핵심 뜻: {core_ko}",
            f"부가 뜻: {sub_ko}",
            f"핵심 느낌: {core_feel}",
            f"구분: {distinction}",
        ]
    )
    return [headword, back], dict_entry


def build_card_task(
    index: int,
    entry: dict[str, object],
    cached_dict_entry: dict[str, object] | None,
) -> tuple[int, str, list[str], dict[str, object]]:
    row, dict_entry = build_card(entry, cached_dict_entry)
    return index, str(entry["headword"]), row, dict_entry


def write_awl_sets(rows: list[list[str]], output_dir: Path, chunk_size: int) -> list[str]:
    names = []
    for index, start in enumerate(range(0, len(rows), chunk_size), 1):
        chunk = rows[start : start + chunk_size]
        name = f"toefl_awl_set_{index:02d}.tsv"
        path = output_dir / name
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerows(chunk)
        names.append(name)
    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-html", default="/tmp/awl_index.php")
    parser.add_argument("--cache-json", default="/tmp/awl_dictionary_cache.json")
    parser.add_argument("--chunk-size", type=int, default=100)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()

    source_html = Path(args.source_html)
    cache_path = Path(args.cache_json)
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}

    entries = parse_awl_entries(source_html)
    if args.limit > 0:
        entries = entries[: args.limit]

    rows_by_index: dict[int, list[str]] = {}
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(
                build_card_task,
                index,
                entry,
                cache.get(str(entry["headword"])),
            )
            for index, entry in enumerate(entries, 1)
        ]
        for future in as_completed(futures):
            index, headword, row, dict_entry = future.result()
            rows_by_index[index] = row
            cache[headword] = dict_entry
            done += 1
            if done % 20 == 0 or done == len(entries):
                cache_path.write_text(
                    json.dumps(cache, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                print(f"built {done}/{len(entries)}", flush=True)

    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = [rows_by_index[index] for index in range(1, len(entries) + 1)]
    names = write_awl_sets(rows, Path("."), args.chunk_size)
    print(f"written {len(names)} files, {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
