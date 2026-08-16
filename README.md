# wwn-apt — removed

This repository is **retired**.

Wawona no longer ships a StoreKit / On-Demand Resources `apt` catalog for
optional Mach-O modules.

## Replacement

| Need | Where |
|------|--------|
| Run / install WASI P1/P2 `.wasm` | [`wwn-wasm`](https://github.com/Wawona/wwn-wasm) — **Wawona Runtime** |
| Files.app drop-in + shell `wasm` | [Wawona `docs/wasm-wasi.md`](https://github.com/Wawona/Wawona/blob/development/docs/wasm-wasi.md) |
| OCI Linux containers (Docker Hub, …) | [`wwn-containers`](https://github.com/Wawona/wwn-containers) + Machines kind `container` |
| VMs | [`wwn-vms`](https://github.com/Wawona/wwn-vms) |

Do not re-add `wwn-apt` as a flake input of Wawona.
