import time
from ipaddress import IPv4Address, IPv4Network
from typing import Dict, Set, Tuple, NamedTuple
from .netflow.flow import Flow


class Subscription(NamedTuple):
    network: IPv4Network
    result: Set[IPv4Address]
    timestamp: int

    @classmethod
    def make(cls, network: IPv4Network):
        self = cls(
            network=network,
            result=set(),
            timestamp=int(time.time()),
        )
        return self

    def on_flow(self, flow: Flow):
        for addr in flow.test_ipv4_network(self.network):
            self.result.add(addr)
