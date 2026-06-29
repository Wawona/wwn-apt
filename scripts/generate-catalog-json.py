#!/usr/bin/env python3
"""Merge catalog/modules/*.yaml into catalog.json and modules.jsonl."""

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


def load_modules(modules_dir: Path) -> list[dict]:
    modules: list[dict] = []
    for path in sorted(modules_dir.glob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        if not isinstance(doc, dict):
            raise ValueError(f"{path}: expected mapping")
        modules.append(doc)
    return modules


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "modules_dir",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parents[1] / "catalog" / "modules",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Write catalog.json and modules.jsonl here",
    )
    args = parser.parse_args()

    modules = load_modules(args.modules_dir)
    modules.sort(key=lambda m: m["id"])

    payload = {"schema_version": 1, "modules": modules}

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        json_path = args.output_dir / "catalog.json"
        jsonl_path = args.output_dir / "modules.jsonl"
    else:
        json_path = Path("catalog.json")
        jsonl_path = Path("modules.jsonl")

    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for mod in modules:
            fh.write(json.dumps(mod, separators=(",", ":")) + "\n")

    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
