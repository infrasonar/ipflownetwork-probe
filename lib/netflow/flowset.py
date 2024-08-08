import struct
from .field import Field
from .field_type import FIELD_TYPE_FMT
from .field_type import FIELD_TYPE_FUNC
from .flow import Flow


def on_flowset_template(line):
    pos = 0
    while pos < len(line):
        template_id, field_count = struct.unpack('>HH', line[pos:pos+4])
        fields = [
            Field(*struct.unpack('>HH', line[i:i+4]))
            for i in range(pos + 4, pos + 4 + field_count * 4, 4)
        ]
        # for f, l in fields:
        #     assert f > 99 or f in FIELD_TYPE_FUNC or f in FIELD_TYPE_FMT, f
        pos += 4 + field_count * 4
        flowset_templates[template_id] = (
            '>' + ''.join(FIELD_TYPE_FMT.get(f.id, f'{f.length}s') for f in fields),
            sum(f.length for f in fields),
            [FIELD_TYPE_FUNC.get(f.id, lambda a: a) for f in fields],
            fields,  # zip(itertools.accumulate([0] + [field_l for _, field_l in fields]), fields),
            [f.id for f in fields],
        )


def on_flowset(line, flowset_id):
    if flowset_id in flowset_templates:
        fmt, l, funs, fields, fields_idx = flowset_templates[flowset_id]
        for i in range(0, len(line) - 4, l):
            values = struct.unpack(fmt, line[i:i+l])
            yield Flow(flowset_id, values)


flowset_templates = {}
