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
    while pos < len(line):  # TODO could also use (flow) count?
        flowset_id, length = struct.unpack('>HH', line[pos:pos+4])
        flowset = line[pos+4:pos+length]
        pos += length
        if flowset_id == 0:
            on_flowset_template(flowset)
        else:
            for flow in on_flowset(flowset, flowset_id):
                yield flow
