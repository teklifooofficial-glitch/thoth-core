#!/usr/bin/env python3
# Copyright (c) 2026 The Thoth Core developers
# Distributed under the MIT software license.
"""
Mine Thoth (TTH) genesis blocks (Scrypt PoW).

Install dependency:
    pip install scrypt

Usage:
    python3 genesis_miner.py              # mine mainnet, testnet, regtest
    python3 genesis_miner.py --network regtest
    python3 genesis_miner.py --verify     # check tx/merkle serialization only
"""

from __future__ import annotations

import argparse
import hashlib
import struct
import sys
import time
from dataclasses import dataclass
from typing import Optional

try:
    import scrypt as scrypt_lib
except ImportError:
    scrypt_lib = None

# --- chainparams.cpp constants -------------------------------------------------

PSZ_TIMESTAMP = "Thoth blockchain - wisdom and knowledge for all - 2024"
GENESIS_REWARD = 50 * 100_000_000
N_VERSION = 1
GENESIS_PUBKEY_HEX = (
    "040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604"
    "fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9"
)
SCRIPT_SIG_PUSH_INT = 486604799  # same as Bitcoin/Litecoin genesis layout
POW_LIMIT_MAIN = int("00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16)
POW_LIMIT_REGTEST = int("7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16)

# Litecoin legacy genesis (for --verify serialization)
# UTF-8 right single quotation mark in U+2019 (matches chainparams.cpp)
LTC_TIMESTAMP = "NY Times 05/Oct/2011 Steve Jobs, Apple\u2019s Visionary, Dies at 56"
LTC_MERKLE = "97ddfbbae6be97fd6cdf3e7ca13232a3afff2353e29badfab7f73011edd4ced9"


@dataclass
class NetworkParams:
    name: str
    n_time: int
    n_bits: int
    pow_limit: int
    max_nonce: Optional[int] = None  # None = search until found
    progress_interval: int = 100_000


NETWORKS = {
    "mainnet": NetworkParams("mainnet", 1735000000, 0x1E0FFFF0, POW_LIMIT_MAIN, progress_interval=50_000),
    "testnet": NetworkParams("testnet", 1735000060, 0x1E0FFFF0, POW_LIMIT_MAIN, progress_interval=50_000),
    "regtest": NetworkParams("regtest", 1735000120, 0x207FFFFF, POW_LIMIT_REGTEST, progress_interval=10_000),
}


# --- script / transaction serialization ---------------------------------------

def _push_data(data: bytes) -> bytes:
    length = len(data)
    if length < 0x4C:
        return bytes([length]) + data
    if length <= 0xFF:
        return bytes([0x4C, length]) + data
    if length <= 0xFFFF:
        return bytes([0x4D]) + struct.pack("<H", length) + data
    return bytes([0x4E]) + struct.pack("<I", length) + data


def _scriptnum_serialize(value: int) -> bytes:
    if value == 0:
        return b""
    result = bytearray()
    neg = value < 0
    absvalue = (~(value) + 1) if neg else value
    while absvalue:
        result.append(absvalue & 0xFF)
        absvalue >>= 8
    if result[-1] & 0x80:
        result.append(0x80 if neg else 0)
    elif neg:
        result[-1] |= 0x80
    return bytes(result)


def _push_int64(value: int) -> bytes:
    if value == 0:
        return bytes([0x00])  # OP_0
    if 1 <= value <= 16:
        return bytes([value + 0x51 - 1])  # OP_1 .. OP_16
    return _push_data(_scriptnum_serialize(value))


def create_coinbase_script(psz_timestamp: str) -> bytes:
    """Match CScript() << 486604799 << CScriptNum(4) << timestamp bytes."""
    ts = psz_timestamp.encode("utf-8")
    script = _push_int64(SCRIPT_SIG_PUSH_INT)
    script += _push_data(_scriptnum_serialize(4))
    script += _push_data(ts)
    return script


def create_genesis_script_pubkey() -> bytes:
    pubkey = bytes.fromhex(GENESIS_PUBKEY_HEX)
    return bytes([len(pubkey)]) + pubkey + bytes([0xAC])  # OP_CHECKSIG


def ser_varint(i: int) -> bytes:
    if i < 0xFD:
        return struct.pack("<B", i)
    if i <= 0xFFFF:
        return struct.pack("<BH", 0xFD, i)
    if i <= 0xFFFFFFFF:
        return struct.pack("<BI", 0xFE, i)
    return struct.pack("<BQ", 0xFF, i)


def ser_uint32(i: int) -> bytes:
    return struct.pack("<I", i)


def ser_int32(i: int) -> bytes:
    return struct.pack("<i", i)


def ser_uint64(i: int) -> bytes:
    return struct.pack("<Q", i)


def ser_bytes(b: bytes) -> bytes:
    return ser_varint(len(b)) + b


def ser_string(s: bytes) -> bytes:
    return ser_bytes(s)


def serialize_tx_no_witness(
    version: int,
    script_sig: bytes,
    script_pubkey: bytes,
    value: int,
    lock_time: int = 0,
) -> bytes:
    """SERIALIZE_TRANSACTION_NO_WITNESS | SERIALIZE_NO_MWEB (genesis coinbase)."""
    tx = ser_int32(version)
    tx += ser_varint(1)  # vin
    tx += b"\x00" * 32  # prev hash
    tx += ser_uint32(0xFFFFFFFF)  # prev index
    tx += ser_bytes(script_sig)
    tx += ser_uint32(0xFFFFFFFF)  # sequence
    tx += ser_varint(1)  # vout
    tx += ser_uint64(value)
    tx += ser_bytes(script_pubkey)
    tx += ser_uint32(lock_time)
    return tx


def double_sha256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def hash256_hex(h: bytes) -> str:
    return h[::-1].hex()


def scrypt_pow_hash(header: bytes) -> bytes:
    if scrypt_lib is not None:
        return scrypt_lib.hash(header, header, N=1024, r=1, p=1, buflen=32)
    return hashlib.scrypt(header, salt=header, n=1024, r=1, p=1, dklen=32)


def compact_to_target(n_bits: int) -> int:
    """arith_uint256::SetCompact (positive targets only)."""
    n_size = n_bits >> 24
    n_word = n_bits & 0x007FFFFF
    if n_size <= 3:
        return n_word >> (8 * (3 - n_size))
    return n_word << (8 * (n_size - 3))


def check_proof_of_work(pow_hash: bytes, n_bits: int, pow_limit: int) -> bool:
    """CheckProofOfWork using Scrypt PoW hash (GetPoWHash)."""
    target = compact_to_target(n_bits)
    if target == 0 or target > pow_limit:
        return False
    return int.from_bytes(pow_hash, "little") <= target


def merkle_root(tx_hash: bytes) -> bytes:
    return tx_hash  # single-tx block


def serialize_block_header(
    n_version: int,
    merkle_root: bytes,
    n_time: int,
    n_bits: int,
    n_nonce: int,
) -> bytes:
    header = ser_int32(n_version)
    header += b"\x00" * 32
    header += merkle_root
    header += ser_uint32(n_time)
    header += ser_uint32(n_bits)
    header += ser_uint32(n_nonce)
    assert len(header) == 80
    return header


def mine_network(params: NetworkParams) -> dict:
    script_sig = create_coinbase_script(PSZ_TIMESTAMP)
    script_pubkey = create_genesis_script_pubkey()
    tx_raw = serialize_tx_no_witness(N_VERSION, script_sig, script_pubkey, GENESIS_REWARD)
    tx_hash = double_sha256(tx_raw)
    root = merkle_root(tx_hash)

    target = compact_to_target(params.n_bits)
    print(f"\n=== {params.name} ===")
    print(f"nTime:        {params.n_time}")
    print(f"nBits:        0x{params.n_bits:08x}")
    print(f"Target:       0x{target:064x}")
    print(f"hashMerkleRoot: {hash256_hex(root)}")
    print("Mining (Scrypt PoW, checking GetPoWHash)...")

    start = time.time()
    nonce = 0
    max_nonce = params.max_nonce if params.max_nonce is not None else 0xFFFFFFFF

    while nonce <= max_nonce:
        header = serialize_block_header(N_VERSION, root, params.n_time, params.n_bits, nonce)
        pow_hash = scrypt_pow_hash(header)
        if check_proof_of_work(pow_hash, params.n_bits, params.pow_limit):
            block_hash = double_sha256(header)
            elapsed = time.time() - start
            print(f"Found in {elapsed:.2f}s at nNonce={nonce}")
            return {
                "network": params.name,
                "nTime": params.n_time,
                "nBits": params.n_bits,
                "nNonce": nonce,
                "hashGenesisBlock": hash256_hex(block_hash),
                "hashMerkleRoot": hash256_hex(root),
                "powHash": hash256_hex(pow_hash),
            }
        if params.progress_interval and nonce > 0 and nonce % params.progress_interval == 0:
            rate = nonce / (time.time() - start)
            print(f"  nNonce={nonce} ({rate:.0f} H/s)...", flush=True)
        nonce += 1

    raise RuntimeError(f"{params.name}: no solution found up to nNonce={max_nonce}")


def verify_serialization() -> None:
    """Ensure coinbase serialization matches legacy Litecoin genesis merkle root."""
    script_sig = create_coinbase_script(LTC_TIMESTAMP)
    script_pubkey = create_genesis_script_pubkey()
    tx_raw = serialize_tx_no_witness(N_VERSION, script_sig, script_pubkey, GENESIS_REWARD)
    tx_hash = double_sha256(tx_raw)
    got = hash256_hex(merkle_root(tx_hash))
    print("Serialization self-test (legacy Litecoin genesis timestamp):")
    print(f"  expected merkle: {LTC_MERKLE}")
    print(f"  computed merkle: {got}")
    if got != LTC_MERKLE:
        raise SystemExit("FAIL: transaction serialization does not match Litecoin genesis")
    print("  OK")


def print_chainparams_snippet(result: dict) -> None:
    net = result["network"]
    print(f"\n--- Paste into chainparams.cpp ({net}) ---")
    print(
        f"        genesis = CreateGenesisBlock(pszThothGenesisTimestamp, "
        f"{result['nTime']}, {result['nNonce']}, 0x{result['nBits']:08x}, 1, 50 * COIN);"
    )
    print("        consensus.hashGenesisBlock = genesis.GetHash();")
    print(f'        assert(consensus.hashGenesisBlock == uint256S("0x{result["hashGenesisBlock"]}"));')
    print(f'        assert(genesis.hashMerkleRoot == uint256S("0x{result["hashMerkleRoot"]}"));')


def main() -> int:
    parser = argparse.ArgumentParser(description="Mine Thoth genesis blocks (Scrypt).")
    parser.add_argument(
        "--network",
        choices=["mainnet", "testnet", "regtest", "all"],
        default="all",
        help="Network to mine (default: all)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Only verify coinbase serialization against Litecoin genesis merkle",
    )
    args = parser.parse_args()

    if scrypt_lib is None:
        print("Note: 'scrypt' package not found; using hashlib.scrypt (stdlib).", file=sys.stderr)
        print("For best compatibility: pip install scrypt\n", file=sys.stderr)

    verify_serialization()
    if args.verify:
        return 0

    names = list(NETWORKS.keys()) if args.network == "all" else [args.network]
    results = []
    for name in names:
        results.append(mine_network(NETWORKS[name]))

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    for r in results:
        print(f"\n[{r['network']}]")
        print(f"  nNonce:           {r['nNonce']}")
        print(f"  hashGenesisBlock: {r['hashGenesisBlock']}")
        print(f"  hashMerkleRoot:   {r['hashMerkleRoot']}")
        print(f"  powHash:          {r['powHash']}")
        print_chainparams_snippet(r)

    return 0


if __name__ == "__main__":
    sys.exit(main())
