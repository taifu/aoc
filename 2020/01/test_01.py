import unittest

import day_01 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """1721
979
366
299
675
1456"""

    def test_part_1(self):
        self.assertEqual(514579, day.solve(self.data))

    def test_part_2(self):
        self.assertEqual(241861950, day.solve2(self.data))
