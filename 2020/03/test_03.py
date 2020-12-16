import unittest

import day_03 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.wood = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    def test_part_1(self):
        self.assertEqual(7, day.solve1(self.wood, 3, 1))

    def test_part_2(self):
        self.assertEqual(336, day.solve2(self.wood))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data, 3, 1), 218)
        self.assertEqual(day.solve2(data), 3847183340)
