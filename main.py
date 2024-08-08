import asyncio
from libprobe.probe import Probe
from lib.check.netflow import check_netflow
from lib.server import start_netflow_server
from lib.version import __version__ as version


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_netflow_server())

    checks = {
        'netflow': check_netflow,
    }

    probe = Probe("netflow", version, checks)

    probe.start()
