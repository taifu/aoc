import unittest
import pytest

import day_22 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

    def test_part1(self):
        self.assertEqual(day.solve(self.data), 306)

    def test_part2(self):
        self.assertEqual(day.solve(self.data, step=2), 291)

    @pytest.mark.slow
    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve(data), 32413)
        self.assertEqual(day.solve(data, step=2), 31596)
