# Thoth Core — project status snapshot

**Date:** 2026-05-29  
**Phase:** [1 — Public testnet & infrastructure](../ROADMAP.md#phase-1--public-testnet--infrastructure-started) — consensus v2 live on mainnet  
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

## What works today

- **Build** from source on **Arch/CachyOS** and **Ubuntu 22.04 VPS** (`doc/build-unix.md`)
- **Consensus v2** in `chainparams.cpp` — Segwit at 144, Taproot window 8064–101376, MWEB off
- **Testnet join doc** published ([TESTNET-JOIN.md](TESTNET-JOIN.md))
- **Headless node** on VPS with systemd; **wallet** on Arch with BDB 4.8
- **RPC mining:** `generatetoaddress` (coinbase must include height ≥ block 1 under v2)
- **Two-node sync** on v2 mainnet (home + VPS seed peering verified)

---

## Known limits

- **Pre-v2 mainnet abandoned** — old blocks invalid; do not reuse pre-v2 datadirs.
- **Very small network** — not suitable for production payments.
- **MWEB disabled** — peg-in/out and extension blocks not available on mainnet/testnet.
- **Regtest MWEB tests** need `-vbparams` override (default MWEB off).
- **No block explorer** or public testnet soak yet.
- **No exchange listing.**

---

## Next three actions (Phase 1)

1. **Run public testnet node(s)** with stable uptime; publish `addnode` when available.
2. **Validate testnet mining guide** — legacy address before block 144, `ttth1` bech32 after ([TESTNET-JOIN.md](TESTNET-JOIN.md) §6).
3. **Begin 30-day testnet soak** and evaluate block explorer ([PHASE1-PREP.md](PHASE1-PREP.md) §B–§C).

---

## Quick links

- [ROADMAP.md](../ROADMAP.md)
- [CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md)
- [TESTNET-JOIN.md](TESTNET-JOIN.md)
- [Join the network](../README.md#join-the-network)
- [LEGAL-NOTICE.md](LEGAL-NOTICE.md)
- [WHITEPAPER.md](WHITEPAPER.md)
- [PHASE1-PREP.md](PHASE1-PREP.md)
