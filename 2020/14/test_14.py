import unittest

import day_14 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""
        self.data2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

    def test_part_1(self):
        self.assertEqual(day.solve(self.data1), 165)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data2), 208)
