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

### Current mainnet state (2026-05-29)

| Metric | Value |
|--------|--------|
| Best block height | **3** (genesis + 3 mined blocks) |
| Public seed | `addnode=152.239.115.145:19333` |
| DNS seeds / fixed seeds | Disabled (manual `addnode` bootstrap) |

---

## Pending

- **Block explorer** — none deployed yet; needs indexer/API and web UI.
- **Public network growth** — more independent nodes, DNS seeds or hardcoded seeds when stable.
- **BIP activation heights review** — audit segwit/taproot (and related) deployment heights vs. new chain birth; adjust `chainparams` if needed before wide release.
- **PoC / experiments** — keep proof-of-concept work (alternate ideas, tooling spikes) in a **separate branch or repo** so mainnet core stays minimal and reviewable.

---

## Key commits (reference)

| Commit | Summary |
|--------|---------|
| `795ee92dc` | Rebrand to Thoth (TTH): genesis, chainparams, Arch build support |
| `031225f70` | BDB 4.8 wallet build profile for Arch/CachyOS |
| `12b548c5a` | Join-the-network instructions in README |
