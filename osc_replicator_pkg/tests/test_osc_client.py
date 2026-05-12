 import pytest
from unittest.mock import Mock0+B
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


def test_wing_triplets_handling():
    client = OSCClient("127.0.0.1", 8000)
    mock_transport = Mock()
    client.remote_transport = mock_transport
    sender1 = ("1.2.3.4", 12345)
    sender2 = ("5.6.7.8", 54321)

    # Test basic wing triplets handling
    client.client_handler(sender1, "/*S", 1)
    assert sender1 in client.wing_triplets_clients
    message = mock_transport.sendto.call_args[0][0]
    assert message.decode().startswith("/*s")

    # Test another client sending /*S
    mock_transport.reset_mock()
    client.client_handler(sender2, "/*S", 2)
    assert sender2 in client.wing_triplets_clients
    message = mock_transport.sendto.call_args[0][0]
    assert message.decode().startswith("/*s")
