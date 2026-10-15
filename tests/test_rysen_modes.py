#!/usr/bin/env python3
"""Smoke tests: RYSEN YSFPEER linked peers and HYTERA routing masters."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if not (ROOT / "rymon.cfg").exists():
    shutil.copy(ROOT / "rymon_SAMPLE.cfg", ROOT / "rymon.cfg")

from dmr_utils3.utils import int_id  # noqa: E402
from monitor import (  # noqa: E402
    build_hblink_table,
    is_linked_peer_mode,
    is_routing_master,
)
from tests.test_ipsc_masters import _ipsc_peer  # noqa: E402


def test_routing_and_linked_peer_modes():
    assert is_routing_master("HYTERA")
    assert is_linked_peer_mode("YSFPEER")
    assert not is_linked_peer_mode("MASTER")


def test_ysfpeer_in_peers_table():
    config = {
        "YSF-ROOM": {
            "ENABLED": True,
            "MODE": "YSFPEER",
            "LOCATION": "UK",
            "DESCRIPTION": "Example YSF room",
            "URL": "",
            "CALLSIGN": "MX0SXC",
            "RADIO_ID": "2356427",
            "MASTER_IP": "ysf.example.net",
            "MASTER_PORT": 42000,
            "STATS": {
                "CONNECTION": "YES",
                "CONNECTED": 0,
                "PINGS_SENT": 10,
                "PINGS_ACKD": 10,
            },
        }
    }
    ctable = {"MASTERS": {}, "PEERS": {}, "OPENBRIDGES": {}}
    build_hblink_table(config, ctable)
    assert "YSF-ROOM" in ctable["PEERS"]
    peer = ctable["PEERS"]["YSF-ROOM"]
    assert peer["MODE"] == "YSFPEER"
    assert peer["CALLSIGN"] == "MX0SXC"
    assert peer["STATS"]["CONNECTION"] == "YES"
    assert peer["SLOTS"] == "2"


def test_hytera_system_in_masters():
    peer_key = b"\x00\x00\x00\x01"
    config = {
        "HYTERA": {
            "ENABLED": True,
            "MODE": "HYTERA",
            "REPEAT": True,
            "PEERS": {
                peer_key: {
                    **_ipsc_peer(),
                    "PROTOCOL": "HYTERA",
                },
            },
        }
    }
    ctable = {"MASTERS": {}, "PEERS": {}, "OPENBRIDGES": {}}
    build_hblink_table(config, ctable)
    assert "HYTERA" in ctable["MASTERS"]
    peer = ctable["MASTERS"]["HYTERA"]["PEERS"][int_id(peer_key)]
    assert peer["PROTOCOL"] == "HYTERA"


if __name__ == "__main__":
    test_routing_and_linked_peer_modes()
    test_ysfpeer_in_peers_table()
    test_hytera_system_in_masters()
    print("OK: RYSEN modes test passed")
