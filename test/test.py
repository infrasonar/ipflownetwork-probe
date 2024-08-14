import struct
import unittest
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
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHHBBH4s4s', line[pos+46:pos+66])
            l4 = struct.unpack('>HHHH', line[pos+66:pos+74])

            # print(l2)
            # print(l3)
            # print(l4)

            size = l4[2] - 8  # exclude l4_header
            pkt = line[pos+74:pos+74+size]
            pos += 74 + size
            for item in on_packet_v5(pkt):
                ct += 1

        # expect 2 flows
        self.assertEqual(2, ct)

    def test_v9(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v9_ipv4.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 74 < len(line):
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHHBBH4s4s', line[pos+46:pos+66])
            l4 = struct.unpack('>HHHH', line[pos+66:pos+74])

            # print(l2)
            # print(l3)
            # print(l4)

            size = l4[2] - 8  # exclude l4_header
            pkt = line[pos+74:pos+74+size]
            pos += 74 + size
            for item in on_packet(pkt):
                ct += 1

        # expect 2 flows
        self.assertEqual(2, ct)

    def test_v9_ipv6(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v9_ipv6.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 94 < len(line):
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHBB16s16s', line[pos+46:pos+86])
            l4 = struct.unpack('>HHHH', line[pos+86:pos+94])

            # print(l2)
            # print(l3)
            # print(l4)

            size = l4[2] - 8  # exclude l4_header
            pkt = line[pos+94:pos+94+size]
            pos += 94 + size

            for item in on_packet(pkt):
                ct += 1

        # expect 3 flows and an exception
        self.assertEqual(3, ct)

    def test_v10(self):
        frame_offset = 100
        with open(f'{DATA_DIR}/netflow_v10_ipv4.pcapng', 'rb') as f:
            line = f.read()[frame_offset:]

        ct = 0
        pos = 0
        while pos + 74 < len(line):
            l2 = struct.unpack('>6s6s2s', line[pos+32:pos+46])
            l3 = struct.unpack('>BBHHHBBH4s4s', line[pos+46:pos+66])
            l4 = struct.unpack('>HHHH', line[pos+66:pos+74])

            # print(l2)
            # print(l3)
            # print(l4)

            size = l4[2] - 8  # exclude l4_header
            pkt = line[pos+74:pos+74+size]
            pos += 74 + size
            for item in on_packet_v10(pkt):
                ct += 1

        # expect 3 flows
        self.assertEqual(3, ct)


if __name__ == '__main__':
    unittest.main()
