import unittest

import day_01 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

    def test_part_1(self):
        self.assertEqual(24000, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(45000, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 67622)
        self.assertEqual(day.solve2(data), 201491)
