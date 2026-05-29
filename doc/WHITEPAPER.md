# Thoth (TTH) — technical whitepaper (draft)

**Version:** 0.1 (draft)  
**Date:** 2026-05-29  
**Status:** Early development — not production-ready; **not exchange-listed**

This document describes the Thoth network and software as implemented in
[teklifooofficial-glitch/thoth-core](https://github.com/teklifooofficial-glitch/thoth-core).
It is informational only. See [LEGAL-NOTICE.md](LEGAL-NOTICE.md): **not investment advice**,
**no guaranteed returns**, **not a security offering**.

**Related:** [ROADMAP.md](../ROADMAP.md) · [PROJECT-STATUS.md](PROJECT-STATUS.md) · [LEGAL-NOTICE.md](LEGAL-NOTICE.md)

---

## 1. Abstract

Thoth (TTH) is an open-source Layer-1 blockchain derived from Litecoin Core 0.21.
It uses **Scrypt** proof-of-work, **2.5-minute** block targets, and a **84 million TTH**
maximum supply with halving every 840,000 blocks. The project prioritizes transparent
documentation, operator-run full nodes, and phased rollout per [ROADMAP.md](../ROADMAP.md).
At the time of writing, mainnet is a **small development network** (~height 3, two known
nodes). This is not a token sale document and makes **no exchange listing promises**.

---

## 2. Problem statement

Many public chains inherit opaque launch history or parameters tuned for unrelated networks.
Thoth aims to provide a **documented Scrypt L1 fork** with a fresh genesis, published
chain parameters, and governance docs (roadmap, status snapshots, legal notice) so operators
can evaluate the software without marketing claims. Participation is voluntary technical
experimentation—not a promise of financial outcome.

---

## 3. Solution overview

Thoth is a **full-node peer-to-peer network**: operators run `thothd` to validate blocks
and relay transactions; miners extend the chain via Scrypt PoW; wallets (when built with
compatible Berkeley DB) manage keys locally. Monetary policy is rule-based (subsidy schedule,
halvings) rather than discretionary issuance. There is **no premine or ICO** described in
the current codebase.

---

## 4. Technology stack

| Component | Description |
|-----------|-------------|
| Lineage | Litecoin Core **0.21.5.5** → Thoth rebrand |
| Language | C++ node; Python tooling (e.g. `genesis_miner.py`) |
| Binaries | `thothd`, `thoth-cli`, `thoth-qt`, `thoth-wallet`, `thoth-tx` |
| Address format | Bech32 HRP: `tth` (main), `ttth` (test), `rtth` (regtest) |
| MWEB HRP | `tthmweb` (extension inherited from upstream) |

Canonical source: GitHub repository above. Builds documented in [build-unix.md](build-unix.md).

---

## 5. Consensus and proof-of-work

- **Algorithm:** Scrypt (header hash via `GetPoWHash`, as in Litecoin lineage).
- **Block time target:** 150 seconds (`nPowTargetSpacing = 2.5 × 60`).
- **Difficulty:** Retargeting per upstream rules (periodic adjustment from observed block times).
- **Chain selection:** Most cumulative proof-of-work valid chain.
- **Coinbase maturity:** 100 blocks before mined coins are spendable (`COINBASE_MATURITY`).
- **Genesis message:** *"Thoth blockchain - wisdom and knowledge for all - 2024"*

Mainnet genesis (height 0):

`3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784`

---

## 6. Network parameters

| Network | RPC port | P2P port | Data directory | Genesis hash (truncated) |
|---------|----------|----------|----------------|---------------------------|
| Mainnet | 19332 | 19333 | `~/.thoth/` | `3f2dc0f6…` (full hash in [README](../README.md)) |
| Testnet | 29332 | 29335 | `~/.thoth/testnet4/` | `439581a3…` |
| Regtest | 19443 | 19444 | `~/.thoth/regtest/` | `b6ae6fa7…` |

**Bootstrap (mainnet, current):** DNS seeds and fixed seeds are **disabled**; operators use
manual `addnode=` (public seed: `152.239.115.145:19333`). RPC must bind to **localhost only**
— never expose port 19332 to the internet.

**Development reality:** With ~height 3 and two known nodes, new peers may require **manual
chain copy** (`scp` of `blocks/` / `chainstate/`) until peer count and relay improve.
See [PROJECT-STATUS.md](PROJECT-STATUS.md).

---

## 7. Tokenomics

Fixed-cap schedule inherited from Litecoin-style economics (84M coin units, halving interval
840,000 blocks). Values below reflect `chainparams` and consensus defaults in this repository.

| Parameter | Value |
|-----------|--------|
| Ticker | **TTH** |
| Max supply | **84,000,000 TTH** (sum of halving series; asymptotic cap) |
| Initial block subsidy | **50 TTH** per block |
| Halving interval | Every **840,000** blocks |
| Smallest unit | 1 satoshi-style unit (1e-8 TTH) |
| Premine / ICO / dev allocation | **None in codebase** |
| Coinbase maturity | **100** blocks |
| Fee market | Transaction fees to miner (standard UTXO model) |

**Subsidy eras (illustrative):**

| Era | Block range (approx.) | Subsidy per block |
|-----|------------------------|-------------------|
| 1 | 0 – 839,999 | 50 TTH |
| 2 | 840,000 – 1,679,999 | 25 TTH |
| 3 | 1,680,000 – 2,519,999 | 12.5 TTH |
| … | halving continues | → 0 |

At mainnet height ~3, **circulating supply is negligible** (only early mined blocks; coinbase
immature until maturity). There is **no market price** implied by this document.

---

## 8. MWEB and inherited consensus features

Thoth inherits **Litecoin MWEB** (Mimblewimble Extension Blocks) and related deployment
machinery from upstream (`DEPLOYMENT_MWEB`, LIP references in `chainparams.cpp`).

**Important:** BIP and deployment **activation heights** (BIP16/34/65/66, Segwit, Taproot,
MWEB start heights, etc.) are still set to **Litecoin legacy values** "Thoth" mainnet began
at genesis in 2024 with height 0; those heights are **not yet re-derived** for this chain.

**Phase 1 action (pending):** Full [consensus / BIP review](../ROADMAP.md#phase-1--public-testnet--infrastructure)
before public testnet campaign and before treating mainnet as “launched.” Until then:

- Treat Segwit/Taproot/MWEB timing as **unaudited for Thoth**.
- Do not assume MWEB is active or user-ready on mainnet at low heights.
- Changes require roadmap update, `chainparams` patch, and release notes.

See [PHASE1-PREP.md](PHASE1-PREP.md) for the review checklist.

---

## 9. Governance and roadmap

Scope is defined in [ROADMAP.md](../ROADMAP.md) (Phases 0–5). **No work outside the roadmap
without updating the roadmap first.** Phase 0 focuses on trust and transparency; Phase 1 on
testnet, explorer, and BIP review; later phases cover public mainnet release, community, and
optional listing prep—**without guaranteed exchange outcomes**.

Live snapshots: [PROJECT-STATUS.md](PROJECT-STATUS.md). History: [DEVLOG.md](../DEVLOG.md).

---

## 10. Security model

- **Node operators:** Keep RPC on localhost; firewall P2P only as needed; run verified builds.
- **Wallet users:** Backup seeds/keys; BDB 4.8 recommended on Arch for wallet builds (see build docs).
- **Network layer:** Small peer set increases eclipse and partition risk during development.
- **Audits:** No third-party security audit commissioned to date; community testnet soak planned in Phase 1.

---

## 11. Wallet and key management

Wallet support follows Bitcoin/Litecoin-style RPC and Berkeley DB storage. Arch/CachyOS builds
should link **BDB 4.8** for reliable wallet creation; `--with-incompatible-bdb` suits **node-only**
VPS builds. Descriptor and Segwit features inherit from upstream; activation timing subject to
Phase 1 BIP review.

---

## 12. Mining and participation

Mining on development mainnet uses RPC **`generatetoaddress`** (legacy `gen=1` is not supported).
Scrypt mining is CPU/GPU accessible but economically meaningless at height ~3 with no market.

Solo mining is the current norm; **mining pools are not deployed** by the project. Environmental
and hardware costs are borne by the operator.

---

## 13. Team and contributors

Development is open-source. Contributions follow [CONTRIBUTING.md](../CONTRIBUTING.md).
Maintainers do not owe fiduciary duties to coin holders. Identities may be pseudonymous.

---

## 14. Legal disclaimer

Read [LEGAL-NOTICE.md](LEGAL-NOTICE.md) in full. Thoth documentation is not investment,
tax, or legal advice. Compliance in your jurisdiction is your responsibility.

---

## 15. Risks

| Risk | Notes |
|------|--------|
| Early-stage network | ~2 nodes, ~height 3; reorgs and sync issues possible |
| Software bugs | Experimental fork; loss of funds possible |
| Unreviewed BIP heights | Legacy Litecoin heights may be wrong for Thoth |
| MWEB complexity | Inherited code paths not validated on Thoth mainnet |
| No liquidity / listing | TTH is **not** on exchanges; no price discovery |
| Regulatory | Mining and holding may have legal implications locally |

No risk can be fully mitigated by documentation alone.

---

## 16. References

- Repository: https://github.com/teklifooofficial-glitch/thoth-core
- [ROADMAP.md](../ROADMAP.md) · [PROJECT-STATUS.md](PROJECT-STATUS.md) · [LEGAL-NOTICE.md](LEGAL-NOTICE.md)
- [WHITEPAPER-OUTLINE.md](WHITEPAPER-OUTLINE.md) (skeleton this draft expands)
- [PHASE1-PREP.md](PHASE1-PREP.md) · [build-unix.md](build-unix.md) · [bips.md](bips.md)
- Genesis tool: `genesis_miner.py` (repository root)

*This draft supersedes the outline for Phase 0 purposes.*
