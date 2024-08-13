from ipaddress import IPv4Address, IPv4Network
from typing import List
from .field_type import FIELD_TYPE_FUNC
from .field_type import FieldType


flowset_templates = {}


class Flow:
    __slots__ = (
        'flowset_id',
        'values',
    )

    def __init__(self, flowset_id, values):
        self.flowset_id = flowset_id
        self.values = values

    def serialize(self):
        fmt, l, fields, fields_idx = flowset_templates[self.flowset_id]
        return {
            f.name: FIELD_TYPE_FUNC.get(f.id, lambda val: val)(val)
            for f, val in zip(fields, self.values)
        }

    def test_ipv4_network(self, network: IPv4Network) -> List[str]:
        fmt, l, fields, fields_idx = flowset_templates[self.flowset_id]
        for ft in (
            FieldType.IPV4_DST_ADDR,
            FieldType.IPV4_NEXT_HOP,
            FieldType.IPV4_SRC_ADDR,
        ):
            if ft.value in fields_idx:
                addr = IPv4Address(self.values[fields_idx.index(ft.value)])
                if addr in network:
                    yield addr
