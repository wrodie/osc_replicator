import argparse
import asyncio
import logging
from pythonosc import osc_server, dispatcher
from osc_replicator_pkg.osc_client import OSCClient
from osc_replicator_pkg.osc_remote import OSCRemote

logging.basicConfig(
    level=logging.WARNING,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)


def main():
    parser = argparse.ArgumentParser(description="OSC Replicator")
    parser.add_argument(
        "--listen-port", type=int, required=True, help="Port to listen for OSC clients"
    )
    parser.add_argument(
        "--remote-host",
        type=str,
        required=True,
        help="Remote OSC server hostname or IP",
    )
    parser.add_argument(
        "--remote-port", type=int, required=True, help="Remote OSC server port"
    )
    parser.add_argument(
        "--enable-wing-triplets-response",
        action="store_true",
        help="Enable wing triplets response mode for clients",
    )
    args = parser.parse_args()

    client = OSCClient(args.remote_host, args.remote_port)
    remote = OSCRemote(client.clients, client.wing_triplets_clients)

    async def start():
        loop = asyncio.get_running_loop()
        # Client side
        disp = dispatcher.Dispatcher()
        disp.set_default_handler(client.client_handler, needs_reply_address=True)
        server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", args.listen_port), disp, loop)  # type: ignore
        transport, protocol = await server.create_serve_endpoint()

        # Remote side (OS picks port)
        remote_disp = dispatcher.Dispatcher()
        remote_disp.set_default_handler(remote.remote_handler)
        remote_server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", 0), remote_disp, loop)  # type: ignore
        remote_transport, remote_protocol = await remote_server.create_serve_endpoint()
        client.remote_transport = remote_transport
        actual_port = remote_transport.get_extra_info("sockname")[1]
        logging.info(f"Remote relay port assigned by OS: {actual_port}")

        logging.info(f"Listening for clients on port {args.listen_port}")
        logging.info(f"Listening for remote server on port {actual_port}")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logging.info("Shutting down...")
        transport.close()
        remote_transport.close()

    asyncio.run(start())


if __name__ == "__main__":
    main()
