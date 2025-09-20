import pytest
from unittest.mock import Mock
from osc_replicator_pkg.osc_client import OSCClient


def test_client_handler_tracks_clients():
    client = OSCClient("127.0.0.1", 8000)
    client.remote_transport = Mock()
    sender = ("1.2.3.4", 12345)
    client.client_handler(sender, "/foo", 1, 2)
    assert sender in client.clients


def test_client_handler_forwards_valid():
    client = OSCClient("127.0.0.1", 8000)
    mock_transport = Mock()
    client.remote_transport = mock_transport
    sender = ("1.2.3.4", 12345)
    client.client_handler(sender, "/bar", 42)
    assert mock_transport.sendto.called


def test_client_handler_invalid_address():
    client = OSCClient("127.0.0.1", 8000)
    client.remote_transport = Mock()
    sender = ("1.2.3.4", 12345)
    # Should not forward if address is not a string or doesn't start with '/'
    client.client_handler(sender, "notosc", 1)
    assert not client.remote_transport.sendto.called
