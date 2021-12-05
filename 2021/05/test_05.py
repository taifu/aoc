import unittest

import day_05 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

    def test_part_1(self):
        self.assertEqual(5, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(12, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 5774)
        self.assertEqual(day.solve2(data), 18423)
