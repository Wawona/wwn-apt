# Bundled vs optional modules

Wawona splits software into two classes for App Store builds.

## Required bundled software

Always included in the app. **Not** in the optional module catalog. Users
**cannot** install or remove these via `apt` (they are not downloadable modules).

| Component | Source repo | Role |
|-----------|-------------|------|
| **zsh** | `wwn-zsh` | In-process shell |
| **coreutils** (uutils) | `wwn-coreutils` | In-process utility dispatch (`ls`, `cat`, …) |
| **waypipe** | `wwn-waypipe` | Remote Wayland proxy |
| **apt** | `wwn-apt` | Module compatibility CLI |

Canonical list: [`catalog/bundled.yaml`](../catalog/bundled.yaml) → `bundled.json` in rootfs.

## Optional downloadable modules

May be installed or removed via `apt` after StoreKit authorization and ODR
download. Each entry in [`catalog/modules/`](../catalog/modules/) must **not**
overlap a bundled component id.

| Module | Source repo |
|--------|-------------|
| **foot** | `wwn-foot` |
| **neovim** | `wwn-neovim` |
| **fastfetch** | `wwn-fastfetch` |

## Policy enforcement

- `scripts/validate-catalog.py` — rejects catalog ids that collide with bundled ids
- `apt install` / `apt remove` — reject bundled component names with exit code 4
