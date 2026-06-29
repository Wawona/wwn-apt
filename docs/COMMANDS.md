# apt command reference

Wawona `apt` — App Store module compatibility layer.

## Commands

| Command | Description |
|---------|-------------|
| `apt --version` | Wawona apt identity (not a package manager version; backends summary) |
| `apt --about` | Print compliance summary |
| `apt help` | Usage |
| `apt search [pattern]` | Filter embedded catalog |
| `apt show <module>` | Module metadata |
| `apt list` | All approved modules |
| `apt list --installed` | Locally installed modules |
| `apt install <module>` | StoreKit + ODR install (requires module manager) |
| `apt remove <module>` | Remove local install |

## Unsupported commands (by design)

These exit with code 1 and an explanatory message:

- `edit-sources`, `add-repository`, `add-apt-repository`
- `update`, `upgrade`, `dist-upgrade`, `autoremove`, `autoclean`

Wawona does not support third-party package repositories. The catalog is
embedded in the app and updated with app releases.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Usage error or unsupported command |
| 2 | Module manager unavailable (v1 default for `install`) |
| 3 | Module not found |
| 4 | Dependency or conflict error (future) |

## Output format

`apt search`, `apt list`, and `apt list --installed` use a Debian-inspired column layout:

```
version/id status
```

- `apt list` — all optional catalog modules; status is `installed` or `approved`
- `apt list --installed` — only modules present in `installed.json`

Installed state is read from:

`~/Library/Application Support/Wawona/modules/installed.json`

Example:

```json
{"modules":[{"id":"foot","version":"1.19.0"}]}
```

## Environment

| Variable | Purpose |
|----------|---------|
| `WAWONA_ROOTFS` | Writable rootfs prefix (Application Support) |
| `WAWONA_BUNDLE_ROOTFS` | Bundled read-only rootfs in app Resources |
| `WAWONA_MODULE_MANAGER` | Set when host socket bridge is active (future) |
