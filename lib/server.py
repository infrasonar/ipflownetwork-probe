import asyncio
import logging
import os
from .ipflow.parser import on_packet
from .state import subscriptions

LISTEN_PORT = int(os.getenv('LISTEN_PORT', '2055'))


class ServerProtocol(asyncio.Protocol):

    def datagram_received(self, data, addr):
        # parse every packet regardless of any subscriptions
        # whe need the template flowsets
        for flow in on_packet(data):
            for subs in subscriptions.values():
                subs.on_flow(flow)


async def start_server():
    logging.info('Starting UDP server')
    loop = asyncio.get_event_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        ServerProtocol,
        local_addr=('0.0.0.0', LISTEN_PORT))

    return transport, protocol
