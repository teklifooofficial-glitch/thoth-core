# Thoth Core — development log

Internal project timeline for Thoth (TTH). No RPC credentials or tokens are stored here.

**Repository:** [teklifooofficial-glitch/thoth-core](https://github.com/teklifooofficial-glitch/thoth-core)  
**Last updated:** 2026-05-29

---

## Project info

| Item | Value |
|------|--------|
| Name / ticker | Thoth / **TTH** |
| Base | Litecoin Core 0.21 lineage (full node fork) |
| Proof-of-work | **Scrypt** |
| Block target | 2.5 minutes (150 s) |
| Subsidy halving | Every 840,000 blocks |
| Bech32 HRP (main / test / regtest) | `tth` / `ttth` / `rtth` |
| Binaries | `thothd`, `thoth-cli`, `thoth-qt`, `thoth-wallet`, `thoth-tx` |
| Mainnet datadir | `~/.thoth/` |
| Testnet datadir | `~/.thoth/testnet4/` |
| Regtest datadir | `~/.thoth/regtest/` |

### Network ports

| Network | RPC (localhost only) | P2P |
|---------|----------------------|-----|
| Mainnet | 19332 | 19333 |
| Testnet | 29332 | 29335 |
| Regtest | 19443 | 19444 |

### Genesis block hashes

| Network | Hash |
|---------|------|
| Mainnet | `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784` |
| Testnet | `439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651` |
| Regtest | `b6ae6fa79bdde8d750bc8dff1e1a0f053dc45422a11f100d57623143fc0e1381` |

Genesis coinbase message: *"Thoth blockchain - wisdom and knowledge for all - 2024"*

---

## Changelog

### 2026-05-05 — Upstream baseline

- Tree based on **Litecoin Core v0.21.5.5** (`d8c8adc0b`).

### 2026-05-26 — Rebrand and genesis

- Full rebrand Litecoin → **Thoth (TTH)**: chainparams, binaries, docs, build system (`795ee92dc`).
- New genesis parameters in `src/chainparams.cpp`; timestamps and asserts for mainnet, testnet, regtest.
- **`genesis_miner.py`**: Python Scrypt miner to find `nNonce` per network (`pip install scrypt`).
- Build fixes on **Arch/CachyOS**: Boost m4, UPnP (`net.cpp`), Qt splash path, BDB install script patches.

### 2026-05-26 — Wallet and build docs

- Documented **BDB 4.8** wallet build profile for Arch (`031225f70`, `doc/build-unix.md`, `contrib/build_wallet_arch.sh`).
- System BDB 6.x with `--with-incompatible-bdb` builds CLI but can **segfault** wallet creation on Arch; BDB 4.8 via `./contrib/install_db4.sh` is the supported wallet path.

### 2026-05-26 — Local testing (regtest / mainnet / testnet)

- **Regtest:** `thothd -regtest`, `generatetoaddress` with wallet when BDB 4.8 is linked.
- **Mainnet (isolated):** genesis hash verified via RPC; block 1 mined with `generatetoaddress` (~1M tries).
- **Testnet:** genesis verified; higher try counts (e.g. 5M) sometimes needed.
- Mining uses **`generatetoaddress`** (not legacy `gen=1`).

### 2026-05-26 — GitHub remote

- Primary remote: **https://github.com/teklifooofficial-glitch/thoth-core.git** (`origin`).
- Upstream reference retained as `litecoin-upstream`.

### 2026-05-29 — Ubuntu VPS public seed node

- **Hostinger VPS** `152.239.115.145` (Ubuntu 22.04.5 LTS): system update, SSH key auth, **ufw** (`OpenSSH`, **19333/tcp** only; RPC not exposed).
- Build deps added beyond base list: `libdb-dev`, `libdb++-dev`, `libfmt-dev`.
- Headless build: `./configure --without-gui --with-incompatible-bdb`, `make -j$(nproc)`.
- **`thothd`** run under **systemd** on the VPS; `[main]` config with `listen=1`, `dnsseed=0`, `fixedseeds=0`, public P2P on 19333.

### 2026-05-29 — Two-node mainnet network

- **Node A:** local Arch/CachyOS full node.
- **Node B:** VPS seed at `152.239.115.145:19333`.
- Peering via `addnode=` in `~/.thoth/thoth.conf`; verified with `getconnectioncount` and `getblockchaininfo`.
- **Chain state sync:** initial blocks directory copied between nodes with **`scp`** so both started from the same mined chain (manual bootstrap before wider peer discovery).

### 2026-05-29 / 2026-05-30 — Join-the-network documentation

- README **"Join the network"** section: seed peer, sample `[main]` config, build pointers, verification commands (`12b548c5a`).
- README listed chain tip at height **2** at commit time; network has since advanced.

### 2026-05-29 — Phase 0 governance (GitHub)

- **`ROADMAP.md`**: Phases 0–5, exit criteria, non-goals, “update roadmap first” rule (`7ec44fe33`).
- **`doc/PROJECT-STATUS.md`**: snapshot (height ~3, two nodes, known limits).
- **`doc/WHITEPAPER-OUTLINE.md`**, **`doc/LEGAL-NOTICE.md`**: outline and disclaimers.
- **README** project-status box: early development, not exchange-listed.
- Pushed to **teklifooofficial-glitch/thoth-core** on `main`.

### 2026-05-29 — Whitepaper draft and Phase 1 prep

- **`doc/WHITEPAPER.md`**: draft from outline — tokenomics, network params, honest dev stage, MWEB inherited (Phase 1 BIP review pending).
- **`doc/PHASE1-PREP.md`**: checklist (BIP review, testnet soak, explorer options, 10-node goal).
- **ROADMAP** Phase 0 updated: whitepaper draft completes exit criteria except optional website.
- **PROJECT-STATUS** next actions shifted to post–Phase 0 / pre–Phase 1.

### 2026-05-29 — Phase 1 started; consensus audit

- **Phase 1** opened per [ROADMAP.md](../ROADMAP.md): focus on consensus / BIP height review ([PHASE1-PREP.md](PHASE1-PREP.md) §A).
- **`doc/CONSENSUS-AUDIT.md`**: full inventory from `src/chainparams.cpp`, problem statement, Options A/B/C, default recommendation (near-genesis BIPs + disable MWEB), proposed height table, future PR checklist.
- **No `chainparams.cpp` changes** in this step — audit and recommendations only.
- [PROJECT-STATUS.md](PROJECT-STATUS.md) and ROADMAP current stage updated to Phase 1.

### 2026-05-29 — Consensus parameter migration (Phase 1)

- Applied **Option A + C** from [doc/CONSENSUS-AUDIT.md](doc/CONSENSUS-AUDIT.md).
- Mainnet/testnet: near-genesis BIP heights; MWEB disabled; Litecoin grandfather/frozen IDs removed.
- **Chain reset:** mainnet datadir must be wiped on seed + home node; height returns to **0** (genesis unchanged).
- Release notes: [doc/release-notes-thoth.md](doc/release-notes-thoth.md#consensus-v2-thoth-mainnet--testnet).
- Regtest: MWEB `NEVER_ACTIVE` by default; MWEB functional tests require `-vbparams` override.
- Commit: `consensus: Thoth near-genesis BIP heights, disable MWEB (chain reset required)` (`0a45b1856`).

### 2026-05-29 — Consensus v2 chain restart (operators)

- **Migration complete:** home + VPS seed reset datadirs, rebuilt v2 chain from genesis.
- **Pre-v2 chain invalidated** (~height 3); fresh v2 mainnet from block 0.
- **Both nodes synced** on mainnet (home + `152.239.115.145:19333`).
- **Tip:** height **1**, best block `6123e5e50555e456fa8808230311538235343d8fdb8fd380de8ad9ab89ea20d1`.
- **Next Phase 1:** publish testnet join doc ([PHASE1-PREP.md](PHASE1-PREP.md) §B).

### 2026-05-29 — Testnet join guide (Phase 1)

- **`doc/TESTNET-JOIN.md`**: testnet4 datadir, genesis, ports, `[test]` config, build/run, mining (legacy before block 144 / `ttth1` after), v2 reset, consensus links, legal notice.
- README **Testnet** section links the guide.
- [PHASE1-PREP.md](PHASE1-PREP.md) §B: join doc published.

### 2026-05-29 — Testnet seed published

- **Public testnet seed:** `addnode=152.239.115.145:29335` (VPS).
- **Testnet peering verified:** home node + VPS seed; **2 peers** on testnet4.
- README **Join testnet** section and [TESTNET-JOIN.md](TESTNET-JOIN.md) updated with seed endpoint.

### 2026-05-30 — Testnet soak period started (Phase 1)

- **Soak start:** 2026-05-30; **end target:** ~2026-06-29 (30-day Phase 1 criterion).
- **Criteria:** no consensus failures; VPS testnet seed uptime; peer count logged weekly in [PROJECT-STATUS.md](PROJECT-STATUS.md).
- **Week 0:** 2 peers (home + VPS seed).

### 2026-05-30 — Block explorer planning (Phase 1 §C)

- **`doc/EXPLORER-PLAN.md`**: requirements, options A–D, recommended Phase 1a (minimal RPC on testnet VPS) + Phase 1b (Blockbook before Phase 3 prep).
- RPC indexers use **localhost only** (29332 testnet, 19332 mainnet).
- [PHASE1-PREP.md](PHASE1-PREP.md) §C: approach selection in progress.

### 2026-05-30 — Minimal testnet explorer (Phase 1a)

- **`contrib/thoth-explorer/`**: Flask app — `/`, `/block/<height>`, `/block/hash/<hash>`, `/tx/<txid>`, `/api/status`.
- RPC via env vars; `.env` gitignored. Blockbook deferred to Phase 3 prep.
- Public HTTPS URL pending VPS deploy.

### 2026-05-30 — Testnet explorer live

- **URL:** http://152.239.115.145:8080/ (Phase 1a minimal RPC explorer on VPS).
- Reads testnet RPC on `127.0.0.1:29332` only; no RPC exposed publicly.
- [PROJECT-STATUS.md](PROJECT-STATUS.md) updated; README **Join testnet** links explorer.

### 2026-05-30 — Project landing page (Phase 1 outreach)

- **`contrib/thoth-landing/`**: static `index.html` + CSS — status, docs links, network seeds, explorer link.
- Deploy target: http://152.239.115.145/ (nginx port 80; separate from explorer :8080).
- No RPC secrets; no exchange promises.

### 2026-05-30 — Testnet node operator guide

- **`doc/RUN-A-TESTNET-NODE.md`**: developer/hobbyist walkthrough (build, `[test]` config, seed, verify, optional mining).
- README **Join testnet** and landing page link to the guide.
- Phase 1 focus: recruit independent operators (≥10 node goal).

### Current mainnet state (2026-05-29, consensus v2)

| Metric | Value |
|--------|--------|
| Best block height | **1** |
| Best block hash | `6123e5e50555e456fa8808230311538235343d8fdb8fd380de8ad9ab89ea20d1` |
| Genesis hash | `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784` |
| Nodes | **2** synced (home + VPS seed) |
| Public seed | `addnode=152.239.115.145:19333` |
| MWEB | Disabled on mainnet/testnet |

### Current testnet state (2026-05-30)

| Metric | Value |
|--------|--------|
| Soak | **2026-05-30 → ~2026-06-29** |
| Public seed | `addnode=152.239.115.145:29335` |
| Explorer | http://152.239.115.145:8080/ |
| Landing | http://152.239.115.145/ (static; deploy via nginx) |
| Peers | **2** (home + VPS; week 0 log) |
| Genesis hash | `439581a3…5651` (full hash in [TESTNET-JOIN.md](doc/TESTNET-JOIN.md)) |

---

## Pending

- **Block explorer** — testnet live at http://152.239.115.145:8080/; TLS optional.
- **Public network growth** — operator onboarding via [RUN-A-TESTNET-NODE.md](doc/RUN-A-TESTNET-NODE.md); ≥10 testnet nodes goal.
- **BIP / consensus v2** — live on mainnet; migration complete (`0a45b1856`).
- **PoC / experiments** — keep proof-of-concept work (alternate ideas, tooling spikes) in a **separate branch or repo** so mainnet core stays minimal and reviewable.

---

## Key commits (reference)

| Commit | Summary |
|--------|---------|
| `795ee92dc` | Rebrand to Thoth (TTH): genesis, chainparams, Arch build support |
| `031225f70` | BDB 4.8 wallet build profile for Arch/CachyOS |
| `12b548c5a` | Join-the-network instructions in README |
| `893760b50` | DEVLOG |
| `7ec44fe33` | Phase 0 governance (ROADMAP, PROJECT-STATUS, legal notice) |
| `0a45b1856` | Consensus v2: near-genesis BIPs, MWEB disabled |
