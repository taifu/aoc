import unittest

import day_01 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """199
200
208
210
200
207
240
269
260
263"""

    def test_part_1(self):
        self.assertEqual(7, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(5, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 1696)
        self.assertEqual(day.solve2(data), 1737)
