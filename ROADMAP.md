# Thoth (TTH) — project roadmap

This document is the single source of truth for planned work. **No work outside this
roadmap without updating this file first** (via pull request or maintainer commit with
rationale in the changelog or DEVLOG).

---

## Vision

**Thoth (TTH)** is an independent Layer-1 blockchain forked from the Litecoin Core
lineage. It uses **Scrypt** proof-of-work, a **2.5-minute** block target, and a fixed
**84 million TTH** supply schedule (halving every 840,000 blocks). The goal is a
transparent, community-operated network with open-source full-node software
(`thothd`, `thoth-cli`, wallet tools) and clear governance documentation—not hype or
guaranteed financial outcomes.

---

## Current stage (2026-05-29)

| Item | Status |
|------|--------|
| Phase | **0 — Trust & transparency** (in progress) |
| Mainnet | Private / small network; **~height 3** |
| Known nodes | **2** (home + VPS seed `152.239.115.145:19333`) |
| Exchange listing | **None** — early development |
| Live snapshot | [doc/PROJECT-STATUS.md](doc/PROJECT-STATUS.md) |

---

## Phases

### Phase 0 — Trust & transparency *(current)*

**Goal:** Publish honest project state, legal disclaimers, and planning docs before
asking for wider participation or capital.

**Deliverables:**
- `ROADMAP.md`, `doc/PROJECT-STATUS.md`, `doc/WHITEPAPER-OUTLINE.md`
- `doc/LEGAL-NOTICE.md` (non-investment disclaimer)
- `DEVLOG.md` maintained with dated milestones
- README links to status and roadmap

**Exit criteria:**
- All Phase 0 docs merged on `main`
- No undisclosed RPC or operator secrets in the repository
- Whitepaper outline reviewed; full whitepaper not required yet
- **No exchange listing claims or listing “promises” in any public material**

---

### Phase 1 — Public testnet & infrastructure

**Goal:** Exercise the chain in public with testnet, tooling, and independent nodes.

**Deliverables:**
- Public **testnet** campaign (docs, faucet or mining guide if applicable)
- **Block explorer** (indexer + web UI) for testnet, then mainnet when ready
- **10+ independent full nodes** on testnet (or mainnet if still pre-launch)
- **Consensus / BIP height review** for a chain born in 2024+ (not Litecoin legacy heights)

**Exit criteria:**
- Testnet runs continuously for an agreed soak period (e.g. 30 days) without consensus bugs
- Explorer shows blocks, txs, and chain tips correctly
- ≥10 non-operator nodes peered on testnet
- BIP activation heights documented and merged in `chainparams` or release notes
- **No exchange listing promises**

---

### Phase 2 — Mainnet launch (public)

**Goal:** Formalize mainnet as a tagged, documented release for miners and node operators.

**Deliverables:**
- **Mainnet launch announcement** (blog or GitHub release)
- **Tagged release** (signed binaries optional; reproducible build docs required)
- **Mining guide** (hardware, `generatetoaddress`, pool guidance if any)
- Seed / DNS strategy or curated peer list published

**Exit criteria:**
- Git tag on `main` matching release notes
- Genesis and chainparams frozen for that tag
- Join-the-network docs verified by a third-party operator
- Known issues listed in PROJECT-STATUS
- **No exchange listing promises**

---

### Phase 3 — Community & market data readiness

**Goal:** Grow operators and prepare factual listings—not trading hype.

**Deliverables:**
- Official **community channels** (e.g. Discord, Matrix, forum—TBD)
- Documentation for contributors and node operators
- **CoinGecko / CoinMarketCap application prep** (requirements checklist only):
  - Public block explorer URL
  - Source code repo (this repo)
  - Official website or docs landing page
  - Clear ticker (TTH) and contract N/A (native L1)
  - Supply transparency (84M cap, halving schedule)
  - At least two independent API/explorer endpoints or sustained node count
  - No misleading claims; legal notice linked

**Exit criteria:**
- Community channel moderated and linked from README
- Listing application **draft packet** complete (submission is optional and not guaranteed)
- PROJECT-STATUS updated monthly during this phase

---

### Phase 4 — Exchange outreach (optional, budget-limited)

**Goal:** Explore **small CEX** integrations only where legally and operationally feasible.

**Deliverables:**
- Outreach to a **small number** of exchanges (no public naming until signed)
- **Market maker / liquidity budget note** (internal or public high-level range only—no token sale)
- Wallet integration docs for custodians

**Exit criteria:**
- At least one signed LOI or integration **or** documented decision to defer
- Liquidity plan does not imply guaranteed price or returns
- **No specific exchange promises** in roadmap or marketing until contracts exist

---

### Phase 5 — Proof of Contribution (research track)

**Goal:** Research alternate incentive or governance mechanisms **separately** from L1 stability.

**Deliverables:**
- PoC design doc in a **separate branch or repository**
- No consensus changes on mainnet until L1 is stable and Phase 2 exit criteria met

**Exit criteria:**
- L1 stable (Phase 2 complete, no critical open consensus issues)
- PoC repo/branch published with clear “not production” disclaimer
- Community review period before any mainnet proposal

---

## Non-goals (all phases)

- **No investment advice** — see [doc/LEGAL-NOTICE.md](doc/LEGAL-NOTICE.md)
- **No guaranteed returns** or price targets
- **Not a security offering** — software and network participation only
- No ICO/IEO/token sale described in this roadmap
- No “guaranteed exchange listing” language in Phases 0–2 (or ever, without signed fact)

---

## How to propose changes

1. Open an issue or PR describing the change and which phase it affects.
2. Update **this file** and, if relevant, `doc/PROJECT-STATUS.md` or `DEVLOG.md`.
3. Maintainer review before work is treated as official scope.

**Related:** [doc/PROJECT-STATUS.md](doc/PROJECT-STATUS.md) · [DEVLOG.md](DEVLOG.md) · [doc/WHITEPAPER-OUTLINE.md](doc/WHITEPAPER-OUTLINE.md)
