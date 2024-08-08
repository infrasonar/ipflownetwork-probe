class Flow:
    def __init__(self, flowset_id, values):
        self.flowset_id = flowset_id
        self.values = values

    def serialize(self):
        # for k in list(f):
        #     if isinstance(f[k], (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        #         f[k] = str(f[k])
        #     elif isinstance(f[k], bytes):
        #         f[k] = [int(a) for a in f[k]]
        #         # del f[k]
        fmt, l, funs, fields, fields_idx = flowset_templates[self.flowset_id]
        values = [fun(v) for fun, v in zip(funs, self.values)]
        return dict(zip([f.name for f in fields], values))

    def test(self, filters):
        fmt, l, funs, fields, fields_idx = flowset_templates[self.flowset_id]
        return any(filter_id in fields_idx and self.values[fields_idx.index(filter_id)] == filter_value for filter_id, filter_value in filters)


from .flowset import flowset_templates
