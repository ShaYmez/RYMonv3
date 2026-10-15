#!/usr/bin/env python3
"""Smoke tests: RYSEN YSFPEER linked peers and HYTERA routing masters."""
import shutil
import sys
import time
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if not (ROOT / "rymon.cfg").exists():
    shutil.copy(ROOT / "rymon_SAMPLE.cfg", ROOT / "rymon.cfg")

from dmr_utils3.utils import int_id  # noqa: E402
import monitor  # noqa: E402
from monitor import (  # noqa: E402
    build_hblink_table,
    is_linked_peer_mode,
    is_routing_master,
    update_hblink_table,
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


def test_ysfpeer_connected_none_does_not_crash():
    """RYSEN YSFPEER sets CONNECTION YES before CONNECTED has a timestamp."""
    config = {
        "YSF-SFG": {
            "ENABLED": True,
            "MODE": "YSFPEER",
            "LOCATION": "UK",
            "DESCRIPTION": "YSF 2359",
            "URL": "",
            "CALLSIGN": "MB6HA",
            "RADIO_ID": "235593305",
            "MASTER_IP": "127.0.0.1",
            "MASTER_PORT": 42010,
            "STATS": {
                "CONNECTION": "YES",
                "CONNECTED": None,
                "PINGS_SENT": 4,
                "PINGS_ACKD": 0,
            },
        }
    }
    ctable = {"MASTERS": {}, "PEERS": {}, "OPENBRIDGES": {}}
    build_hblink_table(config, ctable)
    peer = ctable["PEERS"]["YSF-SFG"]
    assert peer["STATS"]["CONNECTION"] == "YES"
    assert peer["STATS"]["CONNECTED"] == "--   --"
    assert peer["STATS"]["PINGS_SENT"] == 4
    assert peer["STATS"]["PINGS_ACKD"] is None


def test_rysen_ysf_report_shows_room_and_polls():
    """Live RYSEN sends bytes, a description, a login stamp, and PINGS_ACKD 0."""
    saved = monitor.CONF["GLOBAL"].get("HB_INC")
    monitor.CONF["GLOBAL"]["HB_INC"] = False
    try:
        config = {
            "YSF-2350": {
                "ENABLED": True,
                "MODE": "YSFPEER",
                "CALLSIGN": b"MX0SXC    ",
                "RADIO_ID": (2356427).to_bytes(4, "big"),
                "DESCRIPTION": "GB YSF 2350",
                "DGID": 9,
                "MASTER_IP": "77.68.1.2",
                "MASTER_PORT": 42000,
                "STATS": {
                    "CONNECTION": "YES",
                    "CONNECTED": time.time() - 90,
                    "PINGS_SENT": 6,
                    "PINGS_ACKD": 0,
                },
            },
            "TGIF-1": {
                "ENABLED": True,
                "MODE": "PEER",
                "CALLSIGN": b"TGIF1",
                "RADIO_ID": (1).to_bytes(4, "big"),
                "MASTER_IP": "127.0.0.1",
                "MASTER_PORT": 62031,
                "STATS": {"CONNECTION": "NO", "CONNECTED": None, "PINGS_SENT": 0, "PINGS_ACKD": 0},
            },
        }
        ctable = {"MASTERS": {}, "PEERS": {}, "OPENBRIDGES": {}}
        build_hblink_table(config, ctable)
        assert "YSF-2350" in ctable["PEERS"]
        assert "TGIF-1" not in ctable["PEERS"]
        peer = ctable["PEERS"]["YSF-2350"]
        assert peer["CALLSIGN"] == "MX0SXC"
        assert peer["RADIO_ID"] == "2356427"
        assert peer["LOCATION"] == "GB YSF 2350 · DGID 9"
        assert peer["STATS"]["PINGS_ACKD"] is None
        assert "m" in peer["STATS"]["CONNECTED"]

        config["YSF-2350"]["STATS"]["PINGS_SENT"] = 7
        update_hblink_table(config, ctable)
        assert peer["STATS"]["PINGS_SENT"] == 7
        assert peer["STATS"]["PINGS_ACKD"] is None

        env = Environment(loader=FileSystemLoader(str(ROOT / "templates")))
        html = env.get_template("lnksys_table.html").render(_table=ctable, emaster=False)
        assert ">YSF<" in html
        assert "7 polls" in html
        assert "GB YSF 2350 · DGID 9" in html
        assert "YSFPEER" not in html
    finally:
        monitor.CONF["GLOBAL"]["HB_INC"] = saved


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
    test_ysfpeer_connected_none_does_not_crash()
    test_rysen_ysf_report_shows_room_and_polls()
    test_hytera_system_in_masters()
    print("OK: RYSEN modes test passed")
