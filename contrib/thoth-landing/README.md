# Thoth project landing page (static)

Minimal single-page site for Phase 1 outreach. No RPC, no secrets, no exchange claims.
Matches the dark tone of [thoth-explorer](../thoth-explorer/).

**Legal:** [LEGAL-NOTICE.md](../../doc/LEGAL-NOTICE.md)

---

## Files

```
contrib/thoth-landing/
  index.html
  static/style.css
  README.md
```

---

## Local preview

```bash
cd contrib/thoth-landing
python3 -m http.server 8000
# open http://127.0.0.1:8000/
```

---

## VPS deploy (nginx on port 80)

Assumes Ubuntu VPS (e.g. `152.239.115.145`) already runs `thothd` and the testnet explorer on **:8080**.

### 1. Copy files

Option A — web root:

```bash
sudo mkdir -p /var/www/thoth
sudo cp -r index.html static /var/www/thoth/
sudo chown -R www-data:www-data /var/www/thoth
```

Option B — keep in repo checkout:

```bash
# e.g. /root/thoth/contrib/thoth-landing/
```

### 2. nginx server block

Create `/etc/nginx/sites-available/thoth-landing`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name 152.239.115.145;   # replace with your domain when ready

    root /var/www/thoth;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Enable and reload:

```bash
sudo ln -sf /etc/nginx/sites-available/thoth-landing /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

The **explorer** stays on port **8080** (separate systemd service). Do not merge explorer and landing on one port unless you add a reverse-proxy path (e.g. `/explorer/`).

### 3. Firewall

```bash
sudo ufw allow 80/tcp
sudo ufw status
```

Keep **19332 / 29332** (RPC) closed from the internet. P2P **19333 / 29335** only as needed.

### 4. Verify

- Landing: http://152.239.115.145/
- Explorer: http://152.239.115.145:8080/

Update [PROJECT-STATUS.md](../../doc/PROJECT-STATUS.md) when live.

### 5. Optional later

- Point a domain (A record) at the VPS.
- TLS: `certbot --nginx -d yourdomain.example`
- Redirect HTTP → HTTPS

---

## Phase 1 note

This satisfies optional Phase 0 “docs landing” / Phase 1 outreach. It does **not** imply exchange listing or token sale.
