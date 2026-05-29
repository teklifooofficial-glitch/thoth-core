# Phase 1 preparation checklist

Per [ROADMAP.md](../ROADMAP.md#phase-1--public-testnet--infrastructure). **Checklist only** — no dates or exchange commitments. Update items as completed; link evidence in [DEVLOG.md](../DEVLOG.md).

**Prerequisite:** Phase 0 exit criteria met ([ROADMAP.md](../ROADMAP.md#phase-0--trust--transparency-current)).

---

## A. Consensus / BIP height review

- [ ] Inventory all deployment heights in `src/chainparams.cpp` (BIP16/34/65/66, BIP9, Segwit, Taproot, MWEB)
- [ ] Document intended activation strategy for a chain born **2024+** at height 0
- [ ] Decide: retain, reset, or disable MWEB for initial public testnet/mainnet
- [ ] Draft `chainparams` patch + release notes (no merge without roadmap update)
- [ ] Peer review by at least one non-author contributor
- [ ] Regtest/testnet re-sync tests after any height change

---

## B. Public testnet campaign

- [ ] Publish testnet join doc (ports, genesis hash, `[test]` config block)
- [ ] Run public testnet node(s) with stable uptime target
- [ ] Testnet mining guide (`generatetoaddress`, expected try counts)
- [ ] Optional: faucet script or documented donate-and-faucet process
- [ ] **Soak period:** continuous testnet ≥ **30 days** without consensus failures (ROADMAP exit criterion)
- [ ] Log incidents in DEVLOG / PROJECT-STATUS

---

## C. Block explorer (evaluate → deploy)

**Options to evaluate (no decision implied):**

| Option | Pros | Cons |
|--------|------|------|
| Fork/adapt **Esplora**-style indexer | Mature UX, API | Effort to port from Bitcoin/Litecoin |
| **Electrs** + custom front-end | Lightweight index | Scrypt/LTC lineage quirks, MWEB display |
| **Blockbook** (Trezor stack) | Exchange-friendly API | Heavier deploy, customization |
| Minimal **custom indexer** (RPC scan + SQLite) | Full control | Maintenance burden, feature-poor |

**Checklist:**

- [ ] Pick approach and record rationale in DEVLOG
- [ ] Deploy **testnet** explorer first
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

**Links:** [WHITEPAPER.md](WHITEPAPER.md) · [PROJECT-STATUS.md](PROJECT-STATUS.md) · [LEGAL-NOTICE.md](LEGAL-NOTICE.md)
