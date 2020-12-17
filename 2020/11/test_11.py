import unittest
import pytest

import day_11 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

    def test_part_1(self):
        self.assertEqual(day.solve(self.data), 37)

    def test_part_2(self):
        self.assertEqual(day.solve(self.data, step=2), 26)

    @pytest.mark.slow
    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve(data), 2412)
        self.assertEqual(day.solve(data, step=2), 2176)
