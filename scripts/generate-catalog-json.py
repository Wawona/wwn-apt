#!/usr/bin/env python3
"""Merge catalog/modules/*.yaml and bundled.yaml into rootfs JSON artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODULES_DIR = ROOT / "catalog" / "modules"
DEFAULT_BUNDLED = ROOT / "catalog" / "bundled.yaml"


def load_modules(modules_dir: Path) -> list[dict]:
    modules: list[dict] = []
    for path in sorted(modules_dir.glob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        if not isinstance(doc, dict):
            raise ValueError(f"{path}: expected mapping")
        modules.append(doc)
    return modules


def load_bundled(bundled_path: Path) -> dict:
    with bundled_path.open(encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    if not isinstance(doc, dict) or "components" not in doc:
        raise ValueError(f"{bundled_path}: expected components list")
    return doc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "modules_dir",
        type=Path,
        nargs="?",
        default=DEFAULT_MODULES_DIR,
    )
    parser.add_argument(
        "--bundled",
        type=Path,
        default=DEFAULT_BUNDLED,
        help="Required bundled components YAML",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Write catalog.json, modules.jsonl, and bundled.json here",
    )
    args = parser.parse_args()

    modules = load_modules(args.modules_dir)
    modules.sort(key=lambda m: m["id"])
    bundled = load_bundled(args.bundled)

    bundled_ids = {c["id"] for c in bundled["components"]}
    overlap = bundled_ids & {m["id"] for m in modules}
    if overlap:
        print(
            f"Catalog module id(s) collide with required bundled software: {sorted(overlap)}",
            file=sys.stderr,
        )
        return 1

    payload = {"schema_version": 1, "modules": modules}

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        json_path = args.output_dir / "catalog.json"
        jsonl_path = args.output_dir / "modules.jsonl"
        bundled_path = args.output_dir / "bundled.json"
    else:
        json_path = Path("catalog.json")
        jsonl_path = Path("modules.jsonl")
        bundled_path = Path("bundled.json")

    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for mod in modules:
            fh.write(json.dumps(mod, separators=(",", ":")) + "\n")
    bundled_path.write_text(json.dumps(bundled, indent=2) + "\n", encoding="utf-8")

    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
