import unittest

import day_02 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """A Y
B X
C Z"""

    def test_part_1(self):
        self.assertEqual(15, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(12, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 12772)
        self.assertEqual(day.solve2(data), 11618)
