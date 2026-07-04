# wwn-apt

Wawona does not implement an alternative app marketplace or a traditional package manager.

All downloadable software modules are specifically ported to iOS and modified to comply with App Store requirements and iOS's execution model. Each module must be submitted through App Store Connect, reviewed by Apple, and approved before it can be made available to users.

The `apt` command provided by Wawona is not a general-purpose Debian package manager and cannot install arbitrary software, third-party repositories, or user-supplied binaries. Instead, it is a compatibility layer and user interface that presents App Store-approved downloadable modules in a familiar package management workflow.

For example:

* `apt search` lists **optional** downloadable modules in the embedded catalog (foot, neovim, fastfetch today; sway, niri, hyprland, cosmic, xfce, and kde are catalogued as `planned` ports and cannot be installed until reviewed).
* `apt install <package>` uses StoreKit APIs to request and download the corresponding approved optional module.
* `apt remove <package>` removes an optional module from the user's local installation.

**Required bundled software** (zsh, uutils coreutils, waypipe, and the `apt` command itself) is always included in Wawona and **cannot** be installed or removed via `apt`. See [`docs/BUNDLED-SOFTWARE.md`](docs/BUNDLED-SOFTWARE.md).

All package acquisition, installation, and restoration operations are performed exclusively through Apple-approved mechanisms such as StoreKit and App Store-hosted content. No executable code is downloaded from third-party servers, and all modules execute solely within Wawona's constrained single-process runtime environment.

From the user's perspective, `apt` provides a familiar command-line experience. Technically, however, it is a frontend for App Store-approved downloadable components rather than an independent software distribution system.

## App Store Review Notes

Copy-paste reviewer guidance: [`docs/APP-STORE-MODULES.md`](docs/APP-STORE-MODULES.md)

## Use in a flake

```nix
inputs.wwn-apt.url = "github:Wawona/wwn-apt";
registry = wwn-toolchain.lib.baseRegistry // wwn-apt.registryFragment;
```

Fragment key: `apt-rootfs` (prefix tree with `usr/bin/apt` and embedded module catalog).

## Standalone build

```sh
nix build .#catalog-json
nix build .#apt-rootfs-ios
```

## Layout

```
catalog/          Optional module manifests + bundled.yaml + JSON Schema
apt/              Shell CLI stub (search, install, remove, list, show)
docs/             Architecture, compliance, integration spec
scripts/          Catalog validators and generators
dependencies/     Nix recipes (apt-rootfs)
```

## License

MIT for Wawona catalog, CLI, and Nix packaging (see `LICENSE`).
