#!/usr/bin/env python3
"""Fail if forbidden legacy APT strings appear in App Store deliverables."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCAN_ROOTS = [
    ROOT / "apt",
    ROOT / "catalog",
    ROOT / "docs",
    ROOT / "dependencies",
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "flake.nix",
    ROOT / ".github" / "workflows",
]

SKIP_SUFFIXES = {".pyc", ".png", ".jpg", ".gif"}

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("repo hostname", re.compile(r"repo\.wawona", re.I)),
    ("legacy apt tool", re.compile(r"apt" + r"-get", re.I)),
    ("sources list", re.compile(r"sources\.list", re.I)),
    ("dpkg scan tool", re.compile(r"dpkg" + r"-scanpackages", re.I)),
    ("procursus", re.compile(r"procursus", re.I)),
    ("sileo", re.compile(r"sileo", re.I)),
    ("zebra pkg mgr", re.compile(r"\bzebra\b", re.I)),
]

FORBIDDEN_JB = "jail" + "break"


def iter_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file():
            files.append(root)
            continue
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix in SKIP_SUFFIXES:
                continue
            files.append(path)
    return files


def main() -> int:
    violations: list[str] = []
    jb_pattern = re.compile(FORBIDDEN_JB, re.I)
    for path in iter_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            violations.append(f"{path}: read error: {exc}")
            continue
        rel = path.relative_to(ROOT)
        for label, pattern in PATTERNS:
            if pattern.search(text):
                violations.append(f"{rel}: forbidden pattern ({label})")
        if jb_pattern.search(text):
            violations.append(f"{rel}: forbidden legacy distribution term")

    if violations:
        print("App Store documentation firewall violations:", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        return 1

    print(f"Checked {len(iter_files())} file(s): no forbidden strings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
