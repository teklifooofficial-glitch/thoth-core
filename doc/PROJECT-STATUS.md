# Thoth Core — project status snapshot

**Date:** 2026-05-29  
**Phase:** [0 — Trust & transparency](../ROADMAP.md#phase-0--trust--transparency-current)  
**This file is a point-in-time snapshot.** For history see [DEVLOG.md](../DEVLOG.md); for plans see [ROADMAP.md](../ROADMAP.md).

---

## Repository

| Item | Value |
|------|--------|
| GitHub | [teklifooofficial-glitch/thoth-core](https://github.com/teklifooofficial-glitch/thoth-core) |
| Default branch | `main` |
| Upstream reference | Litecoin Core 0.21.5.5 lineage |
| Recent docs commits | `795ee92dc` rebrand · `031225f70` BDB 4.8 docs · `12b548c5a` join network · `893760b50` DEVLOG |

---

## Network (mainnet)

| Item | Value |
|------|--------|
| Stage | Early development — **small private network** |
| Best block height | **~3** (genesis + mined blocks) |
| Genesis hash | `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784` |
| Known full nodes | **2** — home (Arch/CachyOS) + VPS seed |
| Public seed | `addnode=152.239.115.145:19333` (P2P **19333**; RPC **19332** localhost only) |
| DNS / fixed seeds | Disabled; manual `addnode` bootstrap |
| Exchange listed | **No** |

Testnet and regtest genesis hashes are in [README.md](../README.md) and [DEVLOG.md](../DEVLOG.md).

---

## What works today

- **Build** from source on **Arch/CachyOS** and **Ubuntu 22.04 VPS** (`doc/build-unix.md`)
- **Headless node** on VPS: `./configure --without-gui --with-incompatible-bdb`, `make`
- **Wallet** on Arch when linked against **BDB 4.8** (`./contrib/install_db4.sh`, `BDB_LIBS` / `BDB_CFLAGS`)
- **RPC mining:** `generatetoaddress` on regtest, testnet, and isolated mainnet
- **Two-node peering** between home node and VPS via `addnode`
- **`thothd` on VPS** under **systemd** with firewall allowing P2P only (`ufw allow 19333/tcp`)
- Genesis verification via `getblockchaininfo` / `getblockhash 0`

---

## Known limits

- **Very small network** — single-digit blocks; not suitable for production payments or liquidity assumptions.
- **Early P2P sync** — new peers may need a **manual chain copy** (e.g. `scp` of `blocks/` and `chainstate/` from a synced node) until block relay and peer count improve.
- **BIP activation heights** inherited from Litecoin legacy; **not yet reviewed** for a chain born in 2024+. Treat segwit/taproot timing as **unaudited** until Phase 1 review lands.
- **Wallet on Ubuntu VPS build** uses incompatible BDB 5.x — fine for node-only; wallet portability differs from Arch BDB 4.8 profile.
- **No block explorer**, faucet, or public testnet campaign yet.
- **No official listing** on CoinGecko, CoinMarketCap, or any exchange.

---

## Next three actions (Phase 0)

1. **Complete Phase 0 governance docs** — ROADMAP, this file, whitepaper outline, legal notice, README status box *(this PR)*.
2. **Draft full whitepaper** from [WHITEPAPER-OUTLINE.md](WHITEPAPER-OUTLINE.md) — technical and tokenomics sections peer-reviewed before Phase 1.
3. **Publish recurring status updates** — update this file or DEVLOG when height, node count, or phase changes; keep disclaimers visible on README.

---

## Quick links

- [ROADMAP.md](../ROADMAP.md)
- [Join the network](../README.md#join-the-network)
- [LEGAL-NOTICE.md](LEGAL-NOTICE.md)
- [WHITEPAPER-OUTLINE.md](WHITEPAPER-OUTLINE.md)
