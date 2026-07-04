# App Store Review Notes — `apt` command

Copy the block below into **App Store Connect → App Review Information → Notes**
when Wawona ships optional downloadable modules.

---

## Copy-paste: App Review Notes

**Optional modules (`apt` command)**

Wawona includes a shell command named `apt` that provides a familiar workflow for
optional developer modules. It is **not** a general-purpose package manager.

Users cannot add third-party repositories or install arbitrary software. The
only **optional** installable items are **foot**, **neovim**, and **fastfetch**
(listed in an embedded catalog shipped inside the app). Each optional module has
a corresponding **StoreKit product** and **On-Demand Resource (ODR)** asset pack
included in this App Store submission and reviewed by Apple.

**Required bundled software** — always in the app, not optional, not removable
via `apt`: **zsh**, **uutils coreutils**, **waypipe**, and the **apt** command
itself.

- `apt search` — lists optional modules from the embedded catalog
- `apt install <name>` — StoreKit + ODR for optional modules only (foot, neovim, fastfetch). Modules with `status: planned` (sway, niri, hyprland, cosmic, xfce, kde) are listed but refuse installation until the port ships and passes review.
- `apt remove <name>` — removes a locally installed optional module
- `apt list`, `apt show` — catalog metadata

All module code executes within Wawona's existing in-process sandbox (no
downloading of unsigned native code from third-party servers). Attempts to use
repository-management commands (e.g. `edit-sources`) are rejected by design.

---

## Copy-paste: in-app About text (future Settings UI)

**About the apt command**

Wawona's `apt` command installs optional modules that Apple reviewed as part of
this app. It uses the App Store catalog and On-Demand Resources only. You cannot
add external repositories or install software from outside the App Store workflow.

---

## FAQ (for reviewers)

**Why is the command called `apt`?**

Developer familiarity. The command exposes a small, fixed subset of package-manager
UX (`search`, `install`, `remove`, `list`, `show`) over App Store module delivery.

**Can users add repositories?**

No. Repository-management subcommands are unsupported and return an error.

**Where do modules come from?**

An embedded JSON catalog in the app bundle. Downloadable payloads are ODR tags
declared in the submission and fetched from Apple's CDN after StoreKit
authorization.

**Can users install their own binaries?**

No.

**Can users remove zsh, coreutils, waypipe, or apt?**

No. Those components are required bundled software, always included in the app,
and outside the optional module catalog. `apt install` and `apt remove` reject them.

**Which modules are optional?**

foot (terminal), neovim (editor), and fastfetch (system info). All other
listed developer tools in the base app are bundled at install time.

---

## Technical reference

- Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- Compliance mapping: [`COMPLIANCE.md`](COMPLIANCE.md)
- Wawona integration (engineers): [`INTEGRATION-SPEC.md`](INTEGRATION-SPEC.md)
