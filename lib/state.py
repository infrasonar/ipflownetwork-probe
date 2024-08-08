import logging
from typing import Dict, Tuple
from .subscription import Subscription


def subscribe_check(
    asset_id: int,
    check_key: str,
    filters: Tuple[Tuple[int, bytes]]
):
    logging.info(f'subscribe asset `{asset_id}` check `{check_key}`')
    subscriptions[(asset_id, check_key)] = Subscription.make(filters)


def unsubscribe_check(
    asset_id: int,
    check_key: str
):
    logging.info(f'unsubscribe asset `{asset_id}` check `{check_key}`')
    subscriptions.pop((asset_id, check_key), None)


subscriptions: Dict[int, Subscription] = {}
