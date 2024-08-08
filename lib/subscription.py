from typing import Dict, List, Tuple, NamedTuple
from .netflow.flow import Flow


class Subscription(NamedTuple):
    filters: Tuple[Tuple[int, bytes]]
    flows: List[Flow]

    @classmethod
    def make(cls, filters: Tuple[Tuple[int, bytes]]):
        self = cls(
            filters=filters,
            flows=[],
        )
        return self
