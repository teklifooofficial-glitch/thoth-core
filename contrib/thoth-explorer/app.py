#!/usr/bin/env python3
"""Minimal Thoth block explorer — JSON-RPC via Flask (Phase 1a)."""

from __future__ import annotations

import os
import sys
from typing import Any

import requests
from flask import Flask, jsonify, render_template, request

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

GITHUB_REPO = "https://github.com/teklifooofficial-glitch/thoth-core"
DOC_LINKS = {
    "roadmap": f"{GITHUB_REPO}/blob/main/ROADMAP.md",
    "testnet_join": f"{GITHUB_REPO}/blob/main/doc/TESTNET-JOIN.md",
    "legal": f"{GITHUB_REPO}/blob/main/doc/LEGAL-NOTICE.md",
    "explorer_readme": f"{GITHUB_REPO}/blob/main/contrib/thoth-explorer/README.md",
}

RECENT_BLOCKS = 20


class RpcError(Exception):
    def __init__(self, message: str, code: int | None = None):
        super().__init__(message)
        self.code = code


def rpc_url() -> str:
    url = os.environ.get("THOTH_RPC_URL", "http://127.0.0.1:29332/").rstrip("/") + "/"
    return url


def rpc_call(method: str, params: list[Any] | None = None) -> Any:
    params = params or []
    payload = {"jsonrpc": "1.0", "id": "thoth-explorer", "method": method, "params": params}
    auth = None
    user = os.environ.get("THOTH_RPC_USER", "")
    password = os.environ.get("THOTH_RPC_PASSWORD", "")
    if user:
        auth = (user, password)
    try:
        resp = requests.post(rpc_url(), json=payload, auth=auth, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        raise RpcError(f"RPC connection failed: {exc}") from exc
    if data.get("error"):
        err = data["error"]
        raise RpcError(err.get("message", "RPC error"), err.get("code"))
    return data.get("result")


def network_label() -> str:
    return os.environ.get("NETWORK_LABEL", "Thoth Testnet")


def chain_id() -> str:
    return os.environ.get("CHAIN", "test")


def context_extra() -> dict[str, Any]:
    return {
        "network_label": network_label(),
        "chain": chain_id(),
        "doc_links": DOC_LINKS,
        "github_repo": GITHUB_REPO,
    }


def fetch_chain_status() -> dict[str, Any]:
    info = rpc_call("getblockchaininfo")
    return {
        "chain": info.get("chain", chain_id()),
        "blocks": int(info.get("blocks", 0)),
        "bestblockhash": info.get("bestblockhash", ""),
        "difficulty": info.get("difficulty"),
        "mediantime": info.get("mediantime"),
    }


def fetch_block_by_hash(block_hash: str) -> dict[str, Any]:
    block = rpc_call("getblock", [block_hash, 2])
    if not isinstance(block, dict):
        raise RpcError("Invalid block response")
    return block


def fetch_block_by_height(height: int) -> dict[str, Any]:
    if height < 0:
        raise RpcError("Block height must be non-negative")
    block_hash = rpc_call("getblockhash", [height])
    return fetch_block_by_hash(block_hash)


def fetch_tx(txid: str) -> dict[str, Any]:
    tx = rpc_call("getrawtransaction", [txid, True])
    if not isinstance(tx, dict):
        raise RpcError("Invalid transaction response")
    return tx


def render_rpc_error(template: str = "error.html", status: int = 503):
    exc = sys.exc_info()[1]
    message = str(exc) if isinstance(exc, RpcError) else "Unexpected error"
    return (
        render_template(template, error_message=message, **context_extra()),
        status,
    )


@app.route("/")
def index():
    try:
        status = fetch_chain_status()
        height = status["blocks"]
        recent: list[dict[str, Any]] = []
        if height >= 0:
            start = max(0, height - RECENT_BLOCKS + 1)
            for h in range(height, start - 1, -1):
                try:
                    block = fetch_block_by_height(h)
                    recent.append(
                        {
                            "height": h,
                            "hash": block.get("hash", ""),
                            "time": block.get("time"),
                            "tx_count": len(block.get("tx", [])),
                        }
                    )
                except RpcError:
                    recent.append({"height": h, "hash": "", "time": None, "tx_count": 0})
        return render_template(
            "index.html",
            status=status,
            recent_blocks=recent,
            **context_extra(),
        )
    except RpcError:
        return render_rpc_error()


@app.route("/block/<int:height>")
def block_by_height(height: int):
    try:
        block = fetch_block_by_height(height)
        return render_template("block.html", block=block, **context_extra())
    except RpcError:
        return render_rpc_error(status=404 if height < 0 else 503)


@app.route("/block/hash/<hash>")
def block_by_hash(hash: str):
    try:
        block = fetch_block_by_hash(hash.strip())
        return render_template("block.html", block=block, **context_extra())
    except RpcError:
        return render_rpc_error(status=404)


@app.route("/tx/<txid>")
def tx_detail(txid: str):
    try:
        tx = fetch_tx(txid.strip())
        return render_template("tx.html", tx=tx, **context_extra())
    except RpcError:
        return render_rpc_error(status=404)


@app.route("/api/status")
def api_status():
    try:
        status = fetch_chain_status()
        return jsonify(
            {
                "chain": status["chain"],
                "blocks": status["blocks"],
                "bestblockhash": status["bestblockhash"],
                "network_label": network_label(),
            }
        )
    except RpcError as exc:
        return jsonify({"error": str(exc)}), 503


if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "8080"))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
