#!/usr/bin/env python3
"""Tests for SERVER_INFO_SND handling in monitor.py."""
import json
import unittest
from unittest.mock import patch

import monitor


class TestServerInfoOpcode(unittest.TestCase):

    def test_opcode_defined(self):
        self.assertEqual(monitor.OPCODE["SERVER_INFO_SND"], "\x08")

    @patch("monitor.logger")
    def test_process_message_handles_server_info(self, mock_logger):
        payload = json.dumps({"rysen_version": "1.5.3", "hostname": "test"}).encode("utf-8")
        message = b"\x08" + payload
        monitor.process_message(message)
        mock_logger.debug.assert_any_call("got SERVER_INFO_SND opcode")
        mock_logger.debug.assert_any_call("RYSEN version from server: %s", "1.5.3")

    @patch("monitor.logger")
    def test_process_message_ignores_invalid_server_info(self, mock_logger):
        monitor.process_message(b"\x08not-json")
        mock_logger.debug.assert_any_call("got SERVER_INFO_SND opcode")
        mock_logger.warning.assert_not_called()


if __name__ == "__main__":
    unittest.main()
