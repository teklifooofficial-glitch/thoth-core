# Thoth Core — project status snapshot

**Date:** 2026-05-29  
**Phase:** [1 — Public testnet & infrastructure](../ROADMAP.md#phase-1--public-testnet--infrastructure-started) — consensus v2 merged  
**This file is a point-in-time snapshot.** For history see [DEVLOG.md](../DEVLOG.md); for plans see [ROADMAP.md](../ROADMAP.md).

---

## Consensus v2 — chain reset required

**Breaking change:** Near-genesis BIP heights and **disabled MWEB** are now in
`src/chainparams.cpp`. Genesis hashes are **unchanged**; pre-v2 block data is
**invalid**.

**All operators must reset before running the new binary:**

```bash
thoth-cli stop
rm -rf ~/.thoth/blocks ~/.thoth/chainstate ~/.thoth/indexes
thothd -daemon
thoth-cli getblockchaininfo   # height 0, genesis hash unchanged
```

Details: [release-notes-thoth.md](release-notes-thoth.md) · [CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md)

---

## Repository

| Item | Value |
|------|--------|
| GitHub | [teklifooofficial-glitch/thoth-core](https://github.com/teklifooofficial-glitch/thoth-core) |
| Default branch | `main` |
| Upstream reference | Litecoin Core 0.21.5.5 lineage |
| Recent commits | `88c9ffd3b` consensus audit · consensus v2 `chainparams` (pending push hash) |

---

## Network (mainnet)

| Item | Value |
|------|--------|
| Stage | Early development — **reset to height 0** after consensus v2 |
| Best block height | **0** (post-reset; remine required) |
| Genesis hash | `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784` *(unchanged)* |
| Known full nodes | **2** — home + VPS seed (must reset datadirs) |
| Public seed | `addnode=152.239.115.145:19333` (P2P **19333**; RPC **19332** localhost only) |
| DNS / fixed seeds | Disabled; manual `addnode` bootstrap |
| MWEB | **Disabled** on mainnet |
| Exchange listed | **No** |

Testnet genesis: `439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651` — same reset policy under `~/.thoth/testnet4/`.

---

## What works today

- **Build** from source on **Arch/CachyOS** and **Ubuntu 22.04 VPS** (`doc/build-unix.md`)
- **Consensus v2** in `chainparams.cpp` — Segwit at 144, Taproot window 8064–101376, MWEB off
- **Headless node** on VPS with systemd; **wallet** on Arch with BDB 4.8
- **RPC mining:** `generatetoaddress` (coinbase must include height ≥ block 1 under v2)
- Genesis verification via `getblockchaininfo` / `getblockhash 0`

---

## Known limits

- **Chain reset mandatory** after upgrading to consensus v2; old ~height 3 chain abandoned.
- **Very small network** — not suitable for production payments.
- **MWEB disabled** — peg-in/out and extension blocks not available on mainnet/testnet.
- **Regtest MWEB tests** need `-vbparams` override (default MWEB off).
- **No block explorer** or public testnet soak yet.
- **No exchange listing.**

---

## Next three actions (Phase 1)

1. **Reset all nodes** (home + VPS seed) and verify `getblockchaininfo` at height 0.
2. **Remine / peer test** under v2; confirm Segwit at block 144+ on testnet before public campaign.
3. **Public testnet soak** — [PHASE1-PREP.md](PHASE1-PREP.md) §B after operator reset complete.

---

## Quick links

- [ROADMAP.md](../ROADMAP.md)
- [CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md)
- [Join the network](../README.md#join-the-network)
- [LEGAL-NOTICE.md](LEGAL-NOTICE.md)
- [WHITEPAPER.md](WHITEPAPER.md)
- [PHASE1-PREP.md](PHASE1-PREP.md)
