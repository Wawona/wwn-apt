# Catalog schema reference

Module manifests live in [`catalog/modules/`](../catalog/modules/) as YAML files.
The canonical schema is [`catalog/schema/module.schema.json`](../catalog/schema/module.schema.json).

## Required fields

| Field | Description |
|-------|-------------|
| `id` | Stable module identifier (used with `apt install`) |
| `name` | Display name |
| `version` | Semver string |
| `section` | UI grouping (e.g. `editors`, `utils`) |
| `description` | Short summary for `apt search` |
| `maintainer` | Contact string |
| `status` | `approved` or `deprecated` |
| `license` | SPDX license id |
| `wwn_repo` | Source repo (`wwn-foot`, `wwn-neovim`, …) |
| `registry_key` | Nix registry key in `wwn-toolchain` merge |
| `dispatch.commands` | argv0 names routed in-process |
| `dispatch.symbol` | Link symbol (`foot_main`, `wawona_nvim_main`, …) |
| `platforms.<apple>.storekit.product_id` | App Store Connect product id |
| `platforms.<apple>.odr.tag` | On-Demand Resource tag |
| `platforms.<apple>.odr.bundle_subpath` | Path inside ODR bundle |

## Optional fields

| Field | Description |
|-------|-------------|
| `app_store_notes` | Text for App Review / Connect |
| `depends` | Module ids that must be installed first |
| `conflicts` | Incompatible module ids |
| `replaces` | Obsoleted module ids |
| `platforms.android.play` | Play Billing / Feature Delivery (spec only) |

## Example

See [`catalog/modules/foot.yaml`](../catalog/modules/foot.yaml).

## Validation

```sh
python3 scripts/validate-catalog.py
python3 scripts/generate-catalog-json.py catalog/modules -o /tmp/out
```
