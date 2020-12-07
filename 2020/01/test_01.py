import unittest

import day_01


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """1721
979
366
299
675
1456"""

    def test_part_1(self):
        self.assertEqual(514579, day_01.part1(self.data))

    def test_part_2(self):
        self.assertEqual(241861950, day_01.part2(self.data))
