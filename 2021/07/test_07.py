import unittest

import day_07 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """16,1,2,0,4,2,7,1,2,14
"""

    def test_part_1(self):
        self.assertEqual(37, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(168, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 345197)
        self.assertEqual(day.solve2(data), 96361606)
