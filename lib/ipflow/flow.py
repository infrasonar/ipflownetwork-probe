from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Iterator, Union
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

    def serialize(self) -> dict:
        _, _, fields, _ = flowset_templates[self.flowset_id]
        return {
            f.name: FIELD_TYPE_FUNC.get(f.id, lambda val: val)(val)
            for f, val in zip(fields, self.values)
        }

    def test_network(
        self,
        network: Union[IPv4Network, IPv6Network]
    ) -> Iterator[Union[IPv4Network, IPv6Network]]:
        _, _, _, fields_idx = flowset_templates[self.flowset_id]
        for ft in (
            FieldType.IPV4_DST_ADDR,
            FieldType.IPV4_NEXT_HOP,
            FieldType.IPV4_SRC_ADDR,
        ):
            if ft.value in fields_idx:
                addr = IPv4Address(self.values[fields_idx.index(ft.value)])
                if addr in network:
                    yield addr

        for ft in (
            FieldType.IPV6_DST_ADDR,
            FieldType.IPV6_NEXT_HOP,
            FieldType.IPV6_SRC_ADDR,
        ):
            if ft.value in fields_idx:
                addr = IPv6Address(self.values[fields_idx.index(ft.value)])
                if addr in network:
                    yield addr
