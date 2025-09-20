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


def test_remote_handler_inplace_tracker_update_and_forwarding():
    # Simulate two active clients and one stale
    now = 1000000000
    tracker = {
        ("1.2.3.4", 12345): now,           # active
        ("5.6.7.8", 54321): now - 5,       # active
        ("9.9.9.9", 99999): now - 20,      # stale
    }
    orig_tracker = tracker
    remote = OSCRemote(tracker)
    from unittest.mock import patch as _patch
    with _patch("pythonosc.udp_client.SimpleUDPClient") as mock_client, \
         _patch("time.time", return_value=now):
        remote.remote_handler("/test", 42)
        # Only active clients should be called
        calls = [("/test", (42,))] * 2
        actual_calls = [(c.args[0], tuple(c.args[1])) for c in mock_client.return_value.send_message.call_args_list]
        assert set(actual_calls) == set(calls)
        # The tracker should be updated in-place (same object)
        assert tracker is orig_tracker
        # Only active clients remain
        assert set(tracker.keys()) == {("1.2.3.4", 12345), ("5.6.7.8", 54321)}

def test_remote_handler_removes_stale():
    tracker = {("1.2.3.4", 12345): 0}  # stale
    remote = OSCRemote(tracker)
    with patch("pythonosc.udp_client.SimpleUDPClient") as mock_client:
        remote.remote_handler("/reply", 1)
        # Should not forward to stale client
        assert not mock_client.called
