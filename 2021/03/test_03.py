import unittest

import day_03 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

    def test_part_1(self):
        self.assertEqual(198, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(230, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 3633500)
        self.assertEqual(day.solve2(data), 4550283)
