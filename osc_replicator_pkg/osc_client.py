import time
import logging
from pythonosc.osc_message_builder import OscMessageBuilder
from osc_replicator_pkg.utils import flatten_osc_args


class OSCClient:
    def __init__(self, remote_host, remote_port):
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.clients = {}  # (ip, port): last_seen_time
        self.remote_transport = None  # Set by main after remote server is created

    def client_handler(self, sender, address, *args):
        osc_args = []
        if sender and isinstance(sender, tuple) and len(sender) == 2:
            self.clients[sender] = time.time()
            osc_args = args
            logging.debug(f"Received from client {sender}: {address} {osc_args}")
            logging.debug(f"Active clients: {list(self.clients.keys())}")
        else:
            osc_args = flatten_osc_args(args)
            if (
                osc_args
                and isinstance(osc_args[0], str)
                and osc_args[0].startswith("/")
            ):
                osc_args = osc_args[1:]
            logging.debug(
                f"Received from client (no sender tuple): {address} {osc_args}"
            )
        if isinstance(address, str) and address.startswith("/"):
            if self.remote_transport:
                # type: ignore[attr-defined]
                self.remote_transport.sendto(
                    OscMessageBuilder(address=address).build().dgram,
                    (self.remote_host, self.remote_port),
                )
                logging.debug(f"Forwarded to remote server: {address} {osc_args}")
            else:
                logging.error("Remote transport not initialized!")
        else:
            logging.warning(
                f"Not forwarding: address is not a valid OSC address: {address}"
            )
