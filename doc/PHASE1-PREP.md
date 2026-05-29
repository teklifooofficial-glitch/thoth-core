# Phase 1 preparation checklist

Per [ROADMAP.md](../ROADMAP.md#phase-1--public-testnet--infrastructure). **Checklist only** — no dates or exchange commitments. Update items as completed; link evidence in [DEVLOG.md](../DEVLOG.md).

**Prerequisite:** Phase 0 exit criteria met ([ROADMAP.md](../ROADMAP.md#phase-0--trust--transparency-current)).

---

## A. Consensus / BIP height review

- [x] Inventory all deployment heights in `src/chainparams.cpp` — [CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md) §1
- [x] Document intended activation strategy for a chain born **2024+** at height 0 — [CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md) §4, implemented consensus v2
- [x] Decide: retain, reset, or disable MWEB — **disabled** (Option C); regtest default off
- [x] Draft `chainparams` patch + release notes — merged (consensus v2)
- [ ] Peer review by at least one non-author contributor
- [ ] Regtest/testnet re-sync tests after any height change

---

## B. Public testnet campaign

- [x] Publish testnet join doc — [TESTNET-JOIN.md](TESTNET-JOIN.md)
- [x] Run public testnet node(s) with stable uptime target — VPS seed `152.239.115.145:29335`
- [ ] Testnet mining guide (`generatetoaddress`, expected try counts)
- [ ] Optional: faucet script or documented donate-and-faucet process
- [ ] **Soak period:** continuous testnet ≥ **30 days** without consensus failures — **in progress** (started **2026-05-30**, end target **~2026-06-29**)
- [x] Log incidents in DEVLOG / PROJECT-STATUS — weekly peer count (see [PROJECT-STATUS.md](PROJECT-STATUS.md))

---

## C. Block explorer (evaluate → deploy)

**Plan:** [EXPLORER-PLAN.md](EXPLORER-PLAN.md) — Phase 1a minimal RPC explorer (testnet); Phase 1b Blockbook fork before Phase 3 listing prep.

**Options summary:**

| Option | Pros | Cons |
|--------|------|------|
| **A — Minimal RPC** *(recommended Phase 1a)* | Fast, accurate for small chain; MWEB N/A | Limited search |
| **B — Blockbook** *(Phase 1b)* | API for integrators | Fork coin config; heavier |
| **C — Esplora** | Mature UX | Large port effort |
| **D — Electrs + UI** | Light index | Custom UI; MWEB noise |

**Checklist:**

- [x] Pick approach — **Option A** minimal RPC ([contrib/thoth-explorer/README.md](../contrib/thoth-explorer/README.md))
- [ ] Deploy **testnet** explorer first (VPS + HTTPS URL)
- [ ] Verify block hash, height, tx list, coinbase for known blocks
- [ ] Public HTTPS URL documented in PROJECT-STATUS
- [ ] Mainnet explorer only after testnet validation (or parallel if low risk)

---

## D. Node count goal (≥ 10 independent peers)

- [ ] Define “independent” (distinct operators / IPs, not same `/24` if possible)
- [ ] Publish `addnode` / peer instructions ([README join section](../README.md#join-the-network))
- [ ] Track peer count weekly (`getconnectioncount` / `getpeerinfo` aggregates)
- [ ] Reach **≥ 10** non-operator testnet nodes (ROADMAP exit criterion)
- [ ] Consider curated seed list or DNS seed policy doc ([dnsseed-policy.md](dnsseed-policy.md)) — post-review only

---

## E. Phase 1 exit gate (from ROADMAP)

- [ ] Testnet soak complete (30 days, no critical consensus bugs)
- [ ] Explorer accurate on testnet
- [ ] ≥ 10 independent testnet nodes
- [ ] BIP heights documented and merged
- [ ] PROJECT-STATUS updated; Phase 2 proposal in ROADMAP if mainnet public launch next
- [ ] **No exchange listing promises** in any Phase 1 materials

---

**Links:** [EXPLORER-PLAN.md](EXPLORER-PLAN.md) · [TESTNET-JOIN.md](TESTNET-JOIN.md) · [CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md) · [WHITEPAPER.md](WHITEPAPER.md) · [PROJECT-STATUS.md](PROJECT-STATUS.md) · [LEGAL-NOTICE.md](LEGAL-NOTICE.md)
