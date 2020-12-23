import unittest
import pytest

import day_23 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """389125467"""

    def test_part1_short(self):
        self.assertEqual(day.solve(self.data, moves=10), "92658374")

    def test_part1(self):
        self.assertEqual(day.solve(self.data), "67384529")

    @pytest.mark.slow
    def test_part2(self):
        self.assertEqual(day.solve(self.data, moves=10000000, n_cups=1000000), 149245887792)

    @pytest.mark.slow
    def test_solution(self):
        data = "123487596"
        self.assertEqual(day.solve(data), "47598263")
        self.assertEqual(day.solve(data, moves=10000000, n_cups=1000000), 248009574232)
