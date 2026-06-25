#!/usr/bin/env python3
"""Smoke test: IPSC routing systems populate CTABLE['MASTERS']."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if not (ROOT / "rymon.cfg").exists():
    shutil.copy(ROOT / "rymon_SAMPLE.cfg", ROOT / "rymon.cfg")

from monitor import build_hblink_table, is_routing_master  # noqa: E402


def _minimal_peer(callsign="GB7TEST", protocol=None):
    peer = {
        "TX_FREQ": "0000000",
        "RX_FREQ": "0000000",
        "SLOTS": "3",
        "PACKAGE_ID": "IPSC",
        "SOFTWARE_ID": "RYSEN",
        "LOCATION": "Test",
        "DESCRIPTION": "IPSC repeater",
        "URL": "",
        "CALLSIGN": callsign,
        "COLORCODE": "1",
        "CONNECTION": "YES",
        "CONNECTED": 0,
        "IP": "192.168.1.10",
        "PORT": 62030,
    }
    if protocol:
        peer["PROTOCOL"] = protocol
    return peer


def test_is_routing_master():
    assert is_routing_master("MASTER")
    assert is_routing_master("IPSC")
    assert not is_routing_master("PEER")


def test_ipsc_system_in_masters():
    config = {
        "IPSC-1": {
            "ENABLED": True,
            "MODE": "IPSC",
            "REPEAT": True,
            "PEERS": {
                b"\x00\x00\x00\x01": _minimal_peer(protocol="IPSC"),
            },
        }
    }
    ctable = {"MASTERS": {}, "PEERS": {}, "OPENBRIDGES": {}}
    build_hblink_table(config, ctable)
    assert "IPSC-1" in ctable["MASTERS"]
    assert len(ctable["MASTERS"]["IPSC-1"]["PEERS"]) == 1
    peer = next(iter(ctable["MASTERS"]["IPSC-1"]["PEERS"].values()))
    assert "(IPSC)" in peer["CALLSIGN"]


if __name__ == "__main__":
    test_is_routing_master()
    test_ipsc_system_in_masters()
    print("OK: IPSC masters test passed")
