import os
import unittest
from lib.ipflow.parser import on_packet

DATA_DIR = 'test/captures'


class Test(unittest.TestCase):

    def test_v9(self):
        with open(f'{DATA_DIR}/netflow_v9_ipv4.pcapng', 'rb') as f:
            line = f.read()
        print([a for a in line][:52])

        import struct
        l2 = struct.unpack('>6s6sH', line[:14])
        print(l2)
        i = 14

        i = 0
        for _ in range(1):
            size, = struct.unpack('H', line[i+32:i+34])

            pkt = line[i+82:i+40+size]
            i += size + 16
            for item in on_packet(pkt):
                print(item)
