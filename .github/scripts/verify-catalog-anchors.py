#!/usr/bin/env python3
"""Ensure catalog module ids remain stable (anchor check for CI)."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(1)

EXPECTED = frozenset({"foot", "neovim", "fastfetch", "waypipe"})


def main() -> int:
    modules_dir = Path(__file__).resolve().parents[1] / "catalog" / "modules"
    found = {p.stem for p in modules_dir.glob("*.yaml")}
    missing = EXPECTED - found
    extra = found - EXPECTED
    if missing:
        print(f"Missing seed modules: {sorted(missing)}", file=sys.stderr)
    if extra:
        print(f"Unexpected modules (update anchor list): {sorted(extra)}", file=sys.stderr)
    if missing or extra:
        return 1
    print("Catalog module anchors OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
