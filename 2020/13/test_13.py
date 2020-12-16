import unittest

import day_13 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """939
7,13,x,x,59,x,31,19
"""

    def test_part_1(self):
        self.assertEqual(day.solve1(self.data), 295)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data), 1068781)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 2947)
        self.assertEqual(day.solve2(data), 526090562196173)
