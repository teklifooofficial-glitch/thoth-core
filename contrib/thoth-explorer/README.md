# Thoth minimal block explorer (Phase 1a)

Small **Flask** app that reads a local `thothd` node over JSON-RPC. Built for
**testnet** first ([TESTNET-JOIN.md](../../doc/TESTNET-JOIN.md)); mainnet uses the
same code with different RPC URL/ports.

**Not investment advice.** Testnet coins have no market value. See
[LEGAL-NOTICE.md](../../doc/LEGAL-NOTICE.md).

---

## Requirements

- Python 3.10+
- Running `thothd` with RPC enabled on **localhost**
- Testnet: `thothd -testnet -daemon`, RPC **29332** (default)

---

## Local run

```bash
cd contrib/thoth-explorer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config.example.env .env
# Edit .env: set THOTH_RPC_USER / THOTH_RPC_PASSWORD if configured in thoth.conf
python app.py
```

Open http://127.0.0.1:8080/

Optional: `pip install python-dotenv` to load `.env` automatically (otherwise export vars manually).

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `THOTH_RPC_URL` | `http://127.0.0.1:29332/` | JSON-RPC endpoint |
| `THOTH_RPC_USER` | *(empty)* | RPC user |
| `THOTH_RPC_PASSWORD` | *(empty)* | RPC password |
| `NETWORK_LABEL` | `Thoth Testnet` | UI label |
| `CHAIN` | `test` | Shown in API status |
| `FLASK_HOST` | `127.0.0.1` | Bind address |
| `FLASK_PORT` | `8080` | HTTP port |

---

## Routes

| Path | Description |
|------|-------------|
| `/` | Chain stats + recent blocks |
| `/block/<height>` | Block by height |
| `/block/hash/<hash>` | Block by hash |
| `/tx/<txid>` | Transaction detail |
| `/api/status` | JSON health: `{chain, blocks, bestblockhash}` |

---

## VPS deploy (outline)

1. Run **testnet** `thothd` on the VPS; RPC must listen on **`127.0.0.1:29332` only** (`rpcbind` in `[test]` — see TESTNET-JOIN.md).
2. Install this app under e.g. `/opt/thoth-explorer`; create `.env` with **local** RPC URL.
3. **systemd** unit (example):

```ini
[Unit]
Description=Thoth testnet explorer
After=network.target thothd.service

[Service]
Type=simple
User=thoth
WorkingDirectory=/opt/thoth-explorer
EnvironmentFile=/opt/thoth-explorer/.env
ExecStart=/opt/thoth-explorer/.venv/bin/python app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

4. **nginx** reverse proxy: public `443` → `127.0.0.1:8080`; TLS via Let's Encrypt.
5. **Firewall:** allow `443/tcp` (and testnet P2P `29335` on the node); **never** open `29332` or `19332` to the internet.

Verify genesis on testnet:

```bash
thoth-cli -testnet getblockhash 0
# 439581a39f5f59930cf3e349b9aca7c483586160df898fa87b10d278c2515651
```

Compare with the explorer home page and [EXPLORER-PLAN.md](../../doc/EXPLORER-PLAN.md) checklist.

---

## Security

- **Never** commit `.env` or RPC passwords.
- **Never** expose Thoth RPC ports publicly.
- Run the explorer as an unprivileged user; read-only RPC is sufficient (no wallet unlock).

---

## Phase 1 scope

Option **A** from [EXPLORER-PLAN.md](../../doc/EXPLORER-PLAN.md): height/hash/tx lookup only.
No address index. Blockbook (Phase 1b / Phase 3 prep) is deferred.
