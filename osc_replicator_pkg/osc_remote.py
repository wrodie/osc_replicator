import time
import logging
from pythonosc import udp_client

CLIENT_TIMEOUT = 12  # seconds


class OSCRemote:
    def __init__(self, client_tracker, wing_triplets_clients):
        self.client_tracker = (
            client_tracker  # Should be a dict of (ip, port): last_seen_time
        )
        self.wing_triplets_clients = wing_triplets_clients  # Track wing clients specifically

    def remote_handler(self, address, *args):
        now = time.time()
        # Remove stale clients in-place to preserve shared reference
        stale = [
            k for k, v in self.client_tracker.items()
            if now - v >= CLIENT_TIMEOUT
        ]
        for k in stale:
            del self.client_tracker[k]
        logging.debug(f"->Received from remote server: {address} {args}")
        logging.debug(
            f"Forwarding to clients: {list(self.client_tracker.keys())}"
        )
        osc_args = [a for a in args if not isinstance(a, tuple)]
        for ip, port in self.client_tracker:
            current_args = osc_args
            # Handle wing triplets mode for responses to clients
            if (ip, port) in self.wing_triplets_clients:
                if len(osc_args) == 3:  # If it's a triplet
                    current_args = [osc_args[-1]]  # Only keep last value
            client = udp_client.SimpleUDPClient(ip, port)
            client.send_message(address, current_args)
            logging.debug(
                f"Forwarded to client {(ip, port)}: "
                f"{address} {current_args}"
            )
