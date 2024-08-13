import asyncio
import time
import logging
from ipaddress import IPv4Network
from typing import Dict, Tuple
from .subscription import Subscription


CLEANUP_SUBSCRIPTIONS_INTERVAL = 60
MAX_SUBSCRIPTION_AGE = 3600


def subscribe_check(
    asset_id: int,
    check_key: str,
    network: IPv4Network,
):
    logging.info(f'subscribe asset `{asset_id}` check `{check_key}`')
    subscriptions[(asset_id, check_key)] = Subscription.make(network)


def unsubscribe_check(
    asset_id: int,
    check_key: str
):
    logging.info(f'unsubscribe asset `{asset_id}` check `{check_key}`')
    subscriptions.pop((asset_id, check_key), None)


async def cleanup_subscriptions_loop():
    while True:
        now = time.time()
        for key in list(subscriptions):
            subs = subscriptions[key]
            if now - subs.timestamp > MAX_SUBSCRIPTION_AGE:
                subscriptions.pop(key)
        await asyncio.sleep(60)


subscriptions: Dict[int, Subscription] = {}
