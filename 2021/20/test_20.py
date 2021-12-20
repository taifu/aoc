import unittest
import pytest

import day_20 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""

    def test_part_1(self):
        self.assertEqual(day.solve1(self.data), 35)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data), 3351)

    @pytest.mark.slow
    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 5057)
        self.assertEqual(day.solve2(data), 18502)
