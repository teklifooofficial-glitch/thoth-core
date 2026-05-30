# Run a Thoth testnet full node

Step-by-step guide for **developers and hobbyists** who want to run a Thoth **testnet**
full node and relay blocks. This is technical participation only — not an investment
product.

**Not for investors.** Testnet TTH has **no market value**. No exchange listing or profit
is promised. See [LEGAL-NOTICE.md](LEGAL-NOTICE.md).

**Related:** [TESTNET-JOIN.md](TESTNET-JOIN.md) (reference) · [build-unix.md](build-unix.md) ·
[PHASE1-PREP.md](PHASE1-PREP.md) §D (≥10 independent nodes goal)

---

## 1. Audience and goal

You will:

- Build `thothd` and `thoth-cli` from source
- Configure **`[test]`** in `~/.thoth/thoth.conf` (no global `rpcbind` that leaks to mainnet)
- Peer with the public seed and optionally accept inbound connections (`listen=1`)
- Verify chain sync with RPC

You do **not** need a wallet unless you want to try optional mining below.

---

## 2. Prerequisites

| Item | Notes |
|------|--------|
| **OS** | Linux (Ubuntu 22.04, Arch/CachyOS, etc.) |
| **Build tools** | Compiler, autotools, Boost, libevent, OpenSSL — see [build-unix.md](build-unix.md) |
| **Disk / RAM** | Small for early testnet; allow a few GB for blocks |
| **Network** | Outbound internet; open **29335/tcp** only if you want to be a public peer |
| **Git** | Clone [teklifooofficial-glitch/thoth-core](https://github.com/teklifooofficial-glitch/thoth-core) |

Ubuntu example deps (adjust for your distro):

```bash
sudo apt install -y build-essential git libtool autotools-dev automake pkg-config \
  libssl-dev libevent-dev libboost-all-dev libdb-dev libdb++-dev libfmt-dev
```

---

## 3. Quick path (build → config → run → verify)

### 3.1 Clone and build

```bash
git clone https://github.com/teklifooofficial-glitch/thoth-core.git
cd thoth-core
./autogen.sh
./configure --without-gui --with-incompatible-bdb
make -j$(nproc)
```

Binaries: `./src/thothd`, `./src/thoth-cli`.

For wallet support on Arch, see [build-unix.md](build-unix.md#arch-linux--cachyos) (BDB 4.8). A **node-only** build is enough to relay blocks.

### 3.2 Configure `~/.thoth/thoth.conf`

Create the data directory config. Use a **`[test]`** block for all testnet ports and RPC bind.
Put **`rpcbind` / `rpcallowip` inside `[test]` only** — do not set a top-level `rpcbind=0.0.0.0`.

**Public seed:**

    addnode=152.239.115.145:29335

```ini
server=1
# Optional: rpcuser=... and rpcpassword=... here (never commit real passwords)

[test]
testnet=1
listen=1
port=29335
rpcport=29332
rpcbind=127.0.0.1
rpcallowip=127.0.0.1
connect=0
dnsseed=0
fixedseeds=0
addnode=152.239.115.145:29335
```

If you previously ran testnet before **consensus v2**, reset first — see [TESTNET-JOIN.md](TESTNET-JOIN.md) §7.

### 3.3 Start the node

From the repo root (or with `thothd` on your `PATH`):

```bash
./src/thothd -testnet -daemon
```

Wait a few seconds for peer connection.

### 3.4 Verify

```bash
./src/thoth-cli -testnet getblockchaininfo
./src/thoth-cli -testnet getconnectioncount
./src/thoth-cli -testnet getblockhash 0
```

**Expected genesis hash:**

`439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651`

Check that `chain` is `test` and `blocks` increases when the network mines. Compare the tip with the [testnet explorer](http://152.239.115.145:8080/).

Stop the node:

```bash
./src/thoth-cli -testnet stop
```

### 3.5 Public peer (optional)

If you want others to connect to you, allow P2P on your firewall:

```bash
sudo ufw allow 29335/tcp
```

**Never** expose **29332** (RPC) to the internet.

---

## 4. Optional mining

Legacy **`gen=1`** is not supported. Use **`generatetoaddress`**.

**Before block 144** (Segwit not active), use a **legacy** testnet address:

```bash
ADDR=$(./src/thoth-cli -testnet getnewaddress "" legacy)
./src/thoth-cli -testnet generatetoaddress 1 "$ADDR" 5000000
```

**From block 144 onward**, use bech32 (`ttth`):

```bash
ADDR=$(./src/thoth-cli -testnet getnewaddress "" bech32)
./src/thoth-cli -testnet generatetoaddress 1 "$ADDR" 5000000
```

- **`maxtries`:** `5000000` is a reasonable start on testnet; increase if no block is found.
- Without a working wallet build, use any valid legacy address from another operator.
- Mined testnet coins are for **testing only** — not sellable, not listed on exchanges.

---

## 5. Useful links

| Resource | URL |
|----------|-----|
| Project landing | http://152.239.115.145/ |
| Testnet block explorer | http://152.239.115.145:8080/ |
| GitHub | https://github.com/teklifooofficial-glitch/thoth-core |
| Join testnet (detail) | [TESTNET-JOIN.md](TESTNET-JOIN.md) |
| Legal notice | [LEGAL-NOTICE.md](LEGAL-NOTICE.md) |
| Roadmap | [ROADMAP.md](../ROADMAP.md) |

Report bugs: [GitHub issues](https://github.com/teklifooofficial-glitch/thoth-core/issues).

---

## 6. Help the network (Phase 1)

Thoth Phase 1 aims for **≥10 independent testnet nodes** ([PHASE1-PREP.md](PHASE1-PREP.md) §D).
If you run a stable node for a week or more, consider noting your public IP (with `listen=1`
and port 29335 open) in a GitHub issue or community channel when available — operators only,
no financial incentive implied.
