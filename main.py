import asyncio
from libprobe.probe import Probe
from lib.check.network import check_network
from lib.server import start_server
from lib.state import cleanup_subscriptions_loop
from lib.version import __version__ as version


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    start_server(loop)
    asyncio.ensure_future(cleanup_subscriptions_loop(), loop=loop)

    checks = {
        'network': check_network,
    }

    probe = Probe("ipflownetwork", version, checks)

    probe.start(loop=loop)
