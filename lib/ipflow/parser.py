import logging
import struct
from .flowset import on_flowset, on_flowset_template


HEADER_FMT = '>HHLLLL'
HEADER_SIZE = 20


def on_packet(line: bytes):
    (
        version,
        count,
        sysuptime,
        unix_secs,
        sequence_number,
        source_id,
    ) = struct.unpack(HEADER_FMT, line[:HEADER_SIZE])

    pos = HEADER_SIZE
    while pos + 4 < len(line):  # TODO could also use (flow) count?
        flowset_id, length = struct.unpack('>HH', line[pos:pos+4])

        # prevent endless loop
        if length == 0:
            logging.error('failed to parse packet')
            break

        flowset = line[pos+4:pos+length]
        pos += length

        if flowset_id == 0:
            try:
                on_flowset_template(flowset)
            except Exception:
                logging.error('failed to parse FlowSet template')
                break
        else:
            try:
                for flow in on_flowset(flowset, flowset_id):
                    yield flow
            except Exception:
                logging.warning('failed to parse FlowSet')
                break
