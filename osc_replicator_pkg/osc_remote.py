import time
import logging
from pythonosc import udp_client

CLIENT_TIMEOUT = 10  # seconds


class OSCRemote:
    def __init__(self, client_tracker):
        self.client_tracker = (
            client_tracker  # Should be a dict of (ip, port): last_seen_time
        )

    def remote_handler(self, address, *args):
        now = time.time()
        # Remove stale clients
        self.client_tracker = {
            k: v for k, v in self.client_tracker.items() if now - v < CLIENT_TIMEOUT
        }
        logging.debug(f"Received from remote server: {address} {args}")
        logging.debug(f"Forwarding to clients: {list(self.client_tracker.keys())}")
        osc_args = [a for a in args if not isinstance(a, tuple)]
        for ip, port in self.client_tracker:
            client = udp_client.SimpleUDPClient(ip, port)
            client.send_message(address, osc_args)
            logging.debug(f"Forwarded to client {(ip, port)}: {address} {osc_args}")
