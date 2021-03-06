import unittest

import day_02 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

    def test_part_1(self):
        self.assertEqual(2, day.solve(self.data)[0])

    def test_part_2(self):
        self.assertEqual(1, day.solve(self.data)[1])

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        part1, part2, = day.solve(data)
        self.assertEqual(part1, 580)
        self.assertEqual(part2, 611)
