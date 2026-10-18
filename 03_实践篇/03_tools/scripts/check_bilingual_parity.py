#!/usr/bin/env python3
"""Verify the bilingual layout of this topic: Chinese master plus an english/ mirror.

Conventions, identical to the deep-learning-lab course:

* the file without a language suffix, in the module root tree, is the Chinese master edition;
* every English teaching file lives in ``english/`` at the same relative path;
* servers, tests, fixtures, images and ``SKILL.md`` are language-neutral and exist once, so they
  are registered as exceptions instead of being duplicated;
* every pair cross-links to its counterpart, so readers can always switch language.

Run from anywhere: ``python scripts/check_bilingual_parity.py``. Exits non-zero on any break.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

MODULE = Path(__file__).resolve().parent.parent
ENGLISH_DIR = MODULE / "english"
TEACHING_SUFFIXES = {".md", ".ipynb"}
CHECKPOINT_PART = ".ipynb_checkpoints"

# Language-neutral teaching files that intentionally have no counterpart edition.
EXEMPT = {
    "03_skills/cases/01_weather_skill/w-openweather/SKILL.md": (
        "Machine-facing capability list executed by the Skill runtime; a single edition keeps the "
        "installed package and the repository copy identical."
    ),
}


def teaching_files(root: Path) -> list[Path]:
    """Every markdown or notebook teaching file under ``root``, excluding editor checkpoints."""
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix in TEACHING_SUFFIXES
        and CHECKPOINT_PART not in path.parts
    )


def counterpart(path: Path) -> Path:
    """Mirror a file between the Chinese tree and the english/ tree."""
    if ENGLISH_DIR in path.parents:
        return MODULE / path.relative_to(ENGLISH_DIR)
    return ENGLISH_DIR / path.relative_to(MODULE)


def source_text(path: Path) -> str:
    if path.suffix == ".ipynb":
        notebook = json.loads(path.read_text(encoding="utf-8"))
        return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    return path.read_text(encoding="utf-8")


def check_no_legacy_suffix() -> list[str]:
    return [
        f"legacy language suffix still present: {path.relative_to(MODULE)}"
        for path in MODULE.rglob("*")
        if path.is_file() and ".zh-CN" in path.name
    ]


def check_one_to_one(chinese: list[Path], english: list[Path]) -> list[str]:
    problems: list[str] = []
    chinese_names = {path.relative_to(MODULE).as_posix() for path in chinese}
    english_names = {path.relative_to(ENGLISH_DIR).as_posix() for path in english}

    for path in chinese:
        name = path.relative_to(MODULE).as_posix()
        if name not in english_names:
            problems.append(f"Chinese master without an English edition: {name}")
    for path in english:
        name = path.relative_to(ENGLISH_DIR).as_posix()
        if name not in chinese_names:
            problems.append(f"English edition without a Chinese master: english/{name}")
    return problems


def check_exempt_registry(chinese: list[Path]) -> list[str]:
    problems: list[str] = []
    chinese_names = {path.relative_to(MODULE).as_posix() for path in chinese}
    for name, reason in EXEMPT.items():
        if not (MODULE / name).exists():
            problems.append(f"exempt file no longer exists: {name}")
        elif name not in chinese_names:
            problems.append(f"exempt file is not a teaching file: {name}")
        elif (ENGLISH_DIR / name).exists():
            problems.append(f"exempt file now has an English edition, drop the exemption: {name}")
        if not reason.strip():
            problems.append(f"exempt entry needs a reason: {name}")
    return problems


def check_counterpart_links(files: list[Path]) -> list[str]:
    problems: list[str] = []
    for path in files:
        target = counterpart(path)
        if not target.exists():
            continue
        link = os.path.relpath(target, path.parent).replace(os.sep, "/")
        if link not in source_text(path):
            problems.append(
                f"missing link to counterpart {link}: "
                f"{path.relative_to(MODULE).as_posix()}"
            )
    return problems


def main() -> int:
    legacy = check_no_legacy_suffix()
    chinese = [p for p in teaching_files(MODULE) if ENGLISH_DIR not in p.parents]
    english = teaching_files(ENGLISH_DIR)
    paired = [p for p in chinese if p.relative_to(MODULE).as_posix() not in EXEMPT]

    problems = legacy
    problems += check_one_to_one(paired, english)
    problems += check_exempt_registry(chinese)
    problems += check_counterpart_links(paired + english)

    print(f"Chinese master editions : {len(chinese)} ({len(EXEMPT)} language-neutral)")
    print(f"English editions        : {len(english)}")
    print(f"Counterpart links       : {len(paired + english)} checked")
    if problems:
        print(f"\nFAIL - {len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("\nOK - english/ mirrors the Chinese master tree one to one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
