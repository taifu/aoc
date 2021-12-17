import unittest
import pytest

import day_17 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """target area: x=20..30, y=-10..-5
"""

    def test_part_1(self):
        self.assertEqual(day.solve1(self.data), 45)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data), 112)

    @pytest.mark.slow
    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 11781)
        self.assertEqual(day.solve2(data), 4531)
