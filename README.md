**RYMonv3 is a "dashboard" for RYSEN MASTER+ & HBlink3 servers by M0VUB.**

**Version 3.1.0**

***This version has been forked from FDMR-Monitor by OA4DOA 2022***
***This version is also credited to HBMonV2 by SP2ONG 2019 - 2022***

Some of the changes in RYMonv3:
- Upgraded HTML
- Better system info
- Options Generator
- RYSEN Optimisation
- TG Count page added.
- Config file added.
- It's integrated with SQLite database.
- Improved usage of memory and CPU.
- Broadcasting groups has been added to save server's resources.
- JavaScript code was added to support broadcasting groups.
- The code has been updated to HTML5.
- Static and single TG's page added.
- Data QSO's now are showed in the dashboard.
- IPSC repeater peers (`MODE: IPSC`) appear on Linked Systems when RYSEN reports them.

RYMonv2 has been tested on Debian 11, 12 & 13

This version of RYMonv2 requires a web server like apache2, lighttpd and
php 7.x running on the server. The Python backend serves WebSocket updates on port **9000**; the PHP pages under `html/` connect to that socket for live data.

*** Installation is provided in the RYSEN DMR Master+ one-shot installer***

## Stand-alone install (Debian/Ubuntu)

Uses a project virtualenv (PEP 668 safe — no system `pip install`).

```bash
git clone https://github.com/ShaYmez/RYMonv3.git
cd RYMonv3
./install.sh
nano rymon.cfg    # [FDMR CONNECTION] FDMR_IP / FDMR_PORT → RYSEN report (default 4321)
./run.sh
```

`install.sh` installs OS packages (`python3-venv`, `python3-dev`, `libffi-dev`, `libssl-dev`, `build-essential`), creates `.venv`, installs Python dependencies, and copies `rymon_SAMPLE.cfg` → `rymon.cfg` when missing.

## Docker

Build and run the WebSocket backend only (Apache + `html/` still required on the host for the browser UI):

```bash
cp rymon_SAMPLE.cfg rymon.cfg
# Edit FDMR_IP / FDMR_PORT — use the RYSEN container IP on the Docker network, not 127.0.0.1
docker compose build
docker compose up -d
```

Published image: `shaymez/rymonv3:latest`

For a RYSEN + RYMon example on a shared bridge (`172.16.238.0/24`), see `docker-compose.sample.yml`. Typical settings when RYSEN is at `172.16.238.10`:

```ini
[FDMR CONNECTION]
FDMR_IP = 172.16.238.10
FDMR_PORT = 4321
```

Volumes: `./rymon.cfg`, `./log`, and optional alias JSON under `./data/`.

The container process runs as UID/GID **54000** (`radio`). Bind-mounted `log/` (and `data/` if mounted) are owned by root on the host by default; the entrypoint fixes that at startup. Alternatively, on the host:

```bash
mkdir -p log
sudo chown -R 54000:54000 log
```

Or use a Docker named volume for logs (see commented `rymon_log` in `docker-compose.yml`) so no host `chown` is needed.

## systemd (optional)

```bash
sudo cp systemd/rymon.service /etc/systemd/system/
# Edit WorkingDirectory if not /opt/RYMonv3
sudo systemctl daemon-reload
sudo systemctl enable --now rymon
```

## IPSC support

When RYSEN sends IPSC repeater systems in `CONFIG['SYSTEMS']['IPSC-N']` with `MODE: IPSC` and HBP-shaped peer fields, RYMon treats them like routing masters. Peers show on **Linked Systems** (`lnksys`) as `GB7NR (Id: 235287)` with Motorola software/hardware from `SOFTWARE_ID` / `PACKAGE_ID`, **Motorola orange** (`#ff6600`) callsign styling, and live TS1/TS2 activity works via `CTABLE['MASTERS']`.

Run the smoke test:

```bash
python3 tests/test_ipsc_masters.py
```

---

**HBMonv2 by SP2ONG**

HBMonitor v2 for DMR Server based on HBMonv2 https://github.com/sp2ong/HBMonv2

---

**hbmonitor3 by KC1AWV**

Python 3 implementation of N0MJS HBmonitor for HBlink https://github.com/kc1awv/hbmonitor3

---

Copyright (C) 2013-2018  Cortney T. Buffington, N0MJS <n0mjs@me.com>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301  USA

---
