#!/usr/bin/env python3
"""Ensure optional module catalog ids remain stable (anchor check for CI)."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(1)

OPTIONAL_MODULES = frozenset({"foot", "neovim", "fastfetch"})
BUNDLED_COMPONENTS = frozenset({"zsh", "coreutils", "waypipe", "apt"})


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    modules_dir = root / "catalog" / "modules"
    bundled_path = root / "catalog" / "bundled.yaml"

    found = {p.stem for p in modules_dir.glob("*.yaml")}
    missing = OPTIONAL_MODULES - found
    extra = found - OPTIONAL_MODULES
    if missing:
        print(f"Missing optional modules: {sorted(missing)}", file=sys.stderr)
    if extra:
        print(f"Unexpected optional modules: {sorted(extra)}", file=sys.stderr)

    with bundled_path.open(encoding="utf-8") as fh:
        bundled_doc = yaml.safe_load(fh)
    bundled_ids = {c["id"] for c in bundled_doc["components"]}
    if bundled_ids != BUNDLED_COMPONENTS:
        print(
            f"Bundled component ids changed (expected {sorted(BUNDLED_COMPONENTS)}): "
            f"{sorted(bundled_ids)}",
            file=sys.stderr,
        )
        return 1

    if missing or extra:
        return 1

    overlap = found & bundled_ids
    if overlap:
        print(f"Optional modules overlap bundled ids: {sorted(overlap)}", file=sys.stderr)
        return 1

    print("Catalog module anchors OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
