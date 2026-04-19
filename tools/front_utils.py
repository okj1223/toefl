#!/usr/bin/env python3
from __future__ import annotations


def extract_headword(front: str) -> str:
    lines = front.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return lines[0].strip() if lines else ""


def extract_pronunciation(front: str) -> str | None:
    lines = front.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if len(lines) < 2:
        return None
    line = lines[1].strip()
    if line.startswith("[") and line.endswith("]") and len(line) > 2:
        return line[1:-1]
    return None


def format_front(headword: str, pronunciation: str | None = None) -> str:
    word = extract_headword(headword)
    if not pronunciation:
        return word
    return f"{word}\n[{pronunciation}]"
