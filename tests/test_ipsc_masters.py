#!/usr/bin/env python3
"""Smoke test: IPSC routing systems populate CTABLE['MASTERS']."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if not (ROOT / "rymon.cfg").exists():
    shutil.copy(ROOT / "rymon_SAMPLE.cfg", ROOT / "rymon.cfg")

import monitor  # noqa: E402
from dmr_utils3.utils import int_id  # noqa: E402
from monitor import (  # noqa: E402
    _hb_field_str,
    _hb_radio_id,
    _resolve_peer_callsign,
    add_hb_peer,
    build_hblink_table,
    is_routing_master,
)


def _ipsc_peer(
    callsign=b"GB7NR   ",
    radio_id="235287",
    peer_key=b"\x00\x00\x03\x97",
):
    return {
        "TX_FREQ": b"0000000",
        "RX_FREQ": b"0000000",
        "SLOTS": b"3",
        "PACKAGE_ID": b"Motorola IPSC Repeater" + b"\x00" * 19,
        "SOFTWARE_ID": b"Motorola IPSC 04.02.04.01 (voice, data)" + b"\x00" * 2,
        "LOCATION": b"",
        "DESCRIPTION": b"Digital TS1:IPSC TS2:IPSC",
        "URL": b"",
        "CALLSIGN": callsign,
        "RADIO_ID": radio_id,
        "PROTOCOL": "IPSC",
        "COLORCODE": b"1",
        "CONNECTION": "YES",
        "CONNECTED": 0,
        "IP": "192.168.1.10",
        "PORT": 62030,
    }


def test_is_routing_master():
    assert is_routing_master("MASTER")
    assert is_routing_master("IPSC")
    assert not is_routing_master("PEER")


def test_hb_field_str_strips_padded_bytes():
    assert _hb_field_str(b"GB7NR   ") == "GB7NR"
    assert _hb_field_str(b"Motorola IPSC Repeater\x00\x00") == "Motorola IPSC Repeater"


def test_ipsc_system_in_masters():
    peer_key = b"\x00\x00\x03\x97"
    config = {
        "IPSC-198": {
            "ENABLED": True,
            "MODE": "IPSC",
            "REPEAT": True,
            "PEERS": {
                peer_key: _ipsc_peer(),
            },
        }
    }
    ctable = {"MASTERS": {}, "PEERS": {}, "OPENBRIDGES": {}}
    build_hblink_table(config, ctable)
    assert "IPSC-198" in ctable["MASTERS"]
    assert len(ctable["MASTERS"]["IPSC-198"]["PEERS"]) == 1
    peer = ctable["MASTERS"]["IPSC-198"]["PEERS"][int_id(peer_key)]
    assert peer["CALLSIGN"] == "GB7NR"
    assert peer["RADIO_ID"] == "235287"
    assert "(IPSC)" not in peer["CALLSIGN"]
    assert peer["PROTOCOL"] == "IPSC"
    assert peer["SOFTWARE_ID"].startswith("Motorola IPSC 04.02.04.01")
    assert peer["PACKAGE_ID"] == "Motorola IPSC Repeater"
    assert peer["DESCRIPTION"] == "Digital TS1:IPSC TS2:IPSC"
    assert peer["LOCATION"] == "—"
    assert peer["TX_FREQ"] == "N/A"
    assert peer["RX_FREQ"] == "N/A"


def test_ipsc_callsign_fallback_to_peer_ids():
    monitor.peer_ids.clear()
    monitor.peer_ids[235287] = {"CALLSIGN": "GB7NR"}
    peer_conf = _ipsc_peer(callsign=b"235287", radio_id="235287")
    peer_key = b"\x00\x00\x03\x97"
    assert _resolve_peer_callsign(peer_conf, peer_key, "235287") == "GB7NR"


def test_ipsc_radio_id_from_peer_conf():
    peer_conf = _ipsc_peer()
    peer_key = b"\x00\x00\x03\x97"
    assert _hb_radio_id(peer_conf, peer_key) == "235287"


def test_add_hb_peer_stores_radio_id_for_master_peer():
    peer_conf = {
        "TX_FREQ": b"4345000",
        "RX_FREQ": b"4345000",
        "SLOTS": b"2",
        "PACKAGE_ID": b"MMDVM_HS_Hat",
        "SOFTWARE_ID": b"2024.02.05",
        "LOCATION": b"Test City",
        "DESCRIPTION": b"",
        "URL": b"",
        "CALLSIGN": b"TEST1   ",
        "RADIO_ID": "1234567",
        "COLORCODE": b"1",
        "CONNECTION": "YES",
        "CONNECTED": 0,
        "IP": "10.0.0.1",
        "PORT": 62030,
    }
    peers = {}
    add_hb_peer(peer_conf, peers, b"\x00\x12\xd6\x87")
    peer = peers[1234567]
    assert peer["CALLSIGN"] == "TEST1"
    assert peer["RADIO_ID"] == "1234567"


if __name__ == "__main__":
    test_is_routing_master()
    test_hb_field_str_strips_padded_bytes()
    test_ipsc_system_in_masters()
    test_ipsc_callsign_fallback_to_peer_ids()
    test_ipsc_radio_id_from_peer_conf()
    test_add_hb_peer_stores_radio_id_for_master_peer()
    print("OK: IPSC masters test passed")
