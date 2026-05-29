# Thoth block explorer — Phase 1 plan

Planning document for [ROADMAP.md](../ROADMAP.md) Phase 1 exit and [PHASE1-PREP.md](PHASE1-PREP.md) §C.
**No exchange listing promises** — see [LEGAL-NOTICE.md](LEGAL-NOTICE.md).

**Status:** Phase 1a **implemented** — [contrib/thoth-explorer](../contrib/thoth-explorer/). Blockbook deferred to Phase 3 listing prep. Public HTTPS URL pending VPS deploy.

**Decision (2026-05-30):** Option **A** (minimal Flask + JSON-RPC). Option **B** (Blockbook) deferred until pre–Phase 3.

---

## 1. Phase 1 exit requirements

From ROADMAP / PHASE1-PREP §C and §E:

| Requirement | Description |
|-------------|-------------|
| **Testnet coverage** | Public view of blocks and transactions on **testnet4** |
| **Public HTTPS URL** | Browser-accessible explorer (subdomain on VPS or static host) |
| **Accuracy** | Block hash, height, tx count, and coinbase must match **`thoth-cli -testnet`** on the same node |
| **Scope** | MWEB **disabled** — no extension-block or peg UI required in Phase 1 |
| **Mainnet** | Optional after testnet validation; mainnet explorer not required for Phase 1 exit |

Accuracy checks use local RPC — not third-party APIs.

---

## 2. Options comparison (A–D)

Thoth context: **Scrypt** PoW, **consensus v2**, **small chain**, **MWEB off**, Litecoin Core 0.21 lineage.

| Option | Description | Pros (Thoth) | Cons (Thoth) |
|--------|-------------|--------------|--------------|
| **A — Minimal RPC explorer** | Small service: `getblockchaininfo`, `getblock`, `getrawtransaction`; SQLite or in-memory cache; static HTML or lightweight SPA | Fast to ship; fits tiny chain; no MWEB code paths; easy to verify vs `thoth-cli` | Limited search (by height/hash only); no rich address history; manual maintenance |
| **B — Blockbook** | Trezor Blockbook indexer + API + stock or forked frontend | REST/WebSocket API; address/tx index; familiar to exchanges for **Phase 3 prep** (not a listing promise) | Heavier deploy; must fork coin defs for Thoth; Scrypt/LTC params; MWEB fields unused |
| **C — Esplora** | Blockstream Esplora (Rust) + electrs-style backend | Polished UX if ported | Bitcoin-centric; port effort for Scrypt/LTC/Thoth; overkill for Phase 1 testnet |
| **D — Electrs + custom UI** | electrs index + separate front-end | Lightweight index | Litecoin electrs exists but MWEB/extra fields; custom UI still needed; less listing-ready than Blockbook |

**Phase 1 constraint:** Prefer **low operational risk** and **fast accuracy verification** on a chain with &lt;1000 blocks initially.

---

## 3. Recommended path

### Phase 1a — Minimal RPC explorer (now)

**Implementation:** [contrib/thoth-explorer/README.md](../contrib/thoth-explorer/README.md) (Flask, testnet RPC on localhost).

- Deploy on **VPS** alongside existing testnet seed (`152.239.115.145`).
- Index via **`127.0.0.1:29332`** only (`thoth-cli -testnet` / `thothd` RPC).
- Public site: **`https://testnet-explorer.<domain>`** (nginx + TLS).
- Pages: latest blocks, block detail, tx detail, chain info (height, best hash).
- **Goal:** Satisfy Phase 1 “explorer shows blocks, txs, chain tips correctly” with minimal code.

### Phase 1b — Blockbook fork (deferred to Phase 3 prep)

- Before [ROADMAP.md](../ROADMAP.md) Phase 3 listing **prep** (requirements packet only), evaluate Blockbook with a **`thoth-testnet`** / **`thoth`** coin definition.
- Reuse Phase 1a accuracy checklist; add address lookup and stable API for integrators.
- **Not** a commitment to CoinGecko/CMC or any exchange.

---

## 4. Thoth RPC for indexers (localhost only)

| Network | RPC port | Bind | CLI flag |
|---------|----------|------|----------|
| Testnet | **29332** | `127.0.0.1` | `-testnet` |
| Mainnet | **19332** | `127.0.0.1` | *(default)* |

