#!/usr/bin/env bash
# Build Thoth wallet tools on Arch/CachyOS with Berkeley DB 4.8 (required for working wallets).
# For node/RPC-only builds using system BDB 6.2, use --with-incompatible-bdb instead; see doc/build-unix.md.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export BDB_PREFIX="${BDB_PREFIX:-${ROOT}/db4}"

cd "${ROOT}"
./contrib/install_db4.sh "${ROOT}"

./autogen.sh
./configure --with-gui \
  BDB_LIBS="-L${BDB_PREFIX}/lib -ldb_cxx-4.8 -ldb-4.8" \
  BDB_CFLAGS="-I${BDB_PREFIX}/include" \
  CPPFLAGS="-I${BDB_PREFIX}/include" \
  LDFLAGS="-L${BDB_PREFIX}/lib"

make -j"$(nproc)" -C src thothd thoth-cli thoth-wallet

echo
echo "Wallet build complete. Verify:"
echo "  ./src/thoth-wallet -wallet=test create"
echo "  ./src/thothd -daemon -wallet=test"
echo "  ./src/thoth-cli -rpcwallet=test getnewaddress"
