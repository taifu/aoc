import unittest

import day_16 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data_1 = (("""8A004A801A8002F478""", 16),
                       ("""620080001611562C8802118E34""", 12),
                       ("""C0015000016115A2E0802F182340""", 23),
                       ("""A0016C880162017C3686B18A3D4780""", 31))

    def test_part_1_1(self):
        packet = day.compile("""D2FE28""")
        self.assertEqual(packet.typ, 4)
        self.assertEqual(packet.value, 2021)

    def test_part_1_2(self):
        packet = day.compile("""38006F45291200""")
        self.assertEqual(packet.version, 1)
        self.assertEqual(packet.typ, 6)
        self.assertEqual(2, len(packet.packets))
        self.assertEqual(packet.packets[0].value, 10)
        self.assertEqual(packet.packets[1].value, 20)

    def test_part_1_3(self):
        packet = day.compile("""EE00D40C823060""")
        self.assertEqual(packet.version, 7)
        self.assertEqual(packet.typ, 3)
        self.assertEqual(3, len(packet.packets))
        self.assertEqual(packet.packets[0].value, 1)
        self.assertEqual(packet.packets[1].value, 2)
        self.assertEqual(packet.packets[2].value, 3)

    def test_part_1_4(self):
        for data, versions in self.data_1:
            self.assertEqual(day.solve1(data), versions)

    def test_part_2_1(self):
        packet = day.compile("""C200B40A82""")
        self.assertEqual(packet.compute(), 3)

    def test_part_2_2(self):
        packet = day.compile("""04005AC33890""")
        self.assertEqual(packet.compute(), 54)

    def test_part_2_3(self):
        packet = day.compile("""880086C3E88112""")
        self.assertEqual(packet.compute(), 7)

    def test_part_2_4(self):
        packet = day.compile("""CE00C43D881120""")
        self.assertEqual(packet.compute(), 9)

    def test_part_2_5(self):
        packet = day.compile("""D8005AC2A8F0""")
        self.assertEqual(packet.compute(), 1)

    def test_part_2_6(self):
        packet = day.compile("""F600BC2D8F""")
        self.assertEqual(packet.compute(), 0)

    def test_part_2_7(self):
        packet = day.compile("""9C005AC2F8F0""")
        self.assertEqual(packet.compute(), 0)

    def test_part_2_8(self):
        packet = day.compile("""9C0141080250320F1802104A08""")
        self.assertEqual(packet.compute(), 1)

    def _test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 879)
        self.assertEqual(day.solve2(data), 539051804593)
