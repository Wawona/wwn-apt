# App Store compliance: module delivery

Engineering mapping for Wawona's App Store–compliant optional modules via the
`apt` compatibility layer. Reviewer-facing copy: [`APP-STORE-MODULES.md`](APP-STORE-MODULES.md).

Related Wawona doc (integration repo): `Wawona/docs/ios-local-shell/APP-STORE-COMPLIANCE.md`

## Guideline 2.5.2 — downloading code

| Concern | Wawona posture |
|---------|----------------|
| Post-review native download | Only **On-Demand Resources** included in the App Store submission bundle, served from Apple's CDN after StoreKit authorization |
| Third-party executables | **Not supported** — catalog is fixed; no user-supplied binaries |
| Arbitrary repositories | **Not supported** — no repository configuration in the CLI or app |
| JIT / unsigned dynamic loading | **Not used** — in-process weak symbols; no unsigned `dlopen` |

## Execution model

Modules run in Wawona's single-process sandbox:

- Static or ODR-delivered archives registered at install time
- Dispatch via `wawona_dispatch_inprocess` in `wwn-toolchain` (`wawona-pty`)
- Symbols such as `foot_main`, `fastfetch_main`, `wawona_nvim_main`

## Evolution from base shell compliance

The base Wawona shell ships a fixed in-process userland (zsh, coreutils subset).
Optional modules extend that userland through **reviewed ODR asset packs** and
StoreKit products — not through independent distribution channels.

## Explicit non-goals (absolute terms)

- No third-party package repositories
- No user-supplied binary installation
- No post-review executable download from non-Apple servers
- No repository configuration files in the app sandbox
- No sideloading or unsigned native module loading

## CI

`scripts/check-app-store-firewall.py` enforces that App Store deliverables in
this repository do not contain legacy package-manager terminology that could
misrepresent the product to App Review.
