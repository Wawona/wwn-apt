#!/usr/bin/env python3
"""Validate catalog/modules against JSON Schema and Wawona policy checks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
except ImportError:
    print("jsonschema required: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "catalog" / "schema" / "module.schema.json"
MODULES_DIR = ROOT / "catalog" / "modules"

KNOWN_WWN_REPOS = frozenset(
    {
        "wwn-foot",
        "wwn-neovim",
        "wwn-fastfetch",
        "wwn-waypipe",
        "wwn-zsh",
        "wwn-weston",
        "wwn-iland",
        "wwn-coreutils",
        "wwn-toolchain",
    }
)

APPLE_PLATFORMS = ("ios", "ipados", "tvos", "visionos", "watchos")
SYMBOL_RE = re.compile(r"^(wawona_[a-z0-9_]+_main|[a-z0-9_]+_main)$")


def load_schema() -> dict:
    with SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate_module(doc: dict, schema: dict, path: Path) -> list[str]:
    errors: list[str] = []
    try:
        jsonschema.validate(doc, schema)
    except jsonschema.ValidationError as exc:
        errors.append(f"{path}: schema: {exc.message}")

    repo = doc.get("wwn_repo")
    if repo not in KNOWN_WWN_REPOS:
        errors.append(f"{path}: unknown wwn_repo '{repo}'")

    symbol = doc.get("dispatch", {}).get("symbol", "")
    if not SYMBOL_RE.match(symbol):
        errors.append(f"{path}: dispatch.symbol '{symbol}' invalid")

    platforms = doc.get("platforms", {})
    for plat in APPLE_PLATFORMS:
        if plat not in platforms:
            continue
        block = platforms[plat]
        sk = block.get("storekit", {})
        odr = block.get("odr", {})
        if not sk.get("product_id"):
            errors.append(f"{path}: platforms.{plat}.storekit.product_id required")
        if not odr.get("tag"):
            errors.append(f"{path}: platforms.{plat}.odr.tag required")
        if not odr.get("bundle_subpath"):
            errors.append(f"{path}: platforms.{plat}.odr.bundle_subpath required")

    return errors


def main() -> int:
    schema = load_schema()
    seen_ids: set[str] = set()
    all_errors: list[str] = []

    yaml_files = sorted(MODULES_DIR.glob("*.yaml"))
    if not yaml_files:
        all_errors.append(f"No module YAML files in {MODULES_DIR}")
    elif len(yaml_files) < 4:
        all_errors.append(f"Expected at least 4 seed modules, found {len(yaml_files)}")

    for path in yaml_files:
        with path.open(encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        if not isinstance(doc, dict):
            all_errors.append(f"{path}: expected mapping")
            continue
        mod_id = doc.get("id")
        if mod_id in seen_ids:
            all_errors.append(f"Duplicate module id '{mod_id}'")
        seen_ids.add(mod_id)
        all_errors.extend(validate_module(doc, schema, path))

    if all_errors:
        for err in all_errors:
            print(err, file=sys.stderr)
        return 1

    print(f"Validated {len(yaml_files)} module(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
