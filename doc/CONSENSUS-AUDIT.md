# Thoth consensus / BIP height audit

**Date:** 2026-05-29  
**Phase:** [1 — Public testnet & infrastructure](../ROADMAP.md#phase-1--public-testnet--infrastructure)  
**Scope:** Documentation and recommendations only — **no `chainparams.cpp` changes in this task.**

**Source of truth (current code):** `src/chainparams.cpp` as of repository `main`.  
**Related:** [PHASE1-PREP.md](PHASE1-PREP.md) §A · [WHITEPAPER.md](WHITEPAPER.md) §8 · [ROADMAP.md](../ROADMAP.md)

---

## 1. Inventory (extracted from `chainparams.cpp`)

Values below are **what the code sets today**. Thoth genesis is 2024+; mainnet best height is **~3**.

### 1.1 Core consensus heights

| Parameter | Mainnet | Testnet | Regtest |
|-----------|---------|---------|---------|
| **BIP16Height** | 218579 | 0 | 0 |
| **BIP34Height** | 710000 | 76 | 500 |
| **BIP34Hash** | `fa09d204a83a768ed5a7c8d441fa62f2043abf420cff1226c7b4329aeb9d51cf` | `8075c771ed8b495ffd943980a95f702ab34fce3c8c54e379548bda33cc8c0573` | *(null / unused)* |
| **BIP65Height** | 918684 | 76 | 1351 |
| **BIP66Height** | 811879 | 76 | 1251 |
| **CSVHeight** | 1201536 | 6048 | 432 |
| **SegwitHeight** | 1201536 | 6048 | 0 *(always on unless `-segwitheight`)* |
| **MinBIP9WarningHeight** | 1209600 | 8064 | 0 |

**Version-bits windows (BIP9-style height deployments on main/test):**

| Parameter | Mainnet | Testnet | Regtest |
|-----------|---------|---------|---------|
| **nRuleChangeActivationThreshold** | 6048 (75% of 8064) | 1512 (75% of 2016) | 108 (75% of 144) |
| **nMinerConfirmationWindow** | 8064 | 2016 | 144 |

### 1.2 Taproot deployment (`DEPLOYMENT_TAPROOT`)

| Field | Mainnet | Testnet | Regtest |
|-------|---------|---------|---------|
| **bit** | 2 | 2 | 2 |
| **nStartHeight** | 2161152 | 2225664 | — *(uses time)* |
| **nTimeoutHeight** | 2370816 | 2435328 | — |
| **nStartTime** | — | — | `ALWAYS_ACTIVE` |
| **nTimeout** | — | — | `NO_TIMEOUT` |

### 1.3 MWEB deployment (`DEPLOYMENT_MWEB`)

| Field | Mainnet | Testnet | Regtest |
|-------|---------|---------|---------|
| **bit** | 4 | 4 | 4 |
| **nStartHeight** | 2217600 | 2209536 | — |
| **nTimeoutHeight** | 2427264 | 2419200 | — |
| **nStartTime** | — | — | 1601450001 |
| **nTimeout** | — | — | `NO_TIMEOUT` |

### 1.4 MWEB Litecoin-specific consensus fields

| Field | Mainnet | Testnet | Regtest |
|-------|---------|---------|---------|
| **mweb_input_metadata_grandfather_blockhash** | `d1695b5d115f86927a9763768218118ba88b315844e1a0681fa08f6f008be622` | *(not set)* | *(not set)* |
| **frozen_mweb_output_ids** | 1 ID: `2f3a08d9f5ef5f388386c11efe935394b14b524220cff4ec5c81942b82e694f7` | *(not set)* | Same as mainnet via `GetFrozenMWEBOutputIDs()` |

These constants refer to **Litecoin mainnet history** (grandfather block, frozen peg-out). They have **no valid meaning** on Thoth blocks unless the same block hashes exist—which they do not and will not.

**Code touch points (reference only):** `src/mweb/mweb_node.cpp`, `src/consensus/tx_verify.cpp`, `src/wallet/wallet.cpp`, `consensus/params.h`.

### 1.5 Economics, PoW, wire format

| Parameter | Mainnet | Testnet | Regtest |
|-----------|---------|---------|---------|
| **nSubsidyHalvingInterval** | 840000 | 840000 | 150 |
| **powLimit** | `00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff` | same as mainnet | `7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff` |
| **nPowTargetTimespan** | 3.5 days | 3.5 days | 3.5 days |
| **nPowTargetSpacing** | 150 s (2.5 min) | 150 s | 150 s |
| **fPowAllowMinDifficultyBlocks** | false | true | true |
| **fPowNoRetargeting** | false | false | true |
| **pchMessageStart** | `54 48 4f 54` (`THOT`) | `fd d2 c8 f1` | `fa bf b5 da` |
| **nDefaultPort (P2P)** | 19333 | 29335 | 19444 |
| **RPC port** *(chainparamsbase, not chainparams)* | 19332 | 29332 | 19443 |
| **bech32_hrp** | `tth` | `ttth` | `rtth` |
| **mweb_hrp** | `tthmweb` | `tmweb` | `tmweb` |

### 1.6 Genesis (Thoth — not Litecoin)

| Network | nTime | nNonce | nBits | hashGenesisBlock |
|---------|-------|--------|-------|------------------|
| Mainnet | 1735000000 | 1454933 | 0x1e0ffff0 | `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784` |
| Testnet | 1735000060 | 2236257 | 0x1e0ffff0 | `439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651` |
| Regtest | 1735000120 | 1 | 0x207fffff | `b6ae6fa79bdde8d750bc8dff1e1a0f053dc45422a11f100d57623143fc0e1381` |

### 1.7 Effective rules at mainnet height ~3 (today)

| Rule | Active at height 3? | Notes |
|------|---------------------|-------|
| BIP16 (P2SH) | **No** (activates 218579) | Legacy Litecoin height |
| BIP34 (height in coinbase) | **No** (activates 710000) | `BIP34Hash` is a **Litecoin** block hash |
| BIP65 / BIP66 | **No** | Heights in millions / thousands |
| CSV | **No** | Height 1,201,536 |
| Segwit | **No** | Height 1,201,536 |
| Taproot | **No** | Version-bits window starts ~2.16M |
| MWEB | **No** | Version-bits window starts ~2.2M |

Early blocks therefore behave like **pre-Segwit, pre-BIP16-enforcement** consensus, while the **parameter table still documents Litecoin’s timeline** for future heights—a mismatch for a 2024 genesis chain.

---

## 2. Problem statement

1. **Wrong chain history assumptions.** `BIP34Hash`, `mweb_input_metadata_grandfather_blockhash`, and `frozen_mweb_output_ids` embed **Litecoin block/content identifiers**. Thoth mainnet will never produce block 709999 with hash `fa09d204…`. If the network ever reached height 710000 with current params, **BIP34 enforcement would reject the chain**.

2. **Absurd activation calendar.** Segwit/Taproot/MWEB heights (~1.2M–2.4M) imply multi-decade delays on a chain with **~3 blocks** and no economic activity. This is confusing for operators, explorers, and wallet authors.

3. **MWEB without MWEB history.** Mainnet carries Litecoin MWEB grandfather/frozen-output rules. Thoth has **no MWEB blocks** and no peg-in/out history; enabling MWEB later would activate code paths tested against Litecoin, not Thoth.

4. **Public network risk.** Launching **public testnet or “mainnet”** without an explicit activation policy invites:
   - wallets/explorers assuming Segwit/Taproot availability based on upstream docs;
   - accidental transactions invalid under future re-parameterization;
   - need for **chain reset** if heights are fixed after more blocks are mined.

5. **Testnet partially inconsistent.** Testnet uses low BIP heights (76, 6048) but still **Litecoin-era Taproot/MWEB height windows** (~2.2M). Testnet genesis is Thoth-specific; `BIP34Hash` points at block 75 of **Litecoin testnet history**, not Thoth testnet block 75.

**Conclusion:** Proceeding to Phase 1 public testnet requires a **documented activation plan** and a follow-up **`chainparams.cpp` PR**—not silent reliance on inherited Litecoin numbers.

---

## 3. Recommended strategies (three options)

### Option A — Core BIPs from near-genesis; defer Taproot/MWEB

**Policy:** Set BIP16=0, BIP34/65/66=1 (or small stagger), CSV/Segwit within first ~200 blocks; set `BIP34Hash` to **Thoth genesis hash** (block at height `BIP34Height - 1`). Push Taproot/MWEB to high staging heights or `NEVER_ACTIVE` until separately reviewed.

**Example proposed heights (illustrative for a future PR):**

| Parameter | Mainnet | Testnet |
|-----------|---------|---------|
| BIP16Height | 0 | 0 |
| BIP34Height | 1 | 1 |
| BIP34Hash | `3f2dc0f6…` (mainnet genesis) | `439581a3…` (testnet genesis) |
| BIP65Height | 1 | 1 |
| BIP66Height | 1 | 1 |
| CSVHeight | 2 | 2 |
| SegwitHeight | 144 | 144 |
| MinBIP9WarningHeight | 2208 | 2160 |
| Taproot | `nStartHeight` 8064 / timeout +209664 blocks | same pattern (testnet window 2016) |
| MWEB | `NEVER_ACTIVE` or `nStartHeight` = max | same |

| Pros | Cons |
|------|------|
| Modern rules early; clear story for a new L1 | **Invalidates existing mainnet blocks 1–3** if BIP34=1 (no height in coinbase) |
| Correct `BIP34Hash` for Thoth genesis | Requires **mainnet regenesis / reset** and operator coordination |
| Segwit available for public testnet quickly | Taproot still delayed unless staged lower |

**Impact on ~3 mainnet blocks:** **Chain reset required** (delete `blocks/`/`chainstate/`, remine from genesis). **Keep chain** only if activation heights stay above 3 *and* above current tip—but that leaves Litecoin `BIP34Hash` bug unfixed until reset anyway.

---

### Option B — Staged activation (core early, Taproot/MWEB later)

**Policy:** Same near-genesis core BIPs as Option A, but **explicit high blocks** for Taproot (e.g. 50,000) and MWEB (e.g. 100,000 or never). Document calendar (~block time 2.5 min) so operators know when features activate.

| Pros | Cons |
|------|------|
| Predictable feature rollout | More parameters to maintain and communicate |
| Time to audit MWEB before its window | Still requires **reset** if core BIPs move below current tip |
| Matches “progressive hardening” narrative | Long wait for Taproot/MWEB unless heights set low |

**Impact on ~3 mainnet blocks:** Same as Option A for core BIP changes → **reset**. If only Taproot/MWEB heights change (core left as-is), existing 3 blocks **remain valid** but **Litecoin `BIP34Hash` landmine remains** at height 710000.

---

### Option C — Disable MWEB for initial public networks

**Policy:** Do not activate MWEB on mainnet/testnet until a dedicated review pass. Implementation approaches (future PR):

- Set `DEPLOYMENT_MWEB` to `NEVER_ACTIVE` / `NO_TIMEOUT` (height- or time-based per network class).
- Clear `mweb_input_metadata_grandfather_blockhash` (null hash).
- Clear `frozen_mweb_output_ids` (empty vector) on mainnet/testnet.
- Document in release notes that **MWEB RPC/wallet paths are dormant**.

| Pros | Cons |
|------|------|
| Removes Litecoin-specific consensus landmines | Loses MWEB privacy feature until re-enabled |
| Smaller attack surface for Phase 1 | Upstream merge conflicts in `src/mweb/` over time |
| Simpler explorer/wallet scope | Re-enabling MWEB later is a **consensus change** |

**Impact on ~3 mainnet blocks:** **No effect by itself** (MWEB not active yet). Combine with A or B for full fix.

**Code touch points (future PR):** `src/chainparams.cpp` (deployments + grandfather/frozen IDs), possibly `versionbitsinfo.h` / release notes; functional tests under `test/functional/` referencing MWEB.

---

## 4. Proposed default recommendation

**Adopt Option A (near-genesis core BIPs) + Option C (disable MWEB)** for Thoth’s **first public testnet** and any **public mainnet relaunch**.

**Rationale (height ~3):**

- Only **three** non-genesis blocks exist; **chain reset cost is minimal** compared to fixing consensus later at height 710000 or after public users depend on the chain.
- **Simplicity and security** beat carrying Litecoin MWEB grandfather/frozen peg rules on a chain with no MWEB history.
- Segwit from ~144 blocks (~6 hours) is enough for modern addresses on testnet; Taproot can activate after one retarget period (mainnet window 8064 ≈ 14 days).
- Testnet should **not** reuse Litecoin `BIP34Hash`; it should use **Thoth testnet genesis**.

### 4.1 Proposed height table (default for future `chainparams` PR)

| Parameter | Mainnet (proposed) | Testnet (proposed) |
|-----------|-------------------|-------------------|
| BIP16Height | 0 | 0 |
| BIP34Height | 1 | 1 |
| BIP34Hash | `3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784` | `439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651` |
| BIP65Height | 1 | 1 |
| BIP66Height | 1 | 1 |
| CSVHeight | 2 | 2 |
| SegwitHeight | 144 | 144 |
| MinBIP9WarningHeight | 2208 | 2160 |
| Taproot bit | 2 | 2 |
| Taproot nStartHeight | 8064 | 8064 |
| Taproot nTimeoutHeight | 101376 | 101376 |
| MWEB | **Disabled** (`NEVER_ACTIVE`) | **Disabled** |
| mweb_input_metadata_grandfather_blockhash | **null** | **null** |
| frozen_mweb_output_ids | **empty** | **empty** |
| nSubsidyHalvingInterval | 840000 *(unchanged)* | 840000 *(unchanged)* |

*Regtest:* keep flexible defaults for functional tests; override via `-vbparams` / `-segwitheight` as today. Document any regtest-specific MWEB disable in test README.

**Mainnet operator action after merge:** wipe datadirs on all nodes, sync to new chain from genesis, remine; update DEVLOG and PROJECT-STATUS with new “consensus v2” genesis tip.

---

## 5. Implementation checklist (future PR — not this task)

- [ ] **ROADMAP.md** — note consensus change scope; no exchange promises
- [ ] **`src/chainparams.cpp`** — apply chosen option; remove or null Litecoin MWEB constants
- [ ] **`src/chainparams.cpp` (regtest)** — align if needed; preserve `-vbparams` behavior
- [ ] **`doc/release-notes-thoth.md`** — consensus migration section, reset instructions
- [ ] **`doc/WHITEPAPER.md` §8** — replace “pending review” with final heights
- [ ] **`doc/CONSENSUS-AUDIT.md`** — append “Resolved in PR #…” with date
- [ ] **`doc/PROJECT-STATUS.md`** — new height, reset notice
- [ ] **Functional tests** — `test/functional/*` segwit/taproot/MWEB cases; run on regtest/testnet
- [ ] **Regtest/testnet re-genesis** — if genesis unchanged but heights change, reindex may suffice; if coinbase rules change at height ≤ tip, **full reset**
- [ ] **Peer coordination** — announce reset on seed node; bump P2P `protocol version` or user-agent tag if helpful
- [ ] **PHASE1-PREP.md §A** — check remaining boxes after merge + peer review

### DEVLOG entry template (after implementation)

```markdown
### YYYY-MM-DD — Consensus parameter migration (Phase 1)

- Applied Option A+C from [doc/CONSENSUS-AUDIT.md](doc/CONSENSUS-AUDIT.md).
- Mainnet/testnet: near-genesis BIP heights; MWEB disabled; Litecoin grandfather/frozen IDs removed.
- **Chain reset:** mainnet datadir wiped on seed + home node; height restarted from 0.
- Release notes: doc/release-notes-thoth.md#consensus-….
- Commit: `<hash>` — `consensus: Thoth activation heights for new chain (MWEB disabled)`
```

---

## 6. Open questions for maintainer

1. **Keep MWEB long-term or defer indefinitely?** Default recommendation: **defer** until Thoth-specific MWEB review and testnet soak without MWEB complete.

2. **Reset mainnet after param change?** At height ~3, **yes — recommended**. Alternative (keep 3 blocks) only if core BIP heights remain above 3 *and* team accepts fixing `BIP34Hash` later via another reset (not recommended).

3. **Single shared activation plan for testnet + mainnet?** **Same policy**, different `BIP34Hash`/genesis; testnet should activate **first** for 30-day soak ([PHASE1-PREP.md](PHASE1-PREP.md) §B).

4. **Taproot at 8064 vs lower?** Trade-off: earlier Taproot vs more testing time on Segwit-only testnet.

5. **Regtest MWEB in functional tests:** disable globally or keep regtest-only MWEB for upstream test parity?

---

**Audit status:** **Resolved** — Option A + C implemented in `src/chainparams.cpp` (consensus v2). See appendix below.

---

## Appendix — Resolved (2026-05-29)

| Item | Resolution |
|------|------------|
| Strategy | **Option A + C** per §4 |
| Mainnet reset | **Approved** — wipe datadir; height returns to 0 |
| MWEB | **Deferred** — `NEVER_ACTIVE` on mainnet/testnet; regtest default off |
| Implementation | `src/chainparams.cpp` — genesis asserts unchanged |
| Docs | `release-notes-thoth.md`, `WHITEPAPER.md` §8, `PROJECT-STATUS.md`, `DEVLOG.md` |
| Commit | `consensus: Thoth near-genesis BIP heights, disable MWEB (chain reset required)` |

**Open questions (§6) closed:**

1. MWEB — defer until separate review.
2. Mainnet reset — yes, at height ~3.
3. Shared plan — same heights; different `BIP34Hash`/genesis per network.
4. Taproot 8064 — adopted as proposed.
5. Regtest MWEB — `NEVER_ACTIVE`; tests need `-vbparams` to enable MWEB locally.