**Never** expose RPC to the public internet. The explorer backend runs on the VPS and talks to `thothd` on loopback.

Example sanity check:

```bash
thoth-cli -testnet -rpcconnect=127.0.0.1 -rpcport=29332 getblockchaininfo
thoth-cli -testnet getblockhash 0
thoth-cli -testnet getblock $(thoth-cli -testnet getblockhash 0) 2
```

Use RPC credentials from `~/.thoth/thoth.conf` (`[test]` section); do not commit passwords to git.

---

## 5. VPS deploy outline (Phase 1a)

Assumes Ubuntu 22.04 VPS already running testnet `thothd`.

1. **DNS:** `testnet-explorer.example.com` → VPS IP (A record).
2. **Firewall:** `ufw allow OpenSSH`; `ufw allow 443/tcp`; **do not** open 29332 or 29335 for explorer-specific rules (P2P 29335 already for testnet seed).
3. **Explorer service:** systemd unit; binds **127.0.0.1:8080** (or similar).
4. **nginx:** reverse proxy `443` → `127.0.0.1:8080`; HSTS optional after TLS stable.
5. **TLS:** Certbot / Let's Encrypt for the subdomain.
6. **Monitoring:** log sync height vs `getblockcount`; alert if lag &gt; N blocks.

No RPC or wallet keys in the explorer repository.

---

## 6. Blockbook config touch points (Phase 1b)

If/when forking [Blockbook](https://github.com/trezor/blockbook), define a Thoth coin (names illustrative):

| Field | Mainnet | Testnet |
|-------|---------|---------|
| Coin name | `Thoth` | `Thoth Testnet` |
| Shortcut | `TTH` | `TTTH` *(informal)* |
| Coin shortcut (API) | `tth` | `tth_test` |
| SLIP-44 | **2** *(Litecoin lineage; confirm before hardware wallet claims)* | 2 *(test)* |
| Decimals | 8 | 8 |
| P2P port | 19333 | 29335 |
| RPC port | 19332 | 29332 |
| Bech32 HRP | `tth` | `ttth` |
| xpub/xprv magic | `0x0488b21e` / `0x0488ade4` | `0x043587cf` / `0x04358394` |
| P2PKH version | 48 (`T…` legacy) | 111 |
| P2SH version | 5 | 196 |
| Message start | `54 48 4f 54` | `fd d2 c8 f1` |
| Genesis hash | `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784` | `439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651` |
| MWEB | **Omit / disable** in coin params | same |

Blockbook must point at **`127.0.0.1`** RPC with `-testnet` equivalent in coin config. Scrypt does not change Blockbook’s RPC parsing, but coin **must** match `chainparams.cpp`.

---

## 7. Verification checklist

Run after deploy; compare explorer output to `thoth-cli` on the same host.

### Testnet (required for Phase 1)

- [ ] **Genesis (height 0):** hash `439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651`
- [ ] **Chain tip:** `getblockcount` matches explorer “best height”
- [ ] **Best block hash** matches `getbestblockhash`
- [ ] **Block detail:** merkle root, time, tx count match `getblock <hash> 2`
- [ ] **Coinbase tx** visible at height ≥ 1 when mined
- [ ] **HTTPS** URL loads without RPC port exposed (scan 29332 from outside — closed)

### Mainnet (when blocks exist — informational)

- [ ] **Genesis:** `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784`
- [ ] **Height 1:** hash `6123e5e50555e456fa8808230311538235343d8fdb8fd380de8ad9ab89ea20d1` ([PROJECT-STATUS.md](PROJECT-STATUS.md))

Document results in DEVLOG and check off [PHASE1-PREP.md](PHASE1-PREP.md) §C.

---

## 8. Legal

Explorer data is **informational** only. No investment advice, no price data, **no exchange listing guarantees**.
[LEGAL-NOTICE.md](LEGAL-NOTICE.md) applies to all public Thoth materials.

---

**Links:** [PHASE1-PREP.md](PHASE1-PREP.md) · [TESTNET-JOIN.md](TESTNET-JOIN.md) · [PROJECT-STATUS.md](PROJECT-STATUS.md) · [DEVLOG.md](../DEVLOG.md)
