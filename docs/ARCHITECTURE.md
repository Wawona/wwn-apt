# Architecture: App Store module delivery

Wawona's `apt` command is a shell-facing compatibility layer over an embedded
module catalog and Apple-hosted delivery mechanisms.

## Data flow

```
User shell: apt install foot
    → validate id against embedded catalog (modules.jsonl / catalog.json)
    → IPC to WWNModuleManager (Wawona host app — follow-up PR)
    → StoreKit 2 product authorization (product_id from catalog)
    → NSBundleResourceRequest (ODR tag from catalog)
    → install payload to ~/Library/Application Support/Wawona/modules/<id>/
    → register dispatch entry (in-process *_main symbol)
    → zsh exec hook runs module via wawona_dispatch_inprocess
```

## Catalog locations (device)

| Path | Purpose |
|------|---------|
| `$WAWONA_ROOTFS/usr/share/wawona/apt/catalog.json` | Full manifest (Wawona integration) |
| `$WAWONA_ROOTFS/usr/share/wawona/apt/modules.jsonl` | Optional modules (shell CLI) |
| `$WAWONA_ROOTFS/usr/share/wawona/apt/bundled.json` | Required bundled components |
| `$WAWONA_ROOTFS/usr/bin/apt` | CLI stub |
| `~/Library/Application Support/Wawona/modules/installed.json` | Local install state |
| `~/Library/Application Support/Wawona/module-manager.sock` | IPC socket (future) |

## Build pipeline

1. Authors edit `catalog/modules/*.yaml` (optional modules only)
2. Required bundled list: `catalog/bundled.yaml` (zsh, coreutils, waypipe, apt)
3. `scripts/generate-catalog-json.py` → `catalog.json`, `modules.jsonl`, `bundled.json`
3. `scripts/validate-catalog.py` → JSON Schema + policy checks
4. `nix build .#apt-rootfs-ios` → prefix tree for Wawona rootfs merge

## Execution model

Modules are ported to iOS and linked for in-process dispatch (weak `*_main`
symbols). ODR delivers reviewed static archives or rootfs trees bundled at App
Store submission time. There is no runtime download of unsigned native code from
third-party servers.

See [`INTEGRATION-SPEC.md`](INTEGRATION-SPEC.md) for Wawona host-app wiring.
