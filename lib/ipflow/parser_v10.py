import logging
import struct
from .flowset import on_flowset, on_flowset_template


HEADER_FMT = '>HHLLL'
HEADER_SIZE = 16


def on_packet_v10(line: bytes):
    (
        version,
        message_length,
        export_time,
        sequence_number,
        observation_domain_id,
    ) = struct.unpack(HEADER_FMT, line[:HEADER_SIZE])

    pos = HEADER_SIZE
    while pos < len(line):  # TODO could also use message_length?
        flowset_id, length = struct.unpack('>HH', line[pos:pos+4])

        # prevent endless loop
        if length == 0:
            logging.error('failed to parse packet')
            break

        flowset = line[pos+4:pos+length]
        pos += length

        # rfc7011:
        # values 0-255 are reserved for special Set types
        # (e.g., Template Sets themselves)
        if flowset_id < 256:
            try:
                on_flowset_template(flowset)
            except Exception:
                logging.error('failed to parse FlowSet template')
                # TODO break?
        else:
            try:
                for flow in on_flowset(flowset, flowset_id):
                    yield flow
            except Exception:
                logging.warning('failed to parse FlowSet')
                # TODO break?
