import asyncio
import socket
import time
import logging
from ipaddress import IPv4Network, IPv6Network
from typing import Dict, Optional, Tuple, Union
from .subscription import Subscription


CLEANUP_SUBSCRIPTIONS_INTERVAL = 60
MAX_SUBSCRIPTION_AGE = 3600
MAX_HOST_LOOKUP_AGE = 14400


def subscribe_check(
    asset_id: int,
    check_key: str,
    network: Union[IPv4Network, IPv6Network],
):
    logging.info(f'subscribe asset `{asset_id}` check `{check_key}`')
    subscriptions[(asset_id, check_key)] = Subscription.make(network)


def unsubscribe_check(
    asset_id: int,
    check_key: str
):
    logging.info(f'unsubscribe asset `{asset_id}` check `{check_key}`')
    subscriptions.pop((asset_id, check_key), None)


def get_host_by_addr(address: str) -> Optional[str]:
    host, expire_ts = host_lk.get(address, (None, None))

    # request new name when no in lookup or aged
    if expire_ts is None or expire_ts < time.time():
        try:
            host, _, _ = socket.gethostbyaddr(address)
        except Exception:
            # when error set empty
            host = None

        # add expiriation timestamp also when not found
        host_lk[address] = (host, time.time() + MAX_HOST_LOOKUP_AGE)
    return host


async def cleanup_subscriptions_loop():
    while True:
        now = time.time()
        for key in list(subscriptions):
            subs = subscriptions[key]
            if now - subs.timestamp > MAX_SUBSCRIPTION_AGE:
                subscriptions.pop(key)
        await asyncio.sleep(60)


host_lk: Dict[str, Tuple[str, float]] = {}
subscriptions: Dict[int, Subscription] = {}
