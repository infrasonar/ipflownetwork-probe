import struct
import unittest
from lib.ipflow.flow import flowset_templates
from lib.ipflow.parser import on_packet
from lib.ipflow.parser_v10 import on_packet_v10
from lib.ipflow.parser_v5 import on_packet_v5

DATA_DIR = 'test/captures'


class Test(unittest.TestCase):

    def test_v5(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v5_ipv4.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 74 < len(line):
            size, = struct.unpack('H', line[pos+8:pos+10])
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHHBBH4s4s', line[pos+46:pos+66])
            l4 = struct.unpack('>HHHH', line[pos+66:pos+74])

            # print(l2)
            # print(l3)
            # print(l4)

            pkt = line[pos+74:pos+size]
            pos += size
            for item in on_packet_v5(pkt, l3[9]):
                ct += 1

        # expect 3 flows
        self.assertEqual(3, ct)

    def test_v9(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v9_ipv4.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 74 < len(line):
            size, = struct.unpack('H', line[pos+8:pos+10])
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHHBBH4s4s', line[pos+46:pos+66])
            l4 = struct.unpack('>HHHH', line[pos+66:pos+74])

            # print(l2)
            # print(l3)
            # print(l4)

            pkt = line[pos+74:pos+size]
            pos += size
            for item in on_packet(pkt, l3[9]):
                ct += 1

        # expect 2 flows
        self.assertEqual(2, ct)
        del flowset_templates[(l3[9], 0, 256)]

    def test_v9_ipv6(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v9_ipv6.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 94 < len(line):
            size, = struct.unpack('H', line[pos+8:pos+10])
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHBB16s16s', line[pos+46:pos+86])
            l4 = struct.unpack('>HHHH', line[pos+86:pos+94])

            # print(l2)
            # print(l3)
            # print(l4)

            pkt = line[pos+94:pos+size]
            pos += size

            for item in on_packet(pkt, l3[7]):
                ct += 1

        # expect 5 flows
        self.assertEqual(5, ct)
        del flowset_templates[(l3[7], 0, 256)]

    def test_v9_mpls(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v9_mpls.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 74 < len(line):
            size, = struct.unpack('H', line[pos+8:pos+10])
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHHBBH4s4s', line[pos+46:pos+66])
            l4 = struct.unpack('>HHHH', line[pos+66:pos+74])

            # print(l2)
            # print(l3)
            # print(l4)

            pkt = line[pos+74:pos+size]
            pos += size
            for item in on_packet(pkt, l3[9]):
                ct += 1

        # no template
        self.assertEqual(0, ct)

    def test_v10(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v10_ipv4.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 74 < len(line):
            size, = struct.unpack('H', line[pos+8:pos+10])
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHHBBH4s4s', line[pos+46:pos+66])
            l4 = struct.unpack('>HHHH', line[pos+66:pos+74])

            # print(l2)
            # print(l3)
            # print(l4)

            pkt = line[pos+74:pos+size]
            pos += size
            for item in on_packet_v10(pkt, l3[9]):
                ct += 1

        # expect 3 flows
        self.assertEqual(3, ct)
        del flowset_templates[(l3[9], 0, 256)]

    def test_v10_ipv6(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v10_ipv6.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 94 < len(line):
            size, = struct.unpack('H', line[pos+8:pos+10])
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHBB16s16s', line[pos+46:pos+86])
            l4 = struct.unpack('>HHHH', line[pos+86:pos+94])

            # print(l2)
            # print(l3)
            # print(l4)

            pkt = line[pos+94:pos+size]
            pos += size

            for item in on_packet_v10(pkt, l3[7]):
                ct += 1

        # expect 3 flows
        self.assertEqual(3, ct)
        del flowset_templates[(l3[7], 0, 256)]

    def test_v10_mpls(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v10_mpls.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 74 < len(line):
            size, = struct.unpack('H', line[pos+8:pos+10])
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHHBBH4s4s', line[pos+46:pos+66])
            l4 = struct.unpack('>HHHH', line[pos+66:pos+74])

            # print(l2)
            # print(l3)
            # print(l4)

            pkt = line[pos+74:pos+size]
            pos += size
            for item in on_packet_v10(pkt, l3[7]):
                ct += 1

        # no template
        self.assertEqual(0, ct)


if __name__ == '__main__':
    unittest.main()
