# Join Thoth testnet

Public guide for Thoth **testnet** (Phase 1). Not mainnet. No exchange listing or
investment claims — see [LEGAL-NOTICE.md](LEGAL-NOTICE.md).

**Related:** [PHASE1-PREP.md](PHASE1-PREP.md) §B · [CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md) ·
[release-notes-thoth.md](release-notes-thoth.md#consensus-v2-thoth-mainnet--testnet) ·
[README — mainnet](../README.md#join-the-network)

---

## 1. What is Thoth testnet?

Thoth testnet is a separate Scrypt proof-of-work network used to exercise consensus,
peering, and wallets before wider mainnet use. It shares **consensus v2** rules with
mainnet (near-genesis BIPs, Segwit at block 144, MWEB disabled) but has its **own
genesis** and ports.

| Item | Value |
|------|--------|
| Network flag | `-testnet` |
| Data directory | **`~/.thoth/testnet4/`** (testnet4 — not `testnet3`) |
| Ticker (informal) | TTH testnet coins (no market value) |
| Bech32 HRP | `ttth` (active from block **144** onward) |

Do **not** point a mainnet datadir at testnet or mix `[main]` and `[test]` settings in
one running instance without understanding section precedence.

---

## 2. Genesis

Verify after start:

```bash
./src/thoth-cli -testnet getblockhash 0
```

Expected:

`439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651`

---

## 3. Ports

| Service | Port | Notes |
|---------|------|--------|
| P2P | **29335** | Allow in firewall if running a public testnet peer |
| RPC | **29332** | **Localhost only** — bind `127.0.0.1`; never expose to the internet |

Message start (wire): `fd d2 c8 f1` (see `chainparams.cpp`).

---

## 4. Sample `~/.thoth/thoth.conf`

Use a **`[test]`** block for testnet-only settings. Keep RPC credentials in the
global section or per your deployment policy (not committed to git).

```ini
server=1
rpcbind=127.0.0.1
rpcallowip=127.0.0.1

[test]
testnet=1
listen=1
port=29335
rpcport=29332
connect=0
dnsseed=0
fixedseeds=0
# addnode=<host>:29335
```

Add `addnode=` lines when public testnet seeds are published.

---

## 5. Build and run

From the repository root ([build-unix.md](build-unix.md)):

```bash
./autogen.sh
./configure --without-gui --with-incompatible-bdb
make -j$(nproc)
```

Start testnet:

```bash
./src/thothd -testnet -daemon
./src/thoth-cli -testnet getconnectioncount
./src/thoth-cli -testnet getblockchaininfo
```

Stop:

```bash
./src/thoth-cli -testnet stop
```

---

## 6. Mining (`generatetoaddress`)

Legacy **`gen=1`** is not supported. Mine with RPC:

```bash
./src/thoth-cli -testnet generatetoaddress <nblocks> "<address>" <maxtries>
```

### Before Segwit (blocks 1–143)

Segwit is not active yet. Use a **legacy** (base58 P2PKH) testnet address:

```bash
ADDR=$(./src/thoth-cli -testnet getnewaddress "" legacy)
./src/thoth-cli -testnet generatetoaddress 1 "$ADDR" 5000000
```

If wallet creation fails (e.g. BDB build without wallet), use any valid legacy testnet
address from an operator who can run `getnewaddress`.

### From block 144 onward

Segwit activates. Prefer **bech32** addresses with HRP **`ttth`** (e.g. `ttth1…`):

```bash
ADDR=$(./src/thoth-cli -testnet getnewaddress "" bech32)
./src/thoth-cli -testnet generatetoaddress 1 "$ADDR" 5000000
```

Testnet PoW can require **more tries** than mainnet; `5000000` is a reasonable starting
`maxtries`. Increase if the RPC returns without finding a block.

Check height and best hash:

```bash
./src/thoth-cli -testnet getblockchaininfo
```

---

## 7. Reset testnet datadir (consensus v2)

If you ran testnet before **consensus v2** (`0a45b1856`) or see reindex errors, wipe
testnet data and restart from genesis:

```bash
./src/thoth-cli -testnet stop
rm -rf ~/.thoth/testnet4/blocks ~/.thoth/testnet4/chainstate ~/.thoth/testnet4/indexes
./src/thothd -testnet -daemon
./src/thoth-cli -testnet getblockchaininfo
```

Genesis hash must still match §2. Pre-v2 testnet blocks are **not** valid on v2.

---

## 8. Consensus v2 (same rules as mainnet)

Testnet uses the same activation policy as mainnet ([CONSENSUS-AUDIT.md](CONSENSUS-AUDIT.md) §4.1):

| Rule | Testnet height |
|------|----------------|
| BIP34 | 1 |
| CSV | 2 |
| Segwit | 144 |
| Taproot (BIP8 window) | 8064 – 101376 |
| MWEB | **Disabled** |

Full migration notes: [release-notes-thoth.md](release-notes-thoth.md#consensus-v2-thoth-mainnet--testnet).

---

## 9. Legal

Thoth testnet coins have **no official value**. Running a node or mining is experimental.
This document is not investment advice and promises **no exchange listing**.
Read [LEGAL-NOTICE.md](LEGAL-NOTICE.md).

Report technical issues: [teklifooofficial-glitch/thoth-core](https://github.com/teklifooofficial-glitch/thoth-core/issues).
