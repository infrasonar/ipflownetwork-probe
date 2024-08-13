import time
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Dict, Set, Tuple, NamedTuple, Union
from .ipflow.flow import Flow


class Subscription(NamedTuple):
    network: Union[IPv4Network, IPv6Network]
    result: Set[Union[IPv4Address, IPv6Address]]
    timestamp: int

    @classmethod
    def make(cls, network: Union[IPv4Network, IPv6Network]):
        self = cls(
            network=network,
            result=set(),
            timestamp=int(time.time()),
        )
        return self

    def on_flow(self, flow: Flow):
        for addr in flow.test_network(self.network):
            self.result.add(addr)
