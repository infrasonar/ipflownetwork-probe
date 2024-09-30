import asyncio
import logging
import os
import struct
from lib.ipflow.parser import on_packet
from lib.ipflow.parser_v10 import on_packet_v10
from lib.ipflow.parser_v5 import on_packet_v5
from .state import subscriptions

LISTEN_PORT = int(os.getenv('LISTEN_PORT', '2055'))
FORWARD_HOST = os.getenv('FORWARD_HOST', '127.0.0.1')
FORWARD_PORTS = os.getenv('FORWARD_PORTS')
FORWARD = [
    (FORWARD_HOST, pt)
    for pt in map(int, FORWARD_PORTS.split(','))
] if FORWARD_PORTS else []
assert all(0 < pt < 65536 and pt != LISTEN_PORT for _, pt in FORWARD)
assert len(FORWARD) == len(set(FORWARD))

COMMON_HEADER_FMT = '>HHL'
COMMON_HEADER_SZ = 8


class ServerProtocol(asyncio.Protocol):

    def __init__(self):
        super().__init__()
        self.log_unsupported_version = 0
        self.log_failed_to_forward = set()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if len(data) < COMMON_HEADER_SZ:
            return

        (
            version,
            count,
            sysuptime,
        ) = struct.unpack(COMMON_HEADER_FMT, data[:COMMON_HEADER_SZ])

        if version not in (5, 9, 10):
            if self.log_unsupported_version < 10:
                self.log_unsupported_version += 1
                logging.warning('unsupported netflow version')
            return

        for dest in FORWARD:
            try:
                self.transport.sendto(data, dest)
            except Exception:
                if dest not in self.log_failed_to_forward:
                    self.log_failed_to_forward.add(dest)
                    logging.warning(f'failed to forward package to {dest}')

        # v5 has no templates so could be ignored when no checks are listening
        if version == 5 and not subscriptions:
            return

        parser = {
            5: on_packet_v5,
            9: on_packet,
            10: on_packet_v10,
        }[version]
        # parse every packet regardless of any subscriptions
        # whe need the template flowsets
        for flow in parser(data, addr[0]):
            for subs in subscriptions.values():
                subs.on_flow(flow, version)


def start_server(loop: asyncio.AbstractEventLoop):
    logging.info(f'listening for netflow/ipfix packets on port {LISTEN_PORT}')
    for addr, port in FORWARD:
        logging.info(f'forwarding to {addr}:{port}')

    try:
        loop.run_until_complete(
            loop.create_datagram_endpoint(
                ServerProtocol,
                local_addr=('0.0.0.0', LISTEN_PORT))
        )
    except OSError:
        logging.critical(
            f'Port {LISTEN_PORT} is already in use. Most likely the '
            '`ipflow-probe` is using it. Configure the `ipflow-probe` '
            f'to listen to port {LISTEN_PORT + 1} and set the '
            '`ipflownetwork-probe` to forward the traffic there. See the '
            '`LISTEN_PORT` and `FORWARD_PORTS` environment variable or use '
            'the appliance manager '
            '(https://github.com/infrasonar/appliance-manager).'
        )
        exit(1)
