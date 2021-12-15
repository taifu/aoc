import unittest
import pytest

import day_15 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

    def test_part_1(self):
        self.assertEqual(40, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(315, day.solve2(self.data))

    @pytest.mark.slow
    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 698)
        self.assertEqual(day.solve2(data), 3022)
