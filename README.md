# osc_replicator

## Overview

`osc_replicator` is a Python module and command-line tool that acts as a relay between multiple Open Sound Control (OSC) clients and a single remote OSC server. It allows multiple local OSC clients to communicate with a remote OSC server as if they were directly connected, and ensures that replies from the remote server are broadcast back to all active clients.

## How It Works

- The relay listens for OSC messages from any number of local clients on a specified UDP port.
- When a message is received from a client, the relay:
  - Tracks the client’s address (IP and port).
  - Forwards the message to the remote OSC server using a dedicated UDP socket.
- When a reply is received from the remote server, the relay:
  - Forwards the reply to all currently active clients (those who have sent a message recently).
  - Cleans up clients that have not sent a message within a timeout window (default: 10 seconds).

This design allows seamless two-way communication between multiple local OSC clients and a single remote OSC server, even if the server only supports a single client.

## Installation

You can install dependencies either in a virtual environment (recommended) or system-wide.

### Option 1: Using a Virtual Environment (Recommended)

```sh
git clone <your-repo-url>
cd osc_replicator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Option 2: System-wide Install

> **Note:** You may need `sudo` for system-wide installs, and this may affect other Python projects on your system.

```sh
git clone <your-repo-url>
cd osc_replicator
pip install --user -r requirements.txt
```

## Usage

### Main Entry Point (Recommended)

Run the relay from the project root using the wrapper script:

```sh
python run_replicator.py --listen-port 2223 --remote-host 192.168.201.41 --remote-port 2223 --enable-wing-triplets-response
```

- `--listen-port`: UDP port to listen for incoming OSC clients (e.g., 9000)
- `--remote-host`: Hostname or IP of the remote OSC server
- `--remote-port`: UDP port of the remote OSC server
- `--enable-wing-triplets-response`: Enable special handling for wing triplets:
  - Changes `/*S` messages to `/*s`
  - Filters triplets to only pass the last value

### Alternative: Python Module Entry Point

Advanced users can also run the relay directly as a module:

```sh
# Standard mode
python -m osc_replicator_pkg --listen-port 9000 --remote-host 127.0.0.1 --remote-port 8000

# With wing triplets mode enabled
python -m osc_replicator_pkg --listen-port 9000 --remote-host 127.0.0.1 --remote-port 8000 --enable-wing-triplets-response
```

## Running Tests

### With a Virtual Environment
```sh
PYTHONPATH=. .venv/bin/pytest osc_replicator_pkg/tests
```

### Without a Virtual Environment
```sh
PYTHONPATH=. pytest osc_replicator_pkg/tests
```

All tests are located in the `osc_replicator_pkg/tests/` directory.

## Code Formatting

This project uses [Black](https://black.readthedocs.io/) for code formatting.

### With a Virtual Environment
```sh
.venv/bin/black .
```

### Without a Virtual Environment
```sh
black .
```

## Wing Triplets Mode

When enabled with `--enable-wing-triplets-response`, the replicator provides special handling for proxying a Behringer Wing Mixer.:

1. Any OSC message send by a client with address `/*S` will be changed to `/*s`
2. Any message returned by the remote server with triplets of data to a client that has sent `/*S` will only receive the last element


## Project Structure

```
osc_replicator/
├── run_replicator.py           # Wrapper script (main entry point)
├── requirements.txt
├── README.md
└── osc_replicator_pkg/
    ├── __main__.py             # Main entry point for python -m osc_replicator_pkg
    ├── __init__.py
    ├── osc_client.py           # Handles client-side logic
    ├── osc_remote.py           # Handles remote server replies
    ├── utils.py                # Shared utilities
    └── tests/                  # Unit tests
        ├── test_osc_client.py
        ├── test_osc_remote.py
        └── test_utils.py
```

---

## License

MIT License (or specify your license here)
