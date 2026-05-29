# Thoth (TTH) — whitepaper outline

Skeleton for a future whitepaper. Each section below is a **title plus one paragraph** of scope—not final copy. Expand in Phase 0–1 before public testnet campaign.

---

## 1. Abstract

Thoth (TTH) is an open-source Layer-1 blockchain derived from Litecoin Core, using Scrypt proof-of-work and a 84 million coin supply cap. This document will summarize purpose, architecture, tokenomics, and roadmap in non-promotional language suitable for developers and node operators.

## 2. Problem statement

Describe limitations or gaps in existing payment or store-of-value networks that motivate an independent chain (e.g. desire for a transparent, community-governed Scrypt L1 with documented parameters). Avoid implying guaranteed financial benefit.

## 3. Solution overview

Present Thoth as a full-node network with predictable monetary policy, fast block times (2.5 minutes), and bech32-native addresses (`tth`). Emphasize operator-run infrastructure rather than centralized issuance.

## 4. Technology stack

Cover fork lineage (Litecoin Core 0.21), C++ node software, P2P protocol, wallet modules, and build targets (`thothd`, `thoth-cli`, `thoth-qt`, `thoth-wallet`). Reference this repository as the canonical implementation.

## 5. Consensus and proof-of-work

Explain Scrypt PoW, difficulty adjustment, block validation, and chain selection (longest cumulative work). Include genesis parameters, block time, and halving interval (840,000 blocks).

## 6. Network parameters

Document mainnet/testnet/regtest ports, datadirs, genesis hashes, and seed/bootstrap policy. State that early mainnet may rely on manual `addnode` and small operator sets.

## 7. Tokenomics

Fixed **84M TTH** maximum supply; initial subsidy 50 TTH per block with halvings; no premine or ICO described in current codebase. Clarify that coinbase maturity and fee markets follow Bitcoin/Litecoin-style rules unless changed by consensus.

## 8. Governance and roadmap

Point to [ROADMAP.md](../ROADMAP.md) phases 0–5. Describe how scope changes require roadmap updates and public status snapshots ([PROJECT-STATUS.md](PROJECT-STATUS.md)).

## 9. Security model

Threat model for node operators (RPC exposure, wallet encryption, peer diversity). Note audit status: community review and testnet soak—not a formal third-party audit unless commissioned later.

## 10. Wallet and key management

BDB 4.8 vs system BDB trade-offs, descriptor/segwit support as inherited from upstream, backup practices. No custodial promises.

## 11. Mining and participation

`generatetoaddress`, hardware expectations for Scrypt, solo vs pool (pools TBD). Environmental and centralization considerations stated factually.

## 12. Team and contributors

Identify maintainers and contribution process ([CONTRIBUTING.md](../CONTRIBUTING.md)). Pseudonymous or org accounts allowed; no implied fiduciary duty to token holders.

## 13. Legal and regulatory disclaimer

Summarize [LEGAL-NOTICE.md](LEGAL-NOTICE.md): not investment advice, not a security offering, jurisdiction-specific compliance is the reader’s responsibility.

## 14. Risks

Network infancy, small peer count, consensus-parameter review pending, software bugs, exchange non-listing, volatility, regulatory change. No mitigation guarantees.

## 15. References and appendix

Links to repo, genesis miner script, BIPs inherited from upstream, glossary, and revision history.

---

**Status:** Expanded in [WHITEPAPER.md](WHITEPAPER.md) (draft v0.1). This file remains the section skeleton.
