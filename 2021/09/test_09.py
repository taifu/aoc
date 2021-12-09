import unittest

import day_09 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """2199943210
3987894921
9856789892
8767896789
9899965678
"""

    def test_part_1(self):
        self.assertEqual(15, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(1134, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 539)
        self.assertEqual(day.solve2(data), 736920)
