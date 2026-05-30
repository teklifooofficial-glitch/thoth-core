Thoth Core integration/staging tree
=====================================

[![Build Status](https://travis-ci.org/thoth-project/thoth.svg?branch=master)](https://travis-ci.org/thoth-project/thoth)

https://thoth.org

What is Thoth?
----------------

Thoth is an experimental digital currency that enables instant payments to
anyone, anywhere in the world. Thoth uses peer-to-peer technology to operate
with no central authority: managing transactions and issuing money are carried
out collectively by the network. Thoth Core is the name of open source
software which enables the use of this currency.

For more information, as well as an immediately useable, binary version of
the Thoth Core software, see [https://thoth.org](https://thoth.org).

> **Project status:** Thoth is in **early development** (Phase 1). **TTH is not listed on any
> exchange.** See [ROADMAP.md](ROADMAP.md) and [doc/PROJECT-STATUS.md](doc/PROJECT-STATUS.md)
> for current network state and disclaimers.

Official links
--------------

| Resource | URL |
|----------|-----|
| **Website (landing)** | http://152.239.115.145/ *(deploy [contrib/thoth-landing](contrib/thoth-landing/) on VPS nginx :80)* |
| **GitHub** | https://github.com/teklifooofficial-glitch/thoth-core |
| **Testnet explorer** | http://152.239.115.145:8080/ |
| **Project status** | [doc/PROJECT-STATUS.md](doc/PROJECT-STATUS.md) |

Quick start
-----------

Thoth (TTH) is a Litecoin-derived full node: Scrypt proof-of-work, 2.5-minute
block target, and bech32 prefix `tth` on mainnet. Binaries: `thothd`, `thoth-cli`,
`thoth-qt`, `thoth-wallet`, `thoth-tx`.

**Build** (from repository root):

    ./autogen.sh
    ./configure --with-gui --with-incompatible-bdb
    make -j$(nproc)

On Arch/CachyOS, install deps with `pacman` and use `--with-incompatible-bdb` for the
system Berkeley DB; see [doc/build-unix.md](doc/build-unix.md#arch-linux--cachyos).

**Wallet on Arch:** linking against BDB 6.2 can segfault wallet creation. Either build
BDB 4.8 with `./contrib/install_db4.sh $(pwd)` and reconfigure with `BDB_LIBS` /
`BDB_CFLAGS`, or mine with `generatetoaddress` to any valid address (no loaded wallet).

**Regtest** (`~/.thoth/regtest/`):

    ./src/thothd -regtest -daemon
    ADDR=$(./src/thoth-cli -regtest getnewaddress)   # if wallet works
    ./src/thoth-cli -regtest generatetoaddress 2 "$ADDR" 1000000

**Mainnet isolated** (no peers; put `connect=0` and `dnsseed=0` under `[main]` in
`~/.thoth/thoth.conf`):

    ./src/thothd -daemon
    ./src/thoth-cli generatetoaddress 1 "<addr>" 1000000

**Testnet** — [doc/TESTNET-JOIN.md](doc/TESTNET-JOIN.md) (`~/.thoth/testnet4/`, `[test]` config):

    ./src/thothd -testnet -daemon
    ./src/thoth-cli -testnet generatetoaddress 1 "<legacy-addr>" 5000000   # before block 144

Genesis block hashes: mainnet
`3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784`; testnet
`439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651`; regtest
`b6ae6fa79bdde8d750bc8dff1e1a0f053dc45422a11f100d57623143fc0e1381`.

| Network  | RPC port | P2P port | Data directory        |
|----------|----------|----------|------------------------|
| Mainnet  | 19332    | 19333    | `~/.thoth/`            |
| Testnet  | 29332    | 29335    | `~/.thoth/testnet4/`   |
| Regtest  | 19443    | 19444    | `~/.thoth/regtest/`    |

Join the network
----------------

Thoth **mainnet** is a Litecoin-derived chain: **Scrypt** proof-of-work, **2.5-minute**
blocks, ticker **TTH**, bech32 prefix `tth`. Run a full node to relay blocks and
transactions on P2P port **19333** (RPC **19332** — bind to localhost only; never
expose RPC to the internet).

**Public peer (seed):**

    addnode=152.239.115.145:19333

Sample `~/.thoth/thoth.conf` `[main]` block:

    [main]
    listen=1
    connect=0
    dnsseed=0
    fixedseeds=0
    addnode=152.239.115.145:19333

**Build:** Linux/Arch details in [doc/build-unix.md](doc/build-unix.md). On Ubuntu VPS:
install build deps (`libdb-dev`, `libdb++-dev`, `libfmt-dev`, Boost, libevent, etc.),
then `./configure --without-gui --with-incompatible-bdb` and `make -j$(nproc)`.
Open P2P only: `ufw allow 19333/tcp` (not 19332).

**Start and verify:**

    ./src/thothd -daemon
    ./src/thoth-cli getconnectioncount
    ./src/thoth-cli getblockchaininfo

**Chain tip (informational, early network):** see [doc/PROJECT-STATUS.md](doc/PROJECT-STATUS.md); genesis
`3f2dc0f6de03c28bef702416f12688fef4157f92215312ace07a5946a1eb8784`.

Join testnet
-------------

Thoth **testnet** uses datadir `~/.thoth/testnet4/`, consensus **v2** (same rules as mainnet),
P2P **29335**, RPC **29332** (localhost only). Full guide: [doc/TESTNET-JOIN.md](doc/TESTNET-JOIN.md).

**Public testnet peer (seed):**

    addnode=152.239.115.145:29335

Sample `~/.thoth/thoth.conf` `[test]` block:

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

**Start and verify:**

    ./src/thothd -testnet -daemon
    ./src/thoth-cli -testnet getconnectioncount
    ./src/thoth-cli -testnet getblockchaininfo

**Testnet block explorer:** http://152.239.115.145:8080/ ([contrib/thoth-explorer](contrib/thoth-explorer/))

License
-------

Thoth Core is released under the terms of the MIT license. See [COPYING](COPYING) for more
information or see https://opensource.org/licenses/MIT.

Development Process
-------------------

The `master` branch is regularly built (see `doc/build-*.md` for instructions) and tested, but it is not guaranteed to be
completely stable. [Tags](https://github.com/thoth-project/thoth/tags) are created
regularly from release branches to indicate new official, stable release versions of Thoth Core.

The https://github.com/thoth-project/gui repository is used exclusively for the
development of the GUI. Its master branch is identical in all monotree
repositories. Release branches and tags do not exist, so please do not fork
that repository unless it is for development reasons.

The contribution workflow is described in [CONTRIBUTING.md](CONTRIBUTING.md)
and useful hints for developers can be found in [doc/developer-notes.md](doc/developer-notes.md).

The developer [mailing list](https://groups.google.com/forum/#!forum/thoth-dev)
should be used to discuss complicated or controversial changes before working
on a patch set.

Developer IRC can be found on Freenode at #thoth-dev.

Testing
-------

Testing and code review is the bottleneck for development; we get more pull
requests than we can review and test on short notice. Please be patient and help out by testing
other people's pull requests, and remember this is a security-critical project where any mistake might cost people
lots of money.

### Automated Testing

Developers are strongly encouraged to write [unit tests](src/test/README.md) for new code, and to
submit new unit tests for old code. Unit tests can be compiled and run
(assuming they weren't disabled in configure) with: `make check`. Further details on running
and extending unit tests can be found in [/src/test/README.md](/src/test/README.md).

There are also [regression and integration tests](/test), written
in Python, that are run automatically on the build server.
These tests can be run (if the [test dependencies](/test) are installed) with: `test/functional/test_runner.py`

The Travis CI system makes sure that every pull request is built for Windows, Linux, and macOS, and that unit/sanity tests are run automatically.

### Manual Quality Assurance (QA) Testing

Changes should be tested by somebody other than the developer who wrote the
code. This is especially important for large or high-risk changes. It is useful
to add a test plan to the pull request description if testing the changes is
not straightforward.

Translations
------------

We only accept translation fixes that are submitted through [Bitcoin Core's Transifex page](https://explore.transifex.com/bitcoin/bitcoin/).
Translations are converted to Thoth periodically.

Translations are periodically pulled from Transifex and merged into the git repository. See the
[translation process](doc/translation_process.md) for details on how this works.

**Important**: We do not accept translation changes as GitHub pull requests because the next
pull from Transifex would automatically overwrite them again.
