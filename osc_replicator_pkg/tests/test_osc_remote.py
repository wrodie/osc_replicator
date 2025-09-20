import pytest
from unittest.mock import patch
from osc_replicator_pkg.osc_remote import OSCRemote


def test_remote_handler_filters_and_forwards():
    tracker = {("1.2.3.4", 12345): 9999999999}
    remote = OSCRemote(tracker)
    with patch("pythonosc.udp_client.SimpleUDPClient") as mock_client:
        remote.remote_handler("/reply", 1, 2, ("should", "ignore"))
        assert mock_client.called
        instance = mock_client.return_value
        instance.send_message.assert_called_with("/reply", [1, 2])


def test_remote_handler_removes_stale():
    tracker = {("1.2.3.4", 12345): 0}  # stale
    remote = OSCRemote(tracker)
    with patch("pythonosc.udp_client.SimpleUDPClient") as mock_client:
        remote.remote_handler("/reply", 1)
        # Should not forward to stale client
        assert not mock_client.called
