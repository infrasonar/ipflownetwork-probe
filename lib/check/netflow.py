import asyncio
import ipaddress
import logging
from libprobe.asset import Asset
from libprobe.exceptions import IgnoreCheckException
from ..netflow.field_type import FieldType
from ..state import subscriptions, subscribe_check


async def check_netflow(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    try:
        address = check_config['address']
        encoded = ipaddress.ip_address(address).packed
    except Exception:
        logging.warning(
            'Check did not run; '
            'address is not provided, invalid or empty')
        raise IgnoreCheckException

    filters = [
        (FieldType.IPV4_SRC_ADDR.value, encoded),
        # TODO (FieldType.IPV4_NEXT_HOP, encoded),
    ]

    # get current subscription
    subs = subscriptions.get((asset.id, 'netflow'))
    flows = subs.flows if subs else []

    # re-subscribe
    subscribe_check(asset.id, 'netflow', filters)

    # group flows by dst addr
    grouped = {}
    for f in flows:
        dst_addr = f['ipv4_dst_addr']
        dst_port = f['l4_dst_port']
        f['name'] = name = f'{dst_addr}|{dst_port}'
        grouped[name] = f

    state_data = {
        'netflow': list(grouped.values()),
    }
    return state_data
