# Wawona integration spec (follow-up PR)

This document defines how the main **Wawona** app integrates `wwn-apt`. v1 ships
the catalog and CLI stub only; host-app wiring is a separate PR series (W1–W5).

## Flake wiring (W1)

In `Wawona/flake.nix`:

```nix
inputs.wwn-apt.url = "github:Wawona/wwn-apt";
# follows nixpkgs / wwn-toolchain same as other wwn-* inputs

mergedRegistry = wwn-toolchain.lib.baseRegistry
  // wwn-apt.registryFragment
  // ... ;

# In ios-rootfs.nix (or overlay):
# Merge apt-rootfs outputs into wawona-rootfs prefix:
#   usr/bin/apt
#   usr/share/wawona/apt/catalog.json
#   usr/share/wawona/apt/modules.jsonl
#   usr/lib/wawona/apt/apt-common.sh
```

Build catalog in CI before rootfs assembly:

```sh
python3 scripts/generate-catalog-json.py catalog/modules -o $out/share/wawona/apt
```

Or consume `nix build github:Wawona/wwn-apt#catalog-json`.

## Xcode / ODR (W3)

For each module YAML `platforms.ios.odr.tag`:

1. Create matching ODR tag in Xcode → Build Settings → Asset Catalog Compiler
   → On Demand Resources Tags, or tag asset folders in `.xcassets`.
2. Bundle module payload under `platforms.ios.odr.bundle_subpath`.
3. CI check: set of ODR tags in Xcode == set of tags in generated `catalog.json`.

## StoreKit (W3)

1. Create App Store Connect products matching `storekit.product_id` per module/platform.
2. Free modules: non-consumable or consumable with price tier 0 — product policy TBD with finance.
3. Swift: StoreKit 2 `Product.products(for: ids)` → `product.purchase()`.

## WWNModuleManager API (W2)

Objective-C/Swift host singleton (suggested interface):

```objc
@interface WWNModuleManager : NSObject
+ (instancetype)sharedManager;
- (NSArray<NSString *> *)installedModuleIds;
- (void)installModuleWithId:(NSString *)moduleId
           completion:(void (^)(NSError *_Nullable error))completion;
- (void)removeModuleWithId:(NSString *)moduleId
          completion:(void (^)(NSError *_Nullable error))completion;
@end
```

Implementation steps for `installModuleWithId:`:

1. Load `catalog.json` from bundle; validate `moduleId`.
2. Resolve `storekit.product_id` and `odr.tag` for current platform.
3. Run StoreKit purchase / restore flow.
4. `NSBundleResourceRequest(tags: [odrTag])` → `beginAccessingResources`.
5. Copy/extract payload to `Application Support/Wawona/modules/<id>/`.
6. Update `installed.json` and refresh dispatch registry.
7. End ODR access when idle (cache may remain on device).

## IPC protocol (W2)

Unix domain socket: `~/Library/Application Support/Wawona/module-manager.sock`

JSON lines (one request per connection):

```json
{"op":"install","id":"foot"}
{"op":"remove","id":"foot"}
{"op":"list-installed"}
```

Responses:

```json
{"ok":true}
{"ok":false,"error":"module manager unavailable"}
```

When socket exists, set `WAWONA_MODULE_MANAGER=1` in shell environment before
spawning zsh so `apt install` can connect.

**Preferred dispatch path:** rootfs `usr/bin/apt` executed via zsh exec hook
(normal external command path on App Store build — no new native `apt` binary
required). Do not register `apt` in `wawona_dispatch_inprocess` unless exec
hook cannot reach rootfs binaries.

## Dispatch registration (W4)

### Required bundled (always enabled)

Linked into the app at build time; **not** gated on `installed.json`:

| Component | Symbol | Commands |
|-----------|--------|----------|
| zsh | `wawona_zsh_main` | (shell) |
| coreutils | `wawona_coreutils_main` | `ls`, `cat`, … |
| waypipe | `waypipe_main` | `waypipe` |
| apt | (shell script) | `apt` |

### Optional modules (install-gated)

Extend `wawona-dispatch.c` or load a runtime table from `installed.json`:

| Module | Symbol | Commands |
|--------|--------|----------|
| foot | `foot_main` | `foot` |
| neovim | `wawona_nvim_main` | `nvim`, `vi`, `vim` |
| fastfetch | `fastfetch_main` | `fastfetch` |

Weak-link optional module symbols at app link time; gate dispatch on install state.
Bundled symbols are always active.

## Android parallel (spec only)

Catalog `platforms.android.play` fields reserved for Play Feature Delivery /
Billing. Mirror IPC and install dir layout under app files dir.

## App Review (W5)

Copy [`APP-STORE-MODULES.md`](APP-STORE-MODULES.md) into:

- App Store Connect Review Notes
- `Wawona/docs/ios-local-shell/APP-REVIEW-NOTES.md` (new section)

Do not reference external distribution systems in App Store documentation.

## Verification checklist

- [ ] `nix build .#apt-rootfs-ios` merged into Wawona IPA rootfs
- [ ] `apt search foot` works on device/simulator shell
- [ ] `apt install foot` completes with module manager connected
- [ ] `apt edit-sources` returns exit 1; `apt remove waypipe` returns exit 4 (bundled)
- [ ] ODR tags match catalog in CI
- [ ] StoreKit product ids match catalog in CI
