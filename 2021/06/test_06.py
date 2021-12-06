import unittest

import day_06 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """3,4,3,1,2"""

    def test_part_1_18(self):
        self.assertEqual(26, day.solve1(self.data, 18))

    def test_part_1(self):
        self.assertEqual(5934, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(26984457539, day.solve1(self.data, 256))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 345387)
        self.assertEqual(day.solve2(data), 1574445493136)
