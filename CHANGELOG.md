# Changelog

All notable changes to RYMonv3 are documented in this file.

## [3.1.0] - 2026-06-25

### Added

- IPSC repeater support for RYSEN `MODE: IPSC` systems (HBP-shaped `CONFIG_SND` peers).
- Motorola orange (`#ff6600`) callsign pills for IPSC peers on Main, Linked Systems, and Static TG pages (matches [RYSEN-MONITOR](https://github.com/ShaYmez/RYSEN-MONITOR) `ipsc` branch).
- `init_db()` startup path — creates SQLite tables before alias download and dashboard queries.
- `push_main()` — main dashboard renders even when `last_heard` is empty.
- Docker `gosu` privilege drop with bind-mount `chown` for `log/` and `data/`.
- `.gitattributes` for Unix line endings on `entrypoint`.
- `tests/test_ipsc_masters.py` smoke tests for IPSC peer metadata and routing masters.

### Fixed

- Docker `exec /entrypoint: no such file or directory` (CRLF shebang on Windows; build-time `sed` strip).
- Docker `PermissionError` on `/monitor/log/rymon.log` (root-owned bind mounts vs UID 54000 `radio`).
- Main dashboard not loading when `last_heard` table was empty (`if result:` skipped render).
- First `CONFIG_SND` did not push dashboard updates (`build_hblink_table` now calls `build_stats`).
- `UnboundLocalError` on `_lastheard_refresh` in `build_stats()` crashing the reactor.
- Missing SQLite tables on fresh container (`create_tables` never called).
- `update_table` failure when `table_count` returned `None`.
- `update_hblink_table` `KeyError` when new IPSC-N master systems appear after startup.
- `main_table.html` OPENBRIDGES Jinja nesting.
- `hbmon.js` undefined `masters_tbl` on disconnect; null-safe table element updates.

### Changed

- IPSC peers display as `GB7NR (Id: 235287)` using `RADIO_ID`, without redundant `(IPSC)` suffix.
- WebSocket subscribe logging moved from INFO to DEBUG.
- Main table CTABLE updates decoupled from lastheard DB poll interval.
