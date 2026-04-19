#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

from front_utils import extract_headword, extract_pronunciation, format_front

try:
    import eng_to_ipa as eng_to_ipa_lib
except ImportError:  # pragma: no cover - optional fallback for rarer entries
    eng_to_ipa_lib = None


USER_AGENT = "Mozilla/5.0"
CACHE_PATH = Path(__file__).with_name("pronunciation_cache.json")
MANUAL_IPA_OVERRIDES = {
    "bottlenecked": "ˈbɑː.t̬əl.nekt",
    "counterargument": "ˌkaʊn.t̬ɚˈɑːr.ɡjə.mənt",
    "definitional": "ˌdef.əˈnɪʃ.ən.əl",
    "dialogic": "ˌdaɪ.əˈlɑː.dʒɪk",
    "discussant": "dɪˈskʌs.ənt",
    "doublecheck": "ˌdʌb.əlˈtʃek",
    "downregulate": "ˌdaʊnˈreɡ.jə.leɪt",
    "facilitative": "fəˈsɪl.əˌteɪ.t̬ɪv",
    "frontdesk": "ˈfrʌnt.desk",
    "generalizable": "ˈdʒen.ər.əˌlaɪ.zə.bəl",
    "gradational": "ɡrəˈdeɪ.ʃən.əl",
    "inclusionary": "ɪnˈkluː.ʒəˌner.i",
    "leadtime": "ˈliːd.taɪm",
    "maintainability": "meɪnˌteɪ.nəˈbɪl.ə.t̬i",
    "maintainable": "meɪnˈteɪ.nə.bəl",
    "measurability": "ˌmeʒ.ɚ.əˈbɪl.ə.t̬i",
    "microhabitat": "ˌmaɪ.kroʊˈhæb.əˌtæt",
    "operationalize": "ˌɑː.pəˈreɪ.ʃən.əlˌaɪz",
    "organismal": "ˌɔːr.ɡəˈnɪz.məl",
    "parameterize": "pəˈræm.ə.t̬ɚˌaɪz",
    "perspectival": "pɚˈspek.t̬ɪ.vəl",
    "poetics": "poʊˈet̬.ɪks",
    "precolonial": "ˌpriː.kəˈloʊ.ni.əl",
    "preregister": "ˌpriːˈredʒ.ɪ.stɚ",
    "presentational": "ˌprez.ənˈteɪ.ʃən.əl",
    "randomization": "ˌræn.də.məˈzeɪ.ʃən",
    "recommender": "ˌrek.əˈmen.dɚ",
    "reconfigurable": "ˌriː.kənˈfɪɡ.jɚ.ə.bəl",
    "recontextualize": "ˌriː.kənˈteks.tʃu.əˌlaɪz",
    "replicability": "ˌrep.lɪ.kəˈbɪl.ə.t̬i",
    "reusability": "ˌriː.juː.zəˈbɪl.ə.t̬i",
    "roadmapping": "ˈroʊdˌmæp.ɪŋ",
    "serviceability": "ˌsɝː.vɪ.səˈbɪl.ə.t̬i",
    "shareability": "ˌʃer.əˈbɪl.ə.t̬i",
    "timeslot": "ˈtaɪmˌslɑːt",
    "upgradable": "ʌpˈɡreɪ.də.bəl",
    "upregulate": "ˌʌpˈreɡ.jə.leɪt",
    "waittime": "ˈweɪt.taɪm",
    "zoomable": "ˈzuː.mə.bəl",
}


def fetch_cambridge_ipa(word: str) -> str | None:
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="ignore")

    soup = BeautifulSoup(html, "html.parser")
    for selector in (".us.dpron-i .ipa", ".uk.dpron-i .ipa", ".dpron-i .ipa"):
        node = soup.select_one(selector)
        ipa = node.get_text("", strip=True) if node else ""
        if ipa:
            return ipa
    return None


def fetch_eng_to_ipa(word: str) -> str | None:
    if eng_to_ipa_lib is None:
        return None
    candidates = [word]
    if "-" in word:
        candidates.append(word.replace("-", " "))

    for candidate in candidates:
        ipa = eng_to_ipa_lib.convert(candidate).strip().replace("*", "")
        if ipa and ipa.lower() != candidate.lower():
            return ipa
    return None


def fetch_ipa(word: str) -> str:
    override = MANUAL_IPA_OVERRIDES.get(word)
    if override:
        return override

    ipa = fetch_cambridge_ipa(word)
    if ipa:
        return ipa

    ipa = fetch_eng_to_ipa(word)
    if ipa:
        return ipa

    raise RuntimeError(f"IPA not found for: {word}")


def load_cache() -> dict[str, str]:
    if not CACHE_PATH.exists():
        return {}
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.write_text(
        json.dumps(dict(sorted(cache.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def rewrite_file(path: Path, cache: dict[str, str], delay: float) -> tuple[int, int]:
    rows: list[list[str]] = []
    reused = 0
    fetched = 0

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row_no, row in enumerate(reader, 1):
            if len(row) != 2:
                raise RuntimeError(f"{path}:{row_no} has {len(row)} columns, expected 2")

            front, back = row
            headword = extract_headword(front)
            if not headword:
                raise RuntimeError(f"{path}:{row_no} has an empty headword")

            pronunciation = extract_pronunciation(front)
            if pronunciation:
                cache.setdefault(headword, pronunciation)
                reused += 1
            elif headword not in cache:
                cache[headword] = fetch_ipa(headword)
                fetched += 1
                time.sleep(delay)
            else:
                reused += 1

            rows.append([format_front(headword, cache[headword]), back])

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\r\n")
        writer.writerows(rows)
    return reused, fetched


def main() -> int:
    global CACHE_PATH

    parser = argparse.ArgumentParser(
        description="Add a second front-line [IPA] pronunciation to TOEFL TSV cards."
    )
    parser.add_argument("paths", nargs="+", help="TSV files to rewrite in place.")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Delay between dictionary requests in seconds.",
    )
    parser.add_argument(
        "--cache-path",
        type=Path,
        default=CACHE_PATH,
        help="Optional JSON cache path for headword to IPA mappings.",
    )
    args = parser.parse_args()

    CACHE_PATH = args.cache_path
    cache = load_cache()

    for raw_path in args.paths:
        path = Path(raw_path)
        reused, fetched = rewrite_file(path, cache=cache, delay=args.delay)
        print(f"updated={path} reused={reused} fetched={fetched}")
        save_cache(cache)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
