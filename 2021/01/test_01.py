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
        self.assertEqual(514579, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(241861950, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 889779)
        self.assertEqual(day.solve2(data), 76110336)
