# Thoth Core — project status snapshot

**Date:** 2026-05-30  
**Phase:** [1 — Public testnet & infrastructure](../ROADMAP.md#phase-1--public-testnet--infrastructure-started) — **testnet soak in progress**  
**This file is a point-in-time snapshot.** For history see [DEVLOG.md](../DEVLOG.md); for plans see [ROADMAP.md](../ROADMAP.md).

---

## Consensus v2 — migration complete

**Commit:** `0a45b1856` — near-genesis BIP heights, MWEB disabled ([CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md)).

Operators reset datadirs and restarted from genesis. The **pre-v2 chain** (~height 3, legacy
Litecoin activation params) is **invalidated**; the live network is a **fresh v2 chain** from
genesis with unchanged genesis hash.

New nodes must use the v2 binary and reset if they still hold pre-v2 block data. See
[release-notes-thoth.md](release-notes-thoth.md#consensus-v2-thoth-mainnet--testnet).

---

## Repository

| Item | Value |
|------|--------|
| GitHub | [teklifooofficial-glitch/thoth-core](https://github.com/teklifooofficial-glitch/thoth-core) |
| Default branch | `main` |
| Upstream reference | Litecoin Core 0.21.5.5 lineage |
| Recent commits | `0a45b1856` consensus v2 · `88c9ffd3b` consensus audit |

---

## Network (mainnet)

| Item | Value |
|------|--------|
| Stage | Early development — **consensus v2 mainnet** |
| Best block height | **1** |
| Best block hash | `6123e5e50555e456fa8808230311538235343d8fdb8fd380de8ad9ab89ea20d1` |
| Genesis hash | `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784` *(unchanged)* |
| Known full nodes | **2** — home + VPS seed (**synced** on v2 chain) |
| Public seed | `addnode=152.239.115.145:19333` (P2P **19333**; RPC **19332** localhost only) |
| DNS / fixed seeds | Disabled; manual `addnode` bootstrap |
| MWEB | **Disabled** on mainnet |
| Exchange listed | **No** |

Testnet join guide: [TESTNET-JOIN.md](TESTNET-JOIN.md) — reset `~/.thoth/testnet4/` if using pre-v2 data.

---

## Network (testnet)

| Item | Value |
|------|--------|
| Stage | Phase 1 — **30-day soak in progress** |
| Soak started | **2026-05-30** |
| Soak end target | **~2026-06-29** (Phase 1 exit criterion) |
| Genesis hash | `439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651` |
| Known peers | **2** — home + VPS testnet seed (**synced**) |
| Public seed | `addnode=152.239.115.145:29335` (P2P **29335**; RPC **29332** localhost only) |
| Block explorer | http://152.239.115.145:8080/ ([contrib/thoth-explorer](../contrib/thoth-explorer/); HTTP, RPC not exposed) |
| Landing page | http://152.239.115.145/ ([contrib/thoth-landing](../contrib/thoth-landing/); nginx :80 when deployed) |
| DNS / fixed seeds | Disabled; manual `addnode` bootstrap |
| MWEB | **Disabled** |

### Testnet soak criteria ([PHASE1-PREP.md](PHASE1-PREP.md) §B)

| Criterion | Status |
|-----------|--------|
| No consensus failures | Monitoring (v2 rules; MWEB off) |
| Seed uptime (`152.239.115.145:29335`) | Monitoring |
| Peer count logged weekly | Started 2026-05-30 |

**Weekly peer log** (testnet `getconnectioncount` / operator notes):

| Week ending | Peer count | Notes |
|-------------|------------|-------|
| 2026-05-30 | 2 | Soak start; home + VPS seed |

---

## What works today

- **Build** from source on **Arch/CachyOS** and **Ubuntu 22.04 VPS** (`doc/build-unix.md`)
- **Consensus v2** in `chainparams.cpp` — Segwit at 144, Taproot window 8064–101376, MWEB off
- **Testnet explorer** live at http://152.239.115.145:8080/ (Phase 1a; TLS optional follow-up)
- **Landing page** in repo ([contrib/thoth-landing](../contrib/thoth-landing/)); deploy at http://152.239.115.145/ (nginx :80)
- **Headless node** on VPS with systemd; **wallet** on Arch with BDB 4.8
- **RPC mining:** `generatetoaddress` (coinbase must include height ≥ block 1 under v2)
- **Two-node sync** on v2 mainnet (home + VPS seed peering verified)

---

## Known limits

- **Pre-v2 mainnet abandoned** — old blocks invalid; do not reuse pre-v2 datadirs.
- **Very small network** — not suitable for production payments.
- **MWEB disabled** — peg-in/out and extension blocks not available on mainnet/testnet.
- **Regtest MWEB tests** need `-vbparams` override (default MWEB off).
- **Explorer Phase 1a** deployed at http://152.239.115.145:8080/ (HTTP; HTTPS/nginx optional)
- **Testnet soak** running since **2026-05-30** (target end ~2026-06-29)
- **No exchange listing.**

---

## Next three actions (Phase 1)

1. **Maintain testnet soak** through ~2026-06-29 — log peers weekly; no consensus incidents.
2. **Verify explorer accuracy** vs `thoth-cli -testnet` ([EXPLORER-PLAN.md](EXPLORER-PLAN.md) §7); optional TLS front-end.
3. **Validate testnet mining guide** — legacy before block 144, `ttth1` after ([TESTNET-JOIN.md](TESTNET-JOIN.md) §6).

---

## Quick links

- [ROADMAP.md](../ROADMAP.md)
- [CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md)
- [TESTNET-JOIN.md](TESTNET-JOIN.md)
- [EXPLORER-PLAN.md](EXPLORER-PLAN.md)
- [Testnet explorer](http://152.239.115.145:8080/)
- [Landing page](http://152.239.115.145/)
- [Join the network](../README.md#join-the-network)
- [LEGAL-NOTICE.md](LEGAL-NOTICE.md)
- [WHITEPAPER.md](WHITEPAPER.md)
- [PHASE1-PREP.md](PHASE1-PREP.md)
