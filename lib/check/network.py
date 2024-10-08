import ipaddress
import logging
from libprobe.asset import Asset
from libprobe.exceptions import IgnoreCheckException
from ..state import subscriptions, subscribe_check, get_host_by_addr


async def check_network(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    try:
        network = check_config['network']
        network = ipaddress.ip_network(network)
    except Exception:
        logging.warning(
            'Check did not run; '
            'network is not provided, invalid or empty')
        raise IgnoreCheckException

    # get current subscription
    subs = subscriptions.get((asset.id, 'network', network))
    result = subs.result if subs else {}

    # re-subscribe
    subscribe_check(asset.id, 'network', network)

    state_data = {
        'network': [{
            'name': str(addr),
            'host': get_host_by_addr(str(addr)),
            'ipflow_version': version,
        } for addr, version in result.items()],
    }
    return state_data
