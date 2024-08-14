import logging
import struct
from .flowset import on_flowset
from .flow import V5_TEMPLATE_ID


HEADER_FMT = '>HHLLLLBBH'
HEADER_SIZE = 24


def on_packet_v5(line: bytes):
    (
        version,
        count,
        sysuptime,
        unix_secs,
        unix_nsecs,
        flow_sequence,
        engine_type,
        engine_id,
        sampling_interval
    ) = struct.unpack(HEADER_FMT, line[:HEADER_SIZE])

    pos = HEADER_SIZE
    while pos + 48 < len(line):  # TODO could also use (flow) count?
        flowset = line[pos:pos+48]
        pos += 48

        try:
            for flow in on_flowset(flowset, V5_TEMPLATE_ID):
                yield flow
        except Exception:
            logging.warning('failed to parse FlowSet')
            # TODO break?
